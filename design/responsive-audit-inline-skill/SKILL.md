---
name: responsive-audit-inline-skill
description: >-
  In-session responsive audit delegate — wraps the
  playwright-responsive-audit-skill inline loop (detect → fix → re-verify) for
  current-diff frontend changes. Decision tree with skip rules, scope bounds,
  enforcement deltas, and output contract. Triggers: inline responsive audit,
  viewport check in-session, plan-execution-inline-skill responsive step.
license: Apache-2.0
compatibility: opencode
metadata:
  mirrors: responsive-audit-subagent
category: Responsive & Visual Testing
---

# Responsive audit (inline)

You are executing the responsive-audit delegate's workflow **in this session**
via the `playwright-responsive-audit-skill` inline loop — load that skill for
the capture/fix tiers; this skill supplies the decision tree and discipline.

## Decision tree

1. **Skip check (all must hold to skip):**
   - No `playwright.config.*` + no `@playwright/test` in the project → report
     "Playwright not configured — skipping (never install unprompted)", stop.
   - The diff touches no frontend surface (`components/**/*.{tsx,jsx,vue,
     svelte}`, `app|pages|routes|src/ui`, rendered-route handlers) → report
     "no frontend surface in diff", stop.
2. **Load** `playwright-responsive-audit-skill` and run its detect tier:
   mobile/tablet/desktop viewports against the diff's affected pages.
3. **Fix tier:** auto-fixable defects (missing viewport meta, unbounded widths,
   overflow) fixed directly; layout-judgment defects reported, not guessed.
4. **Re-verify tier:** re-capture only the fixed viewports/pages.

## Scope bounds

- Pages affected by the current diff only. No whole-site sweeps.
- Fixes touch frontend files in the diff's blast radius; new dependencies are
  findings, never installs.

## Enforcement deltas (vs responsive-audit-subagent)

| Subagent enforcement | Inline discipline (you) |
|---|---|
| Background execution + timeout model | Runs block this session — state the capture plan first; abort and report if capture exceeds a reasonable interactive wait |
| Fresh context per audit | Restate the affected-pages list before capturing so scope drift is visible |
| Tier model (vision) | Same model as the caller — if you cannot assess the screenshots, report inconclusive instead of guessing |

## Output contract

**Status:** [success | partial | failed | skipped]
**Output:** viewports × pages captured, defects found/fixed/reported (file:line), skip reason if any
**Summary:** ≤3 sentences
**Issues:** inconclusive captures, environment gaps, or "None"
