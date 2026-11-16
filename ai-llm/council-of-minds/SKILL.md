---
name: council-of-minds
description: Convene 6 intellectual personas across multiple LLM providers for hard decisions. Each persona runs on a different provider for genuinely different reasoning — not costume changes on one model. Inspired by council-of-high-intelligence (CC0).
origin: yana-ai — inspired by 0xNyk/council-of-high-intelligence (CC0)
license: MIT
version: 1.0.0
triggers:
  - /council-of-minds
  - council of minds
  - convene the council
  - multi-mind deliberation
modes:
  full: 6 personas, 2 rounds (~4 min)
  quick: 3 personas, 1 round (~90s)
  duo: 2 opposing personas, 1 round (~45s)
---

# /council-of-minds

Six intellectual personas deliberate your hardest decisions across multiple AI providers.
One command. Structured disagreement. No fake consensus.

## Modes

```
/council-of-minds "question"           → full (6 personas, 2 rounds)
/council-of-minds --quick "question"   → quick (3 personas, 1 round)
/council-of-minds --duo "question"     → duo (2 opposing voices, 1 round)
```

## When to Use

- Decision has ≥2 credible paths and no obvious winner
- You want structured disagreement, not a polished "yes"
- You suspect your own anchoring bias
- High stakes: architecture, strategy, go/no-go, hiring, product direction

## When NOT to Use

- Single correct answer (use tools or research instead)
- Pure implementation task (use `/plan`)
- Code review (use `/code-review`)
- Factual lookup (just ask directly)

---

## The Six Personas

Each persona is routed to a different provider to ensure genuinely different reasoning.

| Persona | Intellectual Tradition | Provider | Lens |
|---------|----------------------|----------|------|
| **The Architect** | Systems thinking, long-term | Claude | Correctness, maintainability, 5-year consequence |
| **Socrates** | Socratic questioning | Gemini | Destroys premises, finds the hidden assumption |
| **Feynman** | First-principles empiricism | DeepSeek | "What does evidence actually say? Rebuild from scratch." |
| **The Pragmatist** | Execution realism | Groq | Shipping speed, operational reality, resource constraints |
| **Kahneman** | Behavioral economics | OpenAI | Cognitive bias traps, System 1 vs System 2, loss aversion |
| **Torvalds** | Engineering minimalism | Ollama (local) | "Will this actually work? Is it unnecessarily complex?" |

If a provider is unavailable, fall back to Claude for that persona but explicitly note the fallback in output.

---

## Protocol

### Step 0 — Problem Restate Gate

**Before any analysis**, every persona must reframe the question in one sentence.

> Rule: if ≥3 personas restate the question differently from how it was asked, the original question was the problem. Resolve the question ambiguity before proceeding.

### Step 1 — Extract the real decision

Reduce to:
- What exactly are we deciding?
- What constraints are non-negotiable?
- What does success look like in 6 months?
- What is the cost of reversing this decision?

### Step 2 — Form Architect position first (anti-anchoring)

Before reading other voices, write:
1. Initial position (1 sentence)
2. Three strongest reasons
3. Main risk in preferred path

This prevents synthesis from simply mirroring external voices.

### Step 3 — Launch personas in parallel

Each persona gets only:
- The restated decision question
- Minimal necessary context (no full conversation history)
- Their role prompt

**Persona prompt template:**
```
You are [PERSONA NAME] on a six-voice decision council.

Your intellectual tradition: [tradition]
Your primary lens: [lens]

Question: [restated decision]

Context (only what's needed):
[compact context — code snippet, constraint, metric — max 200 words]

Respond with exactly this structure:
1. Restate — rephrase the question in your own words (1 sentence)
2. Position — your recommendation (1-2 sentences)
3. Reasoning — 3 bullets, each ≤ 25 words
4. Strongest objection to your own position — 1 sentence
5. What the other voices will miss — 1 sentence

Under 250 words total. No hedging. No "it depends" without specifying what it depends on.
```

### Step 4 — Dissent Quota Check

After collecting all positions:

> **Rule**: If ≥4 of 6 personas agree on the same recommendation, force 2 personas (chosen by least-confident alignment) to steelman the opposing view before synthesis.

This prevents groupthink from producing false consensus.

### Step 5 — Round 2 (full mode only)

Show each persona the other five positions (anonymized — no names, just positions).
Each updates or defends their view in ≤ 100 words.

### Step 6 — Synthesize

Rules for synthesis:
- Do not dismiss any external view without explaining why
- If an external voice changed the Architect's recommendation, say so explicitly
- Lead with **Unresolved Questions** before the verdict
- The strongest dissent must appear even if rejected

---

## Output Format

```markdown
## Council of Minds: [decision title]

### Problem Restate Gate
- Original question: [as asked]
- Restated by council: [if different, flag it]

---

### Positions

**The Architect** (Claude) — [1-sentence position]
> [key reasoning, 1 line]

**Socrates** (Gemini) — [1-sentence position]
> [key reasoning, 1 line]

**Feynman** (DeepSeek) — [1-sentence position]
> [key reasoning, 1 line]

**The Pragmatist** (Groq) — [1-sentence position]
> [key reasoning, 1 line]

**Kahneman** (OpenAI) — [1-sentence position]
> [key reasoning, 1 line]

**Torvalds** (Ollama) — [1-sentence position]
> [key reasoning, 1 line]

---

### Synthesis

**Where they align:** [what ≥4 agree on]

**Strongest dissent:** [the most important disagreement — do not soften it]

**Dissent quota triggered:** yes / no — [if yes, who steelmanned what]

**Unresolved questions:**
- [question the council couldn't answer]
- [what you'd need to know to decide with confidence]

**Recommended next steps:** [concrete, not "do more research"]

### Verdict
**Recommendation:** [the synthesized path — commit to one]
**Confidence:** [low / medium / high + why]
**Reversibility:** [how hard to undo if wrong]
```

---

## Quick Mode (3 personas)

Use: Architect + Socrates + Torvalds

Best for: tactical decisions, scope calls, technology choices

One round only. No Round 2. No dissent quota.

Output: same format but 3 positions only.

## Duo Mode (2 personas)

Pick the two most opposing intellectual traditions for the question type:

| Decision type | Best duo |
|--------------|---------|
| Technical architecture | Architect vs Torvalds |
| Strategic direction | Feynman vs Kahneman |
| Ship vs hold | Pragmatist vs Architect |
| Question a premise | Socrates vs anyone |

One round. No restate gate (too short). Verdict required.

---

## Anti-Patterns

```
❌ Feeding the full conversation history to all personas (kills independence)
❌ Hiding disagreement in the verdict to sound decisive
❌ Using council for tasks with an objectively correct answer
❌ Accepting ≥4-way agreement without triggering dissent quota
❌ "It depends" without specifying the dependency
❌ Council when the real blocker is missing information, not conflicting values
```

## Related Skills

- `council` — 4-voice version, lighter
- `multi-agent-debate` — Du et al. 2023 algorithm, multi-round consensus
- `santa-method` — adversarial verification of a specific claim
- `first-principles-thinker` — single voice, Feynman-style deconstruction
