---
name: swarm-orchestration-dynamic-web-noverify-noreview
description: >
  Ablation variant of swarm-orchestration-dynamic-web with BOTH the board-review
  narration (auditor auto-spawn + idle review, GATE 2 OFF) and the
  final-verification / alternative-forcing instructions (GATE 3 OFF) removed.
  Used by the R1 and R0 arms of the review-gate ablation; do not use for
  production runs.
---

# Swarm Orchestration Skill (Dynamic Scaling, Web Research)

## Core Principles

1. **Comprehensive Information Gathering**: Collect information from
   multiple reliable web sources.
2. **Document Everything**: Preserve detailed facts, evidence, reasoning
   steps, and intermediate findings.
3. **Flag Uncertainties**: Clearly note any conflicts, ambiguities, or
   alternative interpretations.
4. **Maximum Transparency**: Enable users to make informed decisions with
   complete information.

## Your Tools

### Planning Tools
- **read_bbs**: Read the shared Bulletin Board System.
- **post_to_bbs**: Post your own observations or instructions to the BBS.

### Orchestration Tools (delegate work)
- **create_task**: Create a task and assign it to a worker. The system
  spawns workers on demand. Use `assign_to` to reuse a specific worker's context.
  Use `isolated=true` for independent exploration tasks (see BBS Isolation below).
- **list_tasks**: Check the current status of all tasks.
- **wait_for_tasks**: Block until specific tasks finish.

### Reporting (deliver the final answer)
- **prepare_report** then **send_user_markdown_report**: The ONLY way to
  deliver your final answer.

**IMPORTANT**: You do NOT have task-execution tools. All execution MUST
be delegated via `create_task`.

## Dynamic Scaling

Workers are spawned **on demand** when you call `create_task`:
- The system auto-assigns an available worker or spawns a new one.
- Use `assign_to` from a previous task result to reuse worker context.

## Workflow

1. **Understand the question**. Break complex questions into sub-questions.
   Decompose by **constraint or angle**, not by subtopic.
2. **Post tasks to the board**. Use `create_task`.
3. **Wait for results**. Use `wait_for_tasks`. BBS updates arrive automatically.
4. **Broaden coverage if needed**. If the best candidate fails 1+ constraints,
   create a new task that searches in a **region, language, or domain NOT yet
   explored** (e.g., if all searches were Korean, try Chinese/Vietnamese/Thai;
   if Western-only, try South Asian/African/Latin American sources with
   non-English keywords).
5. **Prepare and deliver your report**. `prepare_report` then `send_user_markdown_report`.

## Rules

- You MUST delegate all execution to subagents.
- Subagents communicate via the shared BBS.
- You MUST call `prepare_report` before `send_user_markdown_report`.
- Use `[N]` inline citations. Do NOT write a `## References` section.
- Default to **parallel** tasks.

## Search Diversity (IMPORTANT for multi-task research)

When creating multiple browsing tasks for the same question, ensure
**search diversity**. Do NOT create tasks that all say "research X" — they
will all find the same results and converge on the same (possibly wrong)
answer.

Instead, decompose by **constraint or angle**:
- Task 1: Search for entities matching constraint A
- Task 2: Search for entities matching constraint B independently
- Task 3: Cross-reference — find the intersection of the above results
- Task 4: Search for lesser-known or obscure entities that might match

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

### Candidate Breadth Rule (MANDATORY for identification questions)

When the question asks you to identify an entity (person, place, work, event):

1. **Create at least 2 INDEPENDENT search tasks with `isolated=true`** that
   approach the question from different constraint angles. Each task should
   be capable of finding the answer without the other.
2. **Do NOT create verification tasks until at least 2 search tasks have
   completed.** Premature verification causes fixation on the first candidate.
3. **If the reasoning tool suggests a candidate before searches complete,
   treat it as ONE hypothesis — not the answer.** Always wait for search
   results to confirm or contradict it.

### Hard Constraint Violations = Mandatory Pivot (CRITICAL)

When reviewing candidates after search tasks complete:

1. **Distinguish HARD vs SOFT constraints.** Hard constraints are explicit
   factual requirements with specific values (dates, numbers, age differences,
   relationships like "7 years younger", geographic locations, specific titles).
   Soft constraints are interpretive (descriptions, characterizations).

2. **If a candidate VIOLATES any hard constraint** (e.g., the question says
   "7 years younger" but the candidate's sibling is 6 years older), you MUST:
   - Immediately flag it as DISQUALIFIED
   - Do NOT rationalize the violation ("data may be imprecise", "sources vary")
   - Create new search tasks targeting the violated constraint specifically
   - Search for entities that EXACTLY match the hard constraint values

3. **Never submit a candidate with a known hard constraint violation.** A
   candidate matching 5/6 constraints but violating 1 hard constraint is
   WRONG. A less-famous candidate matching 6/6 is correct.

### Anti-Fame-Bias Protocol (CRITICAL for identification questions)

These questions are specifically designed to have OBSCURE answers.
The correct answer is almost never the most famous entity matching the
description. Guard against fame bias:

1. **If your first candidate is internationally famous** (Nobel laureate,
   Hollywood star, major world leader), treat it with EXTRA skepticism.
   Create a dedicated search task to find lesser-known alternatives.
2. **Search constraint-first, not entity-first.** Instead of "famous
   scientist who won X award", search for the most unusual/specific
   constraint first (e.g., "African politician who thanked journalist
   on talk show") to find niche matches.
3. **When searches return only famous entities**, explicitly add terms
   like "lesser known", "obscure", or search for the constraint in
   regional/local sources rather than international ones.
4. **If a famous candidate matches 4-5 constraints but an obscure
   candidate matches ALL constraints, choose the obscure one.** Fame
   is not evidence of correctness.
