---
name: browser-agent
description: Autonomous human-like browser control and professional QA/QC testing. Powered by agent-browser (Rust native CDP, zero Playwright) with ISTQB test matrix generation, automated testcase execution, console/network error tracing, and defect reporting.
mcp: supergraph-browser
---

# /supergraph:browser-agent

Autonomous human-like browser control and professional QA/QC testcase execution without Playwright.
Powered by native Rust `agent-browser` (Chrome DevTools Protocol direct, zero bot-detection footprint).

Announce: "🌐 /supergraph:browser-agent — professional QA testing with real user emulation (Rust CDP)..."

---

## Why Agent-Browser over Playwright?

- **Zero Bot Detection Footprint:** Native Rust client communicating directly via CDP. Removes `navigator.webdriver` and disables Blink automation flags.
- **Human Input Mode (`--input-mode human`):** Natural Bezier mouse curves, randomized typing cadence, natural dwell times.
- **Token Efficiency:** Compact Accessibility Tree snapshots with `@ref` identifiers (~100-300 tokens vs 20,000 HTML tokens).
- **Session & Profile Reuse:** Effortlessly attaches to your authenticated Chrome profile or `--auto-connect` to running Chrome on port 9222.

---

## Available Tools / Commands

Can be invoked via MCP (`mcp__supergraph-browser__*`) or CLI (`agent-browser`):

| Action | MCP Tool | CLI Command | Purpose |
|---|---|---|---|
| Open URL | `agent_browser_open` | `agent-browser open <url>` | Navigate to page |
| Read State | `agent_browser_snapshot` | `agent-browser snapshot -i` | Accessibility tree with `@ref` |
| Find Target | `agent_browser_find` | `agent-browser find role button click` | Locate elements semantically |
| Click | `agent_browser_click` | `agent-browser click @ref` | Click element by ref |
| Type/Fill | `agent_browser_fill` | `agent-browser fill @ref <text>` | Fill input with human keystrokes |
| Key Press | `agent_browser_press` | `agent-browser press Enter` | Send keyboard event |
| Wait | `agent_browser_wait_for_text` | `agent-browser wait <ms>` | Wait for condition or pause |
| Screenshot | `agent_browser_screenshot` | `agent-browser screenshot <path>` | Capture visual evidence |
| Console Logs | `agent_browser_eval` | `agent-browser console` | View browser console errors |
| Page Errors | `agent_browser_eval` | `agent-browser errors` | Catch unhandled exceptions |
| Network Requests | `agent_browser_eval` | `agent-browser network requests` | Inspect failed API calls |
| Close | `agent_browser_close` | `agent-browser close` | Close session |

---

## The 4-Step Human Interaction Loop

```
[1. Open] ───────> [2. Snapshot @refs] ───> [3. Human Action] ───> [4. Verify & Settle]
open <url>          snapshot -i               click @e2                 wait_for_text
                    find                      fill @e3 "text"           snapshot
```

### 1. Observe Before Acting (Never Guess Selectors)
Call `snapshot` to get verified element references (`@e1`, `@e2`, ...).

### 2. Bypassing Strict Bot Walls (Cloudflare, Akamai, CAPTCHA)
Connect directly to your active browser using either method:

**Method A: Supergraph Chrome Relay Extension (Recommended - Zero restart, 100% human profile)**
```bash
# 1. Start relay server
node plugins/supergraph/extensions/chrome-relay/relay-server.js
# 2. Attach agent
export SG_BROWSER_CDP="http://127.0.0.1:9333"
```

**Method B: Chrome Remote Debugging Port**
```bash
# Attach to existing Chrome
export SG_BROWSER_CDP="http://127.0.0.1:9222"
# Or auto-discover running Chrome instance
export SG_BROWSER_AUTO_CONNECT="true"
```
Uses your real user session, cookies, extensions, canvas fingerprints, and hardware profile.

---

## Professional QA/Tester Workflow (ISTQB Standard)

When tasked with testing a feature or application, the agent acts as a Senior QA Automation Engineer:

### Phase 0: Graph Context & Impact Prioritization
Before running test automation, query graph context to prioritize coverage on changed paths:
Use `CBM_PROJECT`: call `detect_changes`, `search_graph` for changed routes/pages, then `trace_path` for inbound/outbound call and data-flow paths. Run validated `test-gaps` recipes. If results are unavailable, fall back to filesystem inspection.

### Phase 1: Test Matrix Generation
Generate a comprehensive test matrix covering 5 dimensions and save to `docs/qa/test-matrix-<feature>.md` (scaffold quickly with `scripts/init-qa.sh matrix <feature> [ui|api|fullstack] [target-url]` from `templates/`):
1. **Happy Path:** Expected valid user flow / 200 OK API contract from entrance to success.
2. **Negative Path:** Missing required fields, invalid credentials, malformed emails/JSON, schema violations.
3. **Boundary Value Analysis:** 0 chars, 1 char, limit max chars, SQLi/XSS probe strings (`<script>`, `' OR 1=1`).
4. **Network & Fault Resilience:** Simulating 500 API errors, timeout, offline state, DB rollback verification.
5. **RBAC & Authorization:** Guest/User attempting to access restricted routes or perform unauthorized operations (401/403/IDOR).

### Phase 2: Autonomous Execution & Verification
For each testcase in the matrix:
1. Navigate to target URL (`agent-browser open <url>`).
2. Input test data with human cadence (`agent-browser fill @ref <data>`).
3. Trigger action (`agent-browser click @ref`).
4. Assert outcome:
   - Check URL transition: `agent-browser get url`
   - Check UI feedback: `agent-browser is visible <selector>` or `agent-browser get text @ref`
   - Capture evidence on failure: `agent-browser screenshot docs/qa/evidence/TC-xxx.png`

### Phase 3: Console & Network Diagnostics
Assert that no silent runtime bugs were introduced:
- `agent-browser console --clear` → Detect React hydration warnings, runtime `console.error`.
- `agent-browser errors` → Unhandled Promise rejections.
- `agent-browser network requests` → Identify failed HTTP 4xx/500 endpoints.

### Phase 4: Structured Defect Reporting
If defects are found, generate a formal Bug Report at `docs/qa/bug-report-<timestamp>.md` (scaffold quickly with `scripts/init-qa.sh bug <feature> <defect-id> <defect-title>` from `templates/bug-report-template.md`):
- **Defect ID & Title:** e.g., `BUG-AUTH-001: Missing password validation triggers unhandled 500 error`.
- **Severity:** Blocker / Critical / Major / Minor.
- **Preconditions & Environment:** Browser profile, viewport, user state.
- **Steps to Reproduce:** Exact command sequence or clicks.
- **Expected vs Actual Result:** Clear contrast.
- **Evidence:** Attached screenshot link + Console/Network error dump.

---

## CLI Quick Examples (in bash)

```bash
agent-browser open https://example.com
agent-browser snapshot -i
agent-browser click @e1
agent-browser fill @e2 "user@example.com"
agent-browser screenshot docs/qa/evidence/verify.png
agent-browser close
```
