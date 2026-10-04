---
name: prototype
description: Build a throwaway prototype to flush out a question before committing to it. Routes between three branches — a runnable terminal app for state/business-logic questions (LOGIC), several radically different UI variations toggleable from one route (UI), or a focused spike that gives a binary verdict on whether a technical assumption holds (FEASIBILITY). Use when the user wants to prototype, sanity-check a data model or state machine, mock up a UI, explore design options, verify an `Uncertain` assumption from `/research` before `/write-a-prd`, or says "prototype this", "let me play with it", "try a few designs", "spike this", "can the library actually do X", or "is this feasible".
sources:
  primary:
    - "Extreme Programming Explained — Kent Beck"
  secondary:
    - "The Pragmatic Programmer — Andrew Hunt & David Thomas"
    - "The Design of Everyday Things — Don Norman"
---

# Prototype

A prototype is **throwaway code that answers a question**. The question decides the shape.

> **Forked from Matt Pocock's `/prototype` on 2026-05-11; kit-owned for iteration.** The LOGIC and UI branches are unchanged from upstream. The FEASIBILITY branch is a kit addition so `/research` and `/execute` can name a discharge route for `Uncertain` assumptions that are cheaply verifiable by code.

## Pick a branch

Identify which question is being answered — from the user's prompt, the surrounding code, or by asking if the user is around:

- **"Does this logic / state model feel right?"** → [LOGIC.md](LOGIC.md). Build a tiny interactive terminal app that pushes the state machine through cases that are hard to reason about on paper.
- **"What should this look like?"** → [UI.md](UI.md). Generate several radically different UI variations on a single route, switchable via a URL search param and a floating bottom bar.
- **"Does this approach actually work?"** → [FEASIBILITY.md](FEASIBILITY.md). Write a focused spike — one automated test or a temporary scratch route — that gives a binary verdict on whether a single technical assumption holds. Then delete the spike and fold the verdict into the calling skill's artifact.

The three branches produce very different artifacts — getting this wrong wastes the whole prototype. The clearest signal:

- If the question is about *which shape feels right* (state model, layout, API ergonomics), pick LOGIC or UI.
- If the question is *yes-or-no on a technical assumption* (does the library expose this, does this configuration survive the streaming path, does this format render where we need it), pick FEASIBILITY.

If the question is genuinely ambiguous and the user isn't reachable, default to whichever branch better matches the surrounding code (a backend module → LOGIC; a page or component → UI; an `Uncertain` assumption in a research artifact → FEASIBILITY) and state the assumption at the top of the prototype.

## Rules that apply to all branches

1. **Throwaway from day one, and clearly marked as such.** Locate the prototype code close to where it will actually be used (next to the module or page it's prototyping for) so context is obvious — but name it so a casual reader can see it's a prototype, not production. For throwaway UI routes, obey whatever routing convention the project already uses; don't invent a new top-level structure.
2. **One command to run.** Whatever the project's existing task runner supports — `pnpm <name>`, `python <path>`, `bun <path>`, `pnpm run test <file>`, etc. The user must be able to start it without thinking.
3. **No persistence by default.** State lives in memory. Persistence is the thing the prototype is *checking*, not something it should depend on. If the question explicitly involves a database, hit a scratch DB or a local file with a clear "PROTOTYPE — wipe me" name.
4. **Skip the polish.** No tests beyond the spike's own assertion (FEASIBILITY only), no error handling beyond what makes the prototype *runnable*, no abstractions. The point is to learn something fast and then delete it.
5. **Surface the state or the verdict.** LOGIC re-renders state after every action; UI shows the variant on every switch; FEASIBILITY emits a pass/fail verdict from the test runner or a single observable outcome from the scratch route.
6. **Delete or absorb when done.** When the prototype has answered its question, either delete it or fold the validated decision into the real code — don't leave it rotting in the repo. For FEASIBILITY specifically, the spike is deleted in the same change that captures the verdict; the verdict is what persists, not the spike. *Carve-out:* when the spike's captured **output** (not its verdict) is a foreseeable downstream asset — a later slice will consume it as a test fixture — preserve that artifact deliberately; see "Preserve reusable captured output" under **When done**.

## When done

The *answer* is the only thing worth keeping from a prototype. Capture it somewhere durable (commit message, ADR, issue, the research artifact's assumption tag, or a `NOTES.md` next to the prototype) along with the question it was answering. If the user is around, that capture is a quick conversation; if not, leave the placeholder so they (or you, on the next pass) can fill in the verdict before deleting the prototype.

For FEASIBILITY spikes specifically, the verdict folds back into the calling skill's artifact: `/research` downgrades the assumption tag (e.g. `Uncertain` → `Verified` or `Refuted`), and `/execute` proceeds, pivots, or files a `/correct-course` depending on the answer.

### Preserve reusable captured output

The verdict is always what persists; the spike itself is disposable scaffolding by default, and most spike output genuinely is — delete it. But a FEASIBILITY spike sometimes captures **output** that is itself the cheapest source of a downstream asset: recorded HTTP responses, sample payloads, challenge-page HTML, golden files. When such output is a *foreseeable* downstream consumer's input — a later slice will commit it as a test fixture — preserve that artifact deliberately, distinct from and in addition to the verdict. Either:

- **Commit it as a fixture now** in its real home (e.g. `fixtures/`), with a one-line note on where it came from and when, so the consuming slice's "captures available" assumption is *true* rather than caught-false at execution time; or
- **Record the exact re-capture recipe** alongside the verdict (the command, the source, any auth/IP conditions) when the artifact can't or shouldn't be committed, so the slice can regenerate it deterministically instead of re-deriving how.

This is a narrow exception, not a license to hoard. Preserve only when a *named* downstream consumer makes the output an asset; verdict-only discipline stays the default for ordinary spikes (Rule 6), where preserving output speculatively just bloats the repo with stale captures. The signal you preserve here is what `/prd-to-issues` and `/execute` rely on when a slice's assumption depends on a spike artifact rather than its verdict.
