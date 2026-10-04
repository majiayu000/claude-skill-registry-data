---
name: responsible-ai-and-governance-check
description: "Classifies an AI initiative's EU AI Act risk tier and surfaces the regulatory, data-governance, and ethics obligations that follow from it, as a first-pass structuring check rather than a legal opinion. Use before an AI initiative goes to approval, especially one touching employment, credit, biometric, or other high-risk decisions about individuals."
---

# Responsible AI & Governance Check

## Purpose

Checks the regulatory, risk, and ethics dimensions of an AI initiative
before it goes to approval. Deeper EU AI Act compliance analysis requires
separate regulatory expertise — this skill is a first-pass structuring
check, not a legal opinion.

## Anchored in research

- EU AI Act (Regulation (EU) 2024/1689)
- LinkedIn 2026 — Risk & Compliance Management

## Method

1. **Classify the system's risk tier under the EU AI Act's risk
   pyramid**, as a first-pass, non-binding read:
   - **Unacceptable risk (prohibited)** — e.g. social scoring,
     manipulative or subliminal techniques, most forms of real-time
     remote biometric identification in public spaces. If the
     initiative plausibly falls here, stop and escalate to legal
     counsel immediately — don't proceed to scoring the rest of the
     initiative as if it were a normal risk trade-off.
   - **High risk** — systems used in the areas the Act lists in Annex
     III (e.g. employment/HR decisions, access to essential services
     including credit scoring, education and exam scoring, law
     enforcement, biometric categorization, critical infrastructure
     management). High-risk classification triggers obligations
     around risk management, data governance, technical
     documentation, logging, human oversight, and conformity
     assessment — flag these as required workstreams, don't estimate
     them from memory.
   - **Limited risk** — systems with transparency obligations, e.g.
     the user must be told they're interacting with AI, or that
     content is AI-generated (chatbots, deepfakes, emotion-recognition
     systems).
   - **Minimal risk** — the majority of AI applications (e.g. spam
     filters, most internal productivity copilots) — no additional
     obligations beyond general product/consumer law.
   Mark the classification `[assumption — verify]` and route it to a
   qualified regulatory reviewer before it's treated as final — this
   skill's classification is a triage aid, not a determination.
2. **If the initiative is high risk or above, list the concrete
   obligations that follow, without estimating their cost or effort
   from memory:** a risk-management system, data governance and
   quality measures, technical documentation, automatic logging,
   human-oversight design, accuracy/robustness/cybersecurity
   requirements, and (for certain categories) third-party conformity
   assessment before market placement. Route the detailed compliance
   work to regulatory/legal expertise — this skill only makes the
   obligation list visible early enough to factor into scoping and
   timeline.
3. **Check the initiative against a broader ethics lens than pure legal
   compliance** — a system can be legally compliant and still cause
   real harm or reputational damage:
   - **Fairness** — could the training data or the decision logic
     produce systematically worse outcomes for a protected group?
     Has this been tested, or only assumed absent?
   - **Transparency and explainability** — can the organization explain,
     in plain language, why the system produced a given output to
     someone affected by it?
   - **Accountability** — is there a named human owner who is
     answerable for the system's outcomes, distinct from whoever built
     it?
   - **Privacy** — does the system process personal data in a way that
     needs a separate GDPR/data-protection assessment (a different,
     complementary check from this one — flag it, don't attempt it
     here)?
4. **Cross-check the Speed to Value & Governance/Risk score already
   assigned in `../ai-opportunity-portfolio/SKILL.md`** against this
   deeper check — if the risk tier found here is materially higher than
   what that score assumed, flag the mismatch and recommend the score
   be revisited rather than silently proceeding.
5. **Produce a structured governance checklist result**: risk tier
   (with `[assumption — verify]` where applicable), triggered
   obligations, ethics-lens findings, open questions requiring legal
   sign-off (see `../../references/` once a template is added).
6. Validate the result with stakeholders or your own experience-based
   checklist, and route anything above minimal risk to qualified
   regulatory counsel before the initiative proceeds to approval.

## What this skill does NOT do

- Doesn't make the final decision for you — it produces a structured
  draft to support a human decision.
- Doesn't confirm figures, market data, or competitor data from
  memory — it uses the inputs you provide, or marks an assumption
  clearly (`[assumption — verify]`).
- Doesn't give a legally binding interpretation of the AI Act — it
  surfaces the risks and routes the initiative to deeper compliance
  analysis; only qualified legal counsel can give a binding
  classification or sign-off.
- Doesn't perform a GDPR/data-protection assessment — that's a
  distinct, complementary check; this skill only flags when one is
  needed.

## Refinement notes

Areas to keep deepening with real practice:

- your own rules of thumb and heuristics for this technique — e.g.
  which initiative types most often turn out higher-risk than they
  first appear
- concrete templates (into `../../references/`, e.g. a governance
  checklist template)
- reference cases / your own examples
- what this skill deliberately does *not* do (guardrails, common
  mistakes) — add to the list above

Once this section is filled in and validated in practice, update the
`maturity` field in `skills_index.json` to `draft`, `validated`, or
`canonical` (see `../../../meta/maturity_levels.md`). **Don't add new
fields to the frontmatter** — `name` and `description` are the only
ones allowed (see `../../../meta/frontmatter_schema.md`).

## Continue from here

- Next in this pack: `../build-vs-buy-vs-partner-ai/SKILL.md` —
  structures the decision to build in-house, buy off a platform, or
  partner on an AI solution.
- If the deployer is a public body: the transparency, fairness, and
  human-oversight bar is generally higher for citizen-facing decisions —
  see
  `../../../specialisation-packs/public-sector-ai-service-design/skills/ps-regulatory-and-ethical-guardrails-for-public-ai/SKILL.md`
  for the public-sector-specific triage on top of this check, and
  `../../../specialisation-packs/public-sector-ai-service-design/skills/ps-community-and-equity-impact-assessment/SKILL.md`
  for the differential-impact check referenced in step 3's fairness
  lens.
- A ready-made skill chain for this situation: see `../../../playbooks/`
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/` — the pack's shared background material
- `../../CLAUDE.md` — the pack's shared guardrails
