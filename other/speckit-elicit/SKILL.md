---
name: "speckit-elicit"
description: "Re-examine an artifact — a spec, a plan, a decision — through named reasoning methods, one at a time, to surface what a single reading missed. Use when a spec reads fine but feels thin, before committing to a plan, or when a decision was made quickly and nobody has argued the other side."
argument-hint: "The artifact to examine (a path), and optionally a method name."
compatibility: "Read-only. Proposes changes; never edits."
metadata:
  author: "speckit-demo"
  source: "adapted from BMAD's bmad-advanced-elicitation"
user-invocable: true
disable-model-invocation: false
model: opus
---

## User Input

```text
$ARGUMENTS
```

## Why this exists

`spec-challenger` reads a spec cold and returns ambiguities. That is one lens,
applied once. BMAD's elicitation is a different move: take an artifact you have
*already* accepted and re-run it through a **named** method, because the value
is in the constraint — "what would break this" produces different output from
"read it again carefully", and naming the method is what stops the second
reading from being the first reading with more words.

## How to run it

Read the artifact in full. Then pick **two or three** methods — not all of them;
a sweep produces volume, not insight — and apply each one separately, saying
which method produced which finding.

| Method | The question it forces |
| --- | --- |
| **Inversion** | What would have to be true for this to be the wrong thing to build? |
| **Failure premortem** | It is six months later and this failed. Write the one-sentence cause. |
| **Edge enumeration** | Empty, one, many, huge, malformed, concurrent, interrupted. Which does the artifact not say anything about? |
| **Reader substitution** | Read it as someone who has never seen this codebase. Where do they guess? |
| **Constraint removal** | Drop the tightest constraint. Does a simpler design appear? If so, is the constraint real? |
| **Cost of being right** | Assume every requirement is correct. What does the full implementation cost, and is any of it disproportionate? |
| **Second-order** | The change ships and is used. What does it make easy that nobody asked for? |
| **Silence audit** | What does the artifact not mention that a reader would expect it to? Absence is the hardest thing to notice. |

## Output

For each method: the method name, then at most three findings, each one
actionable. A finding says what to change, not that something is "worth
considering."

Close with one line: which finding you would act on first, and which you would
drop. Then stop — this proposes; `/speckit-clarify` encodes answers into a spec,
`/speckit-correct-course` handles a changed intent, and neither is this command's
job to do unasked.

## When not to use it

- The artifact does not exist yet — write it first; there is nothing to
  re-examine.
- Nobody has read it once. This is a second pass, not a substitute for a first.
- The decision is already made and is not being reopened. Elicitation that
  cannot change anything is theatre.
