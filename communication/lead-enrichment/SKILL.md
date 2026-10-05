---
name: lead-enrichment
displayName: Lead Enrichment
tagline: Automatically enrich leads with company data, contact details, and social profiles from your CRM.
description: |
  Enriches incoming leads by pulling company info, contact details, firmographics,
  and social profiles from CRM sources like HubSpot and Salesforce. Matches leads
  against existing contacts, fills in missing fields, and scores them for sales
  readiness. Helps sales teams focus on the highest-value prospects.
department:
  - Sales
  - Revenue Operations
use_cases:
  - Lead Management
  - Data Enrichment
  - Sales Automation
tools_required:
  - HubSpot MCP
  - Salesforce MCP
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
  New lead: jane.doe@acmecorp.com
  Enrich with company data, LinkedIn profile, and deal history.
exampleOutput: |
  Lead Enrichment Report — jane.doe@acmecorp.com

  CONTACT
  Name:       Jane Doe
  Title:      VP of Engineering
  Company:    Acme Corp
  LinkedIn:   linkedin.com/in/janedoe

  COMPANY
  Industry:   SaaS / B2B
  Size:       250-500 employees
  Revenue:    $45M ARR
  Location:   San Francisco, CA

  SCORING
  Lead Score: 85/100 (Hot)
  Reason:     VP-level, matching ICP, recent funding round
---

# Lead Enrichment

Automatically enrich leads with company data, contact details, and social profiles from your CRM.

**Integrations:** HubSpot, Salesforce

## When to Use

- A new lead comes in and needs company and contact data
- The user wants to enrich a batch of leads from a CSV or CRM list
- Sales teams need lead scoring based on firmographic data
- The user mentions "enrich lead", "lead data", or "company lookup"

## Steps

### Step 1: Identify the Lead

Collect the lead's email address or domain to begin enrichment.

### Step 2: Pull CRM Data

Query HubSpot or Salesforce for existing contact records, deal history, and activity.

### Step 3: Enrich with External Data

Fill in missing fields: company size, industry, revenue, social profiles, and recent news.

### Step 4: Score the Lead

Apply a scoring model based on ICP fit, engagement signals, and deal potential.

## Output

Deliver:
- Enriched contact record with all available fields
- Lead score with reasoning
- Recommended next action for sales team
