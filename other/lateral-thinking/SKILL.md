---
name: lateral-thinking
description: >
  Use this skill when the user asks for lateral thinking (including naming it
  or directing use/apply/run with obvious misspellings; decisive) or wants to
  break a sticky pattern—provocations, concept fans, challenge questions, and
  deliberate reframes to escape local optima. Use when ideation feels stuck,
  options feel incremental, or they want surprising angles (including after
  conventional brainstorming stalls), even if they never say "lateral thinking"
  or "provocation". Skip when they need a single compliant rule lookup, tight
  logical proof with no exploration phase, or no appetite for playful what-if
  moves.
license: MIT
metadata:
  author: ysskrishna
  version: "2026.5.17"
---

# Lateral Thinking

Movement before judgment. Treat provocative lines as **stepping stones**, not final positions.

**How to run it with this skill:** one clearly headed section per move in the default order from Setup (Provocation (Po) → Extract principle → Concept fan → Candidates), or the alternate path the user chose.

---

## Setup (run before starting)

In one short block:

1. **Stuck point** — what pattern or assumption feels rigid?
2. **Default pass** — Provocation (Po) → Extract principle → Concept fan → Candidates (state this line)

If safety or legal constraints are unclear, ask at most 3 questions in one message before generating provocations. Note any remaining gaps in plain language (no bracket tags in Setup).

If the user asks for **random stimulus** instead of a Po, replace the **Provocation** step with **Random entry**: one random noun or image, then **several bridges** (property → analogy → mechanism → application) into ideas.

If the user asks to **challenge implicit rules**, replace **Provocation** / **Extract principle** / **Concept fan** with: list implicit rules → for each, **Challenge / Reframe / Test** (smallest experiment) → **Escape** (two ways to sidestep the load-bearing rule) → then **Candidates** only from that thread.

---

## The Moves

### Provocation

Offer **one primary Po** (statement can be illogical or impossible) formatted:

> **Po:** … — **Movement idea:** what useful idea does this **suggest** if we treat it as a springboard?

### Extract principle

From the movement idea, state **one operating principle** that *could* work in the real world (even if the Po itself is absurd).

### Concept fan

Widen from the principle along three directions — **broaden**, **deepen**, **redirect** — with **several branches** per direction unless the user wants more.

### Candidates

**Several** actionable ideas. Tag each: `near-term` / `stretch` / `experimental`.

---

## Execution Rules

1. Never present a **Po** as a factual recommendation; always pair with **Movement** or **Principle**.
2. If a provocation touches safety, ethics, or law, **stop** and surface the conflict explicitly — do not rationalize harm.
3. One response for all moves unless interactive pacing is requested.

---

## Checklist (verify before responding)

- [ ] Setup: stuck point + default pass (note if Random entry or rule-challenge path used)
- [ ] Po paired with movement; or alternate path completed as requested
- [ ] Concept fan has three directions with multiple branches each
- [ ] Candidates tagged near-term / stretch / experimental
- [ ] No Po presented as literal policy
