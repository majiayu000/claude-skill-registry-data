---
name: browser-context-infer
description: Infer runtime browser context — CSP, Trusted Types, rendering model, framework family, sandbox iframes. Writes browser_context.json. Run after target-init / js-harvest / passive-listen. Idempotent.
---

# browser-context-infer

## Purpose

A sink's *severity* is fixed, but its *viability* depends on the page
it runs on. `el.innerHTML = userData` is RCE on a no-CSP page,
dangling-markup only on `script-src 'none'`, and inert under enforced
Trusted Types. This skill assembles the page-context evidence we have
and writes `targets/<name>/browser_context.json` for downstream
consumers.

Plan: `plans/ARCHITECTURE_EVOLUTION.md §4`.

## When to run

Run once per target, after at least one of:

- `caido-capture` (real response headers captured),
- `js-harvest` (raw HTML present),
- `passive-listen` (runtime headers captured in `runtime/*/state.json`),
- `js-index` (so Trusted Types policy tags exist in the per-target DB).

Re-run when new evidence lands (e.g. you captured a fresh
`Content-Security-Policy` header you didn't have before).

## Inputs scanned (all optional)

| Source | What it contributes |
|---|---|
| `targets/<name>/raw/_response_headers.txt` / `.json` | Real CSP headers |
| `targets/<name>/raw/*.html` (top-level only) | `<meta http-equiv="CSP">` |
| `targets/<name>/runtime/*/state.json` | passive-listen evidence — headers + policy bodies |
| `targets/<name>/index/frameworks.json` | Framework detection (used by rendering inference) |
| `targets/<name>/db/js_analyzer.db` | `trusted_types_create_policy` tags |

Missing inputs degrade gracefully — every viability factor defaults to 1.0
(no change to chain scoring).

## Steps

1. **Run the driver:**
   ```bash
   python3 bin/infer_browser_context.py <target_name>
   ```
   Output: `targets/<name>/browser_context.json`.

2. **(Optional) Supply a CSP you captured manually:**
   ```bash
   python3 bin/infer_browser_context.py <target_name> \
       --explicit-csp "default-src 'self'; script-src 'self' 'nonce-XXX'; require-trusted-types-for 'script'"
   ```

3. **Enable viability scoring for the next chain extraction:**
   ```bash
   export JS_ENABLE_SINK_VIABILITY=1
   export JS_ENABLE_SANITIZER_REALITY=1        # optional — Sprint A §5 sanitizer reality
   ```
   The reporter (`tlx/modules/js_analyzer/reporter.py`) multiplies the
   chain score by the viability factor and annotates demoted chains
   with `viability_breakdown`. Chains scoring below `JS_VIABILITY_DROP_THRESHOLD`
   (default 0.10) drop out of the hot list.

4. **Sanity-check the output:**
   ```bash
   jq '.csp | {source, raw, unsafe_inline_allowed, unsafe_eval_allowed, trusted_types_required}' \
       targets/<name>/browser_context.json
   jq '.trusted_types' targets/<name>/browser_context.json
   jq '.rendering' targets/<name>/browser_context.json
   ```

## What it produces

`targets/<name>/browser_context.json`:

```json
{
  "csp": {
    "raw": "default-src 'self'; ...",
    "source": "header",
    "script_src": ["'self'", "'nonce-XXX'"],
    "trusted_types_required": true,
    "unsafe_inline_allowed": false,
    "unsafe_eval_allowed": false,
    "confidence": 1.0
  },
  "trusted_types": {
    "enforced": true,
    "policies": ["default", "dompurify"],
    "policy_evidence": [{"qname": "...", "file": "...", "line": 42}]
  },
  "rendering": {
    "model": "ssr_then_csr",
    "framework": "nextjs",
    "hydration": true
  },
  "sandbox_iframes": [],
  "evidence_files": ["raw/_response_headers.txt", "index/frameworks.json"]
}
```

## Boundary conditions

- No CSP evidence anywhere: viability falls back to 1.0 for every sink — no impact on scoring.
- TT enforced + TT-guarded sink (innerHTML etc.): viability factor drops to ~0.05.
- `script-src 'none'` without `unsafe-eval`: eval-family sinks drop to ~0.05; html-parser sinks stay at ~0.20 (CSS injection / dangling-markup still possible).
- Framework override: `dangerouslySetInnerHTML` under React keeps 1.0 (explicit opt-out); `angular_inner_html_binding` without bypass drops to 0.4 (Angular sanitizes by default).

## Idempotency

Safe to re-run. The output file is fully regenerated each time. No
state mutation outside `targets/<name>/`. No network. No LLM. No DB
writes other than reads.

## Failure modes

- Missing per-target DB: Trusted Types policy info is skipped, everything else proceeds.
- Malformed JSON in `runtime/*/state.json`: that file is skipped, others continue.
- Empty `raw/`: only meta-CSP is unavailable; header inputs still work.
