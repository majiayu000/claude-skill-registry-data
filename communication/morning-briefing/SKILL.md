---
name: morning-briefing
description: Use when you want a daily briefing to start your day. Delivers weather, calendar, priorities, news headlines, and urgent email highlights — pushed to Telegram every morning.
version: 1.0.0
author: Pete Swain / Hermes Agent
output_mode: push
destination: Telegram
---

⚠️ OUTPUT NOTE: The goal of this skill is NOT to display results in chat.
The outcome is pushing output to a meaningful destination — Slack, Google Doc,
email draft, Notion, or web. If you're reading this in chat, the skill hasn't
finished its job.

## Overview

Starting the day scattered costs more than most people realise. This skill delivers a concise, personalised morning briefing — everything you need to know in under 2 minutes of reading — pushed to Telegram before you open your laptop. Weather, calendar, top priorities, news that matters to you, and anything urgent from your inbox. One message, every morning, so you start with context instead of chaos.

This skill is designed to run as a scheduled cron job. Configure it once, and it runs automatically.

## Configuration

Before this skill runs automatically, set the following in your Hermes skill config:

- **Location** — your city or region (for weather)
- **Calendar** — connected Google Calendar or Outlook calendar
- **Task platform** — Todoist, Notion, Linear, or plain text (for top priorities)
- **News topics** — your focus areas (default: AI, entrepreneurship, marketing)
- **Email account** — Gmail or Outlook for urgent email scan
- **Telegram channel/chat ID** — where to deliver the briefing
- **Delivery time** — what time to send (default: 7:00 AM in your timezone)

## When to Use

- You say "morning briefing"
- Run automatically as a scheduled daily cron job
- Manually triggered when you've been offline and need to catch up
- You're starting a new Hermes setup and want to establish a daily rhythm

## How It Works

1. **Fetch weather.** Get the current conditions and today's forecast for the configured location. Include: temperature (high/low), conditions (clear, rain, etc.), and one relevant note if conditions are unusual (e.g., storm warning, heatwave).

2. **Pull calendar events.** Access the user's connected calendar and list today's events. Include: event name, time, and any relevant detail (location, attendees if fewer than 4, or "online" if a video call). Flag any event starting within 60 minutes of delivery time as ⚡ urgent.

3. **Surface top 3 priorities.** Access the connected task platform and identify the top 3 tasks for today. These should be: tasks explicitly marked as today's priorities, or the 3 most urgent/overdue tasks if no explicit priority is set. Do not list more than 3 — brevity is the point.

4. **Fetch 3 news headlines.** Search for articles published in the last 24 hours on the user's configured focus areas (default: AI × entrepreneurship × marketing). For each headline include: the title, the source, and a one-sentence summary. No more than 3 headlines — quality over volume.

5. **Scan for urgent email.** Check the inbox for emails received since the last briefing that meet the urgency criteria: emails from known senders (existing contacts) marked as urgent or flagged, emails with subject lines containing time-sensitive keywords (e.g., "urgent", "today", "deadline", "action required"), or replies to a thread you're actively part of. Surface up to 3 urgent items. If none, omit this section entirely.

6. **Compose and push the briefing.** Format the Telegram message as:

   ```
   ☀️ Morning Briefing — [Day, Date]

   🌤 Weather: [City] — [Temp] · [Conditions]

   📅 Today's Calendar:
   · [Time] — [Event name]
   · [Time] — [Event name]
   (+ X more events today)

   🎯 Top Priorities:
   1. [Task 1]
   2. [Task 2]
   3. [Task 3]

   📰 In the News:
   · [Headline 1] — [Source] · [One sentence]
   · [Headline 2] — [Source] · [One sentence]
   · [Headline 3] — [Source] · [One sentence]

   📬 Urgent Inbox (if any):
   · [Sender] — "[Subject]"

   Good morning. Go make it count. 🟢
   ```

7. **Confirm delivery.** Log the send time and status. If the push fails, retry once and notify via a fallback channel if configured.

## What the Agent Needs From You

- **Location** — for weather
- **Connected calendar** — Google Calendar or Outlook
- **Connected task system** — Todoist, Notion, or other
- **News focus areas** — topics you care about
- **Connected email account** — for urgent mail scan
- **Telegram chat ID** — where the briefing lands
- **Preferred delivery time** — and your timezone

## Output

- One clean Telegram message every morning
- Covers: weather, calendar, top 3 priorities, 3 news headlines, urgent emails
- Delivered at the configured time via cron trigger
