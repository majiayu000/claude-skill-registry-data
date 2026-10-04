---
name: pattern-and-analogy-connector
description: "Connects loose observations into a meaningful opportunity by identifying analogies across industries and situations using the Capability Pattern Mapping method: superficially different cases are abstracted into one named capability pattern, which then serves as a diagnostic question in a new context. Use when an opportunity has no obvious precedent in your own industry and a same-industry case search comes up empty."
---

# Pattern & Analogy Connector

## Purpose

Connects loose observations into a meaningful opportunity by identifying
analogies across industries and situations. The core method is
**Capability Pattern Mapping**: instead of asking "has something similar
been done in our industry" — which produces an endless, quickly-outdated
list of cases — superficially different sets of cases are **abstracted into
one named, industry-agnostic capability pattern**. The named pattern then
becomes a **diagnostic question** that can be applied to any new industry or
situation without first having to find a known example from that specific
industry.

This is different from a case library. A case library answers "has an
example of this been done" — it goes stale quickly and tempts people to copy
the surface-level solution as-is. A pattern answers "what kind of
structural situation is this" — it stays useful for years, and forces you to
think through your own context instead of searching for a ready-made
answer.

## Anchored in research

- Tang, J., Kacmar, K. M., & Busenitz, L. (2012), "Entrepreneurial Alertness
  in the Pursuit of New Opportunities," *Journal of Business Venturing*,
  27(1), 77–94 — **association and connection**, one of the paper's three
  dimensions of entrepreneurial alertness (see also
  `../market-and-signal-scanning/SKILL.md` for scanning-and-search and
  `../opportunity-evaluation-and-judgment/SKILL.md` for evaluation-and-judgment).
- Baron, R. A. (2006), "Opportunity Recognition as Pattern Recognition: How
  Entrepreneurs 'Connect the Dots' to Identify New Business Opportunities,"
  *Academy of Management Perspectives*, 20(1), 104–119 — the argument that
  opportunity recognition draws on the same cognitive mechanism as pattern
  recognition generally: connections between previously unrelated events or
  trends are noticed because a person's existing knowledge structures make
  the connection visible in the first place.
- A Capability Pattern Mapping method and worked example described by the
  user (an invoice/customs/CV document case, see point 3 below) — the
  owner's own abstraction technique, not an academic source.

A concrete, fully worked-out application of this to AI capabilities exists
at `../../../ai-strategy-and-governance/references/ai-capability-pattern-library.md`
and its navigation skill
`../../../ai-strategy-and-governance/skills/ai-capability-pattern-matching/SKILL.md`.
This skill here is the GENERAL method; the AI-strategy pack's pattern
library is one concrete implementation of it, applied to one domain (AI
solutions).

## Method

1. **Collect 3+ superficially different observations/cases** in which you
   suspect a similar underlying structure. They can come from different
   industries, different clients, or observations made at different times.
   Don't start by searching for "a comparable industry" — start by looking
   for *structural similarity beneath the surface*.
2. **Ask four abstraction questions of each case**, questions that
   deliberately bypass industry-specific vocabulary:
   - What is the **input**? (e.g. "free-form text/PDF document," not "loan
     application")
   - What is the **actor/role** doing the work today? (e.g. "a highly paid
     specialist reads through the document," not "a loan processor")
   - What is the **core cognitive function**? (e.g. "searching for an
     anomaly/gap in a large volume of unstructured content," not
     "application review")
   - What is the **outcome/decision** the work supports? (e.g. "approve /
     reject / escalate," not "credit decision")
3. **Write a single sentence that describes every case in the set the same
   way, using only the answers from step 2.** This sentence IS the
   pattern's name and definition. Example, from the user's own material:
   three superficially completely different cases — document review of loan
   applications in financial services, tariff-code verification of customs
   declarations in logistics, and CV screening in HR — all abstract to the
   same pattern: **"Validation and anomaly detection in unstructured
   documents"** (input: free-form document; actor: a specialist; cognitive
   core: searching for an anomaly in a large volume of text; outcome:
   approve/reject/escalate decision).
4. **Turn the pattern into a diagnostic question** that can be asked of any
   new client without already knowing an example from their specific
   industry. Example: the pattern "Validation and anomaly detection in
   unstructured documents" produces the question: *"Where in your process
   does a highly paid specialist have to search for anomalies in free-form
   text or a PDF document?"* — the same question can be asked of a
   construction, insurance, or public-sector client without having first
   seen a known example from their specific industry.
5. **Test the pattern's coverage and sharpness before using it:**
   - **Coverage** — can you find at least three genuinely different (across
     industry/context) examples for the pattern? If you can only find one,
     it isn't a pattern yet, just an isolated case — don't generalize too
     early.
   - **Sharpness** — is the pattern precise enough to distinguish it from
     its neighboring patterns? A pattern that's too broad ("AI helps with
     decision-making") doesn't point the diagnostic question anywhere
     useful; one that's too narrow ("PDF loan application review in
     financial services") doesn't generalize across industries.
6. **Use the diagnostic question in a new context** (a client meeting, a
   workshop, your own observation) and record the answer as a structured
   hypothesis: the pattern's name, why this situation matches the pattern,
   and how this situation differs from the known examples.
7. **Validate the hypothesis** with stakeholders or against your own
   experience-based checklist before carrying it forward (see
   `../opportunity-evaluation-and-judgment/SKILL.md`).

## What this skill does NOT do

- Doesn't make the final decision for you — it produces a structured draft
  to support a human decision.
- Doesn't confirm figures, market data, or competitor data from memory — it
  uses the inputs you provide, or clearly flags an assumption
  (`[assumption — verify]`).
- Doesn't guarantee that a found analogy actually holds — it produces a
  hypothesis that still needs validation.
- Doesn't maintain a ready-made, comprehensive pattern library within this
  general-purpose skill — that would make it unwieldy and go stale quickly.
  Industry- or solution-type-specific pattern libraries (e.g. the AI
  capability patterns) live in their own packs and point back to this
  method, not the other way around.
- Doesn't replace in-depth industry research — the pattern is meant to speed
  up hypothesis generation, not to substitute for industry expertise.

## Refinement notes

The method and the invoice/customs/CV example are the owner's own worked
technique. Areas to keep expanding as more of it is put into practice:

- your own validated patterns from opportunity-recognition work (not just
  from the AI context)
- concrete examples of where abstraction went too far (a pattern turned out
  too broad to be useful) or too narrow
- a template for assembling diagnostic questions (into `../../references/`)

Once this section is filled in and validated in practice, update the
`maturity` field in `skills_index.json` to `draft`, `validated`, or
`canonical` (see `../../../meta/maturity_levels.md`). **Don't add new fields
to the frontmatter** — `name` and `description` are the only ones allowed
(see `../../../meta/frontmatter_schema.md`).

## Continue from here

- Next in this pack: `../opportunity-evaluation-and-judgment/SKILL.md` —
  Structurally assesses the viability of the identified opportunity before
  resources are committed.
- Concrete application to AI solutions:
  `../../../ai-strategy-and-governance/references/ai-capability-pattern-library.md`
  (the pattern library) and
  `../../../ai-strategy-and-governance/skills/ai-capability-pattern-matching/SKILL.md`
  (how the library is used in client work).
- A ready-made skill chain for this situation: see `../../../playbooks/`
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/` — the pack's shared background material
- `../../CLAUDE.md` — this pack's shared guardrails
