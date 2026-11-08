---
name: doc-style-trace
kind: pattern
rule: doc-style
description: Pattern of rule doc-style. Load when the completeness of texts is checked from the side of the work — a reverse pass over closed tasks, the machine selection sign, what it does not see, three outcomes per task. Sorting one document — pattern doc-style-sweep.
---
<!-- rt-kit v0.34.0 · patterns/doc-style-trace.md · 066a49f1c769 · правится надстройкой, не здесь -->

# The reverse pass: closed tasks against texts

Pattern of the rule `doc-style`. What must be true — the law
`docs/constitution/project-documentation.md`.

## When to use

- What is checked is not whether a text is right but whether it exists at all.
- Work is reviewed that was closed before the step of bringing texts up to date entered the
  closing of a task.
- A wave of review from the side of the text has ended, and it yielded few findings.

## A pass from the side of the text does not find what was not written

It reads what is written and judges every statement; a statement that does not exist is not in
the pass either. From the side of the work there are ten times more findings: in the first part
seven findings out of eight landed where there was no text at all, not where it was stale.

## The selection sign — the branch added code and touched no text

Selected by the machine, no reading required. What the branch really added is answered by
history, not by the task folder: the folder is taken apart at closing, and the task footprint
table never reaches the main branch at all.

```bash
git log --merges --format='%H %s' <main branch> | grep -E 'from [^/]+/<task key>-[0-9]+-'
git diff --name-only <merge>^1 <merge>
```

The sign is computed by subtraction, not by two path lists: code is everything that is not
`.md`, text is any `.md` outside the archive and the task folders. Hand-written lists diverged at
both edges at once, and diverged silently.

The text list missed the most-read texts of the tree: the one that enters the context of every
session whole, and the one that describes the tree's structure. Three tasks that touched exactly
those made the sample as traceless — and made the second part of the pass a second time, now as
having touched text.

The code list missed the plumbing: guards, the pipeline and the rollout files were not on it, and
two tasks that edited only those made no sample at all. They were found not by the sign but by
checking the two samples against each other — and that check is worth running before every next
part:

```bash
comm -23 <traceless list> <reviewed by the first part>       # whom nobody read
comm -12 <reviewed by the first part> <list of those that touched text>  # who was read twice
```

## The part is assigned by the narrowest area of the task, and sometimes there is no label at all

The sample the sign selected cannot be read in one session, and it is split by area — the task's
area label. A task can have several labels; the part is assigned by the narrowest, and the
narrowing order is chosen once for the whole pass and written into the plan together with the
table of parts. In the reverse order the widest areas would take all the disputed tasks, and
almost nothing would be left for the narrow ones.

A task without a single area label falls into no part at all — under any narrowing order. The
sign selected it, nobody is there to read it, and this shows only by recounting:

```bash
awk -F'\t' 'NR==FNR{k[$1]=1;next} k[$1] && $2==""{print}' <sample numbers> <tasks with labels>
```

Such a task is assigned to a part by subject, by hand, and the decision is written into the
review: otherwise the next part recounts the sample and finds it unread again.

## A task has three outcomes, not two

| Outcome           | Sign                                                                                                                 |
| ----------------- | -------------------------------------------------------------------------------------------------------------------- |
| needs no trace    | the technique is repeated nowhere: layout of its own screen, a one-off edit at the owner's request                   |
| there is a trace  | a statement about the work stands in a rule, a pattern or a spec — including one added by a separate task afterwards |
| there is no trace | the technique is applied and described nowhere — that is the finding                                                 |

A technique written down by a separate task afterwards is not a miss: the work was done by one
task, the record of the technique was created by another, and both are visible in the work
queue. This is told by reading the neighbouring tasks of the same area close in time, not by the
sign.

The worst case the sign does not see at all: the branch touched a neighbouring text and bypassed
the one describing its own work. Such tasks are left to the next part of the pass.

## The boundary "code is not edited" and its only exception

A place was found where the code is wrong — a task is filed, the pass goes on. What describes
the audited rule does not count as code here: the comment in a check's header and the test
title. The title carries the scenario identifier, and without it a new scenario shows as not
covered while the test is alive.

## A finding goes into the layer it belongs to

- the technique is repeated and decided in code — a rule statement with a binding in the tree's
  names;
- ready-made code and an order of actions — a pattern;
- a promise a person sees — a domain spec scenario with the existing numbering;
- a divergence from the agreement — the article text to the owner, the law file is not edited.

## Common misses

- The composition of a part taken from the previous session, not recomputed by the sign.
  Samples live in the session's scratchpad and die with it; they are not put into the tree — the
  split into parts is a trait of the pass, not of the product. A recount costs the two commands
  above and gives the same list, while a composition taken on trust cannot be checked against
  the neighbouring parts — and it is that check that finds those nobody read.
- A task is judged by its folder: it was taken apart at closing, and no trace was left there.
- "There is a trace" by a single mention: a mention in a neighbouring rule does not describe the
  technique.
- A finding written only into a pattern: the rule is read before every edit, the pattern by
  name.
- The sign recomputed on a new path list without checking on a sample by hand.
