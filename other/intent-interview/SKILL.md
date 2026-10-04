---
name: intent-interview
description: Extract the real outcome from a vague ask before any work. Use when a request is broad, multi-step, has unstated decisions, or the user says "let's go deep", "get your context ready", "which skills", "how should I prompt", or names a goal without a shape. Pairs with a decision ledger.
---

# Intent interview

Turn a vague ask into a written contract, then work the contract. The contract is the
artifact; the interview is how it gets written.

**Outcome first.** The interview exists to make one sentence true: *I know what
"done" looks like and what I am allowed to assume.* Everything below serves that
sentence.

## The ladder

Run these in order. Stop as soon as the contract is writeable — depth is not the goal.

1. **Read the ground.** Inspect the real thing before asking about it. Files, config,
   docs, installed skills, command output. A question the filesystem answers is a
   wasted question, and a wasted question is what makes interviews feel like tax.
2. **Name the outcome.** One sentence: the artifact or the changed behaviour, and who
   sees it. Draft it from what you read and put it in front of the user. Vague in,
   vague out; a wrong guess corrected in one line is the cheapest possible repair.
3. **Find the forks.** The open decisions, ranked by how much the finished thing
   changes if the answers differ. Impact = architecture, file layout, user-visible
   behaviour, or hard to reverse. Two forks deserve a question. Six deserve a ranked
   list with recommendations.
4. **Ask the fork that unblocks the most work.** One question, in the user's terms,
   with a recommended pick and its trade-off. Batch only the forks that share an
   answer.
5. **Log the rest.** Every fork the user did not answer becomes an assumed decision
   in the ledger, marked as assumed and reversible. The interview ends; it does not
   become a questionnaire.
6. **Write the contract.** `OUTCOME / DONE WHEN / ASSUMED / OUT OF SCOPE`. Keep it
   where the work will find it. Then execute.

## Question craft

- **Ask about the decision, not the topic.** "Where does the code live" is a fork.
  "Tell me about the architecture" is a lecture request.
- **Carry a recommendation.** Every question ships with a pick. A user who answers
  "yes" to your proposal is faster than one who authors a proposal.
- **Prefer the concrete artifact.** Show a shape, a path, a command. "Option A: driver
  in-tree, one file" beats "Option A: simpler".
- **One question per turn** for high-impact forks. They earn thinking time.
- **Answerable in a sentence** beats answerable in an essay. If the answer needs five
  sentences, the fork was not a fork.
- **Absence is data.** Silence on a high-impact fork means either it did not matter or
  the user is tired. Log it, pick, continue. Do not re-ask.

## Ask-first, grilled

`ask-first` lists the forks. This skill does more: it reads the ground first, names
the outcome, asks only the unblocking ones, and writes the contract. When the ask is
already sharp, the ladder collapses to step 6 and the contract is one line.

## Output discipline

The contract is short because the interview paid for it. In chat:

- Lead with the answer or the decision, not the reasoning that produced it.
- One table per reply, and only when rows genuinely differ.
- Cap a chat reply at roughly fifteen lines. Deeper material goes behind a pointer,
  not into the message.
- Reference and prose are written in normal English. Compression registers apply to
  chat and status lines, where the reader is present to be terse with.

See [`REFERENCE.md`](REFERENCE.md) for the question bank, the failure modes, and how
this composes with the decision ledger.
