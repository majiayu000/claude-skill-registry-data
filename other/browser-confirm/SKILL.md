---
name: browser-confirm
description: Confirm an Opus-flagged true-positive chain in a real browser (live via Caido proxy or mock_backend). Run when opus-deep-audit marked verdict=true_positive or chain queued by cc-taint-route. Writes findings/<id>/confirmed.json. Default live; falls back to mock if rate-limited.
---

# browser-confirm

## Purpose
Static reasoning + headless mock are necessary but not sufficient. A
finding ships only after we *see it fire in a real browser*. This skill
runs that final proof.

## Inputs
- `targets/<name>/opus/<chain_id>.md` with `verdict: true_positive`.
- `targets/<name>/opus/<chain_id>.json` with
  `triage: runtime` (cc-taint-adversarial flow).
- `targets/<name>/findings/_queue_browser_confirm.jsonl` —
  high-confidence runtime chains routed here by `cc-taint-route`.
  Each line: `{chain_id, triage, confidence, chain, opus_record,
  queued_at}`. Process top-to-bottom; treat as a worklog.
- `targets/<name>/findings/_queue_mock_run.jsonl` —
  medium/low-confidence runtime chains. Same schema as above. **Try
  headless `mcp__tlx__mock_run` first** (cheaper, no real browser).
  If `mock_run` confirms the sink fires, promote to live-mode
  follow-up; if it doesn't, demote to `verdict: undetermined` and
  queue for `autoresearch-loop`.
- `memory.md` for default mode preference.

## Queue processing order

1. Drain `findings/_queue_browser_confirm.jsonl` in live mode (or
   mock if memory.md / target sensitivity says so).
2. Drain `findings/_queue_mock_run.jsonl` via `mock_run` →
   selectively promote to live/mock browser.
3. Pick up any remaining `opus/<id>.md verdict: true_positive`
   chains not already in either queue (legacy advisor pipeline).

After confirming each chain, append its `chain_id` to the appropriate
`status.json.phases.browser_confirm.confirmed_ids` / `failed_ids` and
leave the queue file in place — a future re-run that sees a
`findings/<chain_id>/confirmed.json` should skip it.

## Modes

### Live mode (default)
1. Make sure chrome-devtools MCP is running with Caido proxy
   (`caido-capture` should already have set that up).
2. `navigate_page(url=<entry_url from chain>)`.
2a. **DOMLogger++ injection (T2.1).** Immediately after navigation,
    inject the source/sink hook payload:
    ```
    evaluate_script(script=<contents of bin/domlogger_payload.js>)
    ```
    Hooks are idempotent (the payload guards via
    `window.__TLX_DOMLOGGER_INSTALLED`). All source reads + sink calls
    that fire during the rest of the run get appended to
    `window.__TLX_DOMLOGGER_EVENTS`.
2b. **Inline-handler enum (T2.4).** Once:
    ```
    evaluate_script(script=<contents of bin/eventlistener_enum.js>)
    ```
    Returns a JSON object — append to
    `findings/<chain_id>/event_handlers.json`. Cross-reference with
    the static-chain handler list to spot static-only or
    runtime-only handlers.

2c. **DOM verification contract (2026-05).** When the PoC HTML is
    being authored (by `report-finding` or by hand), it MUST emit
    `data-verify-*` attributes on the trigger element and set
    `data-verify-result="<canary>"` from inside the sink-triggering
    code. After the PoC fires, read the contract with:
    ```
    evaluate_script(script=<contents of bin/poc_verify_contract.js>)
    ```
    Returns JSON `{fired, trigger, source, sink, result_canary,
    evidence, entries[]}`. Write to
    `findings/<chain_id>/verify_contract.json`. The structured
    `fired` boolean is the load-bearing verification signal — prefer
    it over screenshot+LLM-judge whenever the PoC emits the contract.
    See [bin/poc_verify_contract.js](../../../bin/poc_verify_contract.js)
    for the attribute schema. Why this exists: a deterministic DOM
    contract replaces LLM-judged screenshots, which historically
    over-confirmed both visual coincidences and outright failures.
3. Inject the PoC payload via the channel the chain identifies:
   - URL parameter / fragment
   - form input + submit
   - `postMessage` from a controlled origin (use `evaluate_script` to
     do it from the same tab as origin-spoof)
4. Watch sink:
   - `list_console_messages` for our canary string
   - `list_network_requests` for a callback to our beacon host
   - `evaluate_script` to read the DOM for our injected node
   - `evaluate_script(script="JSON.stringify(window.__TLX_DOMLOGGER_EVENTS||[])")`
     and write to `findings/<chain_id>/domlogger.jsonl` so passive
     source/sink events are captured even when the explicit canary
     check misses.
5. `take_screenshot` of the moment of triggering.

### Mock mode (fallback)
Uses the SAME chrome-devtools MCP as live mode — just points at the
mock_backend localhost URL instead of the target. Benefit: installed
Chrome extensions (DOMLogger++, Caido browser, etc.) still load, so the
same source/sink instrumentation runs against the mock surface.

1. `mock_start(session_id=<chain_id>, target_folder="targets/<name>/sources/")`
   → returns `http://127.0.0.1:<port>/`.
2. chrome-devtools `new_page(url=<mock_url>)` (or `navigate_page` if a
   tab already exists). DOMLogger++ extension fires automatically.
3. Inject DOMLogger payload + handler enum scripts exactly as in live
   mode (steps 2a / 2b above) — covers any DOM that the extension misses.
4. Trigger the chain analogously (URL param, form submit, postMessage).
5. `mock_confirm(session_id, chain_id)` — TLX hook observes server-side
   sink calls and persists.
6. Inject `bin/poc_verify_contract.js` via `evaluate_script` — same
   DOM contract reader as live mode (step 2c). Write result to
   `findings/<chain_id>/verify_contract.json`. In mock mode the
   contract is the primary verification signal since there's no
   network beacon to corroborate.
7. `take_screenshot` of the trigger moment.
8. `mock_stop(session_id)`.

## Outputs
- `targets/<name>/findings/<chain_id>/confirmed.json`
- `targets/<name>/findings/<chain_id>/screenshots/*.png`
- `targets/<name>/findings/<chain_id>/network.har` (live mode only)
- `targets/<name>/findings/<chain_id>/domlogger.jsonl` (live mode, T2.1)
- `targets/<name>/findings/<chain_id>/event_handlers.json` (live mode, T2.4)
- `targets/<name>/findings/<chain_id>/verify_contract.json` (DOM
  verification contract, 2026-05). If `fired==true` AND
  `result_canary` matches the PoC's canary, the confirmation is
  considered deterministic — `confirmed.json.dom_contract_match: true`.

## Failure modes
- Sink doesn't fire → demote chain to `verdict: undetermined`,
  queue for `autoresearch-loop`.
- Live target has CSP that blocks our payload → record the CSP in
  `findings/<id>/csp_notes.md`; mark `bypass_needed: true`. Don't
  attempt CSP bypass without user OK.
- Target blocks our IP → switch to mock mode; log.

## Result block
```json
"phases": { "browser_confirm": { "status": "done", "ts": "<iso>",
  "confirmed_ids": [...], "failed_ids": [...], "mode_used": "live|mock" } }
```
