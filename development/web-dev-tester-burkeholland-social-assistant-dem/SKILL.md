---
name: web-dev-tester
description: Autonomously build and test web applications using Playwright MCP server. Enables iterative development with automatic verification - make changes, run the app, visually verify, check for errors, and iterate. Use when building websites, debugging UI issues, or implementing features that need visual verification.
compatibility: Requires Playwright MCP server configured in the agent environment.
metadata:
  author: RecordMe
  version: "1.0"
---

# Web Development with Automatic Testing

Build web applications iteratively with automatic visual verification using Playwright.

## Philosophy

This skill enables a **build-verify-iterate** loop:
1. **Build**: Make code changes (HTML, CSS, JS, framework code)
2. **Run**: Start the dev server
3. **Verify**: Use Playwright to check the result visually and functionally
4. **Iterate**: Fix issues based on screenshots and console output

This entire process should be run using #runSubagent so as not to pollute the context window. If #runSubagent is not available, proceed normally.

## Core Workflow

### Step 1: Identify the Dev Server Command

Check `package.json` for the dev script:
```json
{
  "scripts": {
    "dev": "vite",           // Vite projects
    "start": "react-scripts start",  // CRA projects
    "dev": "next dev"        // Next.js projects
  }
}
```

Common dev servers and their default ports:
| Framework | Command | Default Port |
|-----------|---------|--------------|
| Vite | `npm run dev` | 5173 |
| Create React App | `npm start` | 3000 |
| Next.js | `npm run dev` | 3000 |
| Vue CLI | `npm run serve` | 8080 |
| Angular | `ng serve` | 4200 |
| Plain HTML | `npx serve .` | 3000 |

### Step 2: Start the Dev Server

**First, check if server is already running:**
```bash
python scripts/check_server.py --port PORT_NUMBER
```

If `"running": true`, skip to Step 3. Otherwise, start the server:

Start the server as a background process so it keeps running:

```bash
npm run dev
```

### Step 3: Verify with Playwright

Use the Playwright MCP tools to interact with and verify the running application. Always use the edge browser for best compatibility and try to reuse existing browser contexts when possible.

#### Take a Screenshot
```
Use playwright_screenshot to capture the current state:
- name: "initial-state" 
- url: "http://localhost:5173"
- fullPage: true
```

#### Check for Console Errors
```
Use playwright_console to check for JavaScript errors:
- Look for "error" level messages
- Check for failed network requests
- Note any warnings that might indicate issues
```

#### Navigate and Interact
```
Use playwright_navigate, playwright_click, playwright_fill to:
- Navigate to different routes
- Click buttons and links
- Fill out forms
- Trigger interactive behavior
```

### Step 4: Analyze Results

After taking screenshots or checking console:

**Visual Checks:**
- Does the layout match expectations?
- Are colors, fonts, spacing correct?
- Is content visible and readable?
- Are interactive elements visible?

**Console Checks:**
- Any JavaScript errors?
- Failed network requests (404s, 500s)?
- Missing resources (fonts, images)?
- React/Vue/framework warnings?

**Functional Checks:**
- Do buttons trigger expected behavior?
- Do forms validate correctly?
- Does navigation work?
- Do API calls succeed?

### Step 5: Iterate

Based on findings, make code changes and repeat:

```
1. Identify the issue from screenshot/console
2. Edit the relevant file(s)
3. Wait for hot-reload (or restart server)
4. Take new screenshot to verify fix
5. Repeat until correct
```

## Common Verification Patterns

### Verify a Component Renders
```
1. playwright_navigate to the page containing the component
2. playwright_screenshot with a descriptive name
3. Check screenshot shows component correctly
4. playwright_console to ensure no errors
```

### Verify a Form Works
```
1. playwright_navigate to the form page
2. playwright_fill each form field
3. playwright_click the submit button
4. playwright_screenshot to capture result
5. playwright_console to check for validation/API errors
```

### Verify Responsive Layout
```
1. playwright_screenshot at default width
2. Use playwright with viewport options for mobile (375px)
3. Compare layouts at different breakpoints
```

### Verify Dark Mode
```
1. playwright_click on theme toggle (if exists)
2. playwright_screenshot to capture dark mode
3. Verify contrast and colors are correct
```

## Debugging Strategies

### When Screenshot Shows Blank Page
1. Check console for JavaScript errors
2. Verify the correct port/URL
3. Wait longer for server startup
4. Check if route exists

### When Layout is Broken
1. Screenshot at different viewport sizes
2. Check console for CSS loading errors
3. Inspect specific elements with playwright_evaluate
4. Look for missing/incorrect class names

### When Functionality Doesn't Work
1. playwright_console to check for JS errors
2. Use playwright_evaluate to check state
3. Verify event handlers are attached
4. Check network tab for failed API calls

## Example: Full Development Cycle

```markdown
**Task**: Add a contact form to the homepage

**Cycle 1 - Initial Implementation**
1. Create ContactForm component with fields
2. Add to homepage
3. Start dev server: `npm run dev`
4. Screenshot: See form renders but styling is off
5. Fix: Add proper Tailwind classes

**Cycle 2 - Fix Styling**
1. Update component with correct styles
2. Screenshot: Form looks good now
3. Console: No errors
4. Test: Fill form and submit

**Cycle 3 - Fix Submission**
1. playwright_fill the form fields
2. playwright_click submit button
3. Console: "TypeError: handleSubmit is not defined"
4. Fix: Add the missing handler function

**Cycle 4 - Verify Complete**
1. Fill and submit form again
2. Screenshot: Shows success message
3. Console: Clean, no errors
4. Done!
```

## Integration with File Editing

When making changes, follow this pattern:

```
1. Read current file state
2. Make targeted edit
3. Save file
4. Wait 1-2 seconds for hot reload
5. playwright_screenshot to verify
6. If issues, read console and iterate
```

## Tips for Autonomous Development

- **Screenshot frequently**: Visual verification catches issues fast
- **Check console after every change**: Catch errors early
- **Use descriptive screenshot names**: `after-adding-header`, `form-validation-error`
- **Test incrementally**: Verify each feature before moving to the next
- **Mobile-first**: Test responsive layouts as you build

## Playwright MCP Tools Reference

| Tool | Purpose |
|------|---------|
| `playwright_navigate` | Go to a URL |
| `playwright_screenshot` | Capture visual state |
| `playwright_click` | Click elements |
| `playwright_fill` | Enter text in inputs |
| `playwright_console` | Get console messages |
| `playwright_evaluate` | Run JS in browser context |

## When Things Go Wrong

If the dev server won't start:
```bash
# Check if port is in use
netstat -ano | findstr :5173

# Kill existing process if needed
taskkill /PID <pid> /F

# Try starting again
npm run dev
```

If Playwright can't connect:
- Verify server is actually running
- Check the port matches
- Try http://127.0.0.1 instead of localhost
- Wait longer for server startup
