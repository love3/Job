"""Behavior tests for the optional, local YAML preferences interface."""

from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


MODULE_PATH = Path(__file__).resolve().parents[1] / "validate_preferences.py"
SPEC = importlib.util.spec_from_file_location("validate_preferences", MODULE_PATH)
preferences = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(preferences)


@unittest.skipIf(preferences.yaml is None, "Install requirements-dev.txt first")
class PreferencesTests(unittest.TestCase):
    def load(self, text: str) -> dict:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "preferences.yaml"
            path.write_text(text, encoding="utf-8")
            return preferences.load_preferences(path)

    def assert_invalid(self, text: str, category: str) -> None:
        with self.assertRaisesRegex(ValueError, category):
            self.load(text)

    def test_empty_and_partial_configuration(self) -> None:
        self.assertEqual(self.load(""), {})
        self.assertEqual(self.load("{}\n"), {})
        self.assertEqual(self.load("language: zh-CN\n"), {"language": "zh-CN"})
        self.assertEqual(self.load("github: {}\n"), {"github": {}})

    def test_example_validates_with_public_defaults(self) -> None:
        path = MODULE_PATH.parents[1] / "config/preferences.example.yaml"
        data = preferences.load_preferences(path)
        self.assertEqual(data["language"], "auto")
        self.assertEqual(data["github"], {})
        self.assertEqual(data["showcase"]["publish"], "local")
        self.assertEqual(data["showcase"]["frontend_policy"], "prefer_jd")

    def test_missing_optional_file_does_not_load_example(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            script = Path(directory) / "scripts/validate_preferences.py"
            example = Path(directory) / "config/preferences.example.yaml"
            example.parent.mkdir()
            example.write_text("not valid: [\n", encoding="utf-8")
            with patch.object(preferences, "__file__", str(script)), redirect_stdout(io.StringIO()):
                self.assertEqual(preferences.main([]), 0)

    def test_missing_explicit_file_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as directory, redirect_stderr(io.StringIO()):
            self.assertEqual(preferences.main([str(Path(directory) / "missing.yaml")]), 1)

    def test_paths_are_not_opened_or_required_to_exist(self) -> None:
        data = self.load("""resume:
  base_en: nonexistent/private/base.html
  base_zh: nonexistent/private/中文.html
  references: [not-present.pdf]
  primary_language: en
""")
        self.assertEqual(data["resume"]["base_en"], "nonexistent/private/base.html")

    def test_real_booleans_and_quoted_booleans_are_distinct(self) -> None:
        data = self.load("showcase: {enabled: true, pages: false}\n")
        self.assertIs(data["showcase"]["enabled"], True)
        self.assertIs(data["showcase"]["pages"], False)
        for value in ['"false"', "0", "null", "yes", "on"]:
            with self.subTest(value=value):
                self.assert_invalid(f"showcase: {{pages: {value}}}\n", "expected a boolean")

    def test_string_and_language_fields(self) -> None:
        for tag in ["auto", "zh-CN", "en", "pt-BR"]:
            self.assertEqual(self.load(f"language: {tag}\n")["language"], tag)
        self.assertEqual(self.load("github: {owner: on}\n")["github"]["owner"], "on")
        self.assert_invalid("language: 'not a language'\n", "language tag")
        for text in ["github: {owner: ''}", "resume: {base_en: '  '}", "showcase: {frontend: 3}"]:
            with self.subTest(text=text):
                self.assert_invalid(text, "nonempty string")

    def test_options_and_lists(self) -> None:
        data = self.load("""showcase:
  frontend: svelte
  frontend_policy: prefer_config
  publish: private
  notes:
    - Prefer this framework even when the JD uses another one.
resume:
  enabled: false
  notes: [保留明确要求的内容]
""")
        self.assertEqual(data["showcase"]["frontend"], "svelte")
        self.assertEqual(data["resume"]["notes"], ["保留明确要求的内容"])
        for text in ["showcase: {publish: everyone}", "showcase: {frontend_policy: magic}", "resume: {primary_language: fr}"]:
            with self.subTest(text=text):
                self.assert_invalid(text, "unsupported option")
        for text in ["showcase: {notes: sentence}", "resume: {references: [3]}", "resume: {notes: ['']}"]:
            with self.subTest(text=text):
                self.assert_invalid(text, "strings|string")

    def test_unknown_fields_duplicate_keys_and_shapes(self) -> None:
        for text in ["other: true", "showcase: {other: true}", "github: {token: do-not-print}"]:
            with self.subTest(text=text):
                self.assert_invalid(text, "unknown field")
        self.assert_invalid("language: en\nlanguage: zh-CN\n", "duplicate field")
        self.assert_invalid("showcase:\n  pages: true\n  pages: false\n", "duplicate field")
        self.assert_invalid("[]", "expected a mapping")
        self.assert_invalid("resume: []", "expected a mapping")
        self.assert_invalid("true: value", "field name")

    def test_aliases_merges_tags_and_multiple_documents_are_rejected(self) -> None:
        self.assert_invalid("github: &owner {}\nresume: *owner\n", "aliases are unsupported")
        self.assert_invalid("github: {<<: {owner: sample}}", "merge keys are unsupported")
        self.assert_invalid("!!python/object:private {}", "expected a mapping")
        self.assert_invalid("language: !private en", "nonempty string")
        self.assert_invalid("{}\n---\n{}\n", "invalid YAML syntax")
        self.assert_invalid("showcase: [", "invalid YAML syntax")

    def test_errors_do_not_disclose_values_or_unknown_key_names(self) -> None:
        secret = "private-token-do-not-echo"
        for text in [f"github: {{owner: [{secret}]}}", f"{secret}: true", f"showcase: {{publish: {secret}}}", f"language: [{secret}"]:
            with self.subTest(text=text), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "preferences.yaml"
                path.write_text(text, encoding="utf-8")
                output = io.StringIO()
                with redirect_stderr(output):
                    self.assertEqual(preferences.main([str(path)]), 1)
                self.assertNotIn(secret, output.getvalue())

    def test_excessively_nested_yaml_has_a_controlled_private_error(self) -> None:
        secret = "private-value-must-not-appear"
        text = "resume: " + "[" * 1500 + secret + "]" * 1500
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "preferences.yaml"
            path.write_text(text, encoding="utf-8")
            output = io.StringIO()
            with redirect_stderr(output):
                self.assertEqual(preferences.main([str(path)]), 1)
            self.assertIn("invalid YAML syntax or excessive nesting", output.getvalue())
            self.assertNotIn("Traceback", output.getvalue())
            self.assertNotIn(secret, output.getvalue())

    def test_validation_is_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "preferences.yaml"
            path.write_text("showcase: {publish: local}\n", encoding="utf-8")
            before = (path.read_bytes(), path.stat().st_mtime_ns)
            preferences.load_preferences(path)
            self.assertEqual((path.read_bytes(), path.stat().st_mtime_ns), before)

    def test_dependency_failure_uses_distinct_exit_code(self) -> None:
        with patch.object(preferences, "yaml", None), redirect_stderr(io.StringIO()):
            self.assertEqual(preferences.main([__file__]), 2)


if __name__ == "__main__":
    unittest.main()
