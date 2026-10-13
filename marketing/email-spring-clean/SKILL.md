---
name: email-spring-clean
description: Use when you want to declutter your inbox. Scans for top noise-generating senders, shows you the list, and on your confirmation — archives and filters them.
version: 1.0.0
author: Pete Swain / Hermes Agent
output_mode: execute
destination: direct action (inbox management)
---

## Overview

A cluttered inbox is low-grade cognitive noise that runs all day. This skill scans your inbox for the top senders generating the most irrelevant, unread, or unwanted email — then surfaces a clear list with a recommendation for each. On your confirmation, it archives all email from those senders and sets up filters to keep them out of your primary inbox going forward. One execution, a noticeably cleaner inbox.

## When to Use

- You say "clean my inbox"
- You say "email spring clean"
- You say "declutter my email"
- Your inbox has become unmanageable and you don't know where to start
- Your notification volume is interfering with important email
- You want to reclaim inbox as a signal-rich space, not a landfill

## How It Works

1. **Access the inbox.** Connect to the user's email account via Hermes Gmail or Outlook integration. Scan all emails in the inbox (including primary, promotions, and social tabs if applicable).

2. **Identify the top noise generators.** Analyse the inbox to find the 5 senders generating the most clutter. Score each sender based on:
   - Total email volume from this sender in the last 90 days
   - Open rate — what percentage of their emails were opened?
   - Recency of last meaningful interaction — did the user ever reply to this sender?
   - Content type — newsletter, marketing, automated notification, or real person?

   Prioritise senders who: send frequently, have near-zero opens, and have never received a reply. These are the highest-impact targets.

3. **Build the review list.** For each of the 5 senders, display:
   - **Sender name and email address**
   - **Email count** — total emails in the last 90 days
   - **Last email subject** — to remind the user what this sender sends
   - **Open rate** — a rough estimate (e.g., "rarely opened", "never opened", "occasionally opened")
   - **Recommendation** — one of three actions:
     - 🗑 **Archive all + unsubscribe**: They're sending marketing/newsletters you're not reading. Archive everything and unsubscribe.
     - 📁 **Archive all + filter to skip inbox**: They may send something useful occasionally, but it shouldn't hit primary. Archive past emails, create a filter for future ones.
     - ⚠️ **Review manually**: The sender type is ambiguous (e.g., a real person who sends too often, or a notification service that sometimes contains important info). Flag for the user to decide.

4. **Present the list in chat.** Show the full table and wait for confirmation. Do NOT take any action yet. End with:

   *"Here are your top 5 inbox noise generators. For each one I've made a recommendation. Say 'execute all' to apply all recommendations, or tell me which senders to action and which to skip."*

5. **Execute on confirmation.** For each approved action:
   - **Archive all**: Move all existing emails from this sender to archive (out of inbox, not deleted)
   - **Unsubscribe**: Click the unsubscribe link in the most recent email from this sender, or mark as spam/unsubscribe via Gmail/Outlook tools
   - **Create filter**: Set up a filter so future emails from this sender automatically skip the inbox (and optionally get labelled or archived)

6. **Confirm results.** Report back in chat:
   - How many emails were archived per sender
   - Which unsubscribes were executed
   - Which filters were created
   - Total emails moved out of inbox

## What the Agent Needs From You

- **Connected email account** — Gmail or Outlook via Hermes integrations
- **Your approval** — the agent will show the list before taking any action

> ⚠️ **CONFIRM BEFORE ACTING:** This skill will NOT archive, unsubscribe, or filter anything until you explicitly approve. Review the list carefully — especially the "Review manually" flagged senders.

## Output

In chat first:
- A list of 5 top noise-generating senders with volume data and recommendations

On confirmation:
- Archives executed (emails moved out of inbox)
- Unsubscribes executed where recommended
- Filters created for future emails
- Confirmation summary in chat: X emails archived, X unsubscribes, X filters created
