---
name: opus-deep-audit
description: Deep-audit chains in dom_reachable.jsonl (fallback hot.jsonl) via Sonnet→Opus advisor pipeline. Writes opus/<chain_id>.md with verdict + PoC. Respects opus_budget from memory.md. Run after dom-xss-hunt.
---

# opus-deep-audit

## Purpose
Use Opus (via TLX's bounded advisor) to apply real reasoning to chains
that survived static + reachability filtering. This is where TP rate
gets earned.

## Inputs
- `targets/<name>/chains/dom_reachable.jsonl` (preferred) or
  `chains/hot.jsonl` (fallback if dom hunt was skipped).
- budget: `memory.md > opus_budget_per_target_usd`.

## Steps
1. Read budget. If `status.json.opus_cost_usd` already at limit,
   halt and require user to raise.

1a. **Long-context viability probe (T1.3).** Run:
    ```
    python3 bin/source_token_count.py targets/<name>
    ```
    The script estimates token count of `targets/<name>/sources/`
    (heuristic: bytes / 4) and writes
    `status.json.long_context.eligible`. When eligible (≤ 800k tokens
    by default), it also writes
    `targets/<name>/opus/whole_tree_prompt.md` — a manifest +
    instructions you can hand to a Claude Code subagent
    (`/feature-dev`, dispatch on Opus long-context) to perform a
    bundle-wide pass without `docs_query` retrieval.

    When `eligible == true`:
    - Skip `docs_query` retrieval in Step 2c. The whole tree fits in
      conversation context.
    - For the gap-audit pass (`opus-gap-audit`), prefer dispatching the
      whole-tree prompt over the chain-by-chain audit — Opus reads the
      entire bundle and surfaces gaps holistically.

    Per the API-key whitelist, this branch runs as Claude Code in your
    interactive session. Do NOT add a new `anthropic.Anthropic` code
    path to drive long-context audit autonomously.

1b. **Two-tier cascade gate (T1.2).** Before running any per-chain
    audit, gate the input list through `bin/run_cascade.py`:
    ```
    python3 bin/run_cascade.py targets/<name>
    ```
    The cascade combines a deterministic dead-code check with a Sonnet
    triage prompt (rubric: literal-constant source, wrapped safe
    sanitizer, pure-intermediates-only, short-length gate — see
    `wiki/tools/karpathy/js-review-cascade.md`). It writes:
    - `chains/survivors.jsonl` — chains the gate flagged `escalate`
    - `chains/rejected.jsonl` — chains the gate flagged `reject`
    - `chains/cascade_stats.json` — counts + cost
    - `status.json.phases.cascade` and `status.json.cascade_cost_usd`

    Use `chains/survivors.jsonl` as the input to Step 2.

    For each chain in `chains/rejected.jsonl`, write a stub
    `targets/<name>/opus/<chain_id>.md` containing the gate verdict
    and `verdict: false_positive`, reason `gate: <dead_code|sonnet_reject>`.
    Then submit via `js_submit_finding(chain_id, verdict='false_positive',
    proof='gate: ...')` so the verdict store reflects it.
    Do NOT call `js_run_audit` for rejected chains. (2026-05 — Opus
    budget rule; reaffirmed after the cascade-gate landed.)

2. For each chain in `chains/survivors.jsonl`:
   a. `js_examine_chain(chain_id=...)` → full source/sink/path.
   b. `js_get_snippet(qname=...)` for each function in the path
      adjacent ±1 hop.
   c. Compose the audit context (chain detail + snippets + framework
      hints + relevant `wiki/techniques/<sink_kind>/` page if exists —
      retrieve via `docs_query` against the wiki collection).
   d. Trigger `js_run_audit(target_folder=...)` if not already running
      for this target (it's a fire-and-forget audit loop that uses the
      Sonnet→Opus advisor internally).
   e. Poll `js_audit_status(run_id=...)` until `status == "done"`.
   f. Pull verdict + reasoning + PoC from audit output.
3. Write `targets/<name>/opus/<chain_id>.md` with sections:
   - Chain summary
   - Source / sink / path
   - Audit verdict
   - Reasoning trace (summarized — full transcript is in TLX SQLite)
   - Proposed PoC (HTML / curl / browser steps)
4. Submit verdict via `js_submit_finding(chain_id, verdict, proof)`.
5. Track cost: read `js_audit_status` cost fields, add to
   `status.json.opus_cost_usd`. The cascade gate's Sonnet cost is
   tracked separately at `status.json.cascade_cost_usd` so the Opus
   budget cap remains an Opus budget.

## Outputs
- `targets/<name>/chains/{survivors,rejected}.jsonl` (Step 1b).
- `targets/<name>/chains/cascade_stats.json` (Step 1b).
- `targets/<name>/opus/<chain_id>.md` per chain (rejected stubs + audited).
- updated `status.json.phases.{cascade,opus}`.

## Failure modes
- Budget exceeded mid-batch → halt, write partial result block,
  notify user.
- `js_run_audit` errors out → log to `status.json.errors`, mark chain
  `verdict: undetermined` so `autoresearch-loop` can retry later.
- Opus verdict says TP but proposed PoC obviously wrong → write
  verdict but flag `requires_user_review: true` in result block.
- Cascade gate parse failure (`parse_failures > 0` in stats) → those
  chains default to `escalate` (bias toward Opus). Inspect the gate
  payload's `error` field on each survivor's `_gate` annotation.
- Cascade gate rejects a chain that the user later confirms TP →
  feedback loop: add the chain pattern to the cascade rubric in
  `wiki/tools/karpathy/js-review-cascade.md` and re-run.

## Result block
```json
"phases": {
  "cascade": { "status": "done", "ts": "<iso>",
    "total": N, "rejected": R, "escalated": E,
    "rejected_dead_code": D, "rejected_sonnet": S,
    "gate_cost_usd": Decimal, "gate_duration_ms": N,
    "parse_failures": F, "input": "chains/...jsonl" },
  "opus":    { "status": "done", "ts": "<iso>",
    "chains_audited": N, "tp": X, "fp": Y, "undetermined": Z,
    "opus_cost_usd": Decimal, "user_review_flagged": [...] }
}
```
