---
name: trade-mail-group
description: Use when a foreign-trade operator already has a small customer list and needs conservative customer grouping, outreach angles, English subject lines, first-email drafts, follow-up cadence, and human review points before any sending happens.
---

# trade-mail-group

## Use When

- The user has 5-10 prospect companies and wants to avoid one generic cold email.
- The input includes product, target market, company names, industry, country, source, and short customer-intel notes.
- The next step is strategy and draft preparation, not automated sending.

## Do Not Use When

- The user needs SMTP setup, bulk sending, warm-up, tracking, or reply automation.
- The user only has a broad market with no company list.
- The task requires confirming procurement intent, budget, decision makers, or reply probability without evidence.

## Minimum Input

Required:

- `our_product`
- `target_market`
- `tone`
- `customers[]`
  - `company_name`
  - `country`
  - `industry`
  - `source`
  - `intel_summary`
  - `known_signal`

Optional but useful:

- source URLs or source notes
- forbidden claims
- brand voice
- offer constraints
- previous follow-up history

See:

- `examples/minimal-input.json`
- `examples/public-germany-input.json`
- `examples/meta-leads-visible-redacted-input.json`

## Workflow

1. Read the customer list and extract only stated facts.
2. Group customers into 2-4 mail groups using shared industry, use case, source signal, or risk boundary.
3. For each group, separate:
   - facts from the input
   - conservative business inferences
   - missing information that needs human review
4. Write one outreach angle per group.
5. Write 2-3 English subject line candidates per group.
6. Draft a short first email per group.
7. Add a first follow-up cadence.
8. Add handoff notes for `客户背调skill` and `开发信skill`.

## Output Contract

Return Markdown by default and keep the section names stable. Include:

- one-line conclusion
- input quality check
- grouping table
- per-group rationale
- per-group outreach angle
- English subject candidates
- first email draft
- follow-up cadence
- facts / inference / review notes
- explicit non-goals

If JSON is requested, use these top-level keys:

- `sample_type` if provided by the input
- `one_line_conclusion`
- `input_quality`
- `groups[]`
  - `group_id`
  - `group_name`
  - `companies`
  - `facts`
  - `inferences`
  - `outreach_angle`
  - `subject_candidates`
  - `first_email_draft`
  - `follow_up_cadence`
  - `human_review_points`
- `handoff`
  - `to_customer_intel_skill`
  - `to_outreach_email_skill`
  - `non_goals`

If the input is too weak to group safely, return `blocking_recommendation` instead of `groups[]`. Include `reason`, `missing_fields`, `recommended_next_action`, `safe_use_of_current_data`, and `do_not_do`.

## Quality Gates

- Every customer must appear in exactly one group unless explicitly excluded with a reason.
- Every group must include facts, conservative inferences, and human review points.
- Every first email must include uncertainty language when the source signal is indirect.
- Direct category overlap, competitor, supplier, or marketplace profiles must be marked as risk / benchmark / collaboration candidates, not ordinary buyers.
- If `source_url` is present, do not claim the source was verified unless you actually read it in this run.
- If the input is too weak to group safely, return a "needs customer intel first" recommendation instead of forcing groups.

## Rules

- Do not send email.
- Do not configure SMTP, mailbox warm-up, tracking pixels, or sequence automation.
- Do not invent customer demand, budget, supplier status, decision maker, or reply probability.
- Do not write "they need our product" unless the input explicitly proves it.
- Prefer "may be relevant because..." over hard claims when the signal is indirect.
- If a company fits more than one group, choose the safer group and mark the overlap.
- If source evidence is weak, make the email more exploratory.

## Recommended Handoff

- Send uncertain company facts to `客户背调skill`.
- Send approved group angle and selected subject line to `开发信skill`.
- Keep final sending manual or in the user's approved sending system.

## Example Outputs

- `examples/minimal-output.md`
- `examples/minimal-output.json`
- `examples/public-germany-output.md`
- `examples/public-germany-output.json`
- `examples/meta-leads-visible-redacted-output.md`
- `examples/meta-leads-visible-redacted-output.json`

## Validation

Run `python3 scripts/validate_examples.py` after editing examples or the JSON output contract.
