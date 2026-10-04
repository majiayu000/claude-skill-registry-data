---
name: company
description: X Company management panel — real-time dashboard with integrated terminal showing agent activity, core roles, specialists, and project progress. Use to start/stop the company panel. Triggers on "company", "monitor", "dashboard", "team status", "who is working".
user_invocable: true
match_terms:
  - company
  - monitor
  - dashboard
  - team
  - who is working
---

# X Company Panel

Real-time management dashboard with integrated terminal:
- **Core Roles** (CEO, CTO, PM, BA, HR) activity
- **Specialist Agents** running status
- **Project Progress** & Sprint Tasks
- **Terminal** — run commands directly from the panel

## Usage

### Start
```
/company start
```
or just `/company`

### Stop
```
/company stop
```

## Commands

Based on the argument:

- **start** (default): Start the dashboard server and open browser
  ```bash
  cd "$CLAUDE_PROJECT_DIR" && bash .claude/monitor/start.sh
  ```

- **stop**: Stop the dashboard server
  ```bash
  cd "$CLAUDE_PROJECT_DIR" && bash .claude/monitor/stop.sh
  ```

Port is auto-assigned per project (range 3800-3999).

## How It Works

1. Hooks in `settings.json` auto-track agent activity
2. State is written to `.claude/monitor/state/activity.json`
3. Web server pushes updates via Server-Sent Events (SSE)
4. Dashboard + terminal update in real-time
5. Terminal uses Python PTY bridge for full shell access
