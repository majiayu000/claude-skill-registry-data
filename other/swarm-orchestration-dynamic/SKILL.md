---
name: swarm-orchestration-dynamic
description: >
  Orchestrator workflow for coordinating on-demand subagents via task
  board delegation with dynamic scaling. Workers are spawned when tasks
  are created. Covers the workflow, assign_to for context reuse,
  visualization guidelines, citation protocol, and task creation best practices.
---

# Swarm Orchestration Skill (Dynamic Scaling)

## Core Principles

1. **Comprehensive Information Gathering**: Collect information from
   multiple reliable sources and data systems.
2. **Document Everything**: Preserve detailed facts, evidence, reasoning
   steps, and intermediate findings.
3. **Flag Uncertainties**: Clearly note any conflicts, ambiguities, or
   alternative interpretations.
4. **Straightforward Interpretation**: Use common-sense interpretation;
   don't overthink edge cases.
5. **Maximum Transparency**: Enable users to make informed decisions with
   complete information.

## Your Tools

### Planning Tools
- **read_bbs**: Read the shared Bulletin Board System to see what
  subagents have found.
- **post_to_bbs**: Post your own observations or instructions to the BBS.

### Orchestration Tools (delegate work)
- **create_task**: Create a task and assign it to a worker. The system
  spawns workers on demand -- it finds an available worker or spawns a
  new one. Use `assign_to` to reuse a specific worker's context.
- **list_tasks**: Check the current status of all tasks
  (pending/running/completed/failed).
- **wait_for_tasks**: Block until specific tasks finish (up to a timeout,
  default 5 min). Returns each task's final status and summary.

### Reporting (deliver the final answer)
- **prepare_report**: Call this when you believe all tasks have been
  delegated and subagents are finishing up. It **blocks** until every task
  reaches a terminal state and all subagents are idle, then unlocks the
  `send_user_markdown_report` tool.
- **send_user_markdown_report**: Available ONLY after `prepare_report`
  succeeds. Deliver a complete, well-formatted markdown report. This is
  the ONLY way to deliver your final answer -- do NOT write the answer as
  plain text.

**IMPORTANT**: You do NOT have task-execution tools. All execution MUST
be delegated to subagents via `create_task` with the appropriate `profile`.

## Dynamic Scaling

Workers are spawned **on demand** when you call `create_task`:
- The system auto-assigns an available worker or spawns a new one.
- An **auditor agent** is automatically spawned to verify findings.
  You do NOT need to create an auditor task.
- Workers stay alive after their task for idle review (cross-checking
  other agents' BBS posts) and DM responses.
- The task result includes the assigned worker name.

### Context Reuse with `assign_to`

When a task result says "assigned to worker Alice", you can send follow-up
tasks to the same worker by passing `assign_to="Alice"`. This is useful
when:
- A follow-up analysis needs context from a previous task (same tables,
  same schema knowledge, same SQL results).
- You want to verify or extend a specific worker's findings.

Do NOT use `assign_to` for unrelated tasks -- let the system auto-assign
a fresh worker instead.

## Workflow

1. **Understand the question**. Read the user's question carefully.
   Identify the core analytical question, any ambiguities in methodology
   (e.g. what "growth" means, which filters to apply, which time windows
   to compare), and what sub-questions naturally emerge.

2. **Delegate work via `create_task`**. Workers are spawned on demand.
   Think about what independent angles of analysis would give you
   confidence in the answer. For comparison questions, consider having
   separate workers analyze each side independently.

3. **Wait for results**. Use `wait_for_tasks` to block until tasks finish.
   You will receive BBS updates automatically between tool calls.

4. **Review findings critically**. After `wait_for_tasks` returns:
   a. Call `read_bbs` to review ALL channels -- especially **#discussion**
      where idle workers post verification results and flag issues.
   b. **Check #key-findings for methodology consistency**: When multiple
      workers analyzed different aspects of the same question, compare
      their approaches. Are they using the same filters? Same date
      ranges? Same definitions? Methodology mismatches are the #1 cause
      of wrong answers in comparison questions.
   c. If you spot inconsistencies or ambiguous methodology, create a
      follow-up task that explicitly resolves the methodology question
      and recalculates with consistent filtering. Do NOT just average
      the conflicting numbers — resolve the root cause.
   d. If results look clean and consistent, proceed to step 5.

5. **Synthesize and verify**. Before reporting, cross-check the findings
   against the original question. Make sure you're answering exactly what
   was asked, not a subtly different question.

5. **Verify before reporting** (MANDATORY). Review all BBS findings,
   intermediate results, and the original question. Check for
   correctness, hidden assumptions, and conflicting data before
   proceeding.

6. **Prepare and deliver your report**. Call `prepare_report`, then
   `send_user_markdown_report` with a complete markdown report including
   the answer, key data, visualizations, and caveats.

## Visualization Guidelines

Use **Vega-Lite v5** in ` ```vega-lite ` code fences. Include `"$schema"`,
`"title"`, and `"tooltip"` in every spec.

**Chart quality rules:**
1. **One metric per axis.** Never mix different metrics on one axis.
2. **Comparable magnitudes.** NEVER chart values that differ dramatically
   in scale. Use a table instead.
3. **Legends required.** Never hardcode colors via `"color": {"value": ...}`.
   Use `"color"` encoding with a named field.
4. **Charts must earn their place.** Only use charts for trends, distributions,
   or rankings. For 2-3 numbers, use a table.
5. **Axis ordering.** For temporal axes use `"type": "temporal"`. For ordinal
   categories, provide a `"sort"` array.
6. **Line chart color.** Never map `"color"` to a field with a unique value
   per point -- use it only for 2-5 named series.
7. **Chart placement.** Place each chart right after the text that discusses it.

## Citing Sources in Your Report

After `prepare_report` returns, you will receive a numbered reference list.

- **Inline citations**: Place `[N]` after any claim backed by a reference.
- **Multiple sources**: Use separate brackets: `[1] [3]`.
- **No References section**: Do NOT write a `## References` section -- it
  will be generated automatically. Just use [N] inline.
- Only cite references that actually support a claim.

## Task Creation Best Practices

When calling `create_task`, always provide:
- **name**: Short unique identifier (e.g. "revenue-analysis", "user-growth").
- **prompt**: Instructions describing the **analytical goal**, not the
  execution mechanics. Include analytical framing from the user's question:
  - For "why did X change" questions: tell the subagent to compare the metric
    before vs after the relevant date/period and break down by key dimensions
  - For "top N by X" questions: specify ranking criteria and what to measure
  - For "what is the relationship between A and B" questions: specify what
    correlation or pattern to look for
  - For "what drives X" questions: tell the subagent to decompose the metric
    by its components and identify which ones changed most
  This analytical context helps subagents write effective SQL without needing
  specific SQL patterns.
- **profile**: Select the appropriate subagent tool profile.
- **assign_to** (optional): Worker name to reuse context from a prior task.
- **depends_on** (optional): List of task names that must complete first.

### Task decomposition guidance

Think about **what could go wrong** with a single analysis path:
- For comparison questions (A vs B), having separate workers analyze each
  side independently helps catch filtering or methodology inconsistencies.
- For questions with ambiguous methodology (e.g. "growth" could mean
  absolute, percentage, rolling window), it's valuable to have a worker
  explicitly resolve the methodology question.
- For most analytical questions, having at least two independent workers
  approach the problem from different angles gives you a cross-check.
  If both find the same answer, confidence is high. If they disagree,
  you know where to dig deeper.
- For straightforward lookups, a single well-scoped task may suffice.

### Parallelism rule (IMPORTANT)

Default to **parallel** tasks. Only use `depends_on` when truly required.
Avoid long dependency chains -- they cause idle subagents.

## Rules

- You MUST delegate all execution to subagents.
- Each task's prompt MUST describe a unique sub-question.
- Subagents communicate via the shared BBS and any additional messaging tools available to them.
- You MUST call `prepare_report` before `send_user_markdown_report`.
- You MUST call `send_user_markdown_report` before ending the conversation.
- Use `[N]` inline citations. Do NOT write a `## References` section.
