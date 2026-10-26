"""Renderer invariants without browser downloads or private resume sources.

Temporary byte fixtures stand in for rendered files; PDF geometry/text objects
are supplied directly. Real Chrome rendering is an additional integration check.
"""

from contextlib import redirect_stderr, redirect_stdout
import importlib.util
import io
import os
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "render-pdf.py"
spec = importlib.util.spec_from_file_location("resume_renderer", SCRIPT)
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)


class Page:
    def __init__(self, width=renderer.A4_WIDTH_PT, height=renderer.A4_HEIGHT_PT,
                 text="Synthetic text 中文", rotation=0):
        self.mediabox = SimpleNamespace(width=width, height=height)
        self.text = text
        self.rotation = rotation

    def get(self, key, default=None):
        return self.rotation if key == "/Rotate" else default

    def extract_text(self):
        return self.text


class RenderPdfTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "合成 input.html"
        self.source.write_text("<p>Synthetic input only.</p>", encoding="utf-8")
        self.output = self.root / "output.pdf"
        self.output.write_bytes(b"existing-output-fixture")

    def run_main(self):
        self.stdout = io.StringIO()
        self.stderr = io.StringIO()
        with redirect_stdout(self.stdout), redirect_stderr(self.stderr):
            return renderer.main([str(self.source), str(self.output)])

    def render_fixture(self, source, target, playwright):
        self.assertEqual(source, self.source.resolve())
        target.write_bytes(b"new-render-fixture")

    def test_paths_preserve_unicode_and_prevent_source_alias(self):
        source, output = renderer._paths([str(self.source)])
        self.assertEqual(source, self.source.resolve())
        self.assertEqual(output, self.source.resolve().with_suffix(".pdf"))
        self.output.unlink()
        os.link(self.source, self.output)
        with self.assertRaisesRegex(ValueError, "different files"):
            renderer._paths([str(self.source), str(self.output)])

    def test_pdf_geometry_page_count_and_text_are_required(self):
        cases = [([Page()], []), ([Page(), Page()], ["exactly 1 page"]),
                 ([Page(text="  ")], ["no extractable text"]),
                 ([Page(width=500)], ["portrait A4"]),
                 ([Page(rotation=90)], ["portrait A4"]),
                 ([Page(width=renderer.A4_HEIGHT_PT, height=renderer.A4_WIDTH_PT,
                        rotation=90)], [])]
        for pages, messages in cases:
            with self.subTest(pages=len(pages), messages=messages), redirect_stdout(io.StringIO()):
                issues = renderer._verify(self.output, lambda _: SimpleNamespace(pages=pages))
                self.assertEqual(bool(issues), bool(messages))
                for message in messages:
                    self.assertTrue(any(message in issue for issue in issues))

    def test_success_replaces_output_only_after_verification(self):
        def verify(path, reader):
            self.assertEqual(path.read_bytes(), b"new-render-fixture")
            self.assertEqual(self.output.read_bytes(), b"existing-output-fixture")
            return []

        with patch.object(renderer, "_load_dependencies", return_value=(object(), object())), \
                patch.object(renderer, "_render", side_effect=self.render_fixture), \
                patch.object(renderer, "_verify", side_effect=verify):
            self.assertEqual(self.run_main(), 0)
        self.assertEqual(self.output.read_bytes(), b"new-render-fixture")
        self.assertEqual(list(self.root.glob("*.review-*.pdf")), [])

    def test_validation_failure_preserves_output_and_diagnostic(self):
        for result in (["expected exactly 1 page"], RuntimeError("invalid PDF fixture")):
            with self.subTest(result=result), \
                    patch.object(renderer, "_load_dependencies", return_value=(object(), object())), \
                    patch.object(renderer, "_render", side_effect=self.render_fixture), \
                    patch.object(renderer, "_verify", **(
                        {"side_effect": result} if isinstance(result, Exception) else {"return_value": result}
                    )):
                self.assertEqual(self.run_main(), 1)
            self.assertEqual(self.output.read_bytes(), b"existing-output-fixture")
            review = Path(next(line.removeprefix("REVIEW: ") for line in self.stdout.getvalue().splitlines()
                               if line.startswith("REVIEW: ")))
            self.assertEqual(review.read_bytes(), b"new-render-fixture")
            review.unlink()

    def test_render_or_replace_failure_cleans_temporary_and_preserves_output(self):
        def failing_render(source, target, playwright):
            self.render_fixture(source, target, playwright)
            raise RuntimeError("synthetic browser failure")

        for render, replace in [(failing_render, None), (self.render_fixture, OSError("synthetic replace failure"))]:
            with self.subTest(replace=replace), \
                    patch.object(renderer, "_load_dependencies", return_value=(object(), object())), \
                    patch.object(renderer, "_render", side_effect=render), \
                    patch.object(renderer, "_verify", return_value=[]), \
                    patch.object(renderer.os, "replace", side_effect=replace):
                self.assertEqual(self.run_main(), 1)
            self.assertEqual(self.output.read_bytes(), b"existing-output-fixture")
            self.assertEqual(list(self.root.glob("*.review-*.pdf")), [])

    def test_missing_dependency_does_not_touch_output(self):
        with patch.object(renderer, "_load_dependencies", side_effect=RuntimeError("missing fixture dependency")):
            self.assertEqual(self.run_main(), 1)
        self.assertEqual(self.output.read_bytes(), b"existing-output-fixture")
        self.assertEqual(list(self.root.glob("*.review-*.pdf")), [])

    def test_loop_input_is_an_argument_error(self):
        self.source.unlink()
        self.source.symlink_to(self.source)
        self.assertEqual(self.run_main(), 2)
        self.assertIn("Argument error:", self.stderr.getvalue())
        self.assertEqual(self.output.read_bytes(), b"existing-output-fixture")


if __name__ == "__main__":
    unittest.main()
