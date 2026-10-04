---
name: devtools-preview
description: Visual auto-validation via Chrome DevTools MCP — verify rendering and console before final_answer.
---

# DevTools Preview Skill

You have a controllable Chrome browser (**Chrome DevTools MCP**) to visually and functionally verify your page **BEFORE** calling final_answer. The screenshot you capture is returned in context as an image.

## Why
Syntactically valid HTML can still render broken layouts, empty containers, or silent JS exceptions. Previewing directly catches visual flaws and runtime errors immediately.

## Workflow (Mandatory for web tasks after write_file)

1. **Navigate**: `navigate_page(url="<ABSOLUTE file:/// URL>")`
   - The exact primary file URL is provided in the prompt. Use it directly.
2. **Console Verification**: `list_console_messages()` -> check for JS errors.
   - ⚠️ **MANDATORY**: If you see `SyntaxError`, `Unexpected token`, or `Uncaught`, fix it immediately via `search_replace` or `write_file`.
3. **Capture**: `take_screenshot()` -> inspect the rendered image in context.
   - ⚠️ **NEVER pass `filePath`**. Call `take_screenshot()` without arguments.
   - Verify layout, colors, font styling, and proper container utilization.
4. **UI Fuzzing & Interaction**:
   - Call `fuzz_click_all_buttons()` or `click(uid=...)` to wake up event handlers and catch silent JS exceptions.
   - For canvas/animations, verify movement with `probe_canvas_activity()`.
5. **Fix & Re-verify**:
   - If bugs occur, fix them, then re-navigate, re-check console, and re-capture.
6. **final_answer**: Call when rendering is verified **AND** 0 console errors **AND** controls are functional.

## Pitfalls to Avoid
- **HTML ONLY**: NEVER pass `.css` or `.js` files to `navigate_page()`. Always navigate to the parent HTML file (e.g. `index.html`).
- **Stop Condition**: Once files are written and verified with clean console and good rendering, immediately call `final_answer`.
- **Absolute URLs**: `navigate_page(url="index.html")` will not work. Always use the provided absolute `file:///...` URL.

## Key Tools
| Tool | Purpose |
|---|---|
| `navigate_page(url)` | Opens absolute `file:///...` URL in Chrome |
| `take_screenshot()` | Captures page and returns screenshot |
| `list_console_messages()` | Lists runtime JS errors and console logs |
| `evaluate_script(function)` | Executes custom JS inside the page |
| `take_snapshot()` | Returns accessibility/DOM tree |
| `fuzz_click_all_buttons()` | Fuzz-clicks all buttons to trigger handlers |
| `probe_canvas_activity()` | Probes canvas animation liveliness |
