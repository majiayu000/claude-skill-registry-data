---
name: "Compliance"
description: "Track compliance requirements and generate audit trail reports. Use when auditing controls, checking policies, generating audit trails."
version: "2.0.0"
author: "BytesAgain"
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
tags: ["encryption", "protection", "compliance", "security", "privacy"]
---

# Compliance

Security toolkit for logging, tracking, and exporting compliance-related activities. Each command records timestamped entries to its own log file. Call without arguments to view recent entries; call with arguments to record a new entry.

## Commands

| Command | What it does |
|---------|-------------|
| `compliance generate <input>` | Record a generate entry (no args = show recent) |
| `compliance check-strength <input>` | Record a check-strength entry (no args = show recent) |
| `compliance rotate <input>` | Record a rotate entry (no args = show recent) |
| `compliance audit <input>` | Record an audit entry (no args = show recent) |
| `compliance store <input>` | Record a store entry (no args = show recent) |
| `compliance retrieve <input>` | Record a retrieve entry (no args = show recent) |
| `compliance expire <input>` | Record an expire entry (no args = show recent) |
| `compliance policy <input>` | Record a policy entry (no args = show recent) |
| `compliance report <input>` | Record a report entry (no args = show recent) |
| `compliance hash <input>` | Record a hash entry (no args = show recent) |
| `compliance verify <input>` | Record a verify entry (no args = show recent) |
| `compliance revoke <input>` | Record a revoke entry (no args = show recent) |
| `compliance stats` | Show summary statistics across all log files |
| `compliance export <fmt>` | Export all data to json, csv, or txt format |
| `compliance search <term>` | Search all log entries for a keyword |
| `compliance recent` | Show the 20 most recent history entries |
| `compliance status` | Health check — version, entry count, disk usage, last activity |
| `compliance help` | Show help message |
| `compliance version` | Show version (v2.0.0) |

## Data Storage

All data is stored locally in `~/.local/share/compliance/`. Each command writes to its own `.log` file (e.g., `audit.log`, `policy.log`). A unified `history.log` tracks all activity with timestamps.

## Requirements

- Bash 4+
- Standard Unix utilities (`wc`, `du`, `tail`, `grep`, `date`, `sed`)

## When to Use

- Logging compliance audit findings, policy checks, and security events with timestamps
- Tracking credential rotations, revocations, and strength checks over time
- Recording data store/retrieve operations for audit trail purposes
- Searching historical compliance entries by keyword
- Exporting compliance records to JSON, CSV, or plain text for regulatory reporting

## Examples

```bash
# Record an audit finding
compliance audit "reviewed access controls for prod database — 3 issues found"

# Log a credential rotation
compliance rotate "rotated API keys for payment gateway"

# Record a policy update
compliance policy "updated data retention policy to 90 days"

# Check password strength assessment
compliance check-strength "admin account meets complexity requirements"

# Search all logs for "database"
compliance search database

# Export compliance records to JSON
compliance export json

# View overall stats
compliance stats
```

---
Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
