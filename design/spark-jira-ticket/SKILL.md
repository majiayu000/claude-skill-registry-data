---
name: spark-jira-ticket
description: Create a new iOS Spark Jira ticket (project LBCSPARK) with the Atlassian MCP, assigned to and reported by the current user, with the "iOS" and "Spark" labels.
---

# Spark Jira Ticket Skill

## Overview

This skill creates a new Jira ticket for the iOS Spark design system using the **Atlassian MCP** (`mcp__atlassian__*` tools).

## Configuration

| Field | Value |
|---|---|
| Cloud ID | `2bc5cf31-f7d4-47ef-b903-21d7ae568316` (`lbc-lbc.atlassian.net`) |
| Project | `LBCSPARK` (LBC Foundations Spark DS) |
| Labels (Étiquettes) | `iOS`, `Spark` |
| Assignee (Personne assignée) | the current user |
| Reporter (Rapporteur) | the current user |

## Steps

- [ ] Ask the user (with `AskUserQuestion` when possible, otherwise in plain text):
  - **Title** *(required)*
  - **Description** *(optional)*
  - **Figma link** *(optional)*
  - **Priority** *(required)*: fetch the allowed values from the project metadata (see below) and propose them.
  - **Issue type**: default to `Tâche`. Other values: `Story`, `Bug`, `Epic`.
- [ ] Get the current user account id with `mcp__atlassian__atlassianUserInfo` (`account_id`).
- [ ] Get the fields metadata with `mcp__atlassian__getJiraIssueTypeMetaWithFields` (project `LBCSPARK`, chosen issue type) to check the `priority` allowed values and that `reporter` / `labels` are settable.
- [ ] Build the description (Markdown):
  ```markdown
  {description}

  **Figma**: {figma link}
  ```
  - Omit the description part if not provided.
  - Omit the Figma line if not provided.
- [ ] Show a summary of the ticket (title, type, priority, description, labels, assignee, reporter) and ask the user to confirm before creating it.
- [ ] Create the ticket with `mcp__atlassian__createJiraIssue`:
  - `cloudId`: `2bc5cf31-f7d4-47ef-b903-21d7ae568316`
  - `projectKey`: `LBCSPARK`
  - `issueTypeName`: the chosen issue type
  - `summary`: the title
  - `description`: the built description
  - `assignee_account_id`: the current user account id
  - `additional_fields`:
    ```json
    {
      "labels": ["iOS", "Spark"],
      "priority": { "name": "{priority}" },
      "reporter": { "id": "{account id}" }
    }
    ```
- [ ] If the reporter cannot be set at creation (field not on the create screen), the reporter is by default the creator (the current user): retry without `reporter`.
- [ ] Return the ticket key and URL: `https://lbc-lbc.atlassian.net/browse/{KEY}`.

## Rules

- Never create the ticket without the user confirmation.
- Do not mention *Claude* in the ticket.
