---
name: communicate
description: Communication discipline for writing, rewriting, distilling, and reviewing any text meant for human reading, including conversation, task files, planning updates, results, reports, reviews, handoffs, and documentation. Use for every message or artifact a human will read; Must load for superRA who produces human-facing text. 
---

# Communicate

Be **terse** — in chat, returns, task files, and documents. One sentence when one is enough. **The style holds all session** — do not drift back to full prose.

## Write for a reader with no session context

They have the artifact and the repo, not your conversation.

- Session vocabulary: use the standard term.
- Reintroduce a term, sample, or object when it returns after a long gap.
- Editing-history cues: "the table now defines" and "the updated script" have no *before* for this reader.
- A correction is an instruction, not content. When users provide feedback, "No, this is not a robustness check", you fix or delete the sentence without stressing the correction. The reader sees only the final text.
- Every claim the reader may rely on links its artifact, output, source, or commit.

## Pyramid structure

The main point comes first at every level.

- **Message:** the opening line is the outcome, decision, or current state. No preamble, no restating the request, no recap of what you just did, no closing offer.
- **Section:** the heading states the point — `The merge loses 0.7% of observations`, not `Merge results` — and the section reads alone. Split by main points, not by template slots.
- **Nested structure:** nesting at all levels (sections and subsections, nested lists, ...), each layer progressively reveals more detail. 
- **Paragraph:** the first sentence carries the message.

One set of facts, three shapes.

**✗ Paragraph wall** — outcome, evidence, caveat, and implementation detail compete in one block.

> The panel build completed after joining CRSP and Compustat. We ran the merge on firm and month and retained 252,341 observations from 1994 through 2023. There were 1,663 observations without a CRSP match, which is 0.7% of the input, and the output is stored in `Data/panel.parquet`. This means the panel is ready for the alpha regressions, although analyses requiring unmatched firms need a different sample.

**✗ Flat list** — shorter, but every item appears equally important and relationships disappear.

- The panel build completed.
- The panel has 252,341 observations from 1994 through 2023.
- The merge used firm and month.
- The output is in `Data/panel.parquet`.
- The merge dropped 1,663 observations, or 0.7%.
- Analyses requiring unmatched firms need a different sample.

**✓ Nested pyramid** — the first level carries the result; each child limits or locates it.

- The 252,341-observation panel is ready for the 1994–2023 alpha regressions.
  - Analyses requiring unmatched firms need a different sample.
  - The firm-month merge drops 1,663 observations, or 0.7%, without a CRSP match.
  - The maintained output is [`Data/panel.parquet`](../../Data/panel.parquet).

## Choose the form

For long reports, break the document into sections and subsections. Within each block, follow the pecking orders:

- **visualization > tables > prose:** when presenting data, visualize whenever possible; if not, tabulate; 
- **Nested bullet points:** several main points, each with its support or action beneath it.
- Only use **Paragraph** when you need connected reasoning, narrative, or causality whose order a list would break.

## Carry the paragraph forward

- **Start each sentence with something the reader already has; end with what is new.**
  - Test: read three consecutive subjects. Each repeating or succeeding the previous topic means the flow holds; three fresh terms mean it broke.
  - Introducing a topic, or running a deliberate parallel list: fresh subjects are the job.
- **One idea per paragraph.** An idea that needs more than five or six sentences is two ideas.
- **Put the transition at the start.** `however`, `in contrast`, `consequently` belong at the front of the pivoting sentence, not buried mid-sentence.

## Cut the lines that carry little novel information

**Cover a line and read only its heading and parent bullet.** Still predictable from those? It added nothing — delete it.

- `Pyramid structure` → `Lead with the main point`: predictable, cut.
- `Pyramid structure` → `Sibling bullets take the same grammatical form`: new instruction, keep.

A line earns its place by adding a claim, number, caveat, decision, or action.

- **Cut whole units first.** Drop a bullet or a section before compressing the sentences inside one.
- **State each fact once.** Full detail where it is produced or maintained; link there from everywhere else.
- **Keep one example.** Add a second only when it teaches a different case.
- **Keep the words that carry cause, contrast, condition, or sequence.**
- **Choose clear over short.** Explain dependencies, surprising results, irreversible actions, and easy-to-miss caveats in full.

## Fix the sentence

Each rule fires on a real reading problem; applying one to a line that already reads clearly is a failed edit. Preserve technical vocabulary, first-person voice, emphasis, and meaningful punctuation; code, commands, paths, numbers, and error strings stay verbatim.

- **Name the actor and the action.**
  - "The hook blocks the edit" — not "Blocking is performed."
  - "The firm-month merge drops 1,663 observations" — not "There is some observation loss."
  - Passive voice when the actor is unknown or irrelevant.
- **Delete the clause that survives deletion.** Read the sentence without it; if it still works, it was filler.
  - "in order to" → "to"; "serves as" → "is"; "utilize" → "use".
  - Filler and pleasantries go first: "just", "basically", "actually", "of course", "happy to".
  - "It is worth noting that the merge drops 0.7%." → "The merge drops 0.7%."
  - "This is a significant improvement." → give the number, or cut the sentence.
  - Say what a thing is, not what it is not: never "it's not X, it's Y."
- **Keep the hedge that changes a decision.**
  - Keep: "The estimate is probably biased downward."
  - Cut: "somewhat unclear results were obtained" — say what the results are.
  - Never stack hedges: "may possibly suggest" claims less than "suggests".
- **Give `this`, `it`, and `these` a noun** when more than one recent noun could be the antecedent: "this drop", "this specification".
- **Replace a vague quantifier with the count.** "several observations" → "1,663 observations"; "a number of tests" → "three tests". Keep the vague form when the count genuinely does not matter.
- **Break a stack of three or more nouns.** "firm-year panel data regression specification" → "the specification of the firm-year panel regression". Keep recognized terms of art intact.
- **Use one name per concept.** No rotating synonyms, and no abbreviation you invented (`cfg`, `impl`). Define an unfamiliar term at first use.
- **Write short, complete sentences.** In prose, no fragments and no arrow chains (`merge → 0.7% → fine`).

## Route the work
- When editing a markdown file, **MUST** load [markdown.md](references/markdown.md) for formatting and presentation. 
- **Rewriting existing material, or auditing why text is hard to read:** load [rewrite.md](references/rewrite.md).

## Final pass

- **Read only the opening and top-level bullets.** They should carry the answer or current state; in prose, consecutive first sentences should read as a coherent storyline.
- **Run § Cut the lines that carry little novel information once over the whole draft.** Restore any relationship that became unclear.
- **Check the diff, not the length.** No claim got stronger, no caveat disappeared, no voice flattened.
