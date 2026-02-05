---
name: Weekly Review
description: Conduct User's weekly review when he says "weekly review", "week in review", or "end of week review". Synthesizes the week's progress, analyzes what worked/didn't, updates project priorities, and plans the next week.
---

# Weekly Review

Facilitate User's end-of-week reflection and planning session to maintain momentum and course-correct.

## When to Use This Skill

Auto-invoke when User says any of:
- "weekly review"
- "week in review"
- "end of week review"
- "weekly retrospective"
- "review this week"

## Review Structure

### Part 1: Week Retrospective (Looking Back)

**1. Achievements & Wins**
- Read daily notes from `reflections/daily/` for the week
- Identify completed tasks, shipped features, milestones reached
- Celebrate wins (even small ones)

**2. Time Allocation Analysis**
- How was time actually spent vs planned?
- Did Primary project get 40-50% of project time?
- Did art practice happen 3-4x as intended?
- Where did unexpected time go?

**3. What Worked Well**
- Systems/processes that helped
- Decisions that paid off
- Energy management wins
- Good days (what made them good?)

**4. What Didn't Work**
- Blockers that emerged
- Distractions or time sinks
- Energy drains
- Commitments that didn't serve goals

**5. Learnings & Insights**
- Technical learnings
- Process improvements discovered
- Personal insights about working style
- Patterns noticed

### Part 2: Project Review (Current State)

**Invoke Project Health Check skill** to get:
- Status of all projects
- Blockers identified
- Velocity assessment
- Priority alignment check

**Additional considerations:**
- Should any project priority change?
- Should any project be paused?
- Are new opportunities worth pursuing?
- Is scope creep happening?

### Part 3: Domain Check-Ins

Quick pulse check across key life domains:

**Career (Strategist):**
- Progress on career goals?
- Relationships built/maintained?
- Skills developed?

**Wealth (Banker):**
- Financial progress this week?
- Side project revenue movement?
- Investment actions taken?

**Health (Spartan):**
- Fitness consistency?
- Sleep quality?
- Energy levels?

**Art (Artist):**
- Practice sessions completed?
- Skill progress noticed?
- NMA curriculum advancement?

**Operations (Atlas):**
- System health?
- Balance maintained?
- Burnout risk?

### Part 4: Next Week Planning (Looking Forward)

**1. Project Priorities**
- Confirm Primary/Secondary/Maintenance focus
- Adjust if needed based on health check
- Set specific milestones for the week

**2. Calendar Planning**
- Block deep work time for Primary project
- Schedule art practice sessions
- Identify high-meeting days (protect energy)
- Plan YourPet care around work schedule

**3. Top 3 Priorities for Week**
- What MUST ship/progress?
- What would make next week a win?
- What blockers must be cleared?

**4. Commitments & Constraints**
- Any special events or travel?
- Deadlines approaching?
- Energy reserves (coming off busy week)?

**5. One Thing to Improve**
- Based on "what didn't work" - pick ONE
- Specific experiment to try
- How to measure if it worked?

## Output Format

Save to: `reflections/weekly/YYYY-MM-DD.md`

```markdown
# Weekly Review - Week [N], [DATE RANGE]

## 📊 Week Overview

**Theme:** [One word/phrase capturing the week]
**Overall Rating:** [1-10]
**Energy Level:** [High/Medium/Low]

---

## 🎉 Wins & Achievements

### Projects
- ✅ [Specific achievement - project name]
- ✅ [Specific achievement - project name]

### Art Practice
- 🎨 [Sessions completed, skills practiced]

### Career/Growth
- 📈 [Professional wins]

### Personal
- 🌱 [Life/health/relationship wins]

---

## ⏱️ Time Allocation

**Planned vs Actual:**
- **Primary Project:** Planned X hrs → Actual Y hrs
- **Secondary Project:** Planned X hrs → Actual Y hrs
- **Art Practice:** Planned X hrs → Actual Y hrs
- **Work:** 40 hrs
- **YourPet:** ~7 hrs

**Assessment:** [On track / Overcommitted / Need adjustment]

---

## ✅ What Worked Well

1. [System/process that helped]
2. [Decision that paid off]
3. [Energy management win]

**Why it worked:** [Brief analysis]
**Continue:** [How to maintain this]

---

## ❌ What Didn't Work

1. [Blocker or distraction]
2. [Time sink or energy drain]
3. [Commitment that didn't serve]

**Why it didn't work:** [Brief analysis]
**Adjust:** [How to avoid/improve]

---

## 💡 Learnings & Insights

**Technical:**
- [New skills or knowledge gained]

**Process:**
- [Improvements discovered]

**Personal:**
- [Insights about working style, energy, etc.]

---

## 📊 Project Health

[Paste or reference Project Health Check output]

**Priority Changes:**
- [Any adjustments to project priorities]

**Projects to Pause:**
- [Any projects to put on hold]

**New Opportunities:**
- [Anything new worth considering]

---

## 🎯 Domain Check-Ins

### 💼 Career (Strategist)
**Progress:** [Status]
**Actions Taken:** [What was done]
**Next Week:** [Focus area]

### 💰 Wealth (Banker)
**Financial Progress:** [Status]
**Actions Taken:** [Investments, side project revenue]
**Next Week:** [Focus area]

### 🪖 Health (Spartan)
**Fitness:** [Workouts completed, consistency]
**Sleep:** [Quality, average hours]
**Energy:** [Overall assessment]
**Next Week:** [Focus area]

### 🎨 Art (Artist)
**Sessions:** [X of 3-4 target]
**Focus:** [What was practiced]
**Progress:** [Skills developing]
**Next Week:** [Practice focus]

### ⚡ Operations (Atlas)
**System Health:** [How are systems holding up]
**Balance:** [Life balance assessment]
**Burnout Risk:** [Low/Medium/High]
**Next Week:** [Adjustment needed]

---

## 📅 Next Week Planning

### Week [N+1] - [DATE RANGE]

**Primary Focus:** [Main project and milestone]
**Secondary Focus:** [Secondary project goal]
**Maintenance:** [What needs minimal attention]

**Top 3 Priorities:**
1. 🔴 [P0 - must ship/complete]
2. 🟠 [P1 - important progress]
3. 🟡 [P2 - meaningful but flexible]

**Calendar Notes:**
- [Deep work blocks scheduled]
- [High-meeting days to prepare for]
- [Art practice sessions blocked]
- [Special events or constraints]

**One Thing to Improve:**
- **Experiment:** [Specific thing to try differently]
- **Success metric:** [How to know if it worked]

---

## 🧠 Reflections

[Open-ended thoughts, patterns noticed, bigger-picture thinking]

---

*Generated by Weekly Review skill*
*Next review: [Date]*
```

## Implementation Approach

1. **Gather data:**
   - Read daily notes from `reflections/daily/` for past 7 days
   - Read `projects/INDEX.md` for current project state
   - Invoke Project Health Check skill for detailed analysis
   - Check for weekly calendar if available

2. **Analyze patterns:**
   - Look for completed tasks in daily notes
   - Identify blockers mentioned multiple times
   - Notice energy patterns (which days were productive?)
   - Spot time allocation trends

3. **Synthesize:**
   - Honest assessment (no forced positivity)
   - Specific examples (not generic)
   - Actionable insights (not just observations)
   - Connected to long-term goals

4. **Plan forward:**
   - Based on actual capacity (not ideal)
   - Adjust for lessons learned
   - One focused experiment (not five resolutions)

## Context Files to Reference

- `reflections/daily/*.md` (past 7 days) - Daily notes and task completion
- `projects/INDEX.md` - Project status and priorities
- `.system/context/preferences.md` - Time allocation philosophy and goals
- Previous weekly reviews in `reflections/weekly/` - Track progress over time

## Integration with Other Skills

- **Auto-invoke Project Health Check** as part of review
- **May lead to Cabinet Meeting** if major decisions needed
- **Informs Morning Brief** for upcoming week

## Tone

- Reflective but action-oriented
- Honest about what didn't work
- Celebrates wins without inflation
- Strategic and connected to long-term vision
- Pragmatic about capacity and constraints
- Growth-minded (everything is data)

## Best Practices

**Do:**
- Use actual data from daily notes
- Be specific about achievements and failures
- Connect insights to long-term goals
- Recommend one focused improvement
- Acknowledge energy and capacity

**Don't:**
- Force positivity if week was hard
- Make vague observations
- Suggest five new habits to try
- Ignore patterns or recurring issues
- Recommend more than User can handle
