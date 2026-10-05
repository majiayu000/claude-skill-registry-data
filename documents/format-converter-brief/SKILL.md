---
name: format-converter-brief
description: "Produces a clear, step-by-step brief explaining exactly how to convert a finished article or document from one format (Word, plain text, InDesign export) into a specified target format (Markdown, HTML, or structured plain text), preserving all editorial elements correctly."
status: stable
category: production-support
subcategory: publishing
version: 1.0
eval_score: 4.2
tags: [formatting, markdown, html, conversion, production, workflow]
---
# Format Converter Brief

## What This Skill Does
Produces a clear, step-by-step brief explaining exactly how to convert a finished article or document from one format (Word, plain text, InDesign export) into a specified target format (Markdown, HTML, or structured plain text), preserving all editorial elements correctly.

## When To Use This Skill
- You need to move a finished article from a Word document into a CMS that uses Markdown or HTML
- A web editor has sent you a piece that needs to be posted to a platform with specific markup requirements
- You are handing off formatted copy to a developer or digital producer and need to give them precise conversion instructions
- You are preparing archival versions of published articles in multiple formats

## What You Need To Provide
**Required:** The source format (e.g., Word .docx, InDesign exported .txt, plain email text) and the target format (Markdown, HTML, or structured plain text). A description or paste of the article's structural elements — headings, subheadings, pull quotes, captions, byline, bullet lists, embedded links, footnotes.

**Optional:** The name or type of CMS the output will be pasted into (WordPress, Arc, Contentful, Ghost). Any house style rules that affect markup — for example, whether `<h2>` or `##` is used for section heads, or whether links open in new tabs.

## How the Assistant Approaches This
1. Identifies every structural element in the source document — body paragraphs, headlines, subheadings, captions, bylines, pull quotes, bullet lists, links, footnotes — and maps each to its correct equivalent in the target format.
2. Flags any elements that have no clean equivalent in the target format (for example, multi-column layouts or decorated drop caps in Word have no Markdown equivalent) and recommends a practical workaround.
3. Produces a brief structured as a numbered conversion checklist: one instruction per element type, written in plain language so that any editor — not just a developer — can follow it without ambiguity.

## Output Format
A numbered conversion checklist, typically 8–15 items. Each item names the source element, states the target markup or convention, and includes a short example showing before and after. Ends with a short "Watch out for" section listing two or three common conversion errors specific to this format pair. Plain, professional language — no technical jargon beyond the markup itself.

## Quality Criteria
- [ ] Every structural element mentioned in the source description has a corresponding instruction
- [ ] Each instruction includes a concrete before/after example, not just a rule statement
- [ ] The "Watch out for" section is specific to the source/target pair, not generic advice
- [ ] No instruction requires the editor to know how to code — only to copy and paste markup
- [ ] Any element that cannot convert cleanly is flagged with a practical workaround

## Example

### Input
Source format: Word document (.docx)
Target format: Markdown (for Ghost CMS)

Article structure:
- Headline in Title style
- Byline below headline (Author Name, Date)
- Three section subheadings in Heading 2 style
- Body paragraphs in Normal style
- One pull quote (italicised, indented in Word)
- One bulleted list (Word auto-bullets)
- Three hyperlinks embedded in body text
- Two image captions below photos (Caption style in Word)
- One author bio paragraph at the end (italicised Normal)

No footnotes. No footnotes. CMS is Ghost 5. Links should open in the same tab.

### Output

## Format Conversion Brief: Word → Markdown (Ghost 5)

**Source:** Word .docx
**Target:** Markdown for Ghost 5 CMS
**Prepared for:** Editorial handoff

---

### Conversion Checklist

1. **Headline (Title style → `#` heading)**
   Word: `Urban Heat: How Cities Are Rewriting the Climate Rulebook`
   Markdown: `# Urban Heat: How Cities Are Rewriting the Climate Rulebook`
   Paste this as the first line of your Markdown file. Ghost will use it as the article title.

2. **Byline (below headline → plain text block)**
   Word has no standard Markdown equivalent for bylines. In Ghost, enter the author in the post settings panel — do not include it in the body text. The date is set in the post settings as well. Delete the byline line from the Markdown body entirely.

3. **Section subheadings (Heading 2 → `##`)**
   Word: subheading in Heading 2 style
   Markdown: `## Your Subheading Here`
   Apply this to all three subheadings. Use `##` only — do not use `###` unless you have a third level of heading in the original.

4. **Body paragraphs (Normal style → plain paragraphs)**
   No markup needed. Paste body text as-is, with a blank line between each paragraph. Remove any double spaces after full stops — use single spaces throughout.

5. **Pull quote (italicised indent → blockquote)**
   Word: indented italicised paragraph
   Markdown: `> "No city has solved this alone — the answers are regional or they are nothing."`
   Place the `>` symbol at the start of the line. Do not use quotation marks unless they appear in the original text.

6. **Bulleted list (Word auto-bullets → Markdown list)**
   Word: auto-formatted bullet points
   Markdown:
   ```
   - First item
   - Second item
   - Third item
   ```
   Use a hyphen and a space before each item. Remove any tab indentation Word may have added.

7. **Hyperlinks (embedded links → inline Markdown links)**
   Word: underlined blue text with a URL attached
   Markdown: `[link text](https://example.com)`
   Example: `[a 2023 IPCC report](https://ipcc.ch/report/ar6)` — links open in the same tab by default in Ghost Markdown, which matches your requirement. Do not add `{:target="_blank"}`.

8. **Image captions (Caption style → italic text below image card)**
   In Ghost, captions are entered directly in the image card after uploading the photo — not in the Markdown body. Remove caption text from the Markdown file. Keep the captions in a separate notes document to paste into Ghost after upload.
   Markdown caption format (if your Ghost theme uses it): `*A caption describing the image.*`

9. **Author bio (italicised paragraph → italic Markdown)**
   Word: italicised Normal paragraph at article end
   Markdown: `*Firstname Lastname is a journalist covering urban planning and climate adaptation. They are based in [City].*`
   Wrap the entire paragraph in single asterisks. Place it after a horizontal rule: `---` on its own line, then the bio.

---

### Watch Out For

- **Smart quotes.** Word uses curly quotation marks (`"` `"`). Some Markdown parsers handle these fine; others display them as garbled characters. If you see strange symbols in Ghost preview, do a find-and-replace: swap `"` for `"` and `'` for `'` throughout.
- **Hidden line breaks.** Word sometimes inserts a soft return (Shift+Enter) inside paragraphs. These paste as `<br>` tags in some editors, breaking your paragraph spacing. Check that each paragraph is separated by a full blank line, not a single line break.
- **Table formatting.** If the article contains any tables not mentioned above, contact the digital producer before converting — Word tables require manual Markdown table markup and are not covered by this brief.

## Known Limitations
- This skill produces a conversion brief — instructions for a human to follow — not an automated conversion. It will not paste or reformat the article itself; that step remains with the editor.
- Format briefs are specific to the source/target pair. If your CMS uses a custom markup dialect (Arc XP, Brightspot), the standard Markdown instructions may need adjustment — mention your CMS when requesting the brief.
- Complex Word documents with tracked changes, comments, or revision marks should have those resolved before conversion; this skill assumes a clean final draft.

## Related Skills
- [print-web-reformatter](../print-web-reformatter/SKILL.md)
- [layout-placement-advisor](../layout-placement-advisor/SKILL.md)
