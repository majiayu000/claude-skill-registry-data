---
name: prd-refine
description: >
  Use when the user wants to change an existing PRD — 'refinar o PRD', 'adicionar requisito',
  'atualizar escopo do PRD', 'update the PRD' — through targeted questions, bumping the version
  and re-opening approval. Do NOT use to create a PRD (prd-create).
metadata:
  version: 3.0.0
---

# Refine a PRD

## Method (inline — you run in the MAIN context)
You are the PRD interviewer. Follow
`<plugin-root>/references/interview-method.md` (persona, principles,
consistency checks). Never delegate to a subagent — you interview the human.

## Input
The arguments: PRD slug (required).

## Flow

### STEP 0 — Language
Follow `<plugin-root>/references/language.md` (resolve `lang` from
`.planning/config.json`; ask only if unset).

### STEP 1 — Load existing PRD

```bash
PRD_DIR=".planning/prds/<slug>"
if [ ! -f "$PRD_DIR/PRD.md" ]; then
  echo "PRD_NOT_FOUND"
  ls .planning/prds/ 2>/dev/null
else
  cat "$PRD_DIR/PRD.md"
fi
```

If `PRD_NOT_FOUND` → show the available slugs and STOP.

### STEP 2 — Ask what to refine

```
I've loaded the PRD for "{slug}".

What would you like to refine?
1. Add or modify functional requirements
1b. Add or modify business rules (RN)
2. Update non-functional requirements
3. Revise architecture and approach
4. Add or update risks
5. Refine acceptance criteria
6. Update scope
7. Other (describe what you want to change)
```

### STEP 3 — Targeted Interview

Run only the relevant interview steps for the selected sections.
Follow the same rules: one question at a time, summarize, confirm.

### STEP 4 — Re-run Consistency Checks

Validate the entire PRD after changes.

### STEP 5 — Update PRD.md

Rewrite the complete PRD.md with the changes incorporated, and:
- bump `Version` (minor for added or changed requirements, patch for wording fixes);
- append a row to `### Change Log` (version, date, one-line summary of what changed);
- keep existing `FR-xx` / `NFR-xx` / `AC-xx` IDs stable — new items take the next free number,
  removed items keep their ID retired (never reused);
- if the PRD was `APPROVED`, set it back to `DRAFT` and ask for approval again at the end:
  `Approve the updated PRD? (y/n)`.

If `.planning/prds/{slug}/roadmap/` exists, warn that it was generated from an older version
and suggest `/pwdev-prd:roadmap {slug}` (option 2, revise) to bring it in line.
If prd.json exists, update it too (canonical structure in
`<plugin-root>/references/interview-method.md`).
Log: `sh "<plugin-root>/scripts/audit-log.sh" event refine "" completed ".planning/prds/{slug}/PRD.md" ""`

### STEP 6 — Ask about commit

If changes were made:
```
PRD updated. Commit changes? (y/n)
```

If yes:
```bash
git add .planning/prds/{slug}/
git commit -m "docs(prd): update PRD for {slug}"
```

## Prohibitions
- NEVER lose existing content when refining
- NEVER skip consistency checks after changes

Language: resolve `lang` per `references/language.md` before any human-facing output. Paths `<plugin-root>/...`, `references/`, `scripts/`, `templates/` are relative to the plugin root; tool names, subagent dispatch and the command form to show the user depend on the runtime (`references/runtime.md`).
