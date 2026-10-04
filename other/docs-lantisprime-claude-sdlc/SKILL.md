---
name: docs
description: Use this skill at the end of any phase that changed SDLC artifacts to update the SDLC documentation tree — the artifact index, requirements traceability matrix, architecture manifest, changelog, and any user-facing docs affected by the change. Also trigger when the user says "update docs", "refresh the index", "regenerate the traceability matrix", or after a deployment completes.
next_suggestions:
  - when: support_gate_signed
    suggest: "task complete — run /start or /plan to begin the next work item"
  - when: always
    suggest: "docs updated — continue with the current phase or run /start for the next work item"
---

# Docs (Phase 8, cross-cutting)

Keep the SDLC artifact tree navigable and the traceability matrix current.

## When to run

- After any phase signs a gate and the gate recorded artifact changes
- After a deployment completes
- On explicit request

## Step 1 — Update the artifact index

Refresh `.claude/sdlc/docs/index.md`:

- List every artifact by phase with its path and last-modified date
- Flag any orphans (requirements with no test case, test cases with no implementation, etc.)

## Step 2 — Traceability matrix

Refresh `.claude/sdlc/docs/traceability.md`:

| REQ ID  | Tech Spec        | Test Case(s) | Code (files/fns)  | Test Run | Deploy |
|---------|------------------|--------------|-------------------|----------|--------|
| REQ-001 | specs/order.md   | TC-001,002   | order.py::submit  | 2026-... | prod   |

Any empty cell is a visible gap. The human decides whether to fill or waive.

## Step 3 — Changelog

Append to `CHANGELOG.md` in the consuming repo root (not in `.claude/sdlc/`), following the project's convention (Keep a Changelog / Conventional Commits style).

## Step 4 — Architecture manifest

Refresh `.claude/sdlc/architecture/manifest.json`:

- File list with version and last-modified
- Cross-references (which spec refers to which architecture doc)

## Step 5 — User-facing docs

If the change affects user-facing APIs, CLI flags, config keys, or UI flows, update the corresponding user docs. Don't leave this for later.

## What this skill must NOT do

- Do not fabricate traceability. If a REQ has no test, say so in the matrix.
- Do not quietly "clean up" other docs while updating — follow surgical-edit discipline even here.

## References

- `docs/SDLC.md` Docs

## Next step hint

After updating the artifact index, pipe the `next_suggestions` conditions to `skills/_shared/next-hint.sh` and print any output:

```bash
printf '%s\n' \
  'support_gate_signed|task complete — run /start or /plan to begin the next work item' \
  'always|docs updated — continue with the current phase or run /start for the next work item' \
  | bash skills/_shared/next-hint.sh
```

Print any output verbatim. If the script outputs nothing, add nothing.
