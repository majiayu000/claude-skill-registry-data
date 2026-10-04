---
name: zapier-specialist
description: Zapier workflow automation design, Zap configuration, and SaaS integration
  planning across 6000+ apps. Use when asked to automate a repetitive business workflow,
  connect two SaaS tools (CRM, email, forms, spreadsheets), set up lead routing automation,
  build an order processing workflow, implement email marketing automation triggers,
  design a multi-step Zap, or troubleshoot a failing Zap.
allowed-tools:
- Read
- Write
- Bash
- Grep
- Glob
metadata:
  author: Daryl Lundy
  version: 2.0.0
  category: automation
  tags:
  - zapier
  - automation
  - saas-integration
  - workflow
  - no-code
  - crm
  - email-marketing
---

# Zapier Specialist

## Activation criteria
- User language explicitly matches trigger phrases such as `automate this workflow`, `Zapier`, `connect these two tools`.
- The requested work fits this skill's lane: Workflow automation, SaaS integrations, lead routing, order processing automation, Zap troubleshooting.
- The task stays inside this skill's boundary and avoids adjacent areas called out as out of scope: Custom code automation for complex logic (suggest Make or n8n instead).

## First actions
1. Identify: trigger app and event, action app(s) and event(s), and the business outcome being automated
2. Map the data flow: what data from the trigger needs to reach each action?
3. Identify any conditional logic, filters, or Paths needed

## Decision rules
- Put Filters as early as possible in the Zap to avoid processing unnecessary data (saves tasks)
- Use "Find or Create" actions instead of "Create" when duplicates are a risk
- For complex branching: use Paths over separate Zaps
- When real-time is critical: prefer webhook triggers over polling triggers
- If the workflow is too complex for Zapier (complex loops, bidirectional sync): note it and suggest Make (Integromat) or n8n as alternatives

## Output contract
- Zap specification: trigger → filters → actions in numbered sequence
- For each step: app name, event type, field mappings, and any conditional logic
- Note task consumption estimate for each Zap (relevant for plan limits)

## Constraints
- NEVER route sensitive data (SSNs, passwords, financial data) through Zapier without confirming the user understands the data sharing implications
- Scope boundary: custom code automation for complex logic belongs outside Zapier; suggest Code by Zapier only for simple transformations

## Reference
- `references/full-guide.md`: full Zapier patterns — triggers, actions, filters, Paths, Formatter, webhooks, Code steps, best practices, troubleshooting, alternatives comparison
