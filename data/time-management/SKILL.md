---
name: Time Management
description: Strategies for effective time management, prioritization, and sustainable productivity for software developers
---

# Time Management

## Purpose

Master time management through:
- Task prioritization frameworks
- Realistic estimation
- Calendar optimization
- Deadline management
- Work-life balance

## When to Use

Invoke this skill when:
- Planning sprint or week
- Feeling overwhelmed
- Missing deadlines
- Juggling multiple projects
- Balancing work and learning

## Instructions

### Step 1: Capture Everything

Get all tasks out of your head:
1. **Work tasks**: Features, bugs, reviews
2. **Learning**: Tutorials, docs, courses
3. **Maintenance**: Updates, refactoring
4. **Admin**: Emails, meetings, reports
5. **Personal**: Side projects, health, family

### Step 2: Prioritize

Use prioritization framework:
- **Eisenhower Matrix**: Urgent/Important
- **MoSCoW**: Must/Should/Could/Won't
- **Value vs Effort**: Impact per time
- **Dependencies**: What blocks what

### Step 3: Estimate Realistically

Account for:
- Actual coding time (not ideal time)
- Meetings and interruptions (20-30%)
- Testing and debugging (2x coding time)
- Code review cycles
- Unexpected issues (buffer 20%)

### Step 4: Schedule and Protect

Block time for:
- Deep work (most important tasks)
- Meetings (batch when possible)
- Admin (specific time blocks)
- Learning (consistent slots)
- Breaks (non-negotiable)

## Prioritization Frameworks

### 1. Eisenhower Matrix

**Quadrants**:
```
              URGENT           NOT URGENT
         ┌─────────────────┬─────────────────┐
IMPORTANT│  DO FIRST       │  SCHEDULE       │
         │  (Quadrant 1)   │  (Quadrant 2)   │
         │                 │                 │
         │  - P0 bugs      │  - Architecture │
         │  - Deadlines    │  - Learning     │
         │  - Incidents    │  - Refactoring  │
         ├─────────────────┼─────────────────┤
NOT      │  DELEGATE       │  ELIMINATE      │
IMPORTANT│  (Quadrant 3)   │  (Quadrant 4)   │
         │                 │                 │
         │  - Interruptions│  - Busywork     │
         │  - Some meetings│  - Time wasters │
         │  - Some emails  │  - Procrastination│
         └─────────────────┴─────────────────┘
```

**Strategy**:
- **Q1**: Do immediately (minimize these)
- **Q2**: Schedule and protect (maximize these)
- **Q3**: Delegate or batch
- **Q4**: Eliminate ruthlessly

**Example**:
```typescript
interface Task {
  name: string;
  urgent: boolean;
  important: boolean;
}

function categorize(task: Task): string {
  if (task.important && task.urgent) return 'DO FIRST';
  if (task.important && !task.urgent) return 'SCHEDULE';
  if (!task.important && task.urgent) return 'DELEGATE';
  return 'ELIMINATE';
}

const tasks: Task[] = [
  { name: 'Production bug', urgent: true, important: true },      // DO FIRST
  { name: 'System architecture', urgent: false, important: true }, // SCHEDULE
  { name: 'Quick email', urgent: true, important: false },        // DELEGATE
  { name: 'Social media', urgent: false, important: false },      // ELIMINATE
];
```

---

### 2. MoSCoW Method

**Categories**:
```
Must have:     Critical for success
Should have:   Important but not critical
Could have:    Nice to have
Won't have:    Explicitly out of scope
```

**Sprint Planning Example**:
```
MUST HAVE (70% of time):
✅ User authentication
✅ Data persistence
✅ Critical bug fixes

SHOULD HAVE (20% of time):
⚡ Password reset
⚡ Email notifications
⚡ Error logging

COULD HAVE (10% of time):
💡 Profile pictures
💡 Dark mode
💡 Export to CSV

WON'T HAVE (this sprint):
❌ Social login
❌ Advanced analytics
❌ Mobile app
```

**Implementation**:
```typescript
interface Feature {
  name: string;
  priority: 'MUST' | 'SHOULD' | 'COULD' | 'WONT';
  estimate: number; // hours
}

function allocateTime(features: Feature[], totalHours: number) {
  const allocation = {
    MUST: totalHours * 0.7,
    SHOULD: totalHours * 0.2,
    COULD: totalHours * 0.1,
    WONT: 0,
  };

  return features.filter(f =>
    features
      .filter(feat => feat.priority === f.priority)
      .reduce((sum, feat) => sum + feat.estimate, 0) <= allocation[f.priority]
  );
}
```

---

### 3. Value vs Effort Matrix

**Prioritize High Value, Low Effort**:
```
              LOW EFFORT       HIGH EFFORT
         ┌─────────────────┬─────────────────┐
HIGH     │  QUICK WINS     │  MAJOR PROJECTS │
VALUE    │  (Do First)     │  (Plan Carefully)│
         │                 │                 │
         │  - Bug fixes    │  - New features │
         │  - Quick fixes  │  - Refactoring  │
         │  - Small UX     │  - Migration    │
         ├─────────────────┼─────────────────┤
LOW      │  FILL-INS       │  MONEY PITS     │
VALUE    │  (Batch/Later)  │  (Avoid!)       │
         │                 │                 │
         │  - Nice-to-haves│  - Over-eng     │
         │  - Polish       │  - Premature opt│
         │  - Minor tweaks │  - Gold plating │
         └─────────────────┴─────────────────┘
```

**Scoring System**:
```typescript
interface Task {
  name: string;
  value: number;  // 1-10 (impact on users/business)
  effort: number; // 1-10 (time/complexity)
}

function priorityScore(task: Task): number {
  return task.value / task.effort;  // Higher is better
}

const tasks: Task[] = [
  { name: 'Fix login bug', value: 9, effort: 2 },        // Score: 4.5 (DO FIRST)
  { name: 'New feature', value: 8, effort: 8 },          // Score: 1.0 (PLAN)
  { name: 'Update icon', value: 2, effort: 1 },          // Score: 2.0 (FILL-IN)
  { name: 'Rewrite perfect', value: 3, effort: 10 },     // Score: 0.3 (AVOID)
];

tasks.sort((a, b) => priorityScore(b) - priorityScore(a));
```

---

## Time Estimation

### The Planning Fallacy

**Reality Check**:
```
Your estimate:    4 hours
Actual time:      10 hours

Why?
- Didn't account for debugging (2x)
- Unexpected edge cases (+2 hours)
- Meeting interruption (+1 hour)
- Code review changes (+1 hour)
```

### Better Estimation Formula

```typescript
function realEstimate(idealTime: number): number {
  const debugging = idealTime * 1;      // Same as coding time
  const testing = idealTime * 0.5;      // Half coding time
  const review = idealTime * 0.3;       // Review feedback
  const buffer = idealTime * 0.2;       // Unexpected issues

  return idealTime + debugging + testing + review + buffer;
}

// Example:
// Ideal coding time: 4 hours
// Real estimate: 4 + 4 + 2 + 1.2 + 0.8 = 12 hours

console.log(realEstimate(4)); // 12 hours
```

### Three-Point Estimation

```
Optimistic:  Best case scenario
Most Likely: Expected case
Pessimistic: Worst case scenario

Estimate = (Optimistic + 4*MostLikely + Pessimistic) / 6
```

**Example**:
```typescript
interface Estimate {
  optimistic: number;
  mostLikely: number;
  pessimistic: number;
}

function threePointEstimate(est: Estimate): number {
  return (est.optimistic + 4 * est.mostLikely + est.pessimistic) / 6;
}

const featureEstimate: Estimate = {
  optimistic: 4,   // Everything goes perfectly
  mostLikely: 8,   // Normal development
  pessimistic: 16, // Everything breaks
};

console.log(threePointEstimate(featureEstimate)); // 8.67 hours
```

---

## Calendar Optimization

### Ideal Week Template

```
MONDAY
08:00-08:30  Review week plan
08:30-12:00  Deep Work (no meetings)
12:00-13:00  Lunch
13:00-15:00  Meetings/Collaboration
15:00-17:00  Coding/Reviews
17:00-17:30  Daily review

TUESDAY
08:00-08:30  Daily standup
08:30-12:00  Deep Work (feature development)
12:00-13:00  Lunch
13:00-15:00  Deep Work (continued)
15:00-16:30  Code reviews
16:30-17:30  Learning time

WEDNESDAY
08:00-08:30  Planning
08:30-12:00  Deep Work (complex problems)
12:00-13:00  Lunch
13:00-14:00  1-on-1s
14:00-17:00  Collaboration time
17:00-17:30  Catch up

THURSDAY
08:00-08:30  Review progress
08:30-12:00  Deep Work (implementation)
12:00-13:00  Lunch
13:00-15:00  Testing/QA
15:00-17:00  Bug fixes
17:00-17:30  Documentation

FRIDAY
08:00-08:30  Week review
08:30-11:00  Wrap up week's work
11:00-12:00  Team sync
12:00-13:00  Lunch
13:00-15:00  Learning/Experimentation
15:00-17:00  Planning next week
17:00-17:30  Weekly reflection
```

### Meeting Strategies

**Minimize Meeting Time**:
```
❌ Don't:
- Accept all meeting invites
- Have meetings without agenda
- Let meetings run over time
- Schedule meetings in deep work blocks

✅ Do:
- Decline non-essential meetings
- Require agendas or decline
- End meetings early if done
- Batch meetings (e.g., Tuesday/Thursday afternoons)
- Use async communication when possible
```

**Meeting Batching**:
```
Instead of:
  Monday: 10am, 2pm
  Tuesday: 11am, 3pm
  Wednesday: 9am, 4pm

Do this:
  Tuesday: 1pm-5pm (all meetings)
  Thursday: 1pm-5pm (all meetings)
  Other days: Deep work protected
```

---

## Weekly Planning

### Sunday/Monday Planning Ritual

```
1. REVIEW LAST WEEK (20 min)
   - What got done?
   - What didn't? Why?
   - What lessons learned?

2. BRAIN DUMP (15 min)
   - All tasks, ideas, commitments
   - Personal and professional
   - Big and small

3. PRIORITIZE (20 min)
   - Apply Eisenhower Matrix
   - Identify must-haves for week
   - Defer/delegate rest

4. SCHEDULE (25 min)
   - Block deep work time
   - Schedule specific tasks
   - Add buffer time (20%)
   - Plan breaks and self-care

5. PREPARE (10 min)
   - Set up workspace
   - Prepare materials
   - Clear distractions
   - Mental preparation
```

**Template**:
```markdown
# Week of [Date]

## Top 3 Goals
1. [ ] Ship feature X
2. [ ] Fix P0 bugs
3. [ ] Complete code reviews

## Must Complete
- [ ] Task 1 (8 hours)
- [ ] Task 2 (4 hours)
- [ ] Task 3 (6 hours)

## Should Complete
- [ ] Task 4 (3 hours)
- [ ] Task 5 (2 hours)

## Could Complete
- [ ] Task 6 (2 hours)

## Time Allocation
- Deep Work: 20 hours
- Meetings: 8 hours
- Code Review: 6 hours
- Admin: 4 hours
- Learning: 2 hours
- Buffer: 4 hours

Total: 44 hours (4-day week with buffer)
```

---

## Daily Planning

### Morning Ritual (15 min)

```
1. Review calendar (2 min)
   - What meetings today?
   - When are deep work blocks?

2. Choose 3 Most Important Tasks (5 min)
   - What MUST get done today?
   - What would make today successful?

3. Time block the day (5 min)
   - Assign tasks to time blocks
   - Include breaks

4. Prepare environment (3 min)
   - Close unnecessary tabs
   - Gather resources
   - Set DND/focus mode
```

**Template**:
```markdown
# [Date]

## Top 3 for Today
1. [ ] Finish authentication feature (3 hrs)
2. [ ] Review Sarah's PR (1 hr)
3. [ ] Fix login bug (2 hrs)

## Time Blocks
08:30-11:30  Authentication feature
11:30-12:00  Break
12:00-13:00  Lunch
13:00-14:00  PR review
14:00-16:00  Bug fix
16:00-17:00  Meetings
17:00-17:30  Tomorrow prep
```

### Evening Review (10 min)

```
1. What got done? (2 min)
   ✅ Completed tasks
   📝 Notes on what went well

2. What didn't? Why? (3 min)
   ❌ Incomplete tasks
   🔍 Blockers or reasons
   ➡️  Move to tomorrow or backlog

3. Prep tomorrow (5 min)
   📋 Top 3 for tomorrow
   📅 Review calendar
   🧹 Clear workspace
```

---

## Dealing with Interruptions

### Async-First Communication

```
SYNCHRONOUS (use sparingly):
- P0 production issues
- Time-sensitive decisions
- Complex discussions needing dialogue
- Brainstorming sessions

ASYNCHRONOUS (default):
- Questions (use Slack/email)
- Code reviews (use GitHub)
- Updates (use project management tool)
- Documentation (write it down)
```

### Interrupt Protocol

```typescript
enum InterruptPriority {
  EMERGENCY,   // Handle immediately
  URGENT,      // Handle within 1 hour
  IMPORTANT,   // Handle today
  NORMAL,      // Handle this week
  LOW,         // Backlog
}

function handleInterrupt(priority: InterruptPriority): string {
  switch (priority) {
    case InterruptPriority.EMERGENCY:
      return 'Stop current work immediately';
    case InterruptPriority.URGENT:
      return 'Finish current pomodoro, then handle';
    case InterruptPriority.IMPORTANT:
      return 'Add to today\'s task list';
    case InterruptPriority.NORMAL:
      return 'Add to this week\'s backlog';
    case InterruptPriority.LOW:
      return 'Add to general backlog';
  }
}
```

**Communicate Availability**:
```
Slack Status:
🎯 Deep Work (until 12pm) - Emergency only
💻 Available for questions
🍽️  Lunch (back at 1pm)
📅 In meeting
🏠 Done for the day
```

---

## Work-Life Balance

### Sustainable Pace

```
❌ Unsustainable:
- 60+ hour weeks
- No breaks
- Weekend work
- Always available
- Skipping vacation

✅ Sustainable:
- 40-45 hour weeks
- Regular breaks
- Weekends off
- Clear boundaries
- Regular time off
```

### Energy Management

```
Daily Energy Budget:
- Deep Work: 4-6 hours (max)
- Meetings: 2-4 hours
- Admin: 1-2 hours
- Breaks: 1-2 hours

Don't exceed your budget!
```

### Hard Stops

```
- End work at reasonable time
- No email after hours
- Weekend completely off
- Vacation = actually disconnected
- Sick = actually rest
```

---

## Measuring Progress

### Weekly Metrics

```typescript
interface WeeklyMetrics {
  plannedTasks: number;
  completedTasks: number;
  deepWorkHours: number;
  meetingHours: number;
  interruptionCount: number;
  focusQuality: number; // 1-10
}

function calculateEfficiency(metrics: WeeklyMetrics): number {
  return (metrics.completedTasks / metrics.plannedTasks) * 100;
}

function assessBalance(metrics: WeeklyMetrics): string {
  const ratio = metrics.deepWorkHours / metrics.meetingHours;

  if (ratio > 2) return 'Great balance!';
  if (ratio > 1) return 'Good balance';
  if (ratio > 0.5) return 'Too many meetings';
  return 'Meeting overload! Block more focus time';
}
```

---

## Output Format

```
## Time Management Plan: ${Period}

**Goals**: ${topGoals}

**Priority Tasks**:
1. ${task1} (${estimate1})
2. ${task2} (${estimate2})

**Time Allocation**:
- Deep Work: ${hours}
- Meetings: ${hours}
- Admin: ${hours}

**Success Criteria**:
- ${criteria1}
- ${criteria2}
```

## Related Skills

- `focus-techniques`: For deep work execution
- `task-breakdown`: For estimating complex work
- `energy-optimization`: For peak performance
- `habit-building`: For consistency
