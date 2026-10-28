---
name: decision-rules
description: Run FrontierJS doctrine against a design choice. Use when adding an option, flag or config key; coining a noun or concept; choosing between two designs; when the code and a document disagree; or before writing a ruling into `DECISIONS.md` or a proposal into `IDEAS/`. Pass the choice, its options and the files it touches as the argument.
context: fork
---

# Decision rules

The choice to grade: $ARGUMENTS

**The doctrine is `PHILOSOPHY.md` and it is not repeated here.** Read § V (the nine questions) every time. Read § IV (the standing adjudications) only when two goods are in tension, and § VII (the four tiers) only when the answer is going into a document.

Stop within 15 tool calls and return what you have.

## Run it

**Short run** — adding an option, coining a noun, the code and a document disagreeing. Answer four of § V's questions, one line each: **1 origin**, **5 derived**, **6 owner**, **9 silence**. Those are the ones nobody reaches for on their own. Add any other question the choice plainly fails.

**Full run** — choosing between two designs, or writing a ruling or an `IDEAS/` proposal. Answer all nine, one line each, then name the § IV adjudication (or write that none is in tension) and the § VII tier.

**The ninth is TWO answers.** What must stay true, then what fails when it stops — a test, a snapshot, a CI phase, a refusal at the boundary. **`none` is a permitted answer** and records the invariant as unenforced; an artefact left implied is not.

**The owner question asks where the owner IS before how many there are.** A second implementation beside an existing owner breaks Invariants 4 and 5 while answering *exactly one owner* truthfully about itself. `bridge-index` lists the owners that exist.

**Read the § IV row you name before leaning on it.** Reaching for a neighboring row is the failure mode: *familiarity vs. precision* is about the ecosystem's habits and was cited to keep an existing command name, which is *preservation vs. evolution*, the row with the opposite answer.

## Return

At most 25 lines:

- **Verdict** — passes, fails a question (change the proposal, not the answer), or should land anyway (a ruling: the `FJS-D##` names the question it overrides).
- **The answers**, one line each, and the adjudication and tier on a full run.
- **Late** — say so when the code was built before this ran; answers written after the code is green are a defense, not a decision.

Where two proposals both pass, the tiebreak is six months out: the one that lets a developer predict more from less knowledge.

## Recommending

Only when the output is a recommendation on a question for the owner.

- **Match a sibling that already decided the same shape, from the question's own domain.** Precedent outranks both the stricter design and the simpler one. `FJS-D1196` lost on an infra precedent where the app's own domain decided it.
- **With no precedent, recommend what moves fewer callers and adds no convention**, and name the stricter option as the reopen path.
- **For a third party or a product, cite how two or three real products answer it**, with sources. Naming, Dependencies, Mesa and product papers miss most.
- **State a confidence (1–3).**

## When the code disagrees

Hold a hearing, then either fix the code or amend the doctrine, in writing. An undocumented divergence is the failure both directions share.
