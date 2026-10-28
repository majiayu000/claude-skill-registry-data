---
name: note
description: Writes one durable fact into a markdown knowledge vault, with the frontmatter and the provenance that keep it checkable, then reindexes so search can find it. Use when something learned in a session has to outlive it, or on /note <the fact>, and not for what the repo already records.
---

# note: one fact, checkable later

A note that cannot be checked becomes a note nobody knows is still true. This skill exists
because two notes in the vault it was built from produced wrong output for weeks, and in
neither case was the number wrong when written: it was written without a way to re-measure
it.

Input: the fact, or nothing, in which case ask what to record.

## Where it goes

In order:

1. `$CLAUDE_KIT_VAULT`, if set.
2. The session's own memory directory, if the harness has one.
3. Ask. Do not guess a path and do not create a vault the user did not ask for.

One fact per file. A file that holds two facts gets found by a query for one of them and
read for both, and it goes stale in halves.

## What does not go in

- **What the repo already records.** Code structure, a past fix, anything in git history,
  anything in `CLAUDE.md` or `AGENTS.md`. A note that duplicates the repo drifts from it.
- **What only matters to this conversation.** A path you are about to use, a number you are
  about to act on.
- **A credential.** Not a token, not a password, not a connection string. A pointer to
  where the secret lives is fine and is often the useful part.
- **Employer content in the wrong vault.** If more than one vault exists, they are separate
  for a reason and the reason is usually a contract.

If asked to record one of those, say what you are not recording and ask what was
non-obvious about it, which is usually the real note.

## The shape

```markdown
---
name: <short-kebab-case-slug>
description: <one line, and this is what search matches on>
metadata:
  type: user | feedback | project | reference
---

<the fact, in the fewest sentences that survive being read in six months>

**Why:** what made this worth writing, including what was believed before.

**How to apply:** what to do differently, concretely.

Ver [[related-note]].
```

`description` earns its own care: in the vault this came from it is the single strongest
retrieval signal, because 85 of 85 notes had one and 81 had no title at all, and indexing
it moved the retrieval score more than the reranker did. Write it as the sentence someone
would type when looking for this.

Link liberally with `[[name]]`. A link to a note that does not exist yet is not an error,
it marks the note worth writing.

## Provenance, which is the part that gets skipped

Any claim that can age carries **the date it was measured and the command that re-measures
it**:

> Measured 2026-08-17: one repository writes commits in Portuguese, the other seven in
> English. Reproduce with `for r in ~/work/*/; do git -C $r log --oneline -5 --pretty=%s; done`.

- A number, a count, a "right now it is like this": date plus command, always.
- A calibrated constant: the sweep values and the size of the corpus they held for.
- Something decided in conversation rather than measured: mark it as a decision and date
  it.
- **A note that contradicts the current state gets corrected, and the correction records
  what made it age.** The pattern that produced the error will produce it again.

## Before writing

Search first. If a note already covers this, **update that one**, and say what changed
rather than appending a second version underneath. Two notes on one subject is how a vault
starts disagreeing with itself.

If the vault has an index file, add the one-line pointer. If a note turns out to be wrong,
delete it; a wrong note is worse than a missing one.

## After writing

Reindex, or search keeps answering with the old content. With the vault's MCP server that
is `kb_reindex`; otherwise whatever the vault's own indexer is.

Then report in one line: the path, and the one-line description. Not the note back.
