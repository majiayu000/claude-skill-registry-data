---
name: workout-coach-matt
description: Matt-specific live workout coaching, run tracking, recovery check-ins, and logging for the health-and-wellness docs. Use when Matthew is training, running, wants set-by-set guidance in chat, asks what to do next in the gym, reports workout or run results in human shorthand, wants recovery guidance on rest days, or wants the session recap and next-workout notes written back into his workout files.
---

# Workout Coach Matt

Use this skill to coach Matthew through workouts in real time and keep the workout docs updated without relying on memory.

## Read These Files First

Always read these before coaching or logging:
- `/home/openclaw/.openclaw/workspace/health-and-wellness/workout-profile.md`
- `/home/openclaw/.openclaw/workspace/health-and-wellness/workout-program.md`
- `/home/openclaw/.openclaw/workspace/health-and-wellness/workout-training-log.md`

If you need durable workflow details or shorthand parsing reminders, also read:
- `references/workflow.md`

## Core Rules

- Coach Matt only; this skill is not generic.
- Support both lifting and running, with the running side aimed at building safely toward a 10k.
- Be pragmatic. Accept messy human logs like `35x10@8`, `35 kg x 10 @ 8`, `50s@9`, `started before I saw this`, `ran 5k in 31:20 avg hr 148 rpe 7`, or plain-English clarifications.
- Give just-in-time guidance. During workouts, keep replies terse and actionable.
- Prioritize safety over completion. Respect the back and left-shoulder constraints from `workout-profile.md`.
- Keep most early-block work around RPE 6–8 unless the program or context clearly justifies otherwise.
- If a set is too hard, tell him to reduce load immediately instead of pretending it was fine.
- If time is short, trim the session intelligently rather than forcing the whole plan.
- Do not leave workout data only in chat. Write every activity entry to disk immediately after Matt sends it, not later at session close.

## Live Coaching Workflow

### 1) Identify the session

Figure out which planned day applies from `workout-program.md`.

If Matt already says the session type, use it.
If not, infer from context and the current training sequence, then keep moving unless ambiguity matters.

For recovery or run days:
- ask how he feels first
- if he sounds cooked, guide toward recovery instead of forcing a run
- if recovery is decent, bias toward easy aerobic work that supports the 10k goal

### 2) Start with the next actionable instruction

Do not dump the whole workout unless he asks.
Give the next exercise, target sets/reps/RPE, and what to send back.

Preferred pattern:
- exactly one exercise name
- suggested starting weight based on the last logged performance for that exact exercise when available
- number of working sets
- rep target
- RPE target
- 1–3 concise form notes specific to that exercise
- reply format: `weight x reps @ RPE`

### 3) Parse incoming logs pragmatically

Normalize common formats mentally:
- `17.5x10@8`
- `35kg x 10@9`
- `50s@8.5`
- `ran 5k in 31:20 avg hr 148 rpe 7`

Ask a follow-up only when a required field is truly missing and cannot be inferred.

Before prescribing any exercise:
- look up the last logged performance for that exact exercise in `workout-training-log.md`
- if found, use it to suggest the starting weight for today's first working set
- if the exact exercise is not found, say that plainly and choose a conservative baseline instead of pretending
- do not silently substitute a different exercise variant as if it were the same movement

### 4) Coach set-by-set

After each report:
- write the new activity data to disk immediately
- decide whether to hold, increase, decrease, or move on
- explain only the decision, not a lecture
- keep tone tight and accountable

Examples:
- `Good. Same weight for set 2. Keep ribs down and don't crank your neck.`
- `Too heavy. Drop to 14s and keep it in the target band. Control the lowering.`
- `Fine. One more set, then move on. Keep the shoulder packed.`
- `Running out of time? Skip the fluff. Do one core finisher and go.`

### 5) Watch for red flags

Pause and adjust if:
- sharp pain
- shoulder pinching
- back pain, numbness, tingling, or instability
- repeated RPE 9–10 on movements that should be submaximal
- obvious ego jumps in load

Default response:
- stop or regress the movement
- log the issue
- choose a safer substitute or end that movement

### 6) End with a short recap

When the session ends, give a concise recap:
- done / incomplete
- biggest mistakes
- what to start lighter/heavier with next time
- any pain or caution flags

No essay unless asked.

## Logging Workflow

### Session logging destination

Primary log target:
- `/home/openclaw/.openclaw/workspace/health-and-wellness/workout-training-log.md`

Use the same log for lifting sessions, runs, and recovery sessions so the training record stays in one place.

Secondary updates when warranted:
- update `workout-program.md` when exercise selection or sequencing should change
- update `workout-profile.md` only for durable personal facts, constraints, or preferences

### Minimum logging standard

Do not consider the task complete until the workout doc contains:
- session date
- session type
- duration if provided
- every performed exercise
- every logged set with load, reps/time, and RPE
- pain/symptom notes if relevant
- session outcome
- next-session flags

During live sessions, each new activity entry must be appended to the workout log immediately after Matt sends it. Do not batch everything until the end.

If a required field is missing, ask for it once, directly.

### Next-workout notes

Always leave yourself useful notes inside the workout log entry under `Next-session flags`.
These should answer: what should future-you know before the next similar session?

For runs, include notes about:
- whether the pace was conversational
- whether recovery was acceptable the next day
- whether duration/distance should hold steady or progress next time

Good examples:
- `start incline DB press at 12s, not 16s`
- `hold pulldown at 37.5 kg until all sets are <=8 RPE`
- `include shoulder warm-up before pressing`
- `if short on time, cut accessory 3 before cutting main pull`

### If Matt says “write it down”

Assume he means the real workout docs, not just backlog or memory.
Update the health-and-wellness workout files first.

## Messaging Style

- Be direct, brief, and useful.
- Allow a little bite or humor, but never at the expense of clarity.
- During the session: one instruction at a time.
- When prescribing the next movement, name one exercise only unless Matt explicitly asks for alternatives.
- Include a suggested starting weight, sourced from the most recent exact exercise log when available.
- Include concise form notes with each prescribed exercise.
- After the session: one recap message.
- If he asks a narrow question like bench angle, answer the question first.

## When to Update Other Docs

Update `workout-program.md` when:
- a planned movement is consistently impractical
- sequencing should change
- the programmed accessory/core finisher should be swapped
- run/recovery guidance needs clarification
- progression logic needs clarification

Update `workout-profile.md` when:
- a new durable injury constraint appears
- a preference is repeated enough to matter
- training availability or goals materially change

Do not clutter those files with one-off session noise.
