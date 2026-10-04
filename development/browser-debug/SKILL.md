---
name: browser-debug
description: Use browser automation MCP tools to inspect pages for errors, console warnings, and visual issues.
disable-model-invocation: false
allowed-tools: Read Bash mcp__chrome-devtools
---

# Browser Debug

Uses browser automation MCP tools (Chrome DevTools, Playwright, etc.) to inspect the running app for errors and visual issues.

## Prerequisites

- Dev server must be running on the expected port
- Browser automation MCP server must be configured (chrome-devtools or playwright)

## Instructions

### 1. Connect and Navigate

Use available browser MCP tools (load via ToolSearch first):

- List open pages/tabs
- Navigate to a URL
- Take screenshots
- Read console output
- Evaluate JavaScript in page context

### 2. Check for Issues

For each page to inspect:

1. Navigate to the page URL
2. Wait for page load with appropriate selector
3. Read console messages and filter for:
   - Framework warnings (e.g., `[Vue warn]`, `[React]`)
   - Runtime errors (`Error`, `Uncaught`)
   - Hydration mismatches (if SSR)
4. Take a screenshot if visual verification is needed
5. Report findings with component name, error text, and file location

### 3. Common Debug Flows

**Hydration errors**: Navigate to page, check console for hydration warnings.

**Runtime errors**: Check console messages after navigation and interaction.

**Network issues**: List network requests to find failed API calls.

### 4. Key Pages to Check

<!-- Customize this list for your project -->
- `/` - Home page
- `/login` - Authentication
- `/about` - Public content page

## Notes

- Always verify the dev server is running before navigating
- Use headless mode for CI environments
- Report findings with actionable file locations
