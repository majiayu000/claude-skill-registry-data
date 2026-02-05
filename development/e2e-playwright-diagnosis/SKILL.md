---
name: e2e-playwright-diagnosis
description: Diagnose and resolve E2E test failures in Playwright. This skill should be used when E2E tests fail and need investigation, when Playwright test errors require root cause analysis, or when test failures need to be reproduced in the browser for debugging. Orchestrates MCP tools (Playwright, Chrome DevTools, Serena) and delegates code fixes to specialized agents.
---

# E2E Playwright Diagnosis

## Overview

This skill provides a systematic procedure for diagnosing and resolving E2E test failures in Playwright. It orchestrates multiple MCP tools (Playwright, Chrome DevTools, Serena) and delegates code corrections to specialized agents, ensuring all tests pass based on actual application behavior.

## When to Use

- E2E test failure messages are received
- Playwright tests need root cause analysis
- Test failures require browser reproduction for debugging
- Multiple tests in a file are failing and need systematic resolution

## Workflow Decision Tree

```
Error Message Received
        │
        ▼
┌───────────────────┐
│ 1. Analyze Error  │
│    Extract info   │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ 2. Locate Test    │
│    Read test file │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ 3. Prepare Env    │
│    rm .next       │
│    rebuild        │
└─────────┬─────────┘
          │
          ▼
┌───────────────────────────────┐
│ 4. Reproduce in Browser       │
│    MCP Playwright +           │
│    MCP Chrome DevTools        │
└─────────┬─────────────────────┘
          │
          ▼
    Test passes?
     /        \
   Yes         No
    │           │
    ▼           ▼
┌─────────┐  ┌─────────────────┐
│ Run all │  │ Collect info    │
│ tests   │  │ via MCP Serena  │
└────┬────┘  └────────┬────────┘
     │                │
     ▼                ▼
All pass?      ┌─────────────────┐
  /    \       │ Delegate fix to │
Yes     No     │ context-manager │
 │       │     │ → frontend-dev  │
 ▼       ▼     └────────┬────────┘
┌────┐ ┌─────┐          │
│Done│ │Align│          ▼
│    │ │tests│   ┌─────────────────┐
└────┘ │to   │   │ Validate fix    │
       │code │   │ Loop until pass │
       └─────┘   └─────────────────┘
```

## Detailed Procedure

### Step 1: Analyze Initial Failure

1. Receive the E2E test error message
2. Analyze the complete error content
3. Extract relevant information:
   - Error type
   - Stack trace
   - Test file name
   - Failed test name

### Step 2: Identify Problematic Test

4. Locate the E2E test file mentioned in the error
5. Open the test file
6. Identify the specific test that failed
7. Read:
   - The title (describe / test)
   - The test body
8. Infer which application behavior the test attempts to validate

### Step 3: Prepare Environment

9. Remove the `.next` folder from the project:
   ```bash
   rm -rf apps/gateway-financeiro/.next
   ```
10. Execute complete project rebuild to generate a new `.next` folder:
    ```bash
    npm run build --workspace=apps/gateway-financeiro
    ```

### Step 4: Reproduce Test in Browser

11. Use **MCP Playwright** to execute the test in the browser
12. Simultaneously use **MCP Chrome DevTools** to:
    - Observe the DOM
    - Monitor console errors
    - Track network requests
13. Execute only the test that failed

**MCP Playwright tools to use:**
- `mcp__playwright__browser_navigate` - Navigate to test URL
- `mcp__playwright__browser_snapshot` - Capture accessibility snapshot
- `mcp__playwright__browser_click` - Interact with elements
- `mcp__playwright__browser_type` - Fill form fields

**MCP Chrome DevTools tools to use:**
- `mcp__chrome-devtools__take_snapshot` - Capture DOM state
- `mcp__chrome-devtools__list_console_messages` - Check for errors
- `mcp__chrome-devtools__list_network_requests` - Monitor API calls

### Step 5: Evaluate Isolated Test Result

14. **If the test passes in the browser:**
    1. Read all other E2E tests present in the same file
    2. Execute all tests from that file, still via Playwright in the browser
    3. **If tests pass isolated but fail in suite** → Check for data isolation issues:
       - Verify unique identifiers are generated per test, not per describe block
       - Check backend logs for 409 Conflict or "already exists" errors
       - Look for shared state between tests (cookies, localStorage, database records)

15. **If all tests in the file pass:**
    - Invoke the `context-manager` agent
    - Through it, invoke the `frontend-nextjs-developer` agent to:
      - Adjust E2E tests to faithfully reflect the behavior already implemented in the code
      - Consider the code as the source of truth
    - Finalize the process

### Step 6: When Test Cannot Be Reproduced in Browser

16. **If Playwright + Chrome DevTools cannot reproduce the error in the browser:**
    1. Use **MCP Serena** to navigate the project
    2. Collect maximum possible information:
       - Execution logs
       - Server logs
       - Playwright logs
    3. Execute only non-committable commands:
       - Project rebuild
       - Docker container rebuild
       - Log inspection
    4. **Do not alter any code or test files**

**MCP Serena tools to use:**
- `mcp__serena__search_for_pattern` - Search for error patterns in logs
- `mcp__serena__find_symbol` - Locate relevant code symbols
- `mcp__serena__get_symbols_overview` - Understand file structure

### Step 7: Delegate Code Correction

17. Invoke the `context-manager` agent via Task tool:
    ```
    subagent_type: "context-manager"
    ```
18. Through it, invoke the `frontend-nextjs-developer` agent
19. Provide the agent with:
    - Error context
    - Collected logs
    - Expected behavior
20. Await response confirming the code bug was fixed

### Step 8: Validate Correction After Code Change

21. **After fix confirmation:**
    1. Remove the `.next` folder again
    2. Execute project rebuild
    3. Execute only one test from the affected file

22. **If the test passes:**
    - Execute the remaining tests from the same file

23. **If the test does not pass:**
    - Use again:
      - MCP Playwright
      - MCP Chrome DevTools
    - Execute the test in the browser
    - Collect new information

### Step 9: Validation Loop

24. Repeat steps 21 to 23 until:
    - All tests in the file pass successfully
    - No remaining E2E failures related to the original error

## Termination Condition

25. Terminate the process only when:
    - All E2E tests in the affected file are passing
    - Test behavior is aligned with the actual application behavior

## Important Notes

- **Code is the source of truth**: If the application behaves correctly but tests fail, adjust the tests
- **Do not modify code during investigation**: Only collect information until Step 7
- **Always rebuild after changes**: The `.next` folder must be regenerated after any code change
- **Use browser reproduction first**: Visual debugging often reveals issues faster than log analysis
- **Delegate appropriately**: Code fixes go to `frontend-nextjs-developer`, not handled directly by this skill

## Quick Troubleshooting Checklist

When tests fail, check these common issues first:

1. **Backend validation errors (400)** → Check API logs for "Bad Request" - often timeout masks schema mismatch (e.g., enum values, unexpected fields)
2. **Manual testing works, tests fail** → Test in browser first; if app works, issue is in tests or contracts, not code
3. **Timeout on form submit** → Check global timeout `playwright.config.ts` (30s minimum); verify backend accepts request schema
4. **Strict mode violation** → Multiple elements match selector; add `.first()` or scope to container (e.g., `dialog.locator()`)
5. **Stale locators after re-render** → Use inline `.nth()` selectors instead of storing references; re-query DOM after state changes
6. **Dropdown not opening/selecting** → Add `waitForTimeout(500)` after `.click()`; use `waitForLoadState('networkidle')` for async data
7. **Build cache stale** → `rm -rf .next && npm run build`, then restart Docker containers (`docker restart administramos-gateway-financeiro`)
8. **Redirect loops** → Middleware must use `request.headers.get('host')` not `request.nextUrl.href` (localhost vs public domain)
9. **Missing JS chunks (404)** → Rebuild Next.js and restart container; browser may cache old build references
10. **Element not found** → Use `browser_snapshot` to see actual DOM; shadcn components often use portals (render outside parent)
11. **Timeout on element interaction (manual test works, logs show success)** → Selector uses `.filter({ hasText: /pattern/ })` but element text is dynamic (e.g., "Loading...", "Select option"). Use `getByRole('role', { name: 'Label' })` to match accessible name from label, not visible text
12. **409 Conflict when creating records (passes isolated, fails in suite)** → Unique identifier generated once at describe level, causing duplicate keys when multiple tests create records. Generate unique ID inside each test function that creates data: `const uniqueId = \`E2E-${Date.now()}\`;`. Discovery: Backend logs show "already exists" or duplicate key error
13. **Submit button clicked but form not submitted (no navigation, no errors)** → Form validation not complete before submit, or button briefly disabled. Add `waitForTimeout(500)` after filling last field, verify button not disabled before clicking: `await expect(button).not.toBeDisabled()`. Discovery: Screenshot shows filled form, button present but no action occurred
