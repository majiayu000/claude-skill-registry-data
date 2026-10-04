---
name: ai-use-case-feasibility-and-poc-scoping
description: "Scopes an AI proof-of-concept around a single falsifiable hypothesis, sets a quantitative success bar and kill criterion against a named human baseline, and builds a golden test set before development starts. Use when a PoC needs to answer a real feasibility question rather than produce an impressive demo that proves nothing about production readiness."
---

# AI Use Case Feasibility & PoC Scoping

## Purpose

Determines the technical boundary conditions of an AI use case and scopes
the PoC phase — narrow enough to run fast and cheap, but structured
enough that its result (pass or fail) actually tells you something about
production feasibility, instead of producing an impressive demo that
answers no real question.

## Anchored in research

- Perplexity research — PoC scoping through to productionization
- The "evals are the new PRDs" framing and the failing-transcript
  translation technique in step 3 — Anthropic product lead Dianne
  Penn, describing how her team turns vague AI-quality feedback into
  scored test sets ("evals are the new PRDs... it's basically
  test-driven development for PMs... where you write the test first"),
  supplied by the user from a source video transcript. Applied here to
  PoC/use-case scoping specifically, which the source material does
  not itself cover — the source describes an internal product-team
  practice, not a PoC-scoping method.

## Method

1. **State the hypothesis the PoC is meant to test, as a single
   falsifiable sentence** — not "test whether AI can help with X," but
   e.g. "the model classifies inbound tickets into our 12 categories at
   ≥85% accuracy against a human-labeled sample." A PoC without an
   explicit hypothesis produces an opinion, not evidence.
2. **Set success criteria and a kill threshold before building
   anything**, together with the business owner, not after seeing the
   first results:
   - A quantitative success bar (accuracy, latency, cost per
     transaction, adoption rate) tied to the use case's Technical
     Feasibility and Business Impact scores from
     `../ai-opportunity-portfolio/SKILL.md`.
   - An explicit **kill criterion** — the result below which the PoC is
     called a "no" and the use case is retired or fundamentally
     re-scoped, not quietly extended for "one more sprint."
   - A named **human baseline** to compare against — an AI system that
     merely matches a mediocre existing process, without a cost or
     speed advantage, hasn't demonstrated feasibility.
3. **Assemble a golden test set before development starts.** A small
   (often 50–200 item), representative, human-labeled sample of real
   inputs, including edge cases and known failure modes — not just the
   easy majority case. Reusing this same set for evaluation prevents
   the common failure of quietly redefining "good enough" once actual
   outputs are seen.
   - **Build it from real failing transcripts, not a hypothetical
     list.** Vague quality complaints ("the model hallucinates," "it
     doesn't follow instructions") aren't testable — they need to be
     translated into specific input/expected-output pairs before
     they're useful. Practice: collect the exact prompt, system
     context, and actual (wrong) output for each real complaint; from
     roughly 30-40 of these, the pattern of what "good" actually means
     usually becomes clear enough to write as a scored test set. This
     translation step — vague complaint → concrete failing transcript →
     testable example — is the actual bottleneck in building a useful
     golden set, more often than the number of examples.
   - **Treat the resulting eval set as a living regression suite, not
     a one-time PoC gate.** Re-run it every time the underlying model
     changes (a version upgrade, a prompt change, a new tool added to
     the agent), and set an explicit pass-rate bar the new version has
     to clear (e.g. ≥99%) before it replaces the old one in production.
     A golden set built once for the PoC and never run again silently
     stops protecting anything the moment the model behind it changes.
4. **Separate what the PoC must prove from what it deliberately does
   not.** Explicitly out of scope for a PoC, unless the use case
   specifically requires it: production-grade security hardening,
   full-scale load handling, complete UI polish, integration with every
   downstream system. Naming these out loud up front prevents
   scope creep and prevents a stakeholder later treating "PoC passed"
   as "production-ready" (see
   `../../../prototyping-and-demonstration/skills/demo-framing-and-expectation-setting/SKILL.md`
   for framing this boundary in client/stakeholder communication).
5. **Identify the technical fit and risk profile up front:**
   - **Problem type** — classification, generation, prediction,
     extraction, or agentic decision-making? Each has different
     failure modes and evaluation methods.
   - **Data availability and quality** for the golden test set and any
     fine-tuning/retrieval corpus — is it accessible now, or does a
     data-access or cleaning task block the PoC before it can start?
   - **Hallucination/error tolerance** — reuse the SML error-tolerance
     assessment from
     `../task-level-decomposition-and-automation-fit/SKILL.md`
     if it exists for this task; a use case with low error tolerance
     needs a human-in-the-loop check built into the PoC design itself,
     not added afterward.
   - **Integration surface** — does the PoC need to read/write real
     systems, or can it run on an extracted, static dataset? A
     PoC that avoids live integration is faster but proves less about
     production feasibility — state which trade-off was chosen and
     why.
6. **Timebox the PoC explicitly** (typically 2–6 weeks) and name the
   decision point at the end: go to pilot, redesign and retest, or
   kill. An open-ended PoC without a decision date tends to drift into
   a permanent, unaccountable side project.
7. **Produce a structured PoC scope document**: hypothesis, success/
   kill criteria, golden test set description, explicit out-of-scope
   list, technical risk notes, timebox and decision point (see
   `../../references/` once a template is added).
8. Validate the scope with both the technical team (is it buildable in
   the timebox) and the business owner (does passing it actually
   justify a production investment) before starting.

## What this skill does NOT do

- Doesn't make the final decision for you — it produces a structured
  draft to support a human decision.
- Doesn't confirm figures, market data, or competitor data from
  memory — it uses the inputs you provide, or marks an assumption
  clearly (`[assumption — verify]`).
- Doesn't do technical architecture design or model selection for
  you — it scopes the PoC's boundaries and success criteria, not the
  implementation.
- Doesn't guarantee a PoC that passes will succeed in production — a
  PoC deliberately excludes scale, security-hardening, and full
  integration; passing it reduces risk, it doesn't eliminate it.

## Refinement notes

Areas to keep deepening with real practice:

- your own rules of thumb and heuristics for this technique — e.g.
  typical timebox lengths and golden-test-set sizes by use-case type
- concrete templates (into `../../references/`, e.g. a PoC scope
  document template)
- reference cases / your own examples
- what this skill deliberately does *not* do (guardrails, common
  mistakes) — add to the list above

Once this section is filled in and validated in practice, update the
`maturity` field in `skills_index.json` to `draft`, `validated`, or
`canonical` (see `../../../meta/maturity_levels.md`). **Don't add new
fields to the frontmatter** — `name` and `description` are the only
ones allowed (see `../../../meta/frontmatter_schema.md`).

## Continue from here

- Next in this pack: `../responsible-ai-and-governance-check/SKILL.md`
  — checks the regulatory, risk, and ethics dimensions of an AI
  initiative. Deeper EU AI Act compliance analysis requires separate
  regulatory expertise.
- Once the technical scope is done and the PoC needs to be built and
  presented: `../../../prototyping-and-demonstration/skills/rapid-prototype-and-vibe-coding-craft/SKILL.md`
  (prototyping) and `../../../prototyping-and-demonstration/skills/demo-framing-and-expectation-setting/SKILL.md`
  (turning the same scope into a client-communication frame — a
  different question from this skill's technical scoping, use both
  together).
- A ready-made skill chain for this situation: see `../../../playbooks/`
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/` — the pack's shared background material
- `../../CLAUDE.md` — the pack's shared guardrails
