#!/usr/bin/env python3
"""Read-only structural checks for a generated interview preparation pack.

This is deliberately a small Markdown reader, not a CommonMark implementation.
It checks files, local links, and requirement mappings. It cannot establish the
depth or correctness of prose, successful project execution, or GitHub publication.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
import os
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


JD_FILE = "meta/jd.md"
COVERAGE_FILE = "meta/coverage.md"
ESSENTIAL_FILE = "artifacts/essential.md"
QA_FILE = "artifacts/qa.md"
KB_DIR = "artifacts/kb"
SHOWCASE_DIR = "artifacts/showcase"
REQUIRED_FILES = (
    "README.md", JD_FILE, COVERAGE_FILE, "meta/progress.md",
    ESSENTIAL_FILE, QA_FILE, f"{KB_DIR}/00-roadmap.md",
)
JD_HEADERS = ("ID", "来源类型", "JD 要求/补充能力", "优先级")
COVERAGE_HEADERS = (
    "ID", "类型", "优先级", "要求", "Essential", "KB", "QA", "实践证据/差距",
)
# Normalize display-language labels before applying the same structural rules.
HEADER_ALIASES = {
    "来源类型": "Source type",
    "JD 要求/补充能力": "JD requirement / supplemental capability",
    "优先级": "Priority",
    "类型": "Type",
    "要求": "Requirement",
    "实践证据/差距": "Practice evidence / gaps",
}
KIND_ALIASES = {"explicit": "明确", "inferred": "推断"}
IGNORED_DIRS = {
    ".git", ".hg", ".svn", "node_modules", ".venv", "venv", "env",
    "__pycache__", ".cache", "cache", ".pytest_cache", ".mypy_cache",
    ".ruff_cache", ".tox", ".nox", "site-packages", "vendor",
    "bower_components", "dist", "build", "target", "coverage",
}
REQUIREMENT_ID = re.compile(r"(?:JD|INF)-\d{3}\Z")
PLACEHOLDER = re.compile(r"\{\{[^{}\n]{1,200}\}\}|\[\[TODO\s*:[^\]\n]*\]\]", re.I)
LIMITATION = (
    "Structural success does not establish teaching depth, authentic work, "
    "successful project tests, or GitHub publication; verify these separately."
)


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    markdown_files: int = 0

    @property
    def ok(self) -> bool:
        return not self.errors


@dataclass(frozen=True)
class Link:
    destination: str
    label: str
    line: int


@dataclass(frozen=True)
class TableRow:
    cells: dict[str, str]
    line: int


def _blank(text: str) -> str:
    """Remove content without losing offsets or line numbers."""
    return re.sub(r"[^\n]", " ", text)


def without_fences(text: str) -> str:
    output = []
    opening = None
    for line in text.splitlines(keepends=True):
        if opening:
            output.append(_blank(line))
            if re.match(r"^ {0,3}" + re.escape(opening[0]) +
                        "{" + str(opening[1]) + r",}\s*$", line):
                opening = None
            continue
        match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if match and not (match[1][0] == "`" and "`" in match[2]):
            opening = (match[1][0], len(match[1]))
            output.append(_blank(line))
        else:
            output.append(line)
    return "".join(output)


def without_inline_code(text: str) -> str:
    output = list(text)
    cursor = 0
    for opening in re.finditer(r"`+", text):
        if opening.start() < cursor:
            continue
        token = opening.group()
        end = re.search(r"(?<!`)" + re.escape(token) + r"(?!`)", text[opening.end():])
        if end:
            cursor = opening.end() + end.end()
            output[opening.start():cursor] = _blank(text[opening.start():cursor])
    return "".join(output)


def prose(text: str) -> str:
    return without_inline_code(without_fences(text))


def _unescape(text: str) -> str:
    return re.sub(r"\\([\\`*{}\[\]()#+\-.!_>~| ])", r"\1", text)


def _destination(body: str) -> str:
    body = body.strip()
    if body.startswith("<"):
        end = re.search(r"(?<!\\)>", body)
        return _unescape(body[1:end.start()]) if end else ""
    # Accept ordinary destinations with spaces as well as CommonMark <...>
    # destinations. A trailing Markdown title is not part of the filename.
    body = re.sub(r'''\s+(?:"[^"\n]*"|'[^'\n]*'|\([^()\n]*\))\s*$''', "", body)
    return _unescape(body)


def _reference_key(label: str) -> str:
    return " ".join(_unescape(label).split()).casefold()


def _references(clean: str) -> tuple[dict[str, str], list[tuple[int, int, Link]]]:
    references = {}
    found = []
    pattern = r"^ {0,3}\[([^\]\n]+)\]:[ \t]*(.+)$"
    for match in re.finditer(pattern, clean, re.M):
        if match[1].startswith("^"):  # Footnotes are not file links.
            continue
        destination = _destination(match[2])
        references.setdefault(_reference_key(match[1]), destination)
        found.append((match.start(), match.end(), Link(
            destination, match[1], clean.count("\n", 0, match.start()) + 1,
        )))
    return references, found


def _closing(text: str, start: int, left: str, right: str) -> int | None:
    depth = 1
    cursor = start
    while cursor < len(text):
        char = text[cursor]
        if char == "\\":
            cursor += 2
            continue
        if char == left:
            depth += 1
        elif char == right:
            depth -= 1
            if depth == 0:
                return cursor
        cursor += 1
    return None


def markdown_links(text: str, references: dict[str, str] | None = None) -> list[Link]:
    clean = prose(text)
    own_refs, definitions = _references(clean)
    refs = dict(references or {})
    refs.update(own_refs)
    links = [definition[2] for definition in definitions]
    for start, end, _ in definitions:
        clean = clean[:start] + _blank(clean[start:end]) + clean[end:]
    cursor = 0
    while cursor < len(clean):
        if clean[cursor] == "\\":
            cursor += 2
            continue
        if clean[cursor] != "[":
            cursor += 1
            continue
        end_label = _closing(clean, cursor + 1, "[", "]")
        if end_label is None:
            cursor += 1
            continue
        label = clean[cursor + 1:end_label]
        destination = None
        end = end_label + 1
        if end < len(clean) and clean[end] == "(":
            end_target = _closing(clean, end + 1, "(", ")")
            if end_target is not None:
                destination = _destination(clean[end + 1:end_target])
                end = end_target + 1
        elif end < len(clean) and clean[end] == "[":
            end_ref = _closing(clean, end + 1, "[", "]")
            if end_ref is not None:
                key = clean[end + 1:end_ref] or label
                destination = refs.get(_reference_key(key))
                end = end_ref + 1
        else:
            destination = refs.get(_reference_key(label))
        # A linked image is nested Markdown: [![preview](image.png)](demo.md).
        # Its image destination must be checked as well as the outer link.
        if "[" in label:
            first_line = clean.count("\n", 0, cursor) + 1
            links.extend(Link(link.destination, link.label, first_line + link.line - 1)
                         for link in markdown_links(label, refs))
        if destination is not None:
            links.append(Link(destination, label, clean.count("\n", 0, cursor) + 1))
        cursor = end
    return links


def relative_target(destination: str) -> str | None:
    """Decode only a URL's path, after separating its query and fragment."""
    try:
        parsed = urlsplit(destination)
    except ValueError:
        # Malformed local URLs should fail existence checking, not crash.
        return destination if not re.match(r"[A-Za-z][A-Za-z0-9+.-]*:", destination) else None
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    target = unquote(parsed.path)
    if Path(target).is_absolute() or re.match(r"^[A-Za-z]:[/\\]", target):
        return None
    return target


def _table_cells(line: str) -> list[str]:
    cells = []
    current = []
    escaped = False
    for char in line.strip():
        if char == "|" and not escaped:
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(char)
        if char == "\\":
            escaped = not escaped
        else:
            escaped = False
    cells.append("".join(current).strip())
    if line.lstrip().startswith("|"):
        cells.pop(0)
    if line.rstrip().endswith("|") and len(cells) > 1:
        cells.pop()
    return cells


def _is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def _canonical_header(value: str, headers: tuple[str, ...]) -> str:
    key = " ".join(value.split()).casefold()
    for canonical in headers:
        names = (canonical, HEADER_ALIASES.get(canonical, canonical))
        if any(key == " ".join(name.split()).casefold() for name in names):
            return canonical
    return value


def table_rows(text: str, headers: tuple[str, ...], label: str, report: Report) -> list[TableRow]:
    lines = without_fences(text).splitlines()
    rows = []
    found = False
    cursor = 0
    while cursor + 1 < len(lines):
        cells = [_canonical_header(value, headers) for value in _table_cells(lines[cursor])]
        separator = _table_cells(lines[cursor + 1])
        if not _is_separator(separator) or not set(headers).issubset(cells) or cells[0] != "ID":
            cursor += 1
            continue
        found = True
        if len(separator) != len(cells) or len(set(cells)) != len(cells):
            report.errors.append(f"{label}:{cursor + 1}: 表格列定义不一致或重复。")
        header_cells = cells
        cursor += 2
        while cursor < len(lines) and "|" in lines[cursor] and lines[cursor].strip():
            values = _table_cells(lines[cursor])
            if len(values) != len(header_cells):
                report.errors.append(f"{label}:{cursor + 1}: 表格列数应为 {len(header_cells)}。")
            else:
                rows.append(TableRow(dict(zip(header_cells, values)), cursor + 1))
            cursor += 1
    if not found:
        report.errors.append(f"{label}: 缺少要求表格，列名应包含：{'、'.join(headers)}，且 ID 为首列。")
    elif not rows:
        report.errors.append(f"{label}: 要求表格没有数据行。")
    return rows


def _ids(rows: list[TableRow], label: str, report: Report) -> set[str]:
    seen = set()
    for row in rows:
        identifier = row.cells["ID"].strip().strip("`")
        if not REQUIREMENT_ID.fullmatch(identifier):
            report.errors.append(f"{label}:{row.line}: ID 必须独立写为 JD-001 或 INF-001 格式。")
        elif identifier in seen:
            report.errors.append(f"{label}:{row.line}: 重复 ID：{identifier}。")
        else:
            seen.add(identifier)
    return seen


def _requirement_metadata(
    rows: list[TableRow], label: str, report: Report, *,
    kind_column: str, description_column: str,
) -> dict[str, tuple[str, str]]:
    metadata = {}
    for row in rows:
        identifier = row.cells["ID"].strip().strip("`")
        kind = row.cells[kind_column].strip().strip("`*")
        kind = KIND_ALIASES.get(kind.casefold(), kind)
        priority = row.cells["优先级"].strip().strip("`*")
        description = row.cells[description_column].strip()
        location = f"{label}:{row.line}: {identifier}"
        if kind not in {"明确", "推断"}:
            report.errors.append(f"{location} 的 {kind_column} 必须为“明确”或“推断”。")
        elif REQUIREMENT_ID.fullmatch(identifier):
            expected_kind = "明确" if identifier.startswith("JD-") else "推断"
            if kind != expected_kind:
                report.errors.append(f"{location} 的类型应为“{expected_kind}”，与 ID 前缀一致。")
        if priority not in {"P0", "P1", "P2"}:
            report.errors.append(f"{location} 的优先级必须为 P0、P1 或 P2。")
        if description in {"", "-", "—", "–", "N/A", "n/a"}:
            report.errors.append(f"{location} 的 {description_column} 不能为空或仅为占位符。")
        metadata.setdefault(identifier, (kind, priority))
    return metadata


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _nonlearning(value: str) -> bool:
    return bool(re.search(r"(?:非学习项|Non-learning item)\s*[:：]\s*\S", value, re.I))


def _coverage(rows: list[TableRow], text: str, root: Path, report: Report) -> None:
    references, _ = _references(prose(text))
    coverage_path = root / COVERAGE_FILE
    for row in rows:
        identifier = row.cells["ID"]
        for column in ("Essential", "KB", "QA", "实践证据/差距"):
            value = row.cells[column].strip()
            label = f"{COVERAGE_FILE}:{row.line}: {identifier} 的 {column}"
            if value in {"", "-", "—", "–", "N/A", "n/a"}:
                report.errors.append(f"{label} 不能为空或仅为占位符。")
                continue
            links = markdown_links(value, references)
            if column == "实践证据/差距":
                explicit_status = re.search(
                    r"(?:已省略|差距|未验证|待完成|Omitted|Gap|Unverified|Pending)\s*[:：]\s*\S",
                    value, re.I,
                )
                evidence_links = [link for link in links if relative_target(link.destination) is not None]
                has_evidence = any(
                    re.search(r"showcase|exercise|practice|\blabs?\b|练习|实践|项目|演示",
                              link.label + " " + link.destination, re.I)
                    for link in evidence_links
                )
                if not explicit_status and not has_evidence:
                    report.errors.append(f"{label} 应链接到项目/练习，或明确填写已省略：原因、差距：原因、未验证：原因、待完成：原因。")
                continue
            if _nonlearning(value):
                continue
            if column == "Essential" and re.fullmatch(r"(?:非核心|Non-core)\s*[:：]\s*\S.*", value, re.I):
                continue
            expected = {"Essential": ESSENTIAL_FILE, "KB": KB_DIR, "QA": QA_FILE}[column]
            expected_path = (root / expected).resolve()
            matched = False
            for link in links:
                target = relative_target(link.destination)
                if target is None:
                    continue
                try:
                    resolved = (coverage_path.parent / target).resolve()
                except (OSError, ValueError, RuntimeError):
                    continue  # The global link check reports invalid targets.
                if resolved == expected_path or (column == "KB" and _is_within(resolved, expected_path)):
                    matched = True
                    break
            if not matched:
                exemption = "；支撑或扩展要求可填写“非核心：原因”" if column == "Essential" else ""
                report.errors.append(f"{label} 应链接到 {expected}，非教学要求可填写“非学习项：原因”{exemption}。")


def owned_files(root: Path):
    for current, directories, files in os.walk(root, followlinks=False):
        directories[:] = sorted(
            name for name in directories
            if name not in IGNORED_DIRS and not (Path(current) / name).is_symlink()
        )
        for name in sorted(files):
            yield Path(current) / name


def _has_body(text: str) -> bool:
    lines = prose(re.sub(r"<!--.*?-->", "", text, flags=re.S)).splitlines()
    for index, line in enumerate(lines):
        value = line.strip()
        if not value or re.match(r"^#{1,6}(?:\s|$)", value):
            continue
        if re.fullmatch(r"(?:[-*_]\s*){3,}|[=-]{3,}", value):
            continue
        if index + 1 < len(lines) and re.fullmatch(r"[=-]{3,}", lines[index + 1].strip()):
            continue  # Setext heading.
        cells = _table_cells(line)
        if _is_separator(cells):
            continue
        if index + 1 < len(lines) and _is_separator(_table_cells(lines[index + 1])):
            continue  # Table header; a data row does count as body.
        if re.match(r"^\[[^\]]+\]:\s", value):
            continue
        if value not in {"-", "*", ">", "- [ ]", "- [x]"}:
            return True
    return False


def _project_file(path: Path, portfolio: bool = False) -> bool:
    try:
        nonempty = path.stat().st_size > 0
    except OSError:
        return False
    if (not nonempty or path.name.startswith(".") or path.stem.casefold() == "readme"
            or path.name.casefold() == "readme"
            or re.match(r"^(?:LICENSE|LICENCE|NOTICE|AUTHORS|COPYING)(?:[._-]|$)", path.name, re.I)):
        return False
    if portfolio:
        return True
    return path.suffix.lower() not in {
        ".md", ".rst", ".txt", ".adoc", ".pdf", ".png", ".jpg", ".jpeg", ".svg", ".gif", ".webp", ".ico",
    }


def validate_pack(directory: str | Path, no_project: bool = False, portfolio: bool = False) -> Report:
    if no_project and portfolio:
        raise ValueError("no_project 与 portfolio 不能同时启用。")
    root = Path(directory).expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"输入路径不是可读取的准备包目录：{root}")
    report = Report()
    for name in REQUIRED_FILES:
        if not (root / name).is_file():
            report.errors.append(f"缺少必需文件：{name}。")
    files = list(owned_files(root))
    kb_docs = [path for path in files if _is_within(path, root / KB_DIR) and
               path.suffix.lower() == ".md" and path != root / KB_DIR / "00-roadmap.md"]
    if not kb_docs:
        report.errors.append(f"{KB_DIR}/ 至少需要一篇 00-roadmap.md 以外的知识正文。")
    if not no_project:
        if not (root / SHOWCASE_DIR / "README.md").is_file():
            report.errors.append(f"项目已启用，缺少 {SHOWCASE_DIR}/README.md。")
        project_files = [path for path in files if _is_within(path, root / SHOWCASE_DIR) and _project_file(path, portfolio=portfolio)]
        if not project_files:
            if portfolio:
                report.errors.append(f"作品集已启用，{SHOWCASE_DIR}/ 至少需要一个 README 之外的非空作品文件，许可证或隐藏文件不算作品。")
            else:
                report.errors.append(f"项目已启用，{SHOWCASE_DIR}/ 至少需要一个非空的实际项目文件，不能只有目录或说明文档。")
    documents = {}
    for path in files:
        if path.suffix.lower() != ".md":
            continue
        label = path.relative_to(root).as_posix()
        report.markdown_files += 1
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            report.errors.append(f"{label}: 无法读取 UTF-8 Markdown：{error}。")
            continue
        documents[label] = text
        if not _has_body(text):
            report.errors.append(f"{label}: 未检测到正文（仅标题、表头、代码示例或空白不足以说明内容）。")
        for match in PLACEHOLDER.finditer(prose(text)):
            line = text.count("\n", 0, match.start()) + 1
            report.warnings.append(f"{label}:{line}: 疑似未替换模板标记 {match.group()!r}，请人工确认；代码中的标记不参与检查。")
        seen_links = set()
        for link in markdown_links(text):
            target = relative_target(link.destination)
            if target is None:
                continue
            key = (link.line, target)
            if key in seen_links:
                continue
            seen_links.add(key)
            try:
                exists = (path.parent / target).exists()
            except (OSError, ValueError, RuntimeError):
                exists = False
            if not exists:
                report.errors.append(f"{label}:{link.line}: 本地链接目标不存在：{link.destination}。")
    if JD_FILE in documents and COVERAGE_FILE in documents:
        jd_rows = table_rows(documents[JD_FILE], JD_HEADERS, JD_FILE, report)
        coverage_rows = table_rows(documents[COVERAGE_FILE], COVERAGE_HEADERS, COVERAGE_FILE, report)
        jd_ids = _ids(jd_rows, JD_FILE, report)
        coverage_ids = _ids(coverage_rows, COVERAGE_FILE, report)
        jd_metadata = _requirement_metadata(
            jd_rows, JD_FILE, report, kind_column="来源类型", description_column="JD 要求/补充能力",
        )
        coverage_metadata = _requirement_metadata(
            coverage_rows, COVERAGE_FILE, report, kind_column="类型", description_column="要求",
        )
        missing = sorted(jd_ids - coverage_ids)
        extra = sorted(coverage_ids - jd_ids)
        if missing:
            report.errors.append(f"{COVERAGE_FILE} 缺少 JD 要求 ID：{', '.join(missing)}。")
        if extra:
            report.errors.append(f"{COVERAGE_FILE} 存在 {JD_FILE} 未登记的 ID：{', '.join(extra)}。")
        for identifier in sorted(jd_ids & coverage_ids):
            if jd_metadata[identifier] != coverage_metadata[identifier]:
                report.errors.append(f"{COVERAGE_FILE} 的 {identifier} 类型和优先级应与 {JD_FILE} 一致。")
        _coverage(coverage_rows, documents[COVERAGE_FILE], root, report)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pack_dir", metavar="PACK_DIR", help="generated interview preparation pack directory")
    project_options = parser.add_mutually_exclusive_group()
    project_options.add_argument("--no-project", action="store_true", help="project explicitly disabled by the user; still check residual links")
    project_options.add_argument("--portfolio", action="store_true", help="allow nonempty reports or images beyond README for a nontechnical portfolio; authenticity is not verified")
    args = parser.parse_args(argv)
    try:
        report = validate_pack(args.pack_dir, no_project=args.no_project, portfolio=args.portfolio)
    except (ValueError, OSError) as error:
        parser.error(str(error))
    for error in report.errors:
        print(f"ERROR: {error}")
    for warning in report.warnings:
        print(f"WARNING: {warning}")
    if report.ok:
        print(f"Structural checks passed: {report.markdown_files} Markdown files, {len(report.warnings)} warnings.")
    else:
        print(f"Structural checks failed: {len(report.errors)} errors, {len(report.warnings)} warnings.")
    print(LIMITATION)
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
