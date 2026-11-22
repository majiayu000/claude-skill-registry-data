---
name: chronary-cli
description: Chronary CLI — command reference for managing agents, calendars, events, availability, webhooks, and iCal subscriptions from the terminal.
---

# Chronary CLI

The `chronary` CLI lets you manage Chronary resources from the command line. Built in Go for fast, cross-platform execution.

## Installation

```bash
# macOS/Linux
brew install chronary/tap/chronary

# Or download from GitHub releases
# https://github.com/Chronary/chronary-cli/releases
```

## Authentication

```bash
# Interactive login (opens browser)
chronary auth login

# Or set API key directly
export CHRONARY_API_KEY=chr_sk_live_...

# Or pass per-command
chronary agents list --api-key chr_sk_live_...
```

Configuration is stored in `~/.config/chronary/config.yaml`.

## Global Flags

| Flag | Description |
|------|-------------|
| `-o, --output` | Output format: `table` (default), `json`, `yaml` |
| `--debug` | Show HTTP requests and responses |
| `--api-key` | API key (overrides env and config) |
| `--base-url` | Custom API base URL |
| `--no-color` | Disable colored output |

## Commands

### Agents

> Plan note: Free allows 1 agent and 1 calendar; more need Developer or above (<https://chronary.ai/pricing>).

```bash
chronary agents list                          # List all agents
chronary agents list --type ai --status active # Filter by type and status
chronary agents create --name "Support Bot" --type ai
chronary agents get agt_abc123
chronary agents update agt_abc123 --name "New Name"
chronary agents delete agt_abc123
```

### Calendars

```bash
chronary calendars list                       # List all calendars
chronary calendars list --agent-id agt_abc123 # Filter by agent
chronary calendars create --name "Work" --timezone "America/New_York"
chronary calendars create --name "Meetings" --timezone "UTC" --agent-id agt_abc123
chronary calendars get cal_def456
chronary calendars update cal_def456 --name "Updated Name"
chronary calendars delete cal_def456
```

### Events

```bash
chronary events list --calendar-id cal_def456
chronary events list --agent-id agt_abc123    # All events across agent's calendars
chronary events create --calendar-id cal_def456 \
  --title "Team Standup" \
  --start-time "2026-04-16T09:00:00Z" \
  --end-time "2026-04-16T09:30:00Z"
chronary events get evt_ghi789
chronary events update evt_ghi789 --status cancelled
chronary events delete evt_ghi789
```

### Availability

```bash
# Single agent availability
chronary availability --agent-id agt_abc123 \
  --start "2026-04-16T08:00:00Z" \
  --end "2026-04-16T18:00:00Z" \
  --slot-duration 30m

# Cross-agent (find mutual free time)
chronary availability \
  --agents agt_abc123,agt_def456 \
  --start "2026-04-16T08:00:00Z" \
  --end "2026-04-16T18:00:00Z" \
  --slot-duration 1h \
  --include-busy
```

### Webhooks

```bash
chronary webhooks list
chronary webhooks create --url "https://example.com/hook" \
  --events event.created,event.updated
chronary webhooks get whk_jkl012
chronary webhooks update whk_jkl012 --active false
chronary webhooks delete whk_jkl012
```

### iCal Subscriptions

> Plan note: iCal subscriptions are not included on Free; they need Developer or above.

```bash
chronary ical list --agent-id agt_abc123
chronary ical create --agent-id agt_abc123 \
  --calendar-id cal_def456 \
  --url "https://calendar.google.com/calendar/ical/.../basic.ics" \
  --label "Google Calendar"
chronary ical get ics_mno345
chronary ical update ics_mno345 --label "Personal Google"
chronary ical delete ics_mno345
```

### Usage

```bash
chronary usage                                # Current month's usage and limits
chronary usage -o json                        # JSON output for scripting
```

### Health & Version

```bash
chronary health                               # API health check
chronary version                              # CLI version
```

## Scripting Patterns

> Plan note: the script below creates an agent and a calendar, so on Free run it once (Free allows 1 agent, 1 calendar).

```bash
# Create an agent and capture the ID
AGENT_ID=$(chronary agents create --name "Bot" --type ai -o json | jq -r '.id')

# Create a calendar for the agent
CAL_ID=$(chronary calendars create --name "Schedule" --timezone UTC --agent-id $AGENT_ID -o json | jq -r '.id')

# Check availability and pipe to another tool
chronary availability --agent-id $AGENT_ID \
  --start "2026-04-16T08:00:00Z" \
  --end "2026-04-16T18:00:00Z" \
  -o json | jq '.slots[] | .start'
```
