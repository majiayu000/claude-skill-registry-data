---
name: otel-monitoring-setup
version: 0.2.1
description: Use PROACTIVELY when setting up OpenTelemetry monitoring for Claude Code usage tracking, cost analysis, or productivity metrics. Provides local PoC mode (full Docker stack with Grafana) and enterprise mode (centralized infrastructure). Configures telemetry collection, imports dashboards, and verifies data flow. Not for non-Claude telemetry or custom metric definitions.
---

# Claude Code OpenTelemetry Setup

Automated workflow for setting up OpenTelemetry telemetry collection for Claude Code usage monitoring, cost tracking, and productivity analytics.

## Quick Decision Matrix

| User Request | Mode | Action |
|--------------|------|--------|
| "Set up telemetry locally" | Mode 1 | Full PoC stack |
| "I want to try OpenTelemetry" | Mode 1 | Full PoC stack |
| "Connect to company endpoint" | Mode 2 | Enterprise config |
| "Set up for team rollout" | Mode 2 | Enterprise + docs |
| "Dashboard not working" | Troubleshoot | See known issues |

## Mode 1: Local PoC Setup

**Goal**: Complete local telemetry stack for individual developer

**Creates**:
- OpenTelemetry Collector (receives data)
- Prometheus (stores metrics)
- Loki (stores logs)
- Grafana (dashboards)

**Prerequisites**:
- Docker Desktop running
- 2GB free disk space
- Write access to ~/.claude/

**Time**: 5-7 minutes

**Workflow**: `modes/mode1-poc-setup.md`

**Output**:
- Grafana at http://localhost:3000 (admin/admin)
- Management scripts in ~/.claude/telemetry/

## Mode 2: Enterprise Setup

**Goal**: Connect Claude Code to centralized company infrastructure

**Required Info**:
- OTEL Collector endpoint URL
- Authentication (API key or certificates)
- Team/department identifier

**Time**: 2-3 minutes

**Workflow**: `modes/mode2-enterprise.md`

**Output**:
- settings.json configured for central endpoint
- Team rollout documentation

## Critical Configuration

**REQUIRED in settings.json** (without these, telemetry won't work):

```json
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "http://localhost:4317"
  }
}
```

**Must restart Claude Code after settings changes!**

## Pre-Flight Check

Always run before setup:

```bash
# Verify Docker is running
docker info > /dev/null 2>&1 || echo "Start Docker Desktop first"

# Check available ports
for port in 3000 4317 4318 8889 9090; do
  lsof -i :$port > /dev/null 2>&1 && echo "Port $port in use"
done

# Check disk space (need 2GB)
df -h ~/.claude
```

## Metrics Collected

- Session counts and active time
- Token usage (input/output/cached)
- API costs by model (USD)
- Lines of code modified
- Commits and PRs created

## Management Commands

```bash
# Start telemetry stack
~/.claude/telemetry/start-telemetry.sh

# Stop (preserves data)
~/.claude/telemetry/stop-telemetry.sh

# Full cleanup (removes all data)
~/.claude/telemetry/cleanup-telemetry.sh
```

## Common Issues

### No Data in Dashboard
1. Check OTEL_METRICS_EXPORTER and OTEL_LOGS_EXPORTER are set
2. Verify Claude Code was restarted
3. See `reference/known-issues.md`

### Datasource Not Found
Dashboard has wrong UID. Detect your UID:
```bash
curl -s http://admin:admin@localhost:3000/api/datasources | jq '.[0].uid'
```
Replace in dashboard JSON and re-import.

### Metric Names Double Prefix
Metrics use `claude_code_claude_code_*` format. Update dashboard queries accordingly.

## Reference Documentation

- `modes/mode1-poc-setup.md` - Detailed local setup workflow
- `modes/mode2-enterprise.md` - Enterprise configuration steps
- `reference/known-issues.md` - Troubleshooting guide
- `templates/` - Configuration file templates
- `dashboards/` - Grafana dashboard JSON files

## Safety Checklist

- [ ] Backup settings.json before modification
- [ ] Verify Docker is running first
- [ ] Check ports are available
- [ ] Test data flow before declaring success
- [ ] Provide cleanup instructions

---

**Version**: 1.1.0 | **Author**: Prometheus Team
