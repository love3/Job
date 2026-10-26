#!/usr/bin/env python3
"""Validate optional Job preferences without reading referenced personal files.

Usage: python3 scripts/validate_preferences.py [PREFERENCES_YAML]

No argument checks config/preferences.yaml beside this project's source. An
absent default file is valid: public defaults apply. An explicitly supplied
missing file is an error. The example is never loaded automatically.

Exit codes: 0 = valid or absent optional file; 1 = invalid preferences;
2 = missing dependency or invalid command-line usage.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None


class DependencyError(RuntimeError):
    """The optional configuration validator's YAML dependency is missing."""


class PreferencesError(ValueError):
    """A configuration error, deliberately excluding personal values."""


if yaml is not None:
    class PreferencesLoader(yaml.SafeLoader):
        """Compose a small YAML document without aliases or YAML 1.1 booleans."""

        yaml_implicit_resolvers = {
            key: [item for item in values if item[0] != "tag:yaml.org,2002:bool"]
            for key, values in yaml.SafeLoader.yaml_implicit_resolvers.items()
        }

        def compose_node(self, parent: Any, index: Any) -> Any:
            if self.check_event(yaml.AliasEvent):
                raise PreferencesError("preferences: YAML aliases are unsupported")
            return super().compose_node(parent, index)

    PreferencesLoader.add_implicit_resolver(
        "tag:yaml.org,2002:bool",
        re.compile(r"^(?:true|True|TRUE|false|False|FALSE)$"),
        list("tTfF"),
    )


_TAG = "tag:yaml.org,2002:"
_LANGUAGE = re.compile(r"(?:auto|[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})*)\Z")


def _error(scope: str, category: str) -> None:
    raise PreferencesError(f"{scope}: {category}")


def _string(node: Any, scope: str) -> str:
    if not isinstance(node, yaml.ScalarNode) or node.tag != _TAG + "str":
        _error(scope, "expected a nonempty string")
    if not node.value.strip():
        _error(scope, "expected a nonempty string")
    return node.value


def _boolean(node: Any, scope: str) -> bool:
    if (
        not isinstance(node, yaml.ScalarNode)
        or node.tag != _TAG + "bool"
        or node.value.lower() not in ("true", "false")
    ):
        _error(scope, "expected a boolean (true or false)")
    return node.value.lower() == "true"


def _strings(node: Any, scope: str) -> list[str]:
    if not isinstance(node, yaml.SequenceNode) or node.tag != _TAG + "seq":
        _error(scope, "expected a list of nonempty strings")
    return [_string(item, f"{scope}[{index}]") for index, item in enumerate(node.value)]


def _choice(*options: str):
    def check(node: Any, scope: str) -> str:
        value = _string(node, scope)
        if value not in options:
            _error(scope, "unsupported option")
        return value
    return check


def _language(node: Any, scope: str) -> str:
    value = _string(node, scope)
    if not _LANGUAGE.fullmatch(value):
        _error(scope, "expected auto or a language tag")
    return value


def _mapping(node: Any, scope: str, fields: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(node, yaml.MappingNode) or node.tag != _TAG + "map":
        _error(scope, "expected a mapping")
    result: dict[str, Any] = {}
    for key, value in node.value:
        if key.tag == _TAG + "merge" or getattr(key, "value", None) == "<<":
            _error(scope, "YAML merge keys are unsupported")
        if not isinstance(key, yaml.ScalarNode) or key.tag != _TAG + "str":
            _error(scope, "expected a string field name")
        name = key.value
        if name not in fields:
            # An unrecognized key can itself contain private data: do not echo it.
            _error(scope, "unknown field")
        field_scope = f"{scope}.{name}"
        if name in result:
            _error(field_scope, "duplicate field")
        validator = fields[name]
        result[name] = (
            _mapping(value, field_scope, validator)
            if isinstance(validator, dict)
            else validator(value, field_scope)
        )
    return result


_FIELDS = {
    "language": _language,
    "github": {"owner": _string},
    "showcase": {
        "enabled": _boolean,
        "frontend": _string,
        "frontend_policy": _choice("prefer_jd", "prefer_config"),
        "backend": _string,
        "publish": _choice("local", "public", "private"),
        "pages": _boolean,
        "notes": _strings,
    },
    "resume": {
        "enabled": _boolean,
        "base_en": _string,
        "base_zh": _string,
        "references": _strings,
        "primary_language": _choice("en", "zh"),
        "notes": _strings,
    },
}


def load_preferences(path: str | Path) -> dict[str, Any]:
    """Return only supplied settings, or raise ValueError for invalid input.

    This is structural validation, not an Agent preference-resolution engine.
    Source paths are retained as strings and are never opened or resolved.
    """
    if yaml is None:
        raise DependencyError("Install requirements-dev.txt to validate YAML preferences")
    try:
        content = Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        raise PreferencesError("preferences: cannot read UTF-8 configuration") from None
    try:
        node = yaml.compose(content, Loader=PreferencesLoader)
    except PreferencesError:
        raise
    except (yaml.YAMLError, RecursionError):
        raise PreferencesError("preferences: invalid YAML syntax or excessive nesting") from None
    if node is None:
        return {}
    return _mapping(node, "preferences", _FIELDS)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, help="YAML preferences to validate")
    args = parser.parse_args(argv)
    path = args.path or Path(__file__).resolve().parents[1] / "config/preferences.yaml"
    if args.path is None and not path.exists():
        print("SKIP: no personal preferences file; public defaults apply.")
        return 0
    try:
        load_preferences(path)
    except DependencyError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("PASS: preferences are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
