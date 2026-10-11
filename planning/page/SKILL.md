---
name: page
description: 'Create, list, get, or update a Plane page (project or workspace scope) Arguments: <action> [scope] [project] [args...].'
---

# Page

Manage Plane Pages — long-form documents attached to a project or to the workspace. Delegates rendering rules to the `pages-publishing` skill and tool resolution to `connector-bootstrap`.

## Arguments

Format: `<action> [scope] [project] [args...]`

- `action`: `create` | `list` | `get` | `update` | `archive` | `delete`
- `scope`: `project` (default) | `workspace`
- `project`: project name or identifier (required when `scope=project`)
- Remaining: title, content source (`--from-file`, `--from-template`, inline body), `--page-id` for `get`/`update`

Parse from `"$ARGUMENTS"`.

## Process

1. **Bootstrap connector** — consult `connector-bootstrap`. Probe `ToolSearch` for the Plane resource tools `page` and `project` (`mcp__<server>__page` takes every page action below).
2. **Resolve scope**:
   - `project` → `project(action=list)` → `project_id`
   - `workspace` → no project lookup; omit `project_id` from every `page` call
3. **Route by action**:
   - `create` → gather `name` and `description_html`. Sources of body, in order of preference:
     - `--from-file <path>` → read file, convert markdown→HTML if needed
     - `--from-template <name>` → use a template from `pages-publishing` skill (`sprint-report`, `retro`, `release-notes`, `roadmap`, `milestone-update`, `meeting-notes`, `decision-log`, `spec`, `runbook`, `blank`)
     - inline body in arguments → wrap in `<p>` paragraphs
     - none → ask the user once for the body
     Call `page(action=create, project_id?, name, description_html)`. A page's parent is fixed at creation: pass `parent_id` (nest under a page) or `collection_id` (file into a collection), never both.
   - `list` → `page(action=list, project_id?)` (follow `next_cursor`); each entry reports its `parent_id` and `collection_id`.
   - `get` → `page(action=retrieve, project_id?, page_id)`. Render the HTML back as readable markdown for the terminal.
   - `update` → `page(action=retrieve, ...)` first, edit the full HTML, then `page(action=update, project_id?, page_id, description_html, name?)`: `description_html` replaces the whole body, so send the complete edited page, not a fragment. A locked or archived page is refused.
   - `archive` → `page(action=archive, project_id?, page_id)` (hides it; `archive=false` restores it).
   - `delete` → **destructive**: show the page, ask for explicit confirmation, `page(action=archive)` it first (delete is refused for a page that is not archived), then `page(action=delete, project_id?, page_id)`.
4. **Confirm** — print the page name, ID, and URL. Suggest where to link it (cycle description, Slack, README).

## Examples

```
/page create project "TaskFlow" "Q2 Engineering Plan" --from-file ./plan.md
/page create project "TaskFlow" "Sprint 14 Report" --from-template sprint-report
/page create workspace "Team Handbook"
/page get project "TaskFlow" --page-id 7c8e...
/page update project "TaskFlow" --page-id 7c8e... --from-file ./plan-v2.md
/page list project "TaskFlow"
```

## Best Practices

- Project pages live with the project they document — use them for sprint reports, retros, decision logs, runbooks.
- Workspace pages are for cross-project content — handbooks, OKRs, hiring loops.
- Always include a "Last updated" line at the top — Plane does not surface freshness in the sidebar.
- Prefer **editing** an existing page (e.g. roadmap) over recreating it; recreating breaks links.