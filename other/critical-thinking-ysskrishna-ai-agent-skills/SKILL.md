---
name: critical-thinking
description: >
  Use this skill when the user asks for critical thinking (including naming it
  or directing use/apply/run with obvious misspellings; decisive) or wants to
  evaluate a claim, argument, plan, or belief: clarify assertions, weigh evidence,
  surface assumptions, test reasoning for gaps or fallacies, scan biases,
  consider alternatives, and stress-test conclusions—whether they phrase it
  plainly ("red team", "devil's advocate", "what am I missing", steel/straw
  man, bias scan) or indirectly (decision-quality review, epistemic
  calibration). Skip for execution-only tasks with no evaluative angle, or when
  they only want wording, tone, layout, or open-ended brainstorming with no
  request to audit reasons, assumptions, or evidence.
license: MIT
metadata:
  author: ysskrishna
  version: "2026.5.18"
---

# Critical Thinking

**Critical thinking** is disciplined inquiry that keeps **description** separate from **evaluation**: surface assumptions, weigh evidence, test logic, consider alternatives, then state a proportionate conclusion. If the conventional view is well-supported, say so — this is inquiry, not contrarianism by default.

**How to run it with this skill:** one phase per clearly headed section, always in this order: Clarify → Information → Assumptions → Reasoning → Alternatives → Conclusion. Always include **Conclusion** unless the user explicitly stops the whole review early.

---

## Setup (run before starting)

In one short block:

1. **Focus** — the specific claim, proposal, or question under review
2. **Pass** — Clarify → Information → Assumptions → Reasoning → Alternatives → Conclusion (fixed sequence; state this line once in the setup block so the user sees the path)

If essential context is missing, ask at most 3 questions in one message, then proceed. Note any remaining gaps or working guesses in plain language (no bracket tags in Setup).

---

## The Phases

### Clarify

Restate the target in one precise sentence. Separate **factual** vs **normative** claims. Name success criteria if a decision is involved.

### Information

What evidence exists? Each bullet starts with **`[CITED]`** or **`[MISSING]`**:

- **`[CITED]`** — a traceable basis (user text, repo, doc, link, study, etc.); in the same bullet, name the basis and one line on strength or limits (no extra strength tags).
- **`[MISSING]`** — no traceable basis yet for that point, or evidence was requested but not available.

### Assumptions

List tacit premises. For each: **Assumption:** … — **If false:** …

When the **Focus** mixes **is** and **should**, surface **value / normative** premises too (e.g. **Value premise:** … — **If rejected:** …) alongside factual assumptions where it clarifies the chain.

### Reasoning

Trace the argument chain. Flag **leaps**, **circular** patterns, **correlation vs causation**, and **missing steps**. No new factual assertions here — only structure. If a premise is needed but was never established in **Information**, do **not** assert it as true; label it as an **ungrounded premise** (structural gap only). When **values** and **evidence** both do work in the chain, show which links depend on which.

**Bias and fallacy pass (compact):** add a short sub-list — only items that apply; omit the rest rather than padding.

- **Biases to scan:** confirmation; anchoring; survivorship; undue authority; sunk cost — plus any other bias clearly relevant to the case.
- **Fallacies to name if present** (tie each to the chain above): ad hominem; straw man; false dichotomy; slippery slope; hasty generalization; begging the question.

If none apply, state that plainly in one line.

### Alternatives

Credible competing explanations, plans, or frames. Do not collapse into debate rhetoric; keep alternatives plausible.

### Conclusion

1. **Judgment** — answer the **Focus** directly; when factual and normative claims were both in play, separate **what follows from the cited evidence** from **what depends on value premises** (short clauses are enough). Close with **one sentence in plain language** on how strong the case is given `[CITED]` vs `[MISSING]` evidence.

2. **What would change the judgment** — concrete falsifiers or new data; phrase relative to the **Focus** (e.g. the claim-holder’s view, a named third party, or *this assessment* when the review is impersonal).

---

## Execution Rules

1. Run phases in one response unless the user requests step-by-step pacing.
2. Never merge **Information** and **Reasoning** in the same bullet block.
3. Do not smuggle new unsupported facts into **Conclusion**; only synthesize prior phases.
4. If the user is emotionally fused with a position, name it neutrally and continue the phase plan.
5. Be intellectually honest: acknowledge strong opposing evidence and uncertainty where the phases support it.

---

## Checklist (verify before responding)

- [ ] Setup block: **Focus** and stated **Pass** (fixed sequence)
- [ ] Each phase is its own section in canonical order (Clarify through Conclusion)
- [ ] Information: each bullet starts with `[CITED]` (basis + limits in-bullet) or `[MISSING]`
- [ ] Assumptions use **Assumption** / **If false** pairs; **Value premise** / **If rejected** when the Focus mixes facts and shoulds
- [ ] Reasoning references only what earlier phases established; flags **ungrounded premises** where needed; bias/fallacy pass done or explicitly "none identified"
- [ ] Conclusion: judgment (evidence vs values when both apply, plus one plain sentence on strength of case from Information), falsifiers phrased for the **Focus**
