---
name: "Skill: Gmail Auto-Reply for Client"
description: This skill enables the agent to automatically answer Gmail messages
  on behalf of a client. The agent drafts and (when the user approves or when
  configured) sends replies using the client’s tone, si...
---

# Skill: Gmail Auto-Reply for Client

## Purpose

This skill enables the agent to **automatically answer Gmail messages on behalf of a client**. The agent drafts and (when the user approves or when configured) sends replies using the client’s tone, sign-off, and optional templates.

## When to Use

- The user asks to “reply to my emails,” “answer my Gmail,” or “draft responses to incoming mail.”
- The user provides a Gmail context (e.g. “inbox for client@example.com”) and wants automated or semi-automated replies.
- The user wants the agent to act as the client when responding to specific threads or senders.

## Prerequisites (User/Client Must Provide)

- **Gmail access**: OAuth2 or app password for the client’s Gmail (never store raw passwords in the skill; use environment variables or secure config).
- **Client profile** (optional but recommended): short brief (tone, sign-off, topics they handle, topics to defer).

## Instructions

1. **Gather context**
   - Ask for or read the client’s brief: tone (formal/casual), sign-off (e.g. “Best,” “Thanks,”), and any “do not answer” or “always escalate” rules.
   - If the user provides an email thread or summary, use that as the incoming message to answer.

2. **Draft the reply**
   - Write a concise, professional reply that:
     - Addresses the sender and the main question or request.
     - Matches the client’s tone and sign-off.
     - Does not promise anything outside the client’s scope (e.g. legal/financial) unless the user explicitly approves.
   - Prefer short paragraphs and clear next steps (e.g. “I’ll get back to you by Friday”).

3. **Use templates when provided**
   - If the client has added templates (see `templates/reply_templates.json` or user-defined templates), pick the closest match by intent (e.g. “acknowledgment,” “meeting request,” “out of office”) and personalize placeholders like `{{sender_name}}`, `{{topic}}`, `{{deadline}}`.

4. **Safety and approval**
   - By default, **output the draft** for the user/client to approve before sending.
   - Only auto-send if the user has clearly configured “auto-send” and you have applied the client’s rules and filters (e.g. only for certain labels or senders).

5. **Integrations**
   - If the user has configured Gmail API (OAuth2) or IMAP/SMTP, use the credentials from environment or secure config—never from this skill’s files.
   - When “sending,” either return the draft text for the user to paste/send, or call the configured send function if the user has set one up.

## Files in This Package

- `SKILL.md` – This file (skill instructions).
- `manifest.json` – Package metadata.
- `templates/reply_templates.json` – Optional starter templates (acknowledgment, meeting, short reply).
- `scripts/README.md` – Short note on how the client can add their own scripts or rules.

## Example Interaction

**User:** “Reply to this email as my client. Sender: Jane. She’s asking for a meeting next week. Client prefers a short, friendly reply and uses ‘Best’ as sign-off.”

**Agent:** Uses this skill to draft a short, friendly reply addressing Jane, suggesting a time or asking for availability, and signing “Best,” then returns the draft for the user to approve or send.
