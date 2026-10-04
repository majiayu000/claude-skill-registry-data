---
name: architecture-tradeoff-analysis
kind: skill
status: ready
provenance:
  principles:
  - P006
  claims:
  - C00033
  - C00034
  evidence:
  - E00007
  - E00008
  source_anchors:
  - 508117177502-c0001
  authored_from_digest: a69c75eb5be9c5133fe55bb67cf4505c6a15643c5a3e07446821a2f38139a99d
---

# Architecture trade-off analysis

## Purpose

Make the trade-off explicit for every architecture choice. The first law of software
architecture is that everything is a trade-off: any structural option buys some properties at
the expense of others, so the honest default answer to "what is the right architecture?" is
"it depends on the driving forces." This skill turns that stance into a repeatable analysis
that names what an option gains, what it sacrifices, and which forces decide.

## When to use

- The caller proposes or reviews any structural choice where one option could be taken over
  another.
- The caller asks for the single best architecture, pattern, or technology, or presents an
  option's benefits with no cost stated.
- A recommendation is being written and needs its residual consequences surfaced before it
  ships.

Do not invoke for a settled factual definition that carries no design choice.

## Procedure

1. **Restate the decision and the alternatives.** Name the concrete options on the table
   (including the status quo / do-nothing). A trade-off analysis needs at least two options to
   compare; if only one is offered, surface the implied alternative.
2. **Surface the driving forces.** Pull the prioritized architecture characteristics and
   constraints the decision must serve. If they are unstated, that is the first gap — hand off to
   `identify-architecture-characteristics` before judging options.
3. **For each option, state gain AND sacrifice.** Write both halves explicitly: the property it
   improves and the property, cost, or flexibility it gives up. An option with only upside listed
   is an incomplete analysis, not a winner.
4. **Map each option to the prioritized forces.** Score how well it serves the top-ranked
   characteristics, not every quality at once. The option that best serves the highest-priority
   forces wins even if it loses on lower-priority ones.
5. **Name the residual consequence.** State plainly what the caller must accept by choosing the
   recommended option — the sacrifice does not disappear, it becomes a known cost.
6. **Recommend, tied to forces.** Give one recommendation, justified by the ranked forces, never
   as a universal "best." If the forces genuinely do not separate the options, say the choice is
   indifferent and name the tie-breaker.

## Inputs

- The decision under review and its candidate options.
- The system's driving forces: the quality attributes being optimised and the hard constraints.

## Output

A trade-off table or narrative in which every option carries an explicit gain-versus-sacrifice
pair, a recommendation tied to the prioritized forces, and the residual consequence the caller
must accept. Never one option presented as universally best.

## References

- [Laws of software architecture](../../references/laws-of-software-architecture.md) — the
  first law (everything is a trade-off) and the trade-off-analysis frame this skill operationalizes.

## Provenance

Distilled from principle(s) **P001**, claims **C00001/C00002**, evidence **E00001/E00002**, anchored in the cited architecture sources (`sources/anchors/`). Source is `distillation-only`: content is paraphrased, never quoted verbatim.
