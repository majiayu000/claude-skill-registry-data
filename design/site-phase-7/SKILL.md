---
name: site-phase-7
description: >-
  Phase 7 — Automated quality loop: playwright-validate.py score >= 9.0,
  34-criteria system, blueprint adherence, performance, SEO audit.
  Visual review is handled separately by Phase 7b.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
model: opus
effort: high
context: fork
user-invocable: false
---

# Phase 7 — Automated Quality Loop

This is a LOOP. Do NOT exit until ALL automated conditions are satisfied.
Visual analysis is handled by Phase 7b (separate agent with fresh context).

## Objective

Validate the built site across automated scoring, blueprint adherence, performance, and SEO — looping until every automated gate passes. This phase focuses on TECHNICAL quality. Visual quality and enchantment are evaluated in Phase 7b.

## Pre-Gate

```bash
.claude/scripts/gate-quality-loop.sh $LEAD_ID --pre
```

If the pre-gate fails (mapa-encantamento.md missing), STOP. Return to Phase 3.

## Gate 1 — Automated Score >= 9.0

Start dev server in background:
```bash
cd /Users/felipemoreiralanna/Documents/GitHub/vendedor-de-sites-v2/sites/$LEAD_ID && npm run dev
```
(Use `run_in_background: true`. Wait 5 seconds.)

Run validation (31 automated UX/UI checks, score 0-10):
```bash
cd /Users/felipemoreiralanna/Documents/GitHub/vendedor-de-sites-v2
.venv/bin/python sites/_templates/playwright-validate.py http://localhost:5180 sites/$LEAD_ID/screenshots
```

If score < 9.0 (exit code 1):
1. Read EVERY red-CRITICAL and FAIL item
2. Fix in code
3. Kill server: `pkill -f "vite.*5180" 2>/dev/null; true`
4. Restart: `cd sites/$LEAD_ID && npm run dev` (background)
5. Re-run script
6. **LOOP until score >= 9.0**

## Gate 1.1 — 34-Criteria System

Load the complete criteria reference:
```
Read: sites/_templates/visual-review-criteria.md
```

The playwright-validate.py script scores 31 automated criteria. You must also evaluate criteria 32-34 manually:

Load rubrics:
```
Read: sites/_templates/quality-rubric.md
```

Apply criteria 32 (Visual Originality), 33 (Desktop Professionalism), 34 (Mobile Professionalism).

**Approval rules:**
- EVERY one of the 34 criteria >= 8
- Average of all 34 >= 9.0
- ANY originality criterion (29, 30, 32) < 8 → FAIL
- ANY critical criterion = 0 → STOP immediately

## Gate 1.2 — Blueprint Adherence

Read: `sites/$LEAD_ID/mapa-encantamento.md`

For EACH section in the blueprint, verify:
1. Was the specified LAYOUT implemented in code?
2. Does the specified ANIMATION exist in the component?
3. Was the VISUAL TECHNIQUE applied?

If ANY section diverges from the blueprint → FIX and re-validate.

## Gate 1.5 — Performance Profiling (optional)

**Only execute if Chrome DevTools MCP is connected** (Chrome running with `chrome-debug`).

| Metric | Good | Acceptable | Action if exceeded |
|--------|------|------------|-------------------|
| LCP | < 2.5s | < 4.0s | Optimize blocking assets |
| CLS | < 0.1 | < 0.25 | Fix layout shifts |
| INP | < 200ms | - | Reduce JS blocking |

If Chrome DevTools NOT available: skip and log "Gate 1.5 skipped — Chrome DevTools not available."

## Gate 4 — SEO Audit

After Gates 1-1.5 pass, invoke: `/seo page http://localhost:5180`

For EACH issue found:
1. Fix in code (meta tags, schema, headings, alt text, hreflang, sitemap, etc.)
2. Re-run `/seo page http://localhost:5180` to confirm
3. **LOOP until SEO Health Score has zero criticals**

After SEO fixes, re-run playwright-validate.py to confirm score >= 9.0 STILL holds. Re-validate mobile.

## Server Cleanup

Kill dev server when exiting: `pkill -f "vite.*5180" 2>/dev/null; true`

**NOTE:** Do NOT kill the server if Phase 7b will run immediately after — leave it running for the visual review agent.

## Constraints

| Constraint | Enforced by |
|---|---|
| Score >= 9.0 | playwright-validate.py exit code |
| All 34 criteria >= 8 | Criteria check + visual-review-criteria.md |
| Blueprint adherence | Manual section-by-section check |
| SEO no criticals | /seo page audit |
| Mobile parity | Every fix requires mobile re-validation |

## Exit Criteria

ALL must be TRUE:

- [ ] **Gate 1:** Automated score >= 9.0, zero CRITICAL checks
- [ ] **Gate 1.1:** All 34 criteria >= 8, average >= 9.0
- [ ] **Gate 1.2:** Every blueprint section faithfully implemented
- [ ] **Gate 1.5:** CWV within limits OR "skipped — Chrome DevTools not available"
- [ ] **Gate 4:** SEO audit with zero criticals, fixes re-validated
- [ ] Dev server left running for Phase 7b (or killed if orchestrator handles restart)
