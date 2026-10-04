---
id: managing-library
description: "Maintain an adept skill library (repo from `adept init --as-library`): published vs private skills, add --publish, syncing dev helpers to your harness. Apply in a library-layout project or when `adept skill list` shows a published/private source."
activation: agent
allowed-tools:
  - "Bash"
  - "Read"
  - "Edit"
  - "Write"
---

# Managing an adept library

A **library** is a repo created with `adept init --as-library`. It exists to publish skills
to other repos. It has two skill locations — keep them straight:

| location | source in `adept skill list` | published to consumers? | purpose |
|---|---|---|---|
| `skills/<id>/` (repo root) | `published` | **yes** | the library's product |
| `.adeptability/skills/<id>/` | `private` | **no** | dev-only helpers, rendered to your harness |

`config.json` carries `"layout": "library"`. Consumers add the repo with
`adept library add <name> --from <git-url>` and only ever see the **published** `skills/`.

## Adding skills

In a library, `adept skill add` defaults to **private** (it's the safe default — nothing is
published by accident). Use `--publish` for skills that ship to consumers:

```bash
adept skill add my-helper            # → .adeptability/skills/my-helper/   (private, dev-only)
adept skill add pr-review --publish  # → skills/pr-review/                 (published)
adept skill list                     # SOURCE column shows published | private | library:<name>
```

`edit` and `remove` take a bare `<id>` and find it in either location (published wins on a
name clash):

```bash
adept skill edit pr-review
adept skill remove my-helper
```

## Rendering dev helpers to your own harness

Private skills render to your enabled harnesses so they assist you *while you author the
library*, without shipping:

```bash
adept harness add claude-code        # once
adept sync                           # renders published + private → .claude/skills/, …
echo ".claude/" >> .gitignore        # rendered output is not source
```

`adept init --as-library` seeds this skill and the authoring helpers (`using-adept`,
`authoring-adept-skills`) straight into `.adeptability/skills/` for you.

## Publishing

Commit and push. Only `skills/` (published) reaches consumers; `.adeptability/skills/` and the
gitignored `.claude/` stay local.

```bash
git add skills .adeptability && git commit -m "add <skill>" && git push
```

Rules of thumb:

- Edit canonical (`skills/<id>/SKILL.md` or `.adeptability/skills/<id>/SKILL.md`), then
  `adept sync`. Never hand-edit rendered harness files — run `adept sync-from` to adopt those.
- Run `adept status` / `adept diff` before and after a sync to see what changed.
- `adept --help` and `adept skill --help` are the source of truth for flags.
