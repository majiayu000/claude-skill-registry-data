---
name: ps-regulatory-and-ethical-guardrails-for-public-ai
description: "Frames the distinct regulatory and ethical stakes of public-facing AI - higher transparency and accountability bar, disparate-impact risk, due-process concerns when AI touches decisions about individuals - and identifies when a question needs real regulatory or legal expertise rather than general reasoning. Use early when scoping any AI system that will touch citizen-facing decisions or services."
---

# Regulatory and Ethical Guardrails for Public-Sector AI

## Purpose

`ai-strategy-and-governance:responsible-ai-and-governance-check` covers
the general regulatory, risk, and ethics dimensions of an AI initiative
and is explicit that deeper EU AI Act compliance analysis needs separate
regulatory expertise. This skill narrows that same posture to what
changes specifically when the deployer is a public body: AI touching a
citizen's access to a benefit, service, or legal status carries a higher
transparency and due-process bar than the equivalent private-sector use
case, and often a different regulatory classification. This is a
framing and triage skill, not a compliance determination.

## Method

### 1. Ask what kind of decision the AI touches

Sort the use case into one of three bands before anything else:

- **Back-office / internal efficiency** — no direct effect on an
  individual citizen's rights, benefits, or treatment (e.g. internal
  document search, scheduling optimization). Lowest stakes band.
- **Citizen-facing but advisory** — AI informs a decision a human still
  makes and can override (e.g. flagging a case for human review,
  drafting a response a caseworker edits and sends).
- **Citizen-facing and decision-affecting** — AI materially shapes an
  outcome that affects a specific person's access to a service, benefit,
  or legal standing (e.g. eligibility scoring, risk flagging that
  triggers enforcement action, automated triage that limits which
  service track someone is offered).

The third band is where public-sector AI regulation and administrative
due-process expectations bite hardest — flag it explicitly and treat it
as requiring specialist regulatory review, not just this skill's
checklist.

### 2. Check the transparency and explainability bar

Public bodies are generally held to a higher explainability standard
than private companies for decisions affecting individuals — an opaque
"the model said so" is much harder to defend when the decision affects
someone's access to a public service and is subject to appeal or
freedom-of-information requests. Ask: can this system's individual
decisions be explained to the affected person and to an appeals body in
terms a non-technical person can follow? If not, that's a design
requirement to solve before launch, not a caveat to disclose after.

### 3. Screen for disparate impact before launch

Ask specifically who might be systematically disadvantaged by this
system relative to the status quo — by language, disability, digital
access, age, or any protected characteristic relevant in the
jurisdiction — not just whether the system works well "on average."
This overlaps with, and should be run together with,
`ps-community-and-equity-impact-assessment` for the full picture.

### 4. Check for a human-in-the-loop requirement

For the decision-affecting band (step 1), default to assuming a human
review/override point is required unless a specialist confirms
otherwise — many public-sector AI regulatory regimes require this
explicitly for higher-stakes automated decisions. If the design doesn't
currently have one, flag it as a likely gap rather than a stylistic
choice. For the mechanics of designing that human checkpoint well, use
`../../../../human-ai-collaboration-design/` (this repo's core pack on
HITL design).

### 5. Name the regulatory regime, don't guess its content

If the initiative is inside the EU, note explicitly that the EU AI Act's
risk classification (and its stricter obligations for systems used by
public authorities, particularly in areas like eligibility for public
benefits, law enforcement, and migration) is likely relevant and needs
confirmation from a qualified source — don't state a specific risk
classification or compliance obligation from general knowledge. The same
applies to national data-protection and administrative-law requirements.
If a dedicated AI-regulation or legal skill resource is available
separately, hand this question to it explicitly rather than answering it
inside this skill.

## What this skill does NOT do

- Doesn't determine actual legal or regulatory classification — flags
  when that determination is needed and by whom.
- Doesn't replace `../../../../ai-strategy-and-governance/skills/responsible-ai-and-governance-check/SKILL.md` —
  narrows and sharpens it for the public-sector case.
- Doesn't design the human-oversight mechanism itself — see the
  `human-ai-collaboration-design` pack for that.

## Refinement notes

Written deliberately without citing specific article numbers or national
statutes, since regulatory specifics change and vary by jurisdiction —
the goal is durable triage logic (what to ask, when to escalate), not a
compliance summary that goes stale.

## Continue from here

- General governance check: `../../../../ai-strategy-and-governance/skills/responsible-ai-and-governance-check/SKILL.md`
- Human-oversight design: `../../../../human-ai-collaboration-design/`
- Equity/community impact: `../ps-community-and-equity-impact-assessment/SKILL.md`
- Procurement/funding triage: `../ps-procurement-and-public-funding-navigation/SKILL.md`

## References

- `../../references/source-notes.md`

---
**Reminder:** frontmatter has only `name` and `description`. Everything
else goes into `skills_index.json` (run `scripts/generate_index.py`).
