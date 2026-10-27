---
name: opus-gap-audit
description: Find missing security controls — sibling functions that skip a control their peers call. Wraps gap_analyzer + cascade gate + Opus deep-audit. Run when js-index is complete and user names a control qname.
---

# opus-gap-audit

## Purpose
Surface "forgotten security control" findings — root-cause class 3 from
`wiki/tools/karpathy/source-code-review.md`. Given a control function
qname, the skill finds every callsite, then enumerates siblings (same
file + same parent module / same React component file) that do NOT
invoke the control. Survivors are Opus-audited so the verdict
distinguishes real gaps from middleware/SDK-level controls.

## Inputs
- `targets/<name>/db/js_analyzer.db` (per-target snapshot from
  `bin/db-isolate.py snapshot`).
- `targets/<name>/sources/` (post `sourcemap-explode`).
- A control qname. Pick from one of:
  - test files — search `*.test.{ts,tsx,js,jsx}` for the controls the
    team explicitly tests (per the spec page, this is the highest-yield
    starting point).
  - the wiki target page if one exists (`wiki/targets/<name>.md`).
  - `js_get_chains` output filtered by `taxonomy_id LIKE '%authz%'`
    or `'%csrf%'`.

## Steps

1. Resolve the control qname. If the user gave a bare name, run
   `js_get_snippet(qname=<name>)` and confirm it's a function or
   method that the analyzer indexed.

2. Enumerate gaps:
   ```
   python3 bin/run_gap_audit.py targets/<name> '<control_qname>' \
       --max-gaps 50 --cascade
   ```
   This:
   - finds all callers of the control (via callgraph edges)
   - for each caller, lists same-file + same-parent-module siblings
   - drops siblings that already call the control
   - emits `chains/gap_<slug>.jsonl` (gap-shaped chains)
   - `--cascade` runs the T1.2 gate over the gaps and writes
     `chains/gap_<slug>_survivors.jsonl` + `_rejected.jsonl`

3. For each chain in `chains/gap_<slug>_survivors.jsonl`, run the
   Opus gap-audit prompt. The prompt template is in
   `tlx/modules/js_analyzer/gap_analyzer.py:gap_audit_prompt()` and
   matches the longer template in
   `wiki/techniques/recon/adjacent-function-gap.md`. Invoke via the
   existing audit infra: build the prompt with `gap_audit_prompt(...)`,
   then call `js_run_audit(target_folder=...)` — the audit loop will
   accept the gap chain because it's chain-shaped.

4. Write `targets/<name>/opus/gap_<slug>/<sibling_qname>.md` per gap:
   - Control qname + caller (FN_OK)
   - Gap function (FN_GAP) + file + line range
   - Sibling files reviewed
   - Verdict ∈ {true_positive, false_positive, undetermined}
   - Opus reasoning trace
   - Proposed PoC (HTTP request or browser steps)

5. Submit each verdict via `js_submit_finding(chain_id, verdict, proof)`.
   Track Opus cost in `status.json.opus_cost_usd` (same budget as
   `opus-deep-audit`).

## Outputs
- `targets/<name>/chains/gap_<slug>.jsonl`
- `targets/<name>/chains/gap_<slug>_{survivors,rejected}.jsonl` (Step 2)
- `targets/<name>/chains/gap_<slug>_stats.json`
- `targets/<name>/opus/gap_<slug>/<sibling_qname>.md` per audited gap
- updated `status.json.phases.gap_<slug>`

### Output JSON schema (gap chain)
```json
{
  "id": "gap_<control_slug>_<sha10>",
  "kind": "gap",
  "control": "<control_qname>",
  "fn_ok": "<caller_qname>",
  "fn_gap": "<sibling_qname>",
  "file": "<file_rel_to_sources>",
  "score": <int 0-100>,
  "severity": "low|medium|high|critical",
  "source": { "qname": "...", "file": "...", "line": N, "taxonomy_id": "gap_<control>" },
  "sink":   { "qname": "...", "file": "...", "line": N, "taxonomy_id": "missing_<control>" },
  "path":   ["<sibling_qname>"],
  "depth":  1,
  "callsite_in_fn_ok": <int>
}
```

## Failure modes
- `callers_found == 0` → control qname is not invoked anywhere in the
  indexed code. Verify the qname (use `js_get_snippet`) and the index
  is fresh (`status.json.phases.index.ts`).
- All gaps cascade-rejected as `dead_code` → siblings have no inbound
  edges. Either real dead code (good — drop them) or the analyzer
  missed dynamic dispatch wiring. Inspect a few manually.
- Opus says every gap is `false_positive` with reason "control runs
  upstream" → the team really does apply the control at middleware /
  proxy level. Cache that finding in `wiki/targets/<name>.md` so future
  gap audits know to skip this control class.
- Cascade survives a gap but Opus times out → mark
  `verdict: undetermined`, log to `status.json.errors`, surface to user.

## Result block
```json
"phases": {
  "gap_<slug>": {
    "status": "done", "ts": "<iso>",
    "control": "<qname>",
    "callers_found": N, "gaps_found": M, "max_gaps": K,
    "output_file": "chains/gap_<slug>.jsonl",
    "cascade": { "total": M, "rejected": R, "escalated": E,
                 "rejected_dead_code": D, "rejected_sonnet": S,
                 "gate_cost_usd": Decimal }
  }
}
```
