---
name: "Gdpr"
description: "Audit GDPR compliance, generate privacy policies, and document data flows. Use when auditing practices, drafting policies, or checking consent flows."
version: "2.0.0"
author: "BytesAgain"
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
tags: ["encryption", "protection", "gdpr", "compliance", "privacy"]
---

# GDPR

GDPR v2.0.0 — a security toolkit for managing GDPR compliance workflows from the command line. Log security operations, audit trails, policy changes, and more. Each entry is timestamped and persisted locally. Works entirely offline — your data never leaves your machine.

## Commands

### Domain Commands

Each domain command works in two modes: **log mode** (with arguments) saves a timestamped entry, **view mode** (no arguments) shows the 20 most recent entries.

| Command | Description |
|---------|-------------|
| `gdpr generate <input>` | Log a generation event (privacy policy, consent form, etc.) |
| `gdpr check-strength <input>` | Log a strength check result (password, encryption, etc.) |
| `gdpr rotate <input>` | Log a key/credential rotation event |
| `gdpr audit <input>` | Log an audit finding or compliance check result |
| `gdpr store <input>` | Log a data storage event (what was stored and where) |
| `gdpr retrieve <input>` | Log a data retrieval/access event |
| `gdpr expire <input>` | Log a data expiration or retention event |
| `gdpr policy <input>` | Log a policy change or update |
| `gdpr report <input>` | Log a report entry or compliance summary |
| `gdpr hash <input>` | Log a hashing operation (data anonymization, etc.) |
| `gdpr verify <input>` | Log a verification result (identity, consent, integrity) |
| `gdpr revoke <input>` | Log a revocation event (consent withdrawal, access removal) |

### Utility Commands

| Command | Description |
|---------|-------------|
| `gdpr stats` | Show summary statistics across all log files |
| `gdpr export <fmt>` | Export all data to a file (formats: `json`, `csv`, `txt`) |
| `gdpr search <term>` | Search all log entries for a term (case-insensitive) |
| `gdpr recent` | Show the 20 most recent entries from the activity log |
| `gdpr status` | Health check — version, data dir, entry count, disk usage |
| `gdpr help` | Show the built-in help message |
| `gdpr version` | Print the current version (v2.0.0) |

## Data Storage

All data is stored locally at `~/.local/share/gdpr/`. Each domain command writes to its own log file (e.g., `audit.log`, `policy.log`, `revoke.log`). A unified `history.log` tracks all actions across commands. Use `export` to back up your data at any time.

## Requirements

- Bash (4.0+)
- No external dependencies — pure shell script
- No network access required

## When to Use

- Auditing GDPR compliance across your organization's data practices
- Logging data access and retrieval events for accountability
- Tracking consent revocations and data subject requests
- Recording key/credential rotation schedules
- Documenting policy changes with timestamps for audit trails
- Managing data retention and expiration workflows
- Generating compliance reports from logged activity
- Exporting audit logs for regulatory submissions

## Examples

```bash
# Log a compliance audit finding
gdpr audit "User data export endpoint missing encryption — needs fix"

# Record a policy update
gdpr policy "Updated cookie consent banner to include analytics opt-out"

# Log a consent revocation
gdpr revoke "User #4521 withdrew marketing consent via email"

# Track a key rotation
gdpr rotate "API key rotated for payment service, old key expires 2025-04-01"

# Log data storage event
gdpr store "Backup of EU customer PII moved to Frankfurt region"

# Verify identity check
gdpr verify "KYC verification passed for account #8832"

# Log a data expiration
gdpr expire "Inactive accounts older than 2 years purged per retention policy"

# Generate a hash record
gdpr hash "SHA-256 hash of user export file: a3f8c9..."

# Search across all logs
gdpr search "consent"

# Export everything as CSV
gdpr export csv

# Check overall status
gdpr status

# View recent activity
gdpr recent
```

---
Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
