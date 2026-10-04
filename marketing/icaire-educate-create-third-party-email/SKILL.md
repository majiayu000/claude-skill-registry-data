---
name: icaire-educate-create-third-party-email
description: Use when drafting, personalising, creating, or updating partner-ready ICAIRE Educate third_party_email campaign items that an organisation, institution, speaker, or collaborator will send to its own audience.
---

# ICAIRE Educate: Create Third-Party Email

Create a copy-ready `third_party_email` campaign item that fits the partner, its audience, and the verified purpose of the outreach.

## Contract Checklist

- Confirm the partner context and all factual claims before drafting.
- Produce partner-ready copy with no recipient variables or sending controls.
- Treat links as optional; do not require a registration link, CTA, or any
  specific destination.
- Apply the Link Contract to every link that is included.
- Create or update the item through ICAIRE Educate MCP, then read it back.
- Verify the stored fields, absence of recipient variables, and, when links are
  present, rendered clickability and trackability.
- Do not send a test or live email.

## Workflow

1. Establish the partner and outreach context:
   - Confirm or research the partner organisation name, mission, relationship
     to the audience, reason for the email, and preferred forwarding angle.
   - Treat approvals, named contacts, co-branding permissions, programme facts,
     dates, eligibility, capacity, and outcomes as confirmed only when supported
     by ICAIRE or partner context.
   - If context is missing, use `icaire-educate-find-campaign-partners` or read
     the relevant ICAIRE context before drafting.
   - Anti-patterns: inventing partner agreement, inventing contacts, assuming co-branding permission, drafting from unverified programme facts
2. Inspect the existing campaign item and destination context:
   - Read the relevant campaign and existing `third_party_email` items through
     ICAIRE Educate MCP before creating or updating anything.
   - Determine whether the email needs no link, an informational link, a
     registration link, or another verified destination based on its purpose.
   - Confirm each intended URL resolves to the expected destination before it is
     included.
   - Anti-patterns: defaulting every email to registration, requiring a CTA without a content reason, guessing a URL, overwriting an item without reading it
3. Draft copy-ready partner email content:
   - Use `icaire-educate-create-campaign-email` for shared tone, structure,
     logo/header guidance, and ICAIRE signoff.
   - Follow the shared skill's Link Contract: no registration URL, CTA URL,
     primary CTA, or other link is mandatory.
   - Personalise the opening and value proposition to the partner and its
     audience, while preserving ICAIRE ownership through the signoff or a clear
     forwarding note.
   - Do not include recipient merge fields, recipient personalisation
     variables, Resend controls, or test/live send controls.
   - Anti-patterns: mandatory registration language, recipient variables, send controls, generic copy unrelated to the partner, unsupported endorsements
4. Apply the Link Contract when links are present:
   - An email with no links is valid and must not gain a placeholder or forced
     CTA.
   - Use only confirmed `http://` or `https://` destination URLs.
   - Render every destination as a clickable Markdown link in
     `[descriptive link text](https://confirmed.example/path)` form; do not
     leave a raw URL or present a URL as non-clickable text.
   - Keep the actual intended destination in the anchor. Do not substitute a
     registration URL, require a particular URL or placeholder, or change the
     destination merely to satisfy tracking.
   - Anti-patterns: forcing any link, forcing a registration link, unconfirmed URLs, raw URLs, non-clickable link text, unsafe schemes, changing the destination for tracking
5. Create or update the MCP item:
   - Use ICAIRE Educate MCP to create or update the `third_party_email` item.
   - Set `subject`, `preview_text`, `body_markdown`, `publish_date`,
     `sequence_order`, and `status` using the verified campaign context.
   - Make only the requested item change and preserve unrelated campaign data.
   - Anti-patterns: sending the email, using a send endpoint, broad campaign edits, silently changing sequence or status
6. Read back and verify the saved result:
   - Read the created or updated item through ICAIRE Educate MCP and compare the
     stored fields with the intended draft.
   - Confirm the stored body has no recipient variables or sending controls.
   - If the email has no links, verify that no link was inserted and do not run
     a link requirement check.
   - If the email has links, inspect the rendered preview or a non-sending
     render/preflight result. Verify each Markdown link becomes a clickable HTML
     anchor eligible for the eventual sending provider's click tracking while
     preserving the intended destination.
   - For partner-forwarded copy, report click tracking as eligible rather than
     active unless the partner's actual sending provider and tracking setting
     have been verified.
   - Stop and report the failed link if any included URL is malformed,
     unrendered, non-clickable, untrackable, or resolves to the wrong
     destination; do not send or claim completion.
   - Anti-patterns: trusting source Markdown alone, treating no-link email as an error, claiming tracking without rendered verification, sending to test verification, skipping MCP read-back

## Link Contract

Links are optional. When a link is useful to the email's verified purpose, it
must satisfy all of these conditions:

- the destination is a confirmed HTTP(S) URL
- the body uses descriptive clickable Markdown link syntax
- the rendered output contains a clickable anchor
- the rendered anchor is eligible for the sending provider's click tracking
- tracking preserves the intended destination

This contract never requires a registration link, a specific URL, a particular
placeholder, or any link at all. For partner-forwarded copy, do not claim that
tracking is active until the partner's sending provider and settings are known.

## Anti-Patterns

- Requiring every email to contain a link.
- Requiring a registration link or any other specific destination.
- Treating an email without links as invalid.
- Inserting a placeholder CTA or guessed URL.
- Claiming a link is clickable or trackable without checking rendered output.
- Adding recipient variables to partner-forwarded copy.
- Claiming the partner has agreed to send without verification.
- Sending a test or live email.

## Output

Return:

- `Partner`
- `Forwarding Angle`
- `Subject`
- `Preview Text`
- `Body Markdown`
- `Links`: `None` or each confirmed destination and its rendered
  clickability/trackability result
- `MCP Item`
- `Verification`: MCP read-back, recipient-variable check, and link rendering
  check when applicable
- `Not Sent`
