---
name: chrome-browser-control
description: This skill enables comprehensive control and inspection of the Chrome browser without extensions, utilizing the Chrome DevTools Protocol via chrome-devtools-mcp. Use it for advanced browser automation, performance analysis, debugging network requests, taking screenshots, and interacting with web pages. Triggers include explicit requests to browse, automate, debug, or analyze Chrome's behavior, or any task requiring headless/direct browser interaction.
---

# Chrome Browser Control

## Overview

This skill provides a robust interface for direct control and inspection of a live Chrome browser instance, powered by the `chrome-devtools-mcp` server. Unlike traditional browser automation which relies on extensions, this skill leverages the Chrome DevTools Protocol to offer in-depth debugging, performance analysis, and reliable automation capabilities. It's ideal for tasks requiring precise browser interaction, data extraction, or detailed web performance metrics.

## Core Capabilities

This skill wraps the functionalities exposed by `chrome-devtools-mcp`, allowing you to perform a wide range of browser operations:

### 1. Input Automation
Automate user interactions such as clicking elements, filling forms, typing text, hovering, pressing keys, and uploading files.
- `click(selector: string, ...)`
- `drag(startSelector: string, endSelector: string, ...)`
- `fill(selector: string, text: string, ...)`
- `fill_form(selector: string, fields: object, ...)`
- `handle_dialog(accept: boolean, promptText?: string, ...)`
- `hover(selector: string, ...)`
- `press_key(key: string, ...)`
- `upload_file(selector: string, paths: string[], ...)`

### 2. Navigation Automation
Control browser navigation, including opening new pages, listing open pages, navigating to URLs, and closing pages.
- `close_page(targetId?: string, ...)`
- `list_pages()`
- `navigate_page(url: string, ...)`
- `new_page(url?: string, ...)`
- `select_page(targetId: string, ...)`
- `wait_for(selector: string, ...)`

### 3. Emulation
Emulate various device conditions or resize the browser viewport.
- `emulate(device: string, ...)`
- `resize_page(width: number, height: number, ...)`

### 4. Performance Analysis
Record traces, analyze performance insights, and identify bottlenecks.
- `performance_analyze_insight()`
- `performance_start_trace()`
- `performance_stop_trace()`

### 5. Network Inspection
Monitor and inspect network requests made by the browser.
- `get_network_request(requestId: string)`
- `list_network_requests()`

<h3> 6. Debugging & Screenshots</h3>
Evaluate JavaScript in the browser context, log console messages, and capture screenshots or full page snapshots.
- `evaluate_script(expression: string, ...)`
- `get_console_message(messageId: string)`
- `list_console_messages()`
- `take_screenshot(filePath?: string, fullPage?: boolean, ...)` - **CRITICAL:** Use `filePath` to specify the exact save location. If omitted, the screenshot is saved to the MCP server's default directory (often `/config`).
- `take_snapshot()`

## Usage

All capabilities are exposed through the `scripts/chrome-devtools.ts` script. To invoke these functions, you will use `mcporter call chrome-devtools.<tool_name> [args...]`.

**Example: Navigating to a page and taking a screenshot at a specific path**
```bash
mcporter call chrome-devtools.navigate_page url="https://example.com"
mcporter call chrome-devtools.take_screenshot filePath="/Users/tim/.openclaw/workspace/google_home.png" fullPage=true
```

**Note:** The `chrome-devtools-mcp` server must be running and configured in your OpenClaw environment (`mcporter config add chrome-devtools ...`) for this skill to function.

## Resources

### scripts/
- `chrome-devtools.ts`: The auto-generated TypeScript CLI interface for the `chrome-devtools-mcp` server, providing direct access to all listed capabilities. This script handles the communication with the underlying MCP server.
