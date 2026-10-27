---
name: passive-listen
description: Accumulate live browser evidence while user browses — DOMLogger++ + postMessage-tracker + Caido capture into per-target runtime/ tree. Use when browsing a target during static analysis, or before chain-triage for dynamic evidence.
---

# passive-listen

## Purpose

CT podcast methodology (Matanber Ep ~100, Renee, Frans Rosén, Yusuf) emphasizes
dynamic-first JS hunting: get intimate with the app, let extensions log every
DOM source/sink/listener as you click, then read JS only for flagged paths.

This skill formalizes that pattern. While the user (or Claude) drives the
browser, the skill snapshots three extension stores plus Caido network capture
on a poll interval. Output feeds later chain-triage + opus-deep-audit (a hot
chain whose source actually fired at runtime ranks higher than one whose did
not).

## When to fire

- User explicitly says "passive listen for N min" / invokes `/passive-listen`.
- A long static job (extract_chains, rag-ingest, opus-deep-audit) is in
  background AND `memory.md` rule `parallel-dynamic-static` says don't sit
  idle.
- Start of an engagement before any audit, to seed runtime evidence.

## Inputs

- `targets/<name>/status.json` for scope hosts.
- A live `@browser` tab on the target. Caller must have ensured `caido-capture`
  is set up first.
- Optional: poll interval in seconds (default 30).
- Optional: total session minutes (default 15).

## Required Chrome extensions

- DOMLogger++ — DOM source/sink hooks
- postMessage-tracker (fransr) — listener registration capture
- Gecko (Caleb Gross) — sink-context payload candidate detection
- FoxyProxy + Caido browser plugin — request capture

If any are missing, the skill still runs but the corresponding store in
`state.json` will be `null`. Log this in the per-session summary.

## Outputs

- `targets/<name>/runtime/<utc-iso>/state.json` per poll iteration
- `targets/<name>/runtime/_log.jsonl` rolling one-line summary
- `targets/<name>/runtime/<utc-iso>/caido_delta.json` new requests captured
  since last poll (queried via `caido_list_requests`)
- Final session summary at `targets/<name>/runtime/_session_<ts>.md` with:
  - URLs visited
  - Distinct DOMLogger++ sources observed (param names, value samples
    sanitized)
  - Distinct postMessage listeners registered (file + line if available)
  - Forms encountered
  - New JS chunks captured by Caido
  - Inline-handler attribute count

## Flow

1. Read `status.json.active_focus_hosts` and `status.json.tier1_hosts`.
2. Confirm `@browser` tab present via `tabs_context_mcp`. If not, fail loudly.
3. Pre-flight state dump:
   ```
   snippet = `python3 bin/dump_browser_state.py --snippet`
   result  = mcp__claude-in-chrome__javascript_tool(snippet, tabId)
   echo "$result" > /tmp/state.json
   python3 bin/dump_browser_state.py --persist /tmp/state.json <name>
   ```
4. Concurrently: `mcp__caido__caido_list_requests` filtered to in-scope hosts;
   save to `runtime/<ts>/caido_delta.json`.
5. Sleep `poll_interval_s`.
6. Repeat steps 3-5 until session-minutes elapsed OR user says "stop".
7. After the loop, emit `runtime/_session_<ts>.md` with synthesized findings.

## Dialog hazard

Per `feedback_browser_mcp_chrome_only`, claude-in-chrome MCP freezes when JS
alerts pop. DOMLogger++ default config may pop alerts on suspected XSS. Inject
`window.alert = console.log` at session start (already done by `js-harvest` /
`browser-confirm` skills). Skill re-injects defensively at every poll.

## Result block (status.json)

```json
"phases": {
  "passive_listen": {
    "status": "done",
    "ts": "<iso>",
    "session_minutes": 15,
    "polls": 30,
    "domlogger_events_total": 412,
    "postmessage_listeners_total": 17,
    "gecko_sinks_total": 5,
    "new_chunks_observed": 23,
    "summary_path": "targets/<name>/runtime/_session_<ts>.md"
  }
}
```

## What to do AFTER passive-listen

- Re-run `chain-triage` with the runtime evidence — chains whose source name
  matches an observed DOMLogger++ source bump up the priority queue.
- Re-run `js-harvest` if `new_chunks_observed > 0`. Re-index + re-isolate +
  re-triage. The fresh chunks usually include MFEs the initial walk missed
  (account-edit, product-detail, checkout-deep, customer-service).
- Feed `postmessage_listeners_total` set into a tagged chain-triage filter:
  any chain whose entry function is one of these listeners gets explicit Opus
  audit attention.

## Failure modes

- @browser MCP disconnects mid-session: pause loop, surface to user, retry
  on next manual `tabs_context_mcp`.
- DOMLogger++ store globals not present (extension disabled / not loaded):
  fall back to injecting `bin/domlogger_payload.js` via javascript_tool so we
  at least get TLX-payload events.
- Caido requests query fails: continue browser-side capture; flag in
  session summary.
- User navigates to out-of-scope host: skip that poll's caido_delta, retain
  browser-side dump (still useful for hostname / external-resource recon).
