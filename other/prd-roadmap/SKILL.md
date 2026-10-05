---
name: prd-roadmap
description: >
  Use when an approved PRD must become an executable roadmap — 'gerar roadmap do PRD', 'quebrar
  o PRD em épicos e features', 'cadeia de dependências', 'roadmap with dependencies' —
  Phase/Epic/Feature/Task with explicit dependencies, waves and critical path, validated by a
  deterministic checker, with an approval gate. Do NOT use for a PRD that is not approved (prd-
  create/prd-refine first).
metadata:
  version: 3.0.0
---

# PRD roadmap with dependencies

## Method
You run in the MAIN session as the orchestrator: you validate, dispatch the roadmap
writer, run the deterministic checker, and hold the approval gate. When the runtime has a
subagent mechanism you never write the roadmap files yourself — the writer does, and on change
requests you re-dispatch it. Without one, follow `references/roadmap-agent.md` inline (see
`references/runtime.md`), then continue from STEP 5 exactly the same way.
Format contract: `<plugin-root>/references/roadmap-format.md`.

## Input
the arguments: PRD slug (required).

## Flow

### STEP 0 — Language
Follow `<plugin-root>/references/language.md` (resolve `lang` from
`.planning/config.json`; ask only if unset).

### STEP 1 — Load and gate the PRD

```bash
SLUG="<slug>"   # first word of the arguments
PRD=".planning/prds/$SLUG/PRD.md"
[ -f "$PRD" ] && grep -m1 -E '^Status:' "$PRD" || { echo "PRD_NOT_FOUND"; ls .planning/prds/ 2>/dev/null; }
```

- `PRD_NOT_FOUND` → show the available slugs and STOP.
- `Status:` is not `APPROVED` (or missing, in PRDs made before v2.1) → read the PRD, show a
  3-line summary, and ask: `Approve PRD "{slug}" so the roadmap can be generated? (y/n)`.
  On yes, set `Status: APPROVED` in the header and log
  `sh "<plugin-root>/scripts/audit-log.sh" event roadmap "" approved "$PRD" "prd gate"`.
  On no, STOP and point to `/pwdev-prd:refine {slug}`.

### STEP 2 — Readiness check
Read the PRD. Check it has: objectives with metric and target, functional requirements with
`FR-xx` IDs, acceptance criteria, and in/out of scope. If any is missing, name it. If **three
or more** are missing, STOP: the roadmap would be fiction — send the user to
`/pwdev-prd:refine {slug}`. If FRs lack IDs but everything else is there, ask to number them
(`FR-01`…) in the PRD first; traceability depends on it. A PRD without a
`### Business Rules` section (written before v3.0) is not blocking: say that the stories will
carry no RN until `prd-refine` adds them.

### STEP 3 — Existing roadmap
If `.planning/prds/{slug}/roadmap/roadmap.json` exists, ask:
```
A roadmap already exists for "{slug}".
1. Regenerate from the current PRD (replaces it)
2. Revise it with specific changes
3. Keep it and stop
```

### STEP 4 — Dispatch the roadmap writer
Dispatch it per `references/runtime.md` (Claude `subagent_type: "pwdev-prd:roadmap"`, Codex
`spawn_agent`, Hermes `delegate_task`, OpenCode `task`, or inline) with this dispatch block,
and nothing it has to ask back:

```
PRD: .planning/prds/{slug}/PRD.md
Roadmap dir: .planning/prds/{slug}/roadmap/
Contract: <plugin-root>/references/roadmap-agent.md
Format reference: <plugin-root>/references/roadmap-format.md
Checker: python3 "<plugin-root>/scripts/roadmap-check.py" .planning/prds/{slug}/roadmap/roadmap.json
Language: {lang}
Mode: create | revise
Changes / checker errors: {only on re-dispatch}
```

### STEP 5 — Deterministic check

```bash
python3 "<plugin-root>/scripts/roadmap-check.py" ".planning/prds/$SLUG/roadmap/roadmap.json"
```

- `FAIL` → re-dispatch the writer in `revise` mode (inline: revise it yourself) with the error lines (at most **2**
  re-dispatches). Still failing → show the errors and STOP; never patch the files by hand.
- `PASS` → the checker has written `DEPENDENCIES.md`. Continue.

### STEP 6 — Gate
Present at most ten lines, then ask for approval:

```
🗺️ Roadmap "{slug}" — {phases} phases | {epics} epics | {features} features | {tasks} tasks
🔗 Dependencies: {edges} edges | {waves} waves
⏱️ Critical path: {F01-E01-FT01 → … } (weight {n})
📎 Traceability: {PASS | warnings}
📚 Stories: {n} draft across {features} features · Business rules: {rules}
📁 .planning/prds/{slug}/roadmap/ROADMAP.md · DEPENDENCIES.md (Mermaid graph) · STORIES.md

Approve this roadmap? (y = approve / n = describe the changes)
```

- **Approve** → replace the first line of `ROADMAP.md` with `Roadmap: APPROVED ({date})` and
  log `sh "<plugin-root>/scripts/audit-log.sh" event roadmap "" completed ".planning/prds/{slug}/roadmap/ROADMAP.md" ""`.
- **Changes** → re-dispatch in `revise` mode with the user's changes appended; back to STEP 5.

### STEP 7 — Commit (ask)
```
Commit the roadmap? (y/n)
```
If yes: `git add .planning/prds/{slug}/roadmap/ && git commit -m "docs(prd): add roadmap for {slug}"`

### STEP 8 — Next
```
👉 /pwdev-prd:stories {slug} next → evolve each feature: stories, CA and RN up to ready
👉 /pwdev-prd:publish {slug}   → GitHub Project + issues with the dependency chain
👉 /pwdev-prd:refine {slug}    → change the PRD (then regenerate the roadmap)
```

## Prohibitions
- NEVER generate a roadmap from a PRD that is not `APPROVED`
- NEVER write or patch roadmap files yourself when a subagent mechanism exists — dispatch the writer
- NEVER write `DEPENDENCIES.md` by hand — the checker generates it
- NEVER mark the roadmap approved without the user's explicit yes
- NEVER commit without asking

Language: resolve `lang` per `references/language.md` before any human-facing output. Paths `<plugin-root>/...`, `references/`, `scripts/`, `templates/` are relative to the plugin root; tool names, subagent dispatch and the command form to show the user depend on the runtime (`references/runtime.md`).
