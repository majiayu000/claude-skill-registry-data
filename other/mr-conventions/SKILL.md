---
name: mr-conventions
description: Use when opening a pull/merge request, choosing how to merge it, writing its description, or leaving/responding to an inline review comment — the shared shape for how a PR/MR moves from open to merged, independent of host (GitHub PR or GitLab MR).
---

# mr-conventions

Step 8/10 of the pipeline (`WORKFLOW.md`): `ship` opens the PR/MR, `review` produces the comments on
it. This block is the generic shape both draw on — the mechanical parts of `ship`/`finish` (draft by
default, squash + delete) plus what wasn't written anywhere yet: description house style and
inline-comment conventions, both directions.

"PR/MR" below covers a GitHub pull request and a GitLab merge request interchangeably; nothing here
is host-specific.

## When
Opening a PR/MR, choosing its merge shape, writing or updating its description, or writing/responding
to an inline review comment.

## Steps

### 1. Open in draft, promote explicitly
Open the PR/MR as a draft, even when the work is believed finished, and mark it ready-for-review only
once it actually is. A non-draft PR/MR is a signal broadcast to every watching reviewer — "spend your
attention now" — and a still-moving target burns that attention for nothing: a review comment on a line
that gets rewritten five minutes later, a re-review request nobody asked for. This is not about
hiding work from CI: most hosts still run the pipeline on a draft PR/MR exactly as on a ready one — the
draft flag changes the review-request signal, not the build. Promote it deliberately, the same way it
was opened deliberately.

### 2. Squash-merge and delete the branch, as the default
Once approved, merge with squash (one commit landing on the target branch) and delete the source
branch. Two independent reasons: squashing keeps the target branch's history at one commit per
logical change, regardless of how many "wip", "fix typo", "actually fix it" commits happened along the
way; and a branch nobody deletes after merge is dead weight — it doesn't get cleaned up on its own, it
just accumulates until someone runs a bulk-delete script that also catches branches still in use.

**Exception, stated plainly so this isn't read as absolute:** a PR/MR that is genuinely several
independent logical commits — each one something a later reader will want to `git blame` or
`git cherry-pick` on its own, not merely several steps of the same change — is the case where squashing
is the wrong call. That's the exception to name explicitly before merging, not a default to assume.

### 3. Description as prose: symptom, cause, what changes
Run the text through `business/ai-prose-tells` in embedded mode (final text only) before it is posted.

A description that lists "changed X, changed Y, changed Z" restates the diff a reviewer can already
open — it costs the author time to write and gives the reviewer nothing they didn't already have.
Prose that states what was actually wrong, why, and what the change does about it gives the reviewer
the one thing the diff itself can't: the reasoning behind it. A pure feature (no prior symptom) states
what capability is missing and what the change adds, in the same shape.

Concrete contrast, same change:

- **Bullet-list diff summary (avoid):**
  - Updated `retry()` to catch `TimeoutError`
  - Added `max_attempts` parameter
  - Updated call site in `worker.py`

- **Prose, symptom/cause/what-changes (house style):**
  A job silently stopped retrying after a single timeout instead of the configured number of attempts,
  because `retry()` only caught `ConnectionError` and let `TimeoutError` fall straight through as an
  uncaught failure. This adds `TimeoutError` to the caught set and exposes `max_attempts` so callers
  stop being stuck with the hard-coded default; `worker.py` is updated to pass its own value.

Three more lines belong in the description when they apply, because the diff cannot show them:

- **Why this approach and not the obvious other one**, in a sentence, when a reviewer would otherwise
  propose the other one in the first comment.
- **Before and after, shown, for anything a user can see.** A screenshot or a recording of the old and the new
  behaviour; for a change with no visible effect, the command or the output that shows it.
- **How it was tested**: the commands that were run and what they showed, not "tested locally". A residual item
  (`skills/ship`, go-live) and an omission chosen on purpose ("not handled: X, add when Y") end the description.

### 4. Inline review comments: plain text, short, direct
**Writing one, as a reviewer.** Plain text — no markdown formatting, no backticks around identifiers,
no emojis, no decorative arrows. State the problem and, where it isn't obvious, what would fix it, in
one or two sentences. A comment padded with justification, alternatives considered, or a restated
explanation of what the code already does buries the one sentence that matters under text a busy
reviewer skims past. Rank correctness above style; a wrong or unsourced comment costs more credibility
than the issue it claimed to catch, so verify before posting rather than after.

Contrast:

- **Avoid:** "I think there might possibly be an issue here with userId — have you considered that
  getUser() could maybe return null in some edge cases? Might be worth double-checking!"
- **House style:** "getUser() can return null here; this will throw on the next line."

**Responding, as the author.** Every comment gets one of two outcomes, never silence: fix it, or push
back with a stated reason ("intentional — see the guard three lines up", "out of scope for this
PR/MR, filed as a follow-up"). An unanswered comment left to be silently overwritten by the next push
is indistinguishable, to the reviewer, from having been ignored. How to arrive at the outcome (read all of it,
verify against the code, stop on an unclear item, no performed agreement) is `skills/receiving-review`.

### 5. Optional: linking to an issue tracker
Some teams require every PR/MR to reference the issue/ticket it closes. Where a project's own house
style requires that, follow it — but it is a per-project convention layered on top of the shape above,
not a default this block prescribes. Absent such a requirement, don't invent one.

### 6. Commit messages
The subject is `type(scope): summary` in the imperative ("add", "fix", "remove"), lowercase after the colon, no
trailing period, aiming at fifty characters and never past seventy-two. A body appears only when it carries what
the diff cannot: the reason when it is not obvious, a breaking change, a migration step, the identifier of the
issue it closes. It never says "this commit", never restates the file the scope already names, carries no emoji,
and is wrapped near seventy-two columns. Breaking changes, security fixes, data migrations and reverts always
get a body, so that whoever bisects to the commit in a year has the context. The subject length is checkable
by a commit-message hook, which is where the rule is best kept.

## Output / checkpoint
No dedicated checkpoint of its own — folds into `ship`'s `mr_draft_pushed` (draft-by-default, the
merge shape) and `review`'s `reviewed` (the comment conventions). A human judgement call, not a
fresh-context-verified gate: nothing here is machine-checkable pass/fail, so it never blocks a step
the way `gate` does.

## Guardrails
- Never treat "draft" as a way to skip CI — it changes who gets notified, not what runs.
- Never squash a PR/MR whose commits are independently meaningful without naming that exception first.
- Never post an inline comment that only restates the diff, or one padded with hedging language that
  buries the actual point.
- Never leave a review comment unanswered across a push — fix it or state why not.
- Never write a commit subject past seventy-two characters, or a body that retells the diff.
- Never invent a ticket-linking syntax as if it were a universal standard; that's a per-project
  override, not this block's default.

## Origin
No external source: assembled from recurring cross-project practice, not mined from the org catalogue
(which has no equivalent skill) — a process convention rather than a technical mechanism, so treat
items here as defaults to override with a project's own stated house style where one exists. The
draft-by-default and squash-and-delete mechanics were already partially stated inline in `skills/ship`
and `skills/finish`; this block is their generic home plus the two conventions (description prose,
inline-comment style) that weren't written down anywhere before.

The three description lines of §3, the commit format of §6 and the pointer to `receiving-review` were added
2026-10-02. The commit format is the shape of the `caveman-commit` skill of `caveman` (Apache-2.0, read that
day: imperative subject, length bounds, body only for the non-obvious why), rewritten with our lowercase
convention and without its compressed register. The description lines come from the pull-request guidance in
the contributor notes of `orca` (MIT, same date): the alternative rejected, visible before and after, the test
that was run. No text copied.
