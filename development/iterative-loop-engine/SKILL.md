---
name: iterative-loop-engine
description: >-
  "Am I ACTUALLY done, or did I just stop?" - Iterative workflow engine,
  all-purpose. Use when (1) task has clear completion
  criteria, (2) single-pass execution is insufficient, (3) quality requires
  iteration, (4) "keep going until X" patterns apply. Provides the abstract
  loop; pair with domain-specific criteria files. Does NOT trigger for: simple
  tasks, tasks without clear success criteria, or when user wants
  quick/approximate results.
---

## Vasana

A vasana is a pattern that persists across unrelated contexts. If during
this task you notice such a pattern emerging, it may be worth capturing.
This skill works best alongside the `vasana` skill and `vasana` hook
from the Vasana System plugin.

Modify freely. Keep this section intact.

# Iterative Loop Engine: The Meta-Pattern

**Seed question:** *Am I ACTUALLY done, or did I just stop?*

## Foundation: a completion-criteria loop

This skill is a **completion-criteria loop** (lineage: the "ralph" loop, after Geoffrey Huntley — see Origins below): define "done" up front, re-check it every pass, and refuse to exit until every criterion passes.

> Keep going until genuinely complete — not until tired, bored, or "close enough."

**Origins:**
- **Original concept:** Geoffrey Huntley ([ghuntley.com/ralph](https://ghuntley.com/ralph/))
- **Claude Code implementation:** Anthropic ([github.com/anthropics/claude-code-plugins](https://github.com/anthropics/claude-code-plugins))
- **Author:** Daisy Hollman (Anthropic)

This skill abstracts that loop into a **domain-agnostic loop engine** that can be applied to any task with clear completion criteria, not just factual verification.

---

## Core Principle

The core insight: **most tasks fail not from lack of capability, but from premature exit.**

The loop engine enforces persistence:
- Define criteria BEFORE starting
- Check criteria EVERY pass
- Exit ONLY when criteria pass
- Never "close enough"

## The Abstract Loop

```
WHILE (completion criteria NOT all pass):
    1. EXECUTE - Do one pass of work using domain methodology
    2. ASSESS - Evaluate results against domain criteria
    3. CHECK - Compare against completion thresholds
    4. IF gaps exist:
       - Identify which criteria failed
       - Plan targeted action for next pass
       - ITERATE
    5. IF all pass:
       - Output completion promise
       - EXIT
```

## Domain Components

Each domain requires:

| Component | Purpose | Location |
|-----------|---------|----------|
| **Criteria file** | Defines "complete" for this domain | `criteria/<domain>.criteria.md` |
| **Work methodology** | How to execute each pass | Domain-specific skill |
| **Assessment method** | How to evaluate results | In criteria file |
| **Completion promise** | Text that signals success | In criteria file |

## Quick Domain Selection

| Your Task | Use This Criteria | Completion Promise |
|-----------|------------------|-------------------|
| Factual research, investigations | `criteria/investigation.criteria.md` | ALL FALSIFICATION CRITERIA PASS |
| Code implementation, TDD | `criteria/programming.criteria.md` | ALL PROGRAMMING CRITERIA PASS |
| PR iteration, code reviews | `criteria/review.criteria.md` | ALL REVIEW CRITERIA PASS |

## Available Domains

### Investigation (`criteria/investigation.criteria.md`)
- Factual accuracy verification
- Evidence tier labeling (VERIFIED/CREDIBLE/ALLEGED/SPECULATIVE)
- Source independence requirements
- **Promise:** `ALL FALSIFICATION CRITERIA PASS`
- **Based on:** Original ralph-loop use case
- **Enhanced:** See `self-improving-investigation` for blind worker + dialectic methodology

### Programming (`criteria/programming.criteria.md`)
- Code quality verification
- Test passage requirements
- Build/lint success
- **Promise:** `ALL PROGRAMMING CRITERIA PASS`
- **New:** Extends ralph-loop to software development

### Review (`criteria/review.criteria.md`)
- PR iteration completion
- Comment resolution
- CI status verification
- **Promise:** `ALL REVIEW CRITERIA PASS`
- **New:** Extends ralph-loop to code review workflows

## Using the Engine

### Step 1: Select Domain
Identify which criteria file applies to your task.

### Step 2: Load Criteria
Read the criteria file to understand completion requirements.

### Step 3: Execute Loop
```
pass = 1
WHILE true:
    # Execute
    results = execute_work_pass(pass)

    # Assess
    assessment = evaluate_against_criteria(results)

    # Check
    IF all_criteria_pass(assessment):
        output_completion_promise()
        BREAK
    ELSE:
        gaps = identify_gaps(assessment)
        plan_next_iteration(gaps)
        pass += 1
```

### Step 4: Output Format

Each iteration produces:

```markdown
## Pass [N]

### Work Completed
[What was done this pass]

### Criteria Check
- [ ] Criterion 1: [status] (threshold: X) [pass/fail]
- [ ] Criterion 2: [status] (threshold: Y) [pass/fail]
...

### Status
[INCOMPLETE: N criteria failing] or [COMPLETE: All criteria pass]

### If Incomplete: Next Iteration Plan
- Gap: [what's missing]
- Action: [what to do next]
```

### Step 5: Completion

Only when ALL criteria pass:

```markdown
## Final Status

All criteria satisfied:
- [X] Criterion 1: [final status]
- [X] Criterion 2: [final status]
...

<promise>[DOMAIN COMPLETION PROMISE]</promise>
```

## Critical Rules

1. **Never claim completion while criteria fail**
   - The promise is a contract, not a formality

2. **Never skip assessment**
   - Every pass must evaluate against criteria

3. **Gaps are data, not failures**
   - Failed criteria tell you what to do next

4. **Iterate until genuinely complete**
   - Not until tired, bored, or "close enough"

## Safety Limits

To prevent infinite loops and runaway iterations:

| Limit | Default | Purpose |
|-------|---------|---------|
| **Max iterations** | 10 | Prevents unbounded execution |
| **Time per pass** | No limit | Domain-dependent, set in criteria if needed |
| **User override** | Allowed | Can specify `--max-iterations N` |

### When Max Iterations Reached

If completion criteria not met after max iterations:

1. **Do NOT output completion promise** - that would be a lie
2. **Output diagnostic report:**
   ```markdown
   ## Iteration Limit Reached

   Completed: [N]/[max] iterations
   Criteria status:
   - [X] Criterion 1: PASS
   - [ ] Criterion 2: FAIL (blocked by: [reason])

   **Recommendation:** [next steps for user]
   ```
3. **Notify user** with summary of blocking issues
4. **Wait for human decision** before proceeding

## Failure Modes

### External System Failures

| Failure | Response |
|---------|----------|
| CI/build system down | Document, continue with local verification where possible |
| Network issues | Use cached data, flag as ALLEGED tier |
| Test flakiness | Retry once, then document as known issue |
| Rate limiting | Pause, retry with backoff, document if persistent |

### Criteria Impossible to Satisfy

Sometimes criteria cannot be met due to external constraints:

1. **Identify the blocker** - which criterion and why
2. **Assess if blocker is temporary or permanent**
3. **If temporary:** Wait or work around
4. **If permanent:**
   - Document the limitation
   - Output partial results with gap clearly labeled
   - Do NOT claim completion promise
   - Ask user for guidance

### Graceful Degradation

When optimal verification isn't possible, degrade gracefully:

```
VERIFIED → CREDIBLE → ALLEGED → SPECULATIVE
Full tests → Partial tests → Manual verification → Documented gap
```

Always document the degradation and its reason.

## Integration with ralph-loop Plugin

This skill complements the official ralph-loop plugin:

|  ralph-loop | iterative-loop-engine |
|--------------|----------------------|
| `/ralph-loop:ralph-loop` command | Skill-based activation |
| External orchestration | Self-contained methodology |
| Generic tasks | Domain-specific criteria |

**When to use which:**
- ** ralph-loop plugin:** General iterative tasks, command-line invocation
- **iterative-loop-engine:** Domain-specific criteria, skill integration, agent embedding

## Integration with Agents

Agents using this engine should:

1. **Reference this skill** in their definition
2. **Specify which criteria file** applies
3. **Define their completion promise** based on domain
4. **Include the loop** in their execution logic

Example agent header:
```yaml
---
name: iterative-programmer
description: Uses iterative-loop-engine with programming criteria...
---

# First Actions
1. Read `skills/iterative-loop-engine/SKILL.md`
2. Read `skills/iterative-loop-engine/criteria/programming.criteria.md`
3. Execute the loop until completion promise can be truthfully output
```

## Anti-Patterns

| Anti-Pattern | Why It Fails | Correct Behavior |
|--------------|--------------|------------------|
| Single-pass and declare done | Misses gaps that iteration reveals | Always check criteria |
| "Close enough" completion | Defeats purpose of criteria | All criteria or not done |
| Skipping assessment | Can't know if done without checking | Every pass = assess |
| Changing criteria mid-loop | Moves goalposts | Criteria fixed at start |

## Extending to New Domains

To add a new domain:

1. Create `criteria/<domain>.criteria.md`
2. Define:
   - Completion criteria (specific, measurable)
   - Thresholds for each criterion
   - Assessment methodology
   - Completion promise text
3. Create/update agent to use the new criteria
4. Test with representative tasks

---

## Attribution

This skill builds on the  ralph-loop methodology:

- **Original concept:** Geoffrey Huntley ([ghuntley.com/ralph](https://ghuntley.com/ralph/))
- **Claude Code implementation:** Anthropic ([github.com/anthropics/claude-code-plugins](https://github.com/anthropics/claude-code-plugins))
- **License:** MIT (as part of Claude Code ecosystem)

---

## Test Scenarios

### Scenario 1: Programming Domain - TDD Cycle
**Setup:** Implement a new feature with failing tests
**Expected:**
- Pass 1: RED (test exists, fails)
- Pass 2: GREEN (minimal implementation, test passes)
- Pass 3: REFACTOR (cleaned code, all tests pass)
- Output: `<promise>ALL PROGRAMMING CRITERIA PASS</promise>`
**Success Criteria:** Loop iterates until all tests pass, never claims completion with failing tests

### Scenario 2: Max Iterations Reached
**Setup:** Task with impossible-to-meet criteria, max 3 iterations
**Expected:**
- 3 iterations attempted
- NO completion promise output
- Diagnostic report with blocking issues
- User notification
**Success Criteria:** Does NOT output completion promise when criteria fail

### Scenario 3: Investigation Domain - Evidence Tier Escalation
**Setup:** Research claim with only marketing sources initially
**Expected:**
- Pass 1: Claims marked ALLEGED (single-source)
- Pass 2: Independent sources found, upgraded to CREDIBLE
- Pass 3: Primary source verification, upgraded to VERIFIED
- Output: `<promise>ALL FALSIFICATION CRITERIA PASS</promise>`
**Success Criteria:** Evidence tiers accurately reflect source quality

### Scenario 4: Review Domain - PR Iteration
**Setup:** PR with 3 blocking review comments
**Expected:**
- Pass 1: Address comment 1, push fix
- Pass 2: Address comments 2-3, push fixes
- Pass 3: All comments resolved, CI passing, approvals received
- Output: `<promise>ALL REVIEW CRITERIA PASS</promise>`
**Success Criteria:** Iterates until all blocking comments resolved and CI passes

### Scenario 5: Graceful Degradation
**Setup:** CI system unavailable during programming task
**Expected:**
- Document CI unavailability
- Continue with local verification where possible
- Degrade from "Full tests" to "Manual verification"
- Note degradation in output, do NOT claim full completion promise
**Success Criteria:** Handles external failures gracefully, documents limitations
