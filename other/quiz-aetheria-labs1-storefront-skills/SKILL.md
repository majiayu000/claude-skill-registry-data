---
name: quiz
description: Create, update, validate, or preview a Lexsis Quiz island with real product recommendations, branching, variant matching, optional response saving, and consent-aware analytics.
---

# Create a Quiz

Use the live `Quiz` island for the journey. Read
`references/quiz-authoring.md` and the current `vibe://schema/island/Quiz`
before authoring. Resolve unfamiliar MCP arguments through `lexsis_discover`.

## Workflow

1. Resolve the exact workspace, store, page, and theme. Load brand context and
   inspect available desktop/mobile references. Keep the same theme throughout.
2. Refresh real candidate products and variants with `lexsis_catalog`; never
   invent Shopify IDs, prices, availability, option values, or result imagery.
3. Plan stable keys, questions, branches, scoring, deterministic fallback,
   result explanations, product/variant mapping, and entry and exit actions.
   Remove questions that serve no recommendation or stated capture purpose.
4. Decide whether responses should be saved. For saving, define the purpose,
   disclosure, question classifications, merchant visibility, retention, resume
   window, and optional contact purpose. Saving and analytics are independent;
   collecting contact details does not subscribe the visitor to marketing.
5. Author one complete `Quiz` definition in normal page source. Use scoped CSS,
   supported hooks, and managed motion for transitions. Preserve focus and
   reduced-motion behavior; do not invent runtime presets or custom state machines.
6. Compile, repair blockers, then create or update the requested unpublished
   draft with version protection. Keep source and QA in MCP; do not save local
   JSON dumps, screenshot reports, or ad hoc page artifacts.
7. If saving is requested, inspect the immutable page-version UUID using
   `lexsis_capture.quiz_inspect` and prepare its inactive policy with
   `lexsis_drafts.quiz_prepare`. Reinspect after any source edit.
8. Test reachable branches/results, ties/fallbacks, required/optional inputs,
   back/review/restart, unavailable variants, Cart V2 outcomes, focus, transitions,
   and reduced motion at 390, 768, and 1280. Record supported hosted QA via MCP.
9. Return `DRAFT_CREATED` while QA or approval is pending. Record
   `DESIGN_APPROVED` only after hosted QA and explicit approval of that same
   version. This is a valid handoff to `/publish`.
10. When explicitly authorized, activate the reviewed policy with
    `lexsis_live_ops.quiz_activate` and publish the reviewed page through
    `/publish`. These are separate decisions; reuse approval already given for
    the exact scope. Preview does not prove production capture.
11. After publication, verify saving allowed/declined and analytics allowed/denied,
    edit/reload/retry, one completed Forms response, and redacted MCP reads.
    Use the returned published URL. Report any untested path or live limitation.

## Boundaries

- Definitions live in page source. Saved responses use the managed capture
  policy and Forms response viewer; do not edit generic Forms schemas to bypass it.
- Personal and sensitive answers are protected; MCP exposes only permitted
  categorical values. `analytics.answerAllowlist` does not allow raw analytics.
- Result commerce uses Quiz `add_items`. Do not add hidden BuyBoxes, direct
  Shopify requests, authored cart shells, or programmatic clicks.
- `reward` and `offer` actions are unavailable. Verify existing cart promotions
  separately before claiming a discount or gift.
- Only use registered islands and host capabilities present in the live schema.
  If supported hooks cannot express the design, identify the reusable host
  change needed; do not fabricate an island or inject arbitrary JavaScript.
- Do not promise automatic result email, marketing sync, a dedicated quiz funnel
  dashboard, paid-order attribution, preview capture, or historical-version resume.

## Return

Report page/version and hosted URL; product sources and tested paths; responsive,
cart, and motion QA; saving policy state; activation/publication state; and live
capture/analytics evidence or pending checks. Keep design approval, policy
activation, publication, confirmed saving, and purchase as separate outcomes.
