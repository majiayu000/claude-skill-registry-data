---
name: ps-community-and-equity-impact-assessment
description: "Checks an AI-enabled public service design for differential impact across community groups before launch: digital divide, accessibility, and disparate-treatment risk. Use before a public-facing AI service goes live, or when a proposal claims a general improvement and hasn't yet been checked group by group."
---

# Community and Equity Impact Assessment

## Purpose

An AI service can genuinely improve outcomes on average while making
things worse for a specific group — slower, harder to access, or
systematically less accurate for them. In a private-sector context this
is a product-quality problem; in a public sector context it is also a
fairness and, often, a legal problem, since public services generally
carry an obligation to serve all eligible groups, not just the average
user well. This skill is a structured check for that gap, run before
launch rather than discovered after.

## Method

### 1. List who is actually eligible or affected — not just who is
   using the service today

Start from the full eligible population, not the current user base — a
service that already underserves a group will show that group as a
small share of "current users," making the gap invisible if you only
look at existing usage data. Ask: who is entitled to or affected by this
service, and does that list match who the AI system was designed and
tested against?

### 2. Check each of the standard differential-impact categories

Work through these explicitly rather than relying on a general sense
that "it should be fine for everyone":

- **Digital access**: does using this require a device, connectivity,
  or digital literacy level not everyone in the eligible population has?
  Is there a non-digital fallback, and is it genuinely equivalent, not a
  token alternative?
- **Language**: does the system perform as well in every language the
  service is legally or practically expected to support? AI systems
  (especially language models) frequently perform worse in
  lower-resource languages — this needs to be tested, not assumed.
- **Disability and accessibility**: does the interface and the AI
  system's outputs meet accessibility standards, and has it been tested
  with assistive technology, not just checked against a checklist?
- **Age**: does the design assume a level of comfort with technology
  that skews against older (or, in some cases, younger) users?
- **Socioeconomic and geographic**: does access depend on factors
  correlated with income or location (broadband quality, ability to
  take time off during service hours) in ways the previous, non-AI
  process didn't?

### 3. Test for algorithmic disparate treatment, not just access

Beyond who can reach the system, check whether the AI's outputs
themselves differ systematically by group for people in comparable
situations — e.g. does an eligibility-scoring or triage system produce
different outcomes for otherwise-similar cases that differ only by a
protected characteristic or a strong proxy for one (postcode, surname
patterns)? This requires disaggregated outcome data, not an aggregate
accuracy figure — an aggregate accuracy figure can look excellent while
hiding a large gap for a minority subgroup.

### 4. Distinguish a designed trade-off from an unexamined gap

Not every group difference is a problem to fix — sometimes a service is
deliberately targeted (e.g. at low-income applicants only). The check
here is whether a *difference in quality of service delivery* exists
for people who are all supposed to be served equally well, and whether
it was a deliberate, justified design choice or simply never tested for.
Name which one it is explicitly in the assessment output.

### 5. Feed findings into the decision, not just a report

Findings from this skill should feed directly into
`ps-regulatory-and-ethical-guardrails-for-public-ai` (since a disparate
outcome may cross into legal, not just ethical, territory) and into
`ps-decision-readiness-and-public-communication` element 3 (trust) — an
equity check that was run and passed is itself strong evidence for the
decision-readiness case; a check that wasn't run is a visible gap a
scrutinizing decision-maker or journalist will likely ask about.

## What this skill does NOT do

- Doesn't perform statistical bias testing itself — it structures what
  to test for and how to read the results; the actual data analysis may
  need `../../../../data-strategy-and-literacy/skills/data-bias-and-quality-critical-reading/SKILL.md`
  or a data science function.
- Doesn't make the legal determination of unlawful discrimination — see
  `ps-regulatory-and-ethical-guardrails-for-public-ai` for when to
  escalate to legal review.
- Doesn't replace direct engagement with affected communities — this is
  a structuring tool for that engagement, not a substitute for it.

## Refinement notes

The five differential-impact categories are a general-practice synthesis
for public services, not drawn from one named framework. If the owner
has direct case experience with a specific equity failure mode in public
AI deployments, it belongs here as a concrete, named example.

## Continue from here

- Bias/data quality: `../../../../data-strategy-and-literacy/skills/data-bias-and-quality-critical-reading/SKILL.md`
- Legal/regulatory escalation: `../ps-regulatory-and-ethical-guardrails-for-public-ai/SKILL.md`
- Presenting the finding: `../ps-decision-readiness-and-public-communication/SKILL.md`

## References

- `../../references/source-notes.md`

---
**Reminder:** frontmatter has only `name` and `description`. Everything
else goes into `skills_index.json` (run `scripts/generate_index.py`).
