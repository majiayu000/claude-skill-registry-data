---
name: decide-boundary
description: Is this one project or several? Fires at charter, authoring, and verdict.
---

# Skill: Decide Boundary

> "A brief often holds several projects wearing one name."

## The Question

**Would this piece make sense if the request had never existed?**

Most pieces that survive it outlive the request. Some become packages.

## The Test

Two halves. Both must pass.

| Ask | Fails when |
|-----|------------|
| Does it **survive** alone? | it means nothing without the request that produced it |
| Does it **stay correct** alone? | standing alone breaks a guarantee it only held in company |

The second gets missed. A review method separated from the thing that supplies its reviewer still
runs — and now grades its own work.

## The Tells

These surface only in code. The charter gate cannot see them.

| Tell | Reading |
|------|---------|
| the same shape written a third time | it wants to be one thing, elsewhere |
| one file, two unrelated reasons to change | two charters sharing a filename |
| a test needing setup from a concern it doesn't test | the boundary already leaks |

**Any of these outranks the finding you were about to write.** Three findings about symptoms of one
mis-sized boundary is three wasted rounds and a missed call.

## Elsewhere, Not Alone

| Tell | Move |
|------|------|
| it fires more often than its host | extract upward, into whatever is always on |
| it activates differently — always-on vs deliberately invoked | a different home, not a sub-part |

## The Signals

- **Needed twice already** in the work in front of you.
- **Cost asymmetry** — extracting now is nearly free; extracting once both callers exist is not.

## When It Fires

| Time | Outcome |
|------|---------|
| charter | name the pieces; the human chooses the split |
| authoring | stop and say so — cheaper than a judge finding it three rounds later |
| verdict | `SPLIT` — returns to the charter, not to the author |

Never silently build several things under one name.

## Examples

See [examples.md](examples.md).
