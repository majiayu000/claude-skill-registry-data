---
name: agent-orchestration
description: "Spawn and manage hierarchical AI sub-agents (Cursor, Codex, Gemini) in isolated git worktrees with explicit role prompts, structured task briefs, and verification checklists. Supports work vs research modes, await vs fire-and-forget runtime, and role-aware wrappers for cleaner delegation. Use when: (1) Delegate tasks to AI agents, (2) Parallel work across features, (3) Research tasks needing web search, (4) Code refactoring or implementation, (5) Documentation updates, (6) Testing agent orchestration systems. Triggers: spawn agent, delegate to agent, agent orchestration, multi-agent, sub-agent, agent work, agent research."
---

# Agent Orchestration

Spawn and manage hierarchical agents with role-aware prompts, minimal context, and predictable result contracts. This skill is optimized for orchestrator → specialist → helper workflows.

## Quick Start

```bash
# One-call research (waits + collects automatically)
bash skills/agent-orchestration/scripts/agent-run.sh researcher \
  "Summarize this repo in 3 bullets. Cite only files you read."
```

```bash
# Parallel implementers (fire-and-forget, wait for all, auto-merge)
bash skills/agent-orchestration/scripts/agent-run-batch.sh implementer \
  --tasks-file ./tasks.txt \
  --merge
```

## Orchestrator Flow (Required)

Follow this sequence for non-trivial tasks:

1. Get user prompt (requirements, constraints, success criteria)
2. Search (Researcher: codebase search first, then web search if needed)
3. Plan (Orchestrator: phases + workstreams)
4. Implement (Implementer)
5. Test (Tester)
6. Document (Documenter)
7. Verify (Reviewer)

Batch responsibility: The orchestrator owns conflict resolution and ensuring the original prompt is upheld. If a specialist spawns a helper, that specialist owns the same responsibilities for their subtask.

## Role Identities (Specialists)

Use these identities verbatim so subagents stay scoped:

- **Researcher**: Use codebase search first, then Tavily if needed. Write `answer.md` and cite sources. No code changes.
- **Implementer**: Apply code changes only within scope. No tests unless requested.
- **Tester**: Run tests, fix failures, report commands + outcomes.
- **Documenter**: Update docs only. Follow existing docs style and use docs-check + docs-write guidance.
- **Reviewer**: Verify requirements, tests, docs, and report gaps.

Each role must return the `references/result-contract.md` summary.

Role templates include a short **Personality** line (automatically injected) so specialists remain consistent and predictable.

## Data & Context Flow (Internal Map)

1. **User Prompt** → Orchestrator captures requirements and constraints.
2. **Orchestrator Brief** → `references/orchestrator-brief.md` defines phases and workstreams.
3. **Role + Task** → Wrapper builds role header + task + guardrails.
4. **prompt.md (single context file)** → Written to worktree and mirrored to `.ada/data/agents/runs/<runId>/prompt.md`.
5. **Execution** → Provider runs inside worktree with access to prompt.md.
6. **Outputs** → `answer.md` (research) or code changes (work).
7. **Result Contract** → Specialist returns `references/result-contract.md` summary.
8. **Collect** → `agent-collect.sh` generates patch + artifacts.
9. **Merge (optional)** → `agent-run.sh --merge` / `agent-run-batch.sh --merge`.

## Prompt Composition (Required)

All subagent prompts must include a role header before the task. The role-aware wrappers (`agent-run.sh`, `agent-run-batch.sh`, `agent-spawn-role.sh`) build this automatically.

**Prompt structure used by wrappers:**

```
# Subagent Role

- Role: <Role Name>
- Workstream ID: <R1|I1|T1|D1|V1|H1>
- Parent Run ID: <parent|none>
- Mode: <research|work>
- Runtime: <await|ff>

## Role Instructions

<role-specific instructions>

## Role Boundaries (Other roles handle)

<concise list of responsibilities owned by other roles>

## Task Brief

<task or task brief contents>

## Orchestrator Brief (optional)

<orchestrator brief>

## Context Pack (optional)

<context snippets>

## Output Contract

<result contract>

## Guardrails

- Stay within scope. Do not change unrelated files or tasks.
- No lateral communication between specialists. Report only to the parent.
- Level 2 may spawn multiple helpers (Level 3) for tightly scoped subtasks. Helpers must not spawn further agents.
- Research mode must write answer.md.
```

Wrappers also persist the full role + task context to `prompt.md` in both the worktree and the run directory so agents can re-read it.

If you bypass wrappers and call `agent-spawn.sh` directly, you must prefix the prompt with the role header and contract yourself. No additional context file is created automatically.

## Context Passing

Downward (orchestrator → specialist):
- `references/orchestrator-brief.md`
- `references/subagent-task-brief.md`
- Minimal context pack via `--context-file`

Upward (specialist → orchestrator):
- `references/result-contract.md`

## Execution Modes Matrix

| Mode | Runtime | Use Case | Output |
|------|---------|----------|--------|
| Research | Await | Research questions, analysis, web search | `answer.md` + patch |
| Work | Await | Code implementation, refactoring | Patch (manual review/merge) |
| Work | Fire-and-forget | Parallel work, low-risk tasks | Patch (use auto-merge wrappers) |

## Core Commands (Recommended)

### agent-run.sh (one-call)

```bash
bash skills/agent-orchestration/scripts/agent-run.sh <role> "<task>" [options]
```

- Waits and collects automatically
- `--merge` auto-merges work-mode changes
- `--quick-merge` is an alias for `--merge` in this wrapper

### agent-run-batch.sh (parallel)

```bash
bash skills/agent-orchestration/scripts/agent-run-batch.sh <role> --tasks-file <path> [options]
```

- Spawns many tasks in parallel (`runtime=ff` by default)
- Waits for all, collects results, then merges if `--merge` (or `--quick-merge` alias) is set

### agent-spawn-role.sh (role-aware wrapper)

```bash
bash skills/agent-orchestration/scripts/agent-spawn-role.sh \
  --role <researcher|implementer|tester|documenter|reviewer|helper> \
  --workstream <id> \
  --task "<task>" \
  [--mode <work|research>] \
  [--runtime <await|ff>]
```

## Auto-Merge Guidance

- For single tasks: use `agent-run.sh --merge`
- For parallel tasks: use `agent-run-batch.sh --merge`
- Raw `agent-spawn.sh --quick-merge` only affects cleanup; it does not merge on its own
- Use `--auto-resolve` only if you're comfortable preferring agent changes (`-X theirs`) on conflicts

## Rescue & Follow-up

If `agent-collect.sh` cannot detect results after rescue attempts, it marks the run as failed and emits:
- `rescue.md` with diagnostics and next steps
- `rescue.sh` to re-run the same prompt with identical provider/mode

Rescue backoff can be tuned via `RESCUE_MAX_DELAY` and `RESCUE_JITTER_PCT`.

## Hierarchy Rules

- **Level 1 (Orchestrator):** Owns plan, task allocation, verification, merge decisions
- **Level 2 (Specialists):** Execute assigned scope; may spawn multiple Level 3 helpers
- **Level 3 (Helpers):** Tightly scoped tasks only; no further spawning
- **No lateral communication** between specialists

## Templates

- `references/orchestrator-brief.md`
- `references/subagent-task-brief.md`
- `references/result-contract.md`
- `references/verification-checklist.md`

## References

- `references/commands.md` - Full command surface
- `references/workflows.md` - Detailed flow + role workflow
- `references/examples.md` - Usage examples
- `references/operations.md` - Architecture notes + troubleshooting
- `references/role-templates.md` - Role prompts
