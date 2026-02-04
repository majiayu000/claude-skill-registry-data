---
name: Email Communication
description: Send and read emails via Gmail (User) and Transactional Dispatcher (System).
---

# Email Skill

## Capabilities
- **Read**: List and read emails from the user's connected Gmail account.
- **Send (User)**: Send emails *as* the user (via Gmail API).
- **Send (System)**: Send marketing/transactional emails *on behalf of* the brand (via Mailjet/SendGrid).

## Usage
- Use `gmail.list` and `gmail.read` for context gathering ("What did John say about the invoice?").
- Use `gmail.send` when the user wants to reply directly or send a personal note.
- Use `marketing.sendEmail` for newsletters, notifications, or formal system comms.

## Privacy
- Never summarize unrelated sensitive emails.
- Only read emails relevant to the user's query.
