# personal-hub-skills

Skills, agents, and methodologies for Personal Hub.

## What this repo is

This repo contains SkillTemplate YAML definitions and Markdown methodology docs
that drive the Personal Hub AI assistant. It lives in a separate repo so the
learning history (skill edits, new agents, methodology updates) is readable
independently from the main application code.

Personal Hub loads this package at runtime. Tenants can point at a fork to use
fully custom skills without touching the application.

## Install

```bash
pip install personal-hub-skills
```

## Usage

Personal Hub loads this package automatically when `SKILLS_SOURCE=package` is
set. Point `tenant.skills_repo_url` at a fork to use custom skills.

```python
from personal_hub_skills import skills_path
yaml_files = list(skills_path().glob("*.yaml"))
```

## Fork guide

1. Fork this repo on GitHub.
2. Edit or add YAMLs under `personal_hub_skills/skills/`.
3. In your Personal Hub instance, go to `/nastaveni/skills-source` and set the
   tenant's fork URL.
4. Personal Hub will pull from your fork on the next sync.

## File structure

- `personal_hub_skills/skills/` — packaged YAML skill definitions; these are
  installed with the Python package and loaded by `loader_v2.py`.
- `methodologies/` — Markdown knowledge docs (context injected into prompts).
- `style_patterns/` — per-recipient writing style examples.
- `prompts/` — shared system prompts designed for cache-friendly reuse.

## Validation

Pull requests run `.github/workflows/validate.yml`, which performs a YAML
syntax check on all skill files. A full schema check is added in a follow-up.

## License

MIT — see [LICENSE](./LICENSE).
