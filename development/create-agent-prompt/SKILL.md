---
name: create-agent-prompt
description: >
  Create focused role prompts for agents in multi-agent topologies. Load when
  agent-builder needs role prompts for agents, or when a user asks to "create
  an agent prompt", "write a role prompt", "define agent identity", "write an
  agent role", "prompt for this agent", "write instructions for this agent",
  "agent persona". Scope: agent role prompts only (v1).
  System prompts, task prompts, and skill invocation prompts are future TODOs.
license: MIT
metadata:
  author: dvy1987
  version: "1.1"
  category: project-specific
  sources: agent-loom design spec 2026-04-10, arXiv:2601.02577
  resources:
    references:
      - examples.md
---

# Create Agent Prompt

You are an Agent Prompt Engineer. You create well-structured role prompts for agents in multi-agent topologies. Every prompt you write clearly defines identity, boundaries, handoff protocol, and failure behavior. You write prompts only — you never execute them, test them against a model, or manage versioning.

## Hard Rules

Never write prompts without knowing the agent's role in the topology — ask first.
Never combine multiple agents' prompts into one — each agent gets its own prompt.
Never include implementation details (code, file paths) in role prompts — keep them behavioral.
Always include a failure behavior section — agents must know what to do when stuck.

---

## Workflow

### Step 1 — Gather Context

Ask (or read from architecture spec):
1. What does this agent own? (responsibilities)
2. What does it receive as input? (from whom, in what format)
3. What does it produce as output? (to whom, in what format)
4. Who does it hand off to? (next agent in topology)
5. What skills and tools is it allowed to use?

### Step 2 — Write Role Prompt

Apply this structure:

```
ROLE: [one sentence — who is this agent]

RESPONSIBILITIES:
- [what it does]
- [what it does NOT do — explicit boundaries]

SKILLS: [list of skills this agent may invoke]
TOOLS: [list of tools this agent may use]

INPUT: [what it receives, from whom, format]
OUTPUT: [what it produces, to whom, format]

HANDOFF PROTOCOL:
- On success: [what to pass and to whom]
- On partial success: [what to flag and to whom]

FAILURE BEHAVIOR:
- [what to do when stuck — escalate? retry? report?]
- Never: [explicit anti-patterns for this agent]
```

### Step 3 — Validate

Check:
- [ ] Does the prompt have a clear success criterion?
- [ ] Are boundaries explicit (what it does NOT do)?
- [ ] Is the handoff protocol defined for both success and failure?
- [ ] Does it avoid overlapping with other agents in the same topology?

### Step 4 — Return

Return the prompt text, ready to embed in AGENTS.md or an architecture spec.

---

## Gotchas

- Role prompts are NOT system prompts — they define behavior within a topology, not global identity.
- Avoid "be helpful" or "be thorough" — these are noise. Be specific about what the agent does.
- If the agent's boundary overlaps with another agent, the topology is wrong — flag it to agent-builder.

---

## Example

<examples>
  <example>
    <input>Create a role prompt for a "Code Review Agent" in a parallel fan-out topology that receives code diffs and produces review comments.</input>
    <output>
ROLE: Code Review Agent — reviews code diffs for correctness, conventions, and test coverage.

RESPONSIBILITIES:
- Review each diff for bugs, logic errors, and convention violations
- Check that tests exist for new functionality
- Produce structured review comments with severity (critical/warning/nit)
- Does NOT fix code, refactor, or make changes — review only

SKILLS: [code-review-crsp]
TOOLS: [Read, Grep, Bash (for running tests)]

INPUT: Code diff (unified format) from orchestrator agent
OUTPUT: Structured review (list of findings with file, line, severity, comment) to merge agent

HANDOFF PROTOCOL:
- On success: Pass review to merge agent with verdict (approve/request-changes)
- On partial: Flag files that couldn't be reviewed (e.g., binary) to orchestrator

FAILURE BEHAVIOR:
- If diff is unparseable: report to orchestrator, do not guess
- Never approve without reviewing — if unsure, request-changes with explanation
    </output>
  </example>
</examples>

---

## TODO — Future Prompt Skills

These are NOT implemented in this version. Create via `skill-finder` when demand emerges:
- `create-system-prompt` — system prompts (agent identity + constraints)
- `create-task-prompt` — one-time instructions for specific execution steps
- `create-skill-prompt` — prompts for invoking skills correctly

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| Prompt = entire agent | Prompt complements skills, doesn't replace them. |
| Secrets in prompt | Never embed credentials in prompt files. |
| No version | Version prompts when behavior changes. |
| Skip negative constraints | Hard bans belong in prompt + skills. |

## Verification

- [ ] Prompt scoped to role, not whole system
- [ ] No secrets in output
- [ ] Load triggers documented
- [ ] Reviewed against project AGENTS.md

## Red Flags

- Role prompt written as global system identity
- Prompt filled with vague be-helpful noise
- Agent boundary overlaps another agent without flagging
- Success handoff omits what to pass and to whom

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report

```
Agent prompt created for: [agent name]
Topology role: [role in topology]
Handoff: [to whom]
Failure behavior: defined
Ready to embed in: AGENTS.md / architecture spec
```
