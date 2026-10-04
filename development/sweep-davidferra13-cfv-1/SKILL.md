---
name: sweep
description: Batch-verify PARTIAL build queue items via Playwright. Reads UNIFIED-BUILD-QUEUE.md, filters PARTIAL items needing verification, runs Playwright against each route, marks DONE or flags failures. Use when user says /sweep, "verify partials", "what needs testing", "batch verify", or after a swarm session produces many PARTIAL items.
---

# SWEEP (Batch Verification of PARTIAL Items)

## Purpose

Take all PARTIAL items from the build queue that say "Needs Playwright verification" and systematically verify them. Move verified items to DONE. Flag failures with details.

## Procedure

### Phase 1: Inventory

1. Read `docs/UNIFIED-BUILD-QUEUE.md`
2. Extract all rows with status `PARTIAL`
3. Filter to items containing "Needs Playwright verification" or "needs verification"
4. Sort by priority (P0 > P1 > P2) then by dependency order
5. Report count: "Found N items needing verification"

### Phase 2: Pre-Flight

1. Confirm dev server running at `http://localhost:3100`
2. Confirm agent auth exists (`.auth/agent.json`)
3. If server down: start it, wait for ready
4. If auth expired: regenerate via `scripts/generate-agent-auth.mjs`

### Phase 3: Verify Each Item

For each PARTIAL item:

1. Identify the route(s) affected from the item description
2. Navigate to route via Playwright
3. Verify:
   - Page loads without errors (no console errors, no 500s)
   - Key UI elements from the item description are present
   - No broken layouts or missing data
   - Interactive elements respond (buttons, forms)
4. Take screenshot as evidence
5. Record result: PASS or FAIL with details

### Phase 4: Update Queue

1. Items that PASS: update status from `PARTIAL` to `DONE` in build queue
2. Items that FAIL: keep as `PARTIAL`, append failure details to Notes column
3. Items that can't be verified (no route, backend-only): mark with "Verified: logic-only, no UI route"

### Phase 5: Report

Output summary table:

```
## Sweep Results [date]
| # | Item | Result | Notes |
|---|------|--------|-------|
```

Plus: "Verified X/Y items. Z failures need attention."

## Constraints

- Never mark DONE without actual browser verification
- If a migration hasn't been applied, skip that item (note: "blocked on migration")
- Max 10 items per sweep (avoid timeout). If more, run in batches.
- Screenshot every verification (save to `reports/sweep/`)

## Anti-Patterns

- Marking DONE based on "code looks right" without browser check
- Skipping items because they seem trivial
- Running against stale build (rebuild if last build >24h)
