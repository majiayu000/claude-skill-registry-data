---
description: "STUB — not yet hydrated for this project. Dispatch the test buckets that can't run on the agent's machine to CI on this branch, and block for the result. Hydrate this file against the project's CI workflows and test-bucket split before invoking it."
---

> ⚠️ **STUB.** This skill has no working procedure yet. Before it can be
> invoked, fill in: which test buckets exist and which of them can't run
> locally, the workflow that runs each, how to dispatch it against the current
> branch, and how the dispatch is scoped to the diff. Delete this banner once
> you have. If every test in the project runs locally, delete the skill instead.

## What this skill is for

Running the tests the agent's own machine cannot run — the ones needing real
credentials, real third-party services, a real database, or a browser — by
dispatching them to CI on the current branch and waiting for the verdict.

## Concerns that hold regardless of stack

Each is something a hydrated version must handle.

### Name what can't run locally

The split is the whole premise. Enumerate the buckets and say, for each, what
makes it undispatchable locally. A bucket that could run locally and doesn't
belongs in `./scripts/vet.sh` instead.

### Dispatch on the branch, block for the result

The run must be against the branch's current head, and the skill must not return
until it's terminal. A fire-and-forget dispatch is worse than none: it produces
the feeling of coverage with none of the fact.

### Scope to the diff

Select the tests the change actually reaches, so cost scales with the change
rather than the suite. But note the trap this creates: a scoped run of a bucket
the diff never touches selects nothing and passes — which reads identically to
real coverage unless the report says "selected 0".

### Cheap-always vs. expensive-on-demand

Separate the buckets worth dispatching on most branches from the ones (full
browser matrices, long-running integration sweeps) that need a specific reason.
Say what that reason looks like, so the expensive lane is neither reflexive nor
never-used.

### Green local proves nothing here

The most important line in the hydrated skill. `./scripts/vet.sh` passing says
nothing about an undispatched bucket, and an attestation that implies otherwise
is a false record.

## Related

`/finalize` Step 6 decides from the diff whether to dispatch, and its
attestation comment names what ran and what didn't. `/qa-checklist` marks rows
whose backing tests live in a CI-only bucket, so a cluster of them is the signal
to dispatch. `/watch-ci` re-attaches to a dispatch left running. If the first
dispatch of a freshly written workflow fails with
`workflow ... not found on the default branch`, that is GitHub's metadata, not
your hydration — `/bootstrap-workflow-dispatch` clears it.
