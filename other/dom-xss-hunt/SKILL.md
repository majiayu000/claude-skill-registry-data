---
name: dom-xss-hunt
description: Extract DOM sinks and event handlers via mock_extract and probe hot chains for reachability with mock_run. Run after chain-triage. Filters chains/hot.jsonl down to chains/dom_reachable.jsonl — the chains where a synthetic source actually flows into a DOM sink in a headless mock execution. Cheaper than full Opus audit, used as a TP-rate booster.
---

# dom-xss-hunt

## Purpose
Eliminate dead chains before spending Opus tokens. A chain that looks
plausible statically but never executes in a real page won't be a bug,
no matter how much Opus thinks about it. Headless mock execution is
the cheapest way to know.

## Inputs
- `targets/<name>/chains/hot.jsonl`
- `targets/<name>/sources/**`

## Steps
1. Call `mock_extract(target_folder="targets/<name>/sources/")` →
   returns `{routes: [...], dom_scaffold: {...}}`.
2. Call `mock_run(target_folder, chain_ids=[ids from hot.jsonl])` →
   batch-confirm in a single Playwright pass. Each chain gets a
   synthetic taint payload injected at its declared source and
   observed at its declared sink.
3. Partition chains into:
   - **reachable** → fired the sink with payload visible.
   - **unreachable** → no sink event.
   - **errored** → mock couldn't boot a route for this chain.
4. Write `chains/dom_reachable.jsonl` and `chains/dom_unreachable.jsonl`.
5. Update `status.json.phases.dom_hunt`.

## Outputs
- `targets/<name>/chains/dom_reachable.jsonl`
- `targets/<name>/chains/dom_unreachable.jsonl`

## Failure modes
- mock_extract returns empty routes → the analyzer didn't detect
  routes for this framework. File a fallback: route every chain to
  the literal page URL from the source map, if available.
- Mock can't render due to missing assets → some chunks weren't
  exploded. Re-run `sourcemap-explode` with `--include-nomap` (the
  helper supports passing nomap chunks through unmodified).

## Result block
```json
"phases": { "dom_hunt": { "status": "done", "ts": "<iso>",
  "reachable": N, "unreachable": M, "errored": K } }
```
