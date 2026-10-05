---
name: design-thinking
description: >
  Use this skill when the user asks for design thinking (including naming it
  or directing use/apply/run with obvious misspellings; decisive) or wants
  human-centered exploration—empathizing with needs, framing the problem,
  ideating, prototyping intent, and defining what to learn next. Use for HCD,
  service or UX concept sprints, how-might-we style discovery before build, or
  reframing from user evidence, even with messy context. Skip when the spec is
  fully frozen and they want no discovery, or when the task is code-only
  maintenance with no user problem framing requested.
license: MIT
metadata:
  author: ysskrishna
  version: "2026.5.17"
---

# Design Thinking

Fall in love with the problem, not the first solution. End with **what to learn next**, not just ideas.

**How to run it with this skill:** one clearly headed section per stage in this order: Empathize → Define → Ideate → Prototype → Test plan.

---

## Setup (run before starting)

In one short block:

1. **Design challenge** — who is affected and in what situation?
2. **Default pass** — Empathize → Define → Ideate → Prototype → Test plan (state this line)

If users, constraints, or success signals are missing, ask at most 3 questions in one message, then proceed. Note any remaining gaps or working guesses in plain language (no bracket tags in Setup).

If **Empathize** is thin (no real user input), say so honestly in **Define** and keep the POV narrow instead of inventing research.

---

## The Stages

### Empathize

**Who** — primary user or stakeholder (facts from user vs `[INFERRED]`). **Jobs / pains / gains** — what they are trying to do and what hurts. **Context** — when/where the need shows up.

No fabricated quotes; paraphrase only what the user supplied.

### Define

**Insight statement** — non-obvious tension connecting pains and context. **Point of View (POV)** — "**[User]** needs **[verb]** because **[insight]**." **How Might We (HMW)** — 2–3 well-scoped questions opened by the POV.

### Ideate

Quantity + variety. Use **HMW** as prompts. Tag ideas `desirable` / `feasible` / `viable` as **hypotheses** (not proven). Produce a **substantive** list (no fixed count unless the user specifies one).

### Prototype

Describe **low-fidelity** artifacts: paper flow, roleplay script, landing smoke test, clickable sketch. For each: **Purpose:** what question does this answer? **Fidelity note:** one line placing the artifact on a sketch-only vs interactive spectrum (no low/medium labels).

### Test plan

**Learning goals** — what would convince you the idea is wrong? **Participants / sample** (or `[TBD]`). **Signals** — behaviors or metrics to observe. **Next iteration** — what changes if results are mixed.

---

## Execution Rules

1. **Define** must reflect whatever **Empathize** actually contains; do not invent field research.
2. Do not collapse **Ideate** into a single solution before **Prototype**.
3. **Test plan** must include falsifiable signals.

---

## Checklist (verify before responding)

- [ ] Setup: design challenge + default pass
- [ ] Empathize distinguishes fact vs `[INFERRED]`
- [ ] POV + HMW before Ideate
- [ ] Ideation is substantive; desirable / feasible / viable tags used
- [ ] Prototype states purpose and a one-line fidelity note (no low/medium labels)
- [ ] Test plan has learning goals and signals
