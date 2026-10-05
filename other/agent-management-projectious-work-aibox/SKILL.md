---
name: agent-management
description: >
  Orchestrate multi-agent workflows with task decomposition, role
  assignment, handoff protocols, and per-session context budgeting.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-agent-management
    version: "1.1.0"
    created: 2026-04-06T00:00:00Z
    category: processkit
    layer: 4
---

# Agent Management

## Intro

Multi-agent workflows are decomposed tasks with explicit roles,
structured handoffs, and quality gates between stages. The agent
also has to manage its own session — loading context lazily
against a declared budget rather than slurping everything at start.

## Overview

### Task decomposition

Break work into agent-sized units. Each subtask must have:

1. **Clear scope** — one well-defined outcome, not "do everything"
2. **Input specification** — exactly what files, context, or
   prior outputs the agent needs
3. **Output specification** — what artifact the agent produces
   (file, diff, structured answer)
4. **Success criteria** — how to verify the subtask is correct
5. **Estimated complexity** — small (single file), medium
   (module), large (cross-cutting)

Rules of thumb:

- If a subtask requires more than 3 files of context, split it.
- If a subtask has no verifiable output, redefine it.
- Prefer depth-first (finish one subtask fully) over breadth-first
  (start many in parallel).
- Treat MCP-backed subagents as read-only unless the current harness has
  proven stable MCP server startup and shutdown. If MCP servers crash,
  hang, or fail to exit in subagent sessions, keep all MCP and filesystem
  mutations in the primary session.

### Agent role definitions

Assign roles based on the task, not on agent identity:

| Role | Responsibility | Input | Output |
|---|---|---|---|
| **Planner** | Decomposes the task, defines order and dependencies | User request, codebase overview | Task plan with ordered subtasks |
| **Researcher** | Gathers information, reads code, finds patterns | Specific questions, file paths | Structured findings with citations |
| **Coder** | Implements changes, writes code | Task spec, relevant files, findings | Code changes (diff or files) |
| **Reviewer** | Validates correctness, style, completeness | Code changes, task spec, success criteria | Approval or rejection with reasons |

A single agent can fill multiple roles sequentially (plan, then
code, then self-review). Never skip the reviewer role — even
self-review catches errors. The planner role is mandatory for
tasks touching more than 2 files.

### Context sharing

Agents lose context between sessions. Use explicit transfer:

- **File-based (preferred for Claude Code)** — write findings to
  a scratch file (e.g. `_agent_notes.md`) that the next agent
  reads. Use structured formats: headings, bullets, file paths
  with line numbers. Delete scratch files when the workflow ends.
- **Structured handoff messages** — summarize what was done,
  what remains, and what blockers exist. Include exact paths and
  line numbers. List assumptions and decisions.
- **Shared memory (project files)** — use `DECISIONS.md` or
  `HANDOVER.md` for persistent cross-session context. Keep
  entries timestamped and concise. Reference specific commits.

### Handoff protocol

Every handoff between roles must include:

1. **Status** — what is complete and what is not
2. **Artifacts** — list of files created or modified, with paths
3. **Verification** — what was checked and how (tests run, lint,
   manual review)
4. **Blockers** — anything preventing the next step
5. **Next action** — explicit instruction for the receiving agent

Format:

```
## Handoff: [Role] -> [Role]
**Status:** [complete | partial | blocked]
**Changes:** [list of file paths]
**Verified:** [tests passed | linted | reviewed]
**Blockers:** [none | description]
**Next:** [specific instruction]
```

### Quality gates

Insert verification checkpoints between stages:

- **After planning** — does the plan cover all requirements? Are
  subtasks independent?
- **After research** — are findings specific (paths, line numbers)
  not vague?
- **After coding** — do tests pass? Linter clean? Does the change
  match the spec?
- **After review** — are all must-fix items addressed? Reviewer
  satisfied?

A quality gate fails the workflow forward — do not proceed until
the gate passes. If a gate fails twice on the same issue,
escalate to the user.

### Error recovery and fallbacks

When an agent step fails:

1. **Capture the failure** — save error output, not just "it
   failed"
2. **Diagnose** — context issue (missing info), capability issue
   (wrong approach), or environment issue (tool error)?
3. **Retry with adjustment** — provide missing context, try a
   different approach, or fix the environment
4. **Escalate** — if two retries fail, stop and report to the
   user with full context

Fallbacks:

- Coder stuck → switch to researcher role to gather more context
- Review finds fundamental issues → return to planner to re-scope
- Context too large → split the task into smaller independent
  pieces
- MCP server lifecycle unstable in subagents → stop delegating MCP work,
  close or ignore the affected subagent, and continue implementation in
  the primary session. Do not broaden permissions as a workaround.

### Progress tracking

For multi-step workflows, maintain a checklist that doubles as
handoff context:

```
## Agent Workflow: [Task Name]
- [x] Plan: decomposed into N subtasks
- [x] Research: gathered context for subtask 1
- [ ] Code: implement subtask 1
- [ ] Review: verify subtask 1
- [ ] Code: implement subtask 2
...
```

Update the checklist after each step.

### Encode corrections immediately

When the user corrects agent behavior mid-session, encode the
correction before continuing:

1. **Classify** — what kind of failure was it? (deferred action,
   wrong tool, skipped step, scope creep, …)
2. **Check** — does a skill or AGENTS.md already cover this failure
   mode? Search the relevant skill's Gotchas and Anti-patterns.
3. **Encode** — if not covered: edit the relevant file in the same
   turn. A correction that is only remembered is lost at session end.
4. **Log** — add a one-liner to `behavioral_retrospective` in the
   session handover so the session record reflects what was learned.

The same rule applies as for entity creation: do it in the same turn,
not later.

### Context budget and lazy loading

processkit projects can grow to dozens of skills, hundreds of
workitems, and many years of decision history. Loading all of
this every session is wasteful — most files have no relevance
to the current request. The agent must load context
**selectively**.

#### Read INDEX files first, not full directories

Every directory under `context/` should have an `INDEX.md`
(Level 0 per the three-level principle). At session start, the
agent reads:

1. `AGENTS.md` (root) — the canonical agent entry point
2. `context/HANDOVER.md` — current state and recent changes
3. `context/owner/identity.md` and `context/owner/working-style.md`
   (the highest-leverage owner files, if the project uses
   owner-profiling)
4. `context/INDEX.md` and any `context/*/INDEX.md` files
5. `context/migrations/INDEX.md` (always loaded — the migration
   state summary)

Provider-specific harness files (e.g. `CLAUDE.md`, `CODEX.md`)
are thin pointers to `AGENTS.md` and do not need to be in the
always-load set.

These files are short, dense, and tell the agent what exists.
The agent does NOT slurp `context/skills/`, `context/workitems/`,
etc. on session start.

#### Use the index MCP server, not filesystem walks

The `index-management` MCP server is the right way to discover
entities. Instead of `ls context/skills/`, the agent calls
`query_entities(kind="Skill", category="process")` and gets back
a list of just the skills that match. Same for workitems,
decisions, bindings, events. Filesystem walking is the slow,
context-expensive fallback.

#### Load skills on demand, not upfront

When the agent needs a specific skill (e.g. `code-review`), it
reads `context/skills/code-review/SKILL.md` at that moment — not
at session start. If the SKILL.md references a deeper file
(`references/...`), only read that when the agent's task actually
needs it. This is the three-level principle in action: start at
Level 1, drop to Level 2 when the request is more specific, drop
to Level 3 only for edge cases.

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Context overload — passing the entire codebase or conversation to every agent.** Each agent should receive only the files and context it needs for its specific subtask. Passing everything to every agent balloons token usage, produces vague responses, and hits context limits. Reference specific file paths and line ranges in handoffs rather than dumping full file contents.
- **Circular delegation with no forward progress.** Agent A asks Agent B for help, which asks Agent A. The hallmark is growing context with repeated handoffs and no new artifacts. Enforce a strict pipeline direction: every handoff moves the task forward. If an agent cannot proceed, escalate to the user with full context — not back to the previous agent.
- **Premature fan-out before confirming task independence.** Starting parallel agents before the planner has verified that subtasks touch different files and modules leads to merge conflicts and duplicated work. Always run a planning stage first and confirm independence; limit fan-out to 3-4 parallel subtasks.
- **Skipping the reviewer role because the coder "did a good job."** Self-confidence bias is highest immediately after writing code. The reviewer role exists precisely because authors miss their own errors. Even a self-review pass — running tests, linting, reading the diff against the spec — catches errors that accumulate into bugs when skipped.
- **Vague handoffs without specific artifacts, paths, or line numbers.** "I made some changes, please review" tells the receiving agent almost nothing. Use the structured handoff format every time: status, list of file paths changed, what was verified, any blockers, and the exact next action. Include absolute paths and line numbers for all referenced code.
- **Loading all context at session start instead of selectively.** A project with 100 skills, 5 years of decisions, and hundreds of backlog items contains far more context than any session needs. Read INDEX files to understand what exists, then load on demand when the specific task requires it. The three-level principle applies: start at the overview, drill down only when needed.
- **Leaving scratch files (`_agent_notes.md`, `_blackboard.md`) in the repository.** Temporary agent collaboration files are not part of the project's permanent record. Every multi-agent workflow that creates scratch files must clean them up when the workflow completes. Committed scratch files confuse future agents and humans about what is authoritative context.
- **Skipping the skill catalog for domain tasks.** Before starting
  any domain-specific task (writing a PRD, drafting a release,
  creating a schema), search for a matching processkit skill via
  `search_entities` or `skill-finder`. Proceeding from general
  knowledge when a skill exists produces output that misses
  processkit-specific conventions and entity storage paths.

## Full reference

### Worked examples

**"Add authentication to this API — use multiple agents to plan,
implement, and review."** (1) Researcher reads existing route
handlers and middleware patterns, writes findings to
`_auth_notes.md`. (2) Coder implements auth middleware, JWT
validation, and protected route decorators based on findings.
(3) Reviewer checks against OWASP guidelines, verifies tests
pass, confirms no hardcoded secrets. Each handoff includes the
structured handoff block.

**"Set up a code review pipeline for incoming changes."** A
three-stage pipeline: (1) Researcher reads the diff and gathers
context about affected modules. (2) Reviewer evaluates
correctness, security, performance, style using the code-review
checklist. (3) Planner summarizes findings into must-fix,
should-fix, and nit categories with line references. Quality
gate: all must-fix items require a re-review cycle before
approval.

**"Research the best caching strategy, then implement it."**
Research-then-implement workflow: (1) Researcher examines current
data access patterns, identifies hot paths, checks existing
caching, writes structured findings with measured or estimated
latencies. (2) Planner reviews findings and selects an approach,
documenting the decision. (3) Coder implements the cache layer
following the plan. (4) Reviewer verifies cache invalidation,
checks for stale data risks, confirms tests cover hit/miss
paths. Handoff between research and planning includes specific
file paths and quantified findings.

### Coordination patterns

See `references/coordination-patterns.md` for the full pattern
catalog. Summary:

- **Pipeline** — agents execute sequentially
  (Researcher → Planner → Coder → Reviewer). Default choice;
  simplest, lowest risk.
- **Fan-out / Fan-in** — planner decomposes into independent
  subtasks, multiple agents run in parallel, a coordinator merges
  results. Use only when the planner confirms subtasks are
  independent (different files, different modules). Limit to 3-4
  parallel subtasks.
- **Supervisor** — one agent monitors and directs others,
  reassigning work as findings shift the plan. Use for large
  refactors and exploratory tasks where the path is unclear
  upfront.
- **Consensus** — multiple agents independently solve the same
  problem; an evaluator selects or merges. Expensive — reserve
  for high-stakes decisions (architecture, security review).
- **Blackboard** — agents share a common workspace file, picking
  up work items and posting results. Use section-based ownership
  to prevent overwrites.

### Pattern decision matrix

| Characteristic | Pipeline | Fan-Out | Supervisor | Consensus | Blackboard |
|---|---|---|---|---|---|
| Sequential dependencies | Yes | No | Partial | No | Partial |
| Independent subtasks | No | Yes | Yes | Yes | Yes |
| Uncertain requirements | No | No | Yes | Partial | Partial |
| Multiple valid solutions | No | No | No | Yes | No |
| Shared evolving state | No | No | No | No | Yes |
| Low token budget | Yes | No | Yes | No | Yes |
| High-stakes decision | No | No | Partial | Yes | No |

Default to Pipeline. Escalate to Supervisor if scope shifts
during execution. Use Fan-Out only when subtasks are provably
independent. Reserve Consensus for decisions with significant
long-term impact.

### Anti-patterns

- **Context overload** — passing the entire codebase or
  conversation history to every agent. Symptom: vague responses,
  token limits hit. Fix: give each agent only the files it needs
  for its specific subtask; use file paths and line ranges, not
  full file contents, in handoffs.
- **Circular delegation** — Agent A asks Agent B, which asks
  Agent A. Symptom: no progress, repeated handoffs, growing
  context with no new artifacts. Fix: enforce a strict pipeline
  direction. Every handoff moves the task forward; if an agent
  cannot proceed, escalate to the user, not back to the previous
  agent.
- **No verification** — skipping review because "the coder is
  good enough." Fix: always include a review gate. At minimum,
  run tests, run lint, check the output against the spec.
- **Premature parallelism** — fan-out before understanding
  dependencies, causing merge conflicts or duplicated work. Fix:
  always run a planning stage first.
- **Vague handoffs** — "I made some changes, please review"
  without specifics. Fix: use the structured handoff format
  every time.
- **Deferred entity creation** — saying "I'll track that" or
  "I'll file a workitem" without immediately calling the tool.
  Deferred commitments are routinely dropped across turn
  boundaries, leaving the entity layer out of sync with what
  was agreed. Fix: call `create_workitem`, `record_decision`,
  or the relevant MCP tool in the same turn as the commitment.
- **Skipping the skill catalog for domain tasks.** When a
  domain-specific task arrives (writing a PRD, creating a
  release, reviewing a skill), the agent goes to general
  knowledge instead of checking `skill-finder` or
  `search_entities`. The skill catalog exists precisely because
  processkit has conventions (entity storage paths, output
  formats, workitem linking) that general knowledge does not
  know. Fix: run `search_entities(text="<task keyword>")` or
  consult `skill-finder` before starting any domain task.

### Practical tips for Claude Code

1. **One agent session = one role at a time.** Switch roles
   explicitly ("Now acting as Reviewer").
2. **Use files for context, not memory.** Write `_handoff.md` or
   `_findings.md`; read them in the next step.
3. **Keep scratch files temporary.** Clean up `_agent_notes.md`,
   `_blackboard.md` after the workflow completes.
4. **Verify with tools, not judgment.** Run `cargo test`,
   `npm test`, or the appropriate linter rather than "I think
   this looks right."
5. **Time-box research.** Researchers answer specific questions,
   not "tell me everything about X."
6. **Limit fan-out to 3-4 parallel subtasks.** More than that and
   coordination overhead exceeds the benefit.
7. **Always include file paths.** Every handoff and finding
   should reference absolute paths and line numbers.

### Respect the configured context budget

Projects can declare a budget in their processkit configuration
file (the location depends on how processkit was installed — for
example `aibox.toml` if the project uses aibox, or a standalone
`processkit.toml` for unmanaged installs):

```toml
[context.budget]
target_tokens = 8000          # aim NOT to exceed this on initial load
max_tokens = 16000            # hard ceiling — must use lazy loading above this

[context.budget.always_load]
files = [
  "AGENTS.md",
  "context/HANDOVER.md",
  "context/owner/identity.md",
  "context/owner/working-style.md",
  "context/INDEX.md",
  "context/migrations/INDEX.md",
]

[context.budget.on_demand]
patterns = [
  "context/skills/**",
  "context/workitems/**",
  "context/logs/**",
  "context/decisions/**",
]
```

The agent reads `[context.budget]` at session start (it's part
of the `always_load` set if not overridden) and follows the rules:

- `always_load.files` are loaded into the first turn
  unconditionally
- `on_demand.patterns` are loaded only when needed, via the index
  MCP server or direct file reads
- The agent estimates the total token count of `always_load` and
  warns the user if it exceeds `target_tokens`

The values are advisory — there is no runtime enforcement. The
agent honors them as instructions.

### When context is still too big

If even the always-load set is too large, the agent should:

1. Surface this to the user: "Loading 24k tokens of context,
   target is 8k. Want me to run `context-grooming`?"
2. Suggest specific candidates for archival or summarization
   based on the `context-grooming` ruleset
3. Offer to update the `[context.budget]` config to a higher
   target if the project genuinely needs more
4. Never silently truncate or drop files

### Relationship to context-grooming

`agent-management` says HOW to load context efficiently per
session. `context-grooming` runs periodically to make the corpus
smaller. Both work together: grooming reduces the live size;
lazy loading reduces what gets loaded from that smaller corpus.
