---
name: ps-public-value-business-case-framing
description: "Reframes an AI business case around the four public-value types (efficiency, service quality, equity, trust/legitimacy) instead of defaulting to a private-sector ROI story, and shows how to combine cost-avoidance and non-financial value in one case a public decision body can act on. Use after opportunity screening, before or alongside building the full business case."
---

# Public-Value Business Case Framing

## Purpose

`business-case-and-analysis:business-case-builder` and
`roi-npv-sensitivity-model` build the financial and structural skeleton
of a business case. In a public-sector context, forcing that skeleton
into a pure ROI story usually understates the real case and can make a
genuinely strong initiative look weak on paper — because much of its
value is real but not directly monetizable (fewer citizen complaints,
faster service access, reduced disparity between groups). This skill
shows how to build the value case in public-value terms first, then
translate it into the financial model without losing what doesn't
convert to a dollar figure.

## Method

### 1. Build the value case across all four types, not just cost

Using the four public-value types from
`ps-ai-opportunity-screening-for-public-value` (efficiency, service
quality, equity, trust/legitimacy), state explicitly what this
initiative delivers in each — even "none" is a useful, honest answer for
a type that doesn't apply. Don't let cost-efficiency crowd out the other
three just because it's the easiest one to put a number on.

| Value type | Question to answer | How it's usually evidenced |
|---|---|---|
| Efficiency | What cost or staff time does this free up, and for what? | Hours saved, cost per transaction before/after |
| Service quality | What gets better for the person using the service? | Wait time, error rate, satisfaction |
| Equity | Who was underserved before, and how does this close that gap? | Disaggregated outcome data by group, not just an average |
| Trust/legitimacy | What becomes more transparent, accountable, or contestable? | Audit trail, explainability, appeal/complaint data |

### 2. Distinguish cost-avoidance from cost-savings

Public budgets often respond differently to "this frees up €X in the
existing budget" (savings, reallocatable) versus "this avoids €X in
future cost we would otherwise have had to spend" (avoidance, doesn't
free current budget but strengthens the case against a growing problem).
State which one an estimate actually is — presenting avoidance as
savings is a common, avoidable credibility error.

### 3. Give equity and trust value a defensible unit, even if not a
   monetary one

Not everything needs to be forced into a euro figure to be a rigorous
input to a decision. Where a value type resists monetization, use a
clear, stated, non-financial metric instead (e.g. "reduces the gap in
average processing time between the fastest- and slowest-served
language groups from 9 days to 2") rather than either fabricating a
monetary estimate or dropping the value type from the case entirely. Per
the pack-wide guardrail, never present an estimate as more precise or
certain than it is — mark assumptions explicitly.

### 4. Build the financial model on top of this, not instead of it

Once the public-value case is built, feed the monetizable elements (cost
savings, cost avoidance, measurable efficiency gains) into
`../../../../business-case-and-analysis/skills/roi-npv-sensitivity-model/SKILL.md`
for the standard financial modeling — but keep the non-monetized value
types visible in the final case rather than letting them disappear once
the spreadsheet starts. A public decision-maker who only sees the
financial model has been handed an incomplete case even if the model
itself is correct.

### 5. Pressure-test the case the way any business case should be
   pressure-tested

Once assembled, run it through
`../../../../business-case-and-analysis/skills/assumption-and-evidence-audit/SKILL.md`
or the independent `assumption-stress-tester` agent — public-value
claims (especially equity claims) are exactly the kind of soft,
hard-to-verify claim that benefits most from an adversarial second look
before it's presented.

## What this skill does NOT do

- Doesn't replace the core business-case or ROI/NPV skills — it's the
  framing layer that sits before and around them.
- Doesn't invent monetary values for non-financial benefits — see
  guardrail in step 3.
- Doesn't decide which value type matters most — that's a values and
  policy judgment for the client organization, not something this skill
  resolves on its behalf.

## Refinement notes

The efficiency/service-quality/equity/trust taxonomy is shared with
`ps-ai-opportunity-screening-for-public-value` — keep both skills'
definitions of the four types synchronized if either is refined.

## Continue from here

- Opportunity screening (defines the four value types): `../ps-ai-opportunity-screening-for-public-value/SKILL.md`
- Full business case: `../../../../business-case-and-analysis/skills/business-case-builder/SKILL.md`
- Financial modeling: `../../../../business-case-and-analysis/skills/roi-npv-sensitivity-model/SKILL.md`
- Adversarial review: `../../../../business-case-and-analysis/skills/assumption-and-evidence-audit/SKILL.md`
- Presenting the finished case: `../ps-decision-readiness-and-public-communication/SKILL.md`

## References

- `../../references/source-notes.md`

---
**Reminder:** frontmatter has only `name` and `description`. Everything
else goes into `skills_index.json` (run `scripts/generate_index.py`).
