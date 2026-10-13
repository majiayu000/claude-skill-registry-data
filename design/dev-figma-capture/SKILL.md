---
name: dev-figma-capture
description: "Capture web pages and send them to Figma as editable design files. Use when: (1) User wants to capture a webpage to Figma, (2) User says 'figma capture', 'send to figma', 'capture to figma', (3) User provides URLs to convert to Figma designs"
argument-hint: "[url1] [url2] ... [--existing fileKey]"
---

# Figma Capture

Capture web pages and convert them to editable Figma design files via Figma MCP.

## Prerequisites

- Figma MCP (remote) must be connected: `claude mcp add --transport http figma https://mcp.figma.com/mcp`
- For Playwright path: `playwright` npm package available (global or local)

## Workflow

### Step 1: Parse Arguments

- `$ARGUMENTS` contains one or more URLs and optional flags
- `--existing <fileKey>` means add to existing file instead of creating new
- If no URLs provided, ask the user

### Step 2: Determine Capture Method

For each URL, decide the capture approach:

```
Is the page a local dev server (localhost, 127.0.0.1)?
  |
  +-- Yes: Does the page have Figma capture script embedded?
  |   |     (Check by fetching the page source and looking for
  |   |      "mcp.figma.com/mcp/html-to-design/capture.js")
  |   |
  |   +-- Yes → URL Fragment method (lightweight, no Playwright)
  |   +-- No  → Playwright injection method
  |
  +-- No (external site): → Playwright injection method
```

### Step 3: Get Capture ID

Call `mcp__figma__generate_figma_design` to get a capture ID.

- First URL: use `outputMode: "newFile"` (unless `--existing` flag)
- Ask which team/plan to save to if multiple are available
- Subsequent URLs: use `outputMode: "existingFile"` with the fileKey from first capture

### Step 4A: URL Fragment Method (if capture script is on page)

Open the URL with hash parameters:

```bash
open "<URL>#figmacapture=<CAPTURE_ID>&figmaendpoint=https%3A%2F%2Fmcp.figma.com%2Fmcp%2Fcapture%2F<CAPTURE_ID>%2Fsubmit&figmadelay=1000"
```

Wait 5-10 seconds, then poll capture status.

### Step 4B: Playwright Injection Method

Run the bundled capture script:

```bash
node $HOME/.claude/skills/dev-figma-capture/scripts/figma-capture.mjs \
  --url <URL> \
  --capture-id <CAPTURE_ID>
```

The script:

1. Opens the page in headless Chromium
2. Strips CSP headers to allow injection
3. Injects Figma's capture.js
4. Triggers `captureForDesign()` and submits DOM to Figma

Options: `--headless false` (show browser), `--delay <ms>`, `--selector <css>`, `--viewport-w <px>`, `--viewport-h <px>`

**Playwright dependency:** The script requires `playwright` as a Node.js module. If not available in the current project, install it temporarily or check for a global install. The script imports `playwright` directly (not via npx).

### Step 5: Poll and Confirm

Call `mcp__figma__generate_figma_design` with the `captureId` to check status. On success, it returns a claim URL. Open it for the user:

```bash
open "<claim-url>"
```

### Multi-Page Capture

For multiple URLs:

1. Capture first URL as `newFile` → get `fileKey`
2. For each subsequent URL, call `generate_figma_design` with `outputMode: "existingFile"` and the `fileKey` to get a new capture ID
3. Capture each page with its own capture ID
4. Each page becomes a new page in the same Figma file

## Troubleshooting

- **Capture hangs:** The `captureForDesign()` promise often doesn't resolve even when capture succeeds. The script handles this with a timeout. Check browser console logs for `[Figma Capture] Success!` confirmation.
- **CSP errors on external sites:** Playwright strips CSP headers automatically. If still failing, try `--headless false` to debug.
- **Large pages:** Pages over 10MB may fail. Try capturing specific sections with `--selector`.
