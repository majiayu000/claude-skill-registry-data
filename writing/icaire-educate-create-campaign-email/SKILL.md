---
name: icaire-educate-create-campaign-email
description: Create shared ICAIRE Educate campaign email structure, copy, optional trackable links, logo guidance, and signoff. Use when writing or reviewing any ICAIRE Educate campaign email body, announcement, reminder, partner forwarding email, or email template.
---

# ICAIRE Educate: Create Campaign Email

Create clear first-party or third-party ICAIRE Educate campaign email copy that is safe to render in the outreach system.

## Contract Checklist

- Confirm the programme, cohort, workshop, event, or update and the audience's relationship to it.
- Verify dates, times, format, language, capacity, eligibility, deadlines, certificate claims, and destinations before including them.
- Include the ICAIRE logo/header when the sending or forwarding format supports it and include an ICAIRE signoff in every final body.
- A link or CTA is optional; never add one merely to satisfy tracking or validation.
- If a link is useful, use one confirmed HTTP(S) destination and render it as descriptive Markdown, for example `[Read the programme update](https://example.org/update)`.
- Treat a correctly rendered HTTP(S) anchor as click-trackable by the email provider; do not require a registration URL, tracking parameter, or specific destination.
- For a first-party `sendable_email`, use `[descriptive CTA]({{registration_link}})` only when the registration destination is genuinely intended and the caller confirms that supported placeholder.
- Preview the rendered email and verify that every intended link is clickable, points to the confirmed destination, is eligible for click tracking, and is not left as raw Markdown or an unresolved placeholder.
- Return complete email fields and clearly label any assumptions; never send the email unless separately and explicitly requested.

## Workflow

1. Gather the email facts:
   - confirm the audience, sender relationship, purpose, practical details, and whether the item is first-party `sendable_email` or partner `third_party_email`
   - ask for or verify a destination only when the message genuinely needs a link
   - distinguish verified facts from assumptions and omit unsupported claims
   - Anti-patterns: assuming every email is for registration, requiring a URL before drafting, inventing deadlines or approvals
2. Draft the message:
   - use a short opening, a concise reader benefit, scannable practical details when relevant, and an ICAIRE signoff
   - include one primary CTA only when the desired reader action needs one; otherwise write a complete link-free email
   - keep the tone institutional, direct, useful, and free of pressure tactics or engagement bait
   - avoid personalisation variables unless the caller confirms that the first-party Educate send path supports them; never use recipient variables in third-party partner emails
   - Anti-patterns: adding a ceremonial CTA, using vague hype, adding multiple competing actions, inserting unsupported merge fields
3. Make each included link clickable and trackable:
   - use descriptive Markdown link syntax with a valid confirmed `http://` or `https://` destination
   - use the optional `{{registration_link}}` destination only for a real first-party registration CTA that supports it
   - never manually add `outreach_send_id`, recipient data, or invented tracking parameters; platform and provider tracking are applied at render or delivery time
   - do not use raw HTML, `javascript:`, `mailto:`, malformed Markdown, URL shorteners, or a pasted destination that has not been confirmed
   - Anti-patterns: requiring a registration link, showing a URL without making it clickable, confusing a specific tracking URL with general click tracking
4. Review the rendered result:
   - preview the final rendered body rather than validating source Markdown alone
   - allow zero links; if links exist, confirm every anchor is clickable, HTTP(S), safe, correctly labelled, and points to the intended destination
   - confirm no Markdown link syntax or template placeholder remains unresolved
   - verify the logo/header guidance, signoff, subject, preview text, and factual claims
   - Anti-patterns: rejecting a link-free email, checking only that a URL string exists, approving raw Markdown as rendered output
5. Return the finished draft:
   - provide `Subject`, `Preview Text`, `Body Markdown`, optional `Link(s)`, `Logo / Signoff Note`, and `Assumptions`
   - state explicitly when the email intentionally contains no links
   - Anti-patterns: returning an unlabeled draft, hiding assumptions, claiming the email was sent

## Anti-Patterns

- Requiring every email to contain a link, CTA, registration URL, or `{{registration_link}}` placeholder.
- Adding a link solely so the message passes validation.
- Treating a pasted or raw Markdown URL as proof that the rendered email is clickable.
- Manually embedding recipient identifiers or send-tracking parameters.
- Inventing approvals, partners, attendee numbers, endorsements, discounts, eligibility, or deadlines.
- Sending test or live email without explicit authorization.

## Output

Return:

- `Subject`
- `Preview Text`
- `Body Markdown`
- `Link(s)`: each label and confirmed destination, or `None — intentionally link-free`
- `Logo / Signoff Note`
- `Assumptions`
- `Rendered Link Verification`: link count and confirmation that each included link is clickable, HTTP(S), safe, and click-trackable
