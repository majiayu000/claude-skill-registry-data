---
title: Build a Claude Skill for a Smart Daily Pulse
description: Learn how to create a Claude skill that generates a personalized morning briefing powered by Google Calendar and Gmail through Pica MCP Server.
---

<Frame caption="Build your own Claude skill for daily briefings">
  <iframe
    className="w-full aspect-video rounded-xl"
    src="https://www.youtube.com/embed/-Bv72hPFkio"
    title="Build a Claude Skill for a Smart Daily Pulse"
    frameborder="0"
    allowFullScreen
  ></iframe>
</Frame>

## Overview

In this tutorial, you'll learn how to build a Claude skill that generates a personalized Daily Pulse — a smart morning briefing powered by your Google Calendar and Gmail. We'll do this using the Pica MCP Server and Claude Desktop.

By the end, you'll have your own automated daily summary that helps you start every day with clarity and focus — no manual work required. Perfect for founders, operators, or anyone who wants a smarter morning routine.

## Prerequisites

Before you start, make sure you have:

1. A [Pica account](https://app.picaos.com) (free)
2. [Claude Desktop](https://claude.ai/download) installed
3. Google Calendar and Gmail connected in your Pica dashboard

## Getting Started

### Step 1: Connect Your Integrations

Connect your Google Calendar and Gmail accounts to Pica:

1. Go to [Gmail Connection](https://app.picaos.com/connections#open=gmail)
2. Go to [Google Calendar Connection](https://app.picaos.com/connections#open=google-calendar)
3. Authorize both integrations

### Step 2: Install Pica MCP Server

Install and configure the Pica MCP Server in Claude Desktop by following our [setup guide](/mcp-server/claude-desktop).

### Step 3: Create the Daily Pulse Skill

1. Create a new folder called `daily-pulse` on your computer
2. Inside this folder, create a file named `Skill.md`
3. Copy and paste the content below into `Skill.md`:

```markdown expandable
---
name: daily-pulse
description: Generates a personalized daily briefing by analyzing Google Calendar events and unread Gmail messages through Pica MCP Server. Use this when users request their daily overview, morning briefing, day's agenda, pulse check, or want to see what's important today.
---

# Daily Pulse

## Overview

Daily Pulse generates a personalized morning briefing that synthesizes your calendar and email into actionable insights. By connecting to Google Calendar and Gmail through the Pica MCP Server, it identifies priorities, surfaces urgent items, and helps you start your day with clarity.

## When to Use This Skill

Trigger this skill when users request:
- "What's my daily pulse?"
- "Give me my morning briefing"
- "What should I focus on today?"
- "Show me today's priorities"
- "What's on my agenda?"
- "Help me plan my day"
- Any variation requesting a daily overview or pulse check

## How It Works

The skill follows a three-phase process to generate your daily briefing:

### Phase 1: Data Collection

**Calendar Events (via Pica MCP Server)**
- Retrieve today's calendar events from Google Calendar
- Include event titles, times, attendees, and descriptions
- Capture meeting durations and locations (if applicable)

**Email Summary (via Pica MCP Server)**
- Fetch unread Gmail messages from today
- Extract sender, subject, timestamp, and preview content
- Identify emails requiring action vs. informational emails

### Phase 2: Analysis & Prioritization

**Event Intelligence**
- Identify high-impact meetings (1-on-1s, client calls, presentations)
- Detect preparation requirements from event descriptions
- Calculate available focus blocks between meetings
- Flag scheduling conflicts or back-to-back meetings

**Email Triage**
- Categorize by urgency (time-sensitive, actionable, informational)
- Identify emails from key people or about ongoing projects
- Surface items requiring responses before EOD
- Detect opportunities or inbound requests

**Time Analysis**
- Calculate total meeting time vs. available focus time
- Identify optimal work blocks for deep work
- Flag overbooked periods or insufficient breaks

### Phase 3: Briefing Generation

Generate a structured daily pulse containing:

**1. Executive Summary (Top 3 Priorities)**
- The most important items requiring attention today
- Action-oriented statements with context

**2. Calendar Intelligence**
- Total meetings with breakdown by type
- High-priority events requiring preparation
- Available focus blocks for deep work
- Recommendations for rescheduling low-priority items

**3. Email Priorities**
- Urgent emails requiring immediate action
- Important emails needing responses today
- Quick wins (emails that take <5 minutes)
- Can-wait items (FYI or low priority)

**4. Time Optimization**
- Best windows for focused work
- Suggested task sequencing
- Energy management recommendations

**5. Quick Actions**
- Immediate 2-minute tasks to clear
- Preparation items for upcoming meetings
- Follow-ups to send

## Output Format

Structure the daily pulse as follows:

🌅 Daily Pulse for [Date]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 TOP 3 PRIORITIES
1. [Most important item with context]
2. [Second priority with context]
3. [Third priority with context]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 CALENDAR INTELLIGENCE ([X] meetings, [Y]h total)

HIGH-IMPACT EVENTS
- [Time] - [Event Name]
  → [Why it matters / Prep needed]

FOCUS BLOCKS AVAILABLE
- [Time Range] - [Duration] 
  → [Recommendation for use]

⚠️ SCHEDULING NOTES
- [Any conflicts, back-to-backs, or recommendations]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📧 EMAIL PRIORITIES ([X] unread)

🔴 URGENT (Action Required Today)
- From: [Sender] | Re: [Subject]
  → [Why urgent / What's needed]

🟡 IMPORTANT (Response Needed)
- From: [Sender] | Re: [Subject]
  → [Context / Suggested action]

⚡ QUICK WINS (<5 min)
- [Brief email summaries that can be handled quickly]

📥 FYI / Lower Priority
- [Count] informational emails can wait

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏰ TIME OPTIMIZATION

BEST FOCUS WINDOWS
- [Time] - Deep work on [suggested task]
- [Time] - Batch email responses

ENERGY MANAGEMENT
- [Recommendations based on meeting density]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ QUICK ACTIONS (Do These First)

1. [Immediate 2-min action]
2. [Prep for upcoming meeting]
3. [Quick follow-up to send]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Best Practices

**Tone & Language**
- Be concise and action-oriented
- Use clear, scannable formatting with emojis for visual hierarchy
- Focus on "what matters" and "what to do" not just "what exists"
- Provide context for why things are prioritized

**Prioritization Logic**
- Weight meetings by: attendee seniority, meeting type, preparation needs
- Weight emails by: sender importance, subject keywords, time-sensitivity
- Consider recency (items happening soon > items later in day)

**Time Management**
- Always identify at least one substantial focus block if possible
- Flag when the day is overbooked (>80% meeting time)
- Suggest protecting focus time when applicable

**Contextual Intelligence**
- Connect related items (e.g., email about a project + meeting about same project)
- Identify patterns (e.g., multiple requests from same person/topic)
- Surface anomalies (unusual sender, unexpected meeting, urgent language)

## Error Handling

**If Calendar Access Fails**
- Inform user that calendar couldn't be accessed via Pica
- Provide email-only pulse with disclaimer
- Suggest troubleshooting Pica MCP Server connection

**If Gmail Access Fails**
- Inform user that email couldn't be accessed via Pica
- Provide calendar-only pulse with disclaimer
- Suggest checking Pica authentication

**If Both Fail**
- Clearly explain the connection issue
- Provide instructions for reconnecting Pica MCP Server
- Offer to generate pulse again once connection is restored

**If No Events or Emails**
- Generate a positive pulse noting the light schedule
- Suggest proactive tasks or goals to work on
- Highlight this as an opportunity for deep work or planning

## Privacy & Sensitivity

- Never quote full email contents verbatim in the pulse
- Summarize sensitive information professionally
- If calendar events seem private, reference them discreetly
- Focus on actionable insights rather than raw data dumps

## Example Interactions

**User:** "What's my daily pulse?"

**Claude:** [Fetches calendar events via Pica, fetches unread emails via Pica, analyzes data, generates formatted pulse as shown above]

**User:** "Give me my morning briefing"

**Claude:** [Same process - recognizes this as a pulse request]

**User:** "What should I focus on first?"

**Claude:** [Generates pulse with extra emphasis on the Quick Actions section]
```

### Step 4: Add the Skill to Claude

1. Compress the `daily-pulse` folder into a ZIP file
2. Open Claude Desktop
3. Go to **Claude Settings** → **Capabilities** → **Add new Skill**
4. Upload the ZIP file containing your `Skill.md`

### Step 5: Test Your Skill

1. Open a new chat in Claude Desktop
2. Ask: **"What's my daily pulse?"**
3. Claude will analyze your calendar and email, then generate your personalized morning briefing! 🌅

## What You'll Get

Your Daily Pulse skill will provide:

- 🎯 **Top 3 Priorities** - The most important items requiring your attention
- 📅 **Calendar Intelligence** - Meeting breakdown with focus blocks and scheduling insights
- 📧 **Email Priorities** - Categorized emails by urgency and importance
- ⏰ **Time Optimization** - Best windows for focused work and energy management
- ✅ **Quick Actions** - Immediate tasks to tackle first

## Source Code

<Card title="Source Code" icon="github" href="https://github.com/picahq/awesome-pica/tree/main/claude-skills" horizontal>
  View the complete source code for this example on GitHub
</Card>

## 📖 Learning Resources

### Official Anthropic Resources
- [Skills Overview Guide](https://support.claude.com/en/articles/12512176-what-are-skills) - Foundational concepts and setup
- [Skills Usage Manual](https://support.claude.com/en/articles/12512180-using-skills-in-claude) - Practical implementation guide
- [Skills Announcement Blog](https://www.anthropic.com/news/skills) - Vision and roadmap from Anthropic
- [Agent Skills Engineering](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) - Technical deep dive

### Developer Resources
- [Claude API Documentation](https://docs.claude.com/) - Complete platform reference
- [Skills API Reference](https://docs.claude.com/en/api/skills) - `/v1/skills` endpoint details
- [Official Skills Repository](https://github.com/anthropics/skills) - Anthropic's curated collection
- [Skills Cookbook](https://github.com/anthropics/claude-cookbooks/tree/main/skills) - Tutorials and examples

## Resources

<CardGroup cols={2}>
  <Card title="Pica MCP Server" icon="server" href="/mcp-server">
    Learn more about the MCP Server
  </Card>
  <Card title="Gmail Integration" icon="envelope" href="https://app.picaos.com/connections#open=gmail">
    Connect your Gmail account
  </Card>
  <Card title="Google Calendar Integration" icon="calendar" href="https://app.picaos.com/connections#open=google-calendar">
    Connect your Google Calendar
  </Card>
  <Card title="Claude Desktop Setup" icon="desktop" href="/mcp-server/claude-desktop">
    Configure Claude Desktop with Pica
  </Card>
</CardGroup>

