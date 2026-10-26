"""Check contracts shared by documentation, skill discovery, and the public tree."""

from pathlib import Path
import re
import subprocess
import sys
import unittest

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "skills/jd-interview-prep/scripts"))
from validate_pack import markdown_links, relative_target


def shell_commands(path: Path) -> list[list[str]]:
    blocks = re.findall(r"```(?:sh|bash|shell)\n(.*?)```", path.read_text(encoding="utf-8"), re.S)
    return [
        [line.strip() for line in block.splitlines() if line.strip() and not line.lstrip().startswith("#")]
        for block in blocks
    ]


class RepositoryContractsTests(unittest.TestCase):
    def test_documentation_links_resolve_in_the_public_tree(self):
        tracked = set(subprocess.check_output(
            ["git", "-C", str(ROOT), "ls-files", "-z"], text=True,
        ).rstrip("\0").split("\0"))
        for name in sorted(tracked):
            if not name.endswith(".md"):
                continue
            source = ROOT / name
            for link in markdown_links(source.read_text(encoding="utf-8")):
                target = relative_target(link.destination)
                if target is None:
                    continue
                with self.subTest(source=name, line=link.line, target=target):
                    resolved = (source.parent / target).resolve()
                    self.assertTrue(resolved.is_relative_to(ROOT), "public documentation must be self-contained")
                    relative = resolved.relative_to(ROOT).as_posix()
                    self.assertTrue(resolved.exists(), "local link target is missing")
                    if resolved.is_dir():
                        self.assertTrue(any(path.startswith(relative + "/") for path in tracked))
                    else:
                        self.assertIn(relative, tracked, "link depends on an untracked or private file")

    def test_bilingual_guides_run_the_same_commands(self):
        for english, chinese in [("README.md", "README.zh-CN.md"),
                                 ("CONTRIBUTING.md", "CONTRIBUTING.zh-CN.md")]:
            with self.subTest(guide=english):
                commands = shell_commands(ROOT / english)
                self.assertTrue(commands, "guides must contain executable examples")
                self.assertEqual(commands, shell_commands(ROOT / chinese))

    def test_yaml_dependency_is_installed_for_the_development_checks(self):
        self.assertIsNotNone(yaml, "Install requirements-dev.txt before running development checks")

    @unittest.skipIf(yaml is None, "Install requirements-dev.txt first")
    def test_skill_discovery_metadata_matches_the_entrypoint(self):
        for directory in sorted((ROOT / "skills").iterdir()):
            if not directory.is_dir():
                continue
            with self.subTest(skill=directory.name):
                source = (directory / "SKILL.md").read_text(encoding="utf-8")
                frontmatter = re.match(r"\A---\n(.*?)\n---(?:\n|$)", source, re.S)
                self.assertIsNotNone(frontmatter, "skill entrypoint must have YAML frontmatter")
                metadata = yaml.safe_load(frontmatter[1])
                self.assertEqual(metadata["name"], directory.name)
                self.assertIsInstance(metadata["description"], str)
                self.assertTrue(metadata["description"].strip())
                interface = yaml.safe_load((directory / "agents/openai.yaml").read_text(encoding="utf-8"))["interface"]
                for field in ("display_name", "short_description", "default_prompt"):
                    self.assertIsInstance(interface[field], str)
                    self.assertTrue(interface[field].strip())
                self.assertIn("$" + directory.name, interface["default_prompt"])


if __name__ == "__main__":
    unittest.main()
