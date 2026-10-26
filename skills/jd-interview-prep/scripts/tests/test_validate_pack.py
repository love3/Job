"""Temporary-pack regression tests; no generated preparation pack is modified."""

from __future__ import annotations

import hashlib
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import validate_pack as validator


def write(root: Path, name: str, text: str) -> None:
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_pack(root: Path, *, project: bool = True) -> None:
    """Create structural fixtures, not example teaching material or a real JD."""
    write(root, "README.md", "入口正文：[学习](artifacts/essential.md)、[进度](meta/progress.md)。\n")
    write(root, "meta/progress.md", "临时测试的运行状态正文。\n")
    write(root, "meta/jd.md", """临时测试的岗位来源说明。

| ID | 来源类型 | JD 要求/补充能力 | 优先级 |
| --- | --- | --- | --- |
| JD-001 | 明确 | 测试要求 | P0 |
| INF-001 | 推断 | 测试先修 | P1 |
""")
    evidence = (
        "[项目验证](../artifacts/showcase/README.md)" if project
        else "已省略：用户取消项目；[练习](../artifacts/kb/01-topic.md)"
    )
    write(root, "meta/coverage.md", """覆盖正文。

| ID | 类型 | 优先级 | 要求 | Essential | KB | QA | 实践证据/差距 |
| --- | --- | --- | --- | --- | --- | --- | --- |
""" + "".join(
        f"| {identifier} | {kind} | {priority} | 测试要求 | "
        "[本质](../artifacts/essential.md) | [教学](../artifacts/kb/01-topic.md) | "
        f"[答案](../artifacts/qa.md) | {evidence} |\n"
        for identifier, kind, priority in (("JD-001", "明确", "P0"), ("INF-001", "推断", "P1"))
    ))
    write(root, "artifacts/essential.md", "学习正文：[问答](qa.md)、[岗位](../meta/jd.md)。\n")
    write(root, "artifacts/qa.md", "回答正文：[教学](kb/01-topic.md)。\n")
    write(root, "artifacts/kb/00-roadmap.md", "学习路线正文：[教学](01-topic.md)。\n")
    write(root, "artifacts/kb/01-topic.md", "练习与答案正文：[覆盖](../../meta/coverage.md)。\n")
    if project:
        write(root, "artifacts/showcase/README.md", "临时项目运行与验证说明正文。\n")
        write(root, "artifacts/showcase/src/main.py", "print('temporary fixture')\n")


def make_english_pack(root: Path, *, project: bool = True) -> None:
    """Exercise the English public format independently of parser aliases."""
    make_pack(root, project=project)
    write(root, "README.md", "Pack entry: [study](artifacts/essential.md), [progress](meta/progress.md).\n")
    write(root, "meta/progress.md", "Current status of an isolated structural fixture.\n")
    write(root, "meta/jd.md", """The role source for an isolated fixture.

| ID | Source type | JD requirement / supplemental capability | Priority |
| --- | --- | --- | --- |
| JD-001 | Explicit | Test requirement | P0 |
| INF-001 | Inferred | Test prerequisite | P1 |
""")
    evidence = (
        "[Showcase evidence](../artifacts/showcase/README.md)" if project
        else "Omitted: project disabled by the user; [exercise](../artifacts/kb/01-topic.md)"
    )
    write(root, "meta/coverage.md", """Requirement mapping for an isolated fixture.

| ID | Type | Priority | Requirement | Essential | KB | QA | Practice evidence / gaps |
| --- | --- | --- | --- | --- | --- | --- | --- |
""" + "".join(
        f"| {identifier} | {kind} | {priority} | Test requirement | "
        "[Core](../artifacts/essential.md) | [Lesson](../artifacts/kb/01-topic.md) | "
        f"[Answer](../artifacts/qa.md) | {evidence} |\n"
        for identifier, kind, priority in (("JD-001", "Explicit", "P0"), ("INF-001", "Inferred", "P1"))
    ))
    write(root, "artifacts/essential.md", "Core learning: [answers](qa.md), [role](../meta/jd.md).\n")
    write(root, "artifacts/qa.md", "Interview answers: [lesson](kb/01-topic.md).\n")
    write(root, "artifacts/kb/00-roadmap.md", "Learning route: [lesson](01-topic.md).\n")
    write(root, "artifacts/kb/01-topic.md", "An exercise and its answer: [mapping](../../meta/coverage.md).\n")
    if project:
        write(root, "artifacts/showcase/README.md", "Isolated project execution and verification notes.\n")


def change(root: Path, name: str, old: str, new: str) -> None:
    path = root / name
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise AssertionError(f"fixture text not found: {old!r}")
    path.write_text(text.replace(old, new), encoding="utf-8")


def snapshot(root: Path) -> dict[str, tuple[int, str]]:
    return {
        path.relative_to(root).as_posix(): (path.stat().st_mtime_ns, hashlib.sha256(path.read_bytes()).hexdigest())
        for path in root.rglob("*") if path.is_file()
    }


class ValidatePackTests(unittest.TestCase):
    def assert_valid(self, report: validator.Report) -> None:
        self.assertTrue(report.ok, "\n".join(report.errors))

    def assert_error(self, report: validator.Report, text: str) -> None:
        self.assertFalse(report.ok)
        self.assertTrue(any(text in error for error in report.errors), report.errors)

    def test_complete_pack_and_cross_layer_links(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            make_pack(root)
            self.assert_valid(validator.validate_pack(root))

    def test_english_pack_and_case_insensitive_kinds(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            make_english_pack(root)
            change(root, "meta/jd.md", "Explicit", "eXpLiCiT")
            change(root, "meta/jd.md", "Inferred", "INFERRED")
            change(root, "meta/coverage.md", "Explicit", "explicit")
            change(root, "meta/coverage.md", "Inferred", "inferred")
            self.assert_valid(validator.validate_pack(root))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            make_english_pack(root, project=False)
            self.assert_valid(validator.validate_pack(root, no_project=True))

    def test_mixed_language_headers_and_kinds_are_equivalent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            make_english_pack(root)
            change(root, "meta/jd.md", "JD requirement / supplemental capability", "JD 要求/补充能力")
            change(root, "meta/jd.md", "Priority", "优先级")
            change(root, "meta/jd.md", "Explicit", "明确")
            change(root, "meta/coverage.md", "| Type |", "| 类型 |")
            change(root, "meta/coverage.md", "| Requirement |", "| 要求 |")
            change(root, "meta/coverage.md", "Inferred", "推断")
            self.assert_valid(validator.validate_pack(root))

    def test_english_coverage_explanations(self) -> None:
        cases = (
            ("[Core](../artifacts/essential.md)", "Non-core: a supporting topic covered in KB"),
            ("[Core](../artifacts/essential.md)", "non-CORE: supporting knowledge"),
            ("[Core](../artifacts/essential.md)", "Non-learning item: employment tenure is a factual gap"),
            ("[Lesson](../artifacts/kb/01-topic.md)", "Non-learning item: tenure cannot be taught"),
            ("[Answer](../artifacts/qa.md)", "Non-learning item: factual employment requirement"),
            ("[Showcase evidence](../artifacts/showcase/README.md)", "Gap: experience not supplied"),
            ("[Showcase evidence](../artifacts/showcase/README.md)", "Pending: exercise has not been completed"),
            ("[Showcase evidence](../artifacts/showcase/README.md)", "Unverified: no execution environment available"),
            ("[Showcase evidence](../artifacts/showcase/README.md)", "Omitted: project disabled by the user"),
        )
        for old, new in cases:
            with self.subTest(explanation=new), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                make_english_pack(root)
                change(root, "meta/coverage.md", old, new)
                self.assert_valid(validator.validate_pack(root))

    def test_english_markers_require_reasons_and_correct_columns(self) -> None:
        cases = (
            ("[Core](../artifacts/essential.md)", "Non-core:   ", "Essential"),
            ("[Core](../artifacts/essential.md)", "Non-learning item:", "Essential"),
            ("[Lesson](../artifacts/kb/01-topic.md)", "Non-learning item:   ", "KB"),
            ("[Answer](../artifacts/qa.md)", "Non-learning item:", "QA"),
            ("[Lesson](../artifacts/kb/01-topic.md)", "Non-core: supporting knowledge", "KB"),
            ("[Answer](../artifacts/qa.md)", "Non-core: supporting knowledge", "QA"),
        ) + tuple(
            ("[Showcase evidence](../artifacts/showcase/README.md)", f"{marker}:   ", "实践证据/差距")
            for marker in ("Gap", "Pending", "Unverified", "Omitted")
        )
        for old, new, column in cases:
            with self.subTest(value=new, column=column), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                make_english_pack(root)
                change(root, "meta/coverage.md", old, new)
                self.assert_error(validator.validate_pack(root), f"的 {column} 应链接到")

    def test_english_metadata_still_requires_consistent_types_and_priorities(self) -> None:
        cases = (
            ("jd", "| JD-001 | Explicit |", "| JD-001 | Unknown |", "来源类型 必须"),
            ("coverage", "| INF-001 | Inferred |", "| INF-001 | Explicit |", "类型应为“推断”"),
            ("coverage", "| P0 |", "| P3 |", "优先级必须为 P0、P1 或 P2"),
            ("coverage", "| P0 |", "| P1 |", "类型和优先级应与"),
        )
        for document, old, new, message in cases:
            with self.subTest(case=message), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                make_english_pack(root)
                change(root, f"meta/{document}.md", old, new)
                self.assert_error(validator.validate_pack(root), message)

    def test_english_mapping_still_rejects_existing_wrong_targets(self) -> None:
        for column, target in (("Essential", "essential.md"), ("KB", "kb/01-topic.md"), ("QA", "qa.md")):
            with self.subTest(column=column), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                make_english_pack(root)
                write(root, f"meta/decoys/{target}", "An existing file outside the correct deliverable location.\n")
                change(root, "meta/coverage.md", f"../artifacts/{target}", f"decoys/{target}")
                self.assert_error(validator.validate_pack(root), f"的 {column} 应链接到")

    def test_mixed_header_aliases_cannot_duplicate_a_column(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            make_english_pack(root)
            path = root / "meta/coverage.md"
            text = path.read_text(encoding="utf-8")
            text = text.replace("| Type | Priority |", "| Type | 类型 | Priority |")
            text = text.replace("| --- | --- |", "| --- | --- | --- |", 1)
            text = text.replace("| Explicit | P0 |", "| Explicit | 明确 | P0 |")
            text = text.replace("| Inferred | P1 |", "| Inferred | 推断 | P1 |")
            path.write_text(text, encoding="utf-8")
            self.assert_error(validator.validate_pack(root), "表格列定义不一致或重复")

    def test_validator_is_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            make_pack(root)
            write(root, "artifacts/showcase/.git/config", "[core]\nrepositoryformatversion = 0\n")
            before = snapshot(root)
            self.assert_valid(validator.validate_pack(root))
            self.assertEqual(before, snapshot(root))
            # Failing checks must also leave all original files unchanged.
            change(root, "meta/coverage.md", "| P0 |", "| P9 |")
            before = snapshot(root)
            self.assertFalse(validator.validate_pack(root).ok)
            self.assertEqual(before, snapshot(root))

    def test_existing_wrong_targets_do_not_satisfy_coverage(self) -> None:
        for column, target in (("Essential", "essential.md"), ("KB", "kb/01-topic.md"), ("QA", "qa.md")):
            with self.subTest(column=column), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                make_pack(root)
                write(root, f"meta/decoys/{target}", "存在但不是对应交付物的正文。\n")
                change(root, "meta/coverage.md", f"../artifacts/{target}", f"decoys/{target}")
                report = validator.validate_pack(root)
                self.assert_error(report, f"的 {column} 应链接到")
                self.assertFalse(any("目标不存在" in error for error in report.errors), report.errors)

    def test_coverage_is_relative_to_meta_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            make_pack(root)
            # This link exists from meta/, but only ../artifacts/essential.md
            # identifies the deliverable. Resolving from pack root is incorrect.
            write(root, "meta/artifacts/essential.md", "错误位置的真实文件。\n")
            change(root, "meta/coverage.md", "../artifacts/essential.md", "artifacts/essential.md")
            self.assert_error(validator.validate_pack(root), "的 Essential 应链接到 artifacts/essential.md")

    def test_essential_allows_noncore_reason(self) -> None:
        for value in ("非核心：支撑知识在 KB 和 QA 中展开", "非核心: 扩展知识不属于岗位核心主线"):
            with self.subTest(value=value), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                make_pack(root)
                change(root, "meta/coverage.md", "[本质](../artifacts/essential.md)", value)
                self.assert_valid(validator.validate_pack(root))

    def test_noncore_requires_reason_and_only_exempts_essential(self) -> None:
        cases = (
            ("[本质](../artifacts/essential.md)", "非核心：", "Essential"),
            ("[本质](../artifacts/essential.md)", "非核心:   ", "Essential"),
            ("[教学](../artifacts/kb/01-topic.md)", "非核心：支撑知识", "KB"),
            ("[答案](../artifacts/qa.md)", "非核心：扩展知识", "QA"),
        )
        for old, new, column in cases:
            with self.subTest(column=column, value=new), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                make_pack(root)
                change(root, "meta/coverage.md", old, new)
                self.assert_error(validator.validate_pack(root), f"的 {column} 应链接到")

    def test_noncore_preserves_other_coverage_and_link_checks(self) -> None:
        cases = (
            ("[教学](../artifacts/kb/01-topic.md)", "只有文字，没有教学链接", "的 KB 应链接到"),
            ("[答案](../artifacts/qa.md)", "只有文字，没有答案链接", "的 QA 应链接到"),
            ("[项目验证](../artifacts/showcase/README.md)", "只有文字，没有实践或差距", "的 实践证据/差距 应链接到"),
            ("| P0 |", "| P1 |", "类型和优先级应与"),
        )
        for old, new, message in cases:
            with self.subTest(check=message), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                make_pack(root)
                change(root, "meta/coverage.md", "[本质](../artifacts/essential.md)", "非核心：支撑知识")
                change(root, "meta/coverage.md", old, new)
                self.assert_error(validator.validate_pack(root), message)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            make_pack(root)
            change(root, "meta/coverage.md", "[本质](../artifacts/essential.md)",
                   "非核心：支撑知识，见[说明](missing.md)")
            self.assert_error(validator.validate_pack(root), "本地链接目标不存在：missing.md")

    def test_broken_cross_layer_link_has_source_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            make_pack(root)
            change(root, "artifacts/essential.md", "../meta/jd.md", "../meta/missing.md")
            self.assert_error(validator.validate_pack(root), "artifacts/essential.md:1: 本地链接目标不存在")

    def test_requirement_validation(self) -> None:
        cases = (
            ("jd", "JD-001", "JD-01", "ID 必须独立写为"),
            ("coverage", "| INF-001 | 推断 |", "| INF-001 | 明确 |", "类型应为“推断”"),
            ("jd", "| JD-001 | 明确 |", "| JD-001 | 未知 |", "来源类型 必须"),
            ("coverage", "| P0 |", "| P3 |", "优先级必须为 P0、P1 或 P2"),
            ("coverage", "| P0 |", "| P1 |", "类型和优先级应与"),
            ("coverage", "JD-001", "JD-999", "缺少 JD 要求 ID：JD-001"),
            ("coverage", "INF-001", "JD-999", "未登记的 ID：JD-999"),
            ("jd", "INF-001", "JD-001", "重复 ID：JD-001"),
        )
        for document, old, new, message in cases:
            with self.subTest(case=message), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                make_pack(root)
                change(root, f"meta/{document}.md", old, new)
                self.assert_error(validator.validate_pack(root), message)

    def test_required_documents_must_exist_at_specified_paths(self) -> None:
        for name in ("meta/jd.md", "meta/coverage.md", "meta/progress.md", "artifacts/essential.md", "artifacts/qa.md"):
            with self.subTest(file=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                make_pack(root)
                (root / name).unlink()
                self.assert_error(validator.validate_pack(root), f"缺少必需文件：{name}")

    def test_markdown_requires_body(self) -> None:
        for name in ("artifacts/essential.md", "artifacts/qa.md", "artifacts/kb/01-topic.md"):
            with self.subTest(file=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                make_pack(root)
                write(root, name, "# 仅标题\n\n```text\n代码块不是教学正文\n```\n")
                self.assert_error(validator.validate_pack(root), f"{name}: 未检测到正文")

    def test_no_project_and_residual_links(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            make_pack(root, project=False)
            self.assert_valid(validator.validate_pack(root, no_project=True))
            self.assert_error(validator.validate_pack(root), "缺少 artifacts/showcase/README.md")
            write(root, "artifacts/qa.md", "残留链接：[项目](showcase/README.md)。\n")
            self.assert_error(validator.validate_pack(root, no_project=True), "本地链接目标不存在")

    def test_project_requires_actual_non_document_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            make_pack(root)
            (root / "artifacts/showcase/src/main.py").unlink()
            write(root, "artifacts/showcase/docs/design.md", "设计文档正文。\n")
            self.assert_error(validator.validate_pack(root), "实际项目文件")

    def test_portfolio_accepts_report_but_not_license_or_hidden_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            make_pack(root)
            (root / "artifacts/showcase/src/main.py").unlink()
            write(root, "artifacts/showcase/LICENSE", "Temporary license.\n")
            write(root, "artifacts/showcase/.hidden", "Hidden fixture.\n")
            self.assert_error(validator.validate_pack(root, portfolio=True), "非空作品文件")
            write(root, "artifacts/showcase/report.pdf", "Temporary report bytes.\n")
            self.assert_valid(validator.validate_pack(root, portfolio=True))
            self.assert_error(validator.validate_pack(root), "实际项目文件")

    def test_ignored_directories_are_not_read_or_counted_as_implementation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            make_pack(root)
            for ignored in (".git", "node_modules", "dist", ".pytest_cache"):
                write(root, f"artifacts/showcase/{ignored}/broken.md", "[不存在](missing.md)\n")
                write(root, f"artifacts/showcase/{ignored}/generated.js", "ignored();\n")
                write(root, f"artifacts/kb/{ignored}/generated.md", "缓存正文。\n")
            self.assert_valid(validator.validate_pack(root))
            (root / "artifacts/showcase/src/main.py").unlink()
            self.assert_error(validator.validate_pack(root), "实际项目文件")
            (root / "artifacts/kb/01-topic.md").unlink()
            self.assert_error(validator.validate_pack(root), "至少需要一篇 00-roadmap.md 以外")

    def test_project_modes_are_mutually_exclusive(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "不能同时启用"):
                validator.validate_pack(directory, no_project=True, portfolio=True)


if __name__ == "__main__":
    unittest.main()
