---
name: daily-read
description: Use when you want one genuinely worthwhile article to read today. Finds a recent, relevant piece in AI, entrepreneurship, or your focus area and pushes it to Slack with a one-line "insight worth stealing."
version: 1.0.0
author: Pete Swain / Hermes Agent
output_mode: push
destination: Slack
---

# Daily Read

⚠️ OUTPUT NOTE: The goal of this skill is NOT to display results in chat.
The outcome is pushing output to a meaningful destination — Slack. If you're reading this in chat, the skill hasn't finished its job.

## Overview

One article. One insight. Every day. The internet produces infinite content and most of it is noise. This skill cuts through it — finding one thing published in the last 7 days that's actually worth your time, distilling the key insight down to one sentence, and pushing it to your Slack so it's there when you need it. No rabbit holes. No newsletter overwhelm. Just one thing.

## When to Use

- When you want to stay sharp without spending an hour on your RSS feed
- When you've been heads-down for days and want to surface something fresh
- As a daily scheduled cron job to land in Slack each morning
- Trigger phrases: "find me something to read", "daily read", "what should I read today"

## How It Works

1. **Ask for focus area (if not already in memory)**
   If the user hasn't set a focus area, ask: "What's most relevant to you right now? (e.g. AI strategy, leadership, marketing, sales, your specific industry)" Store the answer for future runs.

2. **Search for a recent, relevant article**
   Search for articles published in the last 7 days matching: AI × entrepreneurship × marketing × the user's stated focus area. Prioritise: essays over news, practitioner voice over punditry, specific insight over general trends. Avoid: vendor content, press releases, listicles with no substance, anything that starts with "The future of AI is..."

3. **Evaluate quality**
   The article must have at least ONE insight that is:
   - Specific (not "AI is changing everything")
   - Actionable or perspective-shifting (makes you think or do differently)
   - Not something you'd already know if you've been paying attention

4. **Draft the Slack message**
   Format:
   ```
   📖 *Today's Read*

   *[Article Title]* — [Source/Author]
   [Link]

   *In 2 sentences:* [What the article is about and why it matters]

   *Insight worth stealing:* [The one concrete idea, framing, or tactic to take away]
   ```

5. **Push to Slack**
   Post to the user's configured Slack channel. Default: a personal or #reading channel. Confirm the channel before first use.

6. **Confirm in chat**
   Brief confirmation: "Sent to Slack — [article title]."

## What the Agent Needs From You

- Your Slack workspace and channel (set once, remembered)
- Your focus area / topics of interest (set once, remembered)
- No daily input needed — this is designed to run on schedule without interaction

## Output

A clean Slack message with the article title, link, 2-sentence summary, and one insight worth stealing. Stays in Slack. Doesn't require you to respond.

## Running on Schedule

This skill works best as a daily cron job, triggered each morning before you start work. Ask your agent to set it up: "Run the daily read skill every morning at 7am and push to Slack."

## Quality Bar

If no genuinely worthwhile article can be found on a given day, do not post filler. Post nothing and note in the confirmation: "Nothing worth your time today — skipping." Quality over consistency.
