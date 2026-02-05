---
name: codex-rules
description: "Enforce repo execution discipline: keep PRs small; run migration-smoke when invariants change; never hand-edit vendored contracts."
---

## Always
- Keep PRs small and auditable; avoid drive-by refactors.
- If invariants/plumbing are touched: run the canonical proof command listed in EVALSETS.yaml (currently: `npx nx run evalsets:migration-smoke`).
- Never hand-edit vendored contracts; use sync scripts + drift gates.

## Claude lane (enforced triggers)
If any of the following are true, you MUST propose a Claude Code run before proceeding:
- Repo-wide enumeration / dependency mapping across many files.
- Independent audit/review requested (migration correctness, invariants, compliance).
- Large-context synthesis from long documents.

When proposing Claude, provide all of:
1) **Claude prompt** (ready to copy/paste)
2) **Artifact path** to save output into (default: `docs/reviews/YYYYMMDD-HHMM_<slug>.md`)
3) **Acceptance criteria** (what the artifact must contain)

Do not proceed until the artifact exists, unless the user explicitly declines Claude.
If declined, proceed in Codex but label increased risk.

## Claude Code (optional specialist)
If the user asks for large mechanical edits/refactors, or if the change would touch many files, propose a Claude Code handoff.

When proposing Claude, output a paste-ready “Claude Work Order” with:
- Goal
- Allowed paths
- Hard constraints (no churn, no invariant changes, etc.)
- Verification commands
- Expected deliverable summary
Do not proceed with Claude unless the user explicitly says “yes”.

## Claude Code (optional specialist)
Follow the AGENTS.md handoff protocol. Codex must provide a paste-ready work order (goal, allowed paths, constraints, verification, expected output), then re-verify and update the worklog after Claude returns results.
