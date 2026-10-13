---
name: nurture-sequence-writer
description: Use when you need a 5-email nurture sequence for a new lead or offer. Writes the full sequence with subject lines, preview text, and body copy, then pushes to a Google Doc.
version: 1.0.0
author: Pete Swain / Hermes Agent
output_mode: push
destination: Google Doc
---

⚠️ OUTPUT NOTE: The goal of this skill is NOT to display results in chat.
The outcome is pushing output to a meaningful destination — Slack, Google Doc,
email draft, Notion, or web. If you're reading this in chat, the skill hasn't
finished its job.

## Overview

A nurture sequence is the bridge between someone opting in and deciding to buy. Most sequences fail because they're either too salesy (pitching too fast) or too passive (delivering value with no direction). This skill writes a 5-email sequence structured around the psychology of trust-building — starting with connection, building credibility through story, creating awareness of a problem, demonstrating proof, and ending with a clear, low-friction invitation to the next step. Every email includes a subject line, preview text, and full body copy.

## When to Use

- You say "write a nurture sequence"
- You say "email sequence for this offer"
- You've launched a lead magnet and need the follow-up sequence
- You're building a new funnel and need the middle-of-funnel emails
- You're re-architecting your email automation and starting fresh

## How It Works

1. **Gather the brief.** Ask the user for:
   - What did they opt in for? (The lead magnet topic)
   - What is the paid offer or next step at the end of the sequence?
   - Who is this reader? (Role, situation, biggest pain point)
   - What's the sender's story or background relevant to this topic?
   - Do you have a case study or client result you can share?
   - What's the tone? (Formal/informal, warm/direct, long-form/punchy)

2. **Write all 5 emails.** Each email must include:
   - **Subject line** — tested-format subject (question, number, curiosity gap, or bold statement)
   - **Preview text** — the 60–90 character line that appears after the subject in the inbox
   - **Body copy** — written in first person, conversational, single-column structure

   ---

   **Email 1 — Welcome + Big Promise**
   Send timing: Immediately on opt-in.
   Purpose: Confirm they made the right call and set the tone for what's coming.
   Structure: Welcome them personally → deliver or confirm delivery of the lead magnet → tell them what to expect from the next 4 emails → make the big promise: what their world looks like after they've done the work → sign off warmly.
   Length: 200–300 words.

   **Email 2 — Origin Story / Credibility**
   Send timing: Day 2.
   Purpose: Build connection and establish authority without bragging.
   Structure: Open with a moment of struggle or frustration → share the journey (keep it relevant, not a CV) → land on the realisation or turning point → connect it directly to what the reader is going through → soft close with a forward-looking sentence.
   Length: 300–400 words.

   **Email 3 — The Mistake They're Making**
   Send timing: Day 3 or 4.
   Purpose: Create awareness of the root cause of their problem.
   Structure: Name the common mistake (be specific, not generic) → explain why it's so common and how it keeps them stuck → hint at the better way without fully revealing it → create a sense of "I've been doing this wrong" without shame — make it empowering.
   Length: 300–400 words.

   **Email 4 — Case Study / Proof**
   Send timing: Day 5.
   Purpose: Demonstrate that the approach works — for real people, with real results.
   Structure: Introduce a client or example (can be anonymised) → describe where they started → what changed (the method, not just the result) → specific outcome with numbers if available → connect the story back to the reader's situation.
   Length: 350–450 words.

   **Email 5 — Soft Pitch to Next Step**
   Send timing: Day 7.
   Purpose: Invite without pressure. Open the door, don't push through it.
   Structure: Reference the journey of the last week → summarise what they now know → introduce the next step naturally (the offer, discovery call, community, programme) → explain what it is in one sentence → explain who it's for and who it's NOT for → clear, single CTA → handle the one biggest objection in a P.S.
   Length: 400–500 words.

3. **Push to Google Doc.** Create a new document titled: `[Offer Name] — Nurture Sequence — [Date]`. Format each email with its number, name, subject line, preview text, send timing, and full body. Add a one-page "Sequence Overview" at the top with send schedule and goal of each email.

4. **Confirm delivery.** Share the document link in chat.

## What the Agent Needs From You

- **Lead magnet topic** — what did the reader opt in for?
- **The paid offer** — what is the next step or purchase?
- **Reader description** — who is this person and what's their pain?
- **Your story or background** — relevant credibility to weave into Email 2
- **A case study or result** — for Email 4 (can be rough — the agent will shape it)
- **Tone preference** — how do you write to your list?

## Output

- 5 complete emails: subject line, preview text, full body copy
- Send schedule included for each email
- Sequence overview page included
- Pushed to a new Google Doc with link shared in chat
