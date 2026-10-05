---
name: code-review-practices
description: "The single highest-leverage convention in code review is prefixing every comment"
---

# Code Review Practices (Verbose)

## Core Patterns

### Severity Labels Make Reviews Unblockable

The single highest-leverage convention in code review is prefixing every comment
with its severity. Without it, the author must reverse-engineer your intent, and
the safe default is to treat everything as blocking — which is how a two-nit
review turns into another round trip.

| Prefix | Meaning | Author may merge? |
|---|---|---|
| `blocking:` | Correctness, security, data loss, or a contract break | No |
| `question:` | I don't understand; the answer may become blocking | Answer first |
| `suggestion:` | A better approach; author's call | Yes |
| `nit:` | Style, naming, phrasing | Yes, ignore freely |
| `praise:` | Worth keeping and imitating | Yes |

Discipline for reviewers: you may only write `blocking:` if you can name what
breaks. "I'd have done it differently" is `suggestion:`. If your blocking rate
exceeds roughly one in five comments, you are inflating severity and the labels
stop carrying information.

### Rewriting Real Comments

Most bad review comments share one flaw: they describe the reviewer's reaction
rather than the change required.

```
❌ "This is hard to follow."
✅ "suggestion: `process()` on 40-95 does parse, validate, and persist.
    Splitting out `_parse_payload` would let the validation tests drop the
    DB fixture. Not blocking — fine as a follow-up."

❌ "Why did you do it this way?"
✅ "question: Curious why polling here rather than the existing webhook
    on `OrderUpdated`. If it's because the webhook is unordered, worth a
    comment in the code — the next person will ask the same thing."

❌ "Bug."
✅ "blocking: If `items` is empty, line 63 divides by `len(items)` and
    raises ZeroDivisionError. Empty carts reach this path from the
    abandoned-cart job."

❌ "We don't do it that way here."
✅ "suggestion: The other three handlers use the `@retryable` decorator
    (see `payments/handlers.py:22`) rather than a manual loop. Matching
    that gets you the metrics wiring for free."
```

Note what the good versions share: a line number, a concrete failure or concrete
alternative, and an explicit stance on whether it blocks.

### Size Drives Everything

Review effectiveness is a function of diff size, and the falloff is steep:

| PR size (changed lines) | Typical outcome |
|---|---|
| < 100 | Careful line-by-line reading; highest defect yield |
| 100-400 | Still effective; the practical target band |
| 400-800 | Reviewer skims; structural feedback only |
| > 800 | Approval rate goes up, comment density goes down |

The counterintuitive part: large PRs receive *fewer* comments per line, not
more. A reviewer's attention budget in one sitting is roughly 200-400 lines and
about 60 minutes; past that, defect detection falls off sharply. Treat these as
norms to calibrate against rather than hard thresholds — the shape of the curve
matters more than the exact number. So "LGTM" on a 1,200-line PR is not a signal
of quality, it is a signal of exhaustion.

Splitting is a design activity, not a formatting one. Cut along seams that each
leave the system working:

```
❌ One PR: "Add team billing"  (1,400 lines)

✅ 1. Migration: add `billing_accounts` table, no readers yet    (~90)
   2. Repository + unit tests, unreferenced by any endpoint      (~180)
   3. Service layer wiring behind a disabled feature flag        (~250)
   4. Endpoint + flag enable                                     (~200)
```

Each lands independently, each is reviewable in a sitting, and a rollback of
step 4 does not strand the schema.

### Latency Dominates Cycle Time

Measure the wall-clock life of a PR and the review *waiting* time usually
dwarfs both authoring and reviewing. A change that takes 3 hours to write and 25
minutes to review can easily take 3 days to merge. Every day it waits, the
branch drifts, the author context-switches, and the eventual re-read costs more.

Practical norms that move the number:

- First response within 4 business hours. "Looking this afternoon" counts.
- Review incoming PRs before starting new work of your own.
- Approve-with-comments for anything that is only `nit:` and `suggestion:`.
  Trust the author to apply them; do not require another round.
- Escalate to a synchronous 10-minute call after the second round trip on the
  same disagreement. Text is a bad medium for design arguments that have already
  failed once.

### What Humans Should Review

Anything a machine can check should already be checked before a human looks.
Formatting, import ordering, lint rules, type errors, and test failures belong
in CI. Human attention is the scarce resource; spend it on judgment:

- **Problem fit** — is this solving the right problem, at the right layer?
- **Failure paths** — timeouts, retries, partial writes, concurrent callers.
  What is the state of the world if this process dies at line 40?
- **Data lifecycle** — is the migration reversible? Is there a backfill? What
  reads the old column?
- **Future cost** — will this make the next change harder? Review for the change
  you would have to make later, not for the change you would have written.
- **Test meaning** — do the tests fail if the behavior regresses, or do they
  merely execute the code? (See `test-coverage-categories`.)

Security-sensitive diffs get their own dedicated pass; see `secure-code-review`.

### Author-Side Practice

Reviews are largely won before anyone else reads the code.

Write the description for a reader who lacks your context:

```
❌ "Fixes the checkout bug."

✅ Why: Checkout 500s when a promo expires between cart load and submit.
       ~40/day, PRO-412.
   What: Re-validate the promo at submit time rather than trusting the
       cart snapshot.
   Alternative rejected: locking the promo at cart creation — would hold
       inventory for abandoned carts.
   Risk: adds one read to the submit path (~3ms, measured).
   Testing: new test for the expiry race; verified manually against staging.
```

Then read your own diff on the PR page and annotate it. Flag the file that is a
pure mechanical rename so the reviewer skips it. Explain the odd-looking early
return. Every self-comment you leave is a round trip you did not spend.

## Common Anti-Patterns

❌ **Unlabeled comments** — the author cannot tell a nit from a defect and
treats all of them as gates.
✅ Prefix every comment: `blocking:`, `question:`, `suggestion:`, `nit:`.

❌ **The rewrite review** — reviewer reconstructs the change as they would have
written it, and the author complies to get unblocked.
✅ Accept any design that is correct and maintainable. Reserve objections for
things that are wrong or that make future work harder.

❌ **Reviewing formatting by hand** — comments about spacing and naming style
that CI could enforce, crowding out substantive feedback.
✅ Move it into the linter. If the team argues about it twice, automate it.

❌ **The batched mega-review** — a week of work lands as one 1,500-line PR.
✅ Stack it. Four sequential PRs of 200-400 lines each, merged as they pass.

❌ **Silent approval on a big diff** — LGTM in 90 seconds on 900 lines.
✅ Say what you actually reviewed: "Read the service layer and migration
closely; skimmed the generated client. Someone should check the retry logic."

❌ **Resolving disagreements in DMs** — the decision exists only in two people's
memory, and a third engineer relitigates it next quarter.
✅ Have the conversation wherever it happens, then post the conclusion and its
reasoning back on the PR.

❌ **The drive-by blocker** — a reviewer with no context blocks on an
architectural objection to a design already agreed in review.
✅ Raise architecture at design time. If it genuinely must be reopened, say so
explicitly and take it off the PR thread.

❌ **Nitpicking a hotfix during an incident.**
✅ Review incident fixes for correctness and blast radius only; file the cleanup
as a follow-up ticket.

## Code Review Checklist

**As reviewer**
- [ ] Responded within 4 business hours of the request
- [ ] Every comment prefixed with a severity label
- [ ] Each `blocking:` names a concrete failure, not a preference
- [ ] Checked failure paths: timeout, retry, partial write, concurrency
- [ ] Checked the migration is reversible and the backfill is bounded
- [ ] Verified tests would actually fail on regression
- [ ] Left no comment a linter could have made
- [ ] Stated what you did and did not review if the diff is large
- [ ] Approved with comments when nothing is blocking

**As author**
- [ ] Diff under ~400 changed lines, or split with the stack explained
- [ ] Description covers why, what, alternatives rejected, risk, testing
- [ ] Self-reviewed the diff and annotated the non-obvious parts
- [ ] Mechanical changes (renames, generated files) separated or flagged
- [ ] Responded to every comment, including "won't fix, because…"
- [ ] Off-thread decisions written back onto the PR before merge
