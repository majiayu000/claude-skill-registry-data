---
name: swarm-handoff
description: End-of-session orchestration handoff. Wraps current conversation into a structured prompt that spawns a fresh orchestrator session coordinating parallel build agents across all tiers.
---

# SWARM HANDOFF (Session-Terminal Relay Skill)

**When to use:** End of a research/planning/discussion session when the next step is "go build all of this." Produces a ready-to-paste prompt for a fresh context window that orchestrates parallel agents.

## Phase 1: Read the Unified Build Queue

**Start from `docs/UNIFIED-BUILD-QUEUE.md`** (the shared queue contract). This is the canonical source, not individual spec files.

1. **Read the queue** - identify items relevant to current session decisions
2. **Decisions made** - what was decided, what was rejected, why
3. **Tasks to dispatch** - pull from SPEC-READY and PARTIAL items in the queue
4. **Dependencies** - use the "Depends On" column (within-category) and cross-category notes
5. **Context artifacts** - which files/docs each agent needs to read
6. **New items discovered** - add them to the queue before generating the prompt

## Phase 2: Assign Model Tiers

For each task, assign the cheapest tier that can handle it:

| Complexity                                        | Tier                     | Assignment             |
| ------------------------------------------------- | ------------------------ | ---------------------- |
| Boilerplate, formatting, bulk file ops            | Local (Ollama/Gemma)     | ollama-delegate        |
| Single-file features, tests, mechanical edits     | Worker (Haiku)           | model: "haiku"         |
| Multi-file features, integrations, judgment calls | Executor (Opus)          | model: "opus"          |
| Architecture decisions, hard debugging            | Advisor (Opus, explicit) | main orchestrator only |

## Phase 3: Structure the Waves

Group tasks into waves. Within a wave, tasks are independent (parallelizable). Between waves, there are dependencies.

```
Wave 1: [tasks with no dependencies - launch all in parallel]
Wave 2: [tasks that depend on Wave 1 outputs]
Wave 3: [tasks that depend on Wave 2 outputs]
```

## Phase 4: Generate the Orchestration Prompt

Output a prompt block (fenced, ready to paste) with this structure:

```markdown
# ORCHESTRATION MISSION

## Context Load (Read These First)

- [list of files the orchestrator must read before dispatching]

## Session Decisions (Do Not Re-Debate)

- [bullet list of decisions from this session - these are settled]

## Wave 1 (Parallel - Launch Immediately)

### Agent 1: [task name]

- **Model:** haiku | opus | ollama
- **Task:** [concrete description - what to build, where, acceptance criteria]
- **Read first:** [specific files this agent needs]
- **Done when:** [verification criteria]

### Agent 2: [task name]

...

## Wave 2 (After Wave 1 Verified)

### Agent 3: [task name]

...

## Verification Protocol

- Each agent runs Builder Gate (`.claude/skills/builder/SKILL.md`)
- Orchestrator does NOT build. Orchestrator dispatches, monitors, verifies.
- After each wave: `npx tsc --noEmit --skipLibCheck` must pass
- After final wave: full Playwright verification of affected flows
- Anti-Loop: 3 strikes on same error = stop, report, let developer decide

## Orchestrator Rules

1. You are the COORDINATOR. You do not write implementation code.
2. Dispatch agents via the Agent tool with appropriate model tier.
3. After dispatching a wave, wait for all agents to complete.
4. Verify each agent's output (type check, screenshot, behavioral test).
5. Only proceed to next wave after current wave is fully verified.
6. If an agent fails: diagnose, give it one retry with better context, then flag.
7. At completion: commit all work, update specs to `verified`, push.
```

## Phase 5: Wrap Current Session

After generating the prompt:

1. Commit any uncommitted work from this session
2. Update `docs/session-log.md` with handoff note
3. Tell the developer: "Paste this into a fresh session to launch the swarm"

## Anti-Patterns (What This Skill Prevents)

- "Build everything" with no task list (agents hallucinate scope)
- Giving every agent the full codebase context (noise kills quality)
- No verification between waves (errors compound)
- Orchestrator also building (loses coordination awareness)
- All tasks at same model tier (wastes money or quality)
- No dependency ordering (agents step on each other)

## Usage

Invoke with `/swarm-handoff` at end of planning/research session. Can also invoke mid-session if you realize you have enough to dispatch.

The generated prompt is self-contained. The fresh session needs ONLY that prompt plus CLAUDE.md (which it loads automatically).
