---
name: project-repo-management
category: pm
description: Use when organizing the workspace - create/rename initiative projects and link repositories to them directly, since these are factual actions needing no analiz or approval
---
# Project & Repository Management

## Overview

You own workspace organization, not just the board. Organize actions are factual and reversible — act directly and confirm, don't route them through analiz or approval.

**Core principle:** Organize requests are direct actions: call the tool, confirm with real names.

## The tools

| Tool | Use |
|------|-----|
| `create_project(name, description)` | Open a new initiative project when the stakeholder starts a new product/initiative or asks to group work |
| `update_project(project_id, name?, description?)` | Rename or edit a project's description (empty fields stay unchanged); get the id from `list_projects` first |
| `set_repository_projects(repository_id, project_ids)` | Link a repo to one or more projects (replaces existing links; empty list unlinks); get ids from `list_repositories` and `list_projects` |

## Rules

- For a factual/organize request, **act directly** — no analiz, no approval. Call the tool, then confirm with real names ("Created the Alpha project and linked the X repo to it.").
- You **cannot** create a code repository's filesystem directory. If a brand-new repo is needed, tell the stakeholder to open it from the Repositories screen, then link it with `set_repository_projects`.

## Worked Example

Stakeholder: "Open a new 'Reporting' initiative and link the web repo to it."
1. `create_project("Reporting", "...")` → get the new id.
2. `list_repositories` → find the web repo's id.
3. `set_repository_projects(webRepoId, [reportingId])`.
4. Confirm: "Opened the Reporting project and linked the web repo to it."

## Common Mistakes

- Opening an analiz task for a rename.
- Asking approval for a factual organize action.
- Claiming you can create the repo directory (you can't — direct the stakeholder to the Repositories screen).

## Red Flags

- An analiz task titled "create a project."
- A `set_repository_projects` call with ids you guessed instead of looked up.
