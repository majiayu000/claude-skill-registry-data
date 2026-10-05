---
name: "gsd-spike"
description: "Rapidly spike an idea with throwaway experiments to validate feasibility before planning"
metadata:
  short-description: "Rapidly spike an idea with throwaway experiments to validate feasibility before planning"
---

<codex_skill_adapter>
## A. Skill Invocation
- This skill is invoked by mentioning `$gsd-spike`.
- Treat all user text after `$gsd-spike` as `{{GSD_ARGS}}`.
- If no arguments are present, treat `{{GSD_ARGS}}` as empty.

## B. AskUserQuestion → request_user_input Mapping
GSD workflows use `AskUserQuestion` (Claude Code syntax). Translate to Codex `request_user_input`:

Parameter mapping:
- `header` → `header`
- `question` → `question`
- Options formatted as `"Label" — description` → `{label: "Label", description: "description"}`
- Generate `id` from header: lowercase, replace spaces with underscores

Batched calls:
- `AskUserQuestion([q1, q2])` → single `request_user_input` with multiple entries in `questions[]`

Multi-select workaround:
- Codex has no `multiSelect`. Use sequential single-selects, or present a numbered freeform list asking the user to enter comma-separated numbers.

Execute mode fallback:
- When `request_user_input` is rejected (Execute mode), present a plain-text numbered list and pick a reasonable default.

## C. Task() → spawn_agent Mapping
GSD workflows use `Task(...)` (Claude Code syntax). Translate to Codex collaboration tools:

Direct mapping:
- `Task(subagent_type="X", prompt="Y")` → `spawn_agent(agent_type="X", message="Y")`
- `Task(model="...")` → omit (Codex uses per-role config, not inline model selection)
- `fork_context: false` by default — GSD agents load their own context via `<files_to_read>` blocks

Parallel fan-out:
- Spawn multiple agents → collect agent IDs → `wait(ids)` for all to complete

Result parsing:
- Look for structured markers in agent output: `CHECKPOINT`, `PLAN COMPLETE`, `SUMMARY`, etc.
- `close_agent(id)` after collecting results from each agent
</codex_skill_adapter>

<objective>
Rapid feasibility validation through focused, throwaway experiments. Each spike answers one
specific question with observable evidence. Spikes live in `.planning/spikes/` and integrate
with GSD commit patterns, state tracking, and handoff workflows.

Does not require `$gsd-new-project` — auto-creates `.planning/spikes/` if needed.
</objective>

<execution_context>
@/Users/sasikumar/Documents/n8n/.codex/get-shit-done/workflows/spike.md
@/Users/sasikumar/Documents/n8n/.codex/get-shit-done/references/ui-brand.md
</execution_context>

<runtime_note>
**Copilot (VS Code):** Use `vscode_askquestions` wherever this workflow calls `AskUserQuestion`.
</runtime_note>

<context>
Idea: {{GSD_ARGS}}

**Available flags:**
- `--quick` — Skip decomposition/alignment, jump straight to building. Use when you already know what to spike.
</context>

<process>
Execute the spike workflow from @/Users/sasikumar/Documents/n8n/.codex/get-shit-done/workflows/spike.md end-to-end.
Preserve all workflow gates (decomposition, risk ordering, verification, MANIFEST updates, commit patterns).
</process>
