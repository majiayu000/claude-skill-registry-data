---
name: vercel-qa
description: Senior human-style UAT and product QA for Vercel-deployed Next.js + Supabase apps. Use when Nick asks to test an app, QA a deploy, check for bugs, run E2E/UAT, smoke test, validate signup/login flows, test a feature, or assess whether a URL is ready for users. Always start by understanding the product and source code before browser testing when code is available.
---

# Vercel QA

Run deep product-aware QA for Vercel-deployed apps.

## Hard rule: Phase 0 always first

Before clicking through the app, understand what the product is supposed to do.

If source code is available:
1. Read the codebase structure
2. Identify app purpose
3. Identify user roles
4. Identify core flows for each role
5. Identify key entities and data relationships
6. Compare what should exist vs what actually exists
7. Flag **product gaps** before runtime testing starts

If source is not available:
- infer the product map from landing pages, navigation, UI copy, auth screens, dashboard structure, and API behavior
- say clearly that the product map is inferred from the live app only

## Testing phases

### Phase 0 — Product map
Create:
- app purpose
- target user(s)
- roles
- main flows per role
- main entities/data relationships
- expected features vs actual features

Flag **product gaps** separately from bugs.

### Phase 1 — First impression
Check:
- clear value proposition
- clear CTA
- trust signals
- broken images
- placeholder/demo text
- whether a real user would trust the app

### Phase 2 — Route coverage
Visit all reachable routes.
Check:
- route loads without errors
- meaningful content exists
- mobile responsiveness at 375px
- console errors
- context makes sense
- use route crawler when helpful

### Phase 3 — Auth
Test exhaustively:
- signup per role
- missing role support as product gap
- login
- password reset
- logout
- session persistence
- empty fields
- invalid email
- short password
- valid data

### Phase 4 — Deep functional testing
Test:
- happy paths with realistic data
- unhappy paths
- duplicate submits
- rapid clicks
- XSS-style input attempts
- create/update/delete propagation
- full journey per role

### Phase 5 — Cross-feature interactions
Check:
- feature-to-feature data flow
- filters/search/sort
- notifications or downstream effects

### Phase 6 — Edge cases
Check:
- empty states
- long content
- special characters like O’Brien, José, emojis
- back button
- deep linking
- image uploads
- mobile touch interactions

### Phase 7 — Visual and UX polish
Check:
- loading states
- success/error feedback
- styling consistency
- accessibility basics
- form preservation on error

## Platform-specific checks

### Supabase
Check:
- auth error messaging
- obvious RLS leakage signs
- `NEXT_PUBLIC_` config issues showing as undefined
- realtime behavior if present
- profile/bootstrap issues after signup

### Vercel
Check:
- preview vs production env mismatches if visible
- cold start symptoms
- next/image behavior
- API route responsiveness
- favicon/logo/metadata basics
- 404/500 behavior

## Execution

Use `playwright-skill-safe` for browser execution.

Store screenshots in:

```bash
/tmp/qa-screenshots/
```

Always capture screenshots at every meaningful step.

For consistent runs, initialize a structured QA workspace first:

```bash
bash "$SKILL_DIR/scripts/init_qa_run.sh" <run-name>
```

Generate starter tasks with:

```bash
node "$SKILL_DIR/scripts/generate_playwright_task.js" <url> <mode> <outFile> <shotsDir>
```

Useful helper scripts:

```bash
node "$SKILL_DIR/scripts/crawl_routes.js" <url> [outFile]
node "$SKILL_DIR/scripts/generate_role_test_plan.js" [outFile] [rolesCsv]
node "$SKILL_DIR/scripts/create_bug_artifact.js" [outDir] [title]
node "$SKILL_DIR/scripts/write_uat_report.js" <report.json> [outFile]
```

Modes:
- `smoke`
- `responsive`
- `auth`

Then refine the generated task for the actual product and execute it with `playwright-skill-safe`.

## Modes

### Quick test mode
If Nick says **quick test**, only do:
- Phase 0
- Phase 1
- Phase 3
- Phase 4 happy path

### Post-deploy mode
If Nick says **just deployed**, only do:
- Phase 1 smoke
- Phase 4 happy path
- keep under 5 minutes

## Output format

```text
🧪 UAT REPORT: [App Name] — [URL]

📋 PRODUCT MAP
...

🚨 PRODUCT GAPS
...

❌ BUGS
...

⚠️ UX ISSUES
...

✅ PASSED
...

📊 SUMMARY
...

🏁 VERDICT
READY FOR USERS / NEEDS WORK / NOT READY

📎 SCREENSHOTS
...
```

## Severity
- Critical = unusable or data/security risk
- Major = key flow broken
- Minor = cosmetic or annoyance

## References
- Read `references/checklists.md` before running a deep QA pass
- Read `references/report-template.md` when writing the final report
- Read `references/playwright-patterns.md` when generating QA automation scripts
- Read `references/execution-workflow.md` for the step-by-step run structure
- Read `references/advanced-checks.md` for stronger Supabase/Vercel/accessibility/regression checks

## Bundled scripts
- `scripts/init_qa_run.sh` — create temp QA workspace and starter reports
- `scripts/generate_playwright_task.js` — generate starter Playwright task for smoke/responsive/auth checks
- `scripts/crawl_routes.js` — discover internal routes from the live app
- `scripts/generate_role_test_plan.js` — scaffold role-based QA coverage
- `scripts/create_bug_artifact.js` — create a per-bug artifact template
- `scripts/write_uat_report.js` — render final markdown report from JSON findings
