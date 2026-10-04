---
name: zabbix
description: |
  Use when working with Zabbix — zabbix monitoring platform CLI. Use when
  working with Zabbix hosts, templates, triggers, events, logs, maintenance,
  dashboards, or configuration export/import.
connection_type: zabbix
preload: false
---

# Zabbix CLI Skill

Execute `ct-zabbix-cli` commands with credential injection via environment variables.

## CLI Reference

<critical>
Output is always compact tabular format (toon) — **no output flags needed**.
</critical>

### Severity Scale

| Value | Label | Meaning |
|-------|-------|---------|
| 0 | Not classified | Informational only |
| 1 | Information | Low-noise status |
| 2 | Warning | Degraded, approaching threshold |
| 3 | Average | Service impacted, needs attention |
| 4 | High | Major impact, escalate soon |
| 5 | Disaster | Complete outage, page immediately |

### Read-Only Commands

```bash
# Hosts — filter before listing to avoid large output
ct-zabbix-cli host list
ct-zabbix-cli host list --group "Linux servers"   # filter by group name
ct-zabbix-cli host list --search "web"            # search by name pattern
ct-zabbix-cli host list --limit 20                # cap results (default 50)
ct-zabbix-cli host get --host-id 10084

# Templates
ct-zabbix-cli template list
ct-zabbix-cli template get --template-id 10001

# Items (metrics)
ct-zabbix-cli item list --host-id 10084
ct-zabbix-cli item list --host-id 10084 --search "cpu*"   # wildcard name search
ct-zabbix-cli item get --item-id 12345
ct-zabbix-cli item history --item-id 12345 --limit 10
ct-zabbix-cli item history --item-id 12345 --limit 20 --sort ASC  # oldest first for trends

# Log items (value_type=2 — Zabbix log monitoring)
ct-zabbix-cli log list --host 10084                          # list log items for a host
ct-zabbix-cli log list --host 10084 --search "syslog*"      # filter by name pattern
ct-zabbix-cli log tail --item-id 12345 --limit 20            # last 20 log entries
ct-zabbix-cli log tail --item-id 12345 --limit 50 --sort ASC # oldest first

# Triggers — always scope by host in production
ct-zabbix-cli trigger list --host 10084
ct-zabbix-cli trigger list --host 10084 --min-severity 3       # average and above
ct-zabbix-cli trigger list --host 10084 --active-only          # skip disabled triggers
ct-zabbix-cli trigger list --host 10084 --in-problem           # only currently firing
ct-zabbix-cli trigger get --trigger-id 12345

# Events & Problems — always filter on busy Zabbix instances
ct-zabbix-cli problem list                                         # current active problems
ct-zabbix-cli problem list --min-severity 4                        # high severity and above
ct-zabbix-cli problem list --host 10084                            # problems for one host
ct-zabbix-cli problem list --group "Database servers"              # problems for a host group
ct-zabbix-cli event list --limit 20                                # recent events
ct-zabbix-cli event list --host 10084 --limit 50                   # events for a host
ct-zabbix-cli event list --min-severity 3 --limit 30               # average+ events

# Host Groups
ct-zabbix-cli hostgroup list

# Users
ct-zabbix-cli user list
ct-zabbix-cli user get --user-id 1

# Actions
ct-zabbix-cli action list

# Maintenance
ct-zabbix-cli maintenance list

# Dashboards
ct-zabbix-cli dashboard list
ct-zabbix-cli dashboard get --dashboard-id 1

# Server Info
ct-zabbix-cli info version

# Export
ct-zabbix-cli export hosts --host-ids 10084
ct-zabbix-cli export templates --template-ids 10001
```

### Write Commands (Require Approval)

```bash
# Host management
ct-zabbix-cli host create --host "new-host" --group-id 2 --ip "192.168.1.100"
ct-zabbix-cli host enable --host-ids 10084
ct-zabbix-cli host disable --host-ids 10084
ct-zabbix-cli host delete --host-ids 10084
ct-zabbix-cli host update --host-id 10084 --name "new-name"

# Template linking
ct-zabbix-cli template link --host-id 10084 --template-id 10001
ct-zabbix-cli template unlink --host-id 10084 --template-id 10001

# Trigger management
ct-zabbix-cli trigger enable --trigger-ids 12345
ct-zabbix-cli trigger disable --trigger-ids 12345

# Event acknowledgement
ct-zabbix-cli event ack --event-id 12345 --message "Investigating"

# Host group management
ct-zabbix-cli hostgroup create --name "New Group"
ct-zabbix-cli hostgroup delete --group-ids 5

# Action management
ct-zabbix-cli action enable --action-ids 1
ct-zabbix-cli action disable --action-ids 1

# Maintenance windows
ct-zabbix-cli maintenance create --name "Patching" --duration 7200 --host-group-ids 2
ct-zabbix-cli maintenance delete --maintenance-ids 1

# User management
ct-zabbix-cli user create --alias "newuser" --name "New User" --password "secure123" --group-id 7

# Configuration import
ct-zabbix-cli import --file config.json
```

## Execution Guidelines

<critical>
**Parallel execution**: When querying multiple hosts or items, use background jobs:
```bash
for host_id in 10084 10085 10086; do
    ct-zabbix-cli host get --host-id "$host_id" &
done
wait
```
</critical>

- Read-only commands: set `requires_approval=false`
- Write commands (create, delete, enable, disable, update, link, unlink, ack, import): set `requires_approval=true`
- Consolidate related queries into a single script
- Never print or expose environment variables or credentials

## Workflows

### Incident Triage ("What's on fire right now?")

```bash
# 1. See active problems at high severity first
ct-zabbix-cli problem list --min-severity 4

# 2. Drill into the affected host
ct-zabbix-cli host get --host-id <id>
ct-zabbix-cli trigger list --host <id> --in-problem --min-severity 3

# 3. Check recent event history
ct-zabbix-cli event list --host <id> --limit 20

# 4. Acknowledge and record action
ct-zabbix-cli event ack --event-id <id> --message "Investigating — restarting service"
```

### Alert Fatigue / Noisy Trigger ("Silence this flapping alert")

```bash
# 1. Find the host
ct-zabbix-cli host list --search "hostname"

# 2. List its active triggers and spot the noisy one
ct-zabbix-cli trigger list --host <id> --active-only

# 3. Inspect the trigger threshold
ct-zabbix-cli trigger get --trigger-id <id>

# 4. Disable it (requires approval)
ct-zabbix-cli trigger disable --trigger-ids <id>
```

### Pre-Maintenance Window ("Patch DB servers tonight, suppress alerts")

```bash
# 1. Find the host group
ct-zabbix-cli hostgroup list

# 2. Verify which hosts are in scope
ct-zabbix-cli host list --group "Database servers"

# 3. Create 2-hour maintenance window
ct-zabbix-cli maintenance create --name "DB Patching" --duration 7200 --host-group-ids <id>

# 4. Confirm scheduling
ct-zabbix-cli maintenance list
```

### Capacity Investigation ("Is host X running out of disk?")

```bash
# 1. Find disk/CPU/memory item IDs
ct-zabbix-cli item list --host-id <id>

# 2. Get recent 20 samples (newest first, default)
ct-zabbix-cli item history --item-id <disk-item-id> --limit 20

# 3. Get oldest-to-newest to see the trend direction
ct-zabbix-cli item history --item-id <disk-item-id> --limit 20 --sort ASC
```

### Log Investigation ("Why did the application crash?")

```bash
# 1. List log-monitoring items for the affected host
ct-zabbix-cli log list --host <id>

# 2. Narrow to relevant log source
ct-zabbix-cli log list --host <id> --search "syslog*"

# 3. Tail recent entries (newest first)
ct-zabbix-cli log tail --item-id <log-item-id> --limit 50

# 4. Get chronological view around the incident time
ct-zabbix-cli log tail --item-id <log-item-id> --limit 100 --sort ASC
```

### New Host Onboarding ("Add server to monitoring")

```bash
# 1. Get group and template IDs
ct-zabbix-cli hostgroup list
ct-zabbix-cli template list

# 2. Create host
ct-zabbix-cli host create --host "prod-web-05" --group-id <id> --ip "10.0.1.25"

# 3. Link monitoring template
ct-zabbix-cli template link --host-id <new-id> --template-id <template-id>

# 4. Verify items are collecting
ct-zabbix-cli item list --host-id <new-id>
```

## Output Format

Present results as a structured report:
```
Zabbix Report
═════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

- **Never run `event list` without `--limit`** on a busy Zabbix — can return thousands of rows
- **`problem list` vs `event list`**: `problem list` shows only current unresolved problems (use this first); `event list` shows historical events
- **`trigger list` without `--host`** returns all triggers across all hosts — always scope by host in production
- **`log` commands vs `item history`**: Use `log list`/`log tail` for log-type items (value_type=2); use `item history` for numeric metrics. Mixing them returns empty results silently
- Export defaults to YAML but Zabbix < 5.2 only supports JSON/XML; CLI auto-detects and falls back
- `--host-ids` and `--group-ids` accept space-separated IDs, not comma-separated
- `maintenance create` starts immediately; `--duration` is in seconds (e.g., 7200 = 2 hours)
- Always get host/group IDs from `list` commands before running write operations
