---
name: delegate
description: Prepare a task for delegation to another agent (Codex, Gemini, human) with full context and guardrails.
version: 0.1.0
execution-mode: side_effecting
argument-hint: "\"TASK\" to \"AGENT\" (e.g., \"security audit\" to \"codex\")"
category: fleet-ops
status: candidate
---
# Delegate

Prepare a task package for delegation to another agent or human, with context, constraints, and verification criteria.

## Why Not Just [dispatch]?
`[dispatch]` spawns sub-agents within the same session.
`[delegate]` prepares work for EXTERNAL agents (Codex, Gemini, the team lead, a contractor) who work asynchronously via the bus.

## Execution

### 0. Emit SKILL_INVOKE
Post SKILL_INVOKE to the bus before any stateful action.
```
Type: SKILL_INVOKE
To: all
Message: [skill=delegate] [mode=side_effecting] [args_hash=<sha256>] [session=<session_id>]
```
(The skill invocation runtime injects the caller's canonical identity as `from_id`.)

### 1. Define the task
```
TASK: <clear, specific deliverable>
ASSIGNED TO: <agent identity>
DEADLINE: <when>
PRIORITY: <P0/P1/P2>
```

### 2. Provide context
What does the delegate need to know?
- Relevant files and their purpose
- Current state of the work
- Decisions already made (link to CLP entries)
- Constraints (stdlib-only, no --no-verify, etc.)

### 3. Set guardrails
Based on the delegate's trust level:
- **Scope**: Which files/directories can they modify?
- **Commit limits**: Max LOC / files per commit
- **Prohibited actions**: What they must NOT do
- **Review requirement**: Does their work need Claude review before merge?

### 4. Define done
- [ ] Specific deliverable (code, doc, analysis)
- [ ] Tests passing
- [ ] PR created (or bus RECEIPT posted)
- [ ] No guardrail violations

### 5. Post to bus
Post TASK_REQUEST to the bus for the target agent.
```
Type: TASK_REQUEST
To: <agent>
Message: TASK: <description>. SCOPE: <files>. DEADLINE: <when>. VERIFY: <criteria>.
```
(The skill invocation runtime injects the caller's canonical identity as `from_id`.)

### 6. Monitor
Use `[agent-audit] <agent>` to check progress, or watch the bus:
```bash
grep "<agent>" _state/coordination/messages.tsv | tail -10
```

## Output Format
```
Delegation Package | <task> -> <agent>
══════════════════════════════════════

## Task
<clear deliverable>

## Context
<what they need to know>

## Guardrails
- Scope: <approved directories>
- Limits: <LOC/file caps>
- Prohibited: <what not to do>
- Review: <required/optional>

## Done Criteria
- [ ] <deliverable>
- [ ] <tests>
- [ ] <bus receipt>

## Bus Message Posted
<timestamp and content>
```

## Base120 Context
- Primary: **SY11** (Governance Patterns)
- Related: **CO17** (Orchestration vs Choreography), **SY13** (Incentive Architecture)

## Skill Chains
- For delegation tasks needing LLM inference -> `[reasoning-router]` (`python ~/bin/reasoning_router.py route`)

### Mandatory

None — generates a delegation packet; the delegated task itself has its own chains enforced at execution time.

### Advisory

- `[agent-audit]` — monitor delegated task progress after packet is posted
- `[dispatch]` — for same-session sub-agent spawning (contrast with external delegation)
- `[cross-runtime-bridge]` — for executing Devin→opencode delegation via `python ~/bin/cross_runtime_bridge.py delegate "<message>"`

## Authority

- **T1 (TRUSTED)**: May run (prepare delegation packets for any agent/human)
- **T2 (Active/High)**: May run (prepare delegation packets for any agent/human)
- **T3 (Medium)**: May run (prepare delegation packets for any agent/human)
- **T4 (Probationary)**: May run (generates packet only, does not execute the delegated task)
- **Operator**: Override any restriction
