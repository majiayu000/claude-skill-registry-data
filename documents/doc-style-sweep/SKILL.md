---
name: doc-style-sweep
kind: pattern
rule: doc-style
description: Pattern of rule doc-style. Load when a document has accumulated a list of work and must be sorted into what still holds and what is closed. The selection sign, a pass over the statements, a check against the work queue, the fate of the file itself. New text — pattern doc-style-write.
---
<!-- rt-kit v0.34.0 · patterns/doc-style-sweep.md · cf4050498eb4 · правится надстройкой, не здесь -->

# Sorting a document that has accumulated a work list

Pattern of the rule `doc-style`. What must be true — the law
`docs/constitution/project-documentation.md`, the article saying that upcoming work is listed
in one place.

## When to use

- A document lists what is left to do, and the work queue lists the same.
- The file has grown so much that nobody reads it whole any more.
- Plans lie mixed: some carried out, some not, and the text does not tell them apart.

## The selection sign is one, and it is decided before the first edit

**A statement stays in the document if nobody intends to change it.** Everything else is work,
and its place is the work queue.

| What was found                                                        | Where it goes                                                  |
| --------------------------------------------------------------------- | -------------------------------------------------------------- |
| a hole that will be fixed                                             | a task; the line leaves the document                           |
| a hole it was decided not to fix                                      | stays, together with the reason                                |
| a conditional refusal ("we will add it if the case turns out common") | stays                                                          |
| a conclusion of a review that did not become a rule                   | stays                                                          |
| a description of what was done                                        | removed without transfer: closed tasks and history speak of it |
| a statement that diverged from the tree                               | removed as stale, not transferred into a task                  |

There is no need to ask the owner about this set — it is written here. One thing is worth
asking: the fate of the file itself, once nothing is left in it.

## The pass goes by statements, not by items

Work lies in prose too. The "Requests screen" section listed missing anchors as running text,
without a single bullet, and a pass over `- ` would not have seen it.

```bash
# how much of what is in the file: items, paragraphs, sections
grep -c '^- ' docs/BACKLOG.md
grep -c '^## ' docs/BACKLOG.md
```

A paragraph is judged by the same sign as an item.

## A task number stands in three places

Before counting "items without a task", all the forms of writing it must be known. In this tree
there are three:

```markdown
## Section — #149 ← in the heading

**Тикеты:** #163, #164 ← a separate line at the section or subsection

- An item about a defect. #101 ← at the end of the item
```

A review that knows one form errs silently: "51 items without a task" turned out to be six. **A
number obtained by parsing text is verified on a sample by hand before it is stated.**

## The check against the work queue

An item has a task — that does not yet mean the task carries its content. Before removal the
coverage is measured: how many of the item's significant words occur in the body of its task.

```bash
/opt/homebrew/bin/gh issue list --state all --limit 400 --json number,title,body,state > /tmp/issues.json
```

An item covered by the body half or less is read by eye and sorted into three outcomes:

- a live detail the task lacks — appended to the body;
- a different defect — filed as its own task;
- stale — removed, **not** transferred. Otherwise the review puts a lie into the task: "the guard
  does not check the kit directory" had nowhere to be transferred, the directory no longer
  existed.

**Inheriting a number from the heading is an assumption, not a fact.** An item under a heading
with four numbers belongs to none of them: the link is checked by reading.

## Doneness is read from the tree

A statement that a task is not done ages like any other. Twice in one review something stale was
named current: the unread marker was already shipped by the kit, and half of the task about the
skills gate was done and covered by scenarios.

```bash
# check what you are about to call "not done"
grep -rn '<symbol>' libs apps .claude/hooks
grep -n '<name>' node_modules/<package>/types/*.d.ts
```

## Arguments for deferring are "what it costs"

The "what is worth deferring" section moves not to the archive but **into the bodies of the
tasks it concerns**: there it is the cost estimate. It stays in the file only if the deferral is
the owner's decision, not the review's proposal. The sign is the owner's recorded answer with a
date; without it — a proposal.

## Links to removed sections

A task whose body says `**Источник:** <document>, раздел «…»` leads into the void after the
review, and the path check does not see it: it reads repository files, not task bodies. The
line is removed in the same session.

## The fate of the file

- Something non-task is left — the file lives, and its preamble declares the new selection sign.
- Nothing is left, and the document described work that took place — it moves to
  `docs/archive/`.
- Nothing is left, and it was a work list — it is deleted.

The whole review is one task and one branch: what splits is what would have to be reverted
separately, and here the revert is shared. A code edit found along the way does not go into this
branch — otherwise reverting the review carries the fix away.

## What gets fixed in the tree next

The document is not the only place promising that the work lives in it. A removed name is purged
by one grep, including agent descriptions, skills, READMEs and code comments:

```bash
grep -rn 'BACKLOG' --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=archive .
```

## Common misses

- A pass over bulleted items: half the work lies in prose and survives the review.
- "There is a task for this" without reading its body: the item is removed, the content is lost.
- The number of items stated to the owner before verifying on a sample.
- A stale statement transferred into a task and turned into a current instruction.
- Arguments for deferring left in the document: it becomes a second work list again.
- The review split into several tasks "by size" — the sign for splitting is not size but a
  separate revert.
- The archive touched: it describes the state as of writing and is not edited for new terms.
