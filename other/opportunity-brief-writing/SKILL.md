---
name: opportunity-brief-writing
description: "Writes the results of an opportunity assessment into a concise 1-2 page Opportunity Brief report, understandable to both the technical inventor and the decision-maker."
---

# Opportunity Brief Writing

## Purpose

Writes the assessment produced by the `opportunity-value-assessment` skill
into a concise, 1–2 page Opportunity Brief report (or an equivalent online
report) that is understandable to both the technical inventor and the reader
making the business decision — without requiring familiarity with the
underlying theory.

## Based on

The owner's own service — the report template of the Opportunity Value
Assessment product (own product, see
`../../references/opportunity-brief-template.md` for the full template with
example content).

## Method

1. **Opportunity Snapshot.** A one-paragraph summary of the opportunity and
   its potential, in business language — what's being assessed and which
   angles the report covers.
2. **Evaluation Matrix.** Present the 2D placement (attractiveness ×
   readiness) produced by `opportunity-value-assessment` visually, and add a
   narrative interpretation: what does the placement actually mean for this
   specific opportunity?
3. **Strengths & Gaps.** The top 3 strengthening and top 3 weakening
   factors, with concrete justification (no generic phrases — use numbers or
   named observations where possible).
4. **Market Pathways.** 1–3 potential markets/applications, each with: size
   (TAM), growth, life-cycle stage, entry route, and rationale for why this
   market fits.
5. **Business Snapshot** as five questions in plain business language:
   (1) what's the problem, (2) who has it, (3) what's the current solution,
   (4) what's our innovation, (5) how could this become a business.
6. **Evaluation Lenses table.** The seven angles (the 1–5 scores plus
   🟢/🟡/🔴 color produced by `opportunity-value-assessment`) and a short
   justification for each.
7. **Critical Implementation Issues.** What needs to be solved before the
   opportunity can reach its full value.
8. **License vs. Startup view.** A short recommendation with rationale (see
   the preliminary direction from `opportunity-value-assessment`); can be
   presented as a small comparison table.
9. **Recommended Next Steps (3–6 months).** A prioritized, concrete action
   list derived directly from the critical factors — not generic
   recommendations but actionable steps (e.g. "interview 3–5 potential
   customers about X," "launch a pilot with partner Y").
10. **Always include:** a disclaimer (everything is hypothesis- and
    assumption-based analysis, not a final truth or investment case), a note
    that the report is not an official invention disclosure and doesn't
    replace the IP procedures required by the organization's innovation
    policy, and a confidentiality notice.

## Gotchas

- Step 2 (Evaluation Matrix) asks for a *narrative interpretation* of the
  placement, not just a redrawn 2x2 grid — restating "attractiveness: high,
  readiness: medium" without explaining what that combination means for this
  specific opportunity is the most common way this step turns into a wasted
  diagram.
- Step 3 explicitly bans generic phrases for Strengths & Gaps — if the
  underlying `opportunity-value-assessment` didn't attach numbers or named
  observations to a factor, don't paraphrase it into a stronger-sounding
  claim; keep the same level of specificity the source assessment actually
  had.
- The License vs. Startup view (Step 8) is only ever a *preliminary
  direction* inherited from `opportunity-value-assessment` — presenting it
  in the brief as a settled recommendation, rather than flagging it as
  directional, misleads the decision-maker into thinking a real
  make/license decision has already been made.
- Step 10's disclaimer, "not an invention disclosure" note, and
  confidentiality notice are not optional boilerplate — because this skill
  explicitly does not replace an organization's IP procedures, dropping any
  one of the three when a report gets trimmed to fit "1 page" reintroduces
  the exact risk the skill exists to avoid.
- This skill cannot be run standalone: without a completed
  `opportunity-value-assessment` (2D placement + 7-lens scores) as input,
  filling in the Evaluation Matrix or Evaluation Lenses table from general
  impressions instead of that skill's actual output produces a brief that
  looks authoritative but isn't grounded in the assessment it claims to
  summarize.

## What this skill does NOT do

- Isn't an official invention disclosure and doesn't replace the IP
  procedures required by a university's/organization's innovation policy —
  always mention this in the report (see the note text in the template,
  `../../references/opportunity-brief-template.md`).
- Doesn't present scoring, market data, or TRL assessment as final truth —
  everything is based on information supplied by the client, supplemented
  by desk research and analyst interpretation; flag this clearly.
- Doesn't write the report without a preceding `opportunity-value-assessment`
  evaluation — it needs the matrix placement and 7-lens scoring it produces
  as input, and doesn't generate them itself from scratch.

## Continue from here

- Start of the full chain: `../opportunity-intake-elicitation/SKILL.md` →
  `../opportunity-value-assessment/SKILL.md` → this skill
- Related skill in another pack (when the opportunity needs a full business
  justification): `../../../business-case-and-analysis/skills/business-case-builder/SKILL.md`
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/opportunity-brief-template.md` — the full report template with example content
- `../../CLAUDE.md` — this pack's shared guardrails
