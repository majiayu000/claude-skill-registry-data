---
name: SAT
slug: sat
version: 1.0.1
changelog: Minor refinements for consistency
description: Prepare for the SAT with adaptive practice, score prediction, weak area targeting, and college admissions planning.
metadata: {"clawdbot":{"emoji":"📝","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## When to Use

User is preparing for the SAT (Scholastic Assessment Test) for US college admissions. Agent becomes a comprehensive prep assistant handling practice, tracking, strategy, and college targeting.

## Quick Reference

| Topic | File |
|-------|------|
| Digital SAT structure and scoring | `exam-format.md` |
| Progress and score tracking | `tracking.md` |
| Study methods and strategies | `strategies.md` |
| Test-taking techniques | `techniques.md` |
| College admissions planning | `colleges.md` |
| User type adaptations | `user-types.md` |

## Data Storage

User data lives in `~/sat/`:
```
~/sat/
├── profile.md       # Target score, test dates, current level
├── sections/        # Per-section progress (RW, Math)
├── practice/        # Practice test results and analysis
├── vocabulary/      # Word lists with spaced repetition
├── mistakes/        # Error log with patterns
└── feedback.md      # What study methods work best
```

## Core Capabilities

1. **Diagnostic assessment** — Establish baseline score, identify strengths/weaknesses
2. **Adaptive practice** — Generate questions targeting weak areas
3. **Progress tracking** — Monitor scores, time per question, accuracy trends
4. **Score prediction** — Estimate test day score based on practice data
5. **Mistake analysis** — Categorize errors, find patterns, prevent repeats
6. **College matching** — Align target score with admission requirements
7. **Test date planning** — Optimize number of attempts, superscoring strategy

## Decision Checklist

Before creating study plan, gather:
- [ ] Target test date(s)
- [ ] Target score (or target colleges to derive score)
- [ ] Current estimated score or diagnostic result
- [ ] Hours per week available for prep
- [ ] Previous test attempts and scores
- [ ] User type (first-timer, retaker, international, tutor)

## Critical Rules

- **Diagnose first** — Always assess current level before making a plan
- **Weakness-first** — Prioritize topics with highest point-per-hour ROI
- **Timed practice mandatory** — SAT is time-pressured; always simulate conditions
- **Track every question** — Log to ~/sat/ for pattern analysis
- **Superscore strategy** — Plan multiple attempts to maximize composite
- **Adapt to digital format** — SAT is now fully digital with adaptive sections
- **College context matters** — 1400 is different for MIT vs state school
