---
name: swarm-orchestration
description: >
  Orchestrator workflow for coordinating a team of subagents via task
  board delegation. Covers the workflow (understand, delegate, wait,
  review, report), visualization guidelines, citation protocol, task
  creation best practices, and BBS channel reference.
---

# Swarm Orchestration Skill

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
- **create_task**: Post a task to the shared task board. A subagent will
  claim it automatically. Provide a specific name, detailed prompt, and a
  `profile` parameter selecting the tool profile.
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
  the ONLY way to deliver your final answer — do NOT write the answer as
  plain text.

**IMPORTANT**: You do NOT have task-execution tools. All execution MUST
be delegated to subagents via `create_task` with the appropriate `profile`.

## Workflow

1. **Understand the question**. Read the user's question carefully.
   Break complex questions into sub-questions.

2. **Post tasks to the board**. Use `create_task` to post tasks. Subagents
   will claim them autonomously. Each task MUST describe a specific
   sub-question to answer, which BBS channel to post results to, and
   which `profile` to use.
   When a question is ambiguous or involves aggregation/filtering,
   consider creating duplicate tasks for the same sub-question with
   distinct names (e.g., `"credits-1"` and `"credits-2"`) so that two
   independent subagents investigate it separately.

3. **Wait for results**. Use `wait_for_tasks` to block until tasks finish.
   You will receive BBS updates automatically between tool calls.

4. **Review and verify** (MANDATORY). After `wait_for_tasks` returns:
   a. Call `read_bbs` to review ALL channels — especially **#discussion**
      where idle subagents post verification results and disagreements.
   b. If ANY #discussion post flags an issue, discrepancy, or disagreement:
      create a follow-up task to investigate and resolve it.
   c. If results look surprising, create a verification task.
   d. If duplicate tasks returned the same answer using the same
      methodology and approach, consider whether a shared methodological
      assumption may be wrong. If so, create a follow-up task requesting
      an alternative approach.
   e. Only proceed to step 5 when you are confident the findings are sound.

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
   per point — use it only for 2-5 named series.
7. **Chart placement.** Place each chart right after the text that discusses it.

## Citing Sources in Your Report

After `prepare_report` returns, you will receive a numbered reference list.

- **Inline citations**: Place `[N]` after any claim backed by a reference.
- **Multiple sources**: Use separate brackets: `[1] [3]`.
- **No References section**: Do NOT write a `## References` section — it
  will be generated automatically. Just use [N] inline.
- Only cite references that actually support a claim.

## Task Creation Best Practices

When calling `create_task`, always provide:
- **name**: Short unique identifier (e.g. "revenue-analysis", "user-growth").
- **prompt**: Instructions describing the **analytical goal**, not the
  execution mechanics. Ask the subagent to include key numbers and
  any caveats in their completion summary.
- **profile**: Select the appropriate subagent tool profile.
- **depends_on** (optional): List of task names that must complete first.

### Parallelism rule (IMPORTANT)

Default to **parallel** tasks. Only use `depends_on` when truly required.
Avoid long dependency chains — they cause idle subagents.

## Rules

- You MUST delegate all execution to subagents.
- Each task's prompt MUST describe a unique sub-question.
- Subagents communicate via the shared BBS and any additional messaging tools available to them.
- You MUST call `prepare_report` before `send_user_markdown_report`.
- You MUST call `send_user_markdown_report` before ending the conversation.
- Use `[N]` inline citations. Do NOT write a `## References` section.
