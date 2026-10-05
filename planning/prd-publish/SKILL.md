---
name: prd-publish
description: >
  Use when an approved PRD roadmap must go to GitHub — 'publicar o roadmap no GitHub', 'criar o
  project e as issues do PRD', 'publish PRD roadmap' — handing over to pwdev-github (Project
  from a template, issues, sub-issues, blocked-by). Do NOT use for a single issue with the whole
  PRD (prd-export).
metadata:
  version: 3.0.0
---

# Publish a PRD roadmap to GitHub

## Input
the arguments: PRD slug (required).

## Flow

### STEP 0 — Language
Follow `<plugin-root>/references/language.md` (resolve `lang` from
`.planning/config.json`; ask only if unset).

### STEP 1 — Roadmap gate

```bash
SLUG="<slug>"   # first word of the arguments
DIR=".planning/prds/$SLUG/roadmap"
[ -f "$DIR/roadmap.json" ] || { echo "NO_ROADMAP"; ls .planning/prds/ 2>/dev/null; }
head -1 "$DIR/ROADMAP.md" 2>/dev/null
python3 "<plugin-root>/scripts/roadmap-check.py" "$DIR/roadmap.json" --no-write
```

- `NO_ROADMAP` → point to `/pwdev-prd:roadmap {slug}` and STOP.
- First line of `ROADMAP.md` is not `Roadmap: APPROVED…` → point to `/pwdev-prd:roadmap {slug}`
  to approve it, and STOP. Publishing an unapproved roadmap creates issues nobody agreed to.
- Checker `FAIL` → show the errors and STOP (the roadmap was edited after approval).

### STEP 1.1 — Stories readiness
Read the checker counts (`--json`): if there are `draft` stories, or no stories at all, say so
and ask: `{n} stories are still draft. 1. Refine first (prd-stories {slug} next) · 2. Publish
anyway (drafts are marked as such)`. Never block a publish on drafts without asking.

### STEP 2 — Hand off to pwdev-github
Publishing belongs to the `pwdev-github` plugin, so any roadmap in the `pwdev-roadmap/1`
format — from this plugin or another — goes through the same path.

- If the pwdev-github `github-publish` skill is available (how to call it in each runtime:
  `references/runtime.md` §Calling another plugin) → invoke it with
  `.planning/prds/{slug}/roadmap/roadmap.json` as the argument and follow it completely
  (Project template choice, customization, mapping, dry-run, confirmation).
- If it is not available → STOP with:
  ```
  ⚠️ Publishing needs the pwdev-github plugin.
     Claude Code: claude plugin install pwdev-github@pwdev-claude-marketplace
     Codex / Hermes / OpenCode: see the pwdev-github README (Setup)
     Then publish again.
  Alternative without it: prd-export {slug} --github (one issue with the whole PRD).
  ```

### STEP 3 — Record
When pwdev-github reports success, log
`sh "<plugin-root>/scripts/audit-log.sh" event publish "" completed "$DIR/roadmap.json" "{project url}"`.
The issue map lives in `.planning/github/{slug}.map.json` (written by pwdev-github);
`/pwdev-prd:list` reads the Project URL from it.

## Prohibitions
- NEVER publish a roadmap that is not approved or that fails the checker
- NEVER call `gh` directly from here — pwdev-github owns previews, confirmation, and idempotency

Language: resolve `lang` per `references/language.md` before any human-facing output. Paths `<plugin-root>/...`, `references/`, `scripts/`, `templates/` are relative to the plugin root; tool names, subagent dispatch and the command form to show the user depend on the runtime (`references/runtime.md`).
