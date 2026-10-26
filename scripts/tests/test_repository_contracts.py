"""Check contracts shared by documentation, skill discovery, and the public tree."""

from pathlib import Path
import re
import subprocess
import sys
import unittest
from urllib.parse import unquote, urlsplit

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "skills/jd-interview-prep/scripts"))
from validate_pack import markdown_links, relative_target


def public_file_target(destination: str) -> str | None:
    parsed = urlsplit(destination)
    path = unquote(parsed.path)
    if (parsed.scheme.casefold() == "file"
            or re.match(r"^[A-Za-z]:[/\\]", unquote(destination))
            or (not parsed.scheme and not parsed.netloc and Path(path).is_absolute())):
        raise ValueError("Public documentation must use relative local file links")
    return relative_target(destination)


def unique_yaml(text: str):
    class UniqueKeysLoader(yaml.SafeLoader):
        def construct_mapping(self, node, deep=False):
            self.flatten_mapping(node)
            names = set()
            for key, _ in node.value:
                name = self.construct_object(key, deep=deep)
                if not isinstance(name, str) or name in names:
                    raise yaml.constructor.ConstructorError(
                        None, None, "YAML fields must be unique strings", key.start_mark,
                    )
                names.add(name)
            return super().construct_mapping(node, deep=deep)
    return yaml.load(text, Loader=UniqueKeysLoader)


class RepositoryContractsTests(unittest.TestCase):
    def test_documentation_links_resolve_in_the_public_tree(self):
        tracked = set(subprocess.check_output(
            ["git", "-C", str(ROOT), "ls-files", "-z"], text=True,
        ).rstrip("\0").split("\0"))
        for name in sorted(tracked):
            if not name.endswith(".md") or not (ROOT / name).is_file():
                continue
            source = ROOT / name
            for link in markdown_links(source.read_text(encoding="utf-8")):
                target = public_file_target(link.destination)
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

    def test_yaml_dependency_is_installed_for_the_development_checks(self):
        self.assertIsNotNone(yaml, "Install requirements-dev.txt before running development checks")

    def test_public_documentation_rejects_absolute_local_targets(self):
        for target in ("/tmp/synthetic-input.md", "%2Ftmp/synthetic-input.md",
                       "file:///tmp/synthetic-input.md", r"C:\temp\synthetic-input.md"):
            with self.subTest(target=target), self.assertRaises(ValueError):
                public_file_target(target)
        self.assertEqual(public_file_target("../README.md#使用"), "../README.md")
        self.assertIsNone(public_file_target("https://example.com/reference"))

    @unittest.skipIf(yaml is None, "Install requirements-dev.txt first")
    def test_skill_metadata_rejects_duplicate_fields(self):
        for text in ("name: first\nname: second\n", "description: first\ndescription: second\n",
                     "interface:\n  default_prompt: first\n  default_prompt: second\n"):
            with self.subTest(text=text), self.assertRaises(yaml.YAMLError):
                unique_yaml(text)

    @unittest.skipIf(yaml is None, "Install requirements-dev.txt first")
    def test_skill_discovery_metadata_matches_the_entrypoint(self):
        for directory in sorted((ROOT / "skills").iterdir()):
            if not directory.is_dir():
                continue
            with self.subTest(skill=directory.name):
                source = (directory / "SKILL.md").read_text(encoding="utf-8")
                frontmatter = re.match(r"\A---\n(.*?)\n---(?:\n|$)", source, re.S)
                self.assertIsNotNone(frontmatter, "skill entrypoint must have YAML frontmatter")
                metadata = unique_yaml(frontmatter[1])
                self.assertEqual(metadata["name"], directory.name)
                self.assertRegex(metadata["name"], r"\A[a-z0-9]+(?:-[a-z0-9]+)*\Z")
                self.assertLessEqual(len(metadata["name"]), 64)
                self.assertIsInstance(metadata["description"], str)
                self.assertTrue(metadata["description"].strip())
                self.assertLessEqual(len(metadata["description"]), 1024)
                self.assertLessEqual(set(metadata), {
                    "name", "description", "license", "compatibility", "metadata", "allowed-tools",
                })
                if "compatibility" in metadata:
                    self.assertIsInstance(metadata["compatibility"], str)
                    self.assertTrue(1 <= len(metadata["compatibility"]) <= 500)
                if "metadata" in metadata:
                    self.assertIsInstance(metadata["metadata"], dict)
                    self.assertTrue(all(isinstance(key, str) and isinstance(value, str)
                                        for key, value in metadata["metadata"].items()))
                for field in ("license", "allowed-tools"):
                    if field in metadata:
                        self.assertIsInstance(metadata[field], str)

                # Client UI metadata is an optional extension, not a skill requirement.
                ui_path = directory / "agents/openai.yaml"
                if not ui_path.exists():
                    continue
                interface = unique_yaml(ui_path.read_text(encoding="utf-8"))["interface"]
                for field in ("display_name", "short_description", "default_prompt"):
                    self.assertIsInstance(interface[field], str)
                    self.assertTrue(interface[field].strip())
                self.assertIn("$" + directory.name, interface["default_prompt"])
                self.assertTrue(25 <= len(interface["short_description"]) <= 64)


if __name__ == "__main__":
    unittest.main()
