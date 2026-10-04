---
name: swarm-orchestration-web
description: >
  Orchestrator workflow for coordinating a team of web-research subagents
  via task board delegation. Covers the workflow (understand, delegate,
  wait, review, report), visualization guidelines, citation protocol,
  and task creation best practices.
---

# Swarm Orchestration Skill (Web Research)

## Core Principles

1. **Comprehensive Information Gathering**: Collect information from
   multiple reliable web sources.
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
  Use `isolated=true` for independent exploration tasks (see BBS Isolation below).
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

3. **Wait for results**. Use `wait_for_tasks` to block until tasks finish.
   You will receive BBS updates automatically between tool calls.

4. **Review and verify** (MANDATORY). After `wait_for_tasks` returns:
   a. Call `read_bbs` to review ALL channels — especially **#discussion**
      where idle subagents post verification results and disagreements.
   b. If ANY #discussion post flags an issue, discrepancy, or disagreement:
      create a follow-up task to investigate and resolve it.
   c. If results look surprising, create a verification task.
   d. **Geographic expansion rule**: If the best candidate fails 1+
      constraints, create a new task that explicitly searches in a
      **region or language NOT yet explored**. For example, if all
      searches were Korean/Japanese, try Chinese, Vietnamese, Thai,
      or South Asian sources. If all searches were Western, try Middle
      Eastern, African, or Latin American sources. Include specific
      non-English keywords or region names in the task prompt.
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
- **name**: Short unique identifier (e.g. "market-research", "competitor-analysis").
- **prompt**: Instructions describing the **research goal**, not the
  execution mechanics.
- **profile**: Select the appropriate subagent tool profile.
- **depends_on** (optional): List of task names that must complete first.

### CRITICAL: Do NOT pre-specify implementation details

**Never put specific URLs, search queries, or tool-specific instructions
in task prompts.** Subagents have the right tools and skills to discover
the correct approach themselves.

Instead of:
> "Search Google for 'company X revenue 2025' and scrape the first result"

Write:
> "Find the most recent revenue figures for company X. Search multiple
sources and cross-verify the numbers."

The orchestrator's job is to **decompose the question** into sub-questions.
The subagent's job is to **choose the right sources and approach**.

### Parallelism rule (IMPORTANT)

Default to **parallel** tasks. Only use `depends_on` when truly required.
Avoid long dependency chains — they cause idle subagents.

### Search Diversity (IMPORTANT for multi-task research)

When creating multiple browsing tasks for the same question, ensure
**search diversity**. Do NOT create tasks that all say "research X" — they
will all find the same results and converge on the same (possibly wrong)
answer.

Instead, decompose by **constraint or angle**:
- Task 1: Search for entities matching constraint A (e.g. "Find all
  recipients of X award born before 1900")
- Task 2: Search for entities matching constraint B independently (e.g.
  "Find all winners of Y prize who also published in Z journal")
- Task 3: Cross-reference — find the intersection of the above results
- Task 4: Search for lesser-known or obscure entities that might match
  (not just famous ones)

The goal is to **cast a wide net** so the team finds ALL plausible
candidates, not just the most obvious one. Obvious partial matches are
the #1 source of wrong answers.

### BBS Isolation (MANDATORY for initial exploration)

Use `isolated=true` when creating tasks to make subagents search
WITHOUT seeing other agents' findings. Isolated agents cannot read the
BBS — they search independently and only post their own discoveries.
This prevents premature convergence on a single (possibly wrong) candidate.

**When to use `isolated=true`:**
- First 2-3 exploration tasks (initial broad search from different angles)
- Tasks that need fresh, unbiased investigation of a specific constraint
- "Contrarian search" tasks that must find alternatives independently

**When to use `isolated=false` (default):**
- Verification tasks that need to check findings from earlier tasks
- Cross-referencing tasks that compare candidates
- Follow-up tasks that build on prior discoveries
- Any task with `depends_on` (it naturally needs prior context)

**Recommended pattern for identification questions:**
1. Create 2-3 `isolated=true` browsing tasks, each approaching from
   a different constraint angle
2. `wait_for_tasks` until those initial tasks complete
3. Review all independent findings via `read_bbs`
4. Create `isolated=false` verification/comparison tasks that can
   see all prior findings
5. If candidates disagree, create a targeted resolution task

### Constraint Verification Protocol (MANDATORY before reporting)

Before calling `prepare_report`, you MUST perform a structured constraint
verification on your best candidate(s):

1. **List every constraint** from the original question (dates, locations,
   attributes, relationships, quantities — every factual requirement).
2. **For each constraint**, cite the specific evidence that your candidate
   satisfies it. Use the format:
   - VERIFIED: Constraint "born before 1900" → Evidence: [source] confirms birth year 1872
   - UNVERIFIED: Constraint "won award X" → NOT VERIFIED — no source found
3. **If ANY constraint is unverified or contradicted**, do NOT report yet.
   Instead, create a targeted follow-up task to specifically verify or
   disprove that constraint.
4. **If you have 2+ candidates**, compare them constraint-by-constraint.
   Choose the one satisfying the MOST constraints with the strongest evidence.
5. **Never report an answer with 2+ unverified constraints.** If stuck,
   create a "contrarian search" task targeting the unverified constraints
   before reporting your best guess.

### Anti-Fixation Rule (CRITICAL)

After your first round of search tasks completes:
1. **Count distinct candidates** found across all task results and BBS posts.
2. **If only 1 candidate emerged**: You MUST create at least one additional
   "alternative search" task with `isolated=true` before reporting. This
   task must explicitly search for entities OTHER than the current candidate
   that could match the constraints. Include in the task prompt: "Do NOT
   search for [current candidate]. Find alternative entities matching:
   [key constraints]."
3. **If 2+ candidates emerged**: Compare them directly against all
   constraints before choosing. Do NOT default to the first one found.
4. **BrowseComp questions ALWAYS have exactly one correct answer.** Never
   conclude "unable to determine" — if you haven't found it, you haven't
   searched broadly enough. Try different languages, regions, time periods,
   or domains.

## Rules

- You MUST delegate all execution to subagents.
- Each task's prompt MUST describe a unique sub-question.
- Subagents communicate via the shared BBS and any additional messaging tools available to them.
- You MUST call `prepare_report` before `send_user_markdown_report`.
- You MUST call `send_user_markdown_report` before ending the conversation.
- Use `[N]` inline citations. Do NOT write a `## References` section.
