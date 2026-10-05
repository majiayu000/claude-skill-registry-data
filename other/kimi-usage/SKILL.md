---
name: kimi-usage
description: Show Kimi Code plan-quota usage and pace (5h / weekly / monthly windows), or wire the Kimi footer to Clade's quota pace indicator
when_to_use: "Kimi usage, Kimi quota, Kimi Code limits, 5h limit, monthly limit, Kimi rate limit, Kimi pace, configure Kimi status line, Kimi footer"
argument-hint: '[setup [off]|style [minimal|icon|detail|off]|theme [name]|--json]'
user_invocable: true
---

# Kimi Usage

Shows the Kimi Code managed-plan quota windows — the rolling 5-hour limit, the
weekly limit where the plan has one, and the monthly limit with its
kimi/code split — each compared against Clade's 95% target pace. It can also
wire Kimi Code's footer (`[status_line]` in `~/.kimi-code/tui.toml`) to the
same indicator the Claude Code status line and `/codex-usage` show.

## Usage

```text
/kimi-usage
/kimi-usage setup
/kimi-usage setup off
/kimi-usage style icon
/kimi-usage theme
/kimi-usage theme dragon
/kimi-usage --json
```

The helper talks to Kimi Code's own local server (`kimi web`, the documented
`GET /api/v1/oauth/usage` route) with the loopback token Kimi keeps in
`~/.kimi-code/server.token`. It reuses a running instance and otherwise starts
one for the call and shuts it down. It never reads or refreshes the OAuth
credential in `~/.kimi-code/credentials/`.
