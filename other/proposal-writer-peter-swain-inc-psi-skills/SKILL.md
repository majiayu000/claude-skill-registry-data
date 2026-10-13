---
name: proposal-writer
description: Use when you want to turn call notes into a professional client proposal. Extracts key details, writes a structured proposal and cover email, and pushes both to a Google Doc.
version: 1.0.0
author: Pete Swain / Hermes Agent
output_mode: push
destination: Google Doc → email draft
---

⚠️ OUTPUT NOTE: The goal of this skill is NOT to display results in chat.
The outcome is pushing output to a meaningful destination — Slack, Google Doc,
email draft, Notion, or web. If you're reading this in chat, the skill hasn't
finished its job.

## Overview

Getting off a call and facing a blank document is a conversion killer. The faster a proposal follows the conversation, the higher the close rate — but speed without quality loses deals on substance. This skill takes your raw call notes (however messy) and turns them into a professional, client-ready proposal that mirrors the client's language, addresses their stated concerns, and positions your solution clearly. It also drafts the cover email to accompany it. Both are pushed to a Google Doc.

## When to Use

- You say "write a proposal from these notes"
- You say "turn call notes into a proposal"
- You've just finished a discovery or sales call and want to move fast
- You have old notes from a meeting and need to formalise them into a proposal
- You want to standardise your proposal format across your business

## How It Works

1. **Receive the call notes.** Ask the user to paste their notes. These can be:
   - Rough bullet points
   - A voice-memo transcription
   - A mix of notes and half-sentences
   - A structured summary they've already started
   Raw is fine. The agent will extract and shape.

2. **Extract the key elements.** From the notes, identify and confirm:
   - **Client's stated pain** — what problem did they describe in their own words?
   - **Their goal** — what outcome are they trying to achieve?
   - **Timeline** — when do they need to see results or make a decision?
   - **Budget signal** — any number mentioned, range indicated, or signals about flexibility?
   - **Decision process** — who else is involved? What does their approval process look like?
   - **Objections or concerns raised** — anything they pushed back on or flagged as a risk?

   If any of these are unclear from the notes, ask one clarifying question before writing. Do not invent details.

3. **Write the full proposal.** Structure:

   **Executive Summary (1 paragraph)**
   A plain-language summary of the engagement: who it's for, what the core challenge is, what the outcome of working together will be. Written from the client's perspective — their problem, their goal. No jargon, no fluff.

   **The Problem We're Solving (1–2 paragraphs)**
   Reflect the client's pain back to them in crisp, specific language. Use phrases from the call notes where possible — mirror their words. Show that you heard them, not just processed them. Name the cost of not solving this (time, money, missed opportunity, risk).

   **Our Approach (2–3 paragraphs)**
   Describe the methodology or process clearly. What will actually happen, in what order, and why that approach is the right one for their situation. Be concrete — not "we'll work collaboratively" but "in week 1 we'll do X, then Y." Name any frameworks, tools, or proprietary methods.

   **What You Get (bullet list)**
   A clear, scannable list of deliverables. Each item should be specific: not "strategy sessions" but "4 x 60-minute strategy sessions, recorded and transcribed." Specificity builds trust. Include timelines next to each deliverable.

   **Investment (1 paragraph + clear pricing)**
   State the investment clearly. If it's a range, state the range and explain what determines where they land. If it's fixed, state it plainly. Do not bury the price or hide it in jargon. If there are payment options, list them simply.

   **Next Steps (3–5 bullet points)**
   What happens after they say yes? Make it dead simple: sign here, invoice sent, kickoff call booked, work begins. Reduce the decision friction by making the path forward obvious.

4. **Draft the cover email.** A 150–200 word email to accompany the proposal:
   - Subject line: "[Proposal] [Client Name] × [Your Name/Company]"
   - Open with a warm reference to the call
   - One sentence on what the proposal contains
   - Encourage them to review and raise any questions
   - Suggested next step (e.g., "Happy to walk through this on a 20-minute call")
   - Professional close

5. **Push to Google Doc.** Create a document titled: `Proposal — [Client Name] — [Date]`. Place the cover email at the top, followed by the full proposal. Format with clear headings and clean spacing.

6. **Confirm delivery.** Share the document link in chat.

## What the Agent Needs From You

- **Your call notes** — paste them in, however rough
- **Your name / business name** — for the proposal header
- **Client name and company** — for personalisation
- **Any details not in the notes** — e.g., pricing, your preferred proposal structure

## Output

- Full structured proposal: Executive Summary, Problem, Approach, Deliverables, Investment, Next Steps
- Cover email with subject line
- Both pushed to a new Google Doc, link shared in chat
