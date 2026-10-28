---
name: backlog
description: "Grooms an open backlog before the next task is picked: finds issues that are the same work, adopts orphans into the epic they belong to, and proposes what can ship in one pull request. Read-only until the user approves each move. Use when the board feels like it only grows, before planning a sprint or picking the next issue, or on /backlog [epic-number]."
---

# backlog: make the board readable before working from it

A board that reads as an endless list is usually not a board that is growing. It is
a board whose structure is invisible. Measured on 2026-08-17 in the repository this
was built against: 18 open issues, 107 created against 108 closed over ten days, so
flat. What made it feel endless was one epic with ten open children across three
levels, and two issues with no parent at all sitting next to them as flat rows.

So this skill does not delete work and does not close issues to make a number go
down. It answers three questions with evidence, and every move needs the user's yes.

Input: an epic number, a label, or nothing, in which case groom the whole open
backlog.

## What it may and may not do

- **Read freely.** Issues, bodies, labels, the sub-issue tree, the diffs of anything
  already merged.
- **Propose in writing**, grouped, with the evidence under each proposal.
- **Act only on an explicit yes, one group at a time.** Adopting a child, editing a
  title, adding a label, commenting, closing as duplicate: each is a separate ask.
- **Never close an issue as "stale" or "probably done"** without naming the commit
  or pull request that did it. An issue closed on a guess comes back as a bug
  report.
- **Never merge two issues by deleting one.** The surviving issue absorbs what the
  other one knew, in a comment, and the closed one points at it.

## The three questions, in this order

### 1. Is this already on the board

For each issue in scope, the overlap against every other open one (with no `kit` on
PATH, every `kit` here means `${CLAUDE_PLUGIN_ROOT}/scripts/kit`):

```
kit issues related "<title>" --files <files the body names> --parent <epic>
```

The score is rarity-weighted, so a file every issue names counts for almost nothing
and a file two issues name counts for a lot. Read the verdict, then read the issue
it names. **Two distinctive source files in common is the same work**: the proposal
is one issue absorbing the other, or both delivered in one pull request.

What this is not: a licence to merge on wording. Two issues that share a document
and a subject word are usually two issues. In the measured backlog the maximum
source overlap between open slices was three files at a Jaccard of 0.38, and the
correct conclusion there was to leave the slicing alone.

### 2. Is it an orphan

```
kit issues orphans
```

Neither an epic nor a child. Each one gets a proposal: adopt under the epic it
belongs to, promote it to an epic if it has real children hiding in its prose, or a
written line in the issue saying why it stands alone. "It is small" is not that
reason; a small issue under an epic is one line in a tree instead of one row in a
list.

### 3. Can several ship together

```
kit issues tree <epic>
```

Group the open children by their file scope. A group whose files barely intersect
stays as separate pull requests, and saying so is a result: it is what stops the
next planning round from re-asking. A group that touches the same files in the same
layer is one pull request, and the proposal says which issue leads and which ones
close with it.

Two things override any grouping: a dependency the issues state themselves, and
size. A combined pull request that no longer fits one review is worse than two, and
the funnel's own sizing rule applies here unchanged.

## What to write

One document, in the language of the conversation, with a section per proposal:

| Field | Content |
| --- | --- |
| Proposal | adopt, absorb, group, split, close, or leave alone |
| Issues | the numbers, and which one survives |
| Evidence | the shared files, the commit that already did it, the dependency |
| Cost of doing nothing | what the next person misreads if this stays as it is |

End with the counts: open before, open after if every proposal is accepted, orphans
before and after, and the deepest level of the tree. Those four numbers are what
tell the user whether the board got more readable, and they are the only claim here
that is not a judgement.

Then stop and wait. This skill ends in a proposal, not in a groomed board.
