---
name: synthesize
description: >
  Write a cross-topic synthesis note under vault/wiki/_synthesis/. Trigger
  when the user asks to "compare X and Y", "find themes across these pages",
  "identify contradictions", "do a gap analysis", "build a timeline of Z", or
  invokes /claude-wiki-pages:synthesize directly. Also used as the
  follow-up when /claude-wiki-pages:query offers to file an answer as a
  synthesis.
disable-model-invocation: true
allowed-tools: Read Write(vault/wiki/_synthesis/*) Write(vault/wiki/log.md) Edit(vault/wiki/log.md) Glob Grep
---

# LLM Wiki — Synthesize

Produce a single new page under `vault/wiki/_synthesis/` with
`type: synthesis` frontmatter. Every synthesis covers a defined scope and
cites every source it rests on.

This skill writes one page per invocation. A multi-topic session becomes
several synthesis notes, not one sprawling document.

## When to invoke

- The user names an explicit scope and asks for cross-topic analysis.
- `/claude-wiki-pages:query` offered to file an answer as a synthesis
  and the user accepted.
- The `claude-wiki-pages-ingest-agent` agent detects that a batch of new sources opens
  a synthesis opportunity — the agent passes the scope here.

## Reading contract

- `vault/CLAUDE.md` — the schema.
- The user-selected scope: explicit pages, a topic folder, or a list of
  concepts / entities.
- Pages reached by following wikilinks from the scope, when the synthesis
  type calls for them (e.g., `contradiction` needs to read both sides).

## Writing contract

Exactly one new file:

```
vault/wiki/_synthesis/<kebab-slug>.md
```

The file must carry the synthesis frontmatter schema from `vault/CLAUDE.md`:

- `title` — Title Case, matches the first entry of `aliases`.
- `type: synthesis`.
- `synthesis_type` — one of `comparison`, `theme`, `contradiction`, `gap`,
  `timeline`. No default.
- `path: "_synthesis"`.
- `scope:` — every page the synthesis rests on, as piped-basename
  `[[file-basename|Title]]` wikilinks (never a bare `[[Title]]` — it does not
  resolve and renders as a ghost node). At least two entries (a synthesis of
  one page is an extended page, not a synthesis).
- `sources:` — every source cited. At least one entry.
- `aliases:` — first entry equals `title`.
- `created`, `updated`, `status`, `confidence` per schema defaults.

Plus one log append:

```
## [YYYY-MM-DD] synthesize | <title>
```

This skill MUST NOT:

- Write to `vault/raw/`.
- Write to any wiki path outside `_synthesis/`.
- Edit an existing synthesis note — produce a new one and, if needed, mark
  the prior one `status: superseded` in a follow-up step (separate invocation).
- Rebuild `wiki/index.md` directly. Instead, print a reminder that
  `/claude-wiki-pages:index` should be run after a new synthesis lands.

## Workflow

1. **Schema.** Read `vault/CLAUDE.md`.
2. **Resolve scope.** Convert the user's intent into concrete scope entries.
   Reject the invocation if fewer than two pages are in scope.
3. **Classify.** Choose `synthesis_type` from the enum. Do not default — make
   a deliberate choice based on what the user asked for.
4. **Gather.** Read each page in scope plus any page reached by following
   the relations the synthesis type demands (e.g., `contradicts` for
   `contradiction`; `depends_on` for `gap`).
5. **Draft.** Compose the body. Every non-trivial claim carries a citation.
6. **Write.** Create the new file under `_synthesis/`. Let `PreToolUse`
   enforce the schema.
7. **Log.** Append to `wiki/log.md`.
8. **Handoff hint.** Remind the user (or the calling agent) that the vault
   MOC is stale — offer `/claude-wiki-pages:index`.

## Completion signal

```
READY: wrote <path>; synthesis_type=<type>, scope=<N> pages, sources=<M>.
Remember to refresh the vault MOC: /claude-wiki-pages:index.

## Context contract

Machine-readable read/write contract for the `engine context` verb.

| role           | globs                                          |
| -------------- | ---------------------------------------------- |
| inputs (L4)    | wiki/**, wiki/_sources/**                      |
| reference (L3) | vault/CLAUDE.md, wiki/index.md                 |
| outputs        | wiki/_synthesis/*                              |
```
