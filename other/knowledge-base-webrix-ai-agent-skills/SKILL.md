---
name: knowledge-base
displayName: Knowledge Base Management
tagline: Create and maintain a self-service knowledge base with articles, FAQs, and troubleshooting guides.
description: |
  Manages a customer-facing knowledge base with article creation, content
  organization, and gap analysis. Identifies missing articles based on
  support ticket patterns, generates draft articles from resolved tickets,
  and tracks article effectiveness by deflection rate and helpfulness scores.
department:
  - Customer Support
  - Product
use_cases:
  - Knowledge Management
  - Self-service
  - Content Creation
tools_required:
  - Zendesk MCP
  - Intercom MCP
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
  Analyze support tickets to find knowledge base gaps.
  Generate draft articles for the top 5 missing topics.
exampleOutput: |
  Knowledge Base Gap Analysis

  CURRENT STATE
  Total Articles:    145
  Monthly Views:     28,000
  Ticket Deflection: 32% (target: 45%)

  TOP GAPS (tickets without KB match)
  1. "How to set up SSO with Okta" — 85 tickets/month — NO ARTICLE
  2. "API rate limiting explained" — 62 tickets/month — OUTDATED article
  3. "Migrating from v2 to v3" — 48 tickets/month — NO ARTICLE
  4. "Custom webhook configuration" — 35 tickets/month — NO ARTICLE
  5. "Team permissions breakdown" — 30 tickets/month — INCOMPLETE article

  DRAFT ARTICLES GENERATED
  ✅ 5 draft articles created from resolved ticket patterns
  ✅ 2 existing articles flagged for update
  
  Estimated Impact: +8% deflection rate (to 40%)
---

# Knowledge Base Management

Create and maintain a self-service knowledge base with articles, FAQs, and troubleshooting guides.

**Integrations:** Zendesk, Intercom

## When to Use

- The knowledge base needs new articles or updates
- Ticket deflection rate is below target
- The user mentions "knowledge base", "help articles", or "self-service content"

## Steps

### Step 1: Analyze Ticket Patterns

Identify common queries without matching knowledge base articles.

### Step 2: Generate Draft Articles

Create article drafts from patterns in resolved tickets.

### Step 3: Track Effectiveness

Monitor article views, helpfulness scores, and deflection impact.

## Output

Deliver:
- Gap analysis with priority topics
- Draft articles for missing topics
- Deflection rate tracking and improvement plan
