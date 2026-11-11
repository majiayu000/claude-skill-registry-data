---
name: pair-code
description: Pair-program through a plan or design. Research first, give a short plan, ask only the critical questions one at a time, then batch the minor ones with recommended defaults. Use when the user wants a pairing partner, mentions "pair code", or wants a faster, lighter-touch version of grill-me.
---

Act as a pair-programming partner. Find the balance between a wall of text and a long chain of tiny questions.

## Flow

1. **Listen.** Restate the task in one sentence so the user can correct any misread.

2. **Research.** Explore the codebase and read the relevant files. Resolve anything you can answer yourself — do not ask the user a question the code already answers.

3. **Sort the open questions.**
   - **Critical** — load-bearing choices where the wrong call changes design, scope, or correctness.
   - **Minor** — judgment calls with a sensible default where reversing later is cheap.

4. **Short plan.** Send a brief summary of the plan — a few bullets, not paragraphs. Just enough to anchor the conversation.

5. **Critical questions, one at a time.** Ask each critical question on its own, with your recommended answer and the tradeoff. Wait for the user's response before moving to the next. Use AskUserQuestion when it fits.

6. **Minor questions in a batch.** After the criticals are settled, present the minor questions as a single list, each with your recommended default. The user either accepts the batch, or points at one to drill into. Do not ask them one by one.

7. **Proceed.** Move forward using the agreed answers and the accepted defaults. Don't re-confirm.

## Rules

- **Short plan, never a wall of text.** If the plan can't fit in a few bullets, the user can ask for more.
- **One critical at a time.** Each carries your recommendation — the user is approving or redirecting, not picking from blank.
- **Batch the minors.** One message with all of them, each with a recommended default.
- **Stay proportional.** A small change may have zero critical questions and a two-line minor batch. Don't manufacture questions.
- **Codebase first.** If a question can be answered by reading code, read the code.
