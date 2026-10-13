---
name: inbox-opportunity-scout
description: Use when you want to find hidden sales opportunities in your inbox. Scans the last 30 days for buying signals, surfaces a shortlist of 5 opportunities, and pushes a summary to Slack.
version: 1.0.0
author: Pete Swain / Hermes Agent
output_mode: execute
destination: Slack notification
---

⚠️ OUTPUT NOTE: The goal of this skill is NOT to display results in chat.
The outcome is pushing output to a meaningful destination — Slack, Google Doc,
email draft, Notion, or web. If you're reading this in chat, the skill hasn't
finished its job.

## Overview

Revenue is often hiding in plain sight — in emails you've already received and haven't followed up on. Referrals you haven't acted on, pricing requests that went quiet, problems mentioned in passing that your offer solves. This skill scans your inbox for the last 30 days of emails, identifies buying signals and warm opportunities, and surfaces a shortlist of 5 with a proposed next action for each — pushed directly to Slack so it's actionable the moment it arrives.

## When to Use

- You say "scan my inbox for opportunities"
- You say "what opportunities am I missing"
- You haven't done a formal pipeline review in a while
- You're starting a new week and want to know where to focus
- You want a quick revenue audit without a full CRM review

## How It Works

1. **Access the inbox.** Connect to the user's email account (via Hermes Gmail or Outlook integration). Scan emails received in the last 30 days. Focus on: emails from real people (filter out automated newsletters, receipts, and platform notifications).

2. **Identify buying signals.** Scan for emails that contain any of the following patterns:

   **Explicit signals:**
   - Requests for pricing, rates, or availability
   - Questions about how your offer works or what's included
   - "Are you taking on new clients?" or similar
   - A referral introducing you to a potential client

   **Implicit signals:**
   - Someone describing a problem your offer solves — even if they didn't frame it as a request
   - A past client reaching out again (even socially) — indicates they're re-entering the market
   - Someone asking for a recommendation and your offer is the recommendation
   - A conversation that ended positively but was never followed up on
   - An unanswered email where you were the one who dropped the ball

   **Timing signals:**
   - Emails where a "follow up in X weeks" was mentioned and that time has now passed
   - People who said "not right now" 4–8 weeks ago — the "not right now" window may have closed

3. **Surface 5 opportunities.** Select the 5 highest-potential opportunities. For each, show:
   - **Name and context** — who they are and the nature of your relationship
   - **Email subject and date** — the specific email (or thread) that contains the signal
   - **The signal** — what was said or implied that indicates potential
   - **Opportunity type** — new client, referral, reactivation, upsell, or follow-up
   - **Proposed next action** — the exact message to send or action to take

4. **Draft a proposed next action for each.** The next action should be specific:
   - If it's a follow-up: draft the subject line and a 3-sentence reply
   - If it's a referral: suggest a warm intro email to send
   - If it's a pricing request that went quiet: draft a simple "still interested?" message
   - If it's someone with a problem: draft an offer to help without pitching directly

5. **Push to Slack.** Format the shortlist as a clean Slack message:
   - Title: `📬 Inbox Opportunity Scan — [Date]`
   - Each opportunity as a numbered section with name, opportunity type, and proposed next action
   - Emojis used sparingly to distinguish opportunity types (e.g., 🔁 reactivation, 🤝 referral, 💬 follow-up)
   - End with: `Reply here or in chat to send any of these responses.`

6. **Confirm push.** After pushing to Slack, confirm in chat: *"Your opportunity scan is live in Slack. 5 opportunities found. Let me know which you want to act on."*

## What the Agent Needs From You

- **Connected email account** — Gmail or Outlook via Hermes integrations
- **Connected Slack workspace** — for the push notification
- **Your offer context** (optional but helpful) — a brief description of what you sell so the agent can better calibrate what counts as a buying signal in your world

## Output

- A Slack message with 5 opportunity summaries
- Each entry: name, email reference, signal type, opportunity category, and proposed next action
- Confirmation in chat when the Slack message is sent
