---
name: fitness-programming
description: Build structured training plans, progression blocks, and goal-specific fitness programming for Mick. Trigger when the user wants a training program, block plan, race prep plan, hybrid season layout, exercise split, progression strategy, or asks how to train toward goals such as pull ups, cycling, triathlon, muscle gain, or fat loss.
version: 1.2.0
---

# Fitness Programming

## Intent

Build structured training blocks and progression plans for measurable strength, endurance, cycling, pull-up, and triathlon goals.

## Do Not Use When

- Do not use for medical care, injury diagnosis, unsafe progression, or plans without enough goal and schedule context.
- Required context is missing and cannot be reasonably inferred.
- A more specific skill in this repo is a better match.

## Workflow

1. Identify the exact task and available source material.
2. Apply the domain rules and output format in this skill.
3. State assumptions, uncertainty, and missing inputs clearly.
4. Return the requested artifact, recommendation, or review in a practical format.
5. Check the result against the validation checklist before finishing.

Build practical training plans for Mick with a bias toward structured progression, measurable outcomes, and realistic recovery.

## Trigger When

- The user starts with `program`
- The user asks for a training plan or block
- The user wants race prep, strength cycles, or hybrid programming
- The user asks how to train for pull ups, cycling, triathlon, muscle gain, or cutting
- The user wants to reorganize training volume, split, or progression
- The user wants a season plan or phased training layout

## Athlete Profile

- Age: 51
- Bodyweight: 199 lbs
- Body fat: 18.7%
- Goal: maximum muscle growth while cutting toward 15% body fat
- Training location: YMCA Springfield TN plus home gym
- Home equipment: trap bar, pull-up bar, dumbbells, bench
- TRT: 737 ng/dL, managed by a urologist

## Safety Rules

- Zero axial loading on the spine
- No barbell squats, barbell lunges, or overhead barbell press
- Prefer machine or stable free weight options when risk rises
- Be conservative with calf overload when Achilles irritation risk is present
- Never recommend programming that ignores back safety or recovery signals

## Planning Priorities

- Build around the actual weekly schedule
- Match training to the stated goal instead of giving generic balanced programming
- Keep progress measurable
- Favor repeatable progression over novelty
- Make recovery realistic for the total workload

## Program Presets

When the user does not want to start from scratch, support these presets:

- **Pull up focus**: prioritize vertical pulling frequency, bodyweight strength, grip, and upper back support work
- **Cycling power**: prioritize lower body force production, fatigue control, and bike-supportive conditioning
- **Triathlon base**: prioritize durable swim, bike, and run consistency with controlled strength maintenance
- **Recomposition**: prioritize muscle retention or gain while controlling total fatigue and recovery cost during a cut

## Core Workflows

### Build A Training Block

When the user wants a program or block:

- define the primary goal
- identify the minimum effective weekly structure
- assign the main training days
- choose the key lifts, endurance sessions, or mixed sessions
- define progression for each focus area
- state the block length and what success should look like

Use a structure like:

```text
Goal:
Block length:
Weekly split:
Key sessions:
Progression:
Recovery focus:
Success markers:
```

### Match Programming To Goal

When the user names a goal such as pull ups, cycling, triathlon, body recomposition, or hybrid performance:

- bias the weekly structure toward that goal
- call out what gets priority
- state what is maintained rather than pushed
- note conflicts between simultaneous goals instead of pretending there are none

Use the closest preset first when it helps the user get to a working structure faster.

### Build A Hybrid Season

When the user wants multiple goals trained at once:

- separate the season into phases
- define what each phase emphasizes
- control interference between endurance and strength work
- use the smallest practical volume that still moves the secondary goal

### Annual Season Architecture

When the user wants a longer horizon plan:

- rotate strength, endurance, and hybrid emphasis blocks intentionally
- show how one phase feeds the next
- keep total yearly stress realistic
- tie each phase to a practical purpose such as base building, power, event prep, recomposition, or strength rebuilding

### Progression Logic

When giving a plan, specify how progression works:

- weight progression
- rep progression
- interval or duration progression
- deload or reset triggers
- when to hold steady instead of pushing harder

Do not leave progression as vague advice.

### Fatigue And Recovery Adjustment

When the user reports performance drop off, soreness, poor recovery, or schedule stress:

- identify whether the issue is volume, intensity, frequency, exercise selection, or life load
- reduce or shift stress in the smallest useful way first
- protect the primary goal instead of flattening the whole program blindly
- state what to watch over the next week before pushing progression again

### Weekly Review And Adjustment

When the user wants the program adjusted:

- compare the current plan against performance and recovery
- suggest the smallest useful change first
- identify whether the issue is volume, intensity, exercise selection, schedule, or recovery
- keep changes tied to the stated goal

### Exercise Substitution Guidance

When the current exercise choice conflicts with pain, equipment limits, or safety constraints:

- suggest substitutions that preserve the training effect as closely as possible
- account for back safety and any current injury notes
- keep the substitute simple and available in the real training environment
- explain the reason for the swap briefly

### Session Templates

When building or adjusting a block, define each recurring session as a template so the week is concrete:

- `gym strength`: warm-up pattern, 2 to 3 primary movements with progression scheme, accessory block, total time estimate
- `endurance support`: type (ride, run, swim, row), target zone or pace, duration, and what it must not interfere with
- `brick day`: ordered pairing such as bike to run, transition target, and combined fatigue budget
- `recovery week session`: reduced-volume versions of the same templates so a lighter week keeps the same skeleton

A plan is done when every training day in the split points at one of these templates.

### Failure Point Diagnosis

When a lift, pace, or benchmark stalls, identify which of three causes the evidence supports before changing anything:

- `recovery`: stalls cluster across unrelated movements, sleep or energy notes are poor, or performance dips follow dense weeks. Fix the recovery input, not the program.
- `progression design`: the jump sizes are too big, the rep targets outpace strength gain, or the same scheme has run unchanged past its useful life. Change the progression scheme.
- `exercise choice`: the stalled movement irritates a known problem area or trains the goal indirectly. Substitute, do not push.

Name the diagnosis explicitly and change one variable at a time so the next review can tell whether it worked.

### Equipment Constrained Variants

Every plan should run in both of Mick's real environments. When writing a block:

- mark each session as `YMCA`, `home`, or `either`
- for YMCA sessions, prefer the machine selection that the safety rules favor
- for home sessions, build around trap bar, pull-up bar, dumbbells, and bench only
- provide a home fallback for any YMCA-only session so a missed gym day does not break the week

### Phased Nutrition Prompts

When the user wants nutrition guidance attached to a program:

- match the prompt to the training phase
- support bulk, cut, endurance build, and race week priorities
- focus on intake timing, protein, carbohydrate emphasis, hydration, and recovery need
- keep the nutrition notes practical and phase-specific rather than generic

### Benchmark Review

When the user wants to know whether the current block is working:

- define the target metrics for the block
- compare current performance against those metrics
- state whether the block is moving as intended, stalled, or drifting
- recommend continue, adjust, or deload based on the evidence

### Event Countdown Planning

When the user has a race, event, or target milestone date:

- anchor the plan to the countdown
- break the remaining time into useful phases
- define what should be built now, what should peak later, and what should taper
- call out the latest reasonable point for harder progression

### Fitness Log Integration

When recent logs from `fitness-log` are available:

- use them as the evidence base for the next programming adjustment
- let trend summaries, missed sessions, recovery notes, and actual performance shape the recommendation
- keep the handoff explicit so the user can see how the logged data changed the plan
- do not pretend the adjustment is data-driven if no log evidence was provided

## Output Rules

- Use direct, coach-like language
- No motivational fluff
- Keep plans concrete enough to run
- Prefer tables or compact blocks when they make the plan easier to follow
- State assumptions when the user has not provided schedule, equipment, or current level details

When useful, include:

- the chosen preset
- the benchmark metrics
- the recovery adjustment trigger
- the next review point

## Example Prompts

```text
program build me an 8 week pull up focused strength block that still keeps leg strength moving
```

```text
program give me a hybrid season plan for strength plus triathlon without wrecking recovery
```

```text
program rewrite my current split for muscle gain while cutting and keep it back safe
```

```text
program compare a cycling focused week against a pull up focused week and show the tradeoffs
```

```text
program build a triathlon base block that can adjust automatically if recovery drops after hard bike days
```

```text
program use my recent fitness-log trends to adjust the next 4 weeks and tell me if the block is still moving the right metrics
```

## Validation Checklist

- [ ] The plan matches the stated goal
- [ ] Weekly structure is realistic for the schedule
- [ ] Progression is specific and measurable
- [ ] Program presets match the user goal when used
- [ ] Recovery adjustments are concrete and not generic
- [ ] Exercise substitutions preserve the intended training effect while respecting safety constraints
- [ ] Nutrition prompts match the current phase
- [ ] Benchmark reviews check the intended metrics directly
- [ ] Annual season plans show clear phase purpose
- [ ] Fitness-log handoff is explicit when recent logs are provided
- [ ] Event countdown plans map the remaining timeline clearly
- [ ] Safety constraints are enforced
- [ ] Recovery demands are acknowledged
- [ ] Hybrid plans call out tradeoffs instead of hiding them

## Help And Examples

If the user is not sure how to use this skill, asks what it needs, or asks for examples:

- Explain in plain language what this skill can do.
- Tell the user the minimum input needed for a useful first pass.
- Show the example prompts below.
- Offer the fastest next prompt the user can send.

Minimum useful input:

- Your goal, schedule, constraints, and training level.

Example prompts:

- `Use fitness-programming to build me a 4 week pull up focused strength block around triathlon training.`
- `Create a cycling and strength program that fits 6 training days with one lighter recovery day.`
- `Show me the best example prompt for asking this skill for a structured training block.`

