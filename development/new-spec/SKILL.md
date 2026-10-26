---
name: new-spec
description: Write a spec in docs/todo before building anything bigger than a one-line fix. Use when starting a feature, a change with more than one moving part, or when the user describes what they want but not how it should work.
---

# Writing a spec

Anything beyond a one-line fix starts here. Create `docs/todo/NNN-short-name.md` (specs live in docs/todo/) using the
structure below and fill it in.

**First, ground the spec in the knowledge base.** Read the affected domain's
`docs/system/domains/<domain>/README.md` — its constraints and gotchas feed
"What must NOT change" directly. When the spec ships, fold anything it taught
us back into that domain file.

## Why bother

A chat transcript is not a record. Six months from now the spec is what
explains why the code looks the way it does — and in this codebase, "why" is
usually an incident. The spec is also where the assumptions live, so an
assumption that turns out wrong is findable instead of buried in a diff.

## The sections that actually matter

Most of a spec is quick. Two sections earn their keep:

### "What must NOT change"

The most important section in this repo. Most of the value here is behaviour
that must stay exactly as it is.

- Which behaviour stays byte-identical?
- Which defaults must not move?
- Which tests must pass unmodified?

If the change touches order placement, closing or sizing, list every affected
surface here and note that it needs owner sign-off plus a demo session.

### "Non-goals"

Prevents scope creep more reliably than anything else. Be specific: "does not
change how lot size is calculated" is useful; "keeps it simple" is not.

## Keep it to half a page

A spec nobody reads is worse than no spec. Four questions:

1. What is wrong today?
2. What changes?
3. **What must not change?**
4. How will we know it worked?

## The test plan comes before the code

Fill in the test-plan table while writing the spec, not after building. If you
cannot describe how you would detect the change working, you do not yet
understand the change.

Include the negative controls: for each assertion, how would you know the test
is capable of failing?

## Status

Update the header as it moves: Draft → Approved → Building → Shipped. A spec
left at "Draft" forever is a decision nobody made.

When it ships, fill in the Verification checklist at the bottom — including
the line about no real or demo order being touched.

## Push it to the notes repo, every time

`docs/todo/` is the private repo `MooreSi/forex-gold-notes`, not this one.
After writing the spec, and after every later update to it (status, results,
decisions), commit and push it there in the same session, whether or not a
code commit follows:

```bash
git private status
git private add todo/NNN-short-name.md
git private commit -F <msgfile>
git private push
```

Stage only your own files. See CLAUDE.md, "Private notes".

## Naming

`docs/todo/NNN-short-name.md`, NNN sequential. Keep the number even if the
spec is abandoned — mark it Abandoned with a sentence on why. That sentence is
often more useful later than the spec would have been.
