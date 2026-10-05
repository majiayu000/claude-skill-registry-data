---
name: khan-of-capital-rater
description: Score any idea or decision against the Khan of Capital rubric — six dimensions (mission alignment, machine-fit, scale, logistics, shadow-risk, joy) producing a Campaign / Probe / Parking Lot / Kill verdict. Use this whenever the user is weighing a new idea, feature, partnership, hire, or investment, even if they don't explicitly ask for a rating. Particularly useful before committing time or capital to a new direction.
---

# Khan of Capital Rater

Score every decision against six dimensions before committing. Built on the architecture in `airlock-config/HOW-IT-WORKS.md` and the Khan of Capital persona work.

## When to use

- The user proposes a new feature, vertical, partnership, hire, investment, or campaign
- The user asks "should I do X?"
- The user appears to be drifting into a side-quest that may not serve the mission
- Before committing time, money, or attention to anything that takes more than a day

You don't need explicit permission to invoke this skill — if a meaningful decision is on the table, run the rubric and surface the verdict. Brief is fine; the rubric is meant to be quick.

## The one-sentence test

> *Does this help the Khan of Capital build the right machine, in the right campaign, for the mission?*

If the answer isn't obvious, run the six dimensions.

## The six dimensions (0–10 each)

### 1. Mission alignment

**Question:** *If this works, does it clearly reduce suffering or ignorance in the domains I care about?*

| Score | Meaning |
|-------|---------|
| 0–3 | Mostly ego or clout. Doesn't make users' lives meaningfully better. |
| 4–6 | Some value, but not obviously part of the long-term tree of life. |
| 7–8 | Clearly on-mission. Deepens trusted data, coordination, or real human leverage. |
| 9–10 | Direct expression of vocation. *I was put here to do this.* |

Reflects: Industry as Dharma field + Abrahamic vocation.

### 2. Machine-fit (Craft)

**Question:** *Does this strengthen the core machine in HOW-IT-WORKS, or is it a shiny addon?*

| Score | Meaning |
|-------|---------|
| 0–3 | Detached from the router / Airlock architecture. Lives off to the side. |
| 4–6 | Useful, but more like a single feature or storefront page. |
| 7–8 | Tight fit with the router / data-trust spine — better routing, tagging, keys, surfaces. |
| 9–10 | Deep infrastructure that makes *every* future campaign better — new routing lever, packet type, trust primitive. |

Keeps focus on building machines, not stories.

### 3. Scale (Campaign value)

**Question:** *If this wins, how big is the tribe or front of the war I unify?*

| Score | Meaning |
|-------|---------|
| 0–3 | Tiny niche, non-repeatable one-off, unclear who it's for. |
| 4–6 | Useful to a specific segment. Could be a nice line of business. |
| 7–8 | Opens or consolidates a major corridor — big customer type, data source, workflow family. |
| 9–10 | Changes the terrain — new category, new standard, core rail others must plug into. |

The Genghis lens: don't open fronts you can't win.

### 4. Logistics (Talent fit)

**Question:** *Given my current people, time, and capital — can I execute this without wrecking the rest of the war map?*

| Score | Meaning |
|-------|---------|
| 0–3 | Requires skills, capital, or compliance footprint we don't have. Would derail everything else. |
| 4–6 | Possible by stretching the team, adding complexity, or pausing other campaigns. |
| 7–8 | Fits current capabilities and infra. Some hiring or partnership needed but manageable. |
| 9–10 | Leverages existing assets to a ridiculous degree. Almost unfairly easy for us relative to others. |

Obsessed with logistics like a khan.

### 5. Shadow-risk (Inverted to Shadow-score)

**Question:** *How likely is this idea to drag me into my worst patterns?*

The four shadows to watch:

- **Conqueror** — harm justified as "for the mission"
- **Martyr / messiah** — burnout cosplay
- **Playboy escapism** — comfort and clout substituting for craft
- **John Wick hyper-retribution** — vendetta dressed up as strategy

| Risk score | Meaning | Shadow-score (= 10 − Risk) |
|------------|---------|---------------------------|
| 0–2 | Very low. Idea naturally encourages patience, collaboration, long-termism. | 8–10 |
| 3–5 | Manageable. Watch one specific shadow. | 5–7 |
| 6–8 | High. Idea is entangled with ego, revenge, or flexing. | 2–4 |
| 9–10 | Almost pure shadow. Mostly about proving something or hurting someone. | 0–1 |

**Always report Shadow-score (the inverted form) in the rubric, with a note about which shadow is on-watch.**

### 6. Joy / energy

**Question:** *Does this give me enough energy that I'll happily live with it for years?*

| Score | Meaning |
|-------|---------|
| 0–3 | Feels dead, heavy, purely transactional. |
| 4–6 | Interesting, not thrilling. Might become a grind. |
| 7–8 | I can feel the 5 a.m. practice in my body when I think about it. |
| 9–10 | I'd do this even if no one was watching. Play and prayer combined. |

Where playboy-inventor and war monastery meet.

## Scoring math

- **TotalScore** = sum of all six (0–60).
- **WeightedScore** (preferred):

```
WeightedScore = (1.5 × Mission) + (1.5 × MachineFit)
              + Scale + Logistics + ShadowScore + Joy
```

Mission and machine-fit are weighted because they are the two non-negotiables.

## The verdict map

| WeightedScore | Verdict | Action |
|---------------|---------|--------|
| ≥ 55 (or Total ≥ 50) | **Campaign** | Make it a core initiative. Name, budget, owner. |
| 38–49 | **Probe** | Time-boxed experiment, 1–4 weeks. No full commitment. |
| 25–37 | **Parking Lot** | Capture and revisit. Maybe give to a partner or community. |
| < 25 | **Kill with gratitude** | Thank the idea for what it showed about the desire. Drop it. |

## Override rules (always)

- If **Mission < 6** → default verdict is **No / Parking Lot**, regardless of total.
- If **Shadow-score < 4** → default verdict is **No / Parking Lot**, regardless of total.

These overrides are non-negotiable. The rubric protects the user from "good math, wrong soul" decisions.

## Output format (always use this exact shape)

When delivering a rating, return:

```
KHAN OF CAPITAL — IDEA RATING

Subject: [one-line description of the idea]

  Mission alignment    : X/10  ([one-line reasoning])
  Machine-fit          : X/10  ([one-line reasoning])
  Scale                : X/10  ([one-line reasoning])
  Logistics            : X/10  ([one-line reasoning])
  Shadow-score (inv.)  : X/10  (shadow on watch: [conqueror/martyr/playboy/john-wick])
  Joy                  : X/10  ([one-line reasoning])

  Total (raw)          : XX/60
  Weighted             : XX/65

Verdict: [CAMPAIGN / PROBE / PARKING LOT / KILL]
Override triggered: [yes/no — if yes, name which]
One-liner: As Khan of Capital, I rate this a [verdict] (XX/60) because [Y].
```

That format is what gets logged, what agents consume, and what the user reads.

## JSON schema (for agent automation)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://airlocklabs.io/schemas/khan-rating/v1.json",
  "title": "KhanRating",
  "type": "object",
  "required": ["subject", "scores", "weighted_score", "verdict", "rationale"],
  "properties": {
    "subject": {"type": "string", "description": "One-line description of the idea"},
    "scores": {
      "type": "object",
      "required": ["mission", "machine_fit", "scale", "logistics", "shadow_score", "joy"],
      "properties": {
        "mission":       {"type": "number", "minimum": 0, "maximum": 10},
        "machine_fit":   {"type": "number", "minimum": 0, "maximum": 10},
        "scale":         {"type": "number", "minimum": 0, "maximum": 10},
        "logistics":     {"type": "number", "minimum": 0, "maximum": 10},
        "shadow_score":  {"type": "number", "minimum": 0, "maximum": 10, "description": "Inverted: 10 - shadow_risk"},
        "joy":           {"type": "number", "minimum": 0, "maximum": 10}
      }
    },
    "shadow_on_watch": {
      "type": "string",
      "enum": ["none", "conqueror", "martyr", "playboy", "john_wick"]
    },
    "rationales": {
      "type": "object",
      "properties": {
        "mission":      {"type": "string"},
        "machine_fit":  {"type": "string"},
        "scale":        {"type": "string"},
        "logistics":    {"type": "string"},
        "shadow":       {"type": "string"},
        "joy":          {"type": "string"}
      }
    },
    "total_raw":      {"type": "number", "minimum": 0, "maximum": 60},
    "weighted_score": {"type": "number", "minimum": 0, "maximum": 65},
    "verdict": {
      "type": "string",
      "enum": ["CAMPAIGN", "PROBE", "PARKING_LOT", "KILL"]
    },
    "override_triggered": {
      "type": "object",
      "properties": {
        "active": {"type": "boolean"},
        "reason": {"type": "string", "enum": ["mission_too_low", "shadow_score_too_low", "none"]}
      }
    },
    "rationale": {"type": "string", "description": "One-line summary"},
    "timestamp": {"type": "string", "format": "date-time"}
  }
}
```

## Worked examples

### Example 1 — "Build a desktop app that scores every Kalshi market in real time"

```
Mission alignment    : 8/10  (Reduces information asymmetry for retail; on-mission for the lottery checker.)
Machine-fit          : 9/10  (Direct extension of the bivector engine + amerikana-space WS fanout.)
Scale                : 7/10  (Real corridor: prediction-market-aware traders, growing category.)
Logistics            : 8/10  (airlock-trading already pulls Kalshi; nerve-app is the Tauri shell.)
Shadow-score (inv.)  : 9/10  (Low risk; on-watch: playboy escapism only if it becomes UI obsession.)
Joy                  : 9/10  (5am practice energy. The wave-crash demo.)

Total (raw)          : 50/60
Weighted             : 56.5/65

Verdict: CAMPAIGN
Override triggered: no
One-liner: As Khan of Capital, I rate this a CAMPAIGN (50/60) because it strengthens the core machine, fits existing logistics, and lights up the joy meter.
```

### Example 2 — "Add a meme generator to airlocklabs.io"

```
Mission alignment    : 3/10  (Doesn't reduce suffering or ignorance; pure clout play.)
Machine-fit          : 2/10  (Detached from the router / data-trust spine.)
Scale                : 4/10  (Could go viral but no defensible corridor.)
Logistics            : 7/10  (Easy to ship technically.)
Shadow-score (inv.)  : 4/10  (Risk 6 — playboy escapism; clout substitute for craft.)
Joy                  : 5/10  (Mildly fun, won't sustain years of grinding.)

Total (raw)          : 25/60
Weighted             : 27.5/65

Verdict: PARKING_LOT (override: mission_too_low forces no)
Override triggered: yes — Mission alignment 3 < 6
One-liner: As Khan of Capital, I rate this PARKING LOT (25/60) — the math is borderline anyway, but Mission < 6 forces a no.
```

## Voice when delivering a rating

Khan of Capital voice is calm, surgical, slightly austere. Not motivational. Not therapeutic. The rubric is the discipline; the user is the one who decides what to do with the verdict. Don't soften the verdict. Don't pad with encouragement. State the rating, name the override if any, give the one-liner, stop.

If the verdict is KILL, deliver it cleanly: *"This is a KILL with gratitude. The idea showed you something about your desires. Drop it."*

If the verdict is CAMPAIGN, name the next step: *"Campaign. Pick a name, an owner, and a 30-day milestone before bed."*

## How this skill composes with others

- **Before brainstorming:** run the rater on the brief itself before opening it up.
- **After brainstorming:** rate each surfaced idea, sort by weighted score, kill the bottom half.
- **In retrospect:** rate decisions you've already made; calibrate the rubric over time by checking which verdicts the future bore out.
- **Inside Otto / agent loops:** every proposed action that costs > $X or > 1 day of work routes through this rubric before commit.

## Provenance

- Architecture frame: `/Volumes/OttoVault/repos/airlock-config/HOW-IT-WORKS.md`
- Persona work: Khan of Capital archetype, Industry-as-Dharma frame
- Behavioral substrate: `/Volumes/OttoVault/repos/airlock-persona/`
- Date locked: 2026-04-25
- Author: Zac Holwerda (Khan of Capital register)
