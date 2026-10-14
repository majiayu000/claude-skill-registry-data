---
name: clickmax-campaign-planning
description: Use when the user asks for a multi-week or multi-month marketing plan, campaign sequence, launch calendar or nurture strategy that should be built on the account's own history (open rates, base growth, tags, channels, brand voice) and later executed in Clickmax.
---

## When this applies

The user wants a plan that spans weeks or months (themes, channels, audience per phase, cadence, targets), and expects it to reflect THEIR account — not a generic marketing template.

Not this skill:

- one email or one automation right now -> `clickmax-flows`
- "how did my campaigns do" with no plan -> `clickmax-analytics`
- what is selling / sales trend only -> `clickmax-sales-insights`
- building the segment itself -> `clickmax-list-segments`

## Key assumptions

- A plan without the account's numbers is a failure of this skill. Every target must cite its baseline; every audience must name a real tag, list or filter and its measured size.
- Rates come as fractions (`0.295` = 29,5%); `null` = nothing sent, not zero.
- Campaign open/click rates are over sent recipients and count first opens only. Channel-wide `mcp__plugin_clickmax_clickmax__messages_metrics` rates are over reached recipients, include automations, and have no clicks — never mix the two in one comparison. WhatsApp shows up there as platform `gupshup`.
- Segments can filter by tag, list, purchase/transaction, product/offer, subscription, temperature status, score, UTM/origin, page or funnel visited, form/quiz answers, webinar attendance, email engagement (opened / clicked / received and did not open, in the last N days or on one campaign; opened at least N of the last M campaigns), lead creation date and lead fields. Email engagement counts people only — bot and scanner opens and clicks are excluded, so it can be lower than a campaign's reported opens — and it is the measured "engaged" audience; temperature is a complementary signal, not a substitute.
- "Engaged across campaigns" is one filter: `openedCount` (e.g. opened at least 2 of the last 5 campaigns received; "opened the last 3" = `min: 3, lastCampaigns: 3`). Prefer it over "opened in the last N days" when the plan cares about consistency, not recency, and say which one you used.
- WhatsApp free-form text only reaches contacts inside the 24h customer-care window; everything else needs an approved template. A WhatsApp step is only real if the account has a connected number and approved templates (or the plan includes creating them as a step — see `clickmax-flows`).
- There is no waitlist entity: a "waitlist" is a tag plus an automation.

## Thought process

1. Collect before planning — always, even when the user seems to want text only. Ambiguous goal → still read the snapshot first, then ask ONE question with the numbers in hand (the options can cite them).
2. Resolve the product being promoted (named by the user, else the top seller in the window) and its offer.
3. Derive the baseline: campaign open/click rate, base size and trend, channel mix and its trend, largest relevant tags.
4. Shape phases as a narrative that tightens the audience each phase (broad engaged base -> engaged in previous phase -> qualified non-buyers), with a measured size per phase.
5. Set targets as baseline + a bounded uplift justified by the tighter audience; never a round number pulled from nowhere. Baseline from fewer than 100 reached recipients → show the sample (`3 de 7`), call it a directional reference, and make the first phase's target "medir o baseline real"; never chain later targets off an earlier target.
6. Map every phase to Clickmax building blocks (tag, segment/list, automation, email, WhatsApp template, page/offer) so it can be built.
7. Offer to build phase 1; build nothing without explicit consent.

## Execute guide

1. `mcp__plugin_clickmax_clickmax__account_snapshot` with `windowDays = 90`. Read `unavailable` first — a source listed there was not read; say so, never fill it in. `emailCampaigns.baseline: null` with no `broadcasts` in `unavailable` = the account never sent an email campaign. `emailCampaigns.baseline` covers every email campaign the account ever sent — cite `campaigns` as the sample size.
2. Brand voice is already in the snapshot as `brand`. When `brandChoices` is not empty the workspace has more than one brand: before anything about tone, ask which brand this plan uses (options = the brand names, default one marked "padrão"), then `mcp__plugin_clickmax_clickmax__brand_get` with that `id` — never pick one yourself, not even by matching the product name. Otherwise call `mcp__plugin_clickmax_clickmax__brand_get` alone only to reread it later. Use every filled field of the brand in use, even when `status` is `draft`. Only when `brand` is null or `brand.voiceTone` is null, ask about tone (options: formal, professional, casual, playful, bold) before writing copy angles, and ALWAYS add a second question right after it in the same form: "Salvar esse tom na marca da conta, para os próximos planos já usarem?" with options yes / no. Never ask the tone without that save question. A "yes" is the consent for step 10 — save right after the answers arrive, before writing the plan.
3. If `emailCampaigns.baseline.campaigns` is below 3, also use `mcp__plugin_clickmax_clickmax__messages_metrics` for the same window to get an automation-inclusive email open rate, and label it as such. Need more than the 10 campaigns in `emailCampaigns.recent`? Use `mcp__plugin_clickmax_clickmax__broadcasts_list` with `channel = email`.
4. For the best past campaign, use `mcp__plugin_clickmax_clickmax__broadcasts_insights` to extract the best send hours (`opensByHour`) and the most-clicked link (`topLinks`) — reuse them as scheduling and CTA evidence.
5. Resolve audiences: match the user's words to `tags` from the snapshot (top 15 by size; `mcp__plugin_clickmax_clickmax__tags_list` / `mcp__plugin_clickmax_clickmax__lists_list` for the full set); measure each phase's audience with `mcp__plugin_clickmax_clickmax__segments_preview_count`. Combined audience (tag A AND tag B, tag AND temperature) = one top-level filter item per condition, each with a short label `id` ("a", "b"), `valueUuid` = the real tag id, temperature via `temperatureScore` + `valueNumber` (0-100; hot = `greaterThanOrEqual` the account cutoff, default 60). Engaged audience = `emailEngagement` item with `valueString` `{"engagement":"opened","withinDays":<N>}` (format and recipes in the `segments_preview_count` description; inactive = the same item negated). Report the measured count, not an estimate.
6. WhatsApp: `mcp__plugin_clickmax_clickmax__channel_instances_list`, then `mcp__plugin_clickmax_clickmax__gupshup_templates_list`; if approved templates exist, `mcp__plugin_clickmax_clickmax__gupshup_template_analytics` on the most used one (by its `externalId`) for read/click rates.
7. Product: the user's product, else `topProducts` from the snapshot or `mcp__plugin_clickmax_clickmax__insights_top_offers`.
8. Write the full plan with [the plan template](references/plan-template.md) as the reply text. The user sees only the reply text: a plan that stays in your reasoning was never delivered.
9. Only after the plan is written, offer concrete next actions: create the phase-1 tags and segment, build the phase-1 automation, draft the first email in the brand voice. Only execute after the user says yes.
10. Saving the brand voice (only after the user agreed — the save question of step 2, or a later "salva o tom"): `mcp__plugin_clickmax_clickmax__brand_save_draft` with `voiceTone` plus anything the user already stated in this conversation (`businessName`, `businessAudience`, `businessUsp`, words to prefer/avoid in `voiceVocabulary`) — never invent fields. Pass the `id` of the brand in use (the one the user chose, else the snapshot's `brand`); omit `id` only when `brand` was null (the brand is created as the account default). The brand stays a draft, which is enough for the next plan to use the tone. Publish with `mcp__plugin_clickmax_clickmax__brand_mark_ready` only if the user asks and the brand has `businessName`. Without permission to change account settings the save fails: say so and keep the tone for this conversation only.

## Report

- Open with "Diagnóstico da conta": 4–6 lines, each a number with its source window (base size + trend, campaign open/click baseline, channel mix and trend, relevant tags with sizes, product).
- Every KPI target shows `baseline -> target` (e.g. "abertura 29,5% -> 33%").
- Every audience shows how it is built in Clickmax and its measured size.
- Mark anything not measured as `estimativa` explicitly.
- Tone chosen in this conversation: say in one line whether it was saved to the brand. If the user declined or was never asked, include "salvar o tom na marca" among the next actions.
- Keep copy angles in the brand's tone and vocabulary; never use words in `voiceVocabulary.avoid`.
- Name tones in the user's language, never the raw value (pt-BR: formal, profissional, casual, divertido, ousado for formal, professional, casual, playful, bold) — in questions, options and the plan.
- Follow the language of the user.

## Warnings

- Do not invent tag names, list names or past results. If a needed tag does not exist, list it under "a criar".
- Do not promise features the account does not have (waitlist entity, free-form WhatsApp outside the 24h window).
- A saved segment with a day window is recalculated about once a day on screen; a broadcast to it recalculates the audience when created or scheduled. A phase scheduled days ahead freezes the audience at scheduling time: say so, and prefer scheduling close to the send date.
- Email engagement history before late September 2026 undercounts opens (older data kept only the first open, often a bot's): on long windows, call the number a floor.
- Do not state a campaign open rate from `mcp__plugin_clickmax_clickmax__messages_metrics`, or a channel rate from one campaign.
- Tag counts overlap: never add tag counts together — measure the combination with `mcp__plugin_clickmax_clickmax__segments_preview_count`; only if that call fails, show each tag's own count and say the combination was not measured.
- Dates: compute from today; name weekdays correctly; keep hard deadlines consistent across phases and messages.
- Urgency claims ("7 vagas restantes") must come from the user's real numbers — ask, or leave as a placeholder the user must fill.

## Anti-patterns

- Writing the plan first and fetching data "if the user asks".
- A generic 5-month template with round targets and no baseline.
- Audiences described as "contatos engajados" with no filter and no size.
- Ending with a list of options instead of offering to build phase 1.
- Asking "which part should I prepare?" without having written the plan first.

---

Clickmax skill revision: `b8294822a4d6`
