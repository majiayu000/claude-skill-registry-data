---
name: mde-claude-code-telemetry
description: Validate and configure Claude Code telemetry settings.json env vars against the official monitoring docs. Use when modifying OTEL env vars, debugging telemetry, or verifying settings compliance.
---

# Claude Code Telemetry Settings Skill

Validates `.claude/settings.json` env vars against the official Claude Code monitoring documentation at https://code.claude.com/docs/en/monitoring-usage.

## When to use

- Adding or changing OTEL env vars in settings.json
- Debugging why telemetry data isn't appearing in the collector
- Verifying settings after a Claude Code upgrade
- Checking protocol/endpoint consistency

## Quick validation

```bash
uv run mde-py telemetry verify
```

This runs all checks including the "Official Docs Compliance" section that validates every env var against the documented set.

## Official env vars reference

The complete list of Claude Code telemetry env vars is in:
`docs/research/trail/deep-reviews/claude-code-monitoring-reference.md`

### Core (required)

| Variable | Value | Purpose |
|----------|-------|---------|
| `CLAUDE_CODE_ENABLE_TELEMETRY` | `1` | Master switch — nothing works without this |
| `OTEL_METRICS_EXPORTER` | `otlp` | Enable metrics export |
| `OTEL_LOGS_EXPORTER` | `otlp` | Enable events/logs export |

### Protocol/endpoint (must be consistent)

| Protocol | Endpoint port | Notes |
|----------|--------------|-------|
| `grpc` | `:4317` | Default, most efficient |
| `http/json` | `:4318` | Human-readable, debuggable |
| `http/protobuf` | `:4318` | Compact binary over HTTP |

### Privacy controls

| Variable | Default | When to enable |
|----------|---------|---------------|
| `OTEL_LOG_USER_PROMPTS` | `0` (disabled) | Only on self-hosted collectors — logs full prompt text |
| `OTEL_LOG_TOOL_DETAILS` | `0` (disabled) | Logs MCP server/tool names and skill names |

### Custom attributes

Use `OTEL_RESOURCE_ATTRIBUTES` for project/team segmentation:
```
OTEL_RESOURCE_ATTRIBUTES=project=mde,environment=dev
```

**Do NOT override `service.name`** — Claude Code hardcodes `service.name=claude-code` and the OTEL JS SDK env detector will override it if you set it here, breaking dashboard queries.

## Key facts

- Claude Code emits **metrics and events/logs only** — no traces (`OTEL_TRACES_EXPORTER` is not used)
- Events go via the OTEL Logs API, not the Traces API
- The meter name is `com.anthropic.claude_code`
- 8 metrics: session.count, lines_of_code.count, pull_request.count, commit.count, cost.usage, token.usage, code_edit_tool.decision, active_time.total
- 5 event types: user_prompt, tool_result, api_request, api_error, tool_decision
- All events share a `prompt.id` UUID for correlation

## Validation source code

The validation logic lives in `src/mde/telemetry_verify.py`:
- `_OFFICIAL_VARS` — complete set of 22 documented env vars
- `_check_settings_against_docs()` — validates each var against the official set
- Protocol/endpoint consistency checking
