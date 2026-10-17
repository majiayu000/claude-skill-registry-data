---
name: mythos-reaper
description: "Mythos-style audit harness built into bountyreaper — one engine, two modes. WHITE-BOX (source in scope): rank every file 1-5 by sink density, audit top files, Gate A: a finding only counts if a probe TRIGGERS it. BLACK-BOX/GRAY-BOX (no source): build a threat model from recon inventory, same Gate A promotion discipline. Findings are promoted only by probe evidence, never by agent assertion."
category: "methodology"
version: "1.0"
author: "bountyreaper-built-in"
tags:
  - mythos
  - gate-a
  - threat-model
  - whitebox
  - graybox
  - validation
tech_stack:
  - web
  - api
  - source-audit
cwe_ids:
  - CWE-22
  - CWE-79
  - CWE-89
  - CWE-287
  - CWE-639
  - CWE-862
  - CWE-918
chains_with:
  - attack-403-bypass
  - attack-idor-automation
  - attack-javascript-recon
  - attack-open-redirect
prerequisites:
  - burp (optional, for traffic visibility)
---

# mythos-reaper

## Objective

Run the Mythos methodology (Anthropic Mythos Preview clone, adapted through
mini-mythos → mythos-web) **natively in bountyreaper**, with one engine and
two entry modes:

```
WHITE-BOX (source available)                BLACK-BOX (no source)
─────────────────────────────               ─────────────────────────
1. score source tree (sink density)         1. recon inventory → threat model
2. queue top files, audit each              2. refine queue into attack
   with full instrumentation                   hypotheses + probe specs
3. candidate → write probe spec             3. candidate → write probe spec
4. GATE A: baseline vs exploit delta        4. GATE A: baseline vs exploit delta
   + sink fires (events/OOB)                   + sink fires (events/OOB)
5. PASS → findings ledger                   5. PASS → findings ledger
   FAIL → hypothesis stays unverified         FAIL → hypothesis stays unverified
```

**Gate A is non-negotiable.** A candidate only becomes a finding when an
actual probe produces a controlled delta (exploit response ≠ baseline, not
explainable by it) and the intended sink fires. No "confirmed" without a
response.

## Tool Calling (MCP)

The engine ships as the bundled `mythos-reaper` MCP server
(`mcp/mythos-reaper/` in the repo; enable in bountyreaper.json `mcp` block):

| Tool | Mode | Purpose |
|---|---|---|
| `mythos_score_source(root, src_dir?, top?, min_score?)` | white-box | Rank source files 1-5 by sink density → `scores.json` |
| `mythos_build_threat_model(target, inventory \| inventory_json, top?)` | black-box | Recon inventory → ranked threat model → `threat-model.json` |
| `mythos_refine_queue(target, entries_json)` | both | Persist your hypotheses + probe_refs back into the queue |
| `mythos_probe(target, spec_json, base_url, events_log?, hypothesis?)` | both | **Gate A execution** → verdict + audit ledger |
| `mythos_log_event(target, sink, detail_json?, oob?)` | both | Record a sink/OOB event for correlation |
| `mythos_promote_finding(target, finding_json)` | both | Promote to findings — **refuses without probe PASS** |
| `mythos_gate_status(target)` | both | Ledger readback: audits, PASS/FAIL, findings |
| `mythos_oob_issue(callback_base?)` | blind | Issue canary for blind SSRF/XXE/cache |
| `mythos_oob_poll(canary, sink, callback_base?)` | blind | Correlate callbacks → oob events |

Ledger default: `mcp/mythos-reaper/runs/targets/<target>/`. Override with the
`MYTHOS_REAPER_RUNS` env var (set it in your MCP config env or shell).

## Workflow

### Step 0 — Mode selection

```
Source in scope (GitHub program, vendor source given, JS bundles fully
reconstructed)?  → WHITE-BOX path.
Only a live target? → BLACK-BOX path: recon first (inventory JSON), then
threat model, then treat the target as GRAY-BOX from there on (the rest of
the workflow is identical).
```

### Step 1a — White-box: score

```
mythos_score_source(root="/path/to/src", src_dir="src", min_score=3)
```
Work the queue top-down. For each file, hunt for the sinks the scorer named.

### Step 1b — Black-box: threat model

```
1. recon → collect endpoint inventory (urls+params, auth state)
2. mythos_build_threat_model(target="<name>", inventory_json='<...>')
3. Read the queue. For each rank, write a concrete hypothesis and a probe
   spec, then mythos_refine_queue to persist them.
```

The threat model's `vuln_class_density` tells you which CWE classes dominate
this target's surface — prioritise those attack skills.

### Step 2 — Probe specs

Every hypothesis needs a probe spec (templates ship in the package under
`mcp/mythos-reaper/probes/`):

```json
{
  "name": "static-path-traversal",
  "mode": "whitebox|graybox",
  "baseline": {"method": "GET", "path": "/index.html"},
  "exploit":  {"method": "GET", "path": "/static/..%2f..%2f..%2fetc/passwd"},
  "expect": {
    "baseline_status": [200],
    "exploit_not_in": [403, 404],
    "exploit_contains": ["root:x:0:0"]
  },
  "sink_window": {"sink": "fs.readFileSync"},
  "oob": {"required": false}
}
```

For BLIND classes (blind SSRF/XXE/cache poisoning): use `mythos_oob_issue`
→ embed the returned URL in the exploit → `mythos_oob_poll`. OOB callback
= sink fired.

### Step 3 — Gate A execution

```
mythos_probe(target="<name>", spec_json='<spec>', base_url="http://127.0.0.1:3000",
             hypothesis="<one-line finding claim>")
```

- **PASS** → candidate may be promoted.
- **FAIL** → check `failed_checks`:
  - `delta_exists` failed → your exploit is indistinguishable from baseline;
    refine the payload, not the report.
  - `sink_reached`/`oob_callback` failed → the sink didn't fire; you may be
    hitting a simulator/fallback path. Instrument or find a different sink.

### Step 4 — Promotion + reporting

```
mythos_promote_finding(target="<name>", finding_json='{
  "title": "...", "cwe_id": "CWE-22", "endpoint": "...", "payload": "...",
  "reproduction_steps": ["..."], "probe_result": <the FULL mythos_probe output>
}')
```

Only promoted findings enter the report. In the report, cite the probe's
baseline/exploit pair verbatim — that is your anti-triage evidence.

## Depth discipline (Critic gate)

Before declaring a target or file "not exploitable":
1. Try every bypass variant for the sink's class (encoding, path
   normalisation differences, proxy quirks).
2. Try sibling endpoints/methods (GET→POST, /v1→/v2, export/import).
3. For FPs: run the baseline check — if the "exploit" result also happens
   without the payload, it is a feature, not a bug.

## Severity discipline

Promoted ≠ high severity. Score what the probe DEMONSTRATED (e.g. reading
`/etc/passwd` from a static handler = High file-read; "could be RCE" is
chain-potential, not the base score).
