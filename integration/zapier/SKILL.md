---
name: zapier
description: "Build Zapier automations with triggers, actions, filters, paths, and storage; handle mapping and execution errors."
category: automation
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["zapier", "automation", "zaps", "integration", "no-code", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Zapier Automation AI Skill Guide

## Overview & Engine Architecture

Zapier connects apps through Zaps: a trigger starts a run, then actions execute in order. Filters, Paths, and formatters shape branching; Tables/Storage hold small state. Agents design idempotent flows, map fields explicitly, and avoid infinite loops (A updates B updates A). Prefer official connectors; fall back to Webhooks by Zapier with signed payloads when needed.

```
Trigger app event
   -> Filter / Paths
       -> Action steps (create/update/find)
           -> Optional delay / digest / code
Error handler / email alerts on failure
```

## When to use this skill

- Wiring SaaS tools without a custom integration service
- Prototyping syncs before investing in first-party APIs
- Adding human-in-the-loop approvals via Paths
- Replacing fragile email-forward hacks with structured Zaps

## Operational directives

1. Name Zaps with source -> destination and purpose (`HubSpot deal won -> Asana project`).
2. Always "Find before Create" when a unique external ID exists to prevent duplicates.
3. Guard loops: exclude Zap-authored updates from triggers when the platform allows.
4. Keep secrets in Zapier connections, not in hard-coded Code step strings committed elsewhere.
5. Turn on error notifications; dead Zaps silently drop business events.

## Field mapping hygiene

| Smell | Better approach |
| --- | --- |
| Mapping display names that change | Map stable IDs / API property names |
| One mega-Zap with 30 steps | Split by domain; use Sub-Zaps or shared storage carefully |
| Catch-all Code step for everything | Prefer native Formatter/Filter; Code only for small transforms |
| Trigger on every CRM property change | Narrow to stage/status fields that matter |

## Webhook sketch (catch hook)

```text
1. Trigger: Webhooks by Zapier - Catch Hook
2. Filter: only continue if header X-Env = production
3. Action: Create task in Asana with parsed JSON fields
4. Action: POST acknowledgment to your system if required
```

## Best practices

- Document owner, last review date, and upstream/downstream systems in the Zap description.
- Use staging connections when apps support sandboxes; test with sample payloads.
- Prefer Zapier Interfaces/Tables only for lightweight state - not as a system of record.
- Rate-limit chatty triggers; batch with Digests when humans do not need instant pings.

## Limitations

- Task limits, premium apps, and multi-step Paths depend on plan.
- Complex transforms and exactly-once delivery may require a real queue/worker.
- Compliance (HIPAA, data residency) may prohibit certain Zap routes.

## Related skills

- `@hubspot` / `@salesforce` - CRM triggers and field design
- `@asana` / `@trello` - common action targets
- `@n8n` - self-hosted alternative when data must stay in-house
