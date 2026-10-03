---
name: vard-ship
description: Deploy the app, create landing page, set up analytics, and log the shipment
type: ops
version: v0.1
context_intake: artifact_only
---

# VARD Ship

Invoke as `/vard-ship`.

Rapid shipping for VARD experiments. Deploys the app, creates a landing page if needed, wires up basic analytics, and appends to the running ship log.

## Process

1. **Pre-flight:** Confirm the app is buildable and testable locally.
   - Read the vard-align doc for scope and success metrics.
   - Run the build. Fix blockers.
   - Verify the core feature works end-to-end.
2. **Deploy:**
   - Choose the simplest deployment path (Vercel, Netlify, Cloudflare Pages, GitHub Pages, or static hosting).
   - Deploy and verify the live URL works.
3. **Landing page:** If the app doesn't have one, create a minimal landing page:
   - Hero with concept pitch
   - CTA (try it / install it / share it)
   - Social meta tags (og:image, og:title, og:description) for shareability
4. **Analytics:** Wire up lightweight analytics if not already present:
   - Page views and unique visitors at minimum
   - Core action tracking (the one thing the app does)
   - Prefer simple solutions (Plausible, Umami, or a single event to an existing provider)
5. **Ship log:** Append entry to `research/vard-ship-log.md`:
   - Date, concept name, live URL
   - Tech stack used
   - Build time (estimated hours)
   - Distribution channels hit on launch day
   - Success metric from alignment doc
   - Status: `launched`
6. **Distribution:** Execute launch-day distribution:
   - Post to identified channels from alignment doc
   - Ensure social sharing works (test og tags render correctly)

## Output

End with:

```md
**Shipped:** <concept name> — <live URL>
**Next work:** monitor traction for 1-2 weeks, then run the VARD traction gate before any AFPS graduation decision
**Recommended next command:** /vard-traction (after monitoring) or /vard-scan (next experiment)
```

## Constraints

- Do not gold-plate. Ship the minimum viable version.
- Do not set up paid infrastructure without user confirmation.
- Do not modify unrelated projects or repositories.
- If deployment fails, report the blocker rather than switching to a complex hosting solution.
- Create `research/vard-ship-log.md` with a header if it doesn't exist.

## Default Shipping Contract

Follow the shared shipping contract convention.
