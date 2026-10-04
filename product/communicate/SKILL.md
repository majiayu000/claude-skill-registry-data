---
name: communicate
description: Draft a professional communication (Slack, email, or async doc) with context from the vault
argument-hint: "[what to communicate + to whom + channel]"
---

# Draft a Communication

You help draft a professional communication based on context from the vault. Channel-flexible: Slack, email, or an async update (doc comment, status page, ticket).

## Input

The user provides via `$ARGUMENTS`:
- **What to communicate**: the topic or message content
- **To whom**: the recipient or audience
- **Channel** (optional): "Slack", "email", "doc", "async update". If not specified, ask once.

Example: "update engineering on API scope change - Slack, #eng-platform".

## Workflow

1. **Read relevant context**:
   - Recent meetings in `Meetings/` on this topic
   - Recent decisions in `Loose Notes/Work/` related to the topic
   - `Dashboard/Weekly P-Tasks.md` for current priorities
   - Any other relevant notes found via search

2. **Check recipient preferences**:
   - Read `Dashboard/people-profiles.md` for recipient's communication style (if listed).
   - Note preferred channel, tone, level of detail.

3. **Determine audience and tone**:
   - **Engineering**: technical, specific, actionable. Include links to specs, APIs, issues. Avoid high-level marketing language.
   - **Design**: user-focused, visual references. Include user stories and customer context. Avoid deep technical detail.
   - **Leadership**: strategic, metrics-driven, concise. Include business impact, metrics, goal alignment. Avoid implementation detail.
   - **Customers**: professional, benefits-focused. Include business value and clear ROI. Avoid internal jargon and unfinished features.

4. **Draft the message**:
   - Start with context (why this, now)
   - Present 2-3 key points clearly
   - End with clear next steps or call to action
   - Format for the chosen channel:
     - **Slack**: Slack markdown (`*bold*` single asterisk, `-` bullets, `:emoji_name:`)
     - **Email**: subject line + professional email body
     - **Async doc / comment**: plain Markdown, no emoji-heavy formatting, lead with the conclusion (inverted pyramid)

5. **Include relevant links**:
   - Meeting notes (for prior discussions)
   - GitHub issues (if accessible to the recipient)
   - Any external links that support the message

## Output Format

**Slack:**
```
📧 Slack message for [Recipient / Channel]:

[Message ready to copy-paste with Slack markdown]
```

**Email:**
```
📧 Email draft for [Recipient]:

**Subject**: [Clear, concise subject line]

[Email body ready to copy-paste]
```

**Async doc / comment:**
```
📝 Async update for [Doc / Ticket / Channel]:

[Body - lead with conclusion, then context, then next steps]
```

## Example: Engineering Slack update

User: "update engineering on API scope change - Slack, #eng-platform"

Draft:
```
📧 Slack message for #eng-platform:

*API scope update for next release*

We're adjusting scope based on customer validation feedback:

*In scope* ✅:
- Business key search endpoint (epic: [link])
- Agent status visibility in dashboard
- Retry semantics clarification

*Out of scope* ⭕:
- Full execution timeline (moved to next cycle)

*Why*: Customer validation showed business key search is a migration blocker for 3 accounts. Timeline visualization requires UX work that doesn't fit this cycle.

*Next steps*:
- Epic sizing this week (engineering lead)
- Design review Thursday
- Updated roadmap in tracker: [link]

Questions? Thread below or ping me directly.
```

## Example: Leadership email

User: "draft leadership update on Q1 progress - email"

Draft:
```
📧 Email draft for leadership:

**Subject**: Q1 Platform Progress - Key Milestone Update

Hi team,

Quick update on Q1 progress:

*Progress*:
- 3 of 5 epics scoped and prioritized
- Customer validation sessions completed
- Top priority adjusted based on customer feedback

*Metrics*:
- On track for target release
- 2 epics in active development

*Risks*:
- Engineering capacity tight on one initiative
- Mitigation: deprioritized lower-impact work to next cycle

*Next milestone*: Design review [date], eng handoff [date].

Full details: [link]
```

## Notes

- Match the tone to the audience - don't send engineering-style updates to leadership.
- Keep Slack messages under 200 words (people skim).
- Email subject lines should be clear and actionable.
- Reference `Dashboard/people-profiles.md` for recipient-specific preferences.
- Slack markdown formatting: `*bold*` (single asterisk), `-` bullets, `:emoji_name:` format.
