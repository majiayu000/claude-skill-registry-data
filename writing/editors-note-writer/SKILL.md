---
name: editors-note-writer
description: "Writes a clear, credible editor's note that explains to readers why an article has been updated, corrected, retracted, or needs a disclosure — in plain language and a professional tone."
status: stable
category: writing
subcategory: articles
version: 1.0
eval_score: 4.2
tags: [editor's note, transparency, corrections, disclosure, articles]
---
# Editor's Note Writer

## What This Skill Does
Writes a clear, credible editor's note that explains to readers why an article has been updated, corrected, retracted, or needs a disclosure — in plain language and a professional tone.

## When To Use This Skill
- A factual error has been found and the article is being corrected after publication
- A conflict of interest, funding source, or relationship needs to be disclosed
- An article is being substantially updated because circumstances have changed since original publication
- A source has retracted a statement and the article must reflect that
- An article is being republished or re-promoted and context has shifted
- Legal, editorial, or ethical review requires a note be attached to a piece

## What You Need To Provide
**Required:**
- The reason for the note (correction, update, disclosure, retraction, republication)
- What specifically changed, was wrong, or needs to be disclosed
- The date the original article was published
- The date the note is being added

**Optional:**
- The original incorrect text (for corrections)
- Any statement from a source or spokesperson that prompted the change
- Whether to link to a related correction policy or a fuller explanation
- House style preference (e.g., italics, bold label, inline vs. top-of-article placement)

## How the Assistant Approaches This
1. Identifies the type of note needed (correction, update, disclosure, retraction, or editorial context) and applies the conventions appropriate to that type — corrections name the error directly; disclosures state the relationship; updates explain what changed and why
2. Drafts the note in a direct, professional voice that acknowledges the issue without excessive apology or defensiveness — the note builds trust by being specific, not by over-explaining
3. Formats the note for top-of-article placement with a clear label ("Editor's note:", "Correction:", "Disclosure:") and a concise body of one to three sentences, ending with both the original publication date and the note date

## Output Format
One labeled paragraph, 30–80 words. Label in bold, body in plain prose. Formal but accessible register — no jargon. Dates spelled out (e.g., "March 19, 2026"). No bullet points. Reads like a note from a named masthead, even when the author is anonymous.

## Quality Criteria
- [ ] The label accurately names the type of note (Correction, Editor's note, Disclosure, Update, Retraction)
- [ ] The specific error, change, or disclosure is named — not described vaguely
- [ ] Both publication date and note date are present
- [ ] Tone is accountable and calm — neither defensive nor excessively apologetic
- [ ] Length is under 80 words and every word earns its place
- [ ] A reader who hasn't read the article understands what happened from the note alone

## Example

### Input
Reason for note: Correction
What was wrong: The article stated that the city council vote took place on March 4. It actually took place on March 11.
Original publication date: March 14, 2026
Note date: March 19, 2026
Original incorrect text: "The council voted 7–2 on March 4 to approve the rezoning proposal."

### Output
**Correction:** An earlier version of this article incorrectly stated that the city council voted on March 4. The vote took place on March 11. The article has been updated to reflect the correct date. Originally published March 14, 2026. Corrected March 19, 2026.

## Known Limitations
- This skill writes the note itself but cannot assess whether a correction, disclosure, or retraction is legally or editorially warranted — that judgment belongs to the editor or legal team
- For complex multi-error corrections or articles under active legal scrutiny, the output should be reviewed by counsel before publication
- House style for notes varies widely; if your publication has a strict format (e.g., correction placed at the bottom, specific phrasing required), supply that convention in the input
- Does not generate corrections policy pages or public accountability reports — it writes the note only

## Related Skills
- [copy-editor-assistant](../../../magazine-journalism/editing/copy-editor-assistant/SKILL.md)
- [correction-notice-writer](../correction-notice-writer/SKILL.md)
- [defamation-risk-checker](../../../magazine-journalism/legal/libel-check-brief/SKILL.md)
