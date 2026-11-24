---
name: question-tree
description: "Use when a choice has no sensible default and is costly to reverse, the user asks to test their thinking, or a decision waits on another person."
user-invocable: false
---
# Question tree
Job: Get decisions out of the head of whoever holds them.
Takes: a plan or decision.   Gives: a decisions artifact, or a questionnaire file for someone else.
Team moves: dispatch (scouts)

Building on a quiet guess is expensive to undo, and one question is cheap. Interrogating someone over trivia is expensive too, so ask only what matters.

## Steps

1. **Read the state** and act on every row that holds.

   | State | Do |
   |---|---|
   | In a repo | Run the skill `shared-words` alongside this, and read the glossary and records first |
   | No repo | Keep nothing. The outcome stays in the conversation |
   | The answer lives with another person | Follow `for-someone-else.md` |
   | You started this unprompted | Ask only about decisions that change what gets built, five questions a round at most. State defaults for the rest. If nothing qualifies, skip the interview |
   | You are a worker or scout | Only the lead interviews. Put the question under `Open` in your report |

2. **Model the subject as a tree** of decisions, noting which ones hang on which.

3. **Sort each unknown.** Facts are yours to find, so dispatch a scout and keep asking whatever doesn't depend on its answer. Decisions belong to the user. Read the file `levels.md` in the skill `house-rules` before the first dispatch.

4. **Ask a round.** Ask everything answerable now and hold back what hangs on another open question. Number the questions, give your recommendation, and phrase each so a bare yes adopts it.

   ```markdown
   1. Bill per seat rather than per active user? I recommend yes: invoices stay predictable and the sales team can quote them.
   2. Keep annual plans at launch? I recommend no: it doubles the proration cases.
   ```

5. **Update the tree.** Each answer closes branches and may open new ones. Repeat from step 3 until no decision is left resting on a silent assumption.

6. **Confirm.** Restate the settled choices and any defaults, and get the user's confirmation. Take no action on the plan before that.

7. **Write the outcome.** In a repo, write a decisions artifact to the bench's `charts/` folder, marking each choice `By: user` or `By: default`. Questions you could not close go under `Open` with what each blocks. Terms from the skill `shared-words` go under `Words`. Say where the file is. With no repo, restate the outcome in the conversation and save nothing.

## Done when

- Every branch of the tree is settled, or listed under `Open` with what it blocks.
- No choice rests on a silent assumption: each is marked user or default.
- Every question asked was numbered, carried a recommendation and could be answered with a bare yes.
- No round went out holding a question that depended on another open one.
- The user confirmed, and nothing was built before that.
- An unprompted run stayed at five questions a round, on decisions that change what gets built.
- The decisions artifact exists in a repo, or nothing was saved outside one, or the questionnaire met the Done when in `for-someone-else.md`.
