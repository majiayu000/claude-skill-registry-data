---
name: structure-improvement-advisor
description: "Takes a draft with identified or suspected structural weaknesses and produces a concrete restructuring plan — including a recommended section order and the reasoning behind each change."
status: stable
category: editing
subcategory: editing
version: 1.0
eval_score: 4.2
tags: [structure, rewriting, narrative, editing, organisation]
---
# Structure Improvement Advisor

## What This Skill Does
Takes a draft with identified or suspected structural weaknesses and produces a concrete restructuring plan — including a recommended section order and the reasoning behind each change.

## When To Use This Skill
- After running a structure flow check and you have a list of problems, but you are not sure how to fix them without unravelling the whole piece
- When a draft exists but feels fundamentally hard to follow, and you need a clear plan before you rewrite rather than redrafting blindly
- When you want to experiment with an alternative structure — inverted pyramid, narrative chronology, thematic blocks — without committing to a full rewrite first
- When an editor has returned a draft with "needs restructuring" notes and you need to translate vague feedback into specific moves

## What You Need To Provide
**Required:** The full draft text.

**Optional:** A description of the structural problem as you understand it (e.g. "the story buries the news," "the argument doesn't land until too late," "it feels like two separate pieces joined in the middle"). If an editor has given you notes, paste them in. Also useful: the target format (print feature, bulletin script, online explainer) and intended audience.

## How the Assistant Approaches This
1. Reads the draft and identifies its natural units — the distinct blocks of information, each of which does a single job (establishes context, introduces a person, presents evidence, makes an argument, provides a counterpoint, resolves the story).
2. Assesses what each block requires the reader to already know before it will make full sense, and what each block sets up for what follows. This creates a dependency map: which blocks must come first, which can float, which are doing double duty.
3. Proposes a restructured sequence that puts each block in the position where it lands with maximum clarity and impact. The proposal explains the logic behind each placement decision in plain terms — not "per narrative convention" but "because the reader needs to understand X before Y will make sense."
4. Flags any blocks that are duplicating content, carrying mixed purposes (and should be split), or missing entirely (a gap in the logic that a new passage would need to fill).

## Output Format
A restructuring plan in three parts:

**Part 1 — Diagnosis (one short paragraph)**
What the draft's current structure is doing, and where it is working against the piece's purpose.

**Part 2 — Recommended structure (numbered list)**
Each item is one block of the draft, identified by its opening words or a brief label, placed in the recommended new order. Each item includes:
- A one-line label for what the block does ("establishes the stakes," "introduces the protagonist," "delivers the central finding")
- One sentence explaining why it sits at this position in the sequence

**Part 3 — Additional actions**
Any blocks that need splitting, merging, cutting, or new material to complete the restructure. Kept brief — enough to understand the decision, not a full rewrite.

The plan is a brief working document the writer can pin next to their draft as they restructure. Typically 400–600 words. Tone is direct and practical — decisions and reasons, not general editorial advice.

## Quality Criteria
- [ ] Every block in the draft is accounted for in the restructuring plan — nothing is ignored
- [ ] Placement decisions are explained with specific reasoning, not generic structural principles
- [ ] The recommended sequence is genuinely different from the current one where a change is warranted, not a minor shuffle
- [ ] Part 3 flags are honest — missing material is called out, not smoothed over
- [ ] The plan is usable as a working document: a writer can follow it block by block without needing to re-read the diagnostic

## Example

### Input
**Format:** Online long-read, general news audience
**Problem noted:** "My editor said the piece doesn't earn its opening. The first scene is too big for where the story starts."
**Draft:**

---

**[Block A]** The appeal hearing lasted eleven minutes. After three years of legal proceedings, a wrongful dismissal case that had drawn national attention ended with a brief statement from the bench and a handshake that nobody offered. Daniel Forsythe walked out of the building alone.

**[Block B]** Forsythe had worked as a safety inspector for a regional transport authority for fourteen years. He was dismissed without notice in the spring of a year when the authority was under pressure over a series of inspection failures that had been reported in local media.

**[Block C]** The transport authority declined to comment for this article. Its legal representatives confirmed in a written statement that all proceedings had concluded and that the authority considered the matter closed.

**[Block D]** The inspection failures that preceded Forsythe's dismissal had been flagged internally. Documents obtained under freedom of information law show that Forsythe submitted three written safety reports in the eight months before he was let go. Two of the three reports were not circulated to senior management.

**[Block E]** Whistleblower protection law in this jurisdiction covers employees who report regulatory breaches through official internal channels. Forsythe used the official internal reporting system for all three submissions. Whether that affords him legal protection was the central question of the appeal.

**[Block F]** The appeal tribunal found against him on a procedural point: his legal team had missed a filing deadline. The substantive question — whether suppressing safety reports constitutes grounds for whistleblower protection — was never ruled on.

**[Block G]** He is considering a further application to a higher tribunal. His solicitor says the procedural point may itself be challengeable. That process, if it proceeds, could take another two years.

**[Block H]** Three of the inspection failures flagged in Forsythe's suppressed reports were later identified in an independent audit commissioned by the authority. The audit's recommendations have been partially implemented.

---

### Output

**Restructuring Plan — Online Long-Read**

---

**Diagnosis**

The current structure opens with the appeal outcome (Block A) before the reader understands what the appeal was about, who Forsythe is, or why his situation matters. The opening scene is genuinely strong — but it requires context the reader does not yet have to register its weight. The middle of the draft (Blocks D–F) is where the story's real substance lives, and it arrives too late. The authority's no-comment (Block C) is currently placed as if it resolves something, but it appears before the reader knows what is being alleged.

---

**Recommended structure**

1. **Block B** — *Establishes who Forsythe is and his relationship to the authority*
   The reader needs this before the appeal scene will mean anything. Fourteen years in the role, the inspection pressure, the dismissal — this is the ground the whole piece stands on.

2. **Block D** — *Presents the core allegation: safety reports submitted, two suppressed*
   Placed second so the reader understands what Forsythe actually did before entering the legal dimension. The FOI documents give this block hard factual weight — it earns its position.

3. **Block E** — *Explains the legal framework: whistleblower protection and how it applies*
   The law is context for the appeal, not backstory. It sits here so the reader arrives at the appeal already understanding what was at stake.

4. **Block A** — *The appeal scene: eleven minutes, no handshake, Forsythe walks out alone*
   Now this scene lands. The reader knows who he is, what he reported, and what the hearing was supposed to decide. The brevity of the outcome reads as devastating rather than confusing.

5. **Block F** — *The tribunal's finding: procedural defeat, substantive question unresolved*
   Follows directly from the appeal scene. Explains the eleven minutes. The unresolved whistleblower question is now the piece's unresolved question — which carries the reader forward.

6. **Block H** — *The suppressed reports' findings were later confirmed by an independent audit*
   Placed here for maximum impact: the safety concerns Forsythe raised were real, and the authority subsequently acknowledged them. This is the piece's most damaging finding and belongs near the close.

7. **Block C** — *Authority declines to comment; considers matter closed*
   Now this reads as refusal to engage with what the reader has just learned, rather than a neutral procedural note. Its placement after Block H gives it meaning.

8. **Block G** — *Further legal steps possible; two more years*
   Closes the piece on an open horizon. The reader leaves with the story unfinished, which is honest, and with the sense that the substantive question is still unanswered, which is the point.

---

**Additional actions**

- No blocks need cutting. All eight carry distinct information.
- No new material is strictly required, but consider adding one sentence to Block B naming the specific nature of the inspection failures — readers will want to know what kind of safety risk was involved before they commit to the full piece.
- Block D is currently written as a mid-piece explanatory block; moving it to position 2 means its opening sentence may need a small adjustment so it does not assume prior context. A single line change — not a rewrite.

## Known Limitations
- This skill proposes a restructure based on the draft as written. It cannot assess whether the facts are accurate, whether important information is missing from the draft entirely, or whether the story should exist in this form at all. Those are editorial judgements that require reporting knowledge the skill does not have.
- For very short pieces (under 400 words) the restructuring plan may be more detailed than the underlying problem warrants. Use the structure flow checker for a lighter diagnostic on short-form content.
- The skill works best when blocks of content are reasonably self-contained. Drafts where every paragraph is entangled with every other paragraph — no natural units — may require a manual block-by-block breakdown before the plan is useful.
- The recommended structure is a proposal, not a prescription. The writer knows things about the story — source relationships, what was said off the record, what the editor specifically flagged — that should inform the final decision.

## Related Skills
- [structure-flow-checker](../structure-flow-checker/SKILL.md)
- [copy-editor](../copy-editor/SKILL.md)
- [redundancy-checker](../redundancy-checker/SKILL.md)
- [version-diff-summariser](../version-diff-summariser/SKILL.md)
