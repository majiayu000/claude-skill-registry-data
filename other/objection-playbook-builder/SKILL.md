---
name: objection-playbook-builder
description: Use when you want a structured response guide for your most common sales objections. Builds a formatted playbook with acknowledge-reframe-close scripts for each objection, pushed to a Google Doc.
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

An objection without a prepared response is a deal lost. But the goal isn't to overcome objections with clever comebacks — it's to acknowledge them genuinely, reframe the conversation around value, and close on the real concern underneath. This skill builds a proper objection playbook: a reference document with a scripted 3-part response for each objection, a "never say this" warning, and the underlying mindset to approach each one confidently. Formatted as a Google Doc you can train with, review before calls, or hand to a new salesperson.

## When to Use

- You say "build an objection playbook"
- You say "how do I handle objections about X"
- You're training a sales team and need a consistent response framework
- You keep getting the same objections and want prepared, natural-sounding responses
- You're preparing for a high-stakes call and want to rehearse your responses
- You're launching a new offer and want to anticipate pushback before it happens

## How It Works

1. **Gather the objections.** Ask the user:
   - List your 5–10 most common objections. If they're not sure, prompt them to brainstorm:
     - What do people say when they hesitate to buy?
     - What's the most common reason people say no?
     - What objections do you find hardest to handle?
   - What is the offer or service these objections relate to?
   - What's the investment level? (This affects which objections are most common)

2. **Common objections to include if not mentioned:**
   - "It's too expensive" / "I can't afford it right now"
   - "I need to think about it"
   - "I need to speak to my [partner/team/boss] first"
   - "I'm not ready yet" / "The timing isn't right"
   - "I've tried things like this before and they didn't work"
   - "I can do this myself" / "I can find this for free"
   - "I'm not sure it'll work for my situation"
   - "I don't have time right now"

3. **Build the 3-part response for each objection.** For each objection, write:

   **Part 1 — Acknowledge (1–2 sentences)**
   Validate the concern without agreeing it's a reason not to buy. Never argue. Never dismiss. Example: "That makes complete sense — it's a real investment and I want to make sure it's the right decision for where you are right now."

   **Part 2 — Reframe (2–4 sentences)**
   Shift the perspective without being pushy. Reframe the cost as an investment, the timing as a choice, the doubt as information. Use a question where possible to draw out the real concern. Example: "Can I ask — when you say the timing isn't right, what would need to be different in 3 months for it to make sense?"

   **Part 3 — Close (1–2 sentences)**
   Move to the next micro-step — not a hard close, a natural continuation. Example: "Let's do this: look at the proposal again tonight and let me know by tomorrow what specific part feels unclear — I'll address it directly."

4. **Add a "Never Say This" column for each objection.** For each, name 1–2 phrases that make the situation worse:
   - "I understand, but..." (the "but" cancels the acknowledgement)
   - "Everyone feels that way at first" (condescending)
   - "This is actually a great deal" (defensive)
   - "Let me know when you're ready" (abandons the conversation)
   Write specific warnings relevant to each objection.

5. **Add an "Underlying concern" note.** For each objection, name the real concern hiding underneath — what the person is actually worried about that they're not saying. Example: "I need to think about it" often means "I'm not convinced enough yet" or "I'm afraid of making the wrong decision."

6. **Format as a playbook.** Each objection gets its own section:
   - **Objection:** [stated exactly as the prospect might say it]
   - **What they really mean:** [the underlying concern]
   - **Acknowledge:** [script]
   - **Reframe:** [script]
   - **Close:** [script]
   - **Never say:** [1–2 warnings]

7. **Push to Google Doc.** Create a document titled: `Objection Playbook — [Offer Name] — [Date]`. Include a one-page introduction explaining the 3-part framework and mindset for handling objections. Follow with each objection section. Format for easy scanning — use bold headings and clear visual separation.

8. **Confirm delivery.** Share the link in chat.

## What the Agent Needs From You

- **Your top 5–10 objections** (or let the agent help you brainstorm them)
- **Your offer** — what are you selling?
- **Investment level** — price point of your offer
- **Your sales style** — direct and confident, warm and consultative, or something in between?

## Output

- Full objection playbook for 5–10 objections
- Each entry: the objection, underlying concern, 3-part response script, and "never say" warnings
- Introduction page explaining the framework
- Pushed to a new Google Doc with link shared in chat
