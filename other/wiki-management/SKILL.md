---
name: wiki-management
displayName: Wiki Management
tagline: Organize and maintain team wikis with structure templates, stale content detection, and search optimization.
description: |
  Manages team knowledge bases and wikis in Notion or Google Docs. Organizes
  content with consistent structure templates, detects stale or outdated
  pages, ensures search discoverability, and tracks content coverage gaps.
  Helps teams maintain up-to-date, findable documentation.
department:
  - Engineering
  - Operations
  - Product
use_cases:
  - Knowledge Management
  - Documentation
  - Content Organization
tools_required:
  - Notion MCP
  - Google Workspace MCP
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
  Audit our Notion engineering wiki.
  Find stale pages (>90 days old), missing sections, and broken links.
exampleOutput: |
  Wiki Audit — Engineering Notion

  OVERVIEW
  Total Pages:       284
  Recently Updated:  142 (50%)
  Stale (>90 days):  89 (31%)
  Orphaned:          12 (no links to them)

  STALE PAGES (top priority)
  1. "Deployment Runbook" — 180 days old — HIGH TRAFFIC
  2. "API Authentication Guide" — 120 days old — references deprecated endpoint
  3. "Team Structure" — 95 days old — 3 people have since left

  MISSING SECTIONS
  - No runbook for database failover
  - No onboarding guide for frontend team
  - No architecture diagram for payments service

  BROKEN LINKS: 8 found across 6 pages

  RECOMMENDATIONS
  1. Update top 5 stale high-traffic pages (est. 2 hours)
  2. Create 3 missing runbooks (assign to team leads)
  3. Fix 8 broken links (automated fix available)
---

# Wiki Management

Organize and maintain team wikis with structure templates, stale content detection, and search optimization.

**Integrations:** Notion, Google Workspace

## When to Use

- The team wiki needs an audit or reorganization
- Stale or outdated documentation is a problem
- The user mentions "wiki", "documentation audit", or "knowledge base cleanup"

## Steps

### Step 1: Audit Content

Scan all pages for staleness, broken links, and missing sections.

### Step 2: Identify Gaps

Find topics that should be documented but aren't.

### Step 3: Organize Structure

Apply consistent templates and navigation hierarchy.

### Step 4: Set Maintenance Schedule

Configure review reminders for content owners.

## Output

Deliver:
- Wiki audit report with stale and missing content
- Reorganization plan
- Content owner assignments and review schedule
