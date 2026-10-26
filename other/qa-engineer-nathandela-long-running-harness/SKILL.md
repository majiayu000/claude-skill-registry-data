---
name: QA Engineer
description: Hands-on QA testing of running applications via browser automation. Use whenever the user asks to test a running app, perform exploratory testing, verify UI/UX behavior, check accessibility, test forms and inputs, inspect network requests, do a smoke test, or systematically try to break things. Also use when review needs runtime verification beyond automated tests -- visual checks, boundary inputs, interaction flows, and design review against a live application. Triggers on phrases like "test this app", "QA this", "check the UI", "try to break it", "smoke test", "does this look right", "test the form", "check accessibility", "poke at it", or any request to manually verify a running web application or API.
---

# QA Engineer Skill

## Overview

Perform hands-on quality assurance against a running application. This skill covers what automated unit/integration tests miss: visual correctness, interaction flows, boundary inputs, accessibility, and exploratory "break things" testing. The output is a structured QA report with P0-P3 findings.

The skill works by controlling a real browser (Playwright) against a live application instance. Think of it as a systematic manual tester, but automated.

## Decision Tree

```
User task --> What type of target?
|
+-- Web UI --> Is a dev server already running?
|   |
|   +-- Unknown/No --> Detect framework and start server
|   |                  Wait for HTTP readiness (not just TCP)
|   |                  Then proceed to Reconnaissance
|   |
|   +-- Yes (user gave URL) --> Proceed to Reconnaissance
|
+-- HTTP API (no UI) --> API Reconnaissance
|   1. Probe documented endpoints (OpenAPI, README, route files)
|   2. Test response contracts (status codes, schemas)
|   3. Boundary and error testing (malformed input, auth edge cases)
|   4. Report findings
|
+-- CLI / Library (no server) --> SKIP
    Report: "QA Engineer skipped: no runtime target (CLI/library project)"
```

## Phase 1: Server Lifecycle

If no server URL is provided, detect the project type and start the dev server.

**Detection priority** (check in order):
1. User-provided URL --> use it directly
2. `package.json` scripts --> `npm run dev` or `npm start`
3. Framework markers: `vite.config.*` (port 5173), `next.config.*` (3000), `angular.json` (4200)
4. Python: `manage.py` (Django, 8000), `app.py` (Flask, 5000), `main.py` (FastAPI, 8000)
5. Go: `main.go` with `http.ListenAndServe` (8080)
6. Static HTML: `python3 -m http.server 8000`

**Readiness check**: HTTP GET to the root path, not TCP socket polling. A server accepting TCP connections may still be initializing and returning 503s. Poll every 1s, timeout after 30s. If startup fails, report **P1/INFRA** with stderr output and remediation suggestions.

Start the server in background (`run_in_background: true`). Remember to clean up at the end.

## Phase 2: Reconnaissance (Observe Before Acting)

Before any testing, build a complete picture of the application state. This phase is non-negotiable for dynamic apps -- guessing selectors from source code breaks on client-rendered apps.

1. **Navigate** to the target URL
2. **Wait** for `networkidle` (zero network connections for 500ms -- this is when SPAs finish their initial render)
3. **Capture** across all channels:
   - **Visual**: Full-page screenshot (Claude can read this as a multimodal image)
   - **DOM**: Page content / element enumeration
   - **Console**: Attach `page.on('console')` and `page.on('pageerror')` listeners BEFORE navigation
   - **Network**: Attach `page.on('request')` and `page.on('response')` listeners to log API calls
4. **Discover** interactive elements:
   ```javascript
   // Enumerate what's on the page
   const buttons = document.querySelectorAll('button, [role="button"], input[type="submit"]');
   const forms = document.querySelectorAll('form');
   const inputs = document.querySelectorAll('input, textarea, select');
   const links = document.querySelectorAll('a[href]');
   const navs = document.querySelectorAll('nav, [role="navigation"]');
   ```
5. **Report** what was discovered before proceeding to testing

This reconnaissance output feeds into the test strategy. If the page has forms, run boundary testing. If it has navigation, test all routes. If it has interactive elements, test their behavior.

## Phase 3: Test Execution

Select test strategies based on what reconnaissance discovered. Not every strategy applies to every page -- use judgment.

### Strategy 1: Smoke Testing
Verify the basics work:
- Page loads without console errors
- Main content is visible (not a blank white page)
- Navigation links resolve (no 404s)
- Images load (no broken image icons)
- Key interactive elements are present and visible

### Strategy 2: Exploratory Testing (Break Things)
Systematically probe for failures. Read `.claude/skills/compound/qa-engineer/references/exploratory-testing.md` for the full playbook. In brief:
- **Boundary inputs**: empty strings, maximum-length strings, special characters, SQL injection strings, XSS payloads in form fields
- **State manipulation**: back button mid-flow, refresh during submission, double-click submit, navigate away and return
- **Auth edge cases**: access protected routes without login, expired session behavior
- **Error paths**: invalid URLs, missing required fields, server errors
- **Viewport stress**: extreme widths (320px mobile, 2560px ultrawide), zoom levels

### Strategy 3: Visual Review
Use Claude's multimodal vision to evaluate the UI:
- Layout alignment and spacing consistency
- Text readability (contrast, font size, truncation)
- Responsive behavior across breakpoints (375px, 768px, 1024px, 1440px)
- Dark mode / light mode if supported
- Loading and error states appearance

### Strategy 4: Accessibility Testing
Run axe-core if available, otherwise check manually:
- Color contrast ratios (WCAG 2.1 AA: 4.5:1 for normal text, 3:1 for large text)
- Keyboard navigation (Tab through all interactive elements, check focus indicators)
- ARIA labels on buttons and form fields
- Alt text on images
- Form label associations
- Heading hierarchy (h1 -> h2 -> h3, no skipped levels)

### Strategy 5: Form and Input Testing
For each form discovered:
- Submit with all fields empty
- Submit with valid data (happy path)
- Submit with invalid data per field (wrong types, too long, too short)
- Test paste behavior
- Test autofill behavior
- Check validation messages (are they helpful? do they appear?)

### Strategy 6: Network Inspection
Review captured network traffic:
- API calls returning 4xx/5xx errors
- Excessive API calls (N+1 queries visible as repeated requests)
- Missing CORS headers
- Slow responses (> 2 seconds)
- Unencrypted requests (HTTP instead of HTTPS in production)
- Sensitive data in URLs or query parameters

## Phase 4: Report

Produce a structured QA report with findings classified by severity:

```markdown
## QA Report: [App Name / URL]

**Target**: [URL tested]
**Date**: [timestamp]
**Strategies applied**: [list of strategies used]

### P0 Findings (Blocks Ship)
- Security vulnerability found at runtime
- Application crashes on valid user input
- Data loss scenario

### P1 Findings (Critical)
- Feature does not work as expected
- Accessibility violation (WCAG AA)
- Server errors (5xx) on normal flows
- Infrastructure failure (app won't start)

### P2 Findings (Important)
- Visual bugs (misalignment, truncation, broken layout)
- Poor error messages
- Missing form validation
- Slow responses (> 2s)

### P3 Findings (Minor)
- Cosmetic issues
- Console warnings (non-error)
- Minor UX improvements

### Passed Checks
[List what was tested and passed -- evidence that QA was thorough]

### Screenshots
[Reference screenshots taken during testing]
```

Each finding includes: **what** (the problem), **where** (URL + selector/element), **how to reproduce** (steps), and **severity justification**.

## Phase 5: Cleanup

1. Stop any background dev server processes
2. Delete temporary test files
3. Save the QA report to `docs/qa/` or present inline

## Integration with Review Phase

When invoked as part of the review skill (not standalone):
- Findings merge into the review's P0-P3 classification
- Communicate findings via `SendMessage` to the review lead
- Follow the same format as other reviewer agents
- Respect the review timeout (5min suite max)

## Using Testing Constitutions (Optional)

For repeated QA of the same pages, you can define test constitutions -- persistent JSON files that describe what to test. Read `.claude/skills/compound/qa-engineer/references/constitution-schema.md` for the format. Constitutions are optional -- the skill works without them by using auto-discovery from the reconnaissance phase.

## Browser Automation Patterns

For detailed Playwright patterns (selectors, screenshots, console capture, network interception, viewport emulation), read `.claude/skills/compound/qa-engineer/references/browser-automation.md`.

Key principles from that reference:
- Use Playwright **library APIs** (write and execute scripts), not browser MCP tools
- Prefer text-based and role-based selectors over CSS classes or IDs
- Always wait for `networkidle` before inspecting or acting
- Capture console logs and network requests from the start (attach listeners before navigation)
- Run headless by default for speed; switch to headed for debugging

## Relationship with Runtime Verifier

The runtime-verifier agent (`.claude/skills/compound/agents/runtime-verifier/SKILL.md`) also tests running applications, but serves a different purpose:

| | **Runtime Verifier** | **QA Engineer** |
|---|---|---|
| **Invocation** | Automatic during review (step 7) for web/API projects | On-demand (step 8), when visual/UI changes warrant it |
| **Approach** | Generates ephemeral Playwright **test files**, runs via `npx playwright test` | Writes standalone **scripts**, drives browser interactively |
| **Focus** | API contracts, smoke tests, regression | Exploratory testing, visual review, accessibility, boundary inputs |
| **Output** | Structured test results (pass/fail per test) | QA report with findings + screenshots |

When both are active during a review, they complement each other. Runtime-verifier covers automated contract verification; QA Engineer covers what automation misses (visual bugs, UX issues, edge cases that need human-like exploration). Deduplicate overlapping findings at review consolidation (step 11).

## Graceful Degradation

| Scenario | Behavior | Severity |
|----------|----------|----------|
| No web/API framework detected | SKIP, report informational | P3/INFO |
| App fails to start | Report with stderr diagnostics and remediation | P1/INFRA |
| Playwright not installed | Attempt `pip install playwright && playwright install chromium`, retry once | P1/INFRA if still fails |
| Reconnaissance finds zero interactive elements | Run smoke testing only (page load, console errors, screenshots), note limited scope | P3/INFO |
| Screenshot fails to save | Log warning, continue testing without visual evidence | P3 |
| Timeout exceeded (review: 5min, standalone: 10min) | Stop testing, report partial results + timeout finding | P2 |
| Dev server crashes mid-test | Detect via next failed navigation, report P1/INFRA, stop | P1/INFRA |

## Common Pitfalls
- Starting tests before the server is ready (use HTTP readiness check, not TCP)
- Guessing selectors from source code instead of discovering them from the live DOM
- Not attaching console/network listeners before navigation (misses initial load errors)
- Testing only the happy path (the value of QA is finding what breaks)
- Reporting visual issues without screenshots (always include evidence)
- Running the full strategy suite on a trivial change (match QA depth to change scope)
- Not cleaning up background server processes
- Confusing QA Engineer with runtime-verifier (see Relationship table above)

## Quality Criteria
- Reconnaissance completed before any testing
- At least smoke testing + one additional strategy applied
- All findings classified P0-P3 with reproduction steps
- Screenshots included for visual findings
- Console errors captured and reported
- Passed checks documented (evidence that QA was thorough, not just failure-focused)
- Server processes cleaned up after testing
- Report is actionable (each finding has enough detail to fix)
