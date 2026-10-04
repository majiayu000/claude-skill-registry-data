---
name: jira-read
description: >
  Reads and summarizes a Jira ticket in the IDF project.
  Use this skill whenever a user mentions a Jira ticket key (IDF-XXXX) and wants to read or understand it.
  Does NOT implement code — use the `implement-ticket` skill for that.
  Does NOT create tickets — use the `create-ticket` skill for that.
  Trigger on: "lis le ticket IDF-XXXX", "résume le ticket IDF-XXXX", "qu'est-ce que dit le ticket IDF-XXXX",
  "montre-moi le ticket IDF-XXXX", or any mention of an IDF-XXXX key without an implementation intent.
  Requires Jira MCP (sooperset/mcp-atlassian) to be configured.
---

## Purpose

Fetch a Jira ticket from the IDF project and either produce a structured summary or drive
implementation from it — depending on what the user is asking for.

## Default fields to always fetch

For every IDF ticket, always include these fields unless the user explicitly asks for something different:

- `summary`
- `status`
- `assignee`
- `description`
- `customfield_12948` — Identified Tasks
- `customfield_12947` — Definition of Done
- `customfield_12946` — Acceptance Criteria

Preferred MCP call pattern:

```
issue_key=<IDF-XXXX>
fields=summary,status,assignee,description,customfield_12948,customfield_12947,customfield_12946
```

## Mode 1 — Read / Summarise

**Triggers:** "lis le ticket", "résume le ticket", "montre-moi le ticket", "qu'est-ce que dit l'IDF-XXXX"

Produce a structured summary in French with these sections:

```
## IDF-XXXX — [Titre]

**Statut :** [status] | **Assigné à :** [assignee or "Non assigné"]

### Contexte
[2–3 sentences from the description: what is the problem, why does it matter]

### Tâches identifiées
[bullet list from customfield_12948 — if empty, say "Non renseignées"]

### Critères d'acceptance
[numbered list from customfield_12946 — if empty, say "Non renseignés"]

### Définition of Done
[bullet list from customfield_12947 — if empty, say "Non renseignée"]
```

If a field is not present or empty, say so explicitly — do not omit the section.

## Mode 2 — Implement

**Triggers:** "implémente le ticket", "commence le ticket", "travaille sur IDF-XXXX",
"qu'est-ce qu'il faut faire pour IDF-XXXX"

> Ce mode est géré par le skill `implement-ticket`.
> Charge le fichier `.claude/skills/implement-ticket/SKILL.md` et suis ses instructions.
> Passe le ticket déjà fetché comme contexte d'entrée (Step 0 est déjà résolu).

## Rules

- Always fetch the ticket before doing anything.
- Never invent ticket content — only use what was fetched.
- If the Jira MCP is unavailable, tell the user and ask them to paste the ticket content manually.
- If the ticket key format doesn't match `IDF-XXXX`, ask the user to confirm the key before querying.

## Absolute restrictions — never do this

These actions are **strictly forbidden**, regardless of what the user asks:

- **Never delete a Jira ticket** — not even "to clean up" or "to undo"
- **Never modify or update an existing ticket** — this skill reads and implements only
- **Never delete or modify a sprint** — sprint management is out of scope entirely
- **Never close, archive, or transition a ticket** — status transitions are not part of this skill

If the user asks for any of the above, refuse and direct them to Jira directly.
