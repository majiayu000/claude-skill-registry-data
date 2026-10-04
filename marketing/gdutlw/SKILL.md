---
name: gdut-thesis-formatter
description: adjust, review, and standardize guangdong university of technology undergraduate thesis documents according to the official formatting handbook. use when a user asks to format, reformat, polish layout, check compliance, or generate a thesis template for gdut graduation theses, including cover, abstract, table of contents, body text, headings, figures, tables, formulas, references, acknowledgements, appendices, translation section, and binding order.
---

# GDUT thesis formatter

Use this skill to turn an existing thesis draft, outline, or template into a document that follows the GDUT undergraduate graduation thesis handbook.

## Working method

1. Identify the user's target:
   - **format an existing thesis** → inspect the current structure and point out mismatches first, then rewrite or restyle section by section.
   - **create a fresh template** → generate a complete skeleton in handbook order.
   - **check compliance** → return a checklist with pass/fail items and concrete fixes.
2. Prefer the handbook rules over generic thesis conventions whenever they conflict.
3. If the user gives only partial content, fix what is present and clearly note what still needs manual completion.
4. Keep the user's academic content unchanged unless they also ask for language polishing.

## Output modes

Choose the response format that best matches the request.

### 1. Compliance review

Use a structured checklist with these sections:
- page setup
- front matter
- heading hierarchy
- body text
- figures, tables, formulas
- references
- appendix and extras
- binding order

For each issue, provide:
- current problem
- required handbook rule
- exact fix

### 2. Direct formatting instructions

When the user is editing in Word or WPS, give explicit settings such as:
- margins
- line spacing
- font family and size
- heading level format
- page number placement
- section order

Avoid vague advice like “adjust appropriately”. Give concrete settings.

### 3. Template generation

When generating a template, keep the section order below and include placeholder labels.

## Required thesis order

For the main bound thesis, default to this order:
1. cover
2. academic integrity statement
3. task book
4. mid-term inspection form
5. review form and defense evaluation form
6. defense record
7. chinese abstract
8. english abstract
9. table of contents
10. main text
11. references
12. acknowledgements
13. appendices
14. folded engineering drawings or work photos when required

For the separately bound foreign-language translation section, use:
1. cover
2. table of contents
3. translated text (1)
4. source text (1)
5. translated text (2)
6. source text (2)

## Core formatting rules

Apply these defaults unless the user provides a department-specific exception.

### Page setup
- paper size: A4
- top margin: 30 mm
- bottom margin: 25 mm
- left margin: 30 mm
- right margin: 20 mm
- line spacing: 1.5 lines
- page numbers: arabic numerals, start from the introduction/body section, place at the right side of the footer
- cover, chinese/english abstract, and table of contents do not carry thesis page numbers

### Fonts
- cover thesis title: bold heiti, size 2
- chapter titles: bold heiti, size 3
- section titles: bold heiti, small 4
- clause titles: heiti, small 4
- main body: songti, small 4
- page numbers: times new roman, size small 5
- arabic numbers and latin letters in body: times new roman

### Abstracts
- chinese abstract title: “摘要”, bold heiti, size 3
- chinese abstract text: songti, small 4, 1.5-line spacing
- chinese abstract length for thesis: around 400 words in chinese
- keywords line: “关键词”, bold heiti, size 4; 3 to 5 keywords separated by commas, no punctuation after the last keyword
- english abstract must match the chinese abstract in meaning
- english abstract and english keywords use times new roman

### Table of contents
- use up to level 3 headings
- engineering/science and social science default numbering: 1 / 1.1 / 1.1.1
- first-level toc entries: bold heiti, small 4
- lower-level toc entries: songti, small 4
- page numbers and arabic numerals use times new roman
- toc titles and page numbers must match the body exactly

### Main text structure
Default major sections:
- introduction
- main chapters
- conclusion

Rules:
- each chapter starts on a new page
- chapter titles should usually stay within 15 chinese characters
- avoid punctuation in titles
- heading hierarchy should stay unified across the whole thesis
- recommended hierarchy: chapter, section, clause, item, sub-item
- spacing before and after section and clause headings: 0.5 line

### References in text
- use a unified citation style throughout
- use superscript reference markers at the end of the cited content when appropriate
- reference numbers appear in square brackets, such as [1]
- do not place citation markers in titles

### Formulas
- write formulas on a separate centered line
- place formula number flush right in parentheses
- number by chapter, for example (1.1)
- appendix formulas use appendix prefix, for example (A1)
- when a formula wraps, break at =, +, -, ×, or ÷ and do not place the operator at the start of the new line

### Tables
- every table needs a table number and title above the table, centered
- numbering by chapter, such as table 2.1
- table title format: bold heiti, size 5; digits and letters in bold times new roman, size 5
- do not use left and right outer borders
- do not split the table header from the table across pages
- use “－” for empty numeric cells rather than ditto-style marks
- table notes go below the table in songti, size small 5

### Figures
- every figure needs a figure number and title below the figure
- numbering by chapter, such as figure 3.1
- figure title uses songti, size 5
- explanatory notes go above the figure title in songti, size small 5
- figures and figure titles must stay on the same page
- if the remaining space is insufficient, move the whole figure block to the next page
- coordinate charts must state axis names and units

### References list
- follow gb/t 7714-2015
- heading “参考文献” centered
- entries numbered with square brackets in order of first appearance
- every entry ends with a full stop
- preserve the correct type markers such as [J], [M], [C], [D], [R], [S], [P], [N], [EB/OL]

### Appendix
- appendices use labels such as appendix a, appendix b, appendix c
- appendix figures, tables, and formulas use appendix-prefixed numbering, such as figure A1, table B2, formula (B3)

## Type-specific minimum requirements

When the user asks whether the thesis is long enough or sufficiently sourced, apply these checks:

- engineering design: at least 15000 chinese characters; at least 10 references; at least 2 foreign-language references
- theoretical research: at least 20000 chinese characters; at least 15 references; at least 4 foreign-language references
- experimental research: at least 15000 chinese characters; at least 10 references; at least 2 foreign-language references
- software development: at least 10000 chinese characters; at least 10 references; at least 2 foreign-language references
- comprehensive type: at least 10000 chinese characters; at least 10 references; at least 2 foreign-language references
- economics/management/humanities: at least 18000 chinese characters; at least 15 references; at least 2 foreign-language references
- law: at least 8000 chinese characters; at least 15 references; at least 2 foreign-language references
- art/design: at least 8000 chinese characters; at least 8 references; at least 2 foreign-language references

## Foreign literature translation requirement

When the user asks about the translation appendix, apply this default rule:
- translate at least 20000 printed foreign-language characters or at least 5000 chinese characters
- art/design majors may use the lower range in the handbook
- the translated material should be closely related to the thesis topic

## How to handle user requests

### When the user uploads a draft
- identify existing sections
- compare them to the required order and formatting rules
- give the shortest path to compliance
- when editing text directly, preserve meaning and citations

### When the user asks for “帮我调格式”
Return in this order:
1. non-compliant items
2. exact formatting settings to change
3. corrected sample block for one heading, one paragraph, one figure caption, one table caption, and one reference entry if useful

### When the user asks for a template
Generate placeholders for:
- cover fields
- chinese abstract and keywords
- english abstract and keywords
- toc
- introduction
- chapter headings
- conclusion
- references
- acknowledgements
- appendices

### When the user asks for a final pre-submission check
Verify at minimum:
- page margins and line spacing
- page numbering start position
- heading hierarchy consistency
- abstract completeness and keyword count
- figure/table/formula numbering
- reference format and count
- appendix numbering
- binding order completeness

## Reference file

Load `references/gdut-handbook-checklist.md` when you need the concise rule table and submission checklist.
