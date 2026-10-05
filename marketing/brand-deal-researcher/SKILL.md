---
name: brand-deal-researcher
description: Find paid promotion, sponsorship, brand deal, influencer campaign, creator partnership, affiliate, and paid collaboration opportunities in a user's Gmail or email exports; research each brand/client; dedupe follow-ups; prioritize fit; and produce a Markdown table, document, or spreadsheet of brand leads with notes. Use when the user asks to scan recent email for brand deals, paid promo offers, sponsorship pitches, creator partnerships, or to turn those leads into a table/spreadsheet/doc.
---

# Brand Deal Researcher

## Overview

Turn sponsorship and paid promotion emails into an actionable lead list. Search email with a concrete date window, identify real brand/client opportunities, research each shortlisted brand, and export the result in the format the user asks for.

## Workflow

1. Establish the scope.
   - Use the user's requested range when provided.
   - If the user says "past 2 weeks" or similar, calculate exact start/end dates from the current date and state them in the output.
   - If the user just asks for recent brand deals, default to the last 14 days.
   - If Gmail or the email connector is unavailable, say that plainly and ask the user to reconnect or re-enable it before claiming any search was done.

2. Search email broadly, then narrow.
   - Search with multiple related terms, not just one phrase:
     `paid promotion`, `paid promo`, `sponsorship`, `sponsor`, `brand deal`, `paid collaboration`, `paid partnership`, `influencer campaign`, `creator campaign`, `creator partnership`, `UGC`, `affiliate`, `partnership`, `campaign`, `YouTube integration`, `TikTok`, `Instagram`, `Reels`, `Shorts`.
   - Include agency-style phrasing: `client`, `brief`, `budget`, `deliverables`, `rate`, `media kit`, `usage rights`, `whitelisting`, `timeline`.
   - Read snippets first, then open full messages or threads for any likely lead.
   - Inspect thread history and Google Group/digest style emails carefully; one email can contain multiple brand opportunities.

3. Classify and filter.
   - Include: inbound offers where a brand, agency, or creator platform is offering paid promotion, sponsorship, paid collaboration, affiliate paid work, creator campaign participation, or a likely paid review/integration.
   - Exclude: newsletters, generic product marketing, hiring/recruiting, customer support, PR-only embargoes with no paid angle, and emails asking the creator or company to pay for promotion.
   - Treat the agency sender and the represented brand/client separately. The lead is usually the client brand, with the agency noted.

4. Deduplicate.
   - Deduplicate by real brand/client, not by sender address.
   - Merge repeated follow-ups, bumps, and thread replies into one row.
   - Preserve the most useful latest email evidence: sender or agency, exact email date, and the core ask.
   - If one agency email lists multiple clients, create one row per brand/client when each client is materially distinct.

5. Research every shortlisted brand.
   - Prefer official sources: brand website, app/product pages, docs, pricing pages, press/newsroom, LinkedIn/company pages, App Store/Chrome Web Store/GitHub when relevant.
   - Use current web research for product category, credibility, creator fit, campaign relevance, and any obvious red flags.
   - Add source URLs or source names when the final format has room.
   - Do not overstate findings. Mark uncertain brands as `Unclear` or `Needs verification`.

6. Prioritize for the user.
   - High: strong creator/product fit, AI/dev/productivity/design/video/social tool, credible brand, clear budget or professional campaign brief, reasonable deliverables.
   - Medium: adjacent category, potentially useful but unclear fit, agency/client credible but offer details incomplete.
   - Low: weak fit, generic marketplace, unclear brand, low-trust outreach, vague ask, heavy rights requirements, or likely low-value affiliate-only pitch.
   - Call out urgent timing separately if the email has a deadline.

7. Note deal terms and red flags.
   - Capture deliverables: YouTube integration, dedicated video, Short/Reel/TikTok, newsletter, X/LinkedIn post, UGC, review, affiliate placement, giveaway, or event invite.
   - Capture business terms when present: budget, rate request, usage rights, paid usage window, whitelisting, exclusivity, script approval, bio link, coupon/ad code, payment timing, NDA, deadline.
   - Flag risky patterns: asks to move to WhatsApp before sharing a real brief, unclear client, vague "collab" with no compensation, broad perpetual usage rights, unusually low rates, or requests for account access.

## Output Format

Default to a concise Markdown table unless the user asks for a spreadsheet, doc, or another artifact.

Recommended table columns:

- `Priority`
- `Brand/client`
- `Product category`
- `Latest email evidence`
- `What they asked for`
- `Research / notes`
- `Suggested next step`

For spreadsheet requests:

- Use the spreadsheet tooling/runtime available in the current environment.
- Create an `.xlsx` artifact with at least `Summary` and `Brand Leads` sheets.
- Freeze the header row, enable filters, use readable column widths, and format priority/status cells for scanning.
- Include exact date range and search basis in the summary sheet.
- Final response should link directly to the spreadsheet file.

For document/DOCX requests:

- Use plain ASCII hyphen bullets (`-`) instead of Word bullet glyphs.
- Keep the document practical: table first, short notes after.

## Quality Bar

- Be explicit about what was searched: date range, Gmail/email source, and broad keyword families.
- Do not include private email text verbatim beyond short evidence snippets needed to identify the opportunity.
- Keep notes actionable: what the brand is, why it is or is not a fit, what to ask next, and any risk.
- When the user asks for "all brands," err toward recall first, then mark questionable leads as low priority instead of silently dropping them.
- If research cannot verify a brand, keep the row but mark it clearly as unverified.

## Portability Notes

- Specific to the author's current workflow: the default source is Gmail or email exports for creator sponsorship and paid promotion leads.
- Reusable: date-bounded search, paid-opportunity filtering, brand/client deduplication, official-source research, and prioritized lead-table output.
- Adapt before reuse: replace the mailbox connector, creator niche, priority criteria, deliverable types, and artifact format with the adopting user's account and business model.

## Example Requests

- "Use Gmail from the past 2 weeks and find all paid promotion offers."
- "Research these brand deal emails and put them in a table."
- "Make a spreadsheet of all sponsorship leads from my inbox this month."
- "Which brand deals should I reply to first?"
