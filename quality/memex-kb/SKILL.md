---
name: memex-kb
description: Search, read, create, edit, and maintain knowledge in a Memex KB via the `mx` CLI. Use when the user asks to search the KB, find documentation, check project or organizational docs, add or update knowledge-base entries, audit KB quality, or when reusable knowledge should be captured for future agents.
---

# Memex KB Workflow

Use `mx` as the source of truth for KB state. From a repo checkout, prefix commands with `uv run`.

## First Commands

Before writing or assuming paths:

```bash
mx prime
mx info
mx context show
mx context validate
mx categories
```

Use explicit scope when both KBs are active:

```bash
mx categories --scope=project
mx categories --scope=user
```

Check these before creating entries:
- active KBs and default write directory
- valid categories/directories
- whether paths need `@project/...` or `@user/...`

## Search First

Search before answering from memory or creating content:

```bash
mx search "query"
mx search "query" --mode=keyword
mx search "query" --mode=semantic
mx search "query" --include-neighbors
mx search "query" --content
mx search "query" --parents=nearest
mx get @project/path/to/entry.md
mx get --title="Entry Title"
```

Use keyword mode for exact strings, filenames, command names, or errors. Use semantic mode for
conceptual matches. Use `--scope=project|user` when mixing team and personal KBs would be confusing.
In nested project KBs, parent KBs are opt-in for search; use `--parents=nearest` when shared parent
workspace knowledge may matter. Parent results may appear as `@parent/...` or a configured parent
scope like `@agents/...`; use those exact paths with `mx get`.

## Write Deliberately

Prefer updating an existing entry, then appending to a log/note, then creating a new page. Choose
scope by audience: `project` for shared repo/team knowledge, `user` for personal notes.

Useful write commands:

```bash
mx add --title="..." --tags="..." --category=guides --scope=project --content="..."
mx quick-add --content="..."
mx ingest notes.md --directory=guides --scope=project
mx patch @project/path.md --find="old" --replace="new"
mx append "Entry Title" --content="new section"
mx replace @user/path.md --content="full replacement"
```

Notes:
- `mx add` and `mx ingest` support `--scope=project|user`; `mx quick-add` does not.
- If `.kbconfig` has no `primary`, pass `--category` explicitly.
- Use `mx tags` before inventing new tags.
- After creating, run `mx get <path>` and consider `mx suggest-links <path>`.

## Session Handoffs

For substantial work another agent may continue, keep a concise handoff:

```bash
mx sessions start --goal="..." --harness=codex
mx sessions append --latest --summary="What changed, files touched, tests run, blockers" --files=path
mx sessions append --latest --summary="Linked transcript" --transcript=/path/to/session.jsonl
mx sessions finish --latest --summary="Final state and remaining next steps"
mx sessions recent
```

Use `mx sessions hook <claude|codex> --instructions`, `--print`, or `--install` for harness hooks;
add `--turns N` for periodic session-log reminders. Store summaries and next steps, not full
transcripts or secrets. Store transcript paths with `--transcript`, not transcript content.

## Relations And Health

```bash
mx relations path.md --depth=2
mx relations-add path.md --relation "other.md=documents"
mx relations-remove path.md --relation "other.md=documents"
mx relations-lint
mx health
mx whats-new --days=7
mx hubs
mx doctor --timestamps
mx doctor --timestamps --fix
```

Run health checks after meaningful writes or when auditing stale content, broken links, orphaned
entries, relation type drift, or timestamp issues.

## Details Live Elsewhere

Do not maintain a second copy of the CLI or schema inside this skill.

Read when needed:
- `kb/reference/cli.md` for current command options and JSON output shapes
- `kb/reference/entry-format.md` for frontmatter, links, semantic links, and typed relations
- `kb/guides/quick-start.md` for onboarding flow and category conventions in the current repo
- `kb/design/relations-graph/relations-graph-overview.md` when relation traversal or publish behavior matters

## Avoid

- adding a new entry before searching for an existing one
- assuming unscoped paths target the intended KB when multiple scopes are active
- assuming a nested KB search includes parent KB results without `parent_kbs: nearest` or `--parents=nearest`
- hard-coding categories from another repo
- using `mx quick-add` when you need explicit scope
- using `mx replace` when `mx patch` or `mx append` would preserve more context
- creating personal scratch notes in the project KB
- inventing new tags without checking `mx tags`
