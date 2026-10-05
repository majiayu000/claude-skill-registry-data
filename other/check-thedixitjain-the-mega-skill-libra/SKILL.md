---
name: check
description: "Friendly docflow readiness check: one status, one reason, and the exact next command. Use when asked if docflow is set up, ready, or \"what do I do next\"."
category: general-purpose
source_repo: hashgraph-online/awesome-codex-plugins
source_path: "plugins/MedAdemBHA/docflow/skills/check/SKILL.md"
source_url: https://github.com/hashgraph-online/awesome-codex-plugins/blob/HEAD/plugins/MedAdemBHA/docflow/skills/check/SKILL.md
---


# check

Goal: answer "is this usable and what do I do next?" in one screen.

## Run

```bash
bash scripts/docflow-check.sh --target <REPO ROOT>
```

If running from an installed plugin where scripts are not in the target repo, use the plugin script path.

## Interpret

| Status | Meaning | Next |
|--------|---------|------|
| `Ready` | DocFlow is installed and validation is clean | Start normal docs work |
| `Needs setup` | No meaningful docs or config detected | `/docflow:init` |
| `Needs adoption` | Existing docs need docflow infrastructure | `/docflow:adopt` |
| `Needs repair` | Generated helpers/guidance are missing | `/docflow:repair` |
| `Blocked` | Validation found hard errors | `/docflow:validate` |

## Rules

- Use this before asking the user to choose a setup path.
- Keep the response short: status, reason, next command.
- Do not run mutating commands from this skill; hand off to the matching skill.

---

**Source:** [`hashgraph-online/awesome-codex-plugins`](https://github.com/hashgraph-online/awesome-codex-plugins) → `plugins/MedAdemBHA/docflow/skills/check/SKILL.md`
