---
name: refresh-kb
description: Refresh and validate a hraness/wordcell Markdown knowledge graph after notes, concepts, typed relationships, attachments, repository scopes, or context mappings change. Use when an agent needs to maintain a managed or authored catalog, inspect graph and lifecycle findings, validate local artifacts and scope hubs, or complete a vault health check.
---

# Refresh a knowledge base

Use a refresh-review-check loop. Keep authored prose under deliberate editorial control. A managed vault gives the marked catalog region to the tool; an authored vault leaves its complete front door untouched.

## 1. Locate the vault

- Resolve `<vault>` to the directory containing its managed or authored `index.md`, then
  set the shell-local `KB_ROOT` to that path (`KB_ROOT=kb` from a typical
  repository root, or `KB_ROOT=.` from inside the vault).
- When the change concerns `scopes/` or an `kb:context` marker, resolve the
  repository root and set `KB_REPO` to that path (`KB_REPO=.` from the
  repository root).
- Read the vault's applicable agent instructions and note conventions before editing.
- Preserve note voice, frontmatter, filenames, and link intent unless a reported finding justifies a specific change.

## 2. Refresh derived state

When several agents are still editing a managed vault, do not refresh its
shared catalog in each lane. Validate the lane's Markdown and graph facts with:

```sh
wordcell check --root "$KB_ROOT" --no-catalog
```

The integrating agent performs the managed refresh once after the lanes join.
An authored vault declares `kb_catalog: authored` in `index.md`; its refresh has
no catalog write and is safe from that shared generated-file hotspot.

Run:

```sh
wordcell refresh --root "$KB_ROOT"
```

In managed mode this command atomically updates only the marked catalog region
in `index.md`. In authored mode it reports the index as authored and leaves the
file unchanged. Use `wordcell catalog --root "$KB_ROOT"` for a disposable exhaustive
inventory in either mode. Catalog links are navigation, so they do not count as
contextual graph edges.

## 3. Review the advisories

Open every reported source line and the relevant target notes before deciding whether to edit.

- Repair a broken wikilink only when its intended target is clear. Otherwise, report the uncertainty.
- Repair a broken or ambiguous typed relationship only after confirming its exact canonical target and predicate from the source note.
- Disambiguate a wikilink with a vault-root path only after confirming the author's intent.
- Treat a contextual orphan as a prompt to inspect the note, not as a demand to add a link.
- Treat an unlinked title or alias mention as a candidate, not proof that the sentence should link.
- Add a contextual wikilink only when it improves the meaning or navigation of the sentence.
- Repair a missing, escaping, ambiguous, case-mismatched, symlinked, or hard-linked local image, PDF, or tldraw target. External URLs remain outside this attachment gate.
- When a repository-owned wrapper adds lifecycle findings, treat them as
  migration advisories: active plans should have descriptions and exact
  `repository_scopes`, in-progress plans should retain execution evidence,
  terminal plans should record a result and durable-memory disposition, and
  maintained notes should declare `type: note` or `type: concept`.
- When a repository-owned scope audit reports an absent active or maintained
  scope, inspect it as possible stale routing. Future paths may intentionally
  be absent; terminal records may intentionally retain retired paths. The
  portable `wordcell refresh` and `wordcell check` commands do not impose this lifecycle
  policy by themselves.

Backlinks are derived from explicit contextual wikilinks and typed
relationships. Mention and percolation candidates are derived analysis. Never
inject reciprocal, transitive, or similarity-derived relationships or generated
backlink sections to improve graph counts. Never mutate authored prose
automatically or apply suggestions mechanically in bulk.

Run a bounded percolation review for each materially changed note:

```sh
wordcell percolate "<changed-note-id>" --root "$KB_ROOT" --limit 25 --json
```

Open the cited notes before deciding whether to create a reusable
`type: concept` note or a source-owned typed relationship.

Intentional orphans and unlinked mentions may remain. Record the reason instead of manufacturing a connection.

Review recent captures without maintained disposition when useful:

```sh
wordcell inbox --root "$KB_ROOT" --limit 25 --json
```

The inbox ignores source-to-source and catalog links. It is advisory; an
intentional leaf capture needs no manufactured backlink.

## 4. Validate changed repository-context mappings

If the change adds, removes, renames, or moves a scope hub, changes its
`type` or `scope`, or edits an `kb:context` marker, run:

```sh
wordcell agents identity "<repository-scope>" --json
wordcell agents check --root "$KB_ROOT" --repo "$KB_REPO"
```

Use the non-mutating identity command to derive the hub path and exact marker
when creating or moving a mapping. The check command verifies canonical IDs,
exact repository-relative
directory scopes, collisions, repository confinement, real scope directories
and guide files, guide shape, and reciprocal markers. A moved scope has a new
identity, so update the hub filename and guide marker together. An unmapped
`AGENTS.md` is valid.

Use the audit when the change affects guide structure, inheritance, or repeated
rules:

```sh
wordcell agents audit --root "$KB_ROOT" --repo "$KB_REPO"
```

The audit runs the correctness checks and adds deterministic per-guide,
per-section, inherited-chain, long-bullet, and exact-duplicate advisories.
Review each advisory in context. Length is not correctness: do not move a
load-bearing ownership rule, prohibition, command, invariant, or gate out of
`AGENTS.md` merely to satisfy a suggested budget. Guide discovery skips common
generated and vendor directories and never follows symbolic-link directories.

## 5. Re-refresh and check

After any note or link edit, run the refresh command again so derived state and advisories reflect the final content. Then run the read-only gate:

```sh
wordcell check --root "$KB_ROOT"
```

Finish only when the graph check and any required agent-context check succeed,
the configured catalog mode is satisfied, and broken or ambiguous links,
relationships, and local attachments are resolved. Summarize deliberate
concept, relationship, link, scope, and mapping edits plus advisories
intentionally left in place.
