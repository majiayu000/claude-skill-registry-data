---
name: playwright
description: Run Playwright end-to-end tests — execute, filter, and download the HTML report
activation_keywords: [playwright, e2e, test, ui-test, browser-test, report]
execution_mode: server
---

# Playwright E2E Test Skill

Run Playwright end-to-end tests from the `e2e/` directory. Supports running all tests, filtering by file, and returning the HTML test report as a downloadable file (inline in web chat, file attachment in IM).

Use `builtin_playwright` tool with fields:
- `action`: The action to perform. Options:
  - `"run"` (default): Run Playwright tests and return the HTML report file
  - `"install"`: Install Playwright browsers
  - `"list"`: List available tests without running
  - `"report"`: Retrieve the latest test report without re-running
- `files`: Comma-separated test file paths to run (e.g., `"tests/auth.spec.ts"`). Empty = run all tests.
- `headed`: Run with browser GUI visible — `"true"` or `"false"` (default: `"false"`, headless).
- `project`: Playwright project name (default: `"chromium"`). Other options: `"firefox"`, `"webkit"`.
- `workers`: Number of parallel workers (default: `"2"`). Use `"1"` for serial execution.
- `retries`: Number of retries on failure (default: `"1"`). Use `"0"` for no retries.
- `timeout`: Per-test timeout in milliseconds (default: `"60000"`).

Result:
- Returns the terminal output including pass/fail counts, durations, and failed test names.
- The HTML report is auto-delivered as a file:
  - **Web chat**: shown as a downloadable link in the conversation
  - **IM (Lark/DingTalk/Telegram/QQ)**: sent as a file attachment
- If the `e2e/` directory is not found (e.g., production Docker image without source), the skill reports this clearly.

Example usage:
- "帮我跑一下 E2E 测试" → runs all tests, returns results + report file
- "只跑 auth 的测试" → `files="tests/auth.spec.ts"`
- "看看报告" → `action="report"`
- "列出所有测试" → `action="list"`
