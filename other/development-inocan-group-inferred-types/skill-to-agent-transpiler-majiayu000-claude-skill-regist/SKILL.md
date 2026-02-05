---
name: skill-to-agent-transpiler
description: Compile a skill entry into a provisioned agent request with strict guardrails (approval, quotas, TTL). Use when translating skills into runnable agents or when you need a controlled Skill→Agent path.
---

# Skill → Agent Transpiler

Transforms a skill entry from `skills/INDEX.json` into a provisionable agent request.
This path is strictly guarded and defaults to compile-only unless approved.

## Capabilities

- `compile` (default): Return a guarded agent request (no provisioning)
- `provision`: Provision the agent via the Creator Manager (requires `approved=true`)

## Inputs

Required:
- `skill_id`

Optional:
- `agent_name`
- `model_id`
- `max_steps`
- `output_path`
- `approved` (bool, required for `provision`)
- `approval_note`
- `requester_id`
- `parent_agent_id`

Guardrails are enforced by `config/agent_creator_guardrails.json` under the `transpiler` scope.

## Example (compile)

```json
{
  "skill_id": "automation/dynamic-budget-orchestrator",
  "agent_name": "Budget-Orchestrator-Agent",
  "model_id": "qwen3:latest"
}
```

## Example (provision)

```json
{
  "capability": "provision",
  "skill_id": "automation/dynamic-budget-orchestrator",
  "approved": true,
  "approval_note": "Reviewed by operator"
}
```

## Script

```
python skills/automation/skill-to-agent-transpiler/scripts/transpile_skill.py --skill-id automation/dynamic-budget-orchestrator
```
