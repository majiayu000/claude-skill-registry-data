---
name: browser-automation
description: >-
  Automates browser interactions for web testing, form filling, screenshots and
  data extraction. Use when the user needs to navigate sites, interact with
  pages, fill forms, take screenshots, test web apps, or extract information
  from pages.
---

# Browser Automation

## Overview

Automate browser interactions: navigate pages, click elements, fill forms, take
screenshots, extract data. Use whatever browser automation tool is available in
your environment (e.g., `playwright-cli`, Playwright MCP, `WebFetch`, `curl`).

## Instructions

<step_by_step>

1. **Detect Tool**
   - Check what browser tools are available. Prefer full browser (JS rendering,
     interaction) over HTTP-only tools.
   - If no browser tool is found, fall back to `WebFetch` or `curl` for
     read-only page access. Inform the user about limitations.

2. **Navigate**
   - Open the target URL. Wait for the page to load.

3. **Observe Before Acting**
   - Always capture page state (accessibility snapshot, DOM, or HTML) before
     interacting. Use structured data (accessibility tree, element refs) over
     raw screenshots when possible — structured data is better for reasoning.

4. **Interact**
   - Click, fill, type, select using element references from the snapshot.
   - After each interaction, re-capture page state to verify the result.

5. **Capture Output**
   - Take screenshots or extract data as requested.
   - Save files to the working directory.

6. **Clean Up**
   - Close browser sessions when finished.

</step_by_step>

## Best Practices

1. **Snapshot First**: Always capture page state after navigation or interaction
   before taking next action.
2. **Isolation**: Use separate sessions for independent tasks.
3. **Clean Up**: Always close browser sessions when done.
4. **Prefer Structured Data**: Accessibility snapshots > screenshots > raw HTML
   for element identification.
