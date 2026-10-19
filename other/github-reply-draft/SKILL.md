---
name: github-reply-draft
description: This skill should be used when drafting reply text for GitHub PR review threads or review comments — ensuring replies are terse, reference only committed symbols, are scoped per thread, and include the required attribution footer.
---

<!-- mkdocs-include-start -->

# GitHub Reply Draft

**Owner**: — (orchestrator/agent drafting GitHub replies)
**Consumers**: `/maigo:address-comments` (per-thread replies at Finale), `/maigo:review` (reply drafts at criti gate)

## Overview

Drafting GitHub PR replies badly is a recurring source of reviewer friction.
Common failure modes: long preambles, referencing mid-iteration helpers that
were deleted before merge, merging all threads into one PR-level comment,
or overclaiming that a thread is "done ✅" when the reviewer has not yet
confirmed acceptance.

This skill captures the six conventions that prevent those failures.

## Convention 1 — Default terse

The opening sentence names what changed. If there is a deliberate trade-off,
one more sentence names it and signals the user can ask for more detail.
Cut: preamble, restating the reviewer's comment, hedging phrases
("hopefully this addresses...", "I believe this should..."), verification
narrative ("I re-ran the comparison and got the same result"), the process
of what was done, and anything the reviewer can already see from the diff.

The user will ask for more, not less — default short.

**Word-level conventions:**

- Prefer an em-dash over `, so` for casual flow (`reports should stay in sync from now
  on`, not `, so reports should stay in sync`).
- No comma after a sentence-starting `Also` before a verb (`Also updated the file`, not
  `Also, updated the file`).
- Avoid vague abstract nouns ("window", "a while", "soon", "some buffer") — swap each for
  the concrete, quantifiable mechanism behind it (a number of seconds, a count, an
  explicit configurable flag). A vague noun reads as hand-waving; a measurable mechanism
  is something a reviewer can actually evaluate and implement.
- Never close a reply with `Acceptance pending your review.` or any variant of
  "waiting for your confirmation" — whether to accept is the reviewer's call by
  definition; writing it out is zero-information filler. State what changed and stop.
- Never open with `You're right.` or another flattering opener ("good question",
  "great catch") — start directly with what changed.

**Good:**

> `validate_email` now raises `ValueError` on empty input instead of propagating `IndexError`.

**Bad:**

> Thank you for catching this. I've reviewed your comment about the empty-input
> case on `validate_email` and I believe I've addressed the concern by adding...

## Convention 2 — Describe the change, never cite a commit SHA

Reference the change by symbol or behavior description, not by commit hash.
Rebase and force-push rewrite all commit SHAs; a draft that cites a SHA will
contain an unresolvable orphan link on GitHub the moment the branch is rebased.

**Good:**

> `has_partition_selectors` is now a property on the shared mixin instead of a
> per-subclass attribute.

**Bad:**

> Fixed in `5ab9ca3`.

## Convention 3 — Only name symbols present in the final committed diff

Before presenting a draft, cross-check every code token against the net
committed diff. Remove any reference to helpers tried and deleted mid-iteration.

Reviewers look up symbols you name. A symbol that does not exist in the final
code makes the draft look inaccurate and erodes trust.

## Convention 4 — One reply per thread, never a combined PR-level summary

GitHub's "Resolve conversation" button is per-thread. Collapsing multiple threads
into one PR-level comment breaks that workflow.

Structure:

- List threads by comment ID / URL
- One acknowledgement per thread — name the function or location of the fix,
  not a raw line number (line numbers shift on rebase)
- A PR-level comment is acceptable *in addition to* per-thread replies only when
  there is cross-thread context (e.g. "rebased + force-pushed, please re-review"),
  and it must not replace the per-thread replies

## Convention 5 — Do not overclaim a comment as "done ✅"

Distinguish between:

- "we changed code to address this" — the implementer's claim
- "reviewer accepted" — only confirmed when the reviewer presses Resolve

A thread becoming `outdated` because of an edit is not the same as resolved;
the reviewer has not clicked Resolve yet. State what changed and what deliberate
trade-off was made (if any), then stop — whether to accept is the reviewer's
call, not something the draft narrates.

A draft carried over from an earlier session or round is a claim about the
diff *as it was then*. Before handing it over again, re-check every universal
statement in it ("every resolved anchor exists", "no other provider changed",
"all callers") against the commits landed since: a later commit that widens
the set turns a verified claim into an overclaim without changing a word of
the draft. Re-verify it for the new set, or narrow it to what was verified.

**Good:**

> Changed `_serialize_keys` to return a `frozenset` (was `list`). Trade-off:
> callers that relied on ordering will need adjustment — flagging here in case
> that affects your side.

**Bad:**

> Done ✅ — fixed as suggested.

## Convention 6 — Include the attribution footer

Every reply drafted by an agent must end with an attribution footer on its own
paragraph, separated from the body by a blank line and a horizontal rule.
Use the wording appropriate to whether a human reviewed the draft before posting:

- Agent draft, posted without prior human review:

  ```
  ---
  Drafted-by: <Agent Name and Version> (no human review before posting)
  ```

- Agent draft reviewed and approved by a human before posting:

  ```
  ---
  Drafted-by: <Agent Name and Version>; reviewed by @<github-handle> before posting
  ```

The attribution footer is in addition to any other disclosure in the PR body;
never skip it to shorten a message.

## Comment fetch & triage, and pre-apply verification (references)

The `gh`/GraphQL queries for pulling inline threads, review summaries, and
conversation comments, the triage-file template, and the routing table for
turning selected comments into `/maigo:quick` vs `/maigo:go` work items are
in `references/comment-fetch-and-triage.md`. The same file also covers two
pre-apply verification habits: running a full before/after check on a
reviewer's *suggested* fix (not just their cited example) before applying it
literally, and checking PR review threads before a "unify / clean up" sweep
touches a line you didn't write — it may be a reviewer-directed change
already landed via `fixup!`.

Draft-shape rules (GitHub `suggestion` blocks for concrete fixes, one bullet per reviewer point,
a draft for every listed thread, design replies that pitch differentiation) live in
[`references/draft-shape.md`](https://github.com/Lee-W/maigo/blob/main/skills/github-reply-draft/references/draft-shape.md).
