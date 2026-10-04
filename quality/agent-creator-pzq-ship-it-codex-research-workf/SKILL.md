---
name: agent-creator
description: Create, update, migrate, or validate Codex native custom agents that can be spawned as subagents. Use when the user asks to define an agent, convert a Markdown agent spec into a Codex-recognized agent, create files under .codex/agents or ~/.codex/agents, standardize agent role prompts, or debug why an agent can be read but not spawned.
---

# Agent Creator

## Purpose

Create Codex native custom agents as standalone TOML files, not merely Markdown prompt documents. A Markdown spec can be used as source material, but Codex-recognized custom agents live in `~/.codex/agents/*.toml` for global use or `.codex/agents/*.toml` for project use.

## Quick Workflow

1. Decide scope.
   - Use `.codex/agents/` for project-specific agents.
   - Use `~/.codex/agents/` for portable personal agents.
   - For migration packages, write both locations when requested.
2. Define the agent contract.
   - `name`: snake_case identifier used when spawning.
   - `description`: concise routing guidance for when to use this agent.
   - `developer_instructions`: role, inputs, outputs, ownership boundaries, workflow, quality gates, and final evidence.
3. Create or update the TOML.
   - Prefer `scripts/create_agent.py` for deterministic formatting and validation.
   - Use one TOML file per agent.
   - Use kebab-case filenames, for example `ppt-storyboard.toml`.
4. Validate.
   - Parse the TOML.
   - Check required fields.
   - Confirm `codex features list` has the local multi-agent flags enabled.
   - Restart Codex before testing a newly added custom agent if the current session does not see it.
5. Availability test.
   - Ask for a lightweight native subagent test with no file edits.
   - If the custom name is unavailable, fall back to built-in `worker` or `explorer` and inject the TOML or Markdown spec in the prompt.

## Current Codex Compatibility

For the tested local Codex CLI generation, use these flags in `~/.codex/config.toml`:

```toml
[features]
collab = true
child_agents_md = true

[agents]
max_threads = 6
max_depth = 1
```

Do not assume `features.multi_agent` is accepted by every installed Codex CLI. Check with `codex features list`; if the CLI reports `Unknown feature flag: multi_agent`, use the flags above.

## Agent TOML Schema

Every custom agent TOML must include:

```toml
name = "example_agent"
description = "When to use this agent."
developer_instructions = """
Core behavior and boundaries.
"""
```

Common optional fields:

```toml
model = "gpt-5.4"
model_reasoning_effort = "high"
sandbox_mode = "read-only"
nickname_candidates = ["Scout", "Reviewer"]
```

Use `sandbox_mode = "read-only"` only when the agent should never write files. Do not set read-only for agents expected to create handoff artifacts.

Read `references/native_agent_toml.md` when you need the full schema checklist, examples, or migration notes.

## Script Usage

Create a new agent from direct instructions:

```powershell
python C:\Users\zzt\.codex\skills\agent-creator\scripts\create_agent.py create `
  --name ppt_storyboard `
  --description "Creates slide-by-slide PPT storyboards from a fact ledger and production brief." `
  --instructions-file agent\agents_storyboard_agent_spec.md `
  --output-dir .codex\agents `
  --reasoning-effort high `
  --nickname "Storyboarder"
```

Validate one file or a directory:

```powershell
python C:\Users\zzt\.codex\skills\agent-creator\scripts\create_agent.py validate .codex\agents
```

The script normalizes filenames to kebab-case, validates required fields, and checks that generated TOML can be parsed.

## Writing Rules

- Keep each agent narrow and opinionated.
- Put routing hints in `description`, not only in `developer_instructions`.
- In `developer_instructions`, include allowed write scope and non-goals.
- Include final evidence the agent must return.
- If converting a long Markdown spec, compress it into durable instructions rather than pasting irrelevant project history.
- If preserving a Markdown spec as extended guidance, tell the native agent which spec path to read.
- Avoid project-specific facts in global agents; put those in project `.codex/agents/` or runtime prompts.

## Done Criteria

A created agent is complete when:

- The TOML exists in the chosen native agent directory.
- It parses successfully.
- It has `name`, `description`, and `developer_instructions`.
- The filename, `name`, and expected spawn name are documented in the final response.
- The user knows whether a Codex restart is needed before availability testing.
