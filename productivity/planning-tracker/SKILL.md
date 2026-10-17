---
name: planning-tracker
description: Use when a planning skill must read, create, link, label, or close planning items (maps, decisions, specs, tickets) and the tracker backend must be resolved as local Markdown files or GitHub Issues.
license: MIT
---

# Planning Tracker

## Purpose

Give the planning skills one tracker-neutral contract. `planning-interview`, `planning-spec`, `planning-tickets`, and `planning-wayfinder` describe work as **items** with kinds, statuses, labels, parents, and blocking edges; this skill maps those operations onto the backend the repository uses. Two backends are supported: **local Markdown** (the default and reference backend) and **GitHub Issues**.

## Activate when

- a planning skill needs to create, read, update, link, label, or close an item
- the next unblocked item (the frontier) must be found
- the repository's planning backend is unknown or ambiguous
- a local tracker directory must be validated

## Repository inspection

1. Look for a tracker declaration: a `## Planning tracker` section in `AGENTS.md` or `CLAUDE.md` naming `local` (with its root) or `github` (with `owner/repo`).
2. Look for an existing local tracker directory, `docs/planning/` by default, and existing item files (`NNNN-slug.md`).
3. For GitHub, confirm which tools are available in this session (the `gh` CLI or GitHub MCP tools) and that the repository matches the declaration.
4. Read existing labels before inventing new ones.

## Decision rules

Resolve the backend in this order and state the result before the first write:

1. an explicit instruction in the current task;
2. the repository's `## Planning tracker` declaration;
3. an existing local tracker directory;
4. otherwise ask the user; if nobody can answer, use local Markdown at `docs/planning/`.

Then use the item model below and load the backend's reference for the exact operations.

### Item model

| Field | Values | Meaning |
|---|---|---|
| `id` | integer | stable identity; local ids are sequential, GitHub ids are issue numbers |
| `title` | text | the name people use; refer to items by title, with the id inside the link |
| `kind` | `map`, `decision`, `spec`, `ticket` | a map indexes a large effort; a decision resolves one question; a spec describes a feature; a ticket is one vertical slice of work |
| `status` | `open`, `closed` | nothing else; progress detail belongs in the body |
| `labels` | list | workflow labels such as `ready-for-agent` and `needs-decision` |
| `parent` | item id | the map or spec the item belongs to |
| `blocked_by` | item ids | items that must close before this one can start |
| `assignee` | name | who claimed the item; claim before starting work so parallel sessions skip it |

The **frontier** is every open, unclaimed item, other than a map, whose blockers are all closed.

### Operations

| Operation | Local Markdown | GitHub Issues |
|---|---|---|
| create item | write `NNNN-slug.md` with the next id | create an issue |
| read item | read the file | view the issue and its comments |
| update body or fields | edit the file | edit the issue body or labels |
| link parent | `parent:` front matter | native sub-issue when supported, else a `Parent: #N` body line |
| link blockers | `blocked_by:` front matter | a `Blocked by: #N, #M` body line |
| comment | append a dated `## Notes` entry | add an issue comment |
| claim | `assignee:` front matter | assign the issue |
| close | `status: closed` | close the issue |
| frontier | `scripts/tracker.rb frontier` | list open child issues and check each `Blocked by` line |

## Critical invariants

- One backend per effort. Never split a map's items across local files and GitHub.
- Creating, editing, labelling, or closing a GitHub issue is outward-facing: get the user's confirmation before the first remote write in a session unless the repository declaration authorizes the agent to publish.
- Never delete an item to "close" it; closing keeps the history that later decisions cite.
- Every blocking edge points to an existing item and the graph has no cycles; run `scripts/tracker.rb validate` after local edits.
- Never write secrets, credentials, or personal data into items; they may be published or committed.

## References

Load only the reference for the resolved backend; each is one level deep.

| Load when | Reference | Covers | Patterns |
|---|---|---|---|
| the backend is local Markdown | [references/local-markdown.md](references/local-markdown.md) | Directory layout; item file format; ids; the tracker script; body sections | none |
| the backend is GitHub Issues | [references/github.md](references/github.md) | Issue mapping; labels; parent and blocker links; frontier queries; confirmation | none |

## Reference example

A local tracker, validated and queried with the bundled script (paths relative to this skill's directory):

```bash
ruby scripts/tracker.rb validate --root docs/planning
ruby scripts/tracker.rb frontier --root docs/planning --parent 1
ruby scripts/tracker.rb next-id --root docs/planning
```

```text
Tracker valid: 7 items under docs/planning
0003  decision open   Decide where refund tax is recorded
0004  decision open   Decide the refund ledger entry
0008
```

## Agent review checklist

- [ ] backend resolved from instruction, declaration, existing directory, or the user, and stated
- [ ] items use the shared kinds, statuses, parents, and blocking edges
- [ ] remote writes confirmed or authorized
- [ ] local tracker validates with no errors
- [ ] items referred to by title, not bare ids
- [ ] no secrets or personal data in items

## Failure modes

- guessing a backend and publishing issues the user did not expect
- inventing statuses such as `in-progress` instead of labels and body notes
- blocking edges that point at missing items, or cycles that leave the frontier empty
- deleting items, so later decisions cite nothing
- mixing local files and GitHub issues within one effort

## Verification

For local Markdown, run `ruby scripts/tracker.rb validate --root <root>` and confirm it reports no errors. For GitHub, re-read each created or edited issue and confirm its labels, parent, and `Blocked by` line.

## Source foundation

The item model and backend split are this repository's design. The planning workflow they serve (maps of decision tickets, specs, tracer-bullet tickets with blocking edges) is adapted from the `wayfinder`, `to-spec`, and `to-tickets` skills in https://github.com/mattpocock/skills (MIT License, Copyright (c) 2026 Matt Pocock), with the tracker made backend-neutral.
