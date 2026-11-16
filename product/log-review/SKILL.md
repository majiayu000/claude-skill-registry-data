---
description: "STUB — not yet hydrated for this project. Read the deployed application's logs since the last review, report what they say about how it's actually being used, and triage what looks broken. Hydrate this file against the project's logging and hosting setup before invoking it."
---

> ⚠️ **STUB.** This skill has no working procedure yet. Before it can be
> invoked, fill in: where logs live and how to query them, how the review window
> is determined, and where triaged findings go. Delete this banner once you
> have.

## What this skill is for

Two different jobs that share one input:

- **A qualitative readout** — what are people actually doing with this thing?
  Which paths are hot, which features nobody touches, where do sessions end.
  This is the part that can't be replaced by an alert.
- **Health triage** — what's erroring, how often, and is it new.

Both come from the same log sweep, which is why they're one skill rather than
two.

## Concerns that hold regardless of stack

Each is something a hydrated version must handle.

### A window since the last run

Reviews cover a period, and the period has to start where the previous one
ended. Decide how that boundary is recorded (a timestamp in a tracked file, the
last review's issue, a cursor) — without it, every run either re-reports the
same week or silently skips days.

### Two outputs, kept apart

Don't fold the usage readout into the error list. They have different readers
and different half-lives: the readout informs product decisions, the triage
produces work items.

### Dedupe into tracked issues

A recurring error should attach to the existing issue for it, not generate a new
report every review. Say how a finding is matched to an existing issue and what
happens when it doesn't match (`/propose-issue` is the natural chain here).
Whatever query does the matching, **cap it at or above the population it reads**
— issue listings come back newest-first, so a cap below the count silently drops
the oldest, which is the long tail the read exists for.

### A recurrence is not automatically a regression

Before reopening a closed issue, establish whether the fix was actually
_running_ when the problem recurred — merged is not deployed. A recurrence while
the fix still sits on the trunk is expected, and reopening on it is churn that
repeats every run until the release train catches up. Name the two cheap reads
that settle it (an ancestry check against whatever ref production ships from;
whether any deploy landed inside the window at all), and say what each outcome
does — reopen, comment-only, or flag as ambiguous.

### The readout series is itself a backlog

Reviews that never close their own output accumulate near-identical open issues.
Decide when a _previous_ readout closes — "every finding it filed is resolved"
is the workable rule — and never let a run close its own, since something has to
stay open for a human to notice the run happened.

### A claim about the series needs a read of the series

A run reads one window, so it cannot ground "the first time", "the quietest
yet", "this is new". Either check the claim against the whole readout history
before writing it, or don't make it.

### Interactive vs. unattended

Run by hand, the skill can ask the operator to judge an ambiguous pattern. Run
on a schedule, it can't — it must decide, or file something the operator can
decide from later. Say which mode is which and what changes between them.

### PII when quoting

Logs contain user data, and a readout persists indefinitely somewhere with
different access rules than the logs. Naming which fields are off-limits is
**not enough** — that bar gets cleared by prose that still recounts a user's
situation. Give the redaction an operative test the writer applies to their own
sentence: _could a reader who has never seen the logs reconstruct any part of
this user's actual situation from it?_ If yes, it's too specific, however
innocuous the subject feels. Describe by kind (domain × task-type), not by
substance, and say which sections the test binds in — it's every section that
paraphrases user content, not just the obvious one.

### Identities are a separate surface from content

An email, name, or account label is what turns a category-level observation into
a disclosure about a traceable person — and a readout is read at a glance, on a
shared screen or in a chat unfurl. Decide how identities are hidden, and make it
something the readout is _born_ with rather than a pass applied afterwards. Two
properties are worth designing for: **determinism**, so the same person reads as
the same ref across windows with no registry to maintain; and
**hidden-but-not-removed**, so an agent or an API query can still resolve a ref
while a viewer can't read it (on GitHub, a collapsed `<details>` block does this
— there is no inline spoiler syntax). Keep the category coarse wherever it sits
next to a ref: a ref plus a fine-grained category is still a disclosure.

## Related

`/propose-issue` is the natural sink for triaged findings — it dedupes against
existing open issues rather than filing another copy.
