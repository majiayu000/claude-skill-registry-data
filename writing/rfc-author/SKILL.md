---
name: rfc-author
description: When a change needs an RFC in docs/rfc and how to write one that survives. Use when a change contradicts something already written in docs/design, when reversing an earlier decision, when widening any policy allow-list, and whenever a future contributor would otherwise re-litigate the choice being made.
---

# RFCs

`docs/design/` is rewritten as the design moves, which means the *reasoning*
survives and the *reversals* do not. `docs/rfc/` holds the reversals. Entries
are append-only; a superseded RFC is marked superseded, never edited away.

## When one is needed

- The change contradicts something already written down in `docs/design/`.
- It reverses an earlier RFC.
- It widens a policy: a new `DETERMINISM_ALLOW` path, a crate added to
  `UNSAFE_ALLOW`, a new way into `third_party/`.
- A future contributor would otherwise re-litigate it — which is most cases
  where two reasonable engineers would pick differently.

Not needed for: an implementation that follows a decision already recorded, a
bug fix, or a number (that is a claim, not an RFC).

## Writing one

Copy `docs/rfc/0000-template.md`. Numbering is sequential and permanent.

The section that carries the weight is **What would reverse this**. An RFC with
nothing there is a preference wearing a decision's clothes, and that phrasing is
in `CONTRIBUTING.md` because it is the failure mode. Write an observation
somebody could actually make: a measured number crossing a stated line, a
dependency that fails to materialise, a class of bug appearing that the decision
was supposed to prevent. RFC 0001 does this well — it names 10% unsafe code as
its own reversal condition.

**Decision** is one paragraph, stated so somebody can disagree with it. If it
cannot be disagreed with, it is a description rather than a decision.

**Context** is what was true when this was decided, including which alternatives
were live. The alternatives are what make the entry useful in two years; without
them a reader can only conclude that the author did not think of anything else.

**Consequences** says what this makes easy, what it makes hard, and what it
forecloses. All three. An RFC listing only the first is advocacy.

## Superseding

Add a new RFC. Mark the old one `Status: superseded by RFC NNNN` and change
nothing else in it. The old reasoning is the record of what we believed and why
it was wrong, which is the more expensive half of the pair to reconstruct.
