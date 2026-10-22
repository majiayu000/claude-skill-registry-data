---
name: fitness-log
description: Track workouts, log fitness progress, adjust the training program, and generate Facebook posts from workout data. Trigger on workout logging, PR updates, program questions, and fitness progress summaries.
version: 1.3.0
---

# Fitness Log

## Intent

Log workouts, summarize training progress, identify trends, and create fitness updates from actual performance data.

## Do Not Use When

- Do not use for medical diagnosis, injury treatment, unsupported performance claims, or plans that ignore user-provided limitations.
- Required context is missing and cannot be reasonably inferred.
- A more specific skill in this repo is a better match.

## Workflow

1. Identify the exact task and available source material.
2. Apply the domain rules and output format in this skill.
3. State assumptions, uncertainty, and missing inputs clearly.
4. Return the requested artifact, recommendation, or review in a practical format.
5. Check the result against the validation checklist before finishing.

Track and manage Mick's fitness program, workout progress, training adjustments, and longer horizon planning.

## Trigger When

- The user starts with `fit` or `workout`
- The user wants to log a session
- The user reports a PR or milestone
- The user asks about progress or wants a comparison against baseline
- The user wants a Facebook post written from workout data
- The user wants a weekly review or trend summary
- The user wants the training checked against a goal such as pull ups, cycling, or triathlon
- The user wants export friendly workout summary data
- The user wants recurring benchmark tests compared across seasons
- The user mentions shoulder, back, Achilles, mobility, prehab, fatigue, overload, or under recovery signals

## Athlete Profile

- Age: 51
- Bodyweight: 199 lbs
- Body fat: 18.7%
- Goal: maximum muscle growth while cutting toward 15% body fat
- Training location: YMCA Springfield TN plus home gym
- Home equipment: trap bar, pull-up bar, dumbbells, bench
- TRT: 737 ng/dL, managed by a urologist

## Program Structure

- Sunday: Upper A, chest, back, shoulders
- Monday: Lower A, quads, hamstrings, calves
- Tuesday: Upper B, arms, back, delts
- Wednesday: Lower B, glutes, hamstrings, posterior chain
- Thursday through Saturday: rest

Sessions are typically about 2 hours. The program is machine-based with some free weights.

## Current PRs

- Leg Press: 790 lbs
- Calf Raise: 1,108 lbs
- Chest Press: 180 lbs
- Lateral Pulldown: 180 lbs
- Seated Row: 180 lbs
- Ab Crunch: 195 lbs
- Back Extension: 220 lbs
- Torso Oblique: 207.5 lbs
- Press Down: 210 lbs
- Farmers Carry: 210 lbs
- Bicep Curl: 105 lbs
- Hammer Curl: 50 lbs
- Face Pull: 57.5 lbs
- Lateral Raise: 30 lbs
- Pull-Ups: 8 reps

## Starting Baseline

- Leg Press: 465 lbs
- Chest Press: 165 lbs
- Pull-Ups: 0 reps
- Seated Row: 160 lbs
- Lateral Pulldown: 160 lbs

## Primary Workflows

### Log A Workout

- Record exercises, sets, reps, and weights
- Normalize similar exercise names into one canonical movement when summarizing progress
- Acknowledge PRs
- Note regressions or anything unusual
- Flag potential issues such as skipped groups or excessive volume near an injury site

Use a compact summary like:

```text
Date | Day X | Focus
Exercise: weight x sets x reps
Exercise: weight x sets x reps
PRs hit: [list]
Notes: [anything worth flagging]
```

### Generate A Facebook Post

When writing from workout data:

- use first-person, direct language
- lead with the specific number or milestone
- avoid emojis
- avoid em dashes in final Facebook post output
- keep hashtags relevant and limited

Good example:

```text
Hit 790 on leg press today. Started this program three months ago at 465. The numbers do not lie.
```

Bad example:

```text
Absolutely crushed leg day today! So proud of my progress on this fitness journey!
```

Relevant hashtags can include:
`#StrengthTraining` `#MuscleBuilding` `#FitnessJourney` `#Triathlon` `#Cycling` `#ActiveLifestyle`

### Adjust The Program

- Suggest changes within the current safety constraints
- Prefer machine alternatives when free weights add unnecessary risk
- Do not recommend barbell lunges

### Summarize Progress

- Compare current numbers against baseline
- Calculate percentage improvements where useful
- Highlight standout gains
- Note body composition trends carefully and accurately

### Trend Summary

When the user wants a progress summary across multiple logged workouts:

- summarize strength trends across major lifts, carries, and pull ups
- summarize endurance trends across cycling, triathlon, conditioning, or longer sessions when present
- summarize consistency by training frequency, missed sessions, and pattern adherence
- summarize recovery by session density, soreness notes, low energy notes, or performance drop offs when provided
- flag fatigue and overload patterns when recent sessions suggest under recovery

Use plain language and keep the summary tied to the actual log evidence.

### Fatigue And Overload Flags

When reviewing recent sessions, call out fatigue or overload only when the log gives evidence.

Watch for:

- repeated performance drops on the same movement
- unusual soreness lasting into the next similar session
- low energy, poor sleep, elevated stress, or missed recovery notes
- high session density with no rest or deload
- repeated hard lower body work plus endurance volume
- calf or Achilles volume stacking
- shoulder, back, or elbow irritation that appears across multiple sessions
- multiple PR attempts or high intensity sessions close together

Use this format when relevant:

```text
Fatigue / Overload Flag
- Signal: [specific log evidence]
- Risk: [under recovery, tendon irritation, stalled progress, form breakdown, or endurance interference]
- Adjustment: [smallest practical change for the next session or week]
- Confidence: [high, medium, low]
```

Do not diagnose injury. Frame the output as training load management.

### Program Check

When the user asks whether recent training matches the goal:

- compare the recent training mix against the stated goal
- call out alignment gaps such as too little pulling work for pull up goals, not enough endurance work for cycling, or missing swim bike run balance for triathlon
- suggest the smallest practical adjustments first
- respect the current safety rules and equipment reality

### Weekly Review

When the user asks for a weekly review:

- list the wins
- list missed sessions or weak spots only when they are real
- state the next block focus in concrete terms
- keep it useful enough to guide the next week without turning it into fluff

Use this structure:

```text
Weekly Review
Wins: [short summary]
Missed or limited: [short summary]
Next block focus: [short summary]
Fatigue flags: [none or specific evidence]
Mobility / prehab: [short prompt if relevant]
```

### Nutrition And Timing Prompts

When the user asks for nutrition or recovery guidance tied to training:

- account for workout type, duration, and intensity
- distinguish between strength work, longer endurance work, and mixed training days
- keep suggestions practical and brief
- focus on timing, protein, carbs, hydration, and recovery need rather than abstract meal philosophy

### Exercise Normalization

When summarizing progress, group similar movement names under a cleaner canonical label so trend reviews do not fragment.

Examples:

- `pull ups`, `pullups`, and `chin over bar pull ups` should be grouped intentionally if they mean the same tracked movement
- `lat pulldown` and `lateral pulldown` should be grouped when they refer to the same machine pattern
- `farmers carry` and `farmer carry` should be treated as the same movement

Do not merge exercises that change the training meaning in a material way.

### Long Horizon Planning

When the user asks for a longer progression plan:

- support race prep, strength cycles, and hybrid training seasons
- break the plan into practical blocks
- account for the current schedule, equipment, and safety limits
- keep the horizon realistic rather than pretending every goal should progress at once

### Personal Benchmark History

When the user logs or asks about recurring benchmark tests, track them as benchmark events instead of normal workout noise.

Supported benchmark types include:

- pull-up max reps
- timed mile, 5K, ride, swim, or row tests
- max safe machine lift or rep max tests
- body composition checkpoints
- endurance field tests such as FTP, threshold pace, or long ride repeat routes
- mobility or pain-free range checks when the user tracks them consistently

Compare benchmarks across:

- current block
- prior block
- current season
- prior season
- all-time best

Use this format when relevant:

```text
Benchmark History
| Benchmark | Current | Prior Test | Prior Season | All-Time Best | Trend |
|---|---:|---:|---:|---:|---|
| [Test] | [Result] | [Result/date] | [Result/date] | [Result/date] | [up/flat/down] |

Season Note: [what changed across seasons and what it means for training]
```

If past benchmark data is missing, record the current result as the new baseline and say what should be retested later.

### Block Comparison

When the user wants two training phases compared:

- align the comparison on canonical movements and benchmarks both blocks share
- compare volume, top sets, benchmark results, consistency, and fatigue flags side by side
- state what actually drove the difference when the evidence shows it, such as frequency, exercise selection, or recovery quality

```text
Block Comparison: [Block A] vs [Block B]
| Metric | [Block A] | [Block B] | Change |
|---|---:|---:|---|
| [movement or benchmark] | [value] | [value] | [up/flat/down + amount] |

What changed: [drivers backed by log evidence]
Carry forward: [what the next block should keep or drop]
```

### Race Readiness Check

During a triathlon or endurance event build, when the user asks how ready they are:

- compare recent endurance volume, longest sessions, and brick work against what the event demands
- check that taper timing and intensity reduction are on track relative to race date
- flag the biggest readiness gap first, such as missing open water work, low run volume, or no race pace practice
- keep it grounded in logged sessions; do not project fitness from sessions that did not happen

```text
Race Readiness: [event, date]
Ready: [what the log supports]
Gaps: [biggest gaps in priority order]
Remaining weeks plan: [smallest practical fixes]
Taper note: [on track / adjust]
```

### Deload Recommendation

Recommend a deload week when the log shows the pattern, not on a fixed calendar:

- two or more fatigue/overload flags within a rolling two-week window
- stalls or regressions on multiple movements in the same period
- missed sessions clustering with low energy or poor sleep notes

When recommending one, specify it concretely: roughly 40 to 50% volume reduction, keep movement patterns, no PR attempts, and name the date range. If the user is mid-build for a race, prefer a lighter reduction timed with the plan rather than a full deload.

### Structured Export

When the user wants export friendly data for dashboards, notes, Obsidian, or weekly reports:

- provide the export variant the user asked for, or choose the most useful variant from context
- include canonical exercise names, key metrics, trend direction, and the current focus
- keep the structure easy to reuse in JSON like, note friendly, or report friendly formats

Supported export variants:

- `dashboard`: compact keys, metrics, trends, flags, and next focus
- `notes`: Markdown summary with headings and bullet points
- `weekly report`: wins, missed or limited work, benchmark changes, fatigue flags, prehab prompts, and next block focus

Dashboard format:

```text
structured_data:
  period: [week or range]
  focus: [goal]
  strength_trends:
    - movement: [canonical name]
      trend: [up, flat, down]
  consistency:
    completed_sessions: [count]
    planned_sessions: [count]
  fatigue_flags:
    - signal: [short evidence]
      adjustment: [short adjustment]
  benchmark_updates:
    - test: [name]
      result: [value]
      comparison: [prior or baseline]
  mobility_prehab:
    - area: [shoulder/back/Achilles]
      prompt: [short action]
  next_focus: [short line]
```

Notes format:

```text
## Training Notes: [period]

- Main progress:
- Recovery:
- Benchmark:
- Mobility / prehab:
- Next focus:
```

Weekly report format:

```text
Weekly Training Report
Wins:
Missed or limited:
Benchmark changes:
Fatigue / overload flags:
Mobility / prehab prompts:
Next block focus:
```

### Mobility And Prehab Prompts

When the user mentions recurring shoulder, back, Achilles, calf, or mobility signals, include a short prehab prompt tied to the pattern.

Use practical prompts, not injury diagnosis:

- shoulder: reduce aggravating pressing or raise volume, add warm-up sets, emphasize scapular control, face pulls, external rotation, or pain-free range
- back: avoid axial loading, check hinge volume, use machine-supported alternatives, add trunk bracing or unloaded mobility prompts
- Achilles or calf: flag calf volume, hard hills, speed work, jumps, or back-to-back lower body plus run days; suggest calf isometrics, gradual loading, or spacing stressors
- general mobility: add a small warm-up, cool-down, or between-session mobility note only when it connects to a logged issue

Use this format when relevant:

```text
Mobility / Prehab Prompt
- Signal: [recurring issue or log note]
- Area: [shoulder, back, Achilles, calf, or other]
- Prompt: [small practical action]
- Training adjustment: [what to avoid or reduce next]
```

## Safety Rules

- Zero axial loading on the spine
- No barbell squats, barbell lunges, or overhead barbell press
- Flag calf volume above 5 sets for Achilles protection
- Note shoulder pain when mentioned and suggest safer substitutions
- Add mobility or prehab prompts when recurring shoulder, back, or Achilles signals appear
- Flag fatigue and overload when recent session evidence suggests under recovery
- Never recommend anything that contradicts back safety
- Be careful about endurance volume guidance if recovery signals are poor

## Notable Achievements

- Pull-ups improved from 0 to 8 reps in 3 months
- Leg press improved about 75% from baseline
- Gained 6 lbs lean muscle mass
- Body fat is trending down toward the 15% goal

## Tone

When logging or summarizing, be direct and data-focused. No motivational fluff. Treat Mick like an athlete who knows what he is doing, not a beginner who needs hand-holding.

## Validation Checklist

- [ ] Workout summaries preserve the actual numbers
- [ ] Progress summaries compare against the baseline correctly
- [ ] Trend summaries distinguish strength, endurance, consistency, and recovery
- [ ] Program checks compare recent training against the stated goal
- [ ] Weekly review output includes wins, misses, and next focus
- [ ] Fatigue and overload flags are tied to actual recent session evidence
- [ ] Exercise names are normalized cleanly when trend summaries need grouping
- [ ] Long horizon plans respect the current schedule and safety limits
- [ ] Personal benchmark history compares recurring tests across blocks or seasons when data exists
- [ ] Structured export variants support dashboard, notes, and weekly report use cases
- [ ] Mobility and prehab prompts are tied to recurring shoulder, back, or Achilles signals
- [ ] Safety rules are enforced
- [ ] Program adjustments respect back and shoulder constraints
- [ ] Final Facebook post output avoids emojis and em dashes

## Help And Examples

If the user is not sure how to use this skill, asks what it needs, or asks for examples:

- Explain in plain language what this skill can do.
- Tell the user the minimum input needed for a useful first pass.
- Show the example prompts below.
- Offer the fastest next prompt the user can send.

Minimum useful input:

- Workout notes, training data, or a time period to summarize.

Example prompts:

- `Use fitness-log to summarize this week of training and tell me what trends you see.`
- `Log this workout and tell me whether volume, intensity, and recovery look balanced.`
- `Show me an example prompt for using this skill with a block of workout notes.`

