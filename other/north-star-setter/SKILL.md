---
name: north-star-setter
description: Use when you want to set a clear focus for the week. Runs a 5-question conversation, creates a weekly north star card, and pushes it to Notion and Slack.
version: 1.0.0
author: Pete Swain / Hermes Agent
output_mode: push
destination: Notion + Slack
---

⚠️ OUTPUT NOTE: The goal of this skill is NOT to display results in chat.
The outcome is pushing output to a meaningful destination — Slack, Google Doc,
email draft, Notion, or web. If you're reading this in chat, the skill hasn't
finished its job.

## Overview

A busy week without a north star is just motion, not progress. This skill runs a structured 5-question conversation at the start of each week to surface your true priority, your biggest risks, and what you're explicitly choosing NOT to do. The result is a weekly north star card — a single, compact reference document — pushed to Notion for tracking and posted to Slack so your team (or just you) can see it. Designed to run on Monday mornings, but works anytime you need to reset focus.

## When to Use

- You say "set my north star"
- You say "weekly focus"
- You say "Monday planning"
- It's the start of a new week and you haven't defined your priority
- You've lost focus mid-week and need to re-anchor
- You're context-switching too much and want to force a single point of commitment

## How It Works

1. **Run the 5-question conversation.** Ask each question one at a time. Wait for a full answer before moving to the next. Do not rush — the value is in the thinking, not just the answers.

   **Question 1: What's the #1 outcome this week that would make everything else secondary?**
   Push for specificity. "Growth" is not an answer. "Closing the proposal with [Client]" or "Finishing and publishing the landing page" is an answer. If the user gives something vague, ask: *"What does that look like as a concrete, observable outcome by Friday?"*

   **Question 2: What's the biggest risk to achieving that outcome?**
   This surfaces blockers before they become failures. Prompt if needed: *"Is it a time constraint? A dependency on someone else? A decision you haven't made yet? A task you keep avoiding?"*

   **Question 3: What are you carrying forward from last week?**
   Unclosed loops from last week are this week's hidden drag. Get them named so they can be consciously managed — either prioritised or explicitly deprioritised.

   **Question 4: What are you NOT doing this week?**
   This is often the most powerful question. What's on the list that will NOT get done — and do you accept that? Naming it makes it a decision, not a failure. Prompt: *"What's tempting but would dilute focus this week?"*

   **Question 5: What does winning look like by Friday?**
   Not the north star outcome — the feeling. Are you looking for momentum, completion, breakthrough, calm, or connection? This sets the emotional benchmark for the week.

2. **Synthesise the north star card.** From the 5 answers, create a compact weekly card:

   ```
   🌟 Weekly North Star — [Week of Date]

   🎯 The One Outcome:
   [One sentence — specific, observable, by Friday]

   ⚠️ Biggest Risk:
   [One sentence — the specific threat to the outcome]

   🔄 Carried Forward:
   · [Item 1]
   · [Item 2]

   🚫 Not This Week:
   · [Item 1]
   · [Item 2]

   ✅ Winning Looks Like:
   [One sentence — the feeling/state by Friday]
   ```

3. **Push to Notion.** Create a new page in the user's configured Notion database (Weekly Reviews or similar) with the full north star card. Include the date, all 5 question answers in full, and the synthesised card at the top.

4. **Post to Slack.** Send the compact card (not the full answers) to the configured Slack channel. This could be a personal channel, a team channel, or an accountability channel — whatever the user has configured.

5. **Confirm delivery.** Report in chat: *"Your north star card for the week is live in Notion and posted to Slack. Let's make it happen."*

## What the Agent Needs From You

- **Answers to 5 questions** — asked one at a time in conversation
- **Connected Notion workspace** — with a designated database for weekly planning
- **Connected Slack workspace** — with a configured channel for the post

## Output

- A weekly north star card: one outcome, one risk, carried-forward items, not-this-week list, winning definition
- Full conversation answers saved to Notion
- Compact card posted to Slack
- Confirmation in chat when both pushes are complete
