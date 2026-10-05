---
name: manage-tickets
description: "Create, edit, search, transition, close, and triage Jira tickets via the Atlassian MCP. Use when asked to file a bug, request a feature, create a task, log a defect, search the backlog, triage findings into the tracker, edit ticket fields, transition status, or manage Jira work items. Also use when the user says 'create a Jira issue', 'file a bug', 'open a ticket', 'add to backlog', 'search Jira', 'close ticket', 'move to Done', or names any Jira issue key (e.g. 'PROJ-123'). Also use for read-only backlog sweeps: which ticket to pick up next, what is unblocked, what blocks a given key, how many issues are open. Handles type discovery, parent linking, label assignment, duplicate detection via JQL, status transitions, issue-link creation, and large queries that overflow the tool output limit. Defers all field-content formatting to the `jira-syntax` skill. Do NOT use for pull requests, changelog entries, non-Jira trackers (GitHub Issues, Linear, GitLab), or managing local TODO.md."
metadata:
  author: Serghei Iakovlev
  version: "1.5"
  category: roadmap
---

# Managing Jira Tickets

Manage Jira tickets via the Atlassian MCP. Every ticket must be self-contained, professional, and actionable without prior context. The skill applies only to Jira sites the Atlassian MCP is connected to; if the MCP is unavailable, stop and tell the user.

## Prerequisites

1. Atlassian MCP server is available. MCP is the only path to Jira - never `curl`, never bare HTTP, never `gh`.
2. `jira-syntax` skill is loaded before composing any field content. Jira description and comment fields are wiki markup, not Markdown.

## Discover project metadata (run first)

Before any create, edit, search, or transition operation, fetch the live metadata for the target site and project:

| Need                                | Tool                              |
|-------------------------------------|-----------------------------------|
| Jira site `cloudId`                 | `getAccessibleAtlassianResources` |
| Visible projects and their keys     | `getVisibleJiraProjects`          |
| Types accepted by chosen project    | `getJiraProjectIssueTypesMetadata`|
| Required fields for a chosen type   | `getJiraIssueTypeMetaWithFields`  |
| Site-wide issue link types          | `getIssueLinkTypes`               |
| Valid transitions for an issue      | `getTransitionsForJiraIssue`      |
| Resolve display name to account id  | `lookupJiraAccountId`             |

Use the values verbatim. Never memorize project keys, type names, transition IDs, label names, or account IDs across sessions.

What to do when discovery returns nothing, returns several projects, lacks the type you classified, or reports required custom fields is tabulated in [references/ticket-operations.md](references/ticket-operations.md) § Discovery branching.

## Body shape

Tickets share three common sections; the middle is type-specific.

| Section          | Position | Purpose                                                                                                |
|------------------|----------|--------------------------------------------------------------------------------------------------------|
| Summary          | Top      | One paragraph stating what the ticket addresses. Not a restatement of the title.                       |
| (type-specific)  | Middle   | Background, observed behaviour, root cause, proposed solution, scope, etc. - varies per type.          |
| Requirements     | Near end | Observable outcomes in MUST / MUST NOT form. Each independently verifiable.                            |
| [Self-checks]    | Optional | `Automated` (CI assertions) and `Manual` (operator-runnable scenarios). Encouraged for Bug, Story, Task.|
| Context          | Bottom   | Origin (where the ticket came from), verbatim operator/reviewer quote, related tickets, tracking links.|

The per-type templates in `assets/` realize this shape with the right middle sections for each type. Some sections are bracketed `[…]` in the templates - drop them when there is no content.

## Type classification

Pick exactly one. When two rows match, ask one question that decides between them.

| Signal in the request                                                | Type       | Template                                                |
|----------------------------------------------------------------------|------------|---------------------------------------------------------|
| User-visible feature, capability, behaviour change                   | `Story`    | [assets/template-story.md](assets/template-story.md)     |
| Defect, regression, "broken", "crash", "wrong", "doesn't work"       | `Bug`      | [assets/template-bug.md](assets/template-bug.md)         |
| Non-feature work: infra, build, deps, chore, docs                    | `Task`     | [assets/template-task.md](assets/template-task.md)       |
| Time-boxed investigation, prototype, "spike", "research", "evaluate" | `Spike`    | [assets/template-spike.md](assets/template-spike.md)     |
| Body of work containing multiple stories                             | `Epic`     | [assets/template-epic.md](assets/template-epic.md)       |
| Slice of an existing parent issue                                    | `Sub-task` | [assets/template-subtask.md](assets/template-subtask.md) |

## Parent matching

| Issue type                  | Parent rule                                                                                                                                       |
|-----------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| `Sub-task`                  | MUST have a parent. JQL `project = {key} AND issuetype in (Story, Task, Bug) AND statusCategory != Done` → present keys → ask.                    |
| `Story` / `Task` / `Bug`    | Parent Epic is optional. If the user did not name one, run `project = {key} AND issuetype = Epic AND statusCategory != Done ORDER BY rank ASC` and offer the list; "none" is a valid answer. |
| `Epic` / `Spike`            | No parent.                                                                                                                                        |

## Before creating a ticket

### Duplicate check (BLOCKING)

This check and the parent-matching queries above are the create path's first searches over a populated project, and the first calls that can overflow the tool's output limit into a persisted file. Load [references/jira-recipes.md](references/jira-recipes.md) § "Querying large projects without overflowing tool output" before running either.

Run before every `createJiraIssue` call. Use `searchJiraIssuesUsingJql` with a keyword query:

```
project = {KEY} AND text ~ "<keywords from the user's request>" AND statusCategory != Done
ORDER BY created DESC
```

- **Exact duplicate.** Stop. Report the existing ticket key.
- **Partial overlap.** Mention the related ticket. Ask whether to proceed.
- **No match.** Proceed.

### Proportionality check

A ticket is a durable artifact with a cost of its own: the prose to write it, and the re-derivation a future reader faces because the context that produced it is gone. When the change it would request is smaller than that cost, the ticket is the more expensive half of the transaction.

Weigh both sides before creating:

- **The fix.** Is the whole change a small, local edit whose correctness is evident from the diff, inside code the current work already touches, and covered by the checks that work already runs?
- **The ticket.** How much of the body would restate context that exists only right now, and how much re-derivation does a future reader inherit?

When the fix is clearly the cheaper half, do not create it. Propose the edit instead: name the file and lines, state the change in a sentence or two, give the cost comparison that justifies doing it now, and **ask the user for approval, then wait.** On approval, apply the edit under the boy-scout principle - leave the code better than you found it - and report it as applied rather than filed. On refusal or silence, create the ticket as normal.

Never self-approve this path. The approval is what makes the edit part of the requested work instead of unrequested scope, which is the distinction a surgical-changes convention turns on.

Cheapness alone does not admit an edit. Create the ticket regardless of size when the change would alter behaviour a user notices, touch a security boundary, require a decision the agent cannot make, or reach code the current work does not already touch.

## Create

### Body rules

- **Language.** English.
- **Tone.** Professional, concise, no filler.
- **Privacy.** Never include usernames, API keys, internal URLs, tokens, or personal information, regardless of whether the project is private or read-restricted. Jira is observed by people outside the immediate authoring team.
- **Self-contained.** A reader who has never seen this work must understand the ticket from the body alone.
- **Cite source by file:line.** When the ticket refers to existing code, constants, or behaviour, anchor each claim to a path and line range (e.g. `path/to/module.ts:123-145`). File:line citations turn the ticket into a self-auditable record.
- **Preserve verbatim quotes.** When the ticket originates from a specific operator, reviewer, or customer report, include the exact wording in the Context section. Paraphrasing loses the reporter's mental model and removes the literal phrase a future searcher will type.
- **No hard wrapping mid-sentence.** Write each paragraph as a single line; Jira handles flow at render time. Hard-wrapping mid-paragraph creates spurious paragraph breaks in wiki markup and noisy diffs on edit.
- **Bugs describe problems, not solutions.** Steps to reproduce, Expected, Observed describe the problem. When the reporter investigated and has a concrete fix in mind, it goes into the optional `Proposed solution` section as a suggestion, not as a mandate that bypasses Requirements.
- **Requirements.** Required for `Story` and `Bug`. Optional for `Task`, `Spike`, `Epic`, `Sub-task` (include when a concrete completion signal exists). Write each requirement in MUST / MUST NOT form. Each is independently verifiable. Reserve MAY for genuinely optional outcomes.
- **Markup.** Jira wiki markup via `jira-syntax` (NOT Markdown).
- **Composition.** Draft any description or comment longer than a screen into the session scratchpad first, then send the file's contents. An edit replaces the whole field, so a one-word correction after the fact costs a second full-body send; with the draft on disk the correction is a one-line edit and the resend is mechanical.
- **Never reference internal artefacts.** ADR numbers, architecture section IDs, doc paths, ticket IDs in source-code comments - none of these belong inside the ticket body unless the user explicitly asked. Those identifiers live in specs, not in work items.

### Body templates

Pick the template for the classified type from the table in "Type classification" above. Copy the `## Template` block verbatim, then fill every section. Drop bracketed `{...}` placeholders that do not apply. Required sections (no brackets) stay.

### Title rules

- **Imperative mood**, capitalize first word: "Add X", "Fix Y", "Implement Z".
- **Backtick-wrap code identifiers**: `` Validate `--host` flag for HTTP bind address ``.
- **Under 80 characters**, no trailing period.
- **No `[type]` prefix** - the Jira `issuetype` field carries the classification.
- Self-contained without parent context. Good: "Validate webhook signatures before processing". Bad: "Validation".

### Composing the createJiraIssue call

```
createJiraIssue:
  cloudId:        <from getAccessibleAtlassianResources>
  projectKey:     <KEY>
  issueTypeName:  Story | Bug | Task | Spike | Epic | Sub-task
  summary:        <title>
  description:    <wiki-markup body>
  parent:         <PARENT-KEY>          # required for Sub-task; optional for others
  additional_fields:                    # only non-default fields
    labels:       ["<label>", ...]
    customfield_NNNNN: <value>
```

On rejection of a custom field: drop that field, retry with required-only, surface the omitted field in the report so the user can backfill via `editJiraIssue`.

### Batch creation

When creating multiple related tickets (e.g. an Epic with child Stories):

1. Present all planned tickets as a numbered list (title, type, parent, labels) before creating any.
2. Wait for user confirmation.
3. Order the batch so each ticket is created after every ticket its body names. Jira allocates keys in submission order, which is rarely the order the drafts sit in, and a parallel agent can take the numbers in between: the next free number is a guess, not a key. When two tickets reference each other and no order satisfies both, create with a placeholder naming the target (`{KEY}-???(<subject of the target ticket>)`), then substitute the real keys via `editJiraIssue` in one pass, reading each off the create report. A predicted key renders as a valid link, points at the wrong ticket, and nothing downstream checks it.
4. Create sequentially. Report each ticket key after creation.
5. Print a summary table when done:

```
| # | Key | Type | Parent | Title | Labels |
|---|-----|------|--------|-------|--------|
```

### Confirm before create

Print this block. Wait for explicit user approval before calling `createJiraIssue`.

```
Draft:
  Project:   {KEY} ({name})
  Type:      {type}
  Parent:    {KEY or "none"}
  Title:     {composed title}
  Labels:    {labels or "—"}

Body:
  {full body, wiki markup}

Reply "create" to file the ticket, or send edits.
```

Silence, "ok", or unrelated follow-ups are not confirmation.

### Report after create

```
Created: {KEY} — {title}
URL:     {browseUrl}
Type:    {type}{, parent: PARENT-KEY}
Labels:  {labels or "—"}
Inferred:
  - {field}: {value}     # each field set without explicit user input
Links:
  - {KEY-A} {linkType} {KEY-B}    # each created link, or "—"
```

`Inferred` is the user-care line: it lists every field the agent chose without being told. If empty, write `—`.

## Search, Edit, Transition

Policy for these three operations, plus issue linking, is in [references/ticket-operations.md](references/ticket-operations.md) § Search, Edit, Transition; the MCP call surface is in [references/jira-recipes.md](references/jira-recipes.md). Load both before the first find, modify, transition, or link call: a wrong-direction issue link succeeds silently and this MCP exposes no way to delete it.

## Triage

When triaging a finding from code review, logs, discussion, or PR feedback into the backlog:

1. **Extract the concern.** State it in one sentence.
2. **Duplicate check.** Run the BLOCKING JQL query from "Before creating a ticket".
3. **Classify type** per the table in "Type classification".
4. **Resolve parent** per "Parent matching".
5. **Draft the body** using the matched template.
6. **Present the full `createJiraIssue` payload for review** before executing.

## Actualize

Reconciling tickets that predate work which has since shipped is in [references/ticket-operations.md](references/ticket-operations.md) § Actualize. Open it whenever a ticket may be stale: the current code is ground truth, and a ticket's age is not evidence of its accuracy.

## Quality checklist

Before executing `createJiraIssue`, verify:

- [ ] `getAccessibleAtlassianResources` returned a `cloudId`
- [ ] Project key is explicit (named by user or unambiguous from `getVisibleJiraProjects`)
- [ ] Chosen type appears in `getJiraProjectIssueTypesMetadata`
- [ ] Required custom fields from `getJiraIssueTypeMetaWithFields` are filled
- [ ] Duplicate check performed (JQL keyword search)
- [ ] Proportionality weighed: filing costs less than the change it requests, or the cheaper edit was proposed and approved
- [ ] Title: imperative, ≤ 80 chars, no trailing period, no `[type]` prefix, code identifiers backtick-wrapped
- [ ] Body matches the type's template; bracketed sections dropped if empty
- [ ] Requirements present for Bug and Story, in MUST / MUST NOT form
- [ ] Source-code references cite file path and line range
- [ ] Verbatim quote preserved in Context when the ticket originated from a specific report
- [ ] Self-checks present for non-trivial Bug and Story tickets (Automated + Manual)
- [ ] Parent set for Sub-task (and for Story/Task/Bug if the user named an Epic)
- [ ] No usernames, keys, internal URLs, tokens, or personal information in the body
- [ ] No solution prescribed inside the problem-description sections of a Bug (use `Proposed solution` instead)
- [ ] No ADR numbers, doc paths, or ticket IDs in the body unless explicitly requested
- [ ] Labels exist on prior issues in the project (no invented labels) - or omitted
- [ ] Assignee/priority/reporter only set when the user named them
- [ ] Body passed through `jira-syntax` (wiki markup, not Markdown)

## Error recovery

Every failure this skill expects, with its recovery, is tabulated in [references/ticket-operations.md](references/ticket-operations.md) § Error recovery. Open it the moment an MCP call rejects a field, returns several candidates, or silently ignores what you sent.

## Constraints

- One ticket per `createJiraIssue` invocation. Loop for batches; never run a hidden create-loop.
- Never auto-confirm. The user's explicit "create" is the only gate.
- Never invent labels. Use labels the user named, or labels already present on issues read from the same project. When unsure, omit.
- Never set `priority`, `assignee`, or `reporter` unless the user named them. Resolve display names via `lookupJiraAccountId`; never write a raw email into an account-id field.
- Never reference internal artefacts (ADR numbers, architecture section IDs, doc paths, ticket IDs) inside the ticket body unless the user explicitly asked. Those identifiers belong in specs, not in work items.
- Never use `gh` or `curl` for Jira operations. MCP is the only path.
- All field text passes through `jira-syntax` first. Jira fields are wiki markup, not Markdown.
- After a destructive edit (body replacement, label replacement, status transition), verify by re-reading the ticket via `getJiraIssue` and include the verified state in the report.
