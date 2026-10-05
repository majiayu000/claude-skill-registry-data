---
name: github-copilot-customization-architecture
description: >-
  Use for designing, auditing, or refactoring a GitHub Copilot customization system in Visual Studio Code across instructions, prompt files, Agent Skills, custom agents, hooks, MCP servers, and plugins. Do not use merely to author one already-selected artifact or configure unrelated VS Code settings.
argument-hint: "[customization goal, repository, constraints, and current artifacts]"
---

# GitHub Copilot customization architecture

Choose the smallest customization that supplies the missing behavior. Inspect
the current workspace and active VS Code/Copilot version before writing files.

## Selection model

| Need | Choose | Activation |
|---|---|---|
| Broad convention | Instructions | Automatic |
| File/task-specific convention | `.instructions.md` | Conditional |
| Focused reusable task | Prompt file | Manual slash command |
| Multi-step capability/resources | Agent Skill | Relevant task or slash command |
| Specialist persona/tool boundary | Custom agent | Selected/invoked role |
| Guaranteed lifecycle action | Hook | Deterministic event; preview |
| External live tools/data | MCP | Tool call after trust |
| Installable bundle | Plugin | Install/enable; preview |

Subagents are runtime delegation, not another file to create.

## Workflow

1. Inventory current instructions, prompts, skills, agents, hooks, MCP configs,
   plugins, VS Code settings, and parent-repository discovery.
2. State the repeated job, activation mode, workspace/user scope, required
   capabilities, deterministic enforcement, and trust boundary.
3. Route each requirement using the table. Split requirements whose activation,
   authority, or verification differs.
4. Build a collision map. Remove duplicate or contradictory rules; never rely
   on instruction ordering.
5. Assign least-privilege tools and explicit trust steps. Do not silently enable
   executable hooks, servers, or plugins.
6. Author through the matching specialized skill, then parse and test every
   artifact before a VS Code smoke test.

## Decision rules

- If guidance belongs in nearly every request, use repository instructions.
- If a person deliberately starts one task, use a prompt file; if Copilot must
  discover a multi-step capability with resources, use a skill.
- If behavior must happen even when the model forgets, use a hook, not prose.
- If a role only needs read access, exclude edit and terminal tools.
- If a capability needs live external state, use a trusted tool/MCP server; do
  not paste credentials or pretend durable instructions are current data.
- If several artifacts ship together, use a plugin only when installation and
  trust are worth the packaging cost.
- Default to workspace scope. User scope requires an explicit cross-project job.

Read [the format and scope map](references/artifact-contracts.md) before choosing
locations. Use [architecture recipes](references/recipes-solutions.md) for a
multi-artifact design and [verification](references/verification.md) before
declaring completion.

## Completion

Deliver an artifact map with one owner per rule, explicit activation and trust
boundaries, no unresolved collisions, parsed files, offline executable checks,
and a recorded VS Code discovery plan. Mark hooks and plugins as preview and
host/model/tool identifiers as locally verified or unverified.
