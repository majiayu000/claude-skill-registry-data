---
name: edu-study-plan
version: 1.0.0
description: Build a personalized study plan with spaced-repetition scheduling toward a deadline and goal.
author: matrixx0070
tags: [education, study-plan, spaced-repetition, scheduling, retention]
capabilities: []
---

## When to use

Use this to turn a goal, a deadline, and available study time into a day-by-day plan that schedules review at expanding intervals so material sticks. Good for exam prep, skill acquisition, and language or fact-heavy learning.

**Not for:** designing course content itself (use edu-curriculum-design), authoring the practice questions (use edu-quiz-builder), or running a live study session (use edu-tutor-session).

## Method

1. Capture constraints. Confirm goal, deadline, weekly hours available, and current level. Decision point: if the material clearly won't fit the hours, say so and propose scope cuts rather than a fantasy schedule.
2. Break the goal into topics. List discrete study units and estimate effort (learn vs. review) for each.
3. Order by priority. Weight by exam weight or importance × current weakness; schedule weak/high-value topics first and earliest.
4. Apply spaced repetition. Schedule each topic's first pass, then reviews at expanding intervals (default 1 day, 3 days, 7 days, 16 days). Decision point: compress intervals if the deadline is near; stretch them if there's slack.
5. Interleave, don't block. Mix topics within a week rather than one topic per week — interleaving beats massed practice for retention.
6. Add retrieval and checkpoints. Every session includes active recall (self-quiz), not rereading; add weekly progress checks to reschedule weak areas.

## Example

Goal: pass a Spanish A2 exam in 4 weeks, 5 hrs/week. Topics: verb conjugation (weak, high weight), vocab (500 words), listening, past tense. Week 1: learn conjugation Mon, first review Tue (+1d), Thu (+3d); vocab in daily 15-min recall batches; listening interleaved Wed/Sat. Reviews expand into weeks 2-3; week 4 is mostly spaced review + full mock exam. Weekly check moves anything under 70% recall to an earlier slot.

## Pitfalls

- Blocking one topic per week (massed practice) instead of interleaving, which feels productive but forgets fast.
- Scheduling rereading instead of active recall — recognition isn't retention.
- Planning more material than the hours allow, so the learner falls behind day one.
- No review passes, so early topics are forgotten by exam day.

## Output format

```
Goal: <...> | Deadline: <date> | Hours/week: <n> | Current level: <...>

Topics (priority-ordered):
| Topic | Weight | Current level | First pass | Review dates |

Weekly schedule:
Week 1:
  Mon: <topic + recall/review> (<min>)
  ...

Retrieval method per session: <self-quiz / practice>
Checkpoints: <weekly review + reschedule rule>
Feasibility note: <fits hours? scope cuts if not>
```
