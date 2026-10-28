# personal-hub-skills

Skills, agents, and methodologies for [Personal Hub](https://github.com/hulinl/personal-hub).

## What this repo is

- `personal_hub_skills/skills/*.yaml` — SkillTemplate definitions (names,
  system prompts, tool allowlists, autonomy modes)
- `methodologies/` — Markdown knowledge documents that agents read as context
- `style_patterns/` — example-based style guides per audience (client, colleague,
  friend)
- `prompts/` — shared system-prompt fragments

Personal Hub loads this repo via `apps/api/skills/loader_v2.py`.

## Install

```bash
pip install personal-hub-skills
```

In Personal Hub, set `SKILLS_SOURCE=package` env to load from this package.

## Use with Personal Hub

Point your tenant at this repo (or a fork) in `/settings/skills-source`. See
[docs/skills_repo_setup.md](https://github.com/hulinl/personal-hub/blob/main/docs/skills_repo_setup.md)
in the personal-hub repo.

## Fork

Want your own methodology? Fork this repo, then point your tenant's
`skills_repo_url` at your fork in `/settings/skills-source`. Changes you make
land in your fork; your Personal Hub's nightly cron pushes learned adjustments
there — not into `hulinl/personal-hub-skills`.

```bash
gh repo fork hulinl/personal-hub-skills --clone=false
```

## Validation

Every PR runs `.github/workflows/validate.yml`:

- `yamllint` on `personal_hub_skills/skills/`
- `scripts/validate_schema.py` — schema check (`name`, `version`, `category`,
  `description_markdown`, `agent_spec_json` with `name`/`model_profile`/
  `system_prompt_template`)
- `markdownlint-cli2` on `methodologies/`, `style_patterns/`, `prompts/`

## Nightly bot commits

Personal Hub's `push_skill_changes` cron commits learned adjustments as
`personal-hub-bot <bot@hulin.me>`. These commits are safe to merge or roll
back. Human commits by you are also welcome.

## File structure

```
personal_hub_skills/skills/        # agent YAML definitions
methodologies/                     # user-authored Markdown knowledge docs
style_patterns/                    # example style guides per audience
prompts/                           # shared prompt fragments
scripts/validate_schema.py         # schema check used by CI
.github/workflows/validate.yml     # CI
pyproject.toml                     # pip-installable
```

## License

MIT. See [LICENSE](./LICENSE).
