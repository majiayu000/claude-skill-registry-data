---
name: youtrack
description: >-
  YouTrack via the yt CLI (youtrack-cli / yt-cli) — issues, articles, projects,
  time, boards, reports. Load URL + API_TOKEN from SkillCred .env, then
  `yt auth login`. Use when the user mentions YouTrack, JetBrains issues,
  YouTrack query language, or invokes /youtrack_*.
disable-model-invocation: true
---

### TO COPY

# youtrack

Per-workspace registration slice. Credentials live in `{SKILL_PATH}/.env`.

## Working directory

Placeholders changed by `/meta-skills` at copy time (NAME => {PLACEHOLDER}):

IS_GLOBAL => {IS_GLOBAL}
TYPE_OF_AI_TOOLS => {TYPE_OF_AI_TOOLS}
SKILL_PATH => {SKILL_PATH}

```bash
export CURRENT_SKILL_DIRECTORY="{SKILL_PATH}"
eval "$(~/.meta-skills/.venv/bin/python ~/.meta-skills/skills/productivity/youtrack/scripts/skill_env.py)"
export PATH="$HOME/.meta-skills/.venv/bin:$PATH"
yt auth login --base-url "$URL" --token "$API_TOKEN"
```

##### END TO COPY

# youtrack — Command Index

Router to `yt` command domains. References live in `command.md/` under the
**shared library** (`~/.meta-skills/skills/productivity/youtrack/`).

## Prerequisites

This skill documents the **`yt` CLI** ([PyPI youtrack-cli](https://pypi.org/project/youtrack-cli/) · [docs](https://yt-cli.readthedocs.io/en/stable/)). Install once in the shared venv:

```bash
cd ~/.meta-skills/skills/productivity/youtrack
~/.meta-skills/install.sh pip init .
yt --version
```

Load credentials into the shell, login, then call `yt` directly:

```bash
export CURRENT_SKILL_DIRECTORY="{SKILL_PATH}"
eval "$(~/.meta-skills/.venv/bin/python ~/.meta-skills/skills/productivity/youtrack/scripts/skill_env.py)"
export PATH="$HOME/.meta-skills/.venv/bin:$PATH"
yt auth login --base-url "$URL" --token "$API_TOKEN"
yt issues list --project-id PROJ
```

PowerShell:

```powershell
$env:CURRENT_SKILL_DIRECTORY = "{SKILL_PATH}"
~/.meta-skills/.venv/bin/python ~/.meta-skills/skills/productivity/youtrack/scripts/skill_env.py --shell powershell | Invoke-Expression
$env:PATH = "$HOME/.meta-skills/.venv/bin;$env:PATH"
yt auth login --base-url $env:URL --token $env:API_TOKEN
yt issues list --project-id PROJ
```

`skill_env.py` reads `.env` via SkillCred and prints export commands for the detected OS/shell — no manual `source .env`. Always `eval` it in the **current** terminal so `$URL` and `$API_TOKEN` exist before `yt auth login`.

## Credentials — SkillCred `.env`

| Variable | Example |
|----------|---------|
| `URL` | `https://company.youtrack.cloud` |
| `API_TOKEN` | Permanent token (`perm:…`) |

```bash
cp ~/.meta-skills/skills/productivity/youtrack/.env.example "{SKILL_PATH}/.env"
```

Create a token in YouTrack: **Profile → Account Security → Tokens**
([permanent tokens](https://www.jetbrains.com/help/youtrack/cloud/manage-permanent-token.html)).

Self-signed instance: add `--no-verify-ssl` to `yt auth login`.

## Connect (every YouTrack session)

1. `export CURRENT_SKILL_DIRECTORY="{SKILL_PATH}"`
2. `eval "$(python scripts/skill_env.py)"` — exports `URL` and `API_TOKEN`
3. `yt auth login --base-url "$URL" --token "$API_TOKEN"`
4. Run `yt …` commands

Put `~/.meta-skills/.venv/bin` on `PATH` (or call `~/.meta-skills/.venv/bin/yt`).

Confirm with the user before **write** ops (create, update, delete, assign).

## When to use

Trigger phrases: "YouTrack issue", "create a YouTrack ticket", "YouTrack search",
"log time in YouTrack", "YouTrack board", `/youtrack_*`.

## youtrack-auth

Login, status, token, logout.
Use first every session — `yt auth login` with `$URL` and `$API_TOKEN` from `skill_env.py`.

Commands → `~/.meta-skills/skills/productivity/youtrack/command.md/youtrack-auth.command.md`

---

## youtrack-issues

Issue CRUD, search, comments, attachments, links, tags.
Use for a single issue or YouTrack query language search.

Commands → `~/.meta-skills/skills/productivity/youtrack/command.md/youtrack-issues.command.md`

---

## youtrack-articles

Knowledge base: search, tree, create, tag.

Commands → `~/.meta-skills/skills/productivity/youtrack/command.md/youtrack-articles.command.md`

---

## youtrack-projects

Projects and users: list, create, configure.

Commands → `~/.meta-skills/skills/productivity/youtrack/command.md/youtrack-projects.command.md`

---

## youtrack-time

Worklogs, time reports, summaries.

Commands → `~/.meta-skills/skills/productivity/youtrack/command.md/youtrack-time.command.md`

---

## youtrack-boards

Agile boards, burndown, velocity.

Commands → `~/.meta-skills/skills/productivity/youtrack/command.md/youtrack-boards.command.md`

---

## Notes

- Never commit `.env` or API tokens.
- Never print `API_TOKEN`.
- Prefer `--format json` when the CLI supports it.
- Full reference: `yt --help` / [yt-cli docs](https://yt-cli.readthedocs.io/en/stable/).
