---
name: frame-next
description: Take a paper's open questions from `fli decisions` and make each one decidable — lettered options and a recommendation written into its own bullet — without ruling on any. Use when asked to frame the next question or questions.
disable-model-invocation: true
---

# Frame next

The loop from *an open question* to *a question the owner can answer with one letter*. Arguments: a paper id and the question ids to frame in it (`scripts/frame-loop.mjs` passes both, with a `## Pre-brief`), or one question id.

**The session's job ends at the options.** The ruling is the owner's, made with `fli decide`. So the only file written is the paper holding the questions, and only under each question's bullet. `DECISIONS.md` is left as it is, no question is struck, and `fli decide` is not run. A session that rules has failed, however good the ruling.

## 1. Pick

`fli decisions --open` lists what is open, `--json` the same as data. **Say the paper and the question ids before doing anything else**, so a person watching can redirect.

If the paper is dirty in `git status` and the arguments do not say an earlier frame-loop attempt left those edits, another session holds it: end with `busy` for every question. When they do say so, the edits are yours — read `git diff` on the paper and build on them.

## 2. Brief

The pre-brief carries each question verbatim, what it cites, the paper's sections with line ranges, and the rulings that share its terms. Read the paper's sections a question leans on, never the whole paper blind. Ground each option in the tree: `rg` for the code it would change, `fli outline <file>` before reading a big one, and a cited ruling read in full in `DECISIONS.md`. A search across many packages goes to one `Explore` subagent, asked for `file:line` answers only.

## 3. Frame

**Run `decision-rules` on each question before writing its options** — framing is choosing which alternatives are real, and that is a judgment call.

Options are **real alternatives a reasonable owner could pick**, each stated as what the tree would look like after it, and grounded: a `file:line`, a ruling, a measured behavior. Two options is the floor; the one the paper argues against belongs among them when it is a live choice. The recommendation names its letter and says why in one or two sentences with the evidence.

Write them **under the question's bullet, after its existing prose, before the next top-level bullet** — exactly this shape, since `packages/cli/core/decisions.js` parses it:

```
- **The question's bold lead, unchanged?** Its existing prose, unchanged.
  - **A** — what the tree looks like if A, grounded (`path/file.js:120`)
  - **B** — what the tree looks like if B, grounded
  - **Recommend A** — why, citing the evidence
```

A wrapped line is indented four spaces, under the option it continues. **The bold lead line stays byte for byte as it is**: the question's id is a slug of it, and an edited lead is a new question the loop cannot find.

### Settled — an existing ruling already answers it

When a live `FJS-D` ruling (or shipped code a ruling stands behind) answers the question, frame **one** option that states that answer, and a recommendation naming the ruling id:

```
  - **A** — as `FJS-D123` rules: what that means for this question
  - **Recommend A** — `FJS-D123` settles it: the sentence of the ruling that does
```

The owner confirms it with `fli decide <id> --by FJS-D123`, which cites that ruling and issues no new one. A superseded or withdrawn ruling settles nothing — cite what replaced it, or frame the question.

### Unclear — the question cannot be framed as written

Two questions in one bullet, a premise the tree contradicts, or no choice left to make. Write nothing under it, and say which of those it is in the report line.

## 4. Verify

`fli decisions --json` after the edits, and read each id's `state` and `recommend`. A `framed` question is `decidable` with its recommendation read back; a `settled` one is `open` with the recommendation present. An id that is no longer there means its lead line changed — restore it. Then `fli done` and clear what it lists.

## 5. Report

One line per question on what was framed and why the recommendation. **The last lines of the report are exactly `frame-next: <id> <status>`, one per question**, status one of `framed`, `settled`, `unclear` (followed by ` — ` and the reason), `busy` or `failed`. The loop reads the register first and these lines only for what the register cannot show.

Then end the session. **One paper per session**: its questions share an argument and are framed together so their options agree; a second paper would carry every file the first one read. A batch is `bun run frame:loop`.
