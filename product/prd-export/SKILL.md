---
name: prd-export
description: >
  Use when the user wants a PRD exported — 'exportar o PRD', 'gerar o prd.json', 'criar issue
  com o PRD', 'export PRD to GitHub' — as canonical JSON or as a single GitHub issue. Do NOT use
  to publish a roadmap with many issues (prd-publish).
metadata:
  version: 3.0.0
---

# Export a PRD

## Input
the arguments: `{slug} --json` or `{slug} --github` or just `{slug}` (interactive).

## Flow

### STEP 0 — Language
Follow `<plugin-root>/references/language.md` (resolve `lang` from
`.planning/config.json`; ask only if unset).

### STEP 1 — Load PRD

```bash
SLUG="<slug>"   # first word of the arguments
PRD_DIR=".planning/prds/$SLUG"
[ -f "$PRD_DIR/PRD.md" ] && cat "$PRD_DIR/PRD.md" || { echo "PRD_NOT_FOUND"; ls .planning/prds/ 2>/dev/null; }
```

If `PRD_NOT_FOUND` → show the available slugs and STOP.

### STEP 2 — Determine export type

If `--json` → generate/update prd.json
If `--github` → create GitHub issue
If neither → ask:

```
Export PRD "{slug}" as:
1. JSON file (.planning/prds/{slug}/prd.json)
2. GitHub issue
3. Both
```

### Mode: JSON Export

Generate `.planning/prds/{slug}/prd.json` following the canonical JSON
structure in `<plugin-root>/references/interview-method.md`:

- Keys in English
- Values in the PRD language (as written)
- No empty fields
- No sections that don't appear in the PRD

### Mode: GitHub Issue

One issue carrying the whole PRD. For a roadmap broken into issues with dependencies, use
`/pwdev-prd:publish {slug}` instead — say so once before continuing.

**Preflight (read-only):**

```bash
command -v gh >/dev/null || echo "NO_GH"
gh auth status >/dev/null 2>&1 || echo "NO_AUTH"
gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "NO_REPO"
gh label list --limit 200 --json name -q '.[].name' 2>/dev/null | grep -Ex 'prd|documentation'
wc -c < .planning/prds/{slug}/PRD.md
```

- `NO_GH` → show the install hint below and STOP.
- `NO_AUTH` → tell the user to run `! gh auth login` and STOP.
- `NO_REPO` → ask for the target `owner/repo` (pass it as `--repo`).
- A label from `prd`, `documentation` missing → offer to create it
  (`gh label create prd --color 5319E7 --description "Product requirements"`), or publish
  without it. Never create labels without a yes.
- Size over **60,000** bytes (GitHub rejects bodies over 65,536 characters) → the body becomes
  the Summary, Objectives, Scope and FR titles, plus a pointer to the file in the repository.

**Preview and confirm** — always, even when `--github` was passed:

```
Create issue in {owner/repo}?
  Title:  PRD: {feature name}
  Labels: {labels}
  Body:   {full PRD | summary, N bytes}
(y/n)
```

On yes:

```bash
gh issue create --repo "{owner/repo}" \
  --title "PRD: {feature name}" \
  --body-file .planning/prds/{slug}/PRD.md \
  --label "prd" --label "documentation"
```

(`--body-file` a temporary summary file in the size-limited case; drop the `--label` flags
the user declined.)

If `gh` is not available:
```
⚠️ GitHub CLI (gh) not found.
   Install: https://cli.github.com/
   Or copy the PRD from: .planning/prds/{slug}/PRD.md
```

### STEP 3 — Summary

```
✅ PRD exported

Format: {JSON / GitHub Issue / Both}
Files: {list of files created/updated}
GitHub: {issue URL if created}
```

## Prohibitions
- NEVER push to GitHub without asking
- NEVER modify the original PRD.md during export

Language: resolve `lang` per `references/language.md` before any human-facing output. Paths `<plugin-root>/...`, `references/`, `scripts/`, `templates/` are relative to the plugin root; tool names, subagent dispatch and the command form to show the user depend on the runtime (`references/runtime.md`).
