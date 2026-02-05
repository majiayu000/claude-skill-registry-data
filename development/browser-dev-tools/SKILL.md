---
name: browser-dev-tools
description: This skill should be used when working with browser-rendered artifacts (i.e. Bun, React/React Native) to proactively validate that development work on localhost is being built appropriately and to support debugging browser-rendered content. Use this skill after making frontend changes to verify the output visually.
---

# Browser Dev Tools

## Overview

This skill provides Chrome DevTools Protocol tools for validating and debugging browser-rendered artifacts during development. Use these tools to verify that localhost servers are rendering correctly and to debug visual issues proactively.

The tools connect to Chrome running on port `:9222` with remote debugging enabled.

## When to Use This Skill

Use this skill proactively in these scenarios:

1. **After making frontend code changes** - Validate that React, Bun, HTML, or other frontend code renders correctly on localhost
2. **After starting a dev server** - Verify the application loads and displays properly
3. **When debugging browser rendering issues** - Inspect page state, DOM structure, or cookies
4. **When validating UI changes** - Take screenshots to visually confirm changes appear as expected

**Important:** Always use this skill proactively after completing frontend development tasks to validate the work before considering it done.

## Available Tools

All browser tools are located in `~/.claude/skills/browser-dev-tools/tools/` and should be executed via the Bash tool.

### Start Chrome

```bash
~/.claude/skills/browser-dev-tools/tools/browser-start.js                # Fresh profile
~/.claude/skills/browser-dev-tools/tools/browser-start.js --profile      # Auto-detect profile
~/.claude/skills/browser-dev-tools/tools/browser-start.js --profile "Profile 2"  # Specific profile
```

Launch Chrome with remote debugging.

**Profile Auto-Detection:**

- When using `--profile` without a profile name, the script automatically selects the appropriate Chrome profile based on the current working directory:
  - `~/personal/**` → Uses Default profile (tnagengast@gmail.com)
  - `~/work/**` → Uses Profile 1 (tom@cable.tech)
- You can override this by specifying a profile name: `--profile "Profile 2"`

**Important:** Always use `--profile` (auto-detect) or specify a profile when you need to preserve authentication state for testing authenticated pages.

### Navigate

```bash
~/.claude/skills/browser-dev-tools/tools/browser-nav.js http://localhost:3000
~/.claude/skills/browser-dev-tools/tools/browser-nav.js http://localhost:3000 --new
```

Navigate to URLs. Use `--new` flag to open in a new tab instead of reusing the current tab.

### Screenshot

```bash
~/.claude/skills/browser-dev-tools/tools/browser-screenshot.js
```

Capture the current viewport and return a temporary file path. **Always take screenshots after navigating to validate the rendered output visually.**

### Evaluate JavaScript

```bash
~/.claude/skills/browser-dev-tools/tools/browser-eval.js 'document.title'
~/.claude/skills/browser-dev-tools/tools/browser-eval.js 'document.querySelectorAll("a").length'
```

Execute JavaScript in the active tab to extract data, inspect page state, or perform DOM operations programmatically.

### Pick Elements

```bash
~/.claude/skills/browser-dev-tools/tools/browser-pick.js "Click the submit button"
```

Launch an interactive picker that lets the user click elements to select them. The user can select multiple elements (Cmd/Ctrl+Click) and press Enter when done. Returns CSS selectors for the selected elements.

Use this when the user wants to select specific DOM elements on the page.

### Cookies

```bash
~/.claude/skills/browser-dev-tools/tools/browser-cookies.js
```

Display all cookies for the current tab including domain, path, httpOnly, and secure flags. Use this to debug authentication issues or inspect session state.

## Common Workflows

### Validating Frontend Changes (Primary Use Case)

After making changes to frontend code (React components, HTML, CSS, etc.):

1. **Start Chrome** if not already running:

   ```bash
   ~/.claude/skills/browser-dev-tools/tools/browser-start.js --profile  # Auto-detects profile
   ```

   Note: Use `--profile` to auto-detect the appropriate profile based on cwd (personal vs work).

2. **Navigate to localhost**:

   ```bash
   ~/.claude/skills/browser-dev-tools/tools/browser-nav.js http://localhost:PORT
   ```

   Replace PORT with the appropriate port (e.g., 3000, 5173, 8080).

3. **Take a screenshot**:

   ```bash
   ~/.claude/skills/browser-dev-tools/tools/browser-screenshot.js
   ```

4. **Read the screenshot** using the Read tool to visually validate the changes.

5. **If issues are found**, use JavaScript evaluation to inspect the page state:
   ```bash
   ~/.claude/skills/browser-dev-tools/tools/browser-eval.js 'document.body.innerHTML'
   ```

### Debugging Rendering Issues

When troubleshooting why something isn't rendering correctly:

1. **Navigate to the problematic page**

2. **Take a screenshot** to see the current state

3. **Evaluate JavaScript** to inspect:
   - DOM structure: `document.querySelector('#myElement')`
   - Console errors: `console.log(...)`
   - Element properties: `document.querySelector('#myElement').style`

4. **Check cookies** if authentication or session issues are suspected

## Best Practices

- **Always validate proactively** - Take screenshots after frontend changes to catch visual issues early
- **Use profile auto-detection** - Use `--profile` (without arguments) to automatically load the correct profile based on your working directory (personal vs work)
- **Navigate before evaluating** - Ensure the page is loaded before running JavaScript
- **Read screenshots** - Always use the Read tool on screenshot paths to view the captured image
- **Check common ports** - Typical dev servers run on 3000 (React/Next.js), 5173 (Vite), 8080 (generic), or 4200 (Angular)
