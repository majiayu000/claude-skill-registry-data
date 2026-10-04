---
name: konsilium
description: Council — 5 independent AI perspectives + mutual critique + synthesis (adapted from karpathy/llm-council for Claude Code). For high-stakes decisions where the answer does NOT follow unambiguously from the data — go/no-go before real consequences, critiquing a methodology, choosing between competing approaches, pressure-testing a conclusion you're attached to, designing risk controls. NOT for log/data analysis (the council has no data access) and not for factual lookups. Triggers — "convene the council", "run it past the council", "go/no-go", "pressure-test this".
---

# /konsilium — the Council

Question/decision: **$ARGUMENTS**

The council gives **5 independent perspectives + mutual critique + synthesis** (karpathy/llm-council mechanism: independent opinions → anonymous peer review → chairman synthesizes). It does NOT compute data — it pressure-tests decisions and conclusions. So it's useful where **the cost of error is high and the answer does NOT follow unambiguously from the analysis**.

> **Hard rule.** The council decides WHAT to test and whether to ACT; your harness (tests / backtest / live data) computes the RESULT. Pairing: council raises a hypothesis / surfaces a risk → you run an honest test → council helps decide whether to commit. Neither works alone.

---

## PHASE 0 — relevance gate (mandatory, before convening)

Before spending the council — check it's actually its job.

**✅ Convene:**
- Go/no-go before real consequences (ship this config to production, raise the size, change the parameter).
- Whether to trust an analysis / critique of methodology (sample, look-ahead, regime-dependence, i.i.d. assumptions).
- Choosing between competing approaches with a real tradeoff.
- Pressure-testing a conclusion you/the user are attached to.
- Designing a risk control (circuit-breaker, exposure limit, safety switch).

**❌ Don't convene — do it directly:**
- Real log/data analysis — the council has no data access, compute it yourself.
- A factual lookup (how an API works, a code detail) — that's lookup, not debate.
- A mechanical code edit — just do it.
- Something already settled by data — nothing to argue.

If it's a ❌ — don't convene, say why, and do it directly.

---

## PHASE 1 — briefing

The advisors don't see the data. Gather the facts yourself (numbers, configs, what's known, prior art) and write a **short neutral briefing**:
- Context (what the system/strategy is, what's changing).
- The decision/question in one line.
- Known data (numbers, not interpretations).
- Options on the table.
- What's unknown / disputed.

**No conclusion of your own** — don't lead the advisors to an answer.

## PHASE 2 — 5 independent advisors (in parallel)

Launch 5 agents **in one message** (in parallel), each given: the briefing + its lens. Default lenses are general-purpose; swap them to fit the domain:

1. **Correctness skeptic** — is the reasoning sound? what assumption is load-bearing? what breaks it?
2. **Risk / downside** — worst case, blast radius, protection of the core asset, what happens at the worst outcome.
3. **Methodologist** — significance, sample, metric correctness, how to measure honestly, what's confounded.
4. **Execution / reality** — does it survive contact with the real world? second-order effects, hidden costs, operational friction.
5. **Devil's advocate** — attacks the core hypothesis, argues why NOT to do it and what's been missed.

Each returns: a **verdict** (go / no-go / need test X) + 2–4 main arguments + what it would check BEFORE acting.

## PHASE 3 — mutual critique (in parallel)

Give each advisor all 5 answers (anonymized, no role labels — so they don't side with "their own"). Ask each to: find holes in the others' arguments, re-rate its own verdict in light of the rest, state explicitly what it agrees and disagrees with.

## PHASE 4 — synthesis (you are the chairman)

Assemble the final:
- **Consensus** — where the advisors converge.
- **Disagreements** — where they clash and why (that's the risk zone).
- **Recommendation** — go / no-go / test X first.
- **Risks** — the main ones, what to monitor after acting.
- **What to run in the harness** — the concrete test to run BEFORE committing.

Don't average opinions — **weigh by argument strength, not by majority**. If the user is attached to a conclusion — press, don't play along.

---

## Anti-patterns
- Don't pass the council's opinion off as data: "the council said it's profitable" ≠ profitable. The harness decides outcomes.
- Don't convene for lookup / mechanics / things already settled by data.
- Don't skip Phase 3 (critique) — it's what catches the holes a single answer papers over.
- Keep the briefing neutral. A leading framing → the council confirms your bias instead of surfacing the risk.

---

## Origin
Mechanism — Andrej Karpathy, `github.com/karpathy/llm-council` (independent opinions → anonymized peer review → chairman synthesis). The original is a web app over OpenRouter using DIFFERENT models (GPT/Gemini/Claude/Grok). This is an adaptation for Claude Code: 5 subagents of one model with distinct role-lenses. For genuine multi-model diversity, wire in different providers via their APIs.
