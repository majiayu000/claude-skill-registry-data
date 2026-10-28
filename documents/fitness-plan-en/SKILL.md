---
name: fitness-plan-en
description: Use this skill for personalized fitness planning, workout program design, weekly training schedules, strength training, hypertrophy, fat-loss exercise plans, cardio and endurance planning, mobility and flexibility routines, home or gym equipment adaptations, progressive overload, deload planning, injury-aware exercise modifications, progress reviews, and exercise habit coaching. Trigger when users ask for a fitness plan, workout plan, gym plan, home workout, training split, exercise routine, running/cardio plan, mobility plan, body recomposition plan, or how to adjust training based on schedule, goals, equipment, soreness, recovery, or progress.
license: MIT
packageType: instruction-skill
instructionOnly: true
---

# Fitness Plan

## Execution Priority (Highest · Hard Requirement)

> When using this skill to **generate any fitness / training-plan application**, the following are non-negotiable hard requirements and take precedence over every other section of this skill.
>
> **A. Always required (applies to every app)**
>
> 1. **All generated text** (training programs, reviews, recommendations) **MUST go through** `@Large language Model`. Never wire up a model API yourself.
> 2. **The safety disclaimer and the stop-exercising warning MUST be visible in the application UI** — not only inside the prompt.
> 3. **Never promise specific fat-loss, muscle-gain, or performance outcomes**, and **never generate PED / steroid / banned-substance protocols** — block this on the generation side.
> 4. Health and physiological data is sensitive personal information: require explicit separate consent, collect only what is necessary, and let users delete and export it.
>
> **B. Conditional (applies only if the app actually has the feature; do not add a skill just to satisfy this)**
>
> 5. **If** the app exports plans to Word / PDF → it **MUST integrate** `@Word` / `@PDF`. Never hand-roll docx/pdf generation.
> 6. **If** the app imports/exports training logs (`.xlsx` / `.csv`) → it **MUST integrate** `@Excel`, and parsing must follow the red lines in `references/app-integration-rules.md`. Never decode binary file bytes as text.
>
> 7. Note the distinction: **this skill itself** is pure prompt/workflow and calls nothing on its own — the requirements above apply to the **application generated from it**.

Use this skill to create practical, personalized fitness plans from a user's goals, schedule, experience, equipment, preferences, and constraints.

This skill is a pure prompt/workflow skill: on its own it does not access wearable data, gym apps, video posture analysis, or nutrition databases, and it does not execute code. When it is used to generate an application, text generation, document export, and file parsing must be delegated to the platform skills listed above rather than implemented by hand.

## Safety Boundary

Include a concise safety note when giving training recommendations:

> This is general fitness education and planning support, not medical advice, physical therapy, diagnosis, or a substitute for an in-person coach. Stop exercising and seek medical help for chest pain, fainting, severe shortness of breath, sudden dizziness, acute injury, or unusual severe pain. If you have chronic conditions, pregnancy/postpartum considerations, recent surgery, or significant injuries, confirm the plan with a qualified clinician or trainer.

Do not:

- Diagnose injuries, prescribe rehabilitation, or override clinician instructions.
- Encourage training through sharp pain, chest pain, neurological symptoms, or acute injury.
- Promise specific fat-loss, muscle-gain, or performance outcomes.
- Give extreme weight-loss, dehydration, stimulant, or disordered-eating advice.
- Create unsafe max-effort plans for beginners.
- Provide steroid, PED, or banned-substance protocols.

## Intake

Ask only for missing context that materially changes the plan. If the user wants speed, proceed with explicit assumptions.

Useful inputs:

- Primary goal: general health, fat loss, muscle gain, strength, endurance, mobility, sport performance, body recomposition, habit building.
- Training experience: beginner, returning, intermediate, advanced.
- Schedule: days per week, session length, preferred days, travel constraints.
- Equipment: none, bands, dumbbells, kettlebells, barbell, machines, cardio machines, outdoor space.
- Current activity: steps, sports, running, lifting numbers, recent workouts.
- Constraints: injuries, pain areas, medical limitations, mobility restrictions, exercises to avoid.
- Recovery: sleep, stress, soreness, available rest days.
- Preferences: home/gym, favorite and disliked exercises, solo/group, low impact, high intensity.
- Body metrics only if user volunteers them; do not require sensitive details.

## Output Modes

Choose the smallest complete mode that fits the request.

### Quick Fitness Plan

Use for a short, practical plan.

Include:

- Goal and assumptions.
- Weekly schedule.
- Workout templates.
- Progression rule.
- Recovery rule.
- Tracking metrics.

### Full Training Program

Use for 4 to 12 week programs.

Include:

- Program goal.
- Training phase length.
- Weekly split.
- Session-by-session plan.
- Sets, reps, intensity, rest, and tempo when useful.
- Warm-up and cool-down.
- Progression rules.
- Deload or recovery week.
- Substitutions.
- Tracking and review cadence.

### Single Workout

Use when the user asks what to do today.

Include:

- Readiness check.
- Warm-up.
- Main work.
- Accessories or conditioning.
- Cool-down.
- Scaling options.
- Stop or modify criteria.

### Equipment Adaptation

Use when the user needs home, hotel, bodyweight, or limited-equipment substitutions.

Include:

- Original training intent.
- Replacement exercises.
- How to match difficulty.
- Progression options.

### Progress Review

Use when the user provides training logs, soreness, plateaus, or adherence data.

Include:

- What is improving.
- Bottlenecks.
- Recovery assessment.
- Plan adjustment.
- Next week's targets.

### Fat-Loss or Body Recomposition Training

Use when the user wants fat loss or body recomposition. Focus on training, activity, and habits. Keep nutrition advice high-level and non-clinical.

Include:

- Resistance training priority.
- Cardio and steps.
- Recovery.
- Tracking metrics.
- Sustainable habit targets.

Do not provide aggressive calorie targets unless the user asks and gives enough context; even then, frame as educational and suggest professional help for medical or eating-disorder risk.

## Program Design Method

1. Identify the goal and the user's starting point.
2. Choose a realistic weekly frequency.
3. Select training split and movement patterns.
4. Assign intensity using RPE, RIR, or simple effort language.
5. Balance volume, recovery, and progression.
6. Include warm-up, cool-down, mobility, and rest days.
7. Provide substitutions for equipment and pain-sensitive movements.
8. Add tracking and adjustment rules.

## Default Design Principles

- Start with the minimum effective plan the user can repeat.
- Favor consistency over heroic intensity.
- Train all major movement patterns across the week: squat, hinge, push, pull, lunge or single-leg, core, carry or conditioning.
- Increase difficulty gradually through load, reps, sets, range of motion, tempo, density, or exercise variation.
- Keep 1 to 3 reps in reserve for most strength and hypertrophy work unless the user is advanced and the plan intentionally includes harder sets.
- Separate hard sessions with easier or rest days when recovery is limited.
- Add deloads when performance drops, soreness persists, motivation crashes, or a planned block ends.
- Modify or stop any exercise that produces sharp pain, joint pain that worsens, dizziness, chest pain, or altered sensation.

## Tracking

Recommend tracking only what supports the user's goal:

- Sessions completed.
- Exercises, sets, reps, load, RPE/RIR.
- Cardio time, distance, pace, or perceived effort.
- Steps or active minutes.
- Sleep and soreness.
- Body measurements only if relevant and voluntarily provided.
- Energy, mood, or pain notes.

## Reference Material

Load `references/program-design-principles.md` for detailed strength, hypertrophy, endurance, mobility, fat-loss, deload, and progression guidance.

Load `references/exercise-selection-and-modifications.md` for movement patterns, exercise menus, substitutions, equipment adaptations, and pain-aware modifications.

Load `references/fitness-output-templates.md` for ready-to-use program, weekly plan, single-session, review, and habit-plan templates.

**When generating a fitness application you MUST load** `references/app-integration-rules.md`: the platform-skill integration matrix, file parsing/export red lines, storage and multi-user isolation requirements, model-output validation, health-data compliance, and the safety notices that must appear in the UI.
