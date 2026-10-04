---
name: superpowers-dispatching-parallel-agents
description: 'Use when multiple independent problems exist and sequential investigation
  would waste time — dispatch one specialized agent per problem domain concurrently.
  Purpose: Speed up diagnosis and fixing by running independent investigations in
  parallel, so N problems are solved in the time of 1. Key capabilities: Independent
  domain isolation — each agent operates on a single subsystem with no shared state;
  focused agent briefs with specific scope, clear goal, hard constraints (what not
  to touch), and expected output format; parallel dispatch of 3+ agents at once; integration
  step that checks for fix conflicts and runs the full test suite before reporting
  done. When to trigger: 3+ test files failing with different root causes; multiple
  unrelated subsystems broken at once; independent research tasks that could run in
  parallel (e.g., evaluating 3 different libraries); parallel exploration of a large
  codebase during onboarding; simultaneous bug investigation across different layers
  (frontend, API, database); concurrent spike tasks for a multi-component feature.
  Also for: parallel code review across multiple modules; simultaneous dependency
  updates in a monorepo; concurrent documentation writing for multiple components.'
---

# Dispatching Parallel Agents

**Core principle:** Dispatch one agent per independent problem domain. Let them work concurrently.

## When to Use

**Use when:**
- 3+ test files failing with different root causes
- Multiple subsystems broken independently
- Each problem can be understood without context from others
- No shared state between investigations

**Don't use when:**
- Failures are related (fix one might fix others)
- Need to understand full system state
- Agents would interfere with each other

## The Pattern

### 1. Identify Independent Domains
Group failures by what's broken. Each domain is independent.

### 2. Create Focused Agent Tasks
Each agent gets:
- **Specific scope:** One test file or subsystem
- **Clear goal:** Make these tests pass
- **Constraints:** Don't change other code
- **Expected output:** Summary of what you found and fixed

### 3. Dispatch in Parallel
Run multiple agents concurrently on separate problem domains.

### 4. Review and Integrate
When agents return:
- Read each summary
- Verify fixes don't conflict
- Run full test suite
- Integrate all changes

## Agent Type Selection (MANDATORY)

When spawning subagents, follow this hierarchy — **general-purpose is last resort**:

**Step 1 — Check Agency catalog for a named specialist first:**
- Research/analysis → `Explore`, `Trend Researcher`
- Frontend/UI → `Frontend Developer`, `UI Designer`
- Backend/API → `Backend Architect`, `Data Engineer`
- Full-stack feature → `Senior Developer`, domain-specific PD
- QA/testing → `Testing Lead`, `Evidence Collector`
- Security → `Security Engineer`
- DevOps/infra → `DevOps Automator`
- Legal/compliance → `Legal Compliance Checker`

**Step 2 — Named skills.** Check `~/.claude/skills/INDEX.md` for a skill that covers this domain.

**Step 3 — Fallback: general-purpose.** Only use `general-purpose` when no catalog agent or skill fits.

## Agent Prompt Structure

Good agent prompts are:
1. **Focused** — One clear problem domain
2. **Self-contained** — All context needed to understand the problem
3. **Specific about output** — What should the agent return?

Example:
> "Fix the 3 failing tests in src/agents/agent-tool-abort.test.ts: [specific test names and issues]. These are timing/race condition issues. Do NOT just increase timeouts — find the real issue. Return: Summary of what you found and what you fixed."

## Common Mistakes

- **Too broad:** "Fix all the tests" — agent gets lost
- **No context:** "Fix the race condition" — agent doesn't know where
- **No constraints:** Agent might refactor everything
- **Vague output:** "Fix it" — you don't know what changed

## Key Benefits

1. **Parallelization** — Multiple investigations happen simultaneously
2. **Focus** — Each agent has narrow scope, less context to track
3. **Independence** — Agents don't interfere with each other
4. **Speed** — 3 problems solved in time of 1
