---
name: browser
description: Headless browser automation via agent-browser (Playwright/Chromium) - navigate, snapshot, click, type, screenshot, eval, console
activation_keywords: [browser, web, url, page, navigate, click, type, screenshot, chromium, playwright]
execution_mode: server
---

# Browser Skill

Provides server-side headless browser automation using `agent-browser` CLI (Playwright/Chromium backend):

- Navigate to URLs (with auto-snapshot and bot detection)
- Snapshot accessibility tree with element references (e.g., `@e5`)
- Click elements by reference
- Type text into input fields
- Scroll up/down
- Navigate back in history
- Press keyboard keys
- Take full-page screenshots (base64 PNG)
- Execute JavaScript in page context
- Read console messages and JS errors
- Session isolation per `task_id`

Use `builtin_browser` tool with fields:
- `operation`: one of "navigate", "snapshot", "click", "type", "scroll", "back", "press", "screenshot", "eval", "console", "close"
- `url`: URL to navigate to (required for navigate)
- `ref`: Element reference from snapshot (e.g., `@e5`) for click/type
- `text`: Text to type (for type) or key to press (for press)
- `js`: JavaScript expression to evaluate (required for eval)
- `task_id`: Session identifier (default: "default"); each task_id gets its own browser session
- `direction`: Scroll direction "up" or "down" (default: "down")
- `full`: Full page screenshot "true"/"false" (default: "false")
- `clear`: Clear console/errors after reading "true"/"false"

Response format:
- **Always return the result in a single message**. When taking a screenshot, embed the base64 PNG inline in your reply via `![alt](data:image/png;base64,...)` — do not split into multiple messages.

Notes:
- Requires `agent-browser` CLI installed: `npx agent-browser install --with-deps`
- Each `task_id` maintains an isolated browser session with persistent state
- Sessions auto-clean after 5 minutes of inactivity
- Element references from snapshot (e.g., `@e5`) are used for click/type — not CSS selectors
- For simple HTTP fetches, prefer `builtin_http_client` (faster, lighter)
