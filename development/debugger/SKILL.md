---
name: debugger
description: Verify frontend changes by running flows in browser using Playwright MCP. Checks console logs, captures snapshots, and validates user interactions work correctly.
---

# Frontend Debugger Skill

Automatically verify frontend changes work correctly by running the actual user flow in the browser using Playwright MCP.

## Prerequisites

Requires Playwright MCP server. If not configured, inform the user to run:
```bash
claude mcp add playwright npx @playwright/mcp@latest
```

## When to Use

Invoke this skill automatically after completing ANY frontend task:
- New component implementation
- Bug fixes
- UI modifications
- State management changes
- Form implementations
- Navigation changes

## Verification Process

### Step 1: Start Frontend Server
```
1. Verify the port is active (check if server is already running)
2. If active → continue to next step
3. If not active → run server with "npm start"
4. Wait for server to be ready before proceeding
```

### Step 2: Navigate to the Relevant Page
```
Use browser_navigate to open the page where changes were made.
Example: browser_navigate → http://localhost:<port>/[relevant-path]
```

### Step 3: Execute the User Flow

Use these Playwright MCP tools to simulate user interactions:

| Tool | Purpose |
|------|---------|
| `browser_click` | Click buttons, links, interactive elements |
| `browser_type` | Type into input fields |
| `browser_fill_form` | Fill multiple form fields at once |
| `browser_select_option` | Select dropdown values |
| `browser_hover` | Test hover interactions |
| `browser_press_key` | Keyboard input (Enter, Tab, Escape) |
| `browser_wait_for` | Wait for text/elements to appear |

### Step 4: Monitor and Debug with Console

Use `browser_console_messages` to read ALL console output for debugging:

| Level | Purpose |
|-------|---------|
| `debug` | All messages including debug logs |
| `info` | Info, warnings, and errors |
| `warning` | Warnings and errors |
| `error` | Only errors |

**Use console logs to understand behavior:**

1. **Add debug console.log statements** to the code when you need to understand:
   - Variable values at specific points
   - Function execution order
   - State changes
   - Props being passed
   - API response data
   - Event handler triggers

2. **Run the flow** and check `browser_console_messages` with level `debug` to see your logs

3. **Analyze the output** to understand what's happening

4. **Remove debug logs** after fixing the issue (keep only intentional logging)

**Example debugging workflow:**
```
1. Add console.log to component: console.log('State:', state, 'Props:', props)
2. Run browser_navigate → page
3. Execute the interaction
4. browser_console_messages level="debug" → Read all console output
5. Analyze logs to understand the issue
6. Fix the code
7. Remove debug console.logs
8. Re-verify
```

**Check for errors:**
- JavaScript runtime errors
- React errors (Invalid hook call, undefined props)
- Network/API errors
- Unhandled promise rejections
- Warnings that indicate potential issues

**If issues found:**
1. Report each error/warning with message
2. List all issues found
3. **Wait for user approval before fixing**
4. Only after approval: fix issues, remove debug logs, re-verify

### Step 5: Capture Evidence

- `browser_snapshot` - Get accessibility tree (preferred for LLM analysis)
- `browser_take_screenshot` - Visual documentation when needed
- `browser_network_requests` - Monitor API calls if relevant

### Step 6: Verify Expected Behavior

Confirm:
- UI elements render correctly
- User interactions produce expected results
- State updates properly
- No visual regressions

## Verification Checklist

Before marking task complete:
- [ ] Page loads without console errors
- [ ] Implemented feature/fix works as expected
- [ ] User interactions behave correctly
- [ ] No JavaScript errors in console
- [ ] No unexpected warnings in console
- [ ] No network request failures
- [ ] Visual appearance matches requirements
- [ ] All debug console.logs removed from code

## Error Handling Protocol

**If verification fails:**
1. Document the exact error/failure
2. Analyze root cause
3. **Present list of issues to user**
4. **Wait for user approval before fixing**
5. After approval: fix issues and re-run verification

**Common issues:**
- Hydration errors (SSR/CSR mismatch)
- Missing imports or undefined variables
- Incorrect event handlers
- State not updating properly
- API endpoint errors
- CSS/styling breaking layout

## Example Flows

### Login Form Verification
```
1. browser_navigate → http://localhost:<port>/login
2. browser_snapshot → Verify form elements exist
3. browser_type → Enter email in email field
4. browser_type → Enter password in password field
5. browser_click → Click submit button
6. browser_wait_for → Wait for redirect or success message
7. browser_console_messages level="debug" → Check all console output
8. browser_snapshot → Verify final state
```

### Debugging a Bug
```
1. Add console.log statements to suspect code areas
2. browser_navigate → http://localhost:<port>/[page]
3. Execute the actions that trigger the bug
4. browser_console_messages level="debug" → Read all logs
5. Analyze output to identify root cause
6. Fix the issue
7. Remove debug console.logs
8. Re-run flow to verify fix
9. browser_console_messages level="error" → Confirm no errors
```

### Button Click Verification
```
1. browser_navigate → http://localhost:<port>/[page]
2. browser_snapshot → Locate the button element
3. browser_click → Click the button
4. browser_wait_for → Wait for expected change
5. browser_console_messages level="info" → Check for errors/warnings
6. browser_snapshot → Verify state changed correctly
```

### Form Submission Verification
```
1. browser_navigate → http://localhost:<port>/[form-page]
2. browser_fill_form → Fill all form fields
3. browser_click → Submit form
4. browser_wait_for → Wait for success/error message
5. browser_console_messages level="debug" → Check all console output
6. browser_network_requests → Verify API call succeeded
```

## Reporting Results

**Pass:**
```
Verified: [feature] works correctly. No console errors.
Tested flow: [brief description]
```

**Fail:**
```
Verification failed. Issues found:
1. [Issue 1 description]
2. [Issue 2 description]
...

Should I proceed with fixing these issues?
```

## Important

- **Never skip verification.** Every frontend change must be validated before being considered complete.
- **Never auto-fix issues.** Always present a list of issues and wait for user approval before making any fixes.
