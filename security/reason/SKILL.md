---
name: autoresearch:reason
description: |
  Adversarial multi-round reasoning with blind-judge panel to reach rigorous conclusions.
  TRIGGER when: user wants rigorous reasoning or argument evaluation; user wants a decision
  analyzed from multiple angles; user wants devil's advocate critique; user asks "what are
  the strongest arguments for/against"; user wants a structured debate; user wants to avoid
  groupthink or anchoring; user invokes /autoresearch:reason.
  DO NOT TRIGGER when: user wants a simple recommendation; user wants a quick summary;
  user wants factual lookup; user just wants pros/cons without adversarial pressure.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebFetch
  - WebSearch
---

# autoresearch:reason

Adversarial multi-round reasoning loop with a blind-judge panel. Arguments are assigned
crypto-random IDs before critique so judges evaluate logic, not author identity. Runs until
convergence or budget exhausted.

## Autonomy Directive

**You are an autonomous reasoning agent.** Once the debate begins:

1. **NEVER STOP** to ask permission between rounds.
2. **NEVER ASK** "should I continue?" mid-debate.
3. **NEVER DECLARE CONVERGENCE** prematurely — a single unchallenged round is not convergence.
4. **The loop runs until:** all positions converge OR budget exhausted OR user interrupts.
5. **If neither condition is true, begin the next round immediately.**

---

## Setup

### Step 1 — Define the question
If not provided, ask once: "What is the question or decision to reason about?"
The question must be specific enough to allow falsifiable positions. Refuse vague inputs like
"think about AI" — ask for a concrete framing.

### Step 2 — Set parameters
Ask if not provided:
- **Number of positions** (default: 3). Minimum 2, maximum 5.
- **Max rounds** (default: 4). Minimum 2.
- **Convergence threshold:** "Converged" = all judges rate the top position's logical score ≥8/10
  AND no position has an unanswered rebuttal.

---

## Round Structure

Each round follows this exact sequence:

### Phase 1 — Propose Positions (Round 1 only)
Generate N distinct positions on the question. Positions must:
- Be mutually distinguishable (not minor variations of each other)
- Be stated as falsifiable claims, not vague preferences
- Cover the genuine range of defensible views (not strawmen)

Write each position to `reason/rounds.md` as: `Position [PENDING-ID]: [statement]`

### Phase 2 — Assign Crypto-Random IDs
Assign each position a random alphanumeric ID (e.g., `ARG-7F3A`, `ARG-2C91`).
Write the mapping to `reason/id-map.md` — this file is **sealed until the end** (not read during debate).
Replace all position labels in `reason/rounds.md` with their assigned IDs.
**From this point forward, all debate references use IDs only — never "Position 1" or author names.**

### Phase 3 — Blind Critique Round
For each argument ID, write a rigorous critique:
- Identify the strongest assumption and test whether it holds
- Find the weakest logical link in the chain
- Propose a concrete counterexample or falsifying scenario
- Rate logical strength: 1–10 (where 10 = logically airtight)

Critiques reference IDs only: "ARG-7F3A assumes X, which fails when Y..."
Write all critiques to `reason/rounds.md` under `## Round [N] — Critiques`.

### Phase 4 — Rebuttal Round
Each argument ID responds to the critiques it received:
- Acknowledge valid critiques (update or narrow the claim)
- Rebut invalid critiques with specific evidence or reasoning
- A position may concede partially — update the statement if weakened by critique

Write rebuttals to `reason/rounds.md` under `## Round [N] — Rebuttals`.

### Phase 5 — Judge Evaluation
Three independent judges evaluate all arguments:
- Judge A: Logic and internal consistency
- Judge B: Evidence quality and falsifiability
- Judge C: Practical applicability

Each judge scores every argument ID on their dimension (1–10) and identifies the strongest argument.
Judges reference IDs only. Write scores to `reason/rounds.md` under `## Round [N] — Judgment`.

### Phase 6 — Convergence Check
After each round:
- If top-scoring argument has score ≥8/10 from all judges AND no unanswered rebuttal exists → converged.
- If max rounds reached → converged by budget.
- Otherwise → begin next round (return to Phase 3 with updated positions).

---

## Output Files

All output goes to a `reason/` folder in the working directory.

| File | Purpose |
|------|---------|
| `reason/rounds.md` | Per-round arguments, critiques, rebuttals, and scores (IDs only during debate) |
| `reason/verdict.md` | Final synthesis: winning argument with reasoning, minority positions summarized |
| `reason/id-map.md` | Revealed at end only: maps each ID → original position label |

### verdict.md structure
```
# Verdict: [Question]
Rounds completed: [N]
Convergence: [yes/no — budget exhausted]

## Winning Argument
ID: [ARG-XXXX] (revealed: [original position])
Score: [avg judge score]/10
Summary: [2-3 sentence synthesis]
Key evidence: [bullet points]

## Minority Positions
- [ARG-YYYY]: [why it lost — specific logical weakness identified]
- [ARG-ZZZZ]: [why it lost]

## Synthesis
[2-3 paragraphs on what the debate revealed — including any nuances that
don't fit cleanly into the winning argument]

## Confidence
[Low / Medium / High] — with explicit statement of remaining uncertainty
```

---

## Anti-Anchoring Protocol

The ID system exists to prevent these failure modes:
- **Position ordering bias** — "the first argument always sounds best"
- **Framing bias** — "the argument labeled 'conservative' gets dismissed without evaluation"
- **Authority bias** — "the argument by the named expert wins by default"

Judges MUST NOT reference position order, original labels, or authorship until after `verdict.md` is written and `id-map.md` is revealed.

---

## Edge Cases

| Situation | Handling |
|-----------|----------|
| Two positions are identical | Merge them; reduce N by 1 |
| One position dominates all others in round 1 | Still run min 2 rounds — premature convergence is bias |
| Judges disagree strongly (spread ≥5 points) | Note as "contested" in verdict.md — no forced winner |
| Budget = 1 round | Complete one full cycle, write verdict with low confidence |
| Question has a factual answer | Note this upfront — reason is for judgment calls, not facts |
