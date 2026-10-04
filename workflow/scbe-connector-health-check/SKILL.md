---
name: "scbe-connector-health-check"
description: "Run safety-first connector diagnostics for MCP/services used by SCBE so outreach, research, publishing, and runtime calls do not break silently."
---

# SCBE Connector Health Check

Use this skill when connector reliability matters before running social research, outreach, or automation pipelines.

## Operating Contract

1. Verify capability availability before building assumptions.
2. Record service state as `ok`, `requires_auth`, `degraded`, or `down`.
3. Prefer minimal required scope checks first, then deeper verification.
4. Never claim capability if tool access is not confirmed.
5. Always return explicit next action for each degraded connector.

## Scope

Use this for:

- checking MCP server/tool availability
- verifying API auth and endpoint reachability
- validating connector prerequisites for marketing/outreach workflows
- periodic health snapshots for SCBE runbooks

## Quick Health Workflow

1. Inventory connectors
   - list known local connector groups and expected services.

2. Availability probes
   - check tool discoverability and response latency.

3. Auth & permission check
   - confirm required env vars/tokens are configured.
   - verify command-level access for critical calls.

4. Functionality spot-check
   - run one non-destructive call per connector (read/list/search only).

5. Risk annotation
   - tag degraded services with:
     - impact level (none/low/medium/high)
     - fallback behavior
     - owner and triage owner if available

6. Publish health record
   - provide compact checklist and ordered repair steps.

## Output Contract

- `inventory`: expected services + owner intent.
- `status`: per-connector status map.
- `checks`: quick probe results and timestamps.
- `failures`: auth or dependency blockers with exact error text.
- `next_steps`: prioritized remediation commands or decisions.
- `ready_for_live_use`: true only if primary services are green.

## Connector Priority Matrix (example)

- primary: GitHub, Notion, Obsidian, HF, browser service.
- secondary: Linear, Discord/Slack, Telegram, marketplace tools.
- tertiary: optional APIs used only for enrichment.

## Recovery Patterns

- If `requires_auth`: document missing scopes, rotate creds, rerun spot-check.
- If `degraded`: reduce non-critical calls, queue retries, add backoff and cache.
- If `down`: disable workflow branch and use fallback runbook with explicit user visibility.

## References

- `references/connector-health-checklist.md`
