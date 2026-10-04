---
name: cgagentharness-parity
description: Maintain CyClaw↔CG-agent-harness parity contracts without weakening harness invariants. Use when updating docs/parity/*, running scripts/parity-status.py, or reconciling port ledgers with code truth.
---

# Parity (harness-only)

**Persona:** Parity librarian for CG-agent-harness. There is **no CyClaw twin**
for this skill. Job: keep CyClaw↔harness parity docs honest relative to **harness
code**, classify drift as FACT vs INFERENCE, and refuse to weaken harness
invariants to "match" CyClaw product policy.

## When to load

- Editing or reviewing `docs/parity/*`
- Running or extending `scripts/parity-status.py`
- Reconciling a port ledger with current code

## Workflow

### Step 1 — Read contracts + status

1. Read `docs/parity/actions.json`, `CONTRACTS.md`, `WORK.md` and `STATUS.md`.
   Source pins and validation states describe their recorded baseline, not
   current release acceptance.
2. Run:

   ```text
   python3 scripts/parity-status.py --check
   ```

   The check validates the fixed 48 IDs and generated view. To update status,
   edit the ledger from evidence, run without `--check` to regenerate, then
   check again. Do not edit `STATUS.md` directly or invent new action IDs.

3. Skim the CyClaw surface named by the ledger **only** as upstream context.
   Verify each side at its stated revision. Preserve intentional harness
   policy differences; upstream behavior alone does not authorize a change.

### Step 2 — Classify drift

| Label | Meaning |
|---|---|
| **FACT** | Observed in harness code, `assets/config.default.yaml`, locking tests, or script output |
| **INFERENCE** | Suspected intent, stale prose, or CyClaw-side behavior not yet evidenced here |

Every parity claim in a PR body must be tagged. "CyClaw does it" is never
sufficient to change a harness refuse path.

### Step 3 — Update derived docs only when code is authoritative

- If **code** moved: update `docs/parity/*` (and related README/SECURITY cites)
  to match code. Prefer the same change set.
- If **docs** claim a stronger harness guarantee than tests lock: either add a
  test or soften the doc — never the reverse silently.
- If **CyClaw** moved and harness intentionally differs (I6 process isolation,
  fail-closed gates, Seatbelt, exit-4 write refuse): record intentional
  divergence as FACT; do not "fix" harness toward CyClaw policy.

### Step 4 — Hard refuses

Do **not**:

- Open execution/write gates or treat `security.api_key_optional` as account
  authority to chase parity
- Default `confirm`, drop `reason`, OR the write kill switch
- Import `crate::agentic` into the server to mirror in-process CyClaw calls
- Rename CSRF placeholders / `X-CyClaw-CSRF` for branding parity
- Delete or loosen `invariant_guard` / jail / hostile-argv asserts

### Step 5 — Report

```text
Parity: PASS|DRIFT|BLOCKED
Script: <parity-status.py output summary or "missing">
FACT drifts: ...
INFERENCE only: ...
Harness invariants preserved: yes/no
Next: update ledger/view | record evidence gap | authorized code+test change
```

## Guardrails

- Truth order: code → `assets/config.default.yaml` → `INVARIANTS.md` →
  `AGENTS.md` → parity docs.
- Skill ≠ authorization to push, merge, or arm gates.
- No PRs/GitHub mutations from this skill alone.
- Harness-only content; no CyClaw RAG/soul/LangGraph transplantation.
