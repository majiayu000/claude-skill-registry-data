---
name: sdd-sync
description: >
  Reconcile SDD Composy task Markdown and the JSON projection: read-only inspect and
  plan, then apply only with an explicit authority and the CONFIRM-SDD-SYNC token.
  Use when task contracts and operational state diverged — 'sincronizar as tarefas',
  'o JSON das tasks está desatualizado', 'markdown and json disagree'. Do NOT use to
  list or advance tasks (sdd-tasks), for a status overview (sdd-status), or to
  simulate approval.
metadata:
  version: 0.1.0
---

# SDD Sync

Synchronize the human task contracts (Markdown) and the operational JSON projection without
silently selecting an authority, through the bundled `scripts/sdd_sync.py` helper.

Language: when an operation emits human-facing summaries, run `scripts/sdd_language.py <repo-root>` and use the persisted language; on `not_initialized`, return it with `next_action: run_init`. Localization rules: `references/language.md`.

## Operations

- `inspect <markdown-root> <state> [--root]` — read-only; reports stable, deterministic
  classifications, including conflicts and malformed inputs.
- `plan <markdown-root> <state> [--root]` — read-only; produces the exact plan and input
  fingerprints that an apply must consume.
- `apply <markdown-root> <state> <plan-json-path> --authority markdown|json
  --confirmation-token <plan token> [--root]` — the only mutating operation. The token is the
  plan's `confirmation_token` (`CONFIRM-SDD-SYNC-<digest>`), bound to the exact input
  fingerprints; any change to either side invalidates it. It requires
  explicit human approval of the selected authority; never infer approval from a plan, a clean
  inspection, or model confidence. The CLI forwards the plan JSON to the guarded apply API; it
  implements no second algorithm.

Present the inspect and plan results before asking for approval. A stale plan, changed input,
invalid authority, token that does not match the plan (`CONFIRM-SDD-SYNC-<digest>`), symlink, malformed artifact,
invalid merged projection, or unresolved conflict stops the operation. Markdown authority never
moves lifecycle state: a state divergence is resolved with `sdd_tasks.py transition` or JSON
authority; conflicts are never overwritten silently. After apply,
report the helper's post-apply verification and the exact paths changed. The helper owns
repository confinement, temporary files, atomic replacement, unknown-field preservation, and
deterministic output; do not duplicate those policies here.

## Read when

- `references/synchronization.md` — before `apply`, or to explain a classification.

## Output

Return the operation, repository-bound paths, classifications, selected authority (if any),
approval status, plan/token status, verification result, and next permitted action.

Safety: Do not commit, push, or publish. Do not read or expose `.env`, credentials, tokens, private keys, certificates, or fleet environment files. Full contract: `references/safety.md`.
