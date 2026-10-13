---
name: sales-call-prep
description: Use when you're preparing for an upcoming sales or discovery call. Researches the prospect, generates tailored discovery questions, anticipates objections, and pushes a prep brief to Notion or Google Doc.
version: 1.0.0
author: Pete Swain / Hermes Agent
output_mode: push
destination: Notion / Google Doc
---

⚠️ OUTPUT NOTE: The goal of this skill is NOT to display results in chat.
The outcome is pushing output to a meaningful destination — Slack, Google Doc,
email draft, Notion, or web. If you're reading this in chat, the skill hasn't
finished its job.

## Overview

Walking into a sales call without preparation is leaving money on the table. The best closers aren't necessarily the best talkers — they're the best listeners, and great listening starts with great research. This skill researches your prospect before the call, surfaces their context and likely pain points, and generates a tailored prep brief: discovery questions, objections to prepare for, and an opening insight that shows you've done your homework. The brief is pushed to Notion or Google Doc so it's ready on any device.

## When to Use

- You say "prep for a sales call"
- You say "sales call prep"
- You say "research this prospect"
- A call is on your calendar within the next 48 hours
- You're going into a high-stakes conversation and want to be fully prepared
- You're onboarding a new salesperson and want a repeatable pre-call process

## How It Works

1. **Gather prospect details.** Ask the user for:
   - Prospect's name and title
   - Company name and website
   - What do you already know about them? (How they found you, what they expressed interest in, any prior contact)
   - What is the offer or solution you're presenting on this call?
   - What is the call format? (Discovery call, demo, proposal presentation, follow-up)

2. **Research the prospect.** Using the provided information, research:
   - **Company overview** — size, industry, business model, approximate revenue or headcount if available
   - **Recent news** — announcements, hires, funding rounds, product launches, or press coverage in the last 90 days
   - **Likely pain points** — based on their sector, size, and stage, what challenges are companies like theirs typically navigating?
   - **LinkedIn signals** — the prospect's recent posts, job history, and any public content that reveals their priorities or frustrations
   - **Competitive landscape** — who else are they likely talking to? What alternatives exist in the market?

3. **Generate 5 tailored discovery questions.** These are not generic "tell me about your business" questions. They should:
   - Reference specific signals from the research (e.g., "I noticed you recently expanded into X — how has that changed your approach to Y?")
   - Open up conversation about pain, urgency, and priority — not just situation
   - Include at least one question about what "success" looks like and how they'd measure it
   - Include one question designed to surface the real decision-making process (budget holder, timeline, competing priorities)
   - Be conversational and curious in tone — not interrogative

4. **Prepare for 3 likely objections.** Based on the offer and the prospect profile, identify the 3 most probable objections. For each:
   - State the objection clearly
   - Suggest an acknowledgement + reframe response (not a counter-argument — a repositioning)
   - Flag any specific language to avoid

5. **Write "The One Big Insight."** This is a single, sharp observation you can open the call with — something that shows you've thought about their world specifically, not just generic research. It could be: a trend in their sector that your offer addresses, something you noticed in their recent content or news, or a pattern you see in similar companies. This insight should make them lean in, not just nod politely.

6. **Push the prep brief.** Create a document titled: `Sales Call Prep — [Prospect Name] — [Date]`. Sections: Prospect Research Summary, 5 Discovery Questions, 3 Objection Responses, The One Big Insight, Call Notes space (blank section for live notes).

7. **Confirm delivery.** Share the document link in chat.

## What the Agent Needs From You

- **Prospect name and title**
- **Company name and website**
- **What you already know** — prior contact, stated interests, how they found you
- **Your offer** — what are you presenting or selling?
- **Call format** — discovery, demo, proposal, or follow-up?
- **Destination** — Notion or Google Doc?

## Output

- Prospect research summary (company, recent news, pain points, LinkedIn signals)
- 5 tailored discovery questions
- 3 anticipated objections with prepared responses
- "The One Big Insight" to open with
- Blank call notes section
- Pushed to Notion or Google Doc with link shared in chat
