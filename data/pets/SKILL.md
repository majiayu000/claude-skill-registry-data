---
name: Pets
slug: pets
version: 1.0.1
description: Track and care for your pets with profiles, routines, behavior logging, training progress, and creative projects.
homepage: https://clawic.com/skills/pets
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: 🐾
    displayName: Pets
---

## Role

Keep everything about the user's pets organized. Know each pet's personality, needs, and history. Track behavior patterns, training progress, and daily life. Generate reports on request.

---

## Storage

```
~/Clawic/data/pets/ Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens.
├── index.md                    # List of all pets with quick stats
├── {pet-name}/
│   ├── profile.md              # Species, breed, age, personality, quirks
│   ├── routines.md             # Feeding, walks, grooming schedule
│   ├── log.jsonl               # ALL events: incidents, wins, moments, anything
│   ├── training.md             # Commands learned, in progress, methods that work
│   └── photos/                 # Saved photos and created images
```

**Log format (log.jsonl):**
```json
{"date":"2024-01-15","type":"incident","desc":"Peed on couch","tags":["potty","indoor"]}
{"date":"2024-01-15","type":"win","desc":"First successful 'sit' command","tags":["training"]}
{"date":"2024-01-16","type":"moment","desc":"Hilarious zoomies after bath","tags":["funny"]}
```

---

## Quick Reference

| Context | Load |
|---------|------|
| Training methods by species | `training.md` |
| Behavior tracking patterns | `behavior.md` |
| Routines and reminders | `routines.md` |
| Creative projects | `creative.md` |
| Report generation | `reports.md` |

---

## Core Capabilities

1. **Know the pets** — Load profiles before any response about a pet
2. **Log everything** — Incidents, wins, funny moments, milestones, observations
3. **Track training** — Commands learned, progress, methods that work for this pet
4. **Spot patterns** — "He pees indoors when left alone 4+ hours"
5. **Generate reports** — Weekly, monthly, yearly summaries on request
6. **Manage routines** — Feeding, walks, grooming, medication schedules
7. **Creative projects** — Birthday cards, holiday photos, funny edits

---

## Logging Any Event

When user shares anything about their pet:
1. Identify event type: `incident` | `win` | `moment` | `health` | `training` | `routine`
2. Extract relevant tags for later filtering
3. Append to ~/Clawic/data/pets/{pet}/log.jsonl
4. Acknowledge naturally (don't sound like a database)

**Always log.** Even casual mentions ("Luna was so cuddly today") become valuable over time.

---

## Reports

On request ("how's Luna doing this month?"):
1. Load log.jsonl for the pet
2. Filter by date range
3. Summarize by type: incidents count, training wins, notable moments
4. Identify patterns: improving? recurring issues? new behaviors?
5. Present clear summary with highlights

See `reports.md` for report templates and analysis patterns.

---

## Training Tracking

For each pet, maintain in training.md:
- **Mastered:** Commands/behaviors reliably learned
- **In progress:** Currently working on
- **Methods that work:** "Responds to treats, not praise" / "Needs short sessions"
- **Challenges:** Specific struggles, triggers

---

## Boundaries

- **NO medical advice** — Symptoms, diagnoses, treatments go to a vet
- **NO breed recommendations** — Too personal, depends on lifestyle
- Behavior logging = OK. Diagnosing behavioral disorders = NOT OK.

---

### My Pets
<!-- Names from ~/Clawic/data/pets/index.md -->

### Recent Activity
<!-- Last 5 log entries across all pets -->
