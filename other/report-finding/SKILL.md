---
name: report-finding
description: Compose the human-readable writeup for a confirmed TP finding. Generates SARIF (js_export_findings format=sarif), a markdown writeup using the template, and bundles the PoC HTML/curl into findings/<id>/. Run when findings/<id>/confirmed.json exists and the writeup is missing. Stops short of submission — that's a human step.
---

# report-finding

## Purpose
Produce the deliverable. A confirmed bug isn't useful until it's
written up well: clear repro, clear impact, clear remediation.

## Inputs
- `targets/<name>/findings/<id>/confirmed.json`
- `targets/<name>/opus/<id>.md`
- `targets/<name>/findings/<id>/screenshots/*.png`

## Steps
1. Pull verdict + reasoning from `opus/<id>.md`.
2. Pull confirmed evidence from `findings/<id>/confirmed.json`.
3. Generate SARIF: `js_export_findings(target_folder, format="sarif")`
   filtered to just `<id>`. Save as `findings/<id>/<id>.sarif`.
4. Render writeup using template in
   `.claude/skills/report-finding/templates/writeup.md`. Fill:
   - Title (severity + sink kind + target component)
   - Severity (CVSS guess from chain.sink_severity)
   - Impact (one paragraph, concrete consequence)
   - Repro steps (numbered, copy-pasteable)
   - PoC (HTML / curl / browser script)
   - Remediation suggestion
   - References (CWE, OWASP, related wiki pages)
5. Bundle PoC: `findings/<id>/poc.html` + `findings/<id>/poc.curl` if
   relevant. **DOM verification contract (2026-05):** if the PoC is
   HTML/JS, embed `data-verify-*` attributes on the trigger element
   and set `data-verify-result="<canary>"` from inside the
   sink-triggering code. See `bin/poc_verify_contract.js` for the
   exact attribute schema. This lets `browser-confirm` verify the
   exploit deterministically instead of relying on
   screenshot-plus-LLM-judge.

   Minimal contract example for a fragment-XSS PoC:
   ```html
   <a id="trig"
      data-verify-trigger="fragment-xss"
      data-verify-source="url:#hash"
      data-verify-sink="innerHTML"
      href="https://target.example/#<img src=x onerror=__tlxFire()>">click me</a>
   <script>
     function __tlxFire() {
       document.getElementById("trig")
               .setAttribute("data-verify-result", "TLX_XSS_CANARY_<id>");
     }
   </script>
   ```
6. Update `status.json.findings[]` and `status.json.phases.report`.

## Outputs
- `targets/<name>/findings/<id>/<id>.md`
- `targets/<name>/findings/<id>/<id>.sarif`
- `targets/<name>/findings/<id>/poc.*`

## Failure modes
- Screenshots missing → fall back to text-only repro; flag
  `screenshots_missing: true` in report metadata. Don't block.
- SARIF export fails → writeup still ships; SARIF flagged as missing.
- Multiple chains produced the same root-cause finding → cluster
  before report; emit one finding with `merged_chain_ids: [...]`.

## Result block
```json
"phases": { "report": { "status": "done", "ts": "<iso>",
  "id": "...", "files": [...], "ready_to_submit": bool } }
```

## Submission policy
Never auto-submit to HackerOne, Synack, or any platform. (2026-05 —
platform-trust rule; user must read every report before it ships.)
The skill ends with the writeup ready and the user notified. The
user submits.
