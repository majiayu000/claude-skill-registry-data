---
name: clickmax-visitors
description: Use when the user asks about site visitors, traffic sources, channels or campaigns that brought visits/leads, the visitor conversion funnel, what is happening on the site right now, or what a contact browsed before converting.
---

## When this applies

Use this skill for questions about the tracked visitors of the user pages (Contatos → Visitantes): traffic volume, channels and campaigns, conversion of visitors into contacts, the event funnel, live activity, and the browsing a contact did before being identified.

Not this skill:

- contact/lead records and their custom fields -> `clickmax-leads`
- funnel structure (pages, nodes, checkout) -> `clickmax-funnels`
- custom Insights dashboards and widgets -> `clickmax-insights-dashboards`

## Key assumptions

- A visitor is a browser/device, not a person: one contact can have several visitors (phone + desktop).
- Two attribution models live on the screens, and the answer must name the one it uses:
  - `visitors_list`, `visitors_get` and `visitors_lead_journey` use the channel of the visitor FIRST session (first click — "what brought this person").
  - `visitors_analytics` origin breakdowns and `visitors_attribution` count each SESSION toward the channel it arrived through.
- "Contact generated" = the visitor has an identity link to a contact; `conversionRate` = contacts / visitors.
- `visitors_attribution` rows are channel + campaign PAIRS: the same `utm_campaign` on Google and Facebook are two rows — never add them as one campaign.
- Funnel steps count distinct visitors who reached that step OR a later one in the period; the order of events is not enforced.
- Periods default to the last 30 days and are capped at 180 days.
- Ad click IDs (`clickIds`: fbclid = Meta, gclid/gbraid/wbraid = Google, ttclid = TikTok, msclkid = Microsoft) are shown for checking against the ad manager; they do not change the channel classification.

## Thought process

1. Decide the question type: volume/breakdown (analytics), campaign ranking (attribution), drop-off (funnel), right now (live), one visitor (get) or one contact (lead journey).
2. Resolve the period and project before calling; ask only if the user gave none and the default 30 days would mislead.
3. For one contact, resolve the `leadId` with the leads tools first.

## Execute guide

- Use `mcp__plugin_clickmax_clickmax__visitors_analytics` for totals, daily series and breakdowns by channel, UTM, referrer, landing page, project, pages/funnels/forms, geography and device. Pass `timeZone` when the user asks about hours or weekdays.
- Use `mcp__plugin_clickmax_clickmax__visitors_attribution` for "which campaign/channel brought the most leads"; read `hasMoreCampaigns` before saying the list is complete.
- Use `mcp__plugin_clickmax_clickmax__visitors_conversion_funnel` for drop-off between page view, form view, form submit, checkout start and approved purchase; pass `channel` to compare channels.
- Use `mcp__plugin_clickmax_clickmax__visitors_live_events` to check whether tracking is receiving events now; an empty result means no actions in the last 24 hours.
- Use `mcp__plugin_clickmax_clickmax__visitors_lead_journey` for "what did this contact do before converting"; mention when a link is not confirmed (`linkType` other than form_submit/checkout).
- Use `mcp__plugin_clickmax_clickmax__visitors_list` + `mcp__plugin_clickmax_clickmax__visitors_get` only to inspect specific visitors; never page the list to compute totals.
- Before calling any list complete, read its cut flags: `hasMoreCampaigns`, `hasMoreVisitors`, `hasMoreSessions`, `hasMoreEvents`, `hasMorePages`.

## Report

- Lead with the number that answers the question, then the period and the attribution model used.
- For campaigns, show channel + campaign together and the conversion with its definition.
- For the funnel, show each step with the visitors and the drop from the previous step.
- For a contact journey, show origin first, then the sessions before identification with the pages viewed.

## Warnings

- Do not mix numbers from the first-click screens with the per-visit breakdowns without saying so.
- Do not present a click ID as proof of paid traffic: Meta also adds fbclid to organic post clicks.
- Visitor data only exists for pages with tracking active; zero visitors may mean tracking is not installed.

## Anti-patterns

- Summing the same campaign across channels.
- Paging `visitors_list` to count visitors.
- Calling a visitor "the contact" when the link is probabilistic.

---

Clickmax skill revision: `b8294822a4d6`
