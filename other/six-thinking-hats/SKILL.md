---
name: six-thinking-hats
description: >
  Use this skill when the user asks for six thinking hats, parallel thinking, or
  Edward de Bono's method (including naming any of these or directing
  use/apply/run with obvious misspellings; decisive)—or wants a sequential,
  six-role thinking partner for one focus—keeping facts, feelings, risks,
  benefits, and new ideas in separate passes instead of one mixed reply. Use for
  structured brainstorms, decisions, or reviews when they ask for hat-by-hat
  analysis or name the method or author, even if phrasing is casual or incomplete.
  Skip for plain factual questions, execution-only implementation with no
  structured perspective pass, or one-off hot takes and single-angle verdicts
  where they do not want a fixed, hat-by-hat sequence across six roles.
license: MIT
metadata:
  author: ysskrishna
  version: "2026.5.18"
---

# Six Thinking Hats

**Six Thinking Hats** (Edward de Bono) is a **parallel thinking** method for a single **focus question**. Rather than mixing logic, emotion, optimism, and critique in one back-and-forth, the thinker or group takes **six complementary roles in sequence**, all wearing the “same hat” at each step. That keeps facts, gut reactions, risks, upsides, and new ideas from talking past each other.

Each hat’s meaning, constraints, and bullet formats are defined once in **[The Hats](#the-hats)**; the closing **Blue** pass is in **[Blue Synthesis](#blue-synthesis)**.

**How to run it with this skill:** one hat per section, clearly labelled; never mix two hats in the same section; always close with **Blue synthesis** that integrates earlier hats and adds **no** new facts, risks, ideas, or recommendations beyond what those hats produced.

---

## Setup (run before starting)

Before executing hats, establish in one short block:

1. **Focus question** — one sentence
2. **Mode** — which hat set (see table below); default: Full
3. **Depth** — how much detail per hat (see table below); default: Standard
4. **Hat order** — list the sequence you'll follow

If critical information is missing, ask at most 3 questions in one message, then proceed. Note any remaining gaps or working guesses in plain language (no bracket tags in Setup).

---

## Modes

| Mode | Hats | Use for |
|------|------|---------|
| **Full** (default) | Blue → White → Red → Black → Yellow → Green → Blue | Broad decisions, full-spectrum reasoning |
| **Creative** | Blue → Green → Yellow → Red → Blue | Idea generation; skips Black to avoid premature criticism |
| **Risk** | Blue → White → Black → Blue | Risk scans and failure prevention |
| **Decision** | Blue → White → Black → Yellow → Blue | Go/no-go decisions; skips Red and Green |
| **Custom** | User-defined + Blue at end | User-directed; confirm order before starting |

Custom mode: only the six standard hats are allowed. Blue synthesis is always required at the end — add it silently if the user omits it.

---

## Depth

| Depth | Bullets per hat | Style |
|-------|----------------|-------|
| **Quick** | 2 | Concise; synthesis collapses to 3 bullets |
| **Standard** (default) | 3 | Balanced detail |
| **Deep Dive** | 4–5 | Examples, edge cases, explicit assumptions |

---

## The Hats

### 🔵 Blue — Process
Runs twice: once to open (Setup), once to close (Synthesis). Blue only frames and synthesises — it never introduces new facts, risks, ideas, or recommendations.

### ⚪ White — Facts
Data, evidence, gaps. No interpretation.

Label every bullet:
- `[KNOWN]` — verifiable fact from user or reliable context
- `[ASSUMED]` — working assumption; flag it
- `[UNKNOWN]` — missing information that limits confidence

### 🔴 Red — Emotions
Gut reactions, enthusiasm, resistance, intuition.

- User-stated emotions: pass through verbatim, labeled **stated**
- Inferred emotions: use hypothetical language ("might", "could", "may") — never assert as fact

### ⚫ Black — Risks
Failure modes and weaknesses.

Every bullet format:
> **Risk:** [specific failure mode] — **Mitigation:** [concrete action]

### 🟡 Yellow — Value
Benefits and opportunities.

Every bullet format:
> **Benefit:** [concrete upside] — **Condition:** [what must hold for this to materialise]

### 🟢 Green — Creativity
Alternatives, novel options, reframes. Generate only — no evaluation here.

Produce **one distinct option per bullet**, using the same **bullets-per-hat**
count as the **Depth** table for the chosen level (Quick: 2, Standard: 3,
Deep Dive: 4–5).

When stuck, use a forcing tactic: reversal, analogy, or constraint removal.

---

## Blue Synthesis

A **tension** is where one hat's finding pulls against another's (e.g. a Yellow benefit only holds if a Black risk is mitigated).

**Standard synthesis shape:**
1. Top tension
2. Second tension (if present)
3. Recommendation — grounded only in what the hats produced
4. Next step (with owner/timeframe if known)

**Quick synthesis shape (3 bullets):**
1. Key tension (merged if multiple)
2. Recommendation
3. Next step

After synthesis, ask the user whether to iterate, expand a specific hat, or stop.

---

## Execution Rules

1. Produce all hats in one response unless the user requests interactive pacing (one hat per message, pause between each).
2. Keep hat sections clearly separated — never blend two hats in one section.
3. Blue never adds new content in synthesis; it only draws from what the hats produced.
4. If the user is anchored to one lens (only complaining, only optimistic), name it and route to the contrasting hat.

---

## Checklist (verify before responding)

- [ ] Setup block present with focus question, mode, depth, and hat order
- [ ] Mode and depth defaulted explicitly if not specified by user
- [ ] Hats executed in declared order, one section per hat
- [ ] White: every bullet has `[KNOWN]`, `[ASSUMED]`, or `[UNKNOWN]`
- [ ] Black: every bullet has **Risk** and **Mitigation**
- [ ] Yellow: every bullet has **Benefit** and **Condition**
- [ ] Red: inferred emotions use hypothetical language; stated emotions passed through verbatim
- [ ] Green: option count matches depth; no evaluation mixed in
- [ ] Blue synthesis present; no new content introduced