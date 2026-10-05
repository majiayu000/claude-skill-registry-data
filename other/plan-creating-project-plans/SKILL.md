---
name: plan-creating-project-plans
description: >-
  Guides authoring the six documents of a formal plan so each answers its own question and the checklist is genuinely
  executable.
when_to_use: >-
  Use when writing a formal plan, after its pre-write decision gate has resolved the material branches.
---

# Creating Project Plans

The structural rules — six documents, one technical shape, ordered companions — belong to the plan convention. This is
about writing ones worth executing. A bug-fix plan is one document whose sections take these roles; the plans
organization policy's Bug-Fix Plan module says what makes each useful.

## Each Document Answers Its Own Question

Each of the six documents answers one question, and a document that answers another's is the commonest defect.

The rest of this section is in
[Each Document Answers Its Own Question](references/document-questions.md#each-document-answers-its-own-question); read
it in full before acting.

## Write `delivery.md` Last

It depends on everything else. Written first, it becomes a checklist for a plan that does not exist yet, and the rest of
the plan is then reverse-engineered to justify it.

A phase that changes what a README, documentation page, or specification describes also carries a
[Docs Propagation](../../../repo-governance/workflows/quality/docs-propagation.md) item, landing in the same commit as
the change.

## Granularity Is the Hard Part

An item should be small enough that failing it is informative. "Implement the validator" fails as a unit; the person
resuming learns nothing about where it stopped.

Two tests:

- **Independently verifiable.** Finishing it leaves something observable — a file, an output, a passing check. If not,
  it is a thought rather than an item.
- **Self-contained proof.** If proving it requires finishing the next item, the split is in the wrong place.

## Write for a Cold Executor

The reader is someone who was not present, has no memory of the discussion, and will not ask. Name paths in full, name
commands exactly, and state what the result should look like.

That reader is also, usually, you — later, having forgotten more than seems possible.

## Acceptance Criteria Must Be Falsifiable

Every criterion carries a stable identifier and states a condition that could fail. "The system is reliable" cannot
fail. "Restarting mid-write leaves no partial file" can.

Criteria that cannot fail are the ones that get marked complete without anyone checking, because there is nothing to
check.
