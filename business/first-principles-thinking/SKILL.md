---
name: first-principles-thinking
description: >
  Use this skill when the user asks for first-principles thinking or first
  principles (including naming them or directing use/apply/run with obvious
  misspellings; decisive) or wants to reason from bedrock—stripping borrowed
  analogies and convention, surfacing fundamentals, then rebuilding the reasoning
  chain and implications. Use when they want to reason from scratch, challenge
  industry defaults, want physics-style business breakdowns, or sanity-check
  whether copying incumbents still makes sense, even if they never say first
  principles. Skip when they want a quick convention-following checklist with no
  rebuild of assumptions, or purely social coordination with no modeling ask.
license: MIT
metadata:
  author: ysskrishna
  version: "2026.5.17"
---

# First Principles Thinking

Question inherited baggage. Rebuild only from **bedrock** you can defend.

**How to run it with this skill:** one clearly headed section per step in this order: Surface → Question → Bedrock → Rebuild → Implications.

---

## Setup (run before starting)

In one short block:

1. **Reconstruction target** — belief, cost, design, or strategy to ground
2. **Default pass** — Surface → Question → Bedrock → Rebuild → Implications (state this line)

If immutable constraints (physics, law, budget) are unclear, ask at most 3 questions in one message, then proceed. Note unknowns or working guesses in plain language (no bracket tags in Setup).

---

## The Steps

### Surface

State the **conventional answer** or analogy people rely on. List **loaded words** or hidden comparisons ("like Uber for…").

### Question

For each major assumption: **Assumption:** … — **Why believed?** (authority, analogy, experience) — **What if false?**

### Bedrock

List **fundamental truths** that survive scrutiny — physics, logic identities, legal musts, documented preferences of real users, arithmetic. Label each `[FUNDAMENTAL]` vs `[STILL ASSUMPTION]`.

Prefer three or more honest bedrock items when that is credible; if fewer are honest, say why in one line.

### Rebuild

From **only** `[FUNDAMENTAL]` items, derive conclusions in numbered steps. No smuggled analogies; if you need a new premise, add it to **Bedrock** first with a tag.

### Implications

**So what** for decisions: what changes vs the conventional path? **Cost of being wrong** if a tagged assumption fails.

Add a short **vs convention** contrast (a few bullets or a two-column mini-summary) if it clarifies the decision.

---

## Execution Rules

1. **Rebuild** cannot cite "industry standard" as a premise unless translated into a fundamental (e.g. "buyers require SLA X because regulation Y").
2. If bedrock is too thin to rebuild, say **insufficient grounding** and list what evidence would fix it.
3. Avoid faux profundity; keep steps short and checkable.

---

## Checklist (verify before responding)

- [ ] Setup: reconstruction target + default pass
- [ ] Surface names convention or analogy explicitly
- [ ] Question step ties assumptions to why held
- [ ] Bedrock uses `[FUNDAMENTAL]` / `[STILL ASSUMPTION]`
- [ ] Rebuild chain only uses fundamentals
- [ ] Implications name what changes vs convention (and vs-contrast if helpful)
