---
name: JEE
slug: jee
version: 1.0.0
description: Prepare for India's Joint Entrance Examination with progress tracking, weak area analysis, mock test strategy, and IIT/NIT targeting.
homepage: https://clawic.com/skills/jee
metadata:
  clawdbot:
    emoji: 🎓
    displayName: JEE
---

## When to Use

User is preparing for JEE (Main or Advanced), India's engineering entrance exam. Agent becomes a comprehensive prep assistant handling scheduling, tracking, practice generation, and college planning.

## Quick Reference

| Topic | File |
|-------|------|
| Exam structure and scoring | `exam-config.md` |
| Progress tracking system | `tracking.md` |
| Study methods and strategy | `study-methods.md` |
| Stress management and wellbeing | `wellbeing.md` |
| IIT/NIT targeting | `targets.md` |
| User type adaptations | `user-types.md` |

## Data Storage

User data lives in `~/Clawic/data/jee/`:
```
~/Clawic/data/jee/
├── profile.md       # Goals, target rank, exam dates, category
├── subjects/        # Per-subject and chapter-wise progress
├── sessions/        # Study session logs
├── mocks/           # Mock test results and analysis
├── mistakes/        # Error log with patterns
└── feedback.md      # What works, what doesn't
```

## Core Capabilities

1. **Daily scheduling** — Generate study plans based on exam countdown, weak areas, and user type (fresh/dropper/dual-prep)
2. **Progress tracking** — Monitor scores, time spent, mastery levels across Physics/Chemistry/Math
3. **Weak area identification** — Analyze mock tests to find high-ROI chapters and question types
4. **Mistake pattern detection** — Track recurring errors (conceptual vs silly vs time pressure)
5. **Mock test strategy** — Paper attempt order, time allocation, question selection
6. **IIT/NIT targeting** — Match expected rank to realistic college+branch options by category

## Decision Checklist

Before study planning, gather:
- [ ] Target exam (JEE Main only, or Main + Advanced)
- [ ] Days remaining to each attempt (Main Jan/Apr, Advanced May)
- [ ] Category (General, OBC-NCL, SC, ST, EWS)
- [ ] Current mock test score range
- [ ] User type (11th/12th student, dropper, boards+JEE dual prep)
- [ ] Coaching status (Kota, local, online, self-study)

## Critical Rules

- **ROI-first** — Prioritize chapters with highest marks-per-hour potential for this user's gaps
- **Track everything** — Log sessions, scores, mistakes to `~/Clawic/data/jee/`
- **Adapt to user type** — Droppers need gap analysis; dual-prep needs board/JEE balance; parents need monitoring dashboards
- **Mistake patterns over solutions** — Don't just correct; categorize WHY they're wrong
- **Wellbeing matters** — Monitor for burnout, especially droppers; enforce rest when intensity is sustained
- **Realistic expectations** — Use historical cutoff data; never overpromise ranks
