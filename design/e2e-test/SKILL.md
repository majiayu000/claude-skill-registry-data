---
name: e2e-test
description: Run end-to-end browser tests on a web application. Use when the user says "test the app", "e2e test", "run end-to-end tests", "test all user flows", "verify the UI works", "check for bugs", "test everything before review", or wants to validate a web app works correctly after implementation.
---

# End-to-End Application Testing

Test every user journey in a web application using browser automation, screenshot verification, and database validation.

## Pre-flight Checks

### 1. Platform

agent-browser requires Linux, WSL, or macOS.
```bash
uname -s
```
If the output is `MINGW`, `CYGWIN`, or similar (native Windows), stop:
> "agent-browser requires Linux, WSL, or macOS. Please run from WSL or a compatible environment."

### 2. Frontend Detection

Verify the app has a browser-accessible UI by checking for a dev/start script in `package.json`, framework files (`pages/`, `app/`, `src/components/`, `index.html`), or web server config.

If no frontend exists, stop:
> "No browser-accessible frontend detected. E2E browser testing requires a UI. For API-only testing, use a different approach."

### 3. agent-browser Setup

```bash
agent-browser --version || npm install -g agent-browser
agent-browser install --with-deps
```

The `--with-deps` flag installs Chromium dependencies on Linux/WSL. Harmless on macOS. If installation fails, stop with manual install instructions.

## Phase 1: Parallel Research

Launch three sub-agents simultaneously to research the codebase. If the Task tool (TaskCreate/TaskUpdate) is available, use it to manage these as tracked tasks. Otherwise, use standard sub-agent invocations. The research phase works either way.

### Sub-agent 1: Application Structure & User Journeys

Research and return:
1. **Startup commands** -- exact install + dev server commands, URL, and port
2. **Authentication** -- how to log in or create test accounts (check `.env.example` for credentials, seed data, or sign-up flow). Note the auth type: simple login form, OAuth/SSO, magic link, etc.
3. **Every route/page** -- URL paths and what they render
4. **Every user journey** -- complete flows with steps, interactions, and expected outcomes
5. **Interactive elements** -- forms, modals, dropdowns, pickers, toggles needing testing

### Sub-agent 2: Database Schema & Data Flows

Research and return (read `.env.example`, never `.env`):
1. **Database type and connection** -- DB engine and env var name for the connection string
2. **Full schema** -- tables, columns, types, relationships
3. **Data flows per action** -- what records each user action creates/updates/deletes
4. **Validation queries** -- exact queries to verify correctness after each action

### Sub-agent 3: Bug Hunting

Analyze for potential issues:
1. **Logic errors** -- bad conditionals, null checks, race conditions
2. **UI/UX issues** -- missing error handling, loading states, accessibility
3. **Data integrity** -- missing validation, orphaned records, cascade issues
4. **Security** -- injection, XSS, missing auth checks

Return a prioritized list with file paths and line numbers.

**Wait for all three to complete before proceeding.**

## Phase 2: Start the Application

Using Sub-agent 1's startup instructions:

1. Install dependencies if needed
2. Start the dev server in the background (e.g., `npm run dev &`)
3. Wait for the server to be ready
4. Open: `agent-browser open <url>` and confirm it loads
5. Screenshot: `agent-browser screenshot e2e-screenshots/00-initial-load.png`

### Handling Auth

Choose the right strategy based on Sub-agent 1's auth findings:

- **Simple login form**: Fill credentials and submit before testing protected routes
- **OAuth/SSO**: Check if the app has a dev/test bypass mode, test-user seeding, or API-based auth. If OAuth is the only option and there is no bypass, test only public routes and note the limitation
- **Magic link / email-based**: Look for a dev mailbox or test mode that auto-confirms. If unavailable, test public routes only
- **No auth**: Proceed directly

## Phase 3: Organize Test Plan

If TaskCreate is available, create a task per user journey with the journey name, steps, and expected outcomes. Also create a responsive testing task.

If TaskCreate is not available, list all journeys to test and work through them sequentially. The testing process is the same either way.

## Phase 4: Execute Tests

For each journey, mark it in-progress (if using tasks) and execute the following.

### 4a. Browser Interaction

Core agent-browser commands:
```
agent-browser open <url>              # Navigate
agent-browser snapshot -i             # Get interactive refs (@e1, @e2...)
agent-browser click @eN               # Click
agent-browser fill @eN "text"         # Clear + type
agent-browser select @eN "option"     # Dropdown select
agent-browser press Enter             # Keypress
agent-browser screenshot <path>       # Save screenshot
agent-browser screenshot --annotate   # Screenshot with labeled elements
agent-browser set viewport W H        # Resize viewport
agent-browser wait --load networkidle # Wait for network idle
agent-browser console                 # JS console output
agent-browser errors                  # Uncaught exceptions
agent-browser get text @eN            # Element text
agent-browser get url                 # Current URL
agent-browser close                   # End session
```

**Refs become stale after navigation or DOM changes.** Always re-snapshot after page loads, form submissions, or dynamic updates (modals, tabs, theme switches).

For each step:
1. Snapshot to get current refs
2. Perform the interaction
3. Wait for the page to settle
4. Screenshot to `e2e-screenshots/<journey-name>/NN-description.png`
5. Read the screenshot to check for visual correctness, broken layouts, error states
6. Periodically check `agent-browser console` and `agent-browser errors`

### Handling SPA Behavior

Single-page applications use client-side routing, so `agent-browser open` may not navigate the same way as clicking links. Prefer clicking in-app navigation links over opening URLs directly. After client-side navigations, use `agent-browser wait --load networkidle` before snapshotting since the URL may update before content renders.

### Handling Failures

If an agent-browser command fails:
- **Timeout / element not found**: Re-snapshot, verify the ref still exists, retry once. The DOM may have changed.
- **Navigation error**: Check if the dev server is still running. Restart if needed.
- **Screenshot fails**: Verify the output directory exists (`mkdir -p e2e-screenshots/<journey>`).
- **Persistent failure**: Document the failure, skip the step, and continue with remaining tests. Do not let one broken step block the entire suite.

### 4b. Database Validation

After data-modifying interactions (form submits, deletions, updates):

1. Query the database using the env var from Sub-agent 2's research:
   - **Postgres**: `psql "$DATABASE_URL" -c "SELECT ..."`
   - **SQLite**: `sqlite3 db.sqlite "SELECT ..."`
   - **Other**: Write a small ad-hoc script, run it, then delete it
2. Verify records match UI inputs, relationships are correct, no orphans or duplicates

### 4c. Issue Handling

When an issue is found:
1. Document: expected vs actual, screenshot path, DB query results
2. Fix the code directly
3. Re-run the failing step to verify
4. Screenshot the fix

### 4d. Responsive Testing

Test key pages at multiple viewports. These are sensible defaults -- adjust if the project targets specific breakpoints:

- **Mobile**: `agent-browser set viewport 375 812` (iPhone-sized)
- **Tablet**: `agent-browser set viewport 768 1024` (iPad-sized)
- **Desktop**: `agent-browser set viewport 1440 900`

Screenshot every major page at each size. Check for overflow, broken alignment, unreadable text, and touch target sizing on mobile.

Mark each journey complete (if using tasks) when done.

## Phase 5: Cleanup

1. Stop the dev server background process
2. Close the browser: `agent-browser close`

## Phase 6: Report

Present a summary:

```
## E2E Testing Complete

**Journeys Tested:** [count]
**Screenshots Captured:** [count]
**Issues Found:** [count] ([count] fixed, [count] remaining)

### Issues Fixed
- [Description] -- [file:line]

### Remaining Issues
- [Description] -- [severity: high/medium/low] -- [file:line]

### Bug Hunt Findings
- [Description] -- [severity] -- [file:line]

### Screenshots
All saved to: `e2e-screenshots/`
```

After the summary, offer to export a detailed markdown report to `e2e-test-report.md` with per-journey breakdowns, all screenshot references, database validation results, and recommendations.
