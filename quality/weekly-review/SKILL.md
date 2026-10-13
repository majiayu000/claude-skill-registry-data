---
name: weekly-review
description: Use when you want to do a structured end-of-week reflection. Runs a conversational review covering wins, losses, energy, decisions, and carry-forwards — one question at a time.
version: 1.0.0
author: Pete Swain / Hermes Agent
output_mode: chat
destination: direct chat response
---

## Overview

A week without a review is a week of compounding blind spots. The weekly review isn't about being hard on yourself — it's about learning fast, closing loops, and carrying only what matters into the next week. This skill runs a structured but conversational end-of-week reflection covering five areas: what got done, what didn't and why, energy, decision quality, and what carries forward. One question at a time, no pressure, then a clean summary to close the week properly.

## When to Use

- You say "weekly review"
- You say "Friday review"
- You say "end of week"
- It's Friday afternoon and you want to close the week properly before disconnecting
- You're building a habit of weekly reflection and want a consistent structure
- You had a rough or unexpected week and want to process it before it bleeds into the next

## How It Works

1. **Open the conversation.** Start simply: *"Let's close out the week. I'll ask you 5 questions — take as long or as little as you like with each one. Ready? Let's start."*

2. **Ask the 5 questions, one at a time.** Do NOT ask the next question until the user has answered the current one. Keep your responses between questions minimal — this is their reflection, not a conversation. A brief acknowledgement or one clarifying follow-up is enough.

   **Question 1 — Wins**
   *"What actually got done this week? Not what you planned — what happened?"*
   Listen for: completed outputs, conversations that moved things forward, decisions made, personal wins alongside professional ones. If the user undersells their week, gently name what you heard: *"That sounds like more than you're giving yourself credit for."*

   **Question 2 — Losses / Slips**
   *"What didn't happen this week — and do you know why?"*
   This isn't about self-flagellation. It's about pattern recognition. Listen for: procrastination patterns, unexpected interruptions, overcommitment, decision fatigue, or things that simply weren't as important as they thought. Reflect back what you hear without judgment: *"It sounds like [X] kept getting deprioritised — is that a theme you've noticed before?"*

   **Question 3 — Energy**
   *"What drained you this week? And what fuelled you?"*
   Energy is data. A task that drained you every day this week is a signal. An interaction that lit you up is equally important information. Listen for patterns and reflect them back. If they only mention one side (all drain or all fuel), ask: *"Anything on the other side?"*

   **Question 4 — Decision Quality**
   *"Is there one decision you made this week that you'd make differently — and what would you change?"*
   The goal is learning, not regret. If they struggle to name one, offer: *"It doesn't have to be a big one — even a small decision about time or priorities counts."* If they name one, ask one follow-up: *"What was the assumption that led to that decision?"*

   **Question 5 — Carry-Forwards**
   *"What are the 3 things rolling into next week — in order of importance?"*
   Force the rank order. If they list more than 3, ask: *"If you could only carry 3, which would they be?"* This prevents next week starting with a landslide of last week's unfinished business.

3. **Deliver the summary.** After all 5 questions, write a concise weekly review summary:

   ```
   📋 Weekly Review — [Date]

   ✅ Wins:
   [Bullet list — 3–5 items from what they shared]

   ⚠️ What Didn't Happen (and Why):
   [1–2 sentences — honest, non-judgmental pattern reflection]

   ⚡ Energy This Week:
   Drained by: [list]
   Fuelled by: [list]

   🧠 Decision to Learn From:
   [One sentence naming the decision and the insight]

   📌 Carrying Forward (in order):
   1. [Item]
   2. [Item]
   3. [Item]
   ```

4. **Close the week.** End with a one-line close: something genuine and forward-looking. Not a generic "great work!" — something that acknowledges what actually happened in the review.

## What the Agent Needs From You

- Just your honest answers to the 5 questions — rough, unedited, as they come

## Output

Delivered entirely in chat:
- A conversational 5-question review session
- A clean weekly review summary card at the end
- Closed with a genuine, context-aware one-liner to end the week
