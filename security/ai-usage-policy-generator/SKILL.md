---
name: ai-usage-policy-generator
displayName: AI Usage Policy Generator
tagline: Generate a tailored AI acceptable use policy for your organization based on industry, size, and risk tolerance.
description: |
  Produces a comprehensive, ready-to-review AI acceptable use policy document
  customized to your industry, regulatory requirements, and risk appetite. Covers
  data classification, approved tools, prohibited uses, IP ownership, incident
  response, and training requirements. Outputs a formatted Google Doc with
  table of contents and employee acknowledgment page.
department:
  - Security & Compliance
use_cases:
  - Compliance Audit
  - Documentation
tools_required:
  - Google Drive MCP
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
  Industry: Healthcare (HIPAA regulated)
  Organization size: 500 employees, 80 engineers
  Risk tolerance: Conservative
  AI tools in scope: Code generation, chat assistants
exampleOutput: |
  AI Acceptable Use Policy v1.0 — [Company Name]

  1. PURPOSE & SCOPE
  This policy governs the use of AI tools by all employees. It applies to code
  generation tools (GitHub Copilot, Cursor) and chat assistants (ChatGPT, Claude).

  2. DATA CLASSIFICATION
  - PROHIBITED: PHI, patient data, SSNs, or any HIPAA-protected information
  - RESTRICTED: Internal source code containing business logic
  - PERMITTED: Public documentation, open-source code, general questions

  3. APPROVED TOOLS
  - Tier 1 (Pre-approved): GitHub Copilot Enterprise (with SSO)
  - Tier 2 (Requires approval): Claude Team, ChatGPT Enterprise
  - All others: Requires security review before use

  Generated: Google Doc (12 pages) with Table of Contents, all 10 policy sections,
  appendix with tool-specific guidelines, and signature page template
---

# AI Usage Policy Generator

Generate a tailored AI acceptable use policy for your organization based on industry, size, and risk tolerance.

**Integrations:** Google Drive

## When to Use

- The user needs to create an AI acceptable use policy
- An organization is adopting AI tools and needs formal guidelines
- The user mentions "AI policy", "acceptable use", or "usage guidelines"
- Legal or compliance teams request documentation for AI tool usage

## Steps

### Step 1: Gather Policy Inputs

Ask the user for:

1. **Industry** (finance, healthcare, tech, education, government, etc.)
2. **Organization size** (startup, mid-market, enterprise)
3. **Risk tolerance** (conservative, moderate, progressive)
4. **Regulatory requirements** (SOC2, HIPAA, GDPR, FedRAMP, PCI-DSS, none)
5. **AI tool categories in scope** (code generation, chat assistants, image generation, data analysis)

### Step 2: Generate Policy Sections

Create a comprehensive policy document with these sections:

| Section | Content |
|---------|---------|
| **Purpose & Scope** | Why the policy exists, who it applies to, what tools it covers |
| **Approved Tools** | Categories of approved AI tools, approval process for new tools |
| **Data Classification** | What data can/cannot be shared with AI tools by classification level |
| **Prohibited Uses** | Specific use cases that are not allowed (e.g., PII in prompts, code with trade secrets) |
| **Security Requirements** | Authentication, encryption, data retention, logging requirements |
| **Intellectual Property** | Ownership of AI-generated content, license compliance, attribution |
| **Compliance & Audit** | How usage is monitored, audit frequency, reporting requirements |
| **Incident Response** | What to do if data is accidentally shared, escalation path |
| **Training Requirements** | Mandatory training before AI tool access, ongoing education |
| **Policy Review Cadence** | How often the policy is reviewed and updated |

### Step 3: Customize by Risk Profile

Adjust the policy strictness based on risk tolerance:

- **Conservative**: Allowlist-only tools, mandatory review of all AI outputs, no external AI APIs, quarterly audits
- **Moderate**: Approved tool catalog with self-service request process, spot-check reviews, semi-annual audits
- **Progressive**: Default-allow with blocklist, trust-but-verify approach, annual audits with continuous monitoring

### Step 4: Generate Google Drive Document

Create a well-formatted Google Doc with:

- Company logo placeholder and document metadata (version, date, owner)
- Table of contents with hyperlinks
- Each section with clear headings and actionable language
- Appendix with tool-specific guidelines
- Signature/acknowledgment page template

### Step 5: Provide Rollout Guidance

Recommend a rollout plan:

1. **Legal review** — Have legal/compliance review the draft
2. **Stakeholder feedback** — Share with engineering leads and security team
3. **Employee communication** — Draft an announcement email
4. **Training** — Create or recommend training materials
5. **Acknowledgment** — Process for employees to sign/acknowledge the policy
