---
name: mcp-media-inbox-triage
description: Find media, partnership, and high-intent requests buried in a shared Gmail inbox, summarize the useful ones, and route them to the right owner through Zapier MCP.
---

# MCP Media Inbox Triage

Use this skill when a marketing, PR, community, or partnerships team needs a lightweight triage layer for a shared Gmail inbox.

## What This Skill Does

1. Searches a configured Gmail inbox or label in a bounded window.
2. Reads only the message context needed for classification.
3. Classifies each message as media request, partnership inquiry, customer/community lead, urgent executive risk, vendor pitch, spam/no action, or unclear.
4. Scores urgency and recommends the right owner.
5. Routes relevant requests to Slack, Google Sheets, or a triage doc.
6. Drafts suggested replies only for human review.

## When You Need This Pattern

- A shared inbox mixes press requests, creator pitches, partnership notes, customer signals, newsletters, and vendor spam.
- One person spends time each week skimming every email just to find the real asks.
- The team needs human review before any reply is sent.
- The team already works in Gmail, Slack, and Google Sheets.
- You want a practical Zapier MCP workflow that saves attention, not just time.

## Architecture

```text
Shared Gmail inbox
  -> Zapier MCP Gmail search and read
  -> AI classification
  -> Slack summary, Google Sheets triage log, or Gmail draft
```

## Required Connections Through Zapier MCP

- Gmail: search and read messages from the shared inbox.
- Slack: post triage summaries or urgent alerts.
- Google Sheets: append a persistent triage log.
- LLM: classify and summarize.

Optional:

- Google Docs: create a weekly media-request digest.
- Google Calendar: check deadline windows or schedule follow-ups.
- CRM or advocacy database: match senders to known customers, partners, or advocates.

## Core Workflow

### 1. Define The Inbox Window

Start with a bounded search:

```text
to:{SHARED_INBOX} newer_than:7d -label:triaged
```

Adjust the inbox address, label, and time window for your team.

### 2. Pull Minimal Email Context

For each candidate message, read only:

| Field | Why |
| --- | --- |
| Sender name and email | Identify source and possible owner |
| Subject | Fast classification signal |
| Date received | Urgency and SLA |
| Plain-text body | Extract the ask |
| Thread count | Spot follow-ups and repeated requests |
| Gmail thread link | Source of truth |

Do not dump full email bodies into Slack.

### 3. Classify The Request

| Category | Signal | Default action |
| --- | --- | --- |
| Media request | Journalist, publication, interview, quote, deadline | Route to PR or comms |
| Partnership inquiry | Co-marketing, integration, affiliate, event, sponsorship | Route to partnerships or marketing |
| Customer/community lead | Customer story, testimonial, community invite, user feedback | Route to advocacy or community |
| Urgent executive risk | Legal threat, brand risk, sensitive complaint, public escalation | Alert owner immediately |
| Vendor pitch | Agency, list purchase, ad buy, unrelated service offer | Log or ignore |
| Spam/no action | Generic blast, irrelevant outreach, phishing indicators | Archive or leave unassigned |
| Unclear | Not enough context to decide | Send to human review |

### 4. Score Urgency

| Urgency | Signals | Response target |
| --- | --- | --- |
| High | Deadline within 48 hours, named journalist, public brand risk, customer escalation | Same day |
| Medium | Specific ask, relevant sender, no immediate deadline | Two business days |
| Low | Useful but exploratory, vague timing, non-critical | Weekly batch |
| Ignore | Spam, irrelevant vendor pitch, duplicate | No response |

### 5. Output The Summary

```text
Media inbox triage: 14 messages scanned, 4 need action

High urgency
- Jane Lee, TechWeekly: asks for comment on AI workflow story by Friday.
  Owner: PR
  Suggested action: reply with availability and approved spokesperson.
  Source: Gmail thread link

Ignored
- 8 vendor pitches
- 2 unrelated newsletters
```

## Google Sheets Log

| Column | Purpose |
| --- | --- |
| received_at | Message timestamp |
| sender_name | Human-readable sender |
| sender_email_domain | Domain only if privacy matters |
| subject | Email subject |
| category | Classification |
| urgency | High / Medium / Low / Ignore |
| summary | One-sentence ask |
| suggested_owner | Team or person |
| suggested_next_action | Concrete next step |
| gmail_thread_link | Source link |
| status | New / Routed / Done / Ignored |

## Classification Prompt

```text
You are triaging a shared media inbox.

Classify this email for a human team. Do not draft a reply unless the email needs action.

Return JSON:
{
  "category": "media_request|partnership_inquiry|customer_community_lead|urgent_executive_risk|vendor_pitch|spam_no_action|unclear",
  "urgency": "high|medium|low|ignore",
  "sender_name": "string or unknown",
  "sender_org": "string or unknown",
  "deadline": "string or null",
  "summary": "One sentence describing the actual ask",
  "why_it_matters": "One sentence explaining relevance",
  "suggested_owner": "PR|Community|Marketing|Partnerships|Support|Leadership|Human review|Ignore",
  "suggested_next_action": "Concrete next action",
  "draft_reply_needed": true,
  "confidence": "high|medium|low"
}

Rules:
- Do not expose private email content in team channels.
- If the message is vague, classify as unclear.
- If the message is a generic vendor pitch, classify as vendor_pitch or spam_no_action.
- If the message mentions legal risk, public complaint, a journalist deadline, or a customer escalation, mark high urgency.
```

## Zapier MCP And SDK Role

- Use Zapier MCP to search Gmail, read message context, post Slack summaries, append Google Sheets rows, and create Gmail drafts when approved.
- Use Zapier SDK for recurring runs, owner routing, retry handling, status logging, follow-up reminders, and weekly reporting when the workflow becomes productionized.

## Guardrails

- Never auto-send replies.
- Do not expose full private email threads in Slack.
- Keep Gmail thread links as the source of truth.
- Route uncertain messages to a human.
- Treat generic vendor pitches as vendor_pitch or spam_no_action unless there is a specific relevant ask.
- Keep ignored messages auditable during tuning.

## Inspired By

Generalized from Matt Canning and NoPlex. The reference workflow uses Zapier MCP and Gmail to reduce media inbox review from about 4 hours per week to about 15 minutes.
