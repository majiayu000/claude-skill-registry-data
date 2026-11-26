---
name: agents
description: "Rules for delegating work to subagents: when to spawn, bundle or continue one, how to scope its files, which agent definition and model each role gets, and how to verify and terminate. Use when spawning, coordinating or cleaning up subagents or teammates."
---

# agents

Delegate only where it pays, scope it tightly, and never leave an agent running.

## When to use

- Work splits into independent parts that can run in parallel.
- An independent reviewer is needed for a diff or a decision.
- A long search or audit would flood the orchestrator with output.

## Rules

- The orchestrator does itself: plan, verify a claim, run the verify command, route
  labels, commit, push, open and update a pull request. Also directly: a read, a lookup, a one
  line nit, and a change of about five lines or fewer with no logic: text, configuration, a
  single value. Such a change still goes through review like any other.
- Everything else that changes behaviour runs in a subagent: an implementation, a review fix at
  should or blocker level included. Code with logic and any change that needs a new or changed
  test always run in a subagent.
- One bounded scope per agent: the goal, the files it may touch, the house style, what it must
  not do.
- A subagent cannot fetch, no exception. Fetch in the orchestrator first and give it the
  result; a brief that tells it to fetch gets stale refs reported back as current.
- Parallel spawning only for independent work. One agent waiting on another is sequential work
  pretending to be parallel.
- The session collects the agents' baseline feedback and raises what is worth a change through
  `propose-rule`, one issue per rule, never silently.
- Agent output is a claim, not a fact: verify files, run tests, read the diff before relying on
  it.
- A conflict between two agents' changes, such as a merge conflict on overlapping files from
  parallel work or a review finding that traces to one agent's change, is resolved by the agent
  that caused it. Not by a third agent, and not absorbed silently by the orchestrator.
  Exception: the causing agent is already terminated, stale or stuck. Then the orchestrator
  resolves the conflict directly, or reassigns a fresh agent, and says so in its report.
- Never ask an agent to do something that was denied in this session. Never route work through an
  agent to get around a permission decision.

### Roles and models

- Implementation: the `implementer` agent, `sonnet`. A plan may override one task's model and
  states why in one line, tokens and time against capability.
- Review: the `reviewer` agent, `sonnet`. The `reviewer-boundary` agent, `opus`, only when the
  path list in `work-review` matches. The list decides, not a feeling about the change.
- Plan: `opus`. Search and lookup: the built in search agent.
- An agent definition is missing in this installation: use a general agent with the same model
  and the definition's rules in the brief, and say so in the report.

### Spawn, bundle or continue

- A fresh agent pays its base load again and knows nothing. An agent that grows long reads its
  whole history on every request. Both cost.
- Continue the same agent with a message for a rework round, a re-review and a follow up
  question on its own work. Never spawn a second agent for that.
- Bundle small issues of one repository into one `implementer`: each small enough for one
  commit, no overlap in files, one worktree per issue named in the brief.
- A large issue gets a fresh agent. So does an agent whose report says it neared its turn limit.
- A continued agent that has been idle for more than a few minutes has lost its cache. Still
  continue it when it holds context the next step needs, otherwise spawn fresh.
- No agent waits: not for CI, not for another agent, not for a slow command. The orchestrator
  waits with one background command and continues the agent afterwards.
- Spawn the review only once CI on the head commit has finished.

### Briefs

- Give the agent the plan and the rules it needs, not the full conversation transcript.
- A reviewer's brief names the repository, the issue and the pull request, nothing about why
  the change is right.
- The dispatching session verifies every precondition a brief asserts before it sends the brief:
  a file exists where the brief says, a branch is where it says, a tool is installed.
- A brief that depends on work not merged yet says so plainly and gives the path to read it
  from. It never describes that work as present.
- A statement in a brief about how a tool behaves is an assumption until someone runs it. The
  brief labels it as one.
- An agent that finds a stated precondition false stops and reports it. It does not reconstruct
  what is missing. An unattended agent records it on the issue and stops that task.

### Monitoring

- State an expected duration when spawning an agent.
- Not reported by then: check its status and last output instead of waiting longer.
- Stuck, idle or looping: terminate it, then reassign its scope or finish it directly.
- An agent that stopped at its turn limit reports what is left. Split the rest, do not just
  send it on.
- Terminate every agent whose work is done, or that is stale or stuck. Idle is not done: an agent
  that finished a step and waits for the next instruction stays alive on purpose, judged by its
  reported state, never by idleness alone.
- No status update proves an agent has stopped. Terminate it and confirm before reusing its
  worktree.
- Agent team mode: a teammate idle without reporting is asked once, then terminated if still
  silent.
- Check the running agent list before spawning more, and again before ending the session. The
  list must be empty at the end.

### Report shape

- What changed, per target: a table or a short list, not a walkthrough.
- Which claims were verified by running something, and what ran.
- Which claims are unverified, and why.
- What it stopped on, if anything.
- Baseline feedback: a rule that blocked or misled, a rule that was missing, or "none".
- No narration of work already done. The report stays in the orchestrator's context and
  is paid for on every later request.

## Steps

1. Decide whether the work is a read, a lookup or a one line nit. Anything else goes to a
   subagent.
2. An agent already holds the context: continue it. Otherwise split the work so results do not
   overlap, and name the output of each agent.
3. Spawn with scope, files, style and a reporting instruction.
4. Collect results, verify them, resolve conflicts between agents per the rule above.
5. Terminate every agent, confirm the list is empty.
6. Report outcome per agent, including what was rejected.

## Guardrails

- Scope, allowed files and style given to every agent, no exceptions.
- Results verified before being relied on.
- Agent list empty before the session ends.
