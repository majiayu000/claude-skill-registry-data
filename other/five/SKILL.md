---
name: five
description: >
  The 5-and-5 decision checksum for a plan, feature, or bug fix that is in
  scope: exactly five load-bearing things the artifact DOES — the decisions and
  behaviors, especially choices the agent made that nobody explicitly asked
  for — and five things it explicitly does NOT do, so unwelcome decisions
  surface before approval instead of after. Use whenever the user asks for a
  decision checksum of an in-scope plan, spec, PR description, or fix —
  "five", "/five", "give me the five", "key highlights", "top five", "what
  does this plan do", "what did you decide", "what does this NOT do", "what am
  I not getting" — during planning, writing, or mid-implementation, and before
  final reports. Every item cites where the artifact says it; silence in the
  artifact is reported as "not specified", never dressed up as an explicit
  non-goal. Not a substitute for reading the artifact — it is the layer that
  tells you when to go read it. Not for ordinary content summaries when no
  artifact is under decision, and not when the user asks one specific question
  about the artifact.
argument-hint: "[artifact path, or omit to use the plan/branch under discussion]"
---

# Five — the 5-and-5 decision checksum

An operator asked an AI to move a run-time folder. The AI asked its questions, wrote the
plan, and made decisions the operator never read — the plan was long, the decisions were
buried, and approval happened on trust. Five is the layer that was missing: a checksum
computed **from the artifact**, cheap enough to skim in ten seconds, sharp enough to catch
the decision you would have vetoed.

**Exactly 5 + 5: two five-slot lists, plus the uncertainty line and the reading pointer.**

## The output contract

Emit exactly this block, nothing more:

```markdown
**Five — <artifact name>**

**Does (5):**
1. <decision or behavior, one line> — <citation: §section, file:line, or commit>
2. …
5. …

**Does NOT (5):**
1. <non-goal a reader might assume is included> — <where the artifact excludes it>
2. …
5. …

Not specified (called, not assumed): <adjacent capabilities the artifact is silent on, if any>

Bottom line: if <highest-consequence item> matters to you, read <artifact §section>.
```

The last line is mandatory. Five tells the operator **when to read the plan** — a checksum
that replaces reading is a checksum that lies by omission.

## Procedure

1. **Find the artifact.** A plan file, spec, capture doc, PR description, or the branch
   diff under discussion. If the operator names none and no plan/diff is in scope, stop.
   An artifact that **exists but is empty or whitespace-only** is the same case — a
   zero-byte plan checksums to nothing. Either way emit `Five: no artifact to checksum`
   and stop. **An empty input passes every check** — never summarize from vibes or memory
   of an earlier draft.
2. **Read the whole artifact**, not the diff. The decisions worth surfacing are usually
   the ones made quietly between the asked-for lines.
3. **List candidate highlights** — every decision and behavior the artifact commits to.
   Prioritize, in order: (a) choices the operator never explicitly asked for, (b)
   one-way-door or costly-to-undo choices, (c) behavior changes to existing surfaces,
   (d) the rest. Rank by consequence, not by section order.
4. **Build the NOT-list** from three sources, in this order of authority: (a) the
   artifact's explicit non-goals section, (b) scope boundaries stated in its text, (c)
   adjacent work a reasonable reader would plausibly assume is included. Items from (a)
   and (b) cite where the artifact says so. An item from (c) that the artifact never
   mentions goes in **Not specified** — silence is not a non-goal, and presenting an
   inferred omission as an explicit "does NOT do" is fabrication.
5. **Cut to five and five.** Keep the five highest-consequence highlights and the five
   non-goals most likely to be assumed. If fewer than five real ones exist, fill the
   remaining slots with `— nothing else load-bearing found` / `— no further exclusions
   stated` rather than padding. **Padding is worse than a short list.**

## Hard rules

- **Grounded.** Every substantive item carries a citation to where the artifact says it
  (section, `file:line`, commit). The two honest-fill markers carry none and need none.
- **Empty-input guard outranks the count.** No artifact — or an empty/whitespace-only
  one — → say so and stop, even though that means emitting fewer than ten lines. This
  rule beats the 5+5 contract every time.
- **Exactly five and five** when the artifact supports it — two full slots lists, never
  four-plus-a-shrug, never six because they all felt important.
- **Checksum, not substitute.** Never claim or imply the operator can skip reading the
  artifact on Five's say-so. The Bottom line exists to route them INTO the plan.

## What counts as a highlight

Decisions, not features. The test: *is this a thing the operator could disagree with?*

| Good | Bad (marketing — banned) |
|---|---|
| "Moves the run-time folder to `~/Library/X` and leaves a symlink at the old path — §3.2" | "Improves project organization" |
| "Drops write support for the legacy `.conf` format — L214" | "Cleans up configuration handling" |
| "Asks no further questions; unattended mode is now the default — commit a1b2c3" | "Streamlines the workflow" |

If a highlight would survive into the marketing copy of the feature, it is probably not a
highlight. The operator's veto targets are the file paths, the defaults chosen for them,
the things deleted, and the questions the agent stopped asking.

## What counts as a non-goal

Something a reasonable reader would plausibly assume is included, which the artifact
excludes. Not strawmen nobody would expect ("does not rewrite the kernel"), and not
trivia ("does not update comments"). The best non-goals are the adjacent work that would
have been *reasonable* to include:

- "Does not migrate existing data — the old folder is left in place, §3.4"
- "Does not update the docs that reference the old path — noted as follow-up, §6"
- "Does not change the install script; only the run-time location moves — §2"

If the artifact is silent on something adjacent and tempting, that item goes in
**Not specified** — flagging uncertainty honestly instead of inventing a boundary.

## When NOT to run Five

- The operator asks you to *write or revise* the plan — do that; offer Five afterward.
- The operator asks a specific question about the artifact — answer it; don't force the
  5+5 shape on a one-question ask.
- The artifact does not exist yet. Never checksum an intention.

## Non-goals of Five itself

- No scoring, no grades, no severity numbers — ranking within a list is by consequence,
  and that is all.
- No persistence, no modes, no intensity levels. One invocation, one block.
- No reading of the operator's mind: Five reports what the artifact says, and marks the
  rest "not specified".
- Zero scripts, zero runtime — this file is the whole skill.
