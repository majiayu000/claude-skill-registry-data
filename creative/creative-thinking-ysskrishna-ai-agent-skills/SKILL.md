---
name: creative-thinking
description: >
  Use this skill when the user asks for creative thinking (including naming it
  or directing use/apply/run with obvious misspellings; decisive) or wants
  divergent ideation—fluency, flexible perspectives, novel combinations, and
  elaboration, with optional light convergence. Use when they want fresh ideas,
  blue-sky options, reframes, or more variety before committing, including casual
  or messy prompts. Skip when they want a single delivered answer with no
  exploration, audit-only teardown with no generation asked for, or purely
  mechanical execution.
license: MIT
metadata:
  author: ysskrishna
  version: "2026.5.17"
---

# Creative Thinking

Defer judgment during divergence. Keep **generate** (Prime, Diverge, Connect) separate from **Harvest** (pick and plan).

**How to run it with this skill:** one clearly headed section per phase in this order: Prime → Diverge → Connect → Harvest. Optional **Perspectives** beat only when noted in Setup.

---

## Setup (run before starting)

In one short block:

1. **Creative brief** — goal, audience, constraints (time, tone, taboos)
2. **Default pass** — Prime → Diverge → Connect → Harvest (state this line)

If constraints are missing, ask at most 3 clarifying questions in one message, then proceed. Note any remaining gaps or working guesses in plain language (no bracket tags in Setup).

If the user is **stuck on one framing**, add a short **Perspectives** beat before **Diverge**: Optimist / Skeptic / Outsider — two reframes each, no cross-critique yet.

---

## The Phases

### Prime

Warm context in 2–4 bullets: what would **delight** or **surprise** success look like? What must **not** be violated?

### Diverge

Quantity first. Produce a **substantive** list of ideas (no fixed count unless the user asks for one). Tag ideas `F` (flexible reuse of existing), `N` (novel twist), or `W` (wild — may be impractical).

Use at least **two** different creative triggers drawn from: **analogy** (unrelated domain), **constraint flip** (remove/add a rule), **user fantasy** (absurd ideal), **time shift** (past/future), **scale shift** (micro/macro).

### Connect

Combine or **mash** ideas: **A + B →** hybrid concept in several lines (aim for multiple mashups, fewer than Diverge but not a single mashup unless the brief is tiny).

### Harvest

1. **Top picks** — 3 ideas with **selection rationale** tied to the brief
2. **Next creative step** — e.g. prototype storyboard, user interview, spike, moodboard
3. **Parking lot** — 2 promising ideas deferred (why deferred)

---

## Execution Rules

1. No harsh criticism in **Prime**, **Diverge**, or **Connect**; park risks for a separate pass if the user asks.
2. Do not pretend user research happened; label speculative benefits as hypothetical.
3. One response for all phases unless the user requests pacing.

---

## Checklist (verify before responding)

- [ ] Setup: brief + default pass (and optional Perspectives if used)
- [ ] Diverge uses two+ triggers; ideas tagged F/N/W where applicable
- [ ] Connect present with multiple mashups
- [ ] Harvest has top picks + next step + parking lot
