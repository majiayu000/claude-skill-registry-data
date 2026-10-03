---
name: ls-ui-browser-debugging
description: "UI review and browser-driven debugging workflow for Chrome DevTools MCP, Playwright MCP/CLI, browser ownership, evidence capture, minimal fixes, and durable UI regression tests."
metadata:
  version: "1.0"
compatibility:
  notes:
    - "Includes read-only helpers for Chrome DevTools MCP environment inspection, URL reachability checks, and structured npm snapshot checks."
---

# UI Browser Debugging

Use this skill for UI review, browser-driven debugging, visual/a11y feasibility
checks, console or network triage, Chrome DevTools MCP setup repair, and turning
confirmed UI issues into durable Playwright or project-native regression tests.

## First Inspect The Project

Before opening a browser:

- Identify the app root, package manager, dev-server command, target route, and
  existing UI/e2e test stack.
- Detect browser MCP tools already available in the active agent. If Chrome
  DevTools MCP tools are usable, use them and do not offer setup.
- If tools are missing, inspect the active agent's MCP profiles with that
  agent's native discovery command or current docs.
- If a Chrome DevTools MCP profile exists, prefer use or repair guidance before
  proposing bootstrap.
- Bootstrap only when no usable profile exists, translating the standard MCP
  server definition through current source-backed agent docs.

## Decision Flow

- **MCP missing or misconfigured:** use
  [MCP bootstrap and repair](./references/mcp-bootstrap-and-repair.md).
- **Browser ownership or cleanup:** use
  [browser session management](./references/browser-session-management.md).
- **UI critique and debugging:** use
  [UI feasibility review](./references/ui-feasibility-review.md).
- **Multi-agent work:** use
  [subagent browser workflows](./references/subagent-browser-workflows.md).
- **Tool choice or current facts:** use
  [browser MCP landscape](./references/browser-mcp-landscape.md).

## Chrome DevTools MCP Defaults

Upstream Chrome DevTools MCP enables usage statistics and CrUX field data for
performance work by default. Network-header redaction and isolated profiles are
disabled upstream by default.

For local agent work, prefer privacy-oriented defaults:

```bash
npx -y chrome-devtools-mcp@latest \
  --no-usage-statistics \
  --no-performance-crux \
  --redactNetworkHeaders \
  --isolated=true
```

Use isolated, ephemeral browser state by default. Current Chrome DevTools MCP
page-id routing is enabled by default; assign an explicit page id when sharing
one server, or assign each actor a unique isolated MCP session id. Choose
persistent profile mode only when login or state reuse is required, and then
derive the dedicated absolute `.localsetup-maint/ui-browser-profiles/chrome-devtools`
profile from an explicit project/state root. Do not attach
to a user's everyday Chrome profile unless the user explicitly authorizes that
browser state.

Before opening a new page, use the browser tool's page listing capability
(`list_pages` for Chrome DevTools MCP) and reuse the owned active page for the
same app or route family when practical. Record every agent-created page with
`browser_session_guard.py` before use, and close or mark closed every owned
page at task end. Never close user or pre-existing pages unless the user
explicitly authorizes that action.

## Helper Commands

```bash
python3 scripts/chrome_devtools_mcp_environment.py inspect --state-root <absolute-project-root> --json
python3 scripts/chrome_devtools_mcp_environment.py inspect --state-root <absolute-project-root> --json --require
python3 scripts/chrome_devtools_mcp_environment.py standard-config --json
python3 scripts/chrome_devtools_mcp_environment.py standard-config --mode persistent --state-root <absolute-project-root> --json
python3 scripts/browser_session_guard.py start --tool chrome-devtools --mode isolated --session-id <unique-mcp-session-id> --mcp-session-id <same-id> --state-root <absolute-project-root> --owner <agent> --purpose <text> --json
python3 scripts/browser_session_guard.py record-page --session-id <id> --state-root <absolute-project-root> --page-id <id> --page-owner <agent> --url <url> --purpose <text> --json
python3 scripts/browser_session_guard.py select-page --session-id <id> --state-root <absolute-project-root> --page-id <id> --json
python3 scripts/browser_session_guard.py mark-closed --session-id <id> --state-root <absolute-project-root> --page-id <id> --json
python3 scripts/browser_session_guard.py finish --session-id <id> --state-root <absolute-project-root> --json
python3 scripts/browser_session_guard.py audit --session-id <id> --state-root <absolute-project-root> --json
python3 scripts/chrome_devtools_mcp_environment.py example --agent codex --json
python3 scripts/verify_ui_browser_debugging_sources.py
python3 scripts/verify_ui_browser_debugging_sources.py --refresh --json
```

The verifier's non-npm URL checks prove reachability only, not that a page still
supports a cited claim; exact npm snapshot checks remain separate. The
environment and verifier helpers are read-only. The session guard writes
private ownership records under `.localsetup-maint/ui-browser-sessions/` and
reports cleanup guidance only. These helpers do not edit agent config, delete
profiles, kill browsers, install packages, change existing MCP profiles, call
MCP tools, or close user pages directly.

## Evidence Rules

- Prefer `take_snapshot` for interaction targets and accessibility structure.
- Use screenshots for visual layout evidence.
- Use console, network, Lighthouse, and performance traces only when relevant
  and available.
- Degrade gracefully when the MCP profile is `--slim` or omits network,
  performance, Lighthouse, or screenshot capabilities.
- Record compact evidence: route, viewport, page id, observed issue, tool used,
  and artifact path when one exists.
- Convert confirmed user-facing issues into a focused regression test whenever
  the project has a suitable test stack.

## Frontend App QA Fallback

When a frontend app task does not name a browser-testing skill, keep this skill
canonical for QA. Use Chrome DevTools MCP or Playwright to verify at least one
desktop and one mobile viewport, capture screenshots for visual regressions,
check console and network errors, exercise the primary interaction path, and
record the exact route, viewport, and command or tool used.
