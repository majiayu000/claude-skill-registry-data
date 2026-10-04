---
name: browser-harness
description: >
  Self-healing CDP browser automation connecting LLMs directly to a real Chrome instance
  via WebSocket. Use when you need full browser freedom with the user's actual sessions,
  cookies, and extensions — not a headless sandbox. Agents write helper code on-the-fly
  that persists across runs. Triggers on: "use my real browser", "browser-harness",
  "automate with my Chrome", "self-healing browser", "domain skill", "real browser session".
metadata:
  source: "https://github.com/browser-use/browser-harness"
  install_path: "~/Developer/browser-harness"
  version: "0.1.0"
---

# browser-harness

Self-healing CDP automation framework. Connects directly to your running Chrome via a single WebSocket — agents get full browser freedom and write missing helpers during execution.

## When to Use (Decision Matrix)

| Need | Use This |
|------|----------|
| QA testing / regression / health scores | agent-browser / browse |
| Fast data extraction (no rendering) | Lightpanda |
| Full browser interaction (MCP-native) | Playwright MCP |
| **Real Chrome with your sessions/cookies/extensions** | **browser-harness** |
| **Agent needs to learn and persist site-specific patterns** | **browser-harness** |
| Local dev server testing | webapp-testing |

Use browser-harness when:
- You need the user's logged-in sessions (Gmail, LinkedIn, internal tools)
- The task requires extensions or profiles that headless can't replicate
- You want the agent to learn and improve across runs (self-healing)
- You need stealth mode / captcha solving via Browser Use Cloud

Do NOT use when:
- You only need DOM extraction (Lightpanda is 9x faster)
- You need structured QA reports with health scores (agent-browser)
- You need MCP-native tool calls without heredocs (Playwright MCP)

## Setup

Installed at: `~/Developer/browser-harness` (editable clone)
Binary on PATH: `browser-harness`

### Connect to Chrome

**Option A — Real profile (your running Chrome):**
Navigate to `chrome://inspect/#remote-debugging` and tick the checkbox. Chrome 144+ shows a per-attach popup — click Allow.

**Option B — Isolated profile (no popups):**
```bash
chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-harness
BU_CDP_URL=http://127.0.0.1:9222 browser-harness <<'PY'
print(page_info())
PY
```

### Diagnostics
```bash
browser-harness --doctor
```

## Core Workflow

Always use heredoc invocation:

```bash
browser-harness <<'PY'
new_tab("https://example.com")
wait_for_load()
capture_screenshot()
# Interact via compositor-level clicks (works through iframes/shadow DOM)
click_at_xy(x, y)
capture_screenshot()  # verify after every action
PY
```

Key helpers (pre-imported): `page_info()`, `wait_for_load()`, `new_tab(url)`, `capture_screenshot()`, `click_at_xy(x, y)`, `js(code)`, `http_get(url)`, `cdp("Method", params)`, `ensure_real_tab()`, `restart_daemon()`

## Self-Healing Pattern

When a helper is missing, write it to `~/Developer/browser-harness/agent-workspace/agent_helpers.py`. It takes effect immediately on next invocation (editable install).

## Domain Skills

Site-specific playbooks in `~/Developer/browser-harness/agent-workspace/domain-skills/{host}/`.
Enable with: `BH_DOMAIN_SKILLS=1`

Also check shared domain knowledge at `~/.claude/skills/browser-domain-skills/{host}/notes.md` before navigating to any known host.

## Cloud Browsers

Set `BROWSER_USE_API_KEY` (get from cloud.browser-use.com), then:
```bash
browser-harness <<'PY'
start_remote_daemon("work")
new_tab("https://example.com")
PY
```

## Full Reference

For complete API, interaction skills, and advanced usage:
Read `~/Developer/browser-harness/SKILL.md`
