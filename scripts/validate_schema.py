"""Validate every skill YAML has the fields Personal Hub's SkillTemplate requires.

Usage: python scripts/validate_schema.py personal_hub_skills/skills/

Exits 0 if all pass, 1 otherwise. CI uses this as the "schema check" step.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ALLOWED_CATEGORIES = {"mail", "calendar", "notion", "content", "planning", "other"}

REQUIRED_TOP = ["name", "version", "category", "description_markdown", "agent_spec_json"]
REQUIRED_AGENT_SPEC = ["name", "model_profile", "system_prompt_template"]


def _fail(path: Path, reason: str) -> str:
    return f"FAIL {path}: {reason}"


def validate_one(path: Path) -> list[str]:
    try:
        data = yaml.safe_load(path.read_text())
    except yaml.YAMLError as exc:
        return [_fail(path, f"YAML parse error: {exc}")]
    if not isinstance(data, dict):
        return [_fail(path, "root must be a mapping")]

    errors: list[str] = []
    for key in REQUIRED_TOP:
        if key not in data:
            errors.append(_fail(path, f"missing required key: {key!r}"))

    name = data.get("name")
    if name is not None and not isinstance(name, str):
        errors.append(_fail(path, f"'name' must be str, got {type(name).__name__}"))
    elif isinstance(name, str) and (not name or " " in name or len(name) > 128):
        errors.append(_fail(path, f"'name' invalid (snake_case, 1..128 chars): {name!r}"))

    version = data.get("version")
    if version is not None and (not isinstance(version, int) or version < 1):
        errors.append(_fail(path, f"'version' must be int >= 1, got {version!r}"))

    category = data.get("category")
    if category is not None and category not in ALLOWED_CATEGORIES:
        errors.append(
            _fail(path, f"'category' must be one of {sorted(ALLOWED_CATEGORIES)}, got {category!r}")
        )

    desc = data.get("description_markdown")
    if desc is not None and (not isinstance(desc, str) or not desc.strip()):
        errors.append(_fail(path, "'description_markdown' must be non-empty str"))

    agent_spec: Any = data.get("agent_spec_json")
    if agent_spec is not None:
        if not isinstance(agent_spec, dict):
            errors.append(_fail(path, "'agent_spec_json' must be a mapping"))
        else:
            for key in REQUIRED_AGENT_SPEC:
                if key not in agent_spec:
                    errors.append(_fail(path, f"'agent_spec_json' missing key: {key!r}"))

    is_default = data.get("is_default", False)
    if not isinstance(is_default, bool):
        errors.append(_fail(path, f"'is_default' must be bool, got {type(is_default).__name__}"))

    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_schema.py <skills_dir>", file=sys.stderr)
        return 2
    skills_dir = Path(argv[1])
    if not skills_dir.is_dir():
        print(f"not a directory: {skills_dir}", file=sys.stderr)
        return 2

    yaml_files = sorted(skills_dir.glob("*.yaml"))
    if not yaml_files:
        print(f"no YAML files found in {skills_dir}", file=sys.stderr)
        return 2

    all_errors: list[str] = []
    for path in yaml_files:
        errors = validate_one(path)
        if errors:
            all_errors.extend(errors)
        else:
            print(f"OK   {path}")

    if all_errors:
        print("", file=sys.stderr)
        for e in all_errors:
            print(e, file=sys.stderr)
        print(f"\n{len(all_errors)} schema violation(s) across {len(yaml_files)} file(s).", file=sys.stderr)
        return 1

    print(f"\nAll {len(yaml_files)} skill YAMLs valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
