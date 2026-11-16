---
description: "STUB — not yet hydrated for this project. Ship an urgent fix straight to production, bypassing the normal promotion path, then reconcile it back into the trunk. Hydrate this file against the project's actual branch topology and deploy setup before invoking it."
---

> ⚠️ **STUB.** This skill has no working procedure yet. Before it can be
> invoked, fill in: which ref represents what is live, how a branch is cut from
> it, how the fix reaches production, how it gets reconciled back into the
> trunk, and where the record of it lives. Delete this banner once you have.

## What this skill is for

Getting a fix in front of users **now**, when waiting for the normal release
path is not acceptable — and doing it without leaving the branch topology in a
state where the fix silently disappears later.

It exists because "is the trunk safe to ship right now?" is a question you
cannot always answer yes to. If the trunk has half-finished work on it, shipping
from the trunk to fix one bug ships everything else too. The hotfix path is the
answer to that, and it is _only_ worth having if the project's trunk can be in
that state.

## Concerns that hold regardless of stack

### Branch off what's live, not the trunk

The whole point is to avoid carrying unrelated in-flight work. Cut from the ref
that represents production — a branch, a tag, the deployed SHA — never from the
trunk. Hydration must name that ref precisely.

### It bypasses the promotion path

Whatever staged gauntlet the normal release runs, this skips most of it by
design. Say explicitly which checks still apply. A hotfix that skips
_everything_ isn't fast, it's unreviewed.

### Reconcile back into the trunk, or lose it

A fix that only exists on the production ref gets overwritten by the next
ordinary release. Merging it back into the trunk is part of the procedure, not a
follow-up someone might remember — and the skill should not report success until
it's done or explicitly deferred with an owner.

### It needs a durable record

Hotfixes happen under time pressure and are the changes least likely to be
written down. Decide where the record goes (a notes file, an issue, a PR that
stays open until reconciled) and make writing it non-optional.

### Scope discipline

The urgency that justifies the bypass applies to one fix. Anything that rides
along on the branch inherits a review path it didn't earn. Keep the diff minimal
and say so in the report.

## Related

`/release` is the ordinary path this one deliberately steps around; hydrate that
first, since this skill is defined by what it skips. `/squash-message` expects a
hotfix body to be one or two paragraphs — short, not padded out to look
substantial.
