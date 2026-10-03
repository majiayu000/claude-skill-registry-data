---
name: orchestrating-subagents
description: "Design subagent orchestration plans for multi-step work. Use when a task needs decomposition across multiple specialized agents, model selection, tool assignment, skill selection, handoff contracts, sequencing, or parallelization. Default orchestrator: Opus. Default subagents: openai-codex/gpt-5.4 for coding and research, gemini-3-pro-image-preview for image creation."
---

# Orchestrating Subagents

Design the orchestration plan for subagent work.

## Agent roles

### Orchestrator
- Agent/model: Opus
- Role: planner, coordinator, reviewer, and synthesis owner
- Responsibility: decompose the task, assign subagents, define handoffs, detect gaps, and consolidate outputs

### Default subagents
- `openai-codex/gpt-5.4`
  - Use for coding tasks
  - Use for technical research tasks
  - Use for repo analysis, debugging plans, implementation planning, and validation design
- `gemini-3-pro-image-preview`
  - Use for image creation tasks
  - Use for visual concept generation, mockups, ad/image directions, and image-edit planning

## Orchestration procedure

1. Restate the target outcome in one sentence.
2. Split the work into bounded subtasks with explicit deliverables.
3. Mark each subtask as one of: coding, research, image creation, review, or coordination.
4. Assign the best-fit agent/model.
5. Assign only the tools and skills needed for that subtask.
6. Define the artifact each subagent must return.
7. Define dependency order and what can run in parallel.
8. Define review gates for the orchestrator.

## Tool assignment guidance

### For coding tasks with `openai-codex/gpt-5.4`
Prefer tools such as:
- `read`, `write`, `edit`, `apply_patch`
- `exec` and `process` when execution is allowed by the parent task
- `browser` for web UI inspection when needed
- `web_fetch` only for documentation or primary-source lookup
- `diffs` for real diffs

Prefer skills such as:
- the most task-specific repo/domain skill available
- `coding-agent` when delegation to a coding harness is part of the plan
- `frontend-design` or other domain skills when relevant

### For research tasks with `openai-codex/gpt-5.4`
Prefer tools such as:
- `web_fetch`
- `browser`
- `read`
- `memory_search` and `memory_get` when prior decisions matter

Prefer skills such as:
- the most specific analysis or domain skill available
- `clawhub` only as a recommendation path when identifying missing skills

### For image creation tasks with `gemini-3-pro-image-preview`
Prefer tools such as:
- `image_generate`
- `image`
- `read` for brand/context docs

Prefer skills such as:
- `ad-designer`
- `frontend-design`
- other image/design skills matching the request

## Missing capability rule

When a required tool or skill is missing:
1. name the missing capability clearly
2. check for a close existing substitute
3. if no substitute fits, recommend fetching a skill from ClawHub
4. if no suitable skill is likely available, recommend creating a new skill
5. note the effect on sequencing and risk

## Output format

Return these sections in this order:
1. Outcome
2. Orchestrator
3. Subtasks
4. Subagent assignments
5. Tools per subagent
6. Skills per subagent
7. Handoffs and artifacts
8. Parallelization
9. Gaps
10. Review gates

Keep assignments concrete. Avoid vague labels like "general agent" or "use standard tools".
