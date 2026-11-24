---
name: throwaway-spike
description: "Use when a look or state model is unclear and throwaway code settles it faster than talk, and for the Look bar on any user-facing visual. Side-branch commit needs OK."
user-invocable: false
---
# Throwaway spike
Gate: get the user's OK before committing the spike to its side branch (G2). See gates.md in the skill house-rules.
Job: Answer one design question with cheap running code.
Takes: a question.   Gives: a runnable demo, a verdict, a side branch reference.
Team moves: race (for look questions, when the user wants variants from different kinds)

## Steps

1. **Name the one question and its kind.** The results differ a lot, so decide which it is.

   | Kind | The question | Follow |
   |---|---|---|
   | Logic | Is this state model sound? | `logic-spike.md` |
   | Look | How should this screen work? | `look-spike.md` |

   Any user-facing visual deliverable, even a settled design, also meets the Look bar in `look-spike.md` before it is reported done. For a settled design the Look bar is the whole job: skip the other steps.

   If it could be either and the user is away, infer the kind from nearby code and state your assumption. If the experiment doesn't belong in this session, use the skill `baton-pass` to move it to a side session, and take the verdict back as a note.

2. **Hold these for either kind:**
   - It sits beside the code it informs and follows the existing routing conventions.
   - It is plainly temporary, by name and on screen.
   - One command or a double-click starts it.
   - State lives in memory, unless persistence is the question. Then use a clearly disposable store.
   - It has no tests, no abstractions and no extra error handling.
   - Full state is visible after every action.

3. **Build it** by the kind's file, and get it running.

4. **Put it in front of someone and watch.** The best signs: someone spots a move the model should refuse, or wants a mix of two variants. Write down the verdict. A spike is a stand-in, so its verdict about the real system is `[simulated]` until real code proves it.

5. **Keep the code.** With OK, commit it to an unmerged side branch. A worker reports this under `Needs OK` and leaves it for the lead.

6. **Move only the decision.** Fold the decision into real code or into the chart, then record the question and the verdict in a note artifact in the bench's `notes/` folder. Reference the side branch from any card that implements the decision. A trimmed snippet may go into a chart when it pins a decision better than prose. If this resolves a `try` card, give the verdict to the skill `work-chart` to post.

## Done when

A settled visual needs only the Look bar line.

- One question was stated, with its kind, and any inferred kind was said out loud.
- The spike started from one command or double-click, and showed full state after each action.
- The kind's own Done when is met, and any user-facing visual met the Look bar.
- A verdict answers the question and is recorded with it.
- The code sits on an unmerged side branch committed with OK, or the user declined and that is stated.
- Nothing from the spike reached the main line except the decision, and implementing cards reference the branch.
