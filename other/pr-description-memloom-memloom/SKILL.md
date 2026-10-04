---
name: pr-description
description: Write the PR description for a memloom pull request. Use whenever opening or editing a PR body in this repo, including from /ship.
---

# Writing a memloom PR description

A PR describes the change to someone who was not in the room. It is public. Write only what a
reader needs to understand what shipped and what it cannot do.

## Shape

```markdown
<one sentence: what the feature does>

## What this adds
- bullets

## Docs
<one short paragraph, only if docs changed>

## Known gaps
- one sentence each
```

Nothing else unless the change genuinely calls for it.

## Rules

**Open with one sentence.** Not two. The second sentence is always a summary of the bullets
below, which the reader is about to read anyway.

**Bullets, not tables.** A table looks organised and reads slower. Bold the subject of each
bullet and follow it with the fact.

**Every line earns its place.** Before keeping a sentence, ask what the reader does differently
for having read it. If the answer is nothing, cut it.

**Known gaps are one sentence each.** State the limitation, not the history or the plan.

## Never include

| Never | Why |
|---|---|
| A verification or testing section | Tests passing is the default. Nobody reads "686 tests green" |
| What the code review found | Internal. The reader cares what the code does now, not what it did on Tuesday |
| Migration or repair steps for a dev store | Internal. Say it in chat, never in public |
| Commit counts, file counts, line counts | GitHub already shows these |
| Rationale for design decisions | That belongs in code comments |
| Anything phrased as effort or process | "This was tricky", "after several iterations" |

## Voice

Plain short sentences. No em-dashes, no middle dots. Present tense. Name the thing rather than
describing it: "Set a budget and a run keeps going until the backlog is clear" beats "a
configurable budget mechanism has been introduced".

## Before posting

Read it back and delete the weakest third. It will still say everything that matters.
