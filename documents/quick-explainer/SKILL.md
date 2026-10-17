---
name: quick-explainer
description: >
  Prime the brain for a context switch with one concrete example. Point at a PR,
  a tech design, a plan, a Mikado graph, an issue, a screenshot, or the current
  branch, and get back a sub-terminal-window explainer built entirely out of a
  single worked example: what goes wrong today, and what the same situation looks
  like once the change lands. Use when the user runs /quick-explainer, or asks to
  "catch me up on", "remind me what this is about", "what is this PR actually
  solving", or "explain this without the abstraction". Never a summary, never a
  review -- one example, no theory.
---

# Quick Explainer

Someone is about to context-switch into a thing they haven't touched in a while,
or have never touched at all. The source material is long, abstract, and full of
`Foo.ts:412`, "motivation", and "background". Reading it costs twenty minutes of
sitting down and concentrating, which is exactly the thing they don't have.

Your job is to give them the twenty seconds that make the twenty minutes
unnecessary — or at least easy. Not a summary. **One concrete example.**

## The one hard rule

**Everything in the output is a specific instance. Nothing is a category.**

If a sentence could be true of a hundred different systems, it's wrong. Replace
it with the one thing that actually happens.

| Don't write                                                  | Write                                                                     |
| ------------------------------------------------------------ | ------------------------------------------------------------------------- |
| "Fixes a race condition in presence sync"                     | "Alice sees Bob's cursor freeze at the last spot he stopped moving"        |
| "Introduces idempotency for tool calls"                       | "Bob gets two emails instead of one"                                       |
| "Improves the ergonomics of the storage API"                  | "You currently need 6 lines and a `useCallback` to increment a counter"    |
| "Reduces coupling between `Room` and the transport layer"     | "`new Room()` opens a real socket, so the reconnect test hangs forever"    |
| "Addresses eventual consistency issues in `LiveList`"         | "Alice ends with `[c, a, b]`, Bob ends with `[a, b]`, forever"             |

Concrete means: real names (Alice, Bob), real values (`[a, b, c]`), real
numbers (40s → 3ms), a real sequence of events in order. If you can't picture
it happening on a screen, it isn't concrete yet.

## Output shape

Four parts, in this order. Nothing else — no preamble, no "hope this helps", no
offer to go deeper.

```
**<one line: what this thing is, in the plainest words available>**

### Today

<the smallest scenario where the problem is visible, 3-6 lines, in order>

### After

<the exact same scenario, problem gone, 3-5 lines>

**The trick:** <one line — the single idea that makes the difference>
```

`The trick:` is optional and often the best line in the output. Drop it if the
answer is genuinely just "do the obvious thing that nobody did yet".

The output is rendered as markdown in a terminal, so **the headings carry the
structure, not whitespace.** Leading spaces collapse when rendered, and faking
them with `&nbsp;` prints the entity literally. Write every line flush left, one
beat per line, and let `### Today` / `### After` do the separating. If a beat
genuinely has sub-items, write a real markdown list — those nest and render;
hand-made indentation does not.

**Target: 20 lines.** It should fit on screen without scrolling — that's the
point of the whole thing. When it runs long, shrink the example first: a smaller
scenario is almost always a clearer one, and the cap is there to force that
attempt.

But **clarity outranks the cap.** If the shrunk version has stopped being
obvious, go back and spend the extra lines — a 28-line explainer that lands beats
a 19-line one the reader has to decode. Just don't *start* from the assumption
that you need the room.

## Picking the example

Find the **smallest scenario where the difference is visible.**

- Two actors, not five. One field, not a schema. One request, not a flow.
- Same example in Today and After. Changing the scenario between the two halves
  destroys the comparison, which is the only thing carrying the explanation.
- Show it in the medium the change lives in:
  - UX change → what the person on the screen sees
  - Data/CRDT change → the actual values, before and after
  - Protocol change → the message sequence, in order
  - API change → the code someone writes, both versions
  - Performance → the numbers
  - Build/tooling → the command and its output
- **Repro steps are a first-class example form** — often the best one, because
  the reader can go do it. "Open the doc in two tabs. Type in A. Close B. A's
  cursor list still shows B." is a perfect `### Today` block. If the source has
  steps to reproduce, use them close to verbatim.
- If the source document already has a good motivating example, use it. It's
  grounded, and reusing it means the user recognizes it when they get there.

## When there's no "problem"

Not everything is a bug fix. Keep the same shape, change the labels:

- **New capability** → `### Can't today` / `### Can after`
- **Pure refactor** → the pain *is* the code shape, so show the code shape:
  `### Today you write` / `### After you write`
- **Mikado graph / plan** → `### The blocker right now` / `### After the graph is
  green`, and replace `The trick:` with `**First leaf to do:** <the one node with
  no remaining prerequisites>`. Which node to start on is the most useful thing a
  plan can tell someone re-entering it.
- **A decision doc with alternatives** → `### Today` / `### After` for the
  *chosen* option only. Mentioning the rejected ones is theory, and theory is
  banned.

## Banned

These are the things that force the reader to concentrate, which defeats the
purpose:

- Line numbers, file paths, and function names *as the explanation*. Naming
  `LiveList` because it's the thing being changed is fine. `LiveList.ts:412` is
  not.
- A bullet list of what changed. That's a changelog, not an explainer.
- Restating the doc's own abstract, background, motivation, or goals sections.
- Terms lifted from the source that the example hasn't grounded yet. If your
  example needs the reader to already know what "ack fencing" means, the example
  is wrong — the example is supposed to *be* what "ack fencing" means.
- Hedging that isn't load-bearing. "This appears to potentially address" → "This
  fixes".
- Caveats, edge cases, risks, open questions, testing notes.
- `&nbsp;`, or any other HTML entity, or leading spaces used as indentation.
  Lines are flush left; the headings do the structuring.
- Anything after `The trick:` line.

## Ground it in something real

The example has to be a problem that **actually happens**, not one you
constructed to illustrate the change. Nvie's rule applies with full force here:
**do not guess or hallucinate.** A fabricated scenario that sounds plausible is
worse than no explainer — it's indistinguishable from a real one, and it becomes
the mental model.

In descending order of preference, take the example from:

1. **A real reported failure** — the bug report, the support thread, the Sentry
   error, the incident, the "this bit me on Tuesday" comment on the PR. Real by
   construction.
2. **Repro steps** in the issue, PR, or doc. Use them close to verbatim.
3. **A test that was added or changed.** The test names the scenario the author
   cared about; what it sets up and what it asserts *is* the example.
4. **The diff itself** — but only when you can trace one concrete input through
   the old code and point at the lines that turn it into a concrete wrong output.
   If you're reasoning from "this looks like it would break under concurrency",
   stop. That's a hypothetical wearing a costume.

What you may never do is invent the failure. "Presumably this breaks when two
users edit at once" is a guess, not an example.

If the source genuinely doesn't contain enough to build a real scenario, say so
in one line and stop:

```
Can't ground an example: the design doc argues from principle and never says
what actually breaks today. Worth asking the author for one.
```

That's a useful answer. It tells the user the doc has a hole in it.

## Inputs

Invoked as `/quick-explainer <thing>`. The argument points at context; figure
out what kind it is and go get it.

| Argument                     | How to gather                                                                |
| ---------------------------- | ---------------------------------------------------------------------------- |
| GitHub PR URL or number      | `gh pr view <n> --json title,body` + `gh pr diff <n>`. Diff is truth.        |
| GitHub issue URL             | `gh issue view <n> --comments`                                               |
| Nothing / "this branch"      | `git diff $(git merge-base HEAD main)...HEAD` + the branch's commit subjects |
| A file path (design, plan)   | Read it. Skim for the problem statement and the proposed change only.        |
| A Mikado graph               | Read it, plus the goal node and the current leaves.                          |
| An image / screenshot        | Read the image. Same output shape.                                           |
| A URL to a doc               | Fetch it.                                                                    |
| Pasted text                  | Use it as-is.                                                                |

Read enough to be right, not everything. For a 3000-line design doc you need the
problem it claims to solve and the shape of the fix — not the rollout plan.

If the diff and the description disagree, **the diff wins**, and that's worth one
extra line: `(The description says it also does X. The diff doesn't.)`

## Examples

**Input:** `/quick-explainer https://github.com/org/repo/pull/1842` — a PR making
multi-tab tool calls run at-most-once

```
**Tool calls fire twice when you have the app open in two tabs.**

### Today

You have the doc open in Tab A and Tab B.
The AI decides to call `sendEmail(to: bob@example.com)`.
Both tabs receive the message. Both tabs run it.
Bob gets two emails.

### After

Both tabs still receive the message.
Tab A claims the call first, runs it, writes the result back.
Tab B sees it's already claimed and does nothing.
Bob gets one email.

**The trick:** claiming is a compare-and-swap in room storage, so exactly one tab wins.
```

**Input:** `/quick-explainer` on a branch fixing `LiveList` convergence

```
**Two clients could disagree about a list forever, even after everything synced.**

### Today

Alice and Bob both have [a, b, c].
Alice moves `c` to the front. Bob deletes `c`. Same instant.
Alice ends up with [c, a, b]. Bob ends up with [a, b].
Nothing ever fixes it. Refresh, and Alice's move silently vanishes.

### After

Same two ops, same instant.
Both end up with [a, b]. Delete wins, the move is dropped.
Refresh changes nothing.

**The trick:** moving an item that's already deleted is now a no-op instead of re-inserting it.
```

**Input:** `/quick-explainer docs/td-decouple-transport.md` — a Mikado graph

```
**Goal: get the socket out of `Room`'s constructor so reconnect logic is testable.**

### The blocker right now

You want a unit test for "reconnects after a dropped connection".
You call `new Room(...)` and it opens a real WebSocket immediately.
The test hangs waiting for a server that isn't there.
So every reconnect test today is e2e and the suite takes 40s.

### After the graph is green

`new Room(transport)` takes whatever transport you hand it.
The test hands it a fake, flips it to "disconnected", asserts the retry.
3ms, no server.

**First leaf to do:** pull `SocketTransport` out behind an interface — nothing depends on it yet.
```

**Input:** `/quick-explainer` on a design doc that never states a concrete failure

```
Can't ground an example: the doc argues that the current auth model "doesn't scale
conceptually" but never names a request that fails or a thing you can't build.
Worth asking the author what actually broke.
```

## What this is not

- Not a summary. A summary covers the document; this covers one moment in it.
- Not a review. Findings, concerns, and nits belong in `/pr-review`.
- Not a deep dive. If they want the whole mechanism, that's `/visually-explain`.
- Not a starting point for doing the work. It's a starting point for *thinking*
  about the work.

Stop after the explainer. If they want more, they'll ask.

## Checklist

- [ ] 20 lines — or longer only because shrinking it made it unclear
- [ ] Every claim is a specific instance, not a category
- [ ] Today and After use the *same* scenario
- [ ] Real names, real values, real numbers — nothing placeholder-shaped
- [ ] No line numbers, no file paths, no changelog bullets
- [ ] Every line flush left — no `&nbsp;`, no indentation doing structural work
- [ ] No term used that the example hasn't grounded
- [ ] The example is a real failure (report, repro steps, test, or traced
      through the diff), not one constructed to illustrate the point
- [ ] Nothing after `The trick:` line
