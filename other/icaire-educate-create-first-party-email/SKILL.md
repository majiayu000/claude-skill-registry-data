---
name: icaire-educate-create-first-party-email
description: Use when drafting, creating, updating, or scheduling ICAIRE-owned ICAIRE Educate campaign emails as MCP-backed sendable_email items without sending them.
---

# ICAIRE Educate: Create First-Party Email

Create or update an ICAIRE-owned `sendable_email` through the ICAIRE Educate MCP and verify the saved item without sending it.

## Contract Checklist

- Confirm the email purpose, audience, sender, timing, claims, and practical facts from authoritative sources.
- Read the campaign and existing email item through the ICAIRE Educate MCP before drafting or writing.
- Treat links as optional: an email with no link is valid.
- If a link is included, use a confirmed absolute HTTP(S) destination, render it as a clickable Markdown link, and verify that the rendered link is eligible for click tracking.
- Never require a registration link, registration placeholder, or any other specific destination.
- Use only variables supported by the current Educate send path and approved by the user.
- Create or update only when the user asked for a write; otherwise return a draft.
- Read the saved item back through the MCP and verify all requested fields.
- Never send a test or live email unless the user explicitly asks in a separate send action.

## Workflow

1. Establish the email brief:
   - Confirm the campaign, email purpose, audience, sender relationship, timing, and desired action, if any.
   - Verify dates, times, locations, eligibility, capacity, deadlines, certificate claims, and destination URLs from authoritative sources.
   - Decide whether the email needs a link. No-link informational emails are valid.
   - Use the relevant guidance under `Email Types` when the item is part of a reminder sequence.
   - Anti-patterns: assuming every email is a registration email, inventing campaign facts, forcing a CTA, forcing a link
2. Read before writing:
   - Read the campaign map and current campaign facts through the ICAIRE Educate MCP.
   - Search or list existing `sendable_email` items for the campaign, then read the exact item before updating it.
   - If an expected MCP tool is not visible, use `find-missing-tools` before concluding that the MCP is unavailable.
   - Stop and report the conflict if the requested write would overwrite unclear or mismatched content.
   - Anti-patterns: writing from stale context, skipping duplicate checks, using SQL migrations instead of the MCP, overwriting an ambiguous item
3. Draft the email:
   - Use `icaire-educate-create-campaign-email` for shared structure, tone, logo/header guidance, and signoff.
   - Follow the shared skill's link contract: neither a link nor a CTA is mandatory, and any included destination must serve the email's actual purpose.
   - Set a clear `name`, `subject`, `preview_text`, `body_markdown`, `publish_date` or send date, `sequence_order`, `status`, and relevant recipient `filters`.
   - Match urgency to the date without pressure tactics.
   - Use personalisation variables only when the current Educate send path supports them and the user has approved them.
   - Anti-patterns: copying registration language into unrelated emails, unsupported variables, hype, pressure tactics, vague or unverified claims
4. Make every included link clickable and trackable:
   - Use only a confirmed absolute `http://` or `https://` URL as the destination.
   - Render each destination as a Markdown link such as `[descriptive link text](https://example.org/path)` so the email renderer produces an HTML anchor.
   - Confirm the Markdown is syntactically valid, with no space between `]` and `(`, and do not rely on a bare URL becoming clickable automatically.
   - Use the platform's supported non-sending render or preview path to verify that each included link becomes an `<a href="...">` element and is recognised as eligible for click tracking.
   - Click tracking is a property of any valid rendered link; it must not depend on a registration URL, a registration placeholder, or a particular destination.
   - If rendering or tracking verification is unavailable, state that limitation and do not claim the link is confirmed trackable.
   - Anti-patterns: requiring a specific URL, requiring any URL, using unconfirmed destinations, bare URLs, malformed Markdown, unsafe schemes, claiming tracking from source text alone
5. Create or update the MCP item:
   - Proceed only when the user's request authorises creating or updating the item.
   - Make the narrowest MCP write that preserves unrelated fields and audience filters.
   - Report any intentional change to recipient filters.
   - Do not invoke a test-send, live-send, queue, or delivery action as part of creation or update.
   - Anti-patterns: treating draft approval as send approval, silently changing filters, replacing unrelated fields, sending during item creation
6. Read back and verify:
   - Read the exact saved item through the ICAIRE Educate MCP.
   - Compare `name`, `subject`, `preview_text`, `body_markdown`, dates, order, status, and filters with the intended values.
   - Re-check every included link through the supported rendered preview or validation output for a clickable anchor and click-tracking eligibility; accept an email with no links without link validation.
   - Report the MCP item identifier and distinguish confirmed facts from anything that could not be verified.
   - Stop before sending unless the user has explicitly requested a separate send action.
   - Anti-patterns: declaring success without read-back, treating saved Markdown as rendered proof, failing a no-link email, implying that the email was sent

## Email Types

Default sequence:

- Announcement: explain why the programme matters and what the reader needs to know or do.
- One week reminder: focus on planning and practical details.
- Three day reminder: focus on the final preparation window.
- Same day reminder: focus on logistics, joining details, and any immediate action.

These are defaults, not a requirement that every campaign use every type or contain a registration CTA.

## Anti-Patterns

- Requiring a link, registration URL, registration placeholder, or specific destination in every email.
- Treating raw Markdown, a bare URL, or source text alone as proof that a link is clickable and trackable.
- Sending a test or live email while creating, updating, or verifying the item.
- Writing before reading the current MCP-backed item.
- Using SQL migrations as the default content-management path.
- Inventing facts, approvals, partners, endorsements, deadlines, capacity, or eligibility.
- Adding unsupported personalisation variables or silently changing recipient filters.

## Output

Return:

- `Email Type / Purpose`
- `Subject`
- `Preview Text`
- `Body Markdown`
- `Links`: `None`, or each confirmed destination with clickable-render and click-tracking verification status
- `MCP Item`: action taken and item identifier, or `Draft only`
- `Read-Back Verification`: fields confirmed from the saved item
- `Send Status`: explicitly `Not sent` unless the user separately requested and authorised sending
- `Limitations`: any facts, rendering, tracking, or MCP state that could not be verified
