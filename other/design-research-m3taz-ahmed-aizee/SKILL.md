---
name: design-research
description: "Evidence-based design research via Refero + Mobbin MCP — search real shipped-product styles, screens, flows, and website sections BEFORE designing. Use for any UI design, redesign, landing page, dashboard, paywall, onboarding, or UX-flow task. Research is mandatory: no design from vibe memory."
personas:
  - UX
  - UI
  - DEV
  - SOCIAL
triggers:
  - design research
  - ui inspiration
  - design references
  - refero
  - mobbin
  - landing page design
  - redesign
  - ui patterns
  - ابحث عن تصميم
  - مراجع تصميم
  - الهام تصميم
tech_stack:
  - referodesign/refero
  - mobbin/mobbin
---

[SKILL] design-research
[OBJ] Ground every design decision in real shipped-product evidence via the `refero` and `mobbin` MCP servers — then hand off to `design-md-lord` for token application.

[TOOL-MAP] Pick the layer that answers the question:
| Need | Refero | Mobbin |
|---|---|---|
| Visual direction/taste, tokens, typography | `refero_search_styles` + `refero_get_style` | — |
| Concrete screen/pattern/state | `refero_search_screens` (+`get_similar_screens`, `get_screen_image`) | `search_screens` |
| Multi-step journey | `refero_search_flows` + `refero_get_flow` | `search_flows` |
| Website section (hero/pricing/footer) | — | `search_sections` |
| iOS app screens/flows | `platform=ios` | native coverage |

[RULES]
1. [PROHIBIT] No design from vibe memory — every major visual, layout, content, or interaction decision MUST trace to a searched reference, the user's brief, or a craft doc. Research before implementation, always.
2. [REQ] Search several angles before choosing: 3–5 queries — one broad aesthetic, one domain/category, one named strong product. Compare ≥3 real examples; never copy a single reference.
3. [REQ] Pick ONE dominant direction, don't average. When references conflict, keep the primary's signature traits sharp; secondary references contribute 1–2 narrow details only. Averaged references = generic AI slop.
4. [REQ] Evidence, not proof: a shipped example shows a product USED a design — it does not prove the design performs. A recurring pattern is a convention, not a best practice. Separate "observed on screen" from "recommended".
5. [REQ] Preserve provenance: for every load-bearing reference record product name + canonical URL (Refero/Mobbin link). Check capture metadata when recency matters.
6. [REQ] Token-meaning discipline: if a reference assigns a color/radius/shadow/role, use it only for that role — same law as `design-md-lord` rule 6–7.
7. [REQ] Brief before searching — missing info only if it materially changes the result: `Designing [WHAT] for [WHO] on [PLATFORM]. Goal: [...]. Tone: [...]. Objection: [...]. Must remember: [HOOK]. Constraints: [...]. Research needed: [styles/screens/flows/sections].`
8. [REQ] Reference-lock before build: lock (a) a user-provided source, (b) an existing design-system target, or (c) an explicit reference-locked direction + decision ledger (why this reference, what we take, what we reject).
9. [REQ] Validate after building: compare rendered output against the locked reference; fix design drift — research alone is not "done". Follow with `DesignSlopVerifier` + `ui_a11y_checker` (a11y is evaluated independently — a real product's choice is not an a11y guarantee).
10. [PROHIBIT] No verbatim copying: no protected layouts, branding, copy text, logos, or assets — extract the structure and the why, rebuild it for THIS product.
11. [REQ] Rate limits: Mobbin MCP = 60 req/60s — batch sensibly, respect `Retry-After` on 429. Weak results → query more specifically (platform + category + pattern + goal); too narrow → drop constraints.
12. [REQ] MCP absent? Do NOT fake research — state it plainly and proceed with `design-md-lord`'s bundled catalog references + the user's own examples. Reference-lock still applies.

[WORKFLOWS]
1. New page/screen: brief → `search_styles` (direction) + `search_screens`/`search_sections` (composition) → compare 3+ → lock primary + ledger → `design-md-lord` for token application → build → slop + a11y verify.
2. Flow task (onboarding/checkout/paywall/cancel): `search_flows` → `get_flow` → map step goals/actions/system responses → adapt to product → build → verify sequence against reference flow.
3. Design critique/audit: capture current state → pull comparable `search_screens` evidence → report observed-vs-recommended per rule 4 → diff → fix.
4. Mobile: `platform=ios` (Refero) or Mobbin screens → respect platform HIG conventions found in references.
