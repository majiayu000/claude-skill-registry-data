---
name: percolate-kb
description: Review a hraness/wordcell Markdown vault for recurring ideas and missing structural connections, then promote evidence-backed concepts and typed relationships with the Wordcell CLI. Use after materially adding or revising notes, when organizing an accumulated vault, or when an agent needs to turn repeated tags and prose references into an explicit queryable knowledge graph.
---

# Percolate concepts and relationships

Keep the graph authored, local, and reviewable. `wordcell percolate` proposes
candidates from deterministic evidence; it never changes a note. Backlinks,
graph reports, and QMD results are derived views, while Markdown remains the
authority.

## Locate the vault

- Resolve `<vault>` to the directory containing its authored or managed
  `index.md` front door.
- Read the applicable repository and vault instructions before editing.
- Pass the resolved path to every `--root`.
- Identify the note or small neighborhood changed by the current task. Prefer a
  bounded review to a vault-wide cleanup during parallel work.

## Inspect candidates

Run percolation on the changed note when possible:

```sh
wordcell percolate notes/example --root "$KB_ROOT" --limit 25 --json
```

Run it without a note only when reviewing the whole vault:

```sh
wordcell percolate --root "$KB_ROOT" --min-support 2 --limit 50 --json
```

Treat each result as a prompt to open the cited notes and read the relevant
prose. Candidate kinds may include:

- a recurring tag with no maintained `type: concept` note;
- notes that share a concept or tag but have no explicit relationship;
- an exact title or alias mentioned without a contextual link;
- a self, reciprocal, malformed, broken, or ambiguous authored relationship.

For missing relationships, `support` counts independent shared tags or concept
neighbors; the evidence array shows the participating notes. The default
minimum of two therefore requires two shared signals, not merely both endpoints
of one tag match. Other candidate kinds count their natural unit: supporting
notes, mention occurrences, or authored hygiene evidence.

For a missing concept, use `suggestedId`. When `collidesWith` is non-null, the
natural ID is already an ordinary note, so KB chooses an unoccupied
`*-concept` ID. Read the occupied note before deciding whether to create the
suggested concept or promote and improve the existing note instead.

Semantic search may help discover evidence, but similarity is never enough to
author an edge.

## Promote durable concepts

Create a concept only when the idea is likely to be reused and its definition
can be stated from the source material:

```sh
wordcell note create notes/local-first \
  --root "$KB_ROOT" \
  --title "Local-first" \
  --type concept \
  --tag architecture \
  --body '# Local-first

A concise reviewed definition grounded in the cited notes.'
```

Write a concise definition and cite or link the notes that establish it.
Concepts are ordinary Markdown notes, so they can carry aliases, evidence,
context, and their own outbound relationships. Do not create a concept merely
to mirror every tag.

After promotion, rerun percolation on the cited non-concept notes. The new
concept may support relationships among its neighbors even when a run scoped to
the concept itself has no candidate:

```sh
wordcell percolate notes/write-path --root "$KB_ROOT" --limit 25 --json
```

## Author typed relationships

Add a relationship from the note that owns the assertion:

```sh
wordcell relation add notes/write-path supports notes/durable-agent-memory \
  --root "$KB_ROOT"
```

Use a specific lower-kebab-case predicate. Targets are exact vault-root note
IDs without `.md`. Ground the assertion in nearby prose or evidence; the
frontmatter is an indexable statement, not a substitute for explanation.

List or remove relationships without editing reciprocal notes:

```sh
wordcell relation list notes/write-path --root "$KB_ROOT" --json
wordcell relation remove notes/write-path supports notes/durable-agent-memory \
  --root "$KB_ROOT"
```

Never write inverse edges, generated backlinks, inferred transitive
relationships, or semantic-search scores into Markdown. Those are derived
views.

## Query before concluding

Use exact structure to verify that the promoted graph says what the prose says:

```sh
wordcell links notes/write-path --root "$KB_ROOT" --direction both --depth 2 --json
wordcell relation list notes/write-path --root "$KB_ROOT" --json
wordcell graph --root "$KB_ROOT" --json
```

Prefer the note-scoped commands first. Use the whole-vault graph only when the
question spans several neighborhoods, and confirm returned IDs against their
Markdown notes before reporting a conclusion.

## Finish under the vault's catalog mode

When working alone or integrating several lanes:

```sh
wordcell refresh --root "$KB_ROOT"
wordcell check --root "$KB_ROOT"
```

When several agents are editing different notes in a managed-catalog vault,
each lane should validate authored structure and local attachments without
rewriting the shared catalog:

```sh
wordcell check --root "$KB_ROOT" --no-catalog
```

The integrating agent runs one final managed refresh and normal check. In an
authored-catalog vault, refresh and check leave the front door untouched, while
`wordcell catalog --root "$KB_ROOT"` renders an exhaustive disposable inventory.
Resolve same-note Git conflicts from the prose and evidence; do not accept one
side's frontmatter mechanically.
