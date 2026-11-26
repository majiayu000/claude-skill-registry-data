---
name: doc-consolidator-dedup
description: Merges N overlapping docs/plans into a single deduplicated work-list, archives the superseded ones with a stub-redirect — grep/ls before creating/classifying (LC-3)
---

> **Auto-Trigger:** When there are multiple docs/plans covering the same scope, or before creating a "new" master doc
> **Keywords:** "consolidate", "dedup", "overlapping docs", "master doc", "single work-list", "archive", "superseded", "duplicate"
> **Priority:** MEDIUM
> **Tools:** Bash, Read, Grep, Glob, Write, Edit
> **Related doctrine:** `rules/learned-corrections.md` (LC-3: grep/ls before creating or classifying).

# doc-consolidator-dedup — one work-list, no duplicates

Several competing master docs become noise. Consolidate into a single one, archiving the superseded ones — **but grep/ls BEFORE creating or classifying anything (LC-3)**.

## Contract

**INPUT:** N paths of docs/plans that are candidates for overlap.

**OUTPUT:** 1 canonical doc with a deduplicated work-list; the superseded ones become stub-redirects ("DEPRECATED → see `<canonical>`").

**EXIT CODES** (from `audit_plan.py`, used in step 2 to extract items):

| Exit | Meaning |
|---|---|
| 0 | extraction ok (self-test or real extraction) |
| 1 | doc not found / parsing failed |

**STATE IT TOUCHES:**

| Resource | Reads/Writes | Purpose |
|---|---|---|
| candidate docs/plans | Reads | extracts items (via `audit_plan.py`) |
| doc elected canonical | Writes (with human confirmation) | receives the merged work-list |
| superseded docs | Writes (with human confirmation) | become stub-redirects |

## Process
1. **LC-3 first:** `grep`/`ls`/`Glob` on the target paths to confirm what already exists. Treat "new master doc" as a hypothesis — the canonical one may already exist.
2. **Extract the items** from each doc (reuse the extractor in `${CLAUDE_PLUGIN_ROOT}/scripts/audit_plan.py` — do not reimplement plan parsing).
3. **Collapse aliases:** the SAME item under different IDs/names becomes one canonical entry (configurable alias rule).
4. **Elect the canonical doc** and merge everything into it (single deduplicated work-list).
5. **Archive the superseded ones** leaving a **stub-redirect** ("DEPRECATED → see `<canonical>`"). Configurable superseded criterion: `_DEPRECATED` marker, older date, or lower version.
6. **NEVER move/archive without confirmation** (respects LC-3).

## When NOT to Activate
- A single doc / no real overlap.
- When archiving would require a decision about which one is canonical that only the operator makes → propose, do not execute.

## Executed examples

```console
$ python scripts/audit_plan.py --self-test
self-test OK
```
<!-- executed: 2026-10-30 · exit=0 -->

```console
$ python scripts/audit_plan.py example-plan.md --no-git --json
{
  "total": 2,
  "summary": {"FEITO": 1, "PARCIAL": 0, "AUSENTE": 1},
  "itens": [
    {"text": "Create `README.md`", "status": "FEITO", "on_disk": true},
    {"text": "Create `never-exists-at-all.xyz`", "status": "AUSENTE", "on_disk": false}
  ]
}
```
<!-- executed: 2026-09-22 · exit=0 -->
(proves step 2: nothing is "probably done" — what does not exist on disk becomes AUSENTE.)

```console
$ python scripts/audit_plan.py
usage: audit_plan.py <plan.md> [--json] [--no-git] [--repo <dir>] [--extra-regex <re>]
```
<!-- executed: 2026-10-30 · exit=2 -->
(invalid usage — without the plan.md the extractor has nothing to audit; it never "assumes" a doc.)

## Proof

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/audit_plan.py --self-test
```

## See also
`${CLAUDE_PLUGIN_ROOT}/scripts/audit_plan.py` (deliverables extractor), LC-3 (grep before creating/classifying).
