---
name: spaced-repetition
description: Use when scheduling and executing review sessions at scientifically-calibrated expanding intervals for long-term retention.
version: 1.1.0
authors:
  - edu-agent-skills contributors
tags: [productivity, spaced-repetition, retention, scheduling]
status: stable
---

# Purpose

Schedule review of previously-learned concepts at expanding intervals to exploit the spacing effect. Manages due dates, adjusts intervals based on recall quality, and surfaces overdue items before they decay.

# Activation

- Review session is due based on schedule. Learner initiates review. `flashcards` deck has due items. Sustained learning track (3+ sessions) needing interval maintenance.
- **Skip if**: one-shot session with no continuity. Concept not yet learned. Learner declines scheduling.
- **Routing**: overdue items take priority at session start. Coordinate with `flashcards` for card-level scheduling. Feed interval data to `learning-memory`.

# Inputs

- Flashcard/item schedule with due dates, learner's current session, items from `learning-memory`.

# Interval Algorithm (Simplified SM2)

Each item has an **interval** (days) and **ease factor** (EF, 1.3–2.5). Initial: 1 day → 3 days → then formula.

| Score | Label | Interval Rule | EF Change |
|---|---|---|---|
| 0 | Failed | Reset to 1 day | EF -= 0.2 (min 1.3) |
| 1 | Hard | Stay at current | EF -= 0.1 |
| 2 | Good | Interval × EF | No change |
| 3 | Easy | Interval × EF × 1.3 | EF += 0.1 (max 2.5) |

Mastery threshold: EF > 2.4, interval > 60 days, 5 consecutive successes → archive.

# Workflow

1. **Detect Due Items** — Check `next_review ≤ today`. Sort by overdue duration (most overdue first). Report count.
2. **Scope Session** — ≤10 due: review all. >10: prioritize by overdue + weak-area overlap, cap at 15. Report deferrals.
3. **Execute Review** — Present front, wait for learner response, reveal back. Self-score: Failed/Hard/Good/Easy. Compute new interval immediately. Never reveal answer before attempt.
4. **Handle Failures** — Score 0: reset to 1 day, re-test at end of current session. Failed 3 sessions in a row: flag for `misconception-detector`.
5. **Update Schedule** — Output updated schedule. Show items due in next 7 days. Warn about upcoming review spikes.
6. **Onboard New Items** — Fresh concept → add at interval=1 day. Confirm concept is understood first (not still unclear).

# Rules

- DO: never reveal the answer before learner attempts.
- DO: coach learners on what "Good" vs "Easy" means for self-scoring calibration.
- DO: stagger new item additions to prevent review spikes.
- DO: archive mastered items (meet threshold) — don't review indefinitely.
- DON'T: review items that aren't due — respect the schedule.
- DON'T: let sessions exceed 15 items — defer the rest.
- DON'T: add items to schedule before they're genuinely understood.
- DON'T: frame review sessions as tests — it's memory maintenance.

# Output

Session start: due count + overdue count + estimated time. Per-item: topic, question, learner response, answer, score, next review date. Session close: score distribution (easy/good/hard/failed), failed items list, next 7-day schedule. Format naturally.

# Checklist

- [ ] Overdue items prioritized first.
- [ ] Session capped at 15 items.
- [ ] Answer not revealed before learner attempt.
- [ ] Failed items re-tested within same session.
