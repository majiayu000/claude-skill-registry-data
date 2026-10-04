---
name: Cat
slug: cat
version: 1.0.0
description: Track cat health, litter, routines, behavior, travel, and vet coordination with species-aware memory and emergency triage.
homepage: https://clawic.com/skills/cat
changelog: Initial release with cat care tracking, litter and behavior workflows, travel prep, and emergency-safe vet coordination.
metadata:
  clawdbot:
    emoji: 🐈
    requires:
      bins: []
    os:
    - linux
    - darwin
    - win32
    configPaths:
    - ~/Clawic/data/cat/
    displayName: Cat
  openclaw:
    requires:
      config:
      - ~/Clawic/data/cat/
---

## Setup

On first use, read `setup.md` for activation preference, local memory approval, and the current cat roster. Keep setup light and continue helping immediately.

## When to Use

User talks about a cat or kitten they live with, foster, rescue, or regularly care for. Agent helps with symptom triage, litter tracking, routines, behavior, home setup, travel, vet logistics, shopping, and memories.
Use this for real cat-care operations, not for generic animal trivia, memes, or fictional cats.

## Architecture

Memory lives in `~/Clawic/data/cat/`. See `memory-template.md` for structure.

```text
~/Clawic/data/cat/
├── memory.md           # Household summary, activation, red flags, shared rules
├── cats/
│   └── {name}/
│       ├── profile.md
│       ├── timeline.md
│       ├── health.md
│       ├── routines.md
│       ├── behavior.md
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
| Behavior patterns and interventions | `behavior.md` |
| Home setup and multi-cat environment | `household.md` |
| Travel, moving, and sitter prep | `travel.md` |
| Records, meds, shopping, and reports | `records.md` |

## Scope

This skill ONLY:
- Helps manage real-world cat care, records, logistics, and behavior tracking.
- Uses local files in `~/Clawic/data/cat/` if the user approves memory.
- Gives conservative triage and preparation support for veterinary conversations.

This skill NEVER:
- Diagnoses diseases or claims certainty from short descriptions alone.
- Recommends medication doses, human medicines, or home toxicology fixes.
- Delays emergency care when cat-specific red flags appear.
- Writes memory without user approval.

## Core Rules

### 1. Start with Cat-Specific Triage
Use `triage.md` before giving advice on symptoms or sudden changes.

Check the smallest set of facts needed to judge risk:
- age and life stage
- sex if urinary risk matters
- indoor or outdoor access
- appetite, water, energy, and hiding
- litter box output and vomiting
- toxins, trauma, and current medication

If breathing trouble, collapse, repeated nonproductive retching, major trauma, toxin exposure, or straining without urine appears, switch to emergency guidance immediately.

### 2. Keep One Living Record Per Cat
Use `records.md` and `memory-template.md` to keep each cat's facts stable across sessions.

Store durable facts such as:
- identity, age range, microchip, and household role
- conditions, allergies, meds, and regular vet details
- reliable food, litter, handling, and travel preferences
- ongoing behavior patterns and major milestones

Separate confirmed facts from guesses, and log dates for symptom changes, appointments, and treatments.

### 3. Litter, Appetite, and Hiding Are Primary Signals
Cats hide decline early. Give extra weight to:
- new litter box avoidance or straining
- reduced appetite or unusual thirst
- hiding, withdrawal, or reduced grooming
- sudden aggression, vocalization, or mobility change

Do not frame these as attitude problems until health and environment have been checked.

### 4. Solve Behavior Through Environment Before Force
Use `behavior.md` and `household.md` to fix patterns with setup, routine, and stress reduction.

Prefer:
- litter box changes
- vertical territory and hiding spots
- better scratching options
- shorter, more predictable handling
- introductions done through distance and scent

Avoid punishment, forced exposure, or dog-style obedience assumptions.

### 5. Plan Around Territory and Stress
Cats usually care more about safety, predictability, and control than novelty.

When the user mentions:
- visitors
- a new pet or baby
- travel or moving
- carrier fights
- boarding or sitter handoff

load `travel.md` or `household.md` and reduce the plan to the least stressful path.

### 6. Coordinate Logistics Proactively but Safely
Use `records.md` for vet prep, meds, shopping, and sitter packs.

Support:
- appointment prep with concise questions and timeline
- medication schedules and refill tracking
- food, litter, and supply reorder thresholds
- clean exportable instructions for cat sitters

Do not invent doses, do not reinterpret lab results as diagnosis, and do not tell the user to wait when red flags are active.

### 7. Preserve Moments Without Polluting the Main Record
Track memories and milestones, but keep the hot memory small.

Keep in the per-cat timeline:
- adoption and birthdays
- first successful carrier ride or medication win
- behavior breakthroughs
- travel or introduction milestones
- memorable stories worth resurfacing later

Do not clutter the shared memory file with every cute anecdote.

## Common Traps

- Treating litter box changes as defiance -> misses one of the highest-signal cat health and stress indicators.
- Using punishment for scratching, biting, or hiding -> increases fear and makes the pattern harder to read.
- Ignoring low appetite because the cat still takes treats -> underestimates how quickly cats can deteriorate.
- Planning travel only on the day of departure -> guarantees avoidable carrier and handling stress.
- Storing every conversation detail as memory -> makes the skill slower and less accurate in future sessions.

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
- household summary and activation preference in `~/Clawic/data/cat/memory.md`
- one per-cat record with profile, health, routines, behavior, and logistics
- supply thresholds and sitter notes

**This skill does NOT:**
- access files outside `~/Clawic/data/cat/` for storage
- send cat data to third parties
- create automations or reminders automatically
- replace veterinary care for emergencies or diagnosis

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/<slug> (install if the user confirms):
- `memory` - persistent local memory patterns for durable pet context
- `remind` - reminder workflows for meds, appointments, and recurring care
- `shopping` - purchase planning and reorder support for food and supplies
- `travel` - transport and trip planning support when a cat is moving with the user
- `photos` - organize pet photos and help with albums or memory keepsakes

## Feedback

- If useful, star it: https://clawic.com/skills/cat
- Latest version: https://clawic.com/skills/cat
