---
name: doc-automation
displayName: Document Automation
tagline: Automate document creation from templates with data merging and approval workflows.
description: |
  Automates document generation using templates and data sources. Creates
  proposals, contracts, reports, and SOPs by merging data from Notion,
  Google Docs, or databases. Supports approval workflows, version control,
  and automated distribution to stakeholders.
department:
  - Operations
  - Legal
  - Sales
use_cases:
  - Document Generation
  - Template Automation
  - Workflow Automation
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
  Generate a client proposal for Acme Corp using our standard template.
  Project: Platform Migration, Budget: $150K, Timeline: 3 months.
exampleOutput: |
  Document Generated — Client Proposal

  DOCUMENT: Acme Corp Platform Migration Proposal
  Template:   Standard Client Proposal v3.2
  Pages:      12

  MERGED DATA
  Client:       Acme Corp
  Project:      Platform Migration
  Budget:       $150,000
  Timeline:     3 months (July - September 2026)
  Team Size:    4 engineers + 1 PM

  SECTIONS
  1. Executive Summary (auto-generated)
  2. Scope of Work (from template + project details)
  3. Timeline & Milestones (3 phases)
  4. Team & Resources
  5. Pricing Breakdown
  6. Terms & Conditions (standard)

  STATUS: Draft created in Google Docs
  NEXT: Sent to @sales-lead for review and approval
---

# Document Automation

Automate document creation from templates with data merging and approval workflows.

**Integrations:** Notion, Google Workspace

## When to Use

- The user needs to generate documents from templates
- Repetitive document creation should be automated
- The user mentions "document automation", "proposal generator", or "template merge"

## Steps

### Step 1: Select Template

Choose the appropriate document template for the use case.

### Step 2: Merge Data

Fill template variables with project-specific data.

### Step 3: Generate Document

Create the final document with formatted content.

### Step 4: Route for Approval

Send to reviewers and track approval status.

## Output

Deliver:
- Generated document with merged data
- Approval workflow initiated
- Distribution to stakeholders
