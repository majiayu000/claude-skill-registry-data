---
name: issue-suggest-component
category: business-product
description: >
  Suggest Jira components for one ticket or sweep a project's open tickets, confirming
  before any modification. Use when the user says "suggest components", "tag components",
  "fix components", "categorize tickets", or invokes /issue-suggest-component.
codex-short-description: "Suggest Jira components for one ticket or sweep a project, confirming before changes"
allowed-tools:
  - Read
  - Write
  - Bash
  - AskUserQuestion
  - mcp__atlassian__discover_tools
  - mcp__atlassian__jira_get_issue
  - mcp__atlassian__jira_get_comments
  - mcp__atlassian__jira_get_changelog
  - mcp__atlassian__jira_get_remote_links
  - mcp__atlassian__jira_search
  - mcp__atlassian__jira_get_project_components
  - mcp__atlassian__jira_update_issue
  - mcp__atlassian__confluence_search
  - mcp__atlassian__confluence_get_page
  - mcp__gitlab-mcp__list_merge_requests
  - mcp__gitlab-mcp__get_merge_request
  - mcp__gitlab-mcp__list_commits
  - mcp__gitlab-mcp__search_project_code
loop-eligible: false

compatibility: claude-code codex opencode
---

# Issue Suggest Component

Suggest a focused set of Jira components for a ticket — adding only what's clearly supported by evidence in the ticket, linked Confluence pages, and related GitLab activity. Confirm every change with the user.

## Two modes

| Trigger | Mode | Behavior |
| --- | --- | --- |
| `/issue-suggest-component PROJ-1234` | **Single** | Deep context gather + suggest + per-change confirm |
| `/issue-suggest-component` (no key) | **Bulk** | Loop highest-key-first, max 250 open tickets in the default project (resolved from memory: `reference_jira_default_project.md`) |
| `/issue-suggest-component ABC` (project key only) | **Bulk** | Same as bulk, override project |

If the input is ambiguous, ask once.

## Suggestion bar (read this first)

**Be conservative.** Suggesting nothing is acceptable and often correct. Only propose a component when there is **direct evidence** in the ticket text, comments, linked Confluence, or related MRs/commits. Do not infer from issue key alone, from the assignee, or from "tickets nearby usually have X."

## Constraints

- **Confirm before every write.** Adding existing components, removing components, and creating new components each require explicit user approval.
- **New components** require a second-level confirmation. The skill attempts creation via the Atlassian MCP; if no `create_component` tool is exposed (run `discover_tools` to check), surface the recommendation and instruct the user to create it manually in Jira.
- **Never remove** a component the user has set unless the user explicitly asks for cleanup.
- **No other ticket fields are modified** — never touch summary, description, labels, status, assignee, story points, or comments.

## Workflow — Single mode

```text
Single Progress:
- [ ] Phase 1: Resolve project + load existing components
- [ ] Phase 2: Gather ticket context (Jira)
- [ ] Phase 3: Pull related signals (Confluence + GitLab)
- [ ] Phase 4: Propose components with evidence
- [ ] Phase 5: Per-change confirm + apply
```

### Phase 1 — Project + existing components

1. Extract the project key from the ticket key (`PROJ-1234` → `PROJ`).
2. `jira_get_project_components` to load the canonical component list. Cache it for the session.

### Phase 2 — Ticket context

- `jira_get_issue` — summary, description, type, priority, status, **current components**, labels, fixVersion, environment.
- `jira_get_comments` — investigation notes and additional context users provided.
- `jira_get_remote_links` — Confluence pages, MR URLs, dashboards.
- `jira_get_changelog` — note prior component changes (someone may have removed a component intentionally — respect that signal).

### Phase 3 — Related signals

1. **Confluence** — for each remote link to Confluence (cap at 2), `confluence_get_page` and skim for system/component names. If no remote links exist, skip — do not invent searches.
2. **GitLab MRs** — for each remote link to a GitLab MR, `get_merge_request` and capture the file paths touched. These map most reliably to components.
3. **GitLab code search (single mode only)** — if there is a clear error string, function name, or stack frame in the ticket, run **one** `search_project_code` to locate the owning module(s). Skip if no high-signal token.

### Phase 4 — Propose components

For each candidate, write **one sentence** of evidence. Map evidence → component using the existing component list. Format:

```markdown
## Component suggestions for {KEY} — {summary}

**Currently set:** {list, or "none"}

### Proposed additions
| Component | Status | Evidence |
| --- | --- | --- |
| `auth-service` | existing | Stack trace in description references `auth/middleware.go`; MR !4521 touches that file. |
| `payments-ui` | **NEW** | Description mentions "checkout button"; no existing component covers the React checkout flow. |

### Suggested removals
_None._  (or list with reasoning)

### No change
_The ticket already has the right components._  (use this when applicable)
```

If you have nothing to suggest, say so plainly: *"No component changes proposed — current set looks correct given the available evidence."* Then stop.

### Phase 5 — Per-change confirm

For each proposed addition (existing component), ask via `AskUserQuestion`:
- **Add `{component}`** *(recommended default if evidence is strong)*
- **Skip**

For each proposed **new** component, ask a two-step question:
1. **Create new component `{name}`?** (Yes / No)
2. If yes, attempt creation via the Atlassian MCP. If no `create_component` tool exists, fall back: tell the user to create it manually in Jira and re-run the skill, then **skip** the addition for this ticket.

After confirmations, apply additions in **one** `jira_update_issue` call setting the `components` field to the union of existing + approved-new. Confirm to the user with the final list.

If the user rejects every suggestion, end with one line: *"No changes applied."*

## Workflow — Bulk mode

Read [BULK.md](BULK.md): resolve the project and scratch folder, fetch open tickets highest-key-first
(cap 250), run a light suggest-and-confirm per ticket, keep a rolling report, then summarise and ask
whether to keep the scratch folder.

## Evidence rubric (for both modes)

| Signal | Weight |
| --- | --- |
| Stack trace / file path / function name in ticket → matches a known module | **Strong** |
| GitLab MR linked from ticket touches files in a known module | **Strong** |
| Confluence design doc linked from ticket explicitly names a system | **Strong** |
| Ticket summary contains a system/feature name that matches a component verbatim | **Medium** |
| Reporter or assignee historically works on a component | **Weak — do not use as primary evidence** |
| "Looks like it might fit" with no concrete signal | **Insufficient — do not suggest** |

When in doubt, suggest nothing. The cost of an over-tagged ticket is higher than an under-tagged one because it pollutes filters and reports.

## Quality Loop

Before returning, check the output against these criteria. If two or more fail, revise and re-check — at most two passes, then note what still falls short.

- Suggested components already exist in the project (or a new one is explicitly flagged as new)
- Each suggestion has a rationale tied to the ticket's content
- Confirmation is sought before any modification
- Conservative — no more components suggested than the ticket clearly warrants

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/issue-suggest-component.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
