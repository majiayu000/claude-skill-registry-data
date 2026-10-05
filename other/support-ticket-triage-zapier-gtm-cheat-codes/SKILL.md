---
name: support-ticket-triage
description: Triage support tickets by pulling helpdesk context, searching issue trackers and knowledge bases in parallel, classifying the issue, and giving reps a recommended next action.
---

# Support Ticket Triage Agent

Use this skill when a support rep needs fast, source-backed context before replying to a customer ticket.

## Workflow

1. Accept a ticket URL, ticket ID, or pasted customer message.
2. Pull ticket context through Zapier MCP: subject, body, comments, requester, tags, priority, custom fields, status, and assignee.
3. Search connected systems in parallel:
   - Defect tracker for open or recently fixed bugs.
   - Feature backlog for known gaps or expected behavior.
   - Helpdesk history for similar tickets and resolutions.
   - Knowledge base for docs, runbooks, and troubleshooting steps.
4. Classify the issue into exactly one category: known defect, feature gap, configuration issue, performance issue, or novel issue.
5. Return a concise triage summary with evidence, relevant links, and a recommended next action.
6. Draft a customer-facing reply only when the rep asks.

## Zapier MCP And SDK Role

- Use Zapier MCP to read helpdesk tickets, comments, requester details, issue tracker records, feature backlog items, knowledge-base docs, and optional CRM or account context.
- Use Zapier SDK only if the workflow becomes a durable automation, such as tagging, escalation packet creation, similar-ticket linking, SLA warnings, follow-up reminders, regression alerts, or triage digests.
- Keep customer replies, ticket updates, tags, escalation packets, and broad alerts human-approved.

## Output Format

- Ticket category
- Best matching evidence
- Related docs or similar tickets
- Recommended next action
- Optional customer reply draft
- Open questions or escalation gaps

## Guardrails

- Do not auto-reply to customers.
- Do not expose internal defect IDs, sprint numbers, or engineering-only notes in customer-facing drafts.
- Do not query observability tools unless the rep provides a concrete signal such as a trace ID, timestamp, error code, or request ID.
- Do not invent matches, timelines, fixes, or customer-impact claims.
- Do not store ticket data beyond the working session unless the approved workflow explicitly requires it.

## Inspired By

This skill is generalized from a real implementation by [Corey Smith at ClickUp](https://zapier.com/customer-stories/clickup). Corey built an MCP-powered support triage agent that pulls Zendesk context, searches defect tracking and feature backlog systems in parallel, classifies the ticket, and gives reps structured context before they type a reply.
