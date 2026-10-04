---
name: ps-procurement-and-public-funding-navigation
description: "Flags when an AI idea has crossed from 'just build it' into public-procurement or public-funding territory, and what that changes about timeline, vendor choice, and design freedom. Use when scoping or building an AI solution for a public body, before committing to a build-vs-buy path or a delivery timeline."
---

# Public Procurement and Funding Navigation

## Purpose

`ai-strategy-and-governance:build-vs-buy-vs-partner-ai` structures the
build/buy/partner decision on its technical and organizational merits. In
a public-sector context, that decision is frequently constrained before
it's even made: procurement law, budget-cycle timing, and the funding
source (municipal budget, national grant, EU funding, a mix) all shape
what's actually achievable and by when. This skill is a triage tool: it
tells you *when* you've hit one of these constraints and what it changes
about the project — it does not give procurement-law advice itself.

## Method

### 1. Identify the funding source first

Before scoping technical options, establish:

- Is this funded from the organization's own operating budget, a
  dedicated project/investment budget, a national grant, EU funding, or
  some combination?
- Each source typically comes with its own reporting requirements,
  eligible-cost rules, and timeline — a solution technically ready in
  six weeks can still be blocked for months by a funding cycle that only
  disburses annually, or by reporting obligations tied to how the money
  was justified.
- If the funding involves EU or national grant money, flag explicitly
  that additional dissemination, reporting, or results-ownership
  obligations likely apply, and that these need specialist confirmation
  — don't assume standard commercial terms apply.

### 2. Check the procurement threshold

Ask directly (don't estimate from memory): does this organization have a
procurement threshold above which a formal competitive tender is legally
required, and does this project's value cross it? If unknown or unclear,
say so explicitly and flag it as a question for the organization's own
procurement or legal function — a wrong assumption here (proceeding as a
direct purchase when a tender was actually required) is a serious,
not a cosmetic, mistake.

### 3. Know what a formal procurement process changes

If a tender is required, this changes the project fundamentally, not
just its timeline:

- **Timeline**: procurement processes routinely add months, not weeks.
  Any scoping work should assume this before promising a delivery date.
- **Design freedom**: requirements typically have to be locked and
  published before vendor selection — late-stage design changes are much
  harder once a tender is live.
- **Vendor pool**: some AI vendors, especially smaller or newer ones, may
  not be structured to bid on public tenders at all, narrowing the
  realistic option set.
- **Documentation burden**: decisions need to be defensible on paper, not
  just sound in the room — this feeds directly into
  `ps-decision-readiness-and-public-communication`.

### 4. Consider a pilot or exemption path if the situation allows it

Many procurement regimes have lower thresholds or specific exemptions for
small-scale pilots, proofs of concept, or innovation partnerships — but
whether these apply, and how, is jurisdiction-specific and must be
confirmed by the organization's own procurement function, not assumed
from general knowledge. Where relevant, this repo's user may have access
to a dedicated public-procurement legal skill set — if so, use that for
the actual legal analysis and treat this skill's output as the business
framing that goes into that conversation, not a replacement for it.

### 5. Translate constraints into the roadmap and business case

Once the funding source and procurement path are clear, feed the
resulting timeline and design-freedom constraints into
`ps-public-value-business-case-framing` and into whatever roadmap or
sprint plan is being built — don't let a technically optimistic timeline
survive contact with a procurement requirement that wasn't checked
early.

## What this skill does NOT do

- Doesn't give procurement-law or grant-compliance advice — it flags
  when specialist advice is needed and what to ask.
- Doesn't determine actual legal thresholds, which vary by
  jurisdiction and organization type — always confirm locally.
- Doesn't replace `../../../../ai-strategy-and-governance/skills/build-vs-buy-vs-partner-ai/SKILL.md` —
  it constrains that decision, it doesn't make it.

## Refinement notes

Procurement thresholds and exemption rules are highly jurisdiction- and
sector-specific (EU public procurement directives, national
implementations, and municipal-level rules all differ). This skill is
deliberately written at the level of "what to ask and when it matters"
rather than citing specific thresholds, to avoid presenting
jurisdiction-specific legal detail as general truth.

## Continue from here

- Build/buy/partner decision: `../../../../ai-strategy-and-governance/skills/build-vs-buy-vs-partner-ai/SKILL.md`
- Business case with the resulting constraints: `../ps-public-value-business-case-framing/SKILL.md`
- Presenting a procurement-shaped decision to the board: `../ps-decision-readiness-and-public-communication/SKILL.md`

## References

- `../../references/source-notes.md`

---
**Reminder:** frontmatter has only `name` and `description`. Everything
else goes into `skills_index.json` (run `scripts/generate_index.py`).
