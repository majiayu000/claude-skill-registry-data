---
name: adversarial-team-pattern
description: "Template pattern for multi-agent analysis where agents hold opposing mandates. Use when spawning subagents for complex research, code review, architecture decisions, or risk assessment. Triggers on: 'adversarial team', 'devil's advocate analysis', 'multi-perspective review', 'challenge this decision', 'stress test this plan', 'red team this'."
source: ai-berkshire/xbtlin (MIT) — pattern adapted from investment-team.md four-master debate model
tier: TIER 2 — CORRECTNESS
---

# Adversarial Team Pattern

Multi-agent analysis using opposing mandates — not consensus. Agents challenge each other rather than reinforce each other.

**Core principle:** consensus from multiple agents = one agent with extra compute. Value comes from *productive disagreement*.

---

## When to use

- High-stakes decisions (architecture, security, major refactor)
- Analysis where confirmation bias is a real risk
- Any time you'd normally just "get a second opinion" (make it an adversarial second opinion)
- Code review of critical paths
- Research where you want to surface what could go wrong, not just what looks right

Do NOT use for: simple lookups, single-file changes, mechanical tasks with a clear right answer.

---

## Team structure

Spawn these roles in a single message (parallel, `run_in_background: true`):

```
ROLE A — Advocate
  Mandate: Build the strongest case FOR the proposal.
  Find evidence that supports it. Assume it will work.
  Deliver: 3–5 concrete supporting arguments with evidence.

ROLE B — Challenger  
  Mandate: Find everything wrong with the proposal.
  Assume it will fail. Find the weakest points.
  Deliver: 3–5 specific failure modes or risks with evidence.

ROLE C — Constraint Finder
  Mandate: Find what's missing, what's not accounted for,
  what the other two missed. Be the skeptic of both sides.
  Deliver: unknowns, edge cases, unstated assumptions.

ROLE D — Synthesizer  (run AFTER A, B, C complete)
  Mandate: Read all three reports. Produce a forced conclusion.
  Cannot say "it depends". Must pick a side or a modified path.
  Deliver: verdict + confidence % + 1 concrete next action.
```

---

## Execution template

```
Analyze [TOPIC] using adversarial team pattern.

Agent A (Advocate): Make the strongest case FOR [TOPIC].
Find 3–5 concrete supporting arguments with evidence.
Do not hedge. Assume success.

Agent B (Challenger): Find everything wrong with [TOPIC].
Find 3–5 specific failure modes or risks.
Assume failure. Do not soften findings.

Agent C (Constraint Finder): Find what A and B both missed.
Surface unknowns, unstated assumptions, edge cases.
Be skeptical of both the advocate and challenger.

After all three complete, Agent D (Synthesizer) reads all reports
and produces a forced conclusion: verdict + confidence % + next action.
No "it depends" in the conclusion.
```

---

## Output Contract

```
Advocate findings:   [3–5 supporting arguments]
Challenger findings: [3–5 failure modes]
Missing/unknowns:    [what neither side saw]

VERDICT:     [clear position — not neutral]
CONFIDENCE:  [0–100%]
REASONING:   [which argument won and why]
NEXT ACTION: [one concrete step]
```

---

## In-Skill Verification

Before Synthesizer produces verdict:
1. Check: did Advocate cite at least 1 concrete piece of evidence (not just assertion)?
2. Check: did Challenger identify at least 1 specific failure mode (not generic risk)?
3. If either check fails → Synthesizer notes "incomplete input" in output with confidence ≤ 50%

---

## Anti-patterns

```
❌ All agents instructed to "analyze objectively" — that's consensus, not adversarial
❌ Synthesizer allowed to conclude "both sides have merit, consider your context"
❌ Challenger role that softens findings ("on the other hand, it could work if...")
❌ Running agents sequentially where later agents read earlier agents' output (anchoring bias)
❌ Skipping Synthesizer — raw debate without forced conclusion wastes the pattern
```

---

## Confidence calibration

| Situation | Max confidence |
|-----------|---------------|
| All 3 roles agree | 90% |
| Advocate + Synthesizer agree, Challenger has weak evidence | 75% |
| Split between roles, Synthesizer forced to pick | 60% |
| Missing data flagged by Constraint Finder | 50% |
| Insufficient evidence from any role | 35% |
