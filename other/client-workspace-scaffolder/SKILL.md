---
name: client-workspace-scaffolder
description: Scaffold a complete client project folder from your own reusable structure template, with a filled-in brief file and feedback log. Never overwrites existing work. Use when the user says "new client", "set up a client folder", "onboard this client", or "create a project workspace for".
---

# Client Workspace Scaffolder

Every client engagement starts with the same folder dance. This skill does it once, correctly, from a structure you define one time and reuse forever.

## Step 0: Load the workspace template (once)

Look for a `client-workspace.template.md` file in the project root. If it does not exist, ask the user how they structure a client project, then offer to save the answers. The template defines:

```
CLIENTS_ROOT    The parent folder where client folders live
FOLDERS         The subfolders every client gets, e.g. Assets, Context, Strategy, Website
BRIEF_TEMPLATE  The markdown skeleton for the brief file (status, scope checklist, references, billing section)
EXTRA_FILES     Other starter files, e.g. Feedback.md with a feedback-round table
```

A sensible default when the user has no opinion yet:

```
CLIENTS_ROOT: ./Clients
FOLDERS: 01_Assets, 02_Context, Strategy
BRIEF_TEMPLATE: title, Status (Active/Completed/On hold), Started date,
  Brief paragraph, Scope checklist, References, Files note, Billing section
EXTRA_FILES: Feedback.md with a Date/Round/Notes table
```

## Step 1: Collect the essentials

From the user's message: client name (required) and project scope. Anything else they volunteer (industry, contact, deadline) goes into the brief. Ask at most one short round of questions.

## Step 2: Check for collisions

List CLIENTS_ROOT first. If a folder with the same or a very similar name exists, stop and ask whether to use it or create a variant. Never overwrite an existing client folder or brief.

## Step 3: Scaffold

Create the folder tree from FOLDERS, write the brief from BRIEF_TEMPLATE with everything known filled in (status Active, started today, scope boxes ticked), and create EXTRA_FILES. Leave unknowns as visible placeholders rather than fabricated values. Empty folders are correct; do not create filler files inside them.

## Step 4: Report

Show the created tree and the brief contents. Mention the natural next step if the brief has gaps (a discovery conversation or intake questionnaire).

## Rules

- Never overwrite anything that exists.
- Never invent client details to fill template fields.
- No em dashes in any generated content.

## Output

A ready client folder under CLIENTS_ROOT with a filled brief, a feedback log, and the standard subfolders.
