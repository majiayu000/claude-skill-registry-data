---
name: demo-script-architect
version: 1.0.0
description: Design and refine presenter-centric demo scripts — narrative flow over feature lists, visual-cue mapping, progressive capability reveals, query-to-explanation alignment, redundancy audits. Use when creating live demos, structured walkthroughs, or turning specs into engaging narratives.
---

# Demo Script Architect

Design and refine presenter-centric demo scripts that guide audiences through system capabilities in a natural, engaging narrative flow. Works for any technical or product demo.

## When to use

Creating live demonstration scripts; building structured walkthroughs of systems/features; designing progressive capability reveals; turning technical specs into engaging narratives; adding visual guidance for presenters.

## 1. Core principles

- **Narrative over features.** Each section builds on previous learning; bridge narration explains the *why*. Story arc: observe → understand → apply → verify. Conversational, not documentation-style.
- **Element documentation.** Always include element purpose when referenced: `YI-100 (pump status indicator)`. Help the audience understand what they're looking at.
- **Visual guidance mapping.** Map abstract references to actual visible elements. Data field `"status"` → point to the status icon/light. **Never point to something the audience can't see on screen.**
- **Query-to-explanation alignment.** The explanation must accurately describe what's being queried — don't claim "context-learning" if tags are explicit. Explain the mechanism (parallelization, routing, lookup) and set up expectation for the response.
- **No redundancy.** Don't repeat the same query/capability in consecutive demos. Build progressive revelation: basic → complex → combined → edge cases. Stack elements only when combining for a *new insight*.
- **Conversational tone.** Use contractions ("it's", "we've"). Direct the audience ("Watch", "Notice", "Observe"). Short punchy sentences over long lists. Tell a story.
- **Commentary interprets, doesn't restate.** Explains *significance*, not mechanics; sets up the next logical question.

## 2. Narrative section structure

Every demo follows the same six-part shape:

```
Demo Setup         → purpose, what to watch for
Visual Cue         → "[On screen: Point to X, watch Y]"
Action/Query       → explicit ask of the system
Processing         → 2-3 audience-friendly sentences on what's happening
Expected Responses → multiple outcomes based on system state
Commentary         → interpret results, relate to broader picture
```

## 3. Demo progression template

| # | Focus | New capability | Approach |
|---|---|---|---|
| 1 | Basics | Single element access | Explicit reference |
| 2 | Integration | Multiple related elements | Grouped query |
| 3 | Abstraction | Natural language, no explicit refs | System infers intent |
| 4 | Dynamics | Live data, change over time | Continuous monitoring |
| 5 | Accessibility | Different access methods | Voice/touch/alternative interface |
| 6 | Automation | System behavior without command | Observe automatic logic |
| 7 | Diagnostics | Troubleshooting scenario | Bundle related elements |
| 8 | Knowledge | Search/lookup capability | Find answers in resources |
| 9 | Control | Issue commands | Write operations + verification |

## 4. Anti-patterns

| Anti-pattern | Wrong | Right |
|---|---|---|
| Explanation/query mismatch | Query mentions `YI-100, SI-100, PIT-100`; explanation says "we didn't mention specific tags this time" | "Three different data points from two systems in parallel" |
| Pointing to invisible | "[Point to field `PIT-100` on screen]" when not labeled | "[Point to the pressure gauge display]" |
| Robotic narration | "System processes query, retrieves values from database, returns formatted response." | "Watch the system grab the values and hand them back as one answer." |
| Redundant demos | Demo 1 status query → Demo 2 same status query | Demo 1 status query → Demo 2 combine status with related data |
| Weak bridge | "Now let's do a different demo." | "Now that we know the status, let's check the pressure to see what it's delivering." |

## 5. Review checklist

- [ ] Each demo has a **Setup** explaining purpose
- [ ] **Actions/Queries** are explicit and clear
- [ ] **Processing** accurately describes what's happening
- [ ] Visual cues point to **visible screen elements**
- [ ] Element names include purpose: `NAME (what it does)`
- [ ] **Commentary** interprets results
- [ ] **Bridge narration** connects each demo to the next with a *why*
- [ ] No redundant queries (same action shown twice for same purpose)
- [ ] Multiple expected responses cover realistic system states
- [ ] Tone is conversational throughout (no robotic jargon)

## 6. Output deliverables

1. **Structured script** with the six-part narrative sections (§2).
2. **Visual element map** — reference → visible screen element.
3. **Demo flow diagram** showing connections and progression.
4. **Redundancy audit** — what was removed/consolidated and why.
5. **Presenter notes** — what to watch for, where to point, what to emphasize.
