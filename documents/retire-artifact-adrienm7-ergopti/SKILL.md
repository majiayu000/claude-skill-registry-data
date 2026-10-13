---
name: retire-artifact
description: Retire a tracked plan, report, archive, or document without losing durable information. Use before deleting any tracked document.
---

# Retiring a document

Stale documents are worse than absent ones: they are read as current. But a
document that has outlived its process usually still carries a few live items,
and deleting it blind loses them. The whole job is separating the two.

## Never trust the document about itself

Status labels rot faster than anything else in a repo. Check every claim against
the code, and prefer the code's answer.

Two verified examples from the same file:

- A July plan asserted a timings accessor had "no production consumer". The
  keylogger walker reads it.
- The same plan asserted a set of updater menu keys did not exist, and used that
  to defer an entire i18n batch. All the keys were present in the shared locales.

An archived audit's "Open" labels are the same class of lie — the fix usually
landed, often with a test whose header cites the finding id. Grep for the id
before believing the label.

## The verdict is per item, not per document

Walk the document item by item and sort each one:

- **Delivered** — cite the `file:line` that proves it. This is the bulk of an old
  plan, and it is what makes the deletion safe.
- **Still open** — extract it, with enough context to act _without_ the original:
  what, where (real paths), why it matters today, and how to verify it. If you
  cannot write that, you have not understood it well enough to move it.
- **Decided against** — keep the _reason_, not the item, and put it under a
  "do not re-raise" heading. This is the part everyone drops, and it is why the
  same rejected idea comes back every few months.
- **Superseded** — a test now guards the invariant. Name the test. The test is
  the living memory; the prose was the placeholder.

## Where extracted work goes

`TODO.md` at the repo root, curated — a list, not an inventory. Rank by value and
say plainly what each item costs if it stays undone. If everything looks equally
important, nobody will start.

Durable _lessons_ go to the narrow topic under `docs/memory/` instead; see the
`project-memory` skill. The distinction: a lesson stops someone breaking
something, a TODO is work someone will do.

## Then delete, and fix what pointed at it

`git rm` the document, then find its references:

```bash
grep -rn "<DocName>" --include=*.md --include=*.js . | grep -v node_modules
```

A deleted plan usually leaves dangling links in driver READMEs, prompts and code
comments — a stale link is a small trap of the same family. Point them at what
replaced it.

Run `node ./tools/test/verify-change.cjs` and every selected gate. Independently
verify references to the retired document: `doc-paths` only rejects obsolete
driver-root names and is not a general Markdown link checker.

## When not to delete

Keep the document if it is a **reference** (it describes what _is_) rather than a
**plan** (it described what _was going to be_). A reference that has gone stale
gets corrected, not deleted — and correcting it is urgent, because a wrong
reference actively misleads. One in this repo instructed the reader to add
`Critical` to a block where the live test asserts its absence; following it would
have broken the suite.
