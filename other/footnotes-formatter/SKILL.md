---
name: footnotes-formatter
description: "Takes a list of messy, inconsistent, or unnumbered notes and references and returns them correctly numbered, consistently formatted, and matched to your chosen citation style."
status: stable
category: production-support
subcategory: publishing
version: 1.0
eval_score: 4.2
tags: [footnotes, endnotes, citations, references, style-guide]
---
# Footnotes Formatter

## What This Skill Does
Takes a list of messy, inconsistent, or unnumbered notes and references and returns them correctly numbered, consistently formatted, and matched to your chosen citation style.

## When To Use This Skill
- A long-form article, investigation, or documentary treatment has source notes in varying formats that need standardising before publication
- A reporter has pasted their references in a mix of formats (some Chicago, some URLs only, some bare hyperlinks) and you need them uniform
- You are preparing a grant application, fund pitch, or academic-adjacent journalism piece that requires a specific citation style
- Endnotes from a Word document have lost their numbering and need to be reconstructed

## What You Need To Provide
**Required:**
- The raw footnotes or endnotes, in whatever state they are in (pasted as a list, one per line, or as a block of text)
- The citation style you want: choose one — Chicago (author-date or notes-bibliography), AP, MLA, APA, or "house style" (if house style, describe the format you want)

**Optional:**
- The text of the article or document so the assistant can check that in-text reference numbers match the notes list
- Whether these are footnotes (at the bottom of each page) or endnotes (collected at the end) — affects labelling only, not formatting
- Any special rules: e.g., "shorten URLs," "do not include access dates," "use 'ibid' for repeated consecutive sources"

## How the Assistant Approaches This
1. Reads all the raw notes and identifies each distinct source, stripping duplicates and flagging any entry that is missing information required by the chosen style (e.g., a publisher name, a publication date)
2. Applies the chosen citation format consistently: order of elements, punctuation, italics conventions, and abbreviation rules for that style
3. Numbers the final list sequentially from 1 and returns the formatted block, with a brief note at the end listing any entries where required information was missing or had to be inferred

## Output Format
A numbered list of formatted citations, ready to paste. Each entry on its own line, numbered from 1. If you provided the article text, the assistant will also return a list of any mismatches between in-text reference numbers and the note list. Missing-information flags appear as a short separate section after the main list, not inline, so you can work through them without disrupting the formatted output.

## Quality Criteria
- [ ] All entries follow the same citation style with no mixed conventions
- [ ] Numbering is sequential, starting from 1, with no gaps or repeats
- [ ] Each entry includes all elements required by the chosen style
- [ ] Missing or uncertain information is flagged explicitly, not silently omitted or guessed at
- [ ] Output is clean enough to paste directly into a document without reformatting

## Example

### Input
Style: Chicago notes-bibliography

Raw notes (pasted from a draft):
- Nakamura, H. (2021). The Logistics Gap. Meridian Press.
- https://www.portauthorityreport.org/2022/container-data — accessed March 2024
- Interview with a senior trade official, conducted by the author, November 2023
- Adeyemi, F. and Costa, R., "Port Congestion and Supply Chain Risk," Journal of Maritime Economics, vol. 14, 2020, pp. 88–104
- Nakamura same book p. 67

### Output
1. Adeyemi, Funke, and Ricardo Costa. "Port Congestion and Supply Chain Risk." *Journal of Maritime Economics* 14 (2020): 88–104.
2. Nakamura, Hiroshi. *The Logistics Gap*. Meridian Press, 2021.
3. Nakamura, *The Logistics Gap*, 67.
4. "Container Shipping Data 2022." Port Authority Research Portal. https://www.portauthorityreport.org/2022/container-data. Accessed March 2024.
5. Senior trade official. Interview by the author. November 2023.

**Missing information flags:**
- Entry 4: Page title inferred from URL — confirm the exact page title before publishing.
- Entry 5: Chicago style typically requires the city of interview or a more specific date; confirm whether to add these.

## Known Limitations
- The assistant cannot access URLs to verify that a link is live, that the page title is correct, or that the source says what the note claims. All citations must be fact-checked by the author before publication.
- For sources with complex authorship (institutional reports, government datasets, legal documents), the assistant will apply the citation style rules as best it can, but edge cases may need manual review against the full style guide.
- If you do not provide the article body text, the assistant cannot check whether in-text reference numbers match the notes list — that verification step requires both files.
- Chicago "notes-bibliography" and "author-date" styles have different in-text citation formats; make sure you specify which variant you need.

## Related Skills
- [copy-editor-assistant](../../magazine-journalism/editing/copy-editor-assistant/SKILL.md)
- [house-style-enforcer](../../magazine-journalism/editing/house-style-enforcer/SKILL.md)
