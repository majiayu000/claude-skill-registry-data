---
name: prep-plan
description: Build a realistic week-by-week placement / job-prep plan from the candidate's deadline, daily hours, target companies, current level and their actual weak spots from past cracked sessions. Re-running it reviews progress and re-plans. Use when the user asks for a prep roadmap, a study plan for placements or interviews, "how should I prepare in N weeks", what to study next, or wants to review their prep progress.
---

# Prep plan

A plan that ignores where the candidate actually is goes in the bin by week two. This one is built from their deadline, their hours, and their real performance data in the cracked journal, and it's rebuilt whenever they come back.

## 0. Inputs

1. Call the Skill tool with "cracked-profile". You need: `deadline`, `hours_per_day`, `target_companies`, `target_roles`, `dsa_level`, `language`. Ask for any that are missing (in one round).
2. For each company in `target_companies` (max 3), call the Skill tool with "company-intel". Use the briefs' DSA topic mix to weight the patterns, and their process to schedule company-specific mocks. No target companies? Plan for the target tier.
3. Read `$CRACKED_DIR/journal.md`. **Normalise the tags first**: lowercase, hyphenate, map near-duplicates onto the canonical list in `cracked-profile` (`DP`, `dynamic-programming` and `dp` → `dp-1d` or `dp-2d` by context; `edgecases` → `edge-cases`). Then count sessions per skill, collect every `weak_spots` tag with its frequency and recency, count `pattern:` fields, and note score trends.
4. Read `$CRACKED_DIR/plan.md` if it exists. If it does, this is a **review run**: go to §3 first.

## 1. Budget the time

- Weeks available = deadline − today. Get today's date by running `date +%F` (or `python3 -c "import datetime; print(datetime.date.today())"`); never assume it. Total hours = weeks × 7 × hours_per_day × 0.8 (life happens; plan for 80%).
- Split the hours by target, using [ALLOCATION.md](ALLOCATION.md) as the starting point, then shift 10–20% toward the most frequent weak-spot tags.
- If the time is unrealistic for the goal (e.g. 3 weeks, beginner, big-tech target), say so plainly, then give the **best plan for the time available** and a realistic alternative target. Never pretend it'll be fine.

## 2. Write the plan

Save to `$CRACKED_DIR/plan.md`:

```markdown
# Prep plan · <target> · <today> → <deadline>

## Reality check
<2–3 lines: time budget, the gap, the strategy>

## Weekly plan
### Week 1 (<dates>): <theme>
- DSA: <patterns + target problem counts, e.g. "Sliding window + two pointers: 12 problems (4E/6M/2H)">
- Core: <subject topics>
- Projects/Resume: <one concrete deliverable>
- Mock: <which cracked skill to run and when, e.g. "Sat: /mock-interview on arrays (medium)">
- Checkpoint: <a measurable goal to hit by Sunday>

### Week 2 …

## Daily template (<hours>/day)
<a time-boxed routine, e.g. 60 min new pattern · 45 min revision (spaced repetition of old problems) · 30 min core subject · 15 min log>

## Rules
- Weekly: 1 mock (alternating /mock-interview, /oa-sim, /core-viva), 1 /prep-plan review
- Never more than 2 days without revising old problems
```

Principles:
- **Pattern-first DSA**: group problems by pattern (use the `pattern-coach` skill's catalog by calling the Skill tool with "pattern-coach" if you need it). Sequence: arrays/hashing → two pointers/sliding window → binary search → stack → linked list → trees → heaps → graphs → DP → backtracking.
- **Front-load** resume and project work (`/roast-my-resume`, `/make-it-hireable`): applications open before interviews.
- **Mock early**, from week 1, not at the end. Mocks find weak spots; the plan adapts around them.
- **Company-weighted DSA**: when briefs exist, include each target company's top recent reported questions (`questions.py get "<Company>" --window 3m`) as named problems in the weekly lists.
- In the final 1–2 weeks: company-specific prep (`/resume-blueprint`, `/jd-match`, `/oa-sim` in that company's style, `/hr-round` company mode), revision, and no new topics.
- Keep it achievable. A plan they finish beats a perfect plan they abandon.

## 3. Review run (when a plan exists)

1. Compare the plan's checkpoints so far with the journal: which mocks happened, which scores, which weak-spot tags persist or are new.
2. Show a short progress report: `On track / Behind by ~N days / Ahead`, plus the 3 most important observations (e.g. "DP still fails in 3 of 3 mocks", "Communication up from 5 to 8").
3. Ask what got in the way, if they're behind. One question.
4. Rewrite the **remaining** weeks in `plan.md`. Keep completed weeks as history, marked ✅/🟡/❌.

## 4. Finish

Give the plan's headline and **this week's first three actions**, each with the exact cracked command to run. There's no scorecard for planning sessions; don't log to the journal.

---

*Skill calls:* if your agent has no Skill tool, open the named skill's `SKILL.md` in the cracked skills folder (`core/`, `interview/`, `profile/`, `strategy/`) and follow it instead.
