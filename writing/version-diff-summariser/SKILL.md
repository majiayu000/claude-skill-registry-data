---
name: version-diff-summariser
description: "Takes two versions of the same text — a before and an after — and produces a plain-English summary of every meaningful change: what was added, cut, reworded, restructured, and why each change is likely to matter editorially."
status: stable
category: editing
subcategory: editing
version: 1.0
eval_score: 4.2
tags: [editing, revision, version-control, copy-editing, collaboration]
---
# Version Diff Summariser

## What This Skill Does
Takes two versions of the same text — a before and an after — and produces a plain-English summary of every meaningful change: what was added, cut, reworded, restructured, and why each change is likely to matter editorially.

## When To Use This Skill
- After an editor returns a marked-up draft and you want to understand the full scope of revisions quickly
- When handing a revised piece to a second editor who was not involved in the first round and needs to be brought up to speed
- During collaborative writing when two people have worked on the same section independently and you need to reconcile the differences
- When preparing a correction or update to a published article and you want a clear record of what changed for your corrections log
- Before a legal or compliance review, to document the changes made between draft stages

## What You Need To Provide
**Required:** Both versions of the text, clearly labelled. Paste Version A (original) first, then Version B (revised), separated by a clear divider such as `--- VERSION B ---`.
**Optional:** A brief note on who made the changes and why (e.g., "editor tightened for length" or "legal flagged the third paragraph"). This context lets the assistant frame the summary more accurately.

## How the Assistant Approaches This
1. Reads both versions carefully, mapping the structure of each — paragraphs, sentences, key claims — to understand what belongs to what.
2. Identifies every category of change: deletions (content removed), additions (new content), rewrites (same idea, different words), structural moves (content shifted to a new position), and register or tone shifts (same meaning, changed level of formality or emphasis).
3. Produces a layered summary: a one-paragraph overview of the overall direction of the edit, followed by a change-by-change breakdown. Each item in the breakdown notes what changed, where it appears, and why the change is likely to matter — editorially, factually, or legally.

## Output Format
- **Overall summary:** One paragraph (3–5 sentences) describing the net effect of the revision — e.g., whether the piece was tightened, softened, restructured, or had new material added.
- **Change log:** A numbered list of individual changes. Each entry follows this format:
  - *Type of change* (Addition / Deletion / Rewrite / Structural move / Tone shift)
  - *Location* (e.g., "Opening paragraph", "Second quote", "Final sentence")
  - *What changed*, quoted briefly
  - *Why it matters* — one sentence on the editorial, factual, or legal significance
- Tone is neutral and descriptive — no judgment about whether the changes are improvements.
- Length scales with the volume of changes: a light edit produces a short log; a heavily revised draft produces a longer one.

## Quality Criteria
- [ ] Every substantive change is captured — no meaningful addition, deletion, or rewrite is missed.
- [ ] Trivial changes (punctuation corrections, single-word spelling fixes) are noted only in aggregate, not itemised individually, to keep the log usable.
- [ ] The "why it matters" note for each item is specific to that change — not a generic observation.
- [ ] The overall summary accurately reflects the balance of changes (e.g., does not describe a piece as "lightly edited" if substantial content was removed).
- [ ] Both versions are quoted accurately — no paraphrasing that misrepresents what was actually written.

## Example

### Input

**VERSION A (original)**

The proposed merger between Calloway Group and Sentinel Media has drawn criticism from several industry observers who say the deal will reduce competition in regional news markets. Regulators are expected to review the transaction before the end of the year.

Calloway Group declined to comment. A spokesperson for Sentinel Media said the merger "will strengthen local journalism in underserved communities."

Analysts say the combined entity would control roughly 30 percent of regional print circulation in the country.

--- VERSION B ---

**VERSION B (revised)**

The proposed merger between Calloway Group and Sentinel Media has drawn significant criticism from industry observers and press-freedom advocates, who warn that the deal would eliminate meaningful competition in regional news markets and put dozens of editorial jobs at risk.

Regulators at the National Media Authority are expected to open a formal review before the end of the first quarter.

Calloway Group did not respond to requests for comment. A spokesperson for Sentinel Media said the merger "will strengthen local journalism in underserved communities," though critics dispute this characterisation.

Independent analysts estimate that the combined entity would control approximately 34 percent of regional print circulation — a figure the companies have not confirmed.

### Output

**Overall summary**

The revision substantially strengthens the critical framing of the story. The language around industry concern is sharpened and expanded to include press-freedom advocates, a specific regulatory body is named, a disputed characterisation is flagged, and the circulation figure is revised upward with a new caveat. The piece is now more assertive in tone and carries more factual specificity throughout.

**Change log**

1. **Rewrite** — Opening sentence, criticism language
   Original: "drawn criticism from several industry observers who say"
   Revised: "drawn significant criticism from industry observers and press-freedom advocates, who warn that"
   *Why it matters:* "Significant" adds editorial weight; adding press-freedom advocates broadens the scope of opposition and may require these sources to be named or documented.

2. **Addition** — Opening sentence, consequences of merger
   Added: "and put dozens of editorial jobs at risk"
   *Why it matters:* A new factual claim — job losses — has been introduced. This needs attribution before publication; it is currently unsourced.

3. **Rewrite** — Second sentence, regulatory timeline
   Original: "Regulators are expected to review the transaction before the end of the year."
   Revised: "Regulators at the National Media Authority are expected to open a formal review before the end of the first quarter."
   *Why it matters:* The regulatory body is now named (verify the name is accurate) and the timeline has been made more specific. Both changes create factual liability if incorrect.

4. **Rewrite** — Calloway quote line
   Original: "Calloway Group declined to comment."
   Revised: "Calloway Group did not respond to requests for comment."
   *Why it matters:* A legal and editorial distinction — "declined" implies active refusal; "did not respond" implies non-contact. Ensure the revised phrasing matches what actually happened.

5. **Addition** — After Sentinel Media quote
   Added: "though critics dispute this characterisation"
   *Why it matters:* Adds balance but introduces an unnamed "critics" — attribution needed.

6. **Rewrite** — Analyst circulation figure
   Original: "roughly 30 percent"
   Revised: "approximately 34 percent"
   *Why it matters:* The figure has changed by four percentage points. Verify which figure is correct and update the source citation accordingly.

7. **Addition** — End of analyst sentence
   Added: "— a figure the companies have not confirmed"
   *Why it matters:* Adds editorial transparency. Ensure this is factually accurate — if the companies have confirmed the figure elsewhere, this line creates an error.

## Known Limitations
- The assistant works from the text you provide, not from tracked changes or a file diff. If the two versions are structurally very different (e.g., completely rewritten rather than revised), the log may not be able to map every original sentence to its revised counterpart, and some changes may be described at paragraph level rather than sentence level.
- Very long documents (over approximately 2,000 words per version) may result in a change log that is too long to act on efficiently. For long pieces, consider submitting one section at a time.
- The assistant does not flag whether a change is an improvement — only what changed and why it might matter. Editorial judgment on the quality of the revision remains yours.
- Formatting changes (bullet points becoming prose, headers added or removed) are noted but described in general terms only.

## Related Skills
- [copy-editor](../copy-editor/SKILL.md)
- [unattributed-claims-checker](../unattributed-claims-checker/SKILL.md)
- [structure-flow-checker](../structure-flow-checker/SKILL.md)
- [correction-notice-writer](../../writing/articles/correction-notice-writer/SKILL.md)
