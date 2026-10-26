"""Exercise the publication boundary against real temporary Git indexes."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_public_tree import check_index


class PublicTreeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git("init", "-q")

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.root), *args], check=True, capture_output=True)

    def stage(self, name, content="Synthetic public material.\n"):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        self.git("add", "--", name)

    def test_public_guides_templates_and_synthetic_examples(self):
        for name in ["README.md", "JD/preparations/README.md", "Resume/variants/README.md",
                     "config/preferences.example.yaml", ".env.example", "examples/synthetic/resume.html"]:
            self.stage(name)
        self.assertEqual(check_index(self.root), [])

    def test_private_paths_cannot_enter_the_index(self):
        names = ["config/preferences.yaml", "Resume/private/base.html", "Resume/old-base.pdf",
                 "JD/preparations/case/meta/jd.md", "Resume/variants/case/changes.md",
                 "src/.env", "src/.env.production", "node_modules/dependency/index.js"]
        for name in names:
            self.stage(name)
        errors = check_index(self.root)
        self.assertEqual(len(errors), len(names))
        for name in names:
            self.assertTrue(any(error.startswith(name + ":") for error in errors))

    def test_index_content_is_checked_even_after_worktree_redaction(self):
        name = "example.md"
        self.stage(name, "Source: /" + "Users/fictional/private/input.md\n")
        (self.root / name).write_text("Redacted working copy.\n", encoding="utf-8")
        self.assertEqual(len(check_index(self.root)), 1)
        self.git("add", "--", name)
        self.assertEqual(check_index(self.root), [])

    def test_symlink_is_not_allowed_to_import_outside_material(self):
        (self.root / "external").symlink_to("../outside-material")
        self.git("add", "--", "external")
        self.assertEqual(len(check_index(self.root)), 1)


if __name__ == "__main__":
    unittest.main()
