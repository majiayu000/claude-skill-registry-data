---
name: solo-project-management
description: Project management adapted for solo developers working without a team. Use for personal project planning, time-boxing work sessions, managing scope creep alone, maintaining momentum on side projects, tracking progress without overhead, making decisions without external input, and staying accountable to yourself.
---

# Solo Project Management

Effective project management patterns for developers working alone.

## Solo vs Team Differences

| Team Pattern | Solo Adaptation |
|--------------|-----------------|
| Sprint planning meetings | Weekly written planning session |
| Daily standups | Daily 2-minute journal entry |
| Code review | Self-review checklist + time delay |
| Stakeholder pressure | Self-imposed deadlines with stakes |
| Team velocity | Personal throughput tracking |
| Blockers escalation | Decision journal + timebox |

## Time Management

### Work Session Structure
```
1. PLAN (5 min): Pick ONE task, define "done"
2. WORK (25-50 min): Focus block, no context switching
3. REVIEW (5 min): Did I finish? What's next?
4. BREAK (5-15 min): Actually step away
```

### Time-Boxing Decisions
Avoid analysis paralysis with strict time limits:
```
Small decision (library choice): 15 minutes max
Medium decision (architecture): 1 hour max
Large decision (tech stack): 1 day max

Rule: When timer ends, go with best current option.
Document rationale, move on. Revisit only if proven wrong.
```

### Weekly Rhythm
```
MONDAY: Plan the week, pick 3 key outcomes
DAILY: Pick today's single most important task
FRIDAY: Review what shipped, celebrate wins, note learnings
WEEKEND: Recharge (protect this boundary)
```

## Scope Discipline

### The Solo Scope Trap
Without external pushback, scope creeps invisibly:
- "While I'm here, I'll also..."
- "This would be better if..."
- "Let me just refactor..."

### Scope Defense Tactics

**1. Write It Down First**
Before starting any unplanned work:
```
SCOPE CHANGE REQUEST (to myself)
What: [The thing I want to add]
Why now: [Why can't this wait?]
Trade-off: [What won't get done instead?]
Decision: [Add / Defer / Drop]
```

**2. The "Later" List**
Keep a parking lot for good ideas that aren't now:
- Capture immediately so you don't forget
- Review weekly—most items lose urgency
- Promotes saying "not now" instead of "no"

**3. MVP Goggles**
Ask constantly: "Is this required for the first working version?"

### Feature Creep Signals
Watch for these warning signs:
- Task taking 3x longer than expected
- Building things "users might want"
- Perfectionism on non-critical paths
- Avoiding the hard/boring essential work

## Progress Tracking

### Minimal Viable Tracking
Track only what changes behavior:
```
# Daily Log (30 seconds)
- Date: 2024-01-15
- Shipped: [What actually got done]
- Blocked: [What stopped progress]
- Tomorrow: [Single priority]
```

### Weekly Review Template
```
## Week of [Date]

### Shipped
- [Completed item 1]
- [Completed item 2]

### Didn't Ship (and why)
- [Item]: [Reason - scope creep? blocked? deprioritized?]

### Learnings
- [What would I do differently?]

### Next Week's Goal
- [ONE main outcome]
```

### Progress Visibility
Make progress tangible to maintain motivation:
- Commit frequently (even WIP)
- Deploy to staging often
- Screenshot/record demos for yourself
- Track streak of consecutive work days

## Decision Making

### Solo Decision Framework
Without a team to consult, structure your thinking:

```
DECISION: [What needs to be decided]
OPTIONS:
  A: [Option] - Pros: / Cons:
  B: [Option] - Pros: / Cons:
CONSTRAINTS: [Time, money, skills, dependencies]
REVERSIBILITY: [Easy/Medium/Hard to change later]
DEFAULT: [What happens if I don't decide?]
DECISION: [Choice + reasoning]
```

### When Stuck
1. **Timebox**: Set 30-minute limit, then decide
2. **Flip a coin**: If you resist the result, you know your preference
3. **Sleep on it**: But only once—decide tomorrow
4. **Build both**: Prototype for 1 hour each, then choose
5. **Ask externally**: Post in community, rubber duck with AI

### Decision Journal
Log significant decisions for future reference:
```
- Date: 2024-01-15
- Decision: Use SQLite instead of Postgres
- Reasoning: Single user, simpler deployment, can migrate later
- Revisit if: Need concurrent writes or >10GB data
```

## Momentum Management

### Starting Strategies
When motivation is low:
- **2-minute rule**: Commit to just 2 minutes of work
- **Smallest step**: What's the tiniest possible progress?
- **Easy win first**: Start with something completable
- **Environment shift**: Change location, time, or setup

### Maintaining Momentum
- End sessions mid-task (easier to resume)
- Leave notes for "future you" about next steps
- Keep the build green (broken = friction)
- Visible progress (kanban board, changelog)

### Recovering from Stalls
When you haven't worked on the project in a while:
1. **Don't judge**: Guilt is not productive
2. **Read your notes**: Rebuild context from docs/commits
3. **Pick smallest task**: Rebuild momentum before ambition
4. **Lower the bar**: Ship something, anything

## Accountability Without a Team

### Self-Accountability Tactics
- **Public commitment**: Tweet/blog your goals
- **Deadline with stakes**: Tell someone, bet money
- **Scheduled reviews**: Calendar recurring check-ins
- **Accountability partner**: Another solo dev for weekly sync

### The "Future You" Test
Before deferring work, ask:
- Will future-me thank present-me?
- Am I creating debt or investing?
- Is this avoidance disguised as pragmatism?

## Avoiding Burnout

### Warning Signs
- Working longer but shipping less
- Dreading the project
- Perfectionism increasing
- Avoiding the "real" work

### Prevention
- Protect non-work time ruthlessly
- Celebrate small wins explicitly
- Vary the type of work (code, design, docs)
- Take real breaks (not "productive" breaks)
- Ship imperfect things—done > perfect
