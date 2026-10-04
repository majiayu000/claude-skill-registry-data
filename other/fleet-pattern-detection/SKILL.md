---
name: fleet-pattern-detection
description: How accountability identifies recurring compliance patterns across tasks and sprints — the signals that feed the immune system. Not individual gaps, but systemic trends.
---

# Pattern Detection — Accountability's Immune System Feed

Individual compliance gaps are fleet-ops' concern. YOUR concern is PATTERNS — when the same gap appears across multiple tasks, agents, or sprints, that's a systemic issue. Your pattern reports feed the Doctor, which triggers teaching interventions.

## The Difference Between Gaps and Patterns

**Gap:** Task ABC has no trail events. (One task, one issue.)
**Pattern:** 4 of the last 10 subtasks have no trail events. (Systemic — agents skip trail for subtasks.)

Gaps are noise. Patterns are signal. The immune system responds to patterns, not individual incidents.

## Pattern Categories

### 1. tasks_without_trail

**Signal:** Completed tasks with zero or near-zero trail events.
**What it means:** Agents are completing work without recording their process.
**Threshold:** >20% of done tasks in a sprint have <3 trail events.
**Why it matters:** No trail = no accountability. Fleet-ops can't verify methodology was followed. The Doctor can't detect violations.

**Detection:**
```
acct_pattern_detection()  # scans all done tasks, checks trail event count
```

### 2. skipped_stages

**Signal:** Tasks jumping from inbox to work without passing through analysis/investigation/reasoning.
**What it means:** Agents are implementing without thinking. Or PM is setting task_stage=work for everything.
**Threshold:** >30% of stories/epics skip analysis or reasoning stages.
**Why it matters:** Methodology exists to prevent "code first, think later." Skipping stages means contributions are also skipped.

**Detection:** Check trail for stage_changed events. No analysis → reasoning transition for stories = skipped.

### 3. missing_contributions

**Signal:** Stories/epics completed without required contributions from synergy matrix.
**What it means:** Engineers are implementing without architect design, QA test criteria, or security requirements.
**Threshold:** >25% of stories missing at least one required contribution.
**Why it matters:** The contribution model is how 10 agents coordinate. Without it, each agent works in isolation.

**Detection:** Check task comments for `**Contribution (type)**` typed comments against synergy matrix requirements.

### 4. rubber_stamp_reviews

**Signal:** Approvals with very short comments and no evidence of real review.
**What it means:** Fleet-ops is approving without verifying. The review gate has no teeth.
**Threshold:** >40% of approvals have comments <30 characters.
**Why it matters:** Review is the last gate. If it's rubber-stamped, quality assurance collapses.

**Detection:** Read approval events from board memory. Check comment length and content quality.
Note: The hook on fleet_approve blocks short comments, but if it's set to warn (exit 1) not block (exit 2), agents can override.

### 5. no_qa_predefinition

**Signal:** Stories entering work stage without qa_test_definition contribution.
**What it means:** QA isn't predicting tests. Engineers have no criteria to satisfy.
**Threshold:** >30% of stories have no QA predefinition.
**Why it matters:** Without predefined criteria, "tests pass" is meaningless — pass WHAT?

### 6. readiness_jumps

**Signal:** Task readiness jumping from <50% to 99% in one cycle.
**What it means:** Stage progression is being gamed. Someone is setting readiness artificially.
**Threshold:** Any task with readiness delta >40% in a single update.
**Why it matters:** Readiness maps to methodology stages. Jumps bypass the thinking stages entirely.

## The Detection Protocol

### Periodic (CRON-driven)

Your **pattern-detection** CRON (Wednesday 11am) calls `acct_pattern_detection()`. This:
1. Loads all done tasks from recent sprints
2. For each pattern category: counts occurrences, calculates rate
3. Flags patterns that exceed thresholds
4. Produces report

### Proactive (Heartbeat-driven)

On each heartbeat, if you have compliance data from recent trail verification:
- Do you see the same gap in 3+ tasks? → That's a pattern. Report it.
- Is the same agent appearing in multiple gaps? → Agent-specific pattern.
- Is the same task type consistently missing trails? → Type-specific pattern.

## Reporting Patterns

Post patterns to board memory with specific tags:

```
fleet_alert(
    category="compliance",
    severity="medium",  # or high if threshold exceeded significantly
    details="Pattern: tasks_without_trail. 6/20 done tasks have <3 trail events. "
            "Affected agents: software-engineer (3), devops (2), architect (1). "
            "Recommendation: reinforce trail recording in next teaching cycle."
)
```

Tags: `[compliance, pattern, immune-signal]`

The Doctor reads these tags. When a pattern is confirmed (appears in 2+ consecutive reports), the Doctor can:
- Flag specific agents for teaching interventions
- Adjust detection sensitivity for that pattern
- Report to PO via board memory

## What Pattern Detection is NOT

- NOT enforcement (Doctor enforces, you detect)
- NOT individual task review (fleet-ops reviews, you aggregate)
- NOT punishment (PO decides consequences, you provide data)

You are the fleet's epidemiologist. You track the spread of process disease. The Doctor treats it.
