---
name: plan-validating-quality
description: >-
  Guides judging whether a plan draft is complete, clear, and executable, beyond what structural validation can
  mechanically check.
when_to_use: >-
  Use when auditing a plan draft before execution.
---

# Validating Plan Quality

Structure is checked mechanically. This is about the part that is not: whether a structurally valid plan is actually a
good one.

## Executable by Someone Who Was Not There

The single most useful question about a draft: could a competent person who missed every conversation execute this?

Read `delivery.md` as that person. Where do you have to guess? Which path is named only by description? Which command is
implied rather than written? Each guess is a defect, and each one will be resolved differently by whoever hits it.

## Testable Acceptance Criteria

For each criterion, ask what it would look like if false. A criterion with no failing case cannot be verified, and it
will be marked complete because there is nothing to check.

Then ask the harder question: do the criteria together actually cover the goal in `brd.md`? A plan can have twelve
perfectly testable criteria and still not deliver what it was for.

## Each Document Answers Its Own Question

The common failure is a document that answers someone else's. A `brd.md` that describes the solution has skipped the
argument for doing it at all. A `prd.md` full of tasks has stopped stating outcomes. A technical shape that re-argues
whether the work is worthwhile is defending a decision that was already made.

Read each document alone. If it only makes sense alongside another, one of them is doing the other's job.

## Granularity

Items should be small enough that failing one is informative. Two symptoms of items that are too large: the item cannot
be verified without doing the next one, and finishing it would take longer than a session.

## What This Skill Deliberately Does Not Judge

Whether the work is worth doing. That was settled by grooming and by the pre-write gate, and reopening it inside a
quality gate makes the gate unbounded.

## Findings Must Be Actionable

Every finding names the document, the location, what is wrong, and what would resolve it. A finding the author cannot
act on except by guessing is worse than no finding, because it consumes a repair cycle.

Separate blocking from non-blocking honestly. Treating every finding as blocking teaches people to argue with findings
rather than fix them.
