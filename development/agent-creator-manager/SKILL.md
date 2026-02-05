---
name: agent-creator-manager
description: Provision and register autonomous GPIA agent workspaces with unique IDs, helper functions, and execution reports; use when creating new agents or when other models need a plug to spawn agents.
---

# Agent Creator Manager

Provision new GPIA agent workspaces and register them for auditing. Each provisioned agent receives:
- A unique identifier and workspace directory
- Scoped helper functions for safe file actions
- A runner template that executes a step plan and writes a report

## Quick start

Use the skill with `capability=provision` and a JSON request:

```json
{
  "agent_name": "LogParser-01",
  "primary_goal": "Clean and format all CSVs in data/export",
  "model_id": "qwen3:latest",
  "skill_categories": ["FileSystem", "Formatting"],
  "ephemeral_mode": false,
  "max_steps": 5,
  "custom_helpers": [
    {"name": "parse_csv", "description": "Parse CSV rows safely"}
  ],
  "output_path": "C:/path/to/output",
  "requester_id": "user",
  "requester_type": "user",
  "parent_agent_id": null
}
```

You can also call the provisioning tool directly:

```
python scripts/provision_agent.py --input request.json
```

Capabilities:
- `provision` (default): Create a new agent workspace
- `list_registry`: Return registry entries
- `register_runtime`: Register an in-memory agent
- `provision_skill`: Create a skill stub (name + description)

## Inputs

Required fields:
- `agent_name`
- `primary_goal`
- `model_id`
- `skill_categories` (array)

Optional fields:
- `ephemeral_mode` (bool, default false)
- `max_steps` (int, default 5)
- `custom_helpers` (list of helper specs)
- `output_path` (string)
- `requester_id` (string)
- `requester_type` (string: user, model, agent, system)
- `parent_agent_id` (string or null)
- `policy_scope` (string, default `manual`)
- `approved` / `approval_note` (used when policy requires approval)
- `agent_template` (string, default `standard`, use `living_messenger` for a persistent loop)
- `keep_alive` (bool, default false)
- `poll_interval` (seconds, default 2.0)
- `heartbeat_interval` (seconds, default 60.0)

Guardrails are defined in `config/agent_creator_guardrails.json`.

## Outputs

Provisioning returns:
- `agent_id`
- `workspace`
- `output_path`
- `plan_path`
- `runner_path`
- `registry_path`
