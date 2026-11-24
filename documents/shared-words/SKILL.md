---
name: shared-words
description: "Use when terms clash or stay vague, a costly decision lands, or you write the glossary or decision records. New repo docs: offer first."
user-invocable: false
---
# Shared words
Gate: get the user's OK before creating a glossary or decision records in a repo that lacks them (G3). See gates.md in the skill house-rules.
Job: Keep one precise vocabulary and record why costly choices were made.
Takes: design talk and code.   Gives: glossary edits, short decision records, `Words` for a decisions artifact.

## Stores

Three stores, one rule each.

| Store | Holds | Keep out |
|---|---|---|
| Glossary | Words | Specs, scratch notes, implementation detail, general programming terms |
| Decision records | Reasons behind costly choices | Choices that are cheap to reverse or plain from the code |
| Pinned notes | Traps at one location | Vocabulary and reasons |

The lead alone writes the glossary and records, so parallel workers never conflict.

## Steps

1. **Load.** Read the docs as Project language says in the skill `house-rules`. A repo with several bounded contexts keeps a top-level index of the contexts and how they relate. Infer which one the work sits in, and ask if that isn't clear.

2. **Challenge words as they come up**, during the conversation rather than after it:
   - A clash, where one word has two meanings or two words share one. Name it and settle on one with the user.
   - A vague or overloaded word. Propose a sharper one.
   - A fuzzy concept line. Invent an edge case that tests it: "If a parcel is split at the depot, is it still one shipment?"
   - A claim about the system. Check it against the code and say what the code does.

3. **Record a settled term at once.** An entry takes a side: the one word to use, the rivals to drop, and at most two sentences defining the thing.

   ```markdown
   **Shipment**: everything bound for one address on one collection run. Avoid: parcel, consignment, order.
   ```

   Once a cluster of terms appears, group it under a heading. New or changed terms also go under `Words` in any decisions artifact in progress.

4. **Test each costly decision.** Offer a record only when all three hold: undoing the choice would be expensive, someone reading the code later wouldn't see why, and there were genuine alternatives. Likely subjects are the shape of the system, how contexts integrate, technology that locks you in, who owns what and what the project refuses to do, deliberate departures from the obvious route, constraints the code can't show, and rejections that aren't obvious.

   A single numbered paragraph stating the context, what was chosen and why can be enough. Add status, options or consequences only where they help.

   ```markdown
   12. Depot scans arrive out of order, so totals are rebuilt from the scan log each night. A running counter was simpler but drifted and couldn't be audited, so we took the slower rebuild.
   ```

5. **Handle missing docs.** While reading, say nothing. When you are about to write, offer once, using the gate's question. If the repo's tracker document names a docs layout, follow it. If the user declines, keep terms in `Words` and carry on.

6. **Stay in role.** A worker or scout leaves the glossary and records alone and lists candidates under `Learned` in its report. The lead weighs them and writes the ones that hold up.

## Done when

- Every clash or vague word raised is settled, or listed under `Open` in the decisions artifact.
- Every settled term has a glossary entry, or a `Words` line if the docs were declined.
- Every entry has one word, its rivals and at most two sentences, with no implementation detail.
- Every new record passed all three tests, and every decision that passed them was offered one.
- Only the lead wrote the glossary or records, and any docs created in a repo that lacked them were created with OK.
