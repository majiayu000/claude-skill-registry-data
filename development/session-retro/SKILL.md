---
name: session-retro
description: |
  Session retrospective. Runs after a workflow, coding session, or multi-step task
  completes. Analyzes what shipped, what failed, patterns observed, and growth
  opportunities. Generates a retro summary with per-step breakdowns, shipping streaks,
  and test health trends. Use after any significant session (>3 steps or >15 min).
  Proactively suggest when the user finishes a workflow, completes a feature,
  or says "let's review what we did." Also supports global retro across all projects.
---

# Session Retrospective

You are an **engineering manager running a retro**. Your job is to extract lessons
from what just happened — what worked, what broke, what patterns emerged — so the
next session is better. This is not a performance review; it's a learning system.

**HARD GATE:** Do NOT modify code, fix bugs, or take any action during the retro.
Your only output is analysis and logged learnings.

---

## When to Use

Proactively invoke when:
- A workflow run completes (any status: completed, failed, cancelled)
- A multi-step session ends (>3 steps or >15 minutes)
- User says "what did we just do?" or "how did that go?"
- End of day/week wrap-up
- After a particularly challenging debugging session
- **Global mode:** User says "retro everything" or "retro global" — cross-project analysis

---

## Step 0: Gather Session Data

```bash
# Gather recent session context
BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
echo "Branch: $BRANCH"
echo "Recent commits:"
git log --oneline -10 2>/dev/null || echo "(no git history)"

# Check for workflow run data
echo "Workflow runs today:"
find ~/.gstack/projects -name "*.jsonl" -mtime -1 2>/dev/null | head -5 || echo "(no gstack data)"
```

Also gather:
- Which skills ran during this session (from conversation context)
- Duration of the session
- User's stated goal at session start vs what shipped
- Any errors, retries, or pivots

---

## Step 1: Per-Step Breakdown

For each step/phase of the session, produce:

```
STEP: <name>
Status: PASSED / FAILED / SKIPPED / PARTIAL
Duration: <time>
What happened: <1-2 sentence summary>
Surprise factors: <anything unexpected>
Pattern match: <does this mirror a past session?>
```

If a step failed:
- What was the root cause?
- Was it caught early or late?
- Could a review/qa step have caught it?

---

## Step 2: Pattern Analysis

Look across ALL steps for patterns:

**Strengths:**
- What decisions proved correct?
- What workflow patterns worked well?
- What tools/skills delivered consistent value?

**Weaknesses:**
- What caused rework or backtracking?
- What assumptions were wrong?
- Where did the agent or user get stuck?

**Surprises:**
- What happened that neither user nor agent anticipated?
- What edge cases emerged that the plan didn't cover?
- What did the user discover they actually wanted?

---

## Step 3: Metrics

If available, compute:

| Metric | Value |
|--------|-------|
| Steps attempted | N |
| Steps passed | N |
| Steps failed | N |
| Rework loops (>1 fix for same issue) | N |
| Decisions made via user approval | N |
| Pivots (direction changes) | N |
| Total session duration | X min |
| Shippable output | Y files / Z lines |

If this is a recurring project, compare against previous sessions:
- Shipping streak: N consecutive sessions with shippable output
- Test health: tests added vs tests failing
- Velocity trend: steps per session over time

---

## Step 4: Growth Opportunities

Identify 2-3 concrete improvements:

1. **Process change:** What should we do differently next time?
   - Example: "Run ceo-scope-review before implementing — we spent 40% of time on scope discussion mid-execution"

2. **Skill gap:** What skill would have saved time or improved quality?
   - Example: "A pre-flight-review would have caught the missing auth check before deployment"

3. **Learning to log:** What should the learnings-keeper remember for next session?
   - Example: "This project's error handling pattern: always wrap API calls in try/catch with user-facing messages"

---

## Step 5: Output Format

```
SESSION RETROSPECTIVE
══════════════════════
Project: <project name>
Branch: <branch>
Date: <date>
Duration: <time>

## What shipped
- <item 1>
- <item 2>

## What didn't
- <item> — blocked by <reason>
- <item> — deferred by user

## Per-step breakdown
[Step-by-step table from Step 1]

## Patterns observed
✅ <strength>
✅ <strength>
⚠ <weakness>
⚠ <weakness>
💡 <surprise>

## Metrics
[Metrics table from Step 3]

## Growth opportunities
1. <improvement>
2. <improvement>
3. <learning to log>

## Overall
<1-sentence verdict on session health>
```

---

## Global Retro Mode

When user says "retro global" or "retro everything":

1. Gather data from all projects worked on today/this week
2. Find cross-project patterns
3. Report: which projects are healthy, which are stalled, where time went
4. One recommendation per project

```
GLOBAL RETRO — Week of <date>
══════════════════════════════
Projects worked: N
Total sessions: N
Total shippable output: N files

Project A: ✅ 3 sessions, 2 shipped, 1 in progress
  Pattern: consistent velocity, no rework

Project B: ⚠ 2 sessions, 0 shipped, 2 blocked
  Pattern: scope creep, needs ceo-scope-review
```

---

## Learnings Integration

After the retro, automatically log:
- Top 3 patterns to the learnings-keeper
- User preferences discovered during the session
- Any "never do this again" lessons

This makes retros compound — each one feeds the next.

---

## Key Principles

- **Blame nothing, learn everything.** The retro is about the system, not the person.
- **Be specific.** "We should test more" is useless. "The auth flow had no test for
  expired tokens, which caused the P1 bug" is actionable.
- **Compound across sessions.** The learnings system makes each retro build on
  previous ones. The agent should get noticeably smarter over time.
- **Celebrate what shipped.** Even a partial ship is progress. Name what moved forward.
