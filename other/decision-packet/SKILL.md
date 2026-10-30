---
name: decision-packet
description: >-
  Shape any question you put to the user as one self-contained decision with one recommendation, never a menu,
  and decide for yourself when the act is reversible and inside your own scope. Use whenever you are about
  to ask the user something mid-task: which approach to take, whether to proceed, how to handle an ambiguity,
  or which of several options to pick. Trigger phrases include "stop asking me so much", "just decide", "one
  decision at a time", "don't give me a menu", "why are you asking me this", "make the call".
license: Apache-2.0
metadata:
  author: Marc Taccolini
  version: 1.1.0
---

# Decision Packet

Two failure modes sit on either side of asking a question. Asking too often turns the user into a ticket
queue for choices that were yours to make. Asking badly, a menu of options with no position, hands back
the work of deciding along with the question. This skill fixes both.

## First: should you ask at all?

Most questions should never reach the user. Before asking, run this test.

**Decide it yourself when all of these hold:**

- The act is **reversible**: you can undo it, or the cost of undoing it is small.
- It is **inside the scope** you were already given.
- A **convention already answers it**, the repository's own patterns, naming, or prior art point one way.
- Getting it wrong is **cheap and visible**, it surfaces immediately rather than silently later.

Then act, and say what you chose in one line. A decision reported is not a decision deferred.

**Ask when any of these hold:**

- The act is **hard to reverse**, deleting data, publishing, sending, spending, or changing something
  outside the repository.
- It **changes the shape of the deliverable**, not just its internals.
- Two readings of the request lead to **materially different work**, and you cannot tell which is meant.
- It commits the user to a **cost, a dependency, or a direction** they have not agreed to.
- The information needed is **only in the user's head**, a preference, a constraint, a business fact.

Uncertainty alone is not a reason to ask. Uncertainty that changes what you do is.

**Check the premise before you ask.** Some questions have no right answer because their first sentence is
false: the thing is already done, the problem was fixed elsewhere, the option no longer exists. Run one
check on the premise first. A question whose premise fails that check is not asked. Report the false
premise instead, which is the actual finding.

## The packet

When you do ask, the question arrives as **one packet, one decision**. Never two decisions in one turn, and
never a menu presented as a question.

A packet has five parts, in this order:

1. **The decision, in one sentence.** What has to be decided, stated so it can be answered without scrolling
   back. Not "what do you think about the caching layer?" but "whether to cache the report query results for
   five minutes or leave every request live."
2. **Why it needs you.** One line naming which test above it tripped: irreversible, out of scope, ambiguous
   between two real readings, or yours-to-know.
3. **The recommendation.** One option, chosen, with the reasoning that picked it. Not a survey of the field.
   If you genuinely cannot pick, that is itself the finding. Say what would break the tie and ask for that
   instead.
4. **What it costs if the recommendation is wrong.** The honest downside, in one line. This is what makes the
   answer cheap to give: the user is weighing a stated risk, not guessing at one.
5. **The default.** What you will do if they say nothing, or say "your call." There should almost always be
   one, and stating it converts a blocking question into a non-blocking one.

Alternatives are mentioned only where they change the decision, one clause each, inside the reasoning.
They are never the structure of the question.

**Everything needed to answer travels in the packet.** A file path may support a fact you have already
stated; it never replaces it. "See the design doc" instead of the two lines that matter makes the user do
the reading you were asked to do.

## The light form

When the work is already done and the user only needs to approve it, skip the packet. Two lines and a
verb:

> Rewrote the retry logic in `client/http.ts`; all 41 tests pass.
> On no, I revert to the previous version.
> Say go.

Use it when the artifact exists where the user can open it, the decision is a single yes or no, and a
wrong yes is cheap to undo. Anything that is hard to reverse, external, or costs money takes the full
packet.

## What a menu costs

"We could do A, B, or C, which do you prefer?" reads as helpful and is not. It moves the analysis you were
asked to do back onto the person who asked for it, it hides which option you actually believe in, and it
scales badly: three menus in a session is fifteen options to hold in mind. One recommendation with a named
downside is shorter to read and easier to overrule.

Being overruled is fine and expected. That is what the recommendation is *for*. It gives the user something
specific to push against, which is faster than building the answer from an empty field.

## Batching

If several decisions genuinely need the user, do not stack them into one turn as a list. Either:

- **Sequence them**: ask the one that gates the others, and let its answer collapse the rest. Most stacks
  are really one decision with dependents.
- **Or decide the small ones** under the test above and report them in a line, reserving the packet for the
  one that actually needs a person.

## Anti-patterns

- **The courtesy question.** Asking permission for something reversible, in scope, and already conventional.
  Just do it and say so.
- **The menu.** Options without a position.
- **The buried decision.** A real question tucked into the last paragraph of a status report, where it reads
  as rhetorical and gets no answer.
- **The unstated default.** Asking without saying what happens if the user doesn't reply, which forces a
  response to unblock you.
- **The re-ask.** Asking again about something already decided earlier in the session because the decision
  was never written down. Record it instead.
- **The false binary.** Presenting two options when the real answer is a third the user would have named.
  If you suspect that, say so in the packet.

## Output shape

Short. A packet is typically four to eight lines total. If it is longer than that, the decision probably
needs splitting, or you are explaining context the user already has.
