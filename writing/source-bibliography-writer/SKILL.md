---
name: source-bibliography-writer
description: "Produces a correctly formatted bibliography or source list from details you provide, supporting AP, Chicago (Notes-Bibliography), and APA citation styles."
status: stable
category: archive-legal
subcategory: publishing
version: 1.0
eval_score: 4.2
tags: [bibliography, citations, sourcing, fact-checking, AP-style, Chicago-style, APA-style]
---
# Source Bibliography Writer

## What This Skill Does
Produces a correctly formatted bibliography or source list from details you provide, supporting AP, Chicago (Notes-Bibliography), and APA citation styles.

## When To Use This Skill
- You are submitting an article, documentary treatment, or investigative piece that requires a formal source list for an editor or fact-checker
- Your commissioning editor or broadcaster requires documented sourcing before publication or broadcast
- You are preparing a grant application or press kit and need to show evidence base in a standard academic or journalistic format
- You have gathered sources across multiple types — interviews, government documents, academic papers, websites, books — and need them unified into one consistent list

## What You Need To Provide
**Required:**
- The citation style you need: AP, Chicago (Notes-Bibliography), or APA
- For each source, as much of the following as you have: author name(s), publication or organisation name, title of the work or article, date of publication or access, URL (for online sources), page numbers (for print), volume and issue numbers (for journals)

**Optional:**
- Whether you want the list alphabetised, numbered, or grouped by source type (e.g., interviews separate from documents)
- Whether you want a brief annotation after each entry explaining what the source contributed to your reporting (annotated bibliography)
- The publication or production this bibliography is for — the assistant will adjust the level of formality accordingly

## How the Assistant Approaches This
1. Reads each source you have provided and identifies its type — book, journal article, newspaper article, government document, interview, website, broadcast, or unpublished material — because citation format varies by type within each style guide.
2. Applies the requested style guide rules consistently across all entries: author formatting, title capitalisation, punctuation, date placement, and URL conventions each differ between AP, Chicago, and APA.
3. Delivers the complete list in the requested order, flagging any entries where information is missing that would be required for a complete citation, so you know exactly what to look up before submission.

## Output Format
A clean list of citations, one per source. Format follows the requested style guide precisely. Entries separated by a blank line for readability. Any entry with missing required information is marked with a note in square brackets immediately after the entry (e.g., `[Publisher name not provided — required for Chicago]`). If an annotated bibliography is requested, the annotation appears as an indented sentence below each entry. No introductory prose — the list starts immediately.

## Quality Criteria
- [ ] Every entry follows the selected style guide's rules for that specific source type (book, article, interview, website, etc.)
- [ ] Author names are formatted correctly for the chosen style (AP: first name first; Chicago and APA: surname first for bibliography entries)
- [ ] Titles are capitalised correctly (AP: headline case for most titles; Chicago: headline case for titles, sentence case for subtitles; APA: sentence case for article and book titles)
- [ ] Missing required fields are explicitly flagged rather than silently omitted
- [ ] The list is consistent — no mixing of formatting conventions within a single style

## Example

### Input
Style: Chicago (Notes-Bibliography)
Alphabetise by author surname.
Annotated? No.

Sources:
1. Book — author: Ranjit Mehrotra, title: "The Invisible Archive: How Governments Bury Public Records", publisher: Meridian Press, year: 2019, city: London
2. Journal article — author: Clara Osei-Bonsu, journal: Journal of Investigative Journalism, article title: "Audit culture and the freedom of information request", year: 2021, volume: 14, issue: 2, pages: 88–103
3. Interview — interviewee: Deputy Director of the Regional Housing Authority (name withheld by request), conducted by the reporter, date: 14 November 2025, format: in-person
4. Government document — organisation: Ministry of Housing and Infrastructure, title: "Annual Asset Register 2024", date: March 2024, URL: https://housing.gov.example/asset-register-2024.pdf, accessed: 10 January 2026
5. Newspaper article — author: Sylvie Krantz, title: "Officials deny knowledge of demolition orders", newspaper: The Metropolitan Courier, date: 3 September 2023, URL: https://metrocourier.example/2023/09/03/officials-deny

### Output
Krantz, Sylvie. "Officials Deny Knowledge of Demolition Orders." *The Metropolitan Courier*, September 3, 2023. https://metrocourier.example/2023/09/03/officials-deny.

Mehrotra, Ranjit. *The Invisible Archive: How Governments Bury Public Records*. London: Meridian Press, 2019.

Ministry of Housing and Infrastructure. "Annual Asset Register 2024." March 2024. Accessed January 10, 2026. https://housing.gov.example/asset-register-2024.pdf.

Osei-Bonsu, Clara. "Audit Culture and the Freedom of Information Request." *Journal of Investigative Journalism* 14, no. 2 (2021): 88–103.

Regional Housing Authority, Deputy Director (name withheld). Interview by reporter. In person, November 14, 2025. [Note: Chicago style typically requires the interviewee's name; confirm with editor whether anonymisation convention is acceptable in this context.]

## Known Limitations
- The assistant applies style guide rules as of its training data. Style guides are periodically updated — for submissions to academic journals or grant bodies with strict requirements, verify against the current edition of the relevant guide.
- This skill relies entirely on the details you provide. If you supply an incorrect date, a misspelled author name, or the wrong page range, the citation will reproduce that error. The assistant cannot verify source details against external databases.
- AP style does not have a formal bibliography format in the way Chicago and APA do — AP is primarily an in-text citation system. When AP is selected, the assistant produces a source list modelled on AP wire-service conventions, which may need adaptation for specific editors.
- Very unusual source types — ancient manuscripts, unpublished theses, personal correspondence, oral history recordings — may require manual review against the full style guide rather than relying on this skill alone.

## Related Skills
- [fact-check-prompt](../../magazine-journalism/editing/fact-check-prompt/SKILL.md)
- [document-analysis-brief](../../magazine-journalism/investigation/document-analysis-summary/SKILL.md)
