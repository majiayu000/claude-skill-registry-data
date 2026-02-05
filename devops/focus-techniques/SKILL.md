---
name: Focus Techniques
description: Science-backed techniques for maintaining deep focus, managing distractions, and maximizing productive coding sessions
---

# Focus Techniques

## Purpose

Help developers achieve and maintain deep focus through:
- Proven focus techniques
- Distraction management strategies
- Energy optimization
- Flow state cultivation
- Sustainable productivity habits

## When to Use

Invoke this skill when:
- Starting a coding session
- Struggling with distractions
- Experiencing mental fatigue
- Planning deep work sessions
- Optimizing productivity workflow

## Instructions

### Step 1: Assess Current State

Evaluate:
1. **Energy Level**: High, Medium, Low
2. **Distractions**: Number and severity
3. **Task Complexity**: Simple, Moderate, Complex
4. **Time Available**: Short (<1hr), Medium (1-3hrs), Long (>3hrs)

### Step 2: Choose Appropriate Technique

Select based on context:
- **Pomodoro**: For sustained focus with breaks
- **Time Blocking**: For structured days
- **Deep Work**: For complex problems
- **Batch Processing**: For similar tasks
- **Flow State**: For creative work

### Step 3: Prepare Environment

Optimize for focus:
1. Eliminate physical distractions
2. Close unnecessary apps/tabs
3. Set communication boundaries
4. Prepare water/snacks
5. Ensure comfortable workspace

### Step 4: Execute and Monitor

During session:
1. Start timer/tracker
2. Single-task (no context switching)
3. Take scheduled breaks
4. Monitor energy levels
5. Adjust as needed

## Focus Techniques

### 1. Pomodoro Technique

**Best for**: General coding, learning, documentation

**Method**:
```
1. Choose a task
2. Set timer for 25 minutes
3. Work with full focus (no distractions)
4. Take 5-minute break
5. After 4 pomodoros, take 15-30 minute break
```

**Implementation**:
```typescript
// Pomodoro Timer
const WORK_DURATION = 25 * 60 * 1000; // 25 minutes
const SHORT_BREAK = 5 * 60 * 1000;    // 5 minutes
const LONG_BREAK = 30 * 60 * 1000;    // 30 minutes

class PomodoroTimer {
  private pomodorosCompleted = 0;

  async startWorkSession(): Promise<void> {
    console.log('🍅 Pomodoro started - Focus for 25 minutes');
    await this.timer(WORK_DURATION);
    this.pomodorosCompleted++;

    if (this.pomodorosCompleted % 4 === 0) {
      console.log('🎉 4 pomodoros done! Take a 30-minute break');
      await this.timer(LONG_BREAK);
    } else {
      console.log('✅ Pomodoro complete! Take a 5-minute break');
      await this.timer(SHORT_BREAK);
    }
  }

  private timer(duration: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, duration));
  }
}
```

**Tips**:
- No interruptions during the 25 minutes
- If distracted, restart the pomodoro
- Track number of pomodoros per task
- Adjust duration if needed (20-50 minutes)

**Best Use Cases**:
✅ Learning new concepts
✅ Writing documentation
✅ Code review
✅ Bug fixing
✅ Refactoring

---

### 2. Time Blocking

**Best for**: Full-day planning, multiple projects

**Method**:
```
1. Plan day in advance
2. Assign specific time blocks to tasks
3. Include buffer time (10-15%)
4. Schedule breaks and deep work
5. Protect blocked time fiercely
```

**Example Schedule**:
```
08:00-08:30  Morning review & planning
08:30-10:30  Deep Work: Feature implementation
10:30-10:45  Break
10:45-12:00  Code review & PR feedback
12:00-13:00  Lunch
13:00-15:00  Deep Work: Complex algorithm
15:00-15:15  Break
15:15-16:30  Meetings & collaboration
16:30-17:00  Email, Slack, admin tasks
17:00-17:30  End-of-day review & tomorrow planning
```

**Implementation**:
```typescript
interface TimeBlock {
  start: string;
  end: string;
  task: string;
  type: 'deep-work' | 'meeting' | 'break' | 'admin';
}

const dailySchedule: TimeBlock[] = [
  { start: '08:30', end: '10:30', task: 'Feature implementation', type: 'deep-work' },
  { start: '10:30', end: '10:45', task: 'Break', type: 'break' },
  { start: '10:45', end: '12:00', task: 'Code review', type: 'admin' },
];

function getCurrentTask(schedule: TimeBlock[]): TimeBlock | null {
  const now = new Date();
  const currentTime = `${now.getHours()}:${now.getMinutes()}`;

  return schedule.find(block =>
    block.start <= currentTime && block.end > currentTime
  ) || null;
}
```

**Tips**:
- Block your best hours for deep work (usually morning)
- Batch similar tasks together
- Include buffer time between blocks
- Protect deep work blocks - no meetings
- Review and adjust weekly

---

### 3. Deep Work Sessions

**Best for**: Complex problems, architecture design, learning

**Method**:
```
1. Schedule 2-4 hour uninterrupted blocks
2. Eliminate ALL distractions
3. Single complex task only
4. No context switching
5. Full cognitive engagement
```

**Pre-Session Checklist**:
- [ ] Phone on Do Not Disturb
- [ ] Slack/Email closed
- [ ] Calendar blocked
- [ ] Task clearly defined
- [ ] All resources ready
- [ ] Water/coffee prepared
- [ ] Bathroom break taken

**During Session**:
```
Hour 1: Warm-up, context loading
Hour 2: Peak productivity
Hour 3: Maintain momentum
Hour 4: Wrap up, document progress
```

**Tips**:
- Build up to 4-hour sessions gradually
- Start with 90-minute blocks
- Take real breaks (not social media)
- Track what you accomplished
- Don't schedule back-to-back deep work

**Best Use Cases**:
✅ System architecture design
✅ Complex algorithm implementation
✅ Learning new framework deeply
✅ Major refactoring
✅ Performance optimization

---

### 4. The Two-Minute Rule

**Best for**: Small tasks, preventing task accumulation

**Method**:
```
If a task takes less than 2 minutes, do it immediately
Don't add it to your todo list
```

**Examples**:
- Reply to quick message
- Fix obvious typo
- Update documentation
- Merge approved PR
- Close resolved issue

**Implementation**:
```typescript
function handleTask(task: Task): void {
  if (task.estimatedTime <= 2) {
    // Do it now
    executeTask(task);
  } else {
    // Schedule it
    addToBacklog(task);
  }
}
```

**Tips**:
- Be honest about time estimates
- Don't let it interrupt deep work
- Batch during admin time blocks
- Track to avoid scope creep

---

### 5. Batch Processing

**Best for**: Similar tasks, administrative work

**Method**:
```
1. Group similar tasks together
2. Schedule specific time for batch
3. Process all at once
4. Minimize context switching
```

**Batchable Tasks**:
- Email responses
- Code reviews
- Documentation updates
- Dependency updates
- Bug triage
- Meeting notes review

**Schedule Example**:
```
Monday 4-5pm:     Email & Slack
Tuesday 2-3pm:    Code reviews
Wednesday 4-5pm:  Documentation
Thursday 2-3pm:   Bug triage
Friday 3-5pm:     Weekly review & planning
```

**Tips**:
- Don't check email continuously
- Set expectations (reply within 24hrs)
- Use templates for common responses
- Limit batch duration (max 2 hours)

---

### 6. Flow State Optimization

**Best for**: Creative work, complex problem-solving

**Prerequisites for Flow**:
1. **Clear goals**: Know exactly what you're doing
2. **Immediate feedback**: See results quickly
3. **Challenge/skill balance**: Not too hard, not too easy
4. **No distractions**: Complete focus possible

**How to Enter Flow**:
```
1. Choose challenging but achievable task
2. Set clear, specific goal
3. Eliminate all distractions
4. Start with warm-up coding
5. Increase difficulty gradually
6. Maintain for 90-120 minutes
7. Take break before burnout
```

**Flow State Indicators**:
- Time seems to fly
- Complete absorption
- Effortless concentration
- Losing sense of self-consciousness
- Feeling in control

**Tips**:
- Protect flow time (no meetings)
- Use same environment/music
- Build a flow ritual
- Don't force it when tired
- Track when you achieve flow

---

## Distraction Management

### Digital Distractions

**Eliminate**:
```bash
# macOS: Block distracting sites
sudo echo "127.0.0.1 facebook.com" >> /etc/hosts
sudo echo "127.0.0.1 twitter.com" >> /etc/hosts
sudo echo "127.0.0.1 reddit.com" >> /etc/hosts

# Use browser extensions:
# - Freedom (block sites/apps)
# - Cold Turkey (distraction blocker)
# - RescueTime (track time)
```

**Communication Boundaries**:
```
Slack: Status "🎯 Deep Work - Back at 2pm"
Email: Auto-responder "Checking email at 12pm and 4pm"
Phone: Do Not Disturb mode
Calendar: Block as "Focus Time"
```

### Physical Environment

**Optimize**:
- Clean desk (no clutter)
- Good lighting (natural if possible)
- Comfortable temperature (68-72°F)
- Noise management (headphones, white noise)
- Ergonomic setup (prevent discomfort)

**Focus Music**:
- Instrumental music
- Lo-fi beats
- Nature sounds
- Binaural beats
- Silence (sometimes best)

---

## Energy Management

### Peak Performance Times

**Identify Your Peak**:
```
Morning person: 8am-12pm (deep work here)
Evening person: 2pm-6pm (deep work here)

Track for 2 weeks:
- When do you feel most alert?
- When do complex problems feel easier?
- When do you get into flow?
```

**Match Tasks to Energy**:
```
High Energy:
  - Complex problem-solving
  - Architecture design
  - Learning new concepts

Medium Energy:
  - Code review
  - Refactoring
  - Documentation

Low Energy:
  - Email responses
  - Meeting notes
  - Administrative tasks
```

### Break Strategies

**Micro Breaks** (every 30 min):
```
- 30 seconds: Look away from screen (20-20-20 rule)
- Stand up and stretch
- Deep breathing (5 breaths)
```

**Short Breaks** (every 90-120 min):
```
- 5-10 minutes
- Walk around
- Hydrate
- Quick snack
- Step outside
```

**Long Breaks** (every 4 hours):
```
- 30-60 minutes
- Real meal
- Exercise
- Nature walk
- Power nap (20 min)
```

---

## Measuring Focus

### Track Metrics

```typescript
interface FocusSession {
  date: Date;
  duration: number;  // minutes
  task: string;
  quality: 1 | 2 | 3 | 4 | 5;  // subjective rating
  distractions: number;
  output: string;  // what you completed
}

// Weekly analysis
function analyzeFocusQuality(sessions: FocusSession[]): {
  averageQuality: number;
  totalFocusTime: number;
  bestTimeOfDay: string;
  distractionsPerSession: number;
} {
  // Analyze patterns
}
```

### Indicators of Good Focus

✅ Completed planned tasks
✅ Few distractions (< 3 per hour)
✅ Time flew by
✅ Quality output
✅ Felt energized, not drained
✅ Clear progress made

### Indicators of Poor Focus

❌ Frequent task switching
❌ Checking phone/email repeatedly
❌ Time dragging
❌ Low quality work
❌ Exhaustion without progress
❌ Procrastination

---

## Quick Reference

### Starting a Focus Session

```
1. [ ] Clear goal defined
2. [ ] Timer set
3. [ ] Distractions eliminated
4. [ ] Water/coffee ready
5. [ ] Bathroom break taken
6. [ ] Phone on DND
7. [ ] Communication boundaries set
```

### Best Technique for Each Scenario

| Scenario | Best Technique |
|----------|----------------|
| Bug fixing | Pomodoro (25 min) |
| New feature | Deep Work (2-4 hrs) |
| Learning | Pomodoro + Note-taking |
| Code review | Batch Processing |
| Complex algorithm | Deep Work + Flow |
| Documentation | Time Blocking |
| Admin tasks | Batch Processing |
| Design/Architecture | Deep Work |

---

## Output Format

When providing focus guidance:

```
## Focus Plan: ${Task}

**Recommended Technique**: ${technique}

**Duration**: ${duration}

**Preparation**:
- ${prep1}
- ${prep2}

**During Session**:
1. ${step1}
2. ${step2}

**Success Criteria**:
- ${criteria1}
- ${criteria2}
```

## Related Skills

- `time-management`: For daily/weekly planning
- `task-breakdown`: For complex tasks
- `energy-optimization`: For peak performance
- `habit-building`: For consistency
