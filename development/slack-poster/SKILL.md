---
name: slack-poster
description: Posts intelligent, topic-analyzed business news to Slack channels using threaded messages. Groups stories by themes and provides big-picture insights.
agents:
  - slack-poster-agent
---

# Slack Poster Skill

This skill posts business news and reports to Slack channels with intelligent topic analysis and threaded organization for better readability.

## Purpose

- Post business news digests with automatic topic grouping
- Provide big-picture insights by correlating related stories
- Use threaded messages to organize content by topic
- Send alerts, notifications, or reports to internal Slack channels programmatically

## Key Features

### 1. Topic Analysis & Grouping
- Automatically analyzes headlines to identify major themes
- Groups related stories together (e.g., "AI & Technology", "Markets & Economy")
- Correlates between stories to show the big picture
- Counts stories per topic for quick overview

### 2. Threaded Message Format
- **Main message**: Summary showing topic breakdown and key insights
- **Thread replies**: Detailed stories organized by topic
- Each topic thread includes all relevant stories with source attribution

### 3. Topic Categories
The skill automatically classifies stories into:
- 🤖 AI & Technology
- 📈 Markets & Economy
- 👔 Corporate Leadership & Governance
- 🛒 Retail & Consumer
- 💼 Business & Finance
- 🏥 Healthcare & Biotech
- 💼 Workplace & Careers
- 📰 Other News

## Implementation

### Basic Usage (post_to_slack.py)
Simple format posting top headlines with blocks formatting.

### Advanced Usage (post_to_slack_threaded.py)
Intelligent topic analysis with threaded organization:
- Analyzes all headlines for common themes
- Groups stories by topic
- Creates main summary message with big-picture insights
- Posts detailed stories in topic-specific threads

## Authentication

Slack credentials:
- **Token**: Use environment variable `SLACK_TOKEN`
- **Channel**: `stock_ops_dev` (or use environment variable `SLACK_CHANNEL`)

## Example Output

**Main Message:**
```
📰 Business News Digest - November 19, 2025

40 stories analyzed across 7 major topics

🔍 Today's Big Picture:
• AI & Technology: 19 stories
• Markets & Economy: 4 stories
• Corporate Leadership & Governance: 2 stories

🤖 AI dominates headlines with 19 stories covering Nvidia earnings,
   OpenAI board changes, and the AI bubble debate
```

**Thread Replies:** Each topic gets its own detailed thread with all related stories.


## Output Structure

All outputs are organized in the outputs/ directory:

- Reports should go into `outputs/<agent_name>/<customer_name>/reports/`
- Scripts should go into `outputs/<agent_name>/<customer_name>/scripts/`
- Raw outputs (csvs, jsons) should go into `outputs/<agent_name>/<customer_name>/raw/`
- Screenshots should go into `outputs/<agent_name>/<customer_name>/screenshots/`
