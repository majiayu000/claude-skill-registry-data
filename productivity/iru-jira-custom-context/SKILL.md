---
name: iru-jira-custom-context
description: "Invoked as `Skill({skill: \"iru-jira-custom-context\", args: \"<task purpose>\"})` by `iru-create-jira-ticket` (also runnable as `/iru-jira-custom-context`). Customization point for organization-specific Jira context (custom fields, team, customer, environment, classification); ships with one open-ended question and is meant to be edited in place."
model: sonnet
---

# Jira Custom Context

This skill exists purely as a customization point for `iru-create-jira-ticket`. Out of the box it asks one
generic, optional question and returns whatever the user provides. Its real value comes from being extended, in
place, with the specific extra questions or lookups a given organization's Jira workflow actually needs — without
having to touch `iru-create-jira-ticket`'s own logic to do it.

## Purpose

`iru-create-jira-ticket` already asks for the context every ticket needs regardless of organization: the task's
purpose, linked URLs/attached files, related tickets, an optional epic, a due date, and an importance level. Some
organizations need more than that before a ticket is genuinely ready to file — a required custom field, a specific
team or component, a customer/account name, the affected environment, a compliance or security classification,
and so on. Rather than growing `iru-create-jira-ticket` itself with organization-specific questions that wouldn't
apply to every installation of this skill catalog, that skill delegates to this one during its own
context-gathering step, and this skill is the place to add them — one file, edited per repository/organization,
instead of a fork of the whole ticket-creation flow.

## Step 1 — Ask whatever this organization has defined here

If invoked with an argument (the task's stated purpose, normally passed by `iru-create-jira-ticket`), use it to
judge which of this skill's questions are actually relevant to this particular task — skip ones that obviously
don't apply rather than asking every defined question unconditionally every time.

Out of the box, this skill defines no organization-specific questions yet. Ask a single generic, open-ended
question instead, making clear it's entirely optional:

- "Is there any other context this ticket should carry — team/component ownership, a customer or account, an
  affected environment, compliance/security considerations, or anything else specific to how your organization
  tracks Jira tickets?"

## Step 2 — Extending this skill

To add real questions, edit this section directly — don't just grow the generic Step 1 question into a list of
unrelated asks. A typical extension looks like:

- A fixed-choice question via `AskUserQuestion` when the answer is a known, bounded set (e.g. "Which team owns
  this: Payments, Platform, or Growth?").
- An open-ended plain-text question when the answer is free-form (e.g. "Which customer/account reported this, if
  any?").
- An automated lookup instead of (or in addition to) a question, when the context can be derived rather than
  asked — e.g. resolving an internal Confluence page, checking a CMDB, or querying an internal system via a
  connected MCP tool.
- Keep every added question optional unless this organization's Jira project actually enforces the field as
  required. `iru-create-jira-ticket`'s own confirm-and-create step already surfaces a clear error if ticket
  creation fails on a genuinely missing required field, so this skill doesn't need to guess which fields are
  mandatory ahead of time.
- Once real, specific questions replace the generic catch-all from Step 1, narrow or remove it — keep it only for
  whatever your added questions still don't cover, rather than asking both every time.

## Step 3 — Report back

Return the gathered context as plain text back to the caller, structured as a short list of label/value pairs
(e.g. "Team: Payments", "Environment: production") — clear enough that `iru-create-jira-ticket`'s own drafting
step can fold each one in directly, either as its own bullet in the ticket description or, if a matching Jira
field/label/component exists for it, as that field instead of a bare description line. If the user provided
nothing (the catch-all question was declined, or every extended question was skipped as optional), return that
explicitly rather than an empty response, so the caller knows this step ran and simply found nothing to add.
