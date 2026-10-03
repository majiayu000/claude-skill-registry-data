---
name: codex-subagent-designer
description: Route Codex delegation design, subagent prompting, reusable catalog-asset design, and custom-agent template review.
---

# Codex Subagent Designer

Choose one primary mode and read only its workflow. Add another mode only when the request explicitly requires both deliverables.

| Mode | Use when | Workflow |
| --- | --- | --- |
| `delegation-design` | Decide whether, how, and where to delegate bounded work and integrate results. | [Delegation design](references/workflows/delegation-design.md) |
| `subagent-prompting` | Draft an explorer, worker, validator, reviewer, or forward-test prompt. | [Subagent prompting](references/workflows/subagent-prompting.md) |
| `catalog-asset-design` | Create, improve, or score reusable skills and agent templates. | [Catalog asset design](references/workflows/catalog-asset-design.md) |
| `agent-template-review` | Review Codex TOML, runtime posture, skill resolution, handoffs, or crew coverage. | [Agent-template review](references/workflows/agent-template-review.md) |

Do not load sibling workflows or shared catalog references prospectively. Obey the active session's delegation and mutation constraints; a design does not itself authorize spawning agents, editing files, or external actions.
