---
name: Dog
slug: dog
version: 1.0.0
description: Track dog health, walks, training, routines, travel, and vet coordination with species-aware memory and emergency triage.
homepage: https://clawic.com/skills/dog
changelog: Initial release with dog care tracking, walking and training workflows, travel prep, and emergency-safe vet coordination.
metadata:
  clawdbot:
    emoji: 🐕
    requires:
      bins: []
    os:
    - linux
    - darwin
    - win32
    configPaths:
    - ~/Clawic/data/dog/
    displayName: Dog
  openclaw:
    requires:
      config:
      - ~/Clawic/data/dog/
---

## Setup

On first use, read `setup.md` for activation preference, local memory approval, and the current dog roster. Keep setup light and continue helping immediately.

## When to Use

User talks about a dog or puppy they live with, foster, rescue, or regularly care for. Agent helps with symptom triage, walks, training, behavior, routines, travel, vet logistics, shopping, and memories.
Use this for real dog-care operations, not for generic animal trivia, memes, or fictional dogs.

## Architecture

Memory lives in `~/Clawic/data/dog/`. See `memory-template.md` for structure.

```text
~/Clawic/data/dog/
├── memory.md           # Household summary, activation, red flags, shared rules
├── dogs/
│   └── {name}/
│       ├── profile.md
│       ├── timeline.md
│       ├── health.md
│       ├── routines.md
│       ├── behavior.md
│       ├── training.md
│       └── logistics.md
├── shopping.md         # Shared supplies and reorder thresholds
└── sitter-packs/       # Exportable care instructions for trips or absences
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup process | `setup.md` |
| Memory template | `memory-template.md` |
| Emergency triage and intake | `triage.md` |
| Daily, weekly, and monthly care | `routines.md` |
| Training and handling patterns | `training.md` |
| Behavior patterns and escalation | `behavior.md` |
| Travel, boarding, and sitter prep | `travel.md` |
| Records, meds, shopping, and reports | `records.md` |

## Scope

This skill ONLY:
- Helps manage real-world dog care, records, logistics, walks, and behavior tracking.
- Uses local files in `~/Clawic/data/dog/` if the user approves memory.
- Gives conservative triage and preparation support for veterinary conversations.

This skill NEVER:
- Diagnoses diseases or behavior disorders with certainty from chat alone.
- Recommends medication doses, human medicines, or unsafe home toxicology fixes.
- Uses punishment-heavy training advice as the default path.
- Writes memory without user approval.

## Core Rules

### 1. Start with Dog-Specific Triage
Use `triage.md` before giving advice on symptoms or sudden changes.

Ask only for the facts that change risk:
- age and life stage
- size if heat or bloat risk matters
- appetite, water, stool, urine, and energy
- vomiting, diarrhea, coughing, limping, or pain signs
- toxins, trauma, overheating, and current medication
- whether the change happened during exercise, after eating, or after a specific trigger

If breathing trouble, collapse, seizure, toxin exposure, heavy bleeding, major trauma, heat injury, or a swollen abdomen with unproductive retching appears, switch to emergency guidance immediately.

### 2. Keep One Living Record Per Dog
Use `records.md` and `memory-template.md` to keep each dog's facts stable across sessions.

Store durable facts such as:
- identity, age range, weight range, and microchip
- conditions, allergies, meds, and regular vet details
- normal walk load, feeding pattern, and elimination baseline
- training progress, triggers, and handling limits
- boarding, sitter, travel, and gear notes

Separate confirmed facts from guesses, and date symptom changes, incidents, appointments, and medication events.

### 3. Exercise and Enrichment Must Fit the Actual Dog
Use `routines.md` before prescribing more activity.

Match the plan to:
- age and recovery state
- breed tendencies without stereotyping
- weather and heat risk
- pain or mobility limits
- the dog's real threshold around people, dogs, bikes, or noise

Do not answer every problem with "more exercise."

### 4. Training Means Clear Cues and Reinforcement
Use `training.md` and `behavior.md` together.

Default to:
- one cue for one behavior
- reward timing that is immediate and repeatable
- distance from triggers before adding difficulty
- short sessions with clean resets
- management tools when the dog cannot yet succeed

Avoid punishment loops, flooding, and off-leash risk-taking when recall is not earned.

### 5. Behavior Plans Need Context, Not Just Labels
When the user says "reactive," "stubborn," "anxious," or "aggressive," ask what actually happened.

Track:
- trigger
- distance
- intensity
- duration
- recovery time
- what made it better or worse

Do not skip medical or pain review when a behavior changes fast.

### 6. Coordinate Logistics Proactively but Safely
Use `records.md` for vet prep, meds, shopping, and sitter packs.

Support:
- walk and medication schedules
- appointment prep and follow-up questions
- food and gear reorder thresholds
- boarding, sitter, and travel handoff instructions

Do not invent doses, do not tell the user to stop prescribed medication, and do not minimize heat or bloat warnings.

### 7. Preserve Progress and Memories Without Noise
Keep the shared memory file small, and use each dog's timeline for dated facts worth resurfacing later.

Good examples:
- a clean recall milestone
- first successful crate or car ride
- post-surgery recovery checkpoints
- major trip or boarding milestone
- memorable moments the user wants retained

Do not store every walk anecdote as hot memory.

## Common Traps

- Treating a pain-driven behavior shift as obedience failure -> can worsen both safety and trust.
- Using more intensity when the dog is already over threshold -> turns training into rehearsal of the problem.
- Telling the user to exercise through heat or illness -> creates avoidable medical risk.
- Calling off-leash reliability "good enough" before it is actually tested -> creates safety failures fast.
- Saving every small walk detail into memory -> makes future support noisy and less useful.

## External Endpoints

This skill makes no external network requests.

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| None | None | N/A |

No other data is sent externally.

## Security & Privacy

**Data that leaves your machine:**
- None.

**Data stored locally if approved by the user:**
- household summary and activation preference in `~/Clawic/data/dog/memory.md`
- one per-dog record with profile, health, routines, behavior, training, and logistics
- supply thresholds and sitter notes

**This skill does NOT:**
- access files outside `~/Clawic/data/dog/` for storage
- send dog data to third parties
- create automations or reminders automatically
- replace veterinary care for emergencies or diagnosis

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/<slug> (install if the user confirms):
- `memory` - persistent local memory patterns for durable pet context
- `remind` - reminder workflows for meds, appointments, and recurring care
- `shopping` - purchase planning and reorder support for food and supplies
- `travel` - transport and trip planning support when a dog is moving with the user
- `photos` - organize pet photos and help with albums or memory keepsakes

## Feedback

- If useful, star it: https://clawic.com/skills/dog
- Latest version: https://clawic.com/skills/dog
