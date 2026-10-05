---
name: print-web-reformatter
description: "Adapts print-formatted article text — including column breaks, orphaned lines, print-specific conventions, and layout-dependent phrasing — for clean web publication, producing copy that reads naturally in a single-column digital environment."
status: stable
category: production-support
subcategory: publishing
version: 1.0
eval_score: 4.2
tags: [print, web, reformatting, column-breaks, widows, digital-publishing, production]
---
# Print/Web Reformatter

## What This Skill Does
Adapts print-formatted article text — including column breaks, orphaned lines, print-specific conventions, and layout-dependent phrasing — for clean web publication, producing copy that reads naturally in a single-column digital environment.

## When To Use This Skill
- You are repurposing a published print article for the web and the text contains phrasing or structure that only makes sense on a page (e.g., "continued on page 14," "see chart, left," "as shown opposite")
- A print sub-editor has delivered copy with hard column breaks, soft hyphens, or condensed spacing that needs cleaning for a CMS paste-in
- You are digitising archive print material and need it to read as natural web prose
- A designer has exported article text from InDesign and it contains layout artefacts

## What You Need To Provide
**Required:** The article text as it comes from the print source — paste it in full, with all artefacts intact (broken words, mid-sentence column breaks, "continued" labels, cross-references to page positions or layout elements, print-specific abbreviations).

**Optional:** The original print format (broadsheet, tabloid, magazine double-spread, newsletter column). The target web format (full-width web article, mobile-first single column, newsletter email body). Any house style notes for the web version (e.g., subheadings required every 400 words, links should be added at named sources).

## How the Assistant Approaches This
1. Scans the pasted text for print artefacts — column-break mid-words (soft hyphens), "continued" notices, page cross-references ("see page 4," "chart, right," "above"), orphaned single words at paragraph ends that were forced by column width, and condensed or expanded spacing from InDesign export.
2. Resolves each artefact: rejoins broken words, removes continuation notices, rewrites positional cross-references as self-contained web phrases (e.g., "see chart, left" becomes "see the chart below" or the reference is absorbed into the sentence if no chart will appear on the web page), and normalises paragraph spacing.
3. Checks the text for print conventions that read awkwardly on screen — heavily condensed sentences written to fill a column count, paragraph structures that depend on a page turn for dramatic effect, and any footnote or sidebar references that point to print-only elements. Rewrites or flags these for editorial decision.

## Output Format
The fully reformatted article text, ready to paste into a CMS. Delivered in two parts: (1) the clean text, and (2) a short editorial notes section listing every change made and any decision that requires the editor's sign-off (e.g., "removed reference to sidebar 'Key Dates' — confirm whether a web equivalent will be published"). Paragraph spacing follows web conventions: a blank line between paragraphs, no indentation. Tone and language are preserved exactly as written by the author.

## Quality Criteria
- [ ] No print artefact remains in the cleaned text — no soft hyphens, no "continued" notices, no positional page references
- [ ] Every positional cross-reference ("see opposite," "as shown left") is either rewritten for web or flagged for editorial decision — none are silently deleted
- [ ] Author's voice, sentence structure, and word choice are preserved; only layout artefacts and positional conventions are changed
- [ ] The editorial notes section accounts for every substantive change made
- [ ] Output reads as natural, continuous web prose with no awkward line lengths or forced breaks

## Example

### Input
Print format: broadsheet newspaper, three-column layout
Target: full-width web article

---

Pasted text (as exported from InDesign):

The floods came without warning. In the valley town of Mireaux, pop-
ulation 4,200, residents had less than ninety minutes to gather what
they could carry before the river broke its banks for the first time in
recorded history.

"We had been told the levee would hold," said Clara Fontaine, 67, who
lost her home of forty years. "Nobody believed it could fail. Nobody."
                                                           [Continued on p.7]

Local emergency services were overwhelmed within hours. By nightfall,
fourteen residential streets were submerged. For a full breakdown of
affected zones, see the map on page 8.

The regional government has since launched an independent review —
see panel, right — but critics say the inquiry lacks the statutory pow-
er to compel testimony from infrastructure contractors.

The EU has offered emergency relief funds. Details on p.8.

[SIDEBAR: Key Dates
— March 2019: levee construction completed
— June 2022: first structural survey flagged hairline fractures
— April 2024: flood event]

Fontaine now lives with her daughter forty kilometres away. She does
not expect to return. "Mireaux is still there," she said. "But it isn't
home any more."

---

### Output

**Reformatted Article Text**

The floods came without warning. In the valley town of Mireaux, population 4,200, residents had less than ninety minutes to gather what they could carry before the river broke its banks for the first time in recorded history.

"We had been told the levee would hold," said Clara Fontaine, 67, who lost her home of forty years. "Nobody believed it could fail. Nobody."

Local emergency services were overwhelmed within hours. By nightfall, fourteen residential streets were submerged.

The regional government has since launched an independent review, but critics say the inquiry lacks the statutory power to compel testimony from infrastructure contractors.

The EU has offered emergency relief funds.

Fontaine now lives with her daughter forty kilometres away. She does not expect to return. "Mireaux is still there," she said. "But it isn't home any more."

---

**Editorial Notes**

1. **Soft hyphens removed.** Words broken mid-line by column width ("pop-ulation," "pow-er") have been rejoined. Check: population, power, recorded — confirm spellings in original manuscript if any doubt.

2. **"Continued on p.7" removed.** This notice was a print navigation aid. No equivalent is needed for the web article.

3. **"See the map on page 8" — reference removed from body text.** The sentence now reads: "By nightfall, fourteen residential streets were submerged." Decision required: if an interactive or static map will be embedded in the web article, reinsert a reference such as "By nightfall, fourteen residential streets were submerged — see the map below." If no map will be published on web, the current clean sentence stands.

4. **"See panel, right" removed.** The inline reference to the print sidebar has been removed from the sentence about the independent review. The sentence now reads as self-contained prose. Decision required: if the sidebar content (Key Dates) will be published as a web fact box, consider adding "A timeline of key dates is published below this article" at the end of the paragraph.

5. **"Details on p.8" removed.** The sentence now reads: "The EU has offered emergency relief funds." Decision required: if the web article will link to the EU relief announcement, rewrite as: "The EU has offered emergency relief funds — [link text]."

6. **Sidebar "Key Dates" not included in clean text.** The sidebar was a print-only element and has not been incorporated into the web body. Decision required: if it is to be published on web, it can run as a formatted fact box. The content is preserved here for your use:
   - March 2019: levee construction completed
   - June 2022: first structural survey flagged hairline fractures
   - April 2024: flood event

## Known Limitations
- This skill reformats text and flags decisions — it does not make editorial judgements about whether removed content should be replaced with a web equivalent. Every flagged decision requires a human editor to confirm.
- Soft hyphens from InDesign exports are not always visible when pasting into a chat interface. If you suspect hidden hyphens remain in a word, search the cleaned text for unusual hyphenation before publishing.
- This skill cannot access the original print PDF or InDesign file. It works only from pasted text. If the export is incomplete or garbled, some artefacts may be missed — always compare the cleaned text against a physical copy of the original article before publishing.
- Positional references to print-only elements (sidebars, charts, maps) are flagged but not automatically replaced with web links or embeds. That step requires the editor to know which digital assets will accompany the web version.

## Related Skills
- [format-converter-brief](../format-converter-brief/SKILL.md)
- [layout-placement-advisor](../layout-placement-advisor/SKILL.md)
