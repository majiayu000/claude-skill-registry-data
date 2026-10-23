---
name: wayfinder
description: "Use when a piece of work spans several weeks and stays uncertain (a large migration, a progressive rework): a map of typed Jira tickets rather than one big ticket or a plan frozen up front."
---

# wayfinder

Cross-cutting step, before/alongside `plan` (4): for uncertainty that goes beyond the scope of an
already estimable story. `breakdown` (existing skill) splits a framed story into 1h tasks;
`wayfinder` handles a piece of work whose final shape isn't known yet.

## When
As soon as a piece of work is too big/uncertain for one session, and its complete breakdown can't
be known in advance (progressive migration, rework that sharpens as it goes): never for an
already-framed story (that's `breakdown`).

## Steps

### 1. Parent ticket: the destination, not the detailed path
1. **Destination**: where we want to end up, in one sentence, even if the exact path isn't known
   yet.
2. **Notes**: free-form context that accumulates as things progress.
3. **Decisions already taken**: what is settled and no longer up for discussion.
4. **Not specified yet**: the grey areas identified but unresolved, explicitly listed, never
   implicit.
5. **Out of scope**: what we chose not to do, so a child ticket doesn't drift into it later.

### 2. Typed child tickets
1. **Research**: clear an unknown before being able to move forward (no code deliverable).
2. **Prototype**: check that an approach works, throwaway if needed.
3. **Grilling**: precisely frame an area that's still unclear (close to `spec`).
4. **Task**: concrete, framed work, ready to execute.
5. Every child is linked to the parent by a native tracker dependency (not a plain text link) so
   the tool can visualise what is "frontier" (unblocked, takeable now) vs blocked waiting on
   another ticket.

### 3. One session = one ticket resolved
1. We never work on several child tickets at the same time in the same session: consistent with
   one task per worktree, closed after the merge.
2. The session's report names, per ticket, its outcome, the evidence and any unresolved blocker
   (`skills/dispatch-parallel`, supervision rules).
3. At the end of a session, the parent ticket is updated (notes, decisions, what moved from "not
   specified yet" to "decided").

## Output / checkpoint
A parent Jira ticket with the five sections filled in, typed child tickets created as we go (not
all at once at the start: only what has been identified), linked by native blocking dependencies.

## Guardrails
Don't try to break the whole piece of work down at the start of the project: `wayfinder`
explicitly accepts that the complete breakdown isn't known in advance, unlike `plan`/`breakdown`.
Don't let the parent ticket become an unmaintained catch-all: every session updates it.

## Origin
Rewrite of the `wayfinder` skill from a recognised market skill author: the parent ticket structure
(5 sections) and the 4 child ticket types are taken as-is, adapted to Jira usage (instead of the
original generic tracker) and explicitly distinguished from the already existing `breakdown`.
