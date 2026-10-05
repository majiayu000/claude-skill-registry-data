---
name: chatbot-automation
displayName: Chatbot Automation
tagline: Build and manage automated chatbot workflows for customer support and self-service.
description: |
  Creates intelligent chatbot workflows that handle common customer
  queries, collect information, and route complex issues to human agents.
  Designs conversation flows, configures response templates, and tracks
  chatbot performance metrics like resolution rate and handoff rate.
department:
  - Customer Support
  - Product
use_cases:
  - Chatbot Design
  - Customer Self-service
  - Support Automation
tools_required:
  - Intercom MCP
  - Slack MCP
agents_compatible:
  - Claude / Claude Code
  - Cursor
  - Windsurf
  - ChatGPT
  - Any MCP-compatible agent
author: Webrix
verified: true
updatedAt: 2026-05-08
version: 1.0.0
exampleInput: |
  Build a chatbot for our SaaS product that handles:
  - Password resets
  - Billing questions
  - Feature requests
  - Bug reports
exampleOutput: |
  Chatbot Configuration — SaaS Support

  CONVERSATION FLOWS
  1. Password Reset:     Self-service (link to reset page)
  2. Billing Questions:  Check subscription -> show invoice -> escalate if needed
  3. Feature Requests:   Collect details -> create ticket -> thank user
  4. Bug Reports:        Collect repro steps -> priority assessment -> route to eng

  PERFORMANCE (last 30 days)
  Conversations:     1,840
  Bot Resolved:      1,104 (60%)
  Handed to Human:   736 (40%)
  Avg Resolution:    2.3 minutes (bot) vs 18 minutes (human)
  CSAT (bot):        4.1/5.0

  TOP QUERIES HANDLED BY BOT
  1. "How do I reset my password?" — 320 conversations
  2. "What's my billing date?" — 180 conversations
  3. "How do I upgrade my plan?" — 145 conversations
---

# Chatbot Automation

Build and manage automated chatbot workflows for customer support and self-service.

**Integrations:** Intercom, Slack

## When to Use

- The user wants to build chatbot flows for customer support
- Common queries should be handled without human intervention
- The user mentions "chatbot", "automated support", or "self-service"

## Steps

### Step 1: Identify Common Queries

Analyze support tickets to find the most frequent customer questions.

### Step 2: Design Conversation Flows

Create decision trees for each query type with response templates.

### Step 3: Configure Handoff Rules

Define when and how to escalate to human agents.

### Step 4: Track Performance

Monitor resolution rate, CSAT, and handoff metrics.

## Output

Deliver:
- Chatbot conversation flows
- Response templates
- Performance tracking dashboard
