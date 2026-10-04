---
name: verify
description: Run the full ChefFlow verification protocol - spec audit, build integrity, production parity, and Playwright pressure testing.
user-invocable: true
---

# ChefFlow Verification Protocol

The system is considered fully up to date and complete. Your job is to prove that claim, not trust it.

Do not ask questions. Do not stop early. Run all phases autonomously.

## GLOBAL RULES

- No new feature work
- No refactors unless required to fix a verified issue
- Do not trust "marked complete" - verify behavior
- Do not interact with OpenClaw
- Evidence > claims

## PHASE 1 - RECENT WORK INVENTORY

Identify everything completed recently (last 14-30 days).

Pull from:

- `docs/specs/` (check status fields)
- `git log --oneline --since="14 days ago"`
- Recently modified routes and components

Build a structured inventory: feature name, spec reference, files involved, routes, expected behavior.

## PHASE 2 - SPEC TO CODE TO RUNTIME VALIDATION

For each inventory item, verify:

1. Spec exists
2. Code exists
3. Code is wired (routing/navigation)
4. Feature runs in the app
5. Behavior matches spec intent

Classify each: VERIFIED / PARTIAL / MISSING / UNPROVEN

## PHASE 3 - LOCAL BUILD CONFIRMATION

- Confirm dev server on port 3100 responds
- Run `npx tsc --noEmit --skipLibCheck` and capture output
- Verify no stale cache issues

## PHASE 4 - PRODUCTION PARITY

Compare local (localhost:3100) vs production (app.cheflowhq.com):

- Route availability
- UI rendering
- Feature behavior
- Recent changes present

Output: PARITY PASS or FAIL with mismatch list.

## PHASE 5 - PLAYWRIGHT PRESSURE TEST

Sign in using `.auth/agent.json` credentials via `POST http://localhost:3100/api/e2e/auth`.

Test all recently modified surfaces:

- Authentication flow
- Navigation paths
- Forms and submissions
- Buttons and actions
- Lists/tables
- Modals/drawers
- Route protection
- Refresh/reload behavior
- Empty/error states

Not just happy paths. Attempt breakage. Rapid interactions, refresh mid-flow, back navigation.

DO NOT test OpenClaw-related flows.

## PHASE 6 - ISSUE CLASSIFICATION

Classify findings:

- BLOCKING (prevents core usage)
- CRITICAL (major feature broken)
- MINOR (non-blocking)

Tag each: local-only / production-only / both

## PHASE 7 - SURGICAL FIX PASS (IF NEEDED)

If BLOCKING or CRITICAL issues exist:

- Apply minimal fixes
- Do not expand scope
- Re-run affected tests
- Capture before/after evidence

## PHASE 8 - FINAL REPORT

1. Recent Work Inventory
2. Validation Matrix (spec -> code -> runtime)
3. Local Build Proof
4. Production Parity Results
5. Playwright Test Results
6. Issues Found (classified)
7. Fixes Applied (if any)
8. Final Verdict

Final Verdict must answer:

- Is everything marked complete actually complete?
- Is local fully up to date?
- Is production fully up to date?
- What breaks under real user interaction?
- Is any work still required?
