---
name: craft-swimlane
description: Draw who or what acts at each step, and what crosses between them. Use when a hand-off, an approval, a human touchpoint or an adapter seam is the point. Not for static structure (craft-map), ownerless process (craft-flow), or a call and return trace.
when_to_use: swimlane, handoff, touchpoint, who does what, responsibility boundary
---

# Craft Swimlane

> "A flow shows what happens. A swimlane shows who it happens to, and what crosses."

## Which of the three

| `craft-map` | what exists, where it lives, what each part is for |
| `craft-flow` | what happens next, in what stages, where it branches |
| **`craft-swimlane`** | **who acts, who decides, and what crosses between them** |

**Reach for this when sequence alone hides the answer.** If the important fact is who owns a step, or
what passes a boundary, a flow will not show it.

## One scenario

Name the question, the start and the end. **Never the whole product.**

*How does a request become a merged change?* is a scenario. *The system* is not.

## A lane is a responsibility

Every lane answers the same question: **who or what does the work here?**

**Responsibility is not accountability.** A system can be responsible for work. What that work means
to people stays with a person, and no arrow moves it.

A person, a role, a system, a plugin, an adapter. Never a file, a folder or a step.

Four to six lanes. More than that, and you are drawing two scenarios.

## Time runs down

Lanes sit left to right. Actions descend. Same house style as `craft-flow`.

## Every action has one home

Put each action in exactly one lane. Start its label with a verb.

**A decision lives where it is made**, never where its result is used.

## Every crossing says what it carries

**No bare arrow.** Label what passes.

```
──▶   a request, a work item, a decision, a delivery
╌╌▶   information, an observation, evidence
```

Two arrows and nothing more. **The label carries the meaning.** An arrow never grants authority by
being drawn.

**An artefact carries no authority.** A work item, a delivery and a merge each move work along. None
of them is a yes. Authority crosses only where a named person's recorded grant is the thing being
carried, and the label has to say so.

## A human touchpoint is not always a decision

A person may hand over an observation, a fact only they hold, a constraint, or a decision. **Say
which.** Drawing all four as approval is how a system quietly grows authority nobody gave it.

Where a person does decide, show four things:

| what reaches them |
| the one decision they own |
| what comes back |
| what carries on without them |

**Never a box saying "approval".** Name the trade-off they own. And never add a person where no
meaning, consequence or authority is at stake.

## Adapters live at the edge

Use the names the model uses: work source, execution, judgement, delivery, outcome.

GitHub, a directory, Jira — an annotation at the edge, or a lane of its own only when the adapter
itself is the scenario.

**The same drawing should survive a different work source.** If it does not, you drew the provider,
not the system.

## What is missing is part of the picture

**Do not draw an arrow because two things are installed.** Draw it because one calls the other.

Where two parts meet only through direction, work, evidence and outcome, the gap between their lanes
is the finding. A swimlane that hides it is worse than none.

## Before you publish it

Ask a reader who was not there:

1. Who acts at each step?
2. Who decides?
3. What crosses each boundary?
4. Where does a person get stuck?

**If they cannot say, the drawing failed.** Adding boxes will not fix it.

See [examples](examples.md) — Foundry's own path, and the gap the drawing found.
