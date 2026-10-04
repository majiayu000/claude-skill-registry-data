---
name: walkthrough
description: Explains things and writes reader-facing documents point-first ("explain how this works", "walk me through this", "why did this break", "write up a handoff"), with a lead line that answers, an optional ASCII diagram, a body shaped to the content (steps, prose, or table), and one next action. Use when asked to explain something, walk through it, or say how it works or why it broke, when giving a multi-step plan, or when writing a plan, handoff, spec, or report for someone to read and act on. For one-line answers and status replies, answer directly instead.
---

# Walkthrough

The reader reads this once, acts on it, and comes back later to skim. Everything below serves those three moments.

The shape defined here applies to anything written to be read: chat replies, markdown documents, and PR bodies. For text written *as* the user, a voice skill, if installed, sets the voice and this skill keeps only the shape.

On every invocation, read `.claude/shipyard/walkthrough.md` in the project root if it exists; its settings win over the defaults below. It can set the reader's level, the length ceiling, the heading style, extra phrases to avoid, and which documents get the cold-read check; its shape is in [references/overlay-example.md](references/overlay-example.md). Without it, write for an experienced developer with the defaults as written.

When rules conflict, this order wins:

1. **Reader-first structure.** Answer first, one next action last.
2. **Exactness.** Identifiers, paths, commands, ports, and IDs match the source character for character, and the prose is spell-checked.
3. **Brevity.** Every line carries information the reader doesn't have yet.

## Shape

1. **Lead line.** One sentence with the conclusion, the answer, or what the piece covers. The reader should be able to stop here and know the outcome.
2. **Diagram**, only when the subject has branches, gates, or more than three moving parts. At most two, and two only when the topic splits (a client flow and a server check). Draw it with the flow-diagram skill when it's available, since it owns the diagram rules. Otherwise: plain ASCII, at most 72 columns (wider rows wrap in terminals and indented chat panes, and one wrapped row breaks the figure), box borders counted to match their labels, and node labels that are the same names the body uses, so the reader can move between them.
3. **Body, shaped by what the content is.** One shape per section:
   - *Something to do* (a plan, a fix, a procedure): numbered steps, one action each. Put the condition before the action ("If the migration fails, roll back with …"). In plans, each step that changes code or config names how to verify it, and each lookup or decision step names what it produces (`write down the interface's methods`).
   - *How or why something works or broke*: short prose paragraphs, one idea each, using the diagram's labels. Steps would chop the reasoning apart.
   - *Things to look up* (files changed, flags, options): a table or grouped list.
4. **Close.** Exactly one concrete next action the reader can start in under two minutes, small enough to begin without planning, such as `next: run pnpm test -- auth.test.ts and paste the first failure`. Offer two options only when the right next step depends on a decision the reader has to make. A pure reference piece has no close.

Headings are short lowercase fragments that say what the section tells, such as `## why the retry fails`, so a skimming reader can find their place. On later turns of multi-step work, open with a one-line position marker, such as `step 3/5 done: schema migrated. on step 4: backfill.`, stating only where the work stands.

## Length

- About 40 lines per reply, roughly one screen. Past that, give the part the reader needs now and offer the rest in one line: `that's phase 1. want phase 2 (deploy) now or after you run it?`
- Group lists into five or fewer chunks. A reference list such as changed files can run longer if it's grouped.
- Split a walkthrough of more than seven steps into named phases of at most five steps.
- Full length, always, for error text, failing test output, security warnings, and confirmations before destructive actions. The reader needs them complete to act safely; they don't count toward the ceiling.

## Evidence and certainty

- **Point to evidence instead of explaining more:** `file:line`, the command and its output, the test result. Longer explanations raise a reader's confidence whether or not they're right; evidence lets the reader check.
- **State what you know plainly, and mark what you don't, once, in first person:** `unverified: I didn't run the migration against real data.` A marked uncertainty helps the reader decide what to check; a scatter of "might" and "possibly" hides which claims are actually shaky.
- **Estimate time only from a basis**, such as a measured runtime or a known command: `~40 s, measured`. Without one, give a size (`small`, `half a day`) and label it a guess. Made-up precise numbers anchor the reader's own planning.
- **Report errors as symptom, cause, and fix**, one line each: `auth.test.ts fails: expected 200, got 401. cause: token expires before the retry. fix: step 2.`
- **Correct an earlier statement only when it changes what the reader will do**, in one line.
- **Finish the walkthrough before raising a side issue**, then give it one line: `separately: the retry config is also stale. handle after?`

## Wording

Write the way this file is written: plain words, sentence case, imperative steps. Connect ideas with `also`, `then`, and `ie`. Put anything the reader must remember into the step where it matters, so nothing depends on memory. For the specific phrases and formatting habits that make text read as filler or machine-written, and what to write instead, read [references/writing-tells.md](references/writing-tells.md) before writing anything longer than a few lines.

## Documents

A plan, handoff, spec, report, or analysis written to a file follows everything above, with these differences, because a file is read out of order and has no turns:

- The 40-line ceiling applies per `##` section.
- Instead of position markers, give each tracked item its own status line.
- Diagrams stay ASCII, since the file is read in an editor or terminal. Where the page renders diagram code (a wiki page, a PR body), use it, drawn per the diagram step in Shape.
- Headings name content (`## auth fails on token refresh`). Generic headings (`Overview`, `Summary`, `Background`, `Conclusion`) and recap sections add nothing the lead line and headings don't already give.
- Where a section argues for a decision, write it as prose paragraphs; bullets hide the reasoning between points.

**Cold-read check.** Run it for a plan, handoff, or spec that someone else, or a later session, will act on. Skip it for scratch notes.

1. Give a fresh subagent only the document, with no conversation context.
2. Ask it for the first five actions it would take, and for anything ambiguous, assumed, or contradictory.
3. Fix each gap it hits in the document, not in chat.
4. Repeat until its first actions match what you intended, at most twice. If it still diverges after that, tell the reader which part is unclear.

## Worked example

Illustrative, not a real bug. A "why is this failing" question mixes explanation and a fix, so it gets prose for the why and steps for the fix:

```
The login test fails because the retry reuses an expired token.

+------------+     +-------------+     +---------------+
| login test | --> | first call  | --> | token valid?  |
+------------+     +-------------+     +---------------+
                                          |         |
                                         yes        no
                                          |         |
                                          v         v
                                     +--------+   X 401, test fails
                                     | 200 ok |
                                     +--------+

The test config issues tokens that live 1 s (auth.test.ts:12). The
first call is slow, so the retry fires after the 2 s backoff, token
valid? takes the no arm, and the call returns 401.

1. Set the test token lifetime to 30 s in auth.test.ts:12
2. Re-run npm test -- auth.test.ts (~40 s, measured)

next: change line 12 and re-run that one test.
```

## Before sending

1. The first line is the answer, not an announcement of one.
2. The last line is one concrete action under two minutes, or there is none because this is reference.
3. Each section has one shape: steps for doing, prose for why, a table for lookup.
4. The reply is about 40 lines or fewer (per section in a document); if longer, it gives the part needed now and offers the rest.
5. Error text, test output, and warnings are complete.
6. Nothing from `references/writing-tells.md` slipped in.
7. Reading only the first and last lines tells the reader what this is and what to do next.
