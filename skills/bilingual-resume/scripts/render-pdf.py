#!/usr/bin/env python3
"""Render resume HTML with system Chrome and require one nonblank A4 page.

Usage: python3 render-pdf.py INPUT_HTML [OUTPUT_PDF]

Exit codes: 0 = verified; 1 = dependency, render, or PDF validation failure;
2 = invalid arguments. A rendered PDF that fails validation is kept at a unique
REVIEW path; an existing output is replaced only after validation succeeds.
Playwright and pypdf are imported only when rendering is requested. No browser
is downloaded: Playwright must be able to launch the installed Google Chrome.
"""

import importlib
import os
import sys
import tempfile
from pathlib import Path


A4_WIDTH_PT = 210 / 25.4 * 72
A4_HEIGHT_PT = 297 / 25.4 * 72
SIZE_TOLERANCE_PT = 2.0  # Accommodate Chrome's millimetre-to-point rounding.


def _paths(argv):
    if len(argv) not in (1, 2):
        raise ValueError("usage: python3 render-pdf.py INPUT_HTML [OUTPUT_PDF]")
    src = Path(argv[0]).expanduser().resolve()
    if not src.is_file():
        raise ValueError(f"Input HTML file does not exist: {src}")
    if src.suffix.lower() not in (".html", ".htm"):
        raise ValueError("Input must be an .html or .htm file.")
    out = Path(argv[1]).expanduser().resolve() if len(argv) == 2 else src.with_suffix(".pdf")
    if src == out or (out.exists() and os.path.samefile(src, out)):
        raise ValueError("Input HTML and output PDF must be different files.")
    if out.suffix.lower() != ".pdf":
        raise ValueError("Output filename must end in .pdf.")
    if out.is_dir():
        raise ValueError(f"Output is a directory: {out}")
    if not out.parent.is_dir():
        raise ValueError(f"Output directory does not exist: {out.parent}")
    return src, out


def _load_dependencies():
    try:
        sync_playwright = importlib.import_module("playwright.sync_api").sync_playwright
        pdf_reader = importlib.import_module("pypdf").PdfReader
    except (ImportError, AttributeError) as exc:
        raise RuntimeError(
            "Missing or unusable Python dependency. Install playwright and pypdf "
            "in the Python environment running this script, and install system "
            f"Google Chrome separately. Details: {exc}"
        ) from exc
    return sync_playwright, pdf_reader


def _render(src, temporary_pdf, sync_playwright):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="chrome")
        try:
            page = browser.new_page(viewport={"width": 1280, "height": 1600})
            page.emulate_media(media="print")
            page.goto(src.as_uri(), wait_until="load")
            page.evaluate("() => document.fonts.ready.then(() => undefined)")
            page.pdf(
                path=str(temporary_pdf),
                format="A4",
                prefer_css_page_size=True,
                print_background=True,
            )
        finally:
            browser.close()
    if not temporary_pdf.is_file() or temporary_pdf.stat().st_size == 0:
        raise RuntimeError("Chrome did not produce a nonempty PDF.")


def _verify(path, pdf_reader):
    reader = pdf_reader(str(path))
    count = len(reader.pages)
    print(f"PAGES: {count}")
    issues = []
    if count != 1:
        issues.append(f"expected exactly 1 page; found {count}")
    for index, page in enumerate(reader.pages, 1):
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        if int(page.get("/Rotate", 0) or 0) % 180:
            width, height = height, width
        if not (
            abs(width - A4_WIDTH_PT) <= SIZE_TOLERANCE_PT
            and abs(height - A4_HEIGHT_PT) <= SIZE_TOLERANCE_PT
        ):
            issues.append(f"page {index} is {width:.2f} x {height:.2f} pt; expected portrait A4")
        if not (page.extract_text() or "").strip():
            issues.append(f"page {index} has no extractable text")
    return issues


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    try:
        src, out = _paths(argv)
    except (ValueError, OSError, RuntimeError) as exc:
        print(f"Argument error: {exc}", file=sys.stderr)
        return 2
    try:
        sync_playwright, pdf_reader = _load_dependencies()
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    temporary_pdf = None
    try:
        # Validate before atomic replacement, so a failed render or validation
        # leaves any previous PDF untouched. Keep failed PDFs for inspection.
        with tempfile.NamedTemporaryFile(
            prefix=f"{out.stem}.review-", suffix=".pdf", dir=out.parent, delete=False
        ) as temporary_file:
            temporary_pdf = Path(temporary_file.name)
        _render(src, temporary_pdf, sync_playwright)
        try:
            issues = _verify(temporary_pdf, pdf_reader)
        except Exception as exc:
            issues = [f"could not inspect PDF: {exc}"]
        if issues:
            print("PDF validation failed: " + "; ".join(issues), file=sys.stderr)
            print(f"REVIEW: {temporary_pdf}")
            temporary_pdf = None  # Retain this diagnostic without replacing out.
            return 1
        os.replace(temporary_pdf, out)
        temporary_pdf = None
    except Exception as exc:
        print(f"PDF rendering failed: {exc}", file=sys.stderr)
        return 1
    finally:
        if temporary_pdf is not None:
            try:
                temporary_pdf.unlink(missing_ok=True)
            except OSError as exc:
                print(f"Could not remove temporary PDF {temporary_pdf}: {exc}", file=sys.stderr)

    print(f"OUTPUT: {out}")
    print("VERIFIED: one portrait A4 page with extractable text")
    return 0


if __name__ == "__main__":
    sys.exit(main())
