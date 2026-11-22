---
name: ab-test
description: Analyze an editable Lexsis landing-page URL, plan one controlled change, build verified challenger pages, and create or evaluate a draft A/B test. Use for URL-first storefront experimentation, not ordinary page editing.
---

# Create or Evaluate an A/B Test

Read `references/ab-testing.md` and
`references/consumer-behavior-cro.md`.

For offer, positioning, or pricing hypotheses, also read
`references/offers/offer-strategy.md`. Separate an actual price change from a
presentation test; confirm the purchase flow can honor each arm's terms before
building price challengers.

Use the host's available browser capability to inspect the supplied URL at
desktop and mobile widths. For Lexsis state, use
`lexsis_pages.find`, `lexsis_pages.get`, `lexsis_pages.edit_context`,
`lexsis_pages.source`, `lexsis_pages.compile`, `lexsis_pages.integrity`,
`lexsis_analytics.page`, `lexsis_analytics.experiment`,
`lexsis_workspace.credits`, `lexsis_drafts.page_duplicate`,
`lexsis_drafts.page_replace`, `lexsis_drafts.page_update_section`,
`lexsis_drafts.page_split_create` (whole-page and product/collection template
tests), `lexsis_analytics.page_split_get`, `lexsis_analytics.page_split_list`,
and `lexsis_drafts.experiment_create` (legacy blueprint variants). Bring a
running test's arms up to date with `lexsis_live_ops.experiment_refresh` only
after explicit approval.

Use `lexsis_live_ops.publish` and `lexsis_live_ops.scale_winner` only after
explicit approval. Resolve unfamiliar or newly available start/pause arguments
through exact router/action discovery.

Follow `references/ab-testing.md`:

1. Open and visually inspect the supplied Lexsis or custom-domain URL.
2. Resolve it to an editable Lexsis page and current source.
3. Present evidence-based candidates tied to one shopper uncertainty or
   behavioral pattern, then ask what the user wants to test.
4. Write and approve one focused `ab-test-plan.md`.
5. Confirm duplicate credits.
6. Build challengers locally, using isolated sub-agents when available.
7. Compile, duplicate, apply, and verify every challenger.
8. Create the draft experiment only after variant approval.

Default to one control and one challenger. Do not use `page_variation`, do not
let sub-agents perform paid or remote writes, and do not publish or start live
traffic merely because the user approved the test plan.

Return the control URL and page id, plan path, variant source and preview
paths, remote page and blueprint ids, experiment id, current state, and
remaining activation or evaluation steps.
