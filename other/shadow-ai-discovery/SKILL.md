---
name: shadow-ai-discovery
displayName: Shadow AI Discovery
tagline: Identify unapproved AI tools being used across your org and create a remediation plan.
description: |
  Scans your GitHub repositories, Slack workspace, and SSO logs to detect
  unauthorized AI tool usage. Classifies each finding by risk level and data
  exposure, then generates a prioritized remediation plan with actions ranging
  from approve-with-controls to block-and-notify. Includes communication
  templates for affected users.
department:
  - Security & Compliance
  - Cloud Security
use_cases:
  - Compliance Audit
  - Incident Response
  - Threat Modeling
tools_required:
  - Slack MCP
  - GitHub MCP
agents_compatible:
  - Claude / Claude Code
  - Cursor
  - Windsurf
  - ChatGPT
  - GitHub Copilot
  - Any MCP-compatible agent
author: Webrix
verified: true
updatedAt: 2026-02-24
version: 1.0.0
exampleInput: |
  Approved tools: GitHub Copilot, ChatGPT Enterprise
  Organization: 300 employees, 60 repositories on GitHub
  Slack workspace: 45 channels, 120 installed apps
  Concerns: Developers may be using personal AI accounts with company code
exampleOutput: |
  Shadow AI Discovery Report — February 2026

  SUMMARY: Found 7 unapproved AI tools across 4 departments

  FINDINGS
  | Tool              | Users | Risk   | Data Exposure  | Action       |
  |-------------------|-------|--------|----------------|--------------|
  | Claude (personal) | 12    | High   | Source code     | Replace      |
  | Cursor (free)     | 8     | Medium | Internal code   | Approve+SSO  |
  | Phind             | 5     | Medium | Code snippets   | Evaluate     |
  | ChatGPT (free)    | 15    | High   | Internal docs   | Block        |
  | Codeium           | 3     | Low    | Public code     | Approve      |
  | TabNine           | 2     | Low    | Local only      | Approve      |
  | Custom GPT bot    | 1     | High   | PII in prompts  | Block+Review |

  GitHub scan: Found .cursor/ in 8 repos, .cline/ in 2 repos
  Slack scan: 3 unauthorized AI bot integrations detected

  REMEDIATION PLAN
  - Immediate: Block ChatGPT free, notify 15 users with approved alternatives
  - This week: Onboard 8 Cursor users to enterprise plan with SSO
  - This month: Evaluate Phind and Codeium for approved catalog
---

# Shadow AI Discovery

Identify unapproved AI tools being used across your organization and create a remediation plan.

**Integrations:** Slack, GitHub

## When to Use

- The user wants to find unapproved AI tools being used in their organization
- Security teams need to audit for "shadow AI" usage
- The user mentions "shadow AI", "unapproved tools", "AI audit", or "unauthorized AI usage"
- Compliance requires an inventory of all AI tools in use

## Steps

### Step 1: Define the Approved Tool List

Ask the user for their list of approved AI tools. If they don't have one, help them create a baseline:

| Category | Common Approved Tools |
|----------|----------------------|
| Code Generation | GitHub Copilot, Cursor, Cline |
| Chat Assistants | ChatGPT Team/Enterprise, Claude, Gemini |
| Code Review | CodeRabbit, Sourcery |
| Documentation | Mintlify, Readme.com |
| Testing | Testim, Mabl |

### Step 2: Scan for Shadow AI Indicators

Guide the user through these detection methods:

**GitHub/GitLab Repository Scan:**
- Search for AI tool configuration files: `.cursorrules`, `.github/copilot`, `.cline/`, `.claude/`, `.openai/`, `.cursor/`
- Search for AI-related dependencies in `package.json`, `requirements.txt`, `Gemfile`
- Search for AI API keys in code (patterns: `sk-`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `HUGGINGFACE_TOKEN`)
- Review `.gitignore` for AI tool patterns being hidden

**Slack Workspace Scan:**
- Search for AI tool bot integrations (ChatGPT, Claude, custom bots)
- Search message history for AI tool mentions and sharing of AI-generated content
- Review installed Slack apps for AI-related integrations
- Check for webhook URLs pointing to AI services

**Network/SSO Indicators:**
- Review SSO logs for OAuth connections to AI services
- Check browser extension inventories for AI tools
- Review DNS logs for AI service domains (api.openai.com, api.anthropic.com, etc.)

### Step 3: Classify Discovered Tools

For each discovered tool, classify:

| Field | Options |
|-------|---------|
| **Risk Level** | Low, Medium, High, Critical |
| **Data Exposure** | None, Internal Only, Confidential, PII/PHI |
| **User Count** | Estimated number of users |
| **Business Value** | Low, Medium, High |
| **Compliance Impact** | None, Minor, Major, Blocking |

### Step 4: Generate Remediation Plan

For each unapproved tool, recommend one of:

1. **Approve** — Tool is low-risk, add to approved list with usage guidelines
2. **Replace** — Redirect users to an approved alternative with similar capabilities
3. **Restrict** — Allow with conditions (e.g., specific teams only, no sensitive data)
4. **Block** — High-risk tool, block access and notify users with alternatives

### Step 5: Create Reports

Generate:

- **Executive Summary** — Total shadow AI tools found, risk distribution, top recommendations
- **Detailed Inventory** — Spreadsheet of all discovered tools with classification
- **Remediation Tracker** — Jira tickets or task list with owners and deadlines
- **Communication Template** — Message to affected users about policy and approved alternatives

## Output

Deliver:
- Shadow AI inventory spreadsheet
- Risk-classified remediation plan
- Communication templates for affected users
- Updated approved tools list recommendation
