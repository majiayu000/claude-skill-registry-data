---
name: ai-adoption-readiness-assessment
displayName: AI Adoption Readiness Assessment
tagline: Evaluate your org's AI readiness across security, tooling, culture, and governance dimensions.
description: |
  A structured assessment framework that scores your organization across five critical
  dimensions of AI readiness. Produces an actionable scorecard with prioritized
  recommendations, a detailed gap analysis spreadsheet, and optional Jira tickets
  to track remediation efforts.
department:
  - Engineering
  - Security & Compliance
  - AI Enablement Leaders
use_cases:
  - Compliance Audit
  - Documentation
  - Onboarding
tools_required:
  - Google Sheets MCP
  - Jira MCP
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
  We're a 200-person fintech company with 40 engineers.
  Some developers use GitHub Copilot informally but we have no official AI policy.
  We're SOC2 compliant and handle PII. Leadership wants to roll out AI tools company-wide.
exampleOutput: |
  Dimension                  | Score | Status
  ---------------------------|-------|--------
  Security & Compliance      | 3/5   | Needs Work
  Tooling & Infrastructure   | 2/5   | Critical Gap
  Culture & Change Mgmt      | 4/5   | Ready
  Governance & Policy        | 1/5   | Critical Gap
  Measurement & ROI          | 2/5   | Critical Gap
  ---------------------------|-------|--------
  Overall Readiness          | 12/25 | Partially Ready

  Top 3 Recommendations:
  1. [Quick Win] Draft an AI acceptable use policy covering data classification
  2. [Medium-Term] Establish an approved AI tool catalog with SSO integration
  3. [Strategic] Create an AI governance board with quarterly review cadence

  Generated: Google Sheet with 3 tabs (Summary Dashboard, Detailed Assessment, Action Plan)
  Created: Jira Epic "AI Adoption Readiness" with 8 stories for identified gaps
---

# AI Adoption Readiness Assessment

Evaluate your organization's AI readiness across security, tooling, culture, and governance dimensions.

**Integrations:** Google Sheets, Jira

## When to Use

- The user wants to assess their organization's AI readiness
- A team is planning to roll out AI tools and needs a baseline evaluation
- Leadership asks for a structured view of gaps before AI adoption
- The user mentions "readiness assessment", "AI maturity", or "adoption scorecard"

## Steps

### Step 1: Gather Organization Context

Ask the user for:

1. **Industry** (e.g., finance, healthcare, tech, manufacturing)
2. **Organization size** (number of employees, engineering team size)
3. **Current AI tool usage** (any tools already in use, even informally)
4. **Existing security policies** (data classification, access controls)

### Step 2: Assess Across Dimensions

Evaluate readiness across these five dimensions, scoring each from 1 (not ready) to 5 (fully ready):

| Dimension | What to Evaluate |
|-----------|-----------------|
| **Security & Compliance** | Data classification policies, access controls, audit logging, regulatory requirements (SOC2, HIPAA, GDPR) |
| **Tooling & Infrastructure** | Developer environment standardization, SSO/IdP integration, network policies, approved tool catalog |
| **Culture & Change Management** | Leadership buy-in, developer sentiment, training programs, experimentation culture |
| **Governance & Policy** | Acceptable use policies, approval workflows, risk assessment frameworks, incident response plans |
| **Measurement & ROI** | Productivity metrics baseline, cost tracking, success criteria definition, feedback loops |

### Step 3: Generate the Scorecard

Create a Google Sheets spreadsheet with:

- **Sheet 1: Summary Dashboard** — Radar chart of the 5 dimensions, overall score, and top 3 recommendations
- **Sheet 2: Detailed Assessment** — Each dimension broken into sub-criteria with individual scores, evidence, and notes
- **Sheet 3: Action Plan** — Prioritized list of gaps to address, owner assignment columns, and target dates

### Step 4: Create Jira Tickets (Optional)

If the user uses Jira, offer to create:

- An Epic for "AI Adoption Readiness"
- Stories for each gap identified in the assessment
- Acceptance criteria based on moving from current score to target score

### Step 5: Provide Recommendations

Based on the scores, provide:

1. **Quick wins** — Items that can be addressed in 1-2 weeks
2. **Medium-term initiatives** — Items requiring 1-3 months
3. **Strategic investments** — Items requiring organizational change (3-6 months)

## Output Format

Present the summary as a table:

```
Dimension                  | Score | Status
---------------------------|-------|--------
Security & Compliance      | X/5   | [Ready/Needs Work/Critical Gap]
Tooling & Infrastructure   | X/5   | [Ready/Needs Work/Critical Gap]
Culture & Change Mgmt      | X/5   | [Ready/Needs Work/Critical Gap]
Governance & Policy        | X/5   | [Ready/Needs Work/Critical Gap]
Measurement & ROI          | X/5   | [Ready/Needs Work/Critical Gap]
---------------------------|-------|--------
Overall Readiness          | X/25  | [Ready/Partially Ready/Not Ready]
```
