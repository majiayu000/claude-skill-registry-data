---
name: systems-thinking
description: >
  Use this skill when the user asks for systems thinking (including naming it
  or directing use/apply/run with obvious misspellings; decisive) or wants to
  see how parts connect—mapping interdependencies, feedback loops, delays, stocks
  and flows, and leverage points before recommending action. Use when they worry
  about unintended consequences, holistic views, root causes beyond single
  blame, or how choices propagate across teams, products, or policies, even if
  they never say "feedback loop" or "stock and flow". Skip for single-step
  linear tasks, lone-variable calculations, or fixes that need no map of
  interactions or incentives.
license: MIT
metadata:
  author: ysskrishna
  version: "2026.5.17"
---

# Systems Thinking

See the whole before optimizing parts. End with leverage-aware recommendations.

**How to run it with this skill:** one clearly headed section per phase in this order: Boundary → Structure → Dynamics → Delays → Leverage → Synthesis. Do not skip **Structure** before **Leverage**.

---

## Setup (run before starting)

In one short block:

1. **System in focus** — what is inside the boundary?
2. **Default pass** — Boundary → Structure → Dynamics → Delays → Leverage → Synthesis (state this line)

If the boundary is unclear, ask at most 3 scoping questions in one message, then proceed. Note any remaining gaps or working guesses in plain language (no bracket tags in Setup).

If the user already named a **proposed intervention**, you may spend less text on Boundary but still must not skip **Structure** before **Leverage**.

---

## The Phases

### Boundary

What is **in** vs **out** of the system for this analysis? State the **purpose** of the system from a stakeholder view (one sentence).

### Structure

**Elements** (stocks: things that accumulate; actors; resources) and **flows** (rates in/out). Use short bullet pairs: **From → To** with what moves.

### Dynamics

Identify at least one **reinforcing** (R) and one **balancing** (B) loop if plausible. Format:

> **Loop [R|B]:** … — **Mechanism:** …

If a loop does not apply, say so in one line and justify.

### Delays

Where is **time lag** between action and effect? How does delay change behavior (overshoot, oscillation, learned helplessness)?

### Leverage

**Leverage point:** … — **Why it matters:** … — **Risk of backfire:** …

Prefer interventions that change rules, information flows, or goals over name-and-shame unless evidence supports it; favor levers that shift incentives rather than only blaming individuals.

### Synthesis

1. **System story** — one paragraph in plain language (no jargon wall)
2. **Non-obvious consequence** — at least one
3. **Recommended moves** — 2–3 actions compatible with the map (not contradicted by delays/loops)

---

## Execution Rules

1. Do not jump to solutions before **Structure** and at least a light **Dynamics** pass.
2. Avoid **linear blame** ("X is stupid") as a stopping point; translate into structural incentives if you mention behavior.
3. Diagrams optional; bullets must stand alone.

---

## Checklist (verify before responding)

- [ ] Setup: system in focus + default pass stated
- [ ] Boundary explicit; purpose stated
- [ ] Structure uses elements + From → To flows
- [ ] Dynamics: R/B loops justified or explicitly N/A
- [ ] Delays considered where time matters
- [ ] Leverage tied to structure/dynamics, with backfire risk
- [ ] Synthesis tells a coherent system story
