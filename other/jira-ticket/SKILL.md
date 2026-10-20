---
name: jira-ticket
description: Draft a copy-pasteable JIRA ticket from the current discussion. Use when asked to write, draft, or prepare a ticket for filing.
---

# JIRA ticket

Turn the discussion into a JIRA ticket a teammate can understand without reading the conversation. Propose only; do not create the ticket.

## Content

Describe the problem, intended outcome, and any agreed approach. Make clear what completing the work means.

Let the work determine the structure and level of detail. Include acceptance criteria, scope boundaries, open questions, or relevant examples when they clarify the work. A simple change may need only a paragraph; do not add sections merely to fill a template.

Distinguish agreed decisions from suggestions and open questions. When the intended work is an investigation, describe what it should resolve.

Stay within the discussed scope. Do not invent requirements, commitments, assignees, or priorities. Include material assumptions and uncertainty in the description. Read code only to confirm a path or name you cite.

## Required details

Include these details in every ticket, in addition to the description of the work.

- Include a T-shirt size in the description. Do not include story points.
- End the description with an `AI-assisted by:` line naming the drafting agent.

## Output

Put the title and description in separate fenced code blocks, using a `markdown` fence for the description.
