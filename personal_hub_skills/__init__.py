"""personal-hub-skills — SkillTemplate definitions, methodologies, prompts.

Loaded by Personal Hub via `apps/api/skills/loader_v2.py` with
`SKILLS_SOURCE=package`.
"""
from __future__ import annotations

from pathlib import Path

__version__ = "1.0.0"


def skills_path() -> Path:
    """Return the directory containing packaged skill YAML files."""
    return Path(__file__).parent / "skills"
