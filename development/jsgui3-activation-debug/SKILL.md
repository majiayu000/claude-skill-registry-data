---
name: jsgui3-activation-debug
description: Debug jsgui3 client-side activation issues. Use when SSR renders but clicks don’t work, this.dom.el is null, or you see Missing context.map_Controls / activation failures.
---

# jsgui3 Activation Debug

## Scope

- Diagnose “renders but no interactivity” failures
- Ensure client bundle is current when tests run in a browser
- Add a minimal check script when behavior is unclear

## Inputs

- Which UI server/route/control is affected
- Whether the issue reproduces in E2E (Puppeteer/Playwright)
- Whether client bundling is involved

## Procedure

1. Confirm this is an activation issue, not just CSS/DOM.
2. Follow the documented activation flow and look for the canonical signatures.
3. If E2E is involved, rebuild the client bundle before debugging behavior.
4. If unclear, create a minimal reproduction check under a local `checks/` folder.

## Validation

- Prefer a `node src/ui/**/checks/<name>.check.js` script that exits cleanly.
- Then run the smallest relevant Jest suite via `npm run test:by-path ...`.

## Escalation / Research request

Ask for dedicated research if:

- activation semantics differ between SSR and bundled client unexpectedly
- the issue appears to involve `context.map_Controls` lifecycle gaps across multiple controls

## References

- jsgui3 activation flow: `docs/guides/JSGUI3_UI_ARCHITECTURE_GUIDE.md`
- AGENTS.md quick anchor (“Client-side activation flow critical”)
- Fast browser verification (single browser, many scenarios): `docs/guides/PUPPETEER_SCENARIO_SUITES.md`
