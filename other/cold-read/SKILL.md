---
name: cold-read
description: Use when dispatched to cold-read a plan, as an agent that was not in the conversation that wrote it, to say whether it can be carried out from the document alone. Produces what the reader would build, its questions, and a verdict, ready or not ready, repeated as the writer fixes the plan. Not for judging the design (interview, pr-review), not for the mechanical checks (aiview plan check, tracker check), and not for writing the plan (write-plan).
---

# Cold read

**You stand for the agent who will carry this plan out with nothing but the document.** You were
not in the conversation that wrote it, and that is the point: its writer cannot see what is in
their head and not on the page. Your job is to find it. A question you guess past is a task
built on a guess.

## What to do

1. **Read the plan** through the `aiview` skill, every document it links, and the code it names
   where you need it to understand a part. Do not edit anything.
2. **Answer, in this order**:
   1. **What you would build**: the goal, the design and the phases, in your own words, short.
      The writer compares it with what they meant.
   2. **Your questions**: everything you would have to ask, or guess, before writing any
      phase's tasks. Each one says where in the plan it arises.
   3. **Your verdict**: `ready` when no question is left, `not ready` otherwise.
3. **Talk it through with the writer.** Ask back, push on an answer that does not convince you,
   say how you read a passage and let them correct you, propose a wording. The exchange is how
   you both find what the plan leaves unsaid; keep it going until you understand the work as
   they do.
4. **A question closes in the plan, not in the talk.** Once you agree, re-read the changed place:
   what the next agent needs and only the conversation holds is still a question. Give the
   verdict again with what is closed and any new question the change raised.

## What to check

- **Every term** is defined or plainly the codebase's.
- **Every decision has its reason**, so a case it did not foresee can be decided the same way.
- **The plan agrees with itself**: the design, the decisions, the phases and the tracker say
  the same thing.
- **Every done-when is checkable**: a command, an observable result, never a judgement.
- **Every file, module and document named exists**, or the plan says it is created.
- **Each phase's tasks can be written from the plan alone**: what it builds on, what it must not touch.

**You judge clarity, not the design.** A design you would have done otherwise is not a question;
a design you cannot understand is. A flaw you cannot leave unsaid is named once, as a flaw, apart
from the questions.
