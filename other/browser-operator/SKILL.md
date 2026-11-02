---
name: browser-operator
description: Operate an authorized browser using DOM snapshots and repeatable actions.
priority: P0
category: browser
status: builtin-guidance
---

# Browser Operator

**Scope:** agent-browser + Microsoft Playwright MCP. **Source:** https://github.com/vercel-labs/agent-browser

## Workflow

First decide whether webpage interaction is needed. For deployments, migrations, cloud administration, configuration, builds, logs and database work, prefer available CLI tools or documented APIs through start_process. A service having a web dashboard does not make it a browser task. Honor the user's explicit tool preference. Use browser tools only for required webpage interactions that CLI/API cannot complete, and explain that step.

Use existing Remote Arc shared_tab_read for read-only work on a tab the user shared first. In the user's own browser with the Remote Arc Browser extension 0.4.0 or later, shared_tab_open opens a tab on a site the user allowed (SITE_NOT_ALLOWED means ask the user to click Allow once) and shared_tab_act clicks, fills, selects, presses keys, navigates and waits there; final submits need effect=submit with an idempotency_key and are settled with action=confirm. For multi-step work on a linked computer, use the Remote Arc Browser Runner (browser_runner_*) when it is enabled for the device: a separate Runner window by default, or the user's own Chrome with browser=your_chrome when the user asks for it; otherwise use locally approved agent-browser or Playwright, in a separate profile; never attach to personal sessions without explicit permission. Steps: 1) confirm device, origin and requested interaction scope; 2) snapshot DOM and locate stable accessible selectors; 3) plan bounded clicks/fills; 4) ask permission for modifying site state, checkout, account settings, irreversible submissions; 5) verify changed page and report evidence. Keep navigation URLs within allowed origins. Never use anti-bot evasion, cookie export, credential harvesting or silent downloads. Headless browser must be explicitly chosen; a Chrome extension tab is a different permission boundary. CLI examples only after installation: agent-browser open https://example.com; agent-browser snapshot -i; agent-browser close. If browser CLI is absent, use existing Remote Arc browser tools and report limits.

## Device and permission gates

Required authorization scopes: browser:read, browser:interact. Scripts, OS/desktop actions, external service side effects, media generation and paid API usage require independent user-approved execution permissions. This skill does not elevate Remote Arc Tool privileges or authorize use of hidden credentials.

## Preflight

Check the engines this skill names before relying on them, with tools you already have (for example `<engine> --version` through start_process, or list_directory on its install folder). Missing executors must be installed explicitly on the correct user device. A Skill being built-in is NOT evidence an engine is present.

## Evidence of completion

Report input constraints, executed tools and device, verified output path/result, permissions used, cost (if known) and failures. Do not imply successful execution from merely writing a plan.
