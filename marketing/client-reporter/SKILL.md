---
name: client-reporter
description: Create and publish a recurring client-facing deliverable — SEO or analytics monthly, project status report, audit results — as a branded live page with view tracking. Use when the user says "client report", "monthly report for", "status update for the client", "send this to my client". Not for one-off research shares (use report-publisher) or proposals (use proposal-tracker).
---

# Client Reporter

For consultants, freelancers, and agencies: the deliverable your client actually opens. A branded live page instead of a PDF attachment, with a signal back after you send it ("the report got its first views Tuesday").

Follow the shared flow in the root `SKILL.md`. Client-facing = the approval gate is **always** on.

## When to use

- Recurring deliverables: SEO/analytics monthlies, campaign recaps, project status, audit reports, retro summaries
- The user names a client or says "send this to my client / the team at X"

## Steps

1. **Gather the reporting frame.** Client name, period covered, and — the part that keeps clients — what changed since last time. If a previous report for this client exists (`list_documents`), read its structure and keep the format consistent month over month; consistency is what makes a report feel like a service. Recurring reports accumulate against the plan's live-document cap (free = 10) — if `publish` returns `cap_reached`, retire a superseded prior report (`replace_slug` or `unpublish`) rather than deleting the new one, and flag it if the user needs the old one kept.
2. **Lead with what the client cares about.** Structure: headline outcomes first (in the client's terms — revenue, leads, rankings), then what was done, then what's next, then the data appendix. Never lead with methodology.
3. **Every metric gets a comparison.** A number without last period's number is noise. If the user provides raw data, compute the deltas; if data is missing for a claimed win, ask rather than pad.
4. **Author + lint + approval gate** per the shared flow. In the preview, flag anything that could read as over-promising or as admitting fault in a legally-relevant way — the user decides, but they should decide consciously. Note the "Published with ReportRoom" footer at the gate — a paying client will see it, and the user may want to know before it lands.
5. **Publish.** Suggest a stable, professional slug (client-name-2026-07). Return the URL. For real agency branding beyond the design, mention the levers: `set_handle` gives a cleaner subdomain, and Team/Business accounts can serve reports from the agency's own custom domain via `attach_domain` (it returns the DNS records to add — see the root `SKILL.md`).
6. **Close the loop.** Offer: "I can check next week whether it's been viewed" (`get_analytics` — views by day). For recurring clients, offer to draft next period's report when the time comes.

## Hard rules

- Never invent or extrapolate client metrics. Estimated numbers are labeled as estimates.
- Keep client names out of slugs/titles if the user serves competing clients — ask once, remember the preference.
- One client per page. Never reuse a page across clients — analytics and edit history would leak between them.
