---
description: Read, criticize, and propose improvements for a table of content of a book
model: opus
---

# Goal
- Review and criticize the table of content of a book's chapter (or chapters)
- Identify mistakes and improvement opportunities, focusing on factual errors
  over style suggestions
- Propose concrete, ranked improvements to topics, ordering, scope, and audience
  fit

# Workflow

## Read the Material
- Read `.claude/templates/book_map.template.md` for the expected TOC structure

- Read `book_map.md`, which stores the `### Topics` of the book's TOC
  - Read `**Title**` and `**Target audience**` at the top of `book_map.md`
  - Read the `# Part` heading description the chapter belongs to
  - Read the target chapter's `### Topics` that the user refers to
  - Ignore all other sections
    - I.e., `### Lessons`, `### Tutorials`, `### Related packages`,
      `### Related books`, `### Related papers`
  - Read the `### Topics` of sibling chapters in that Part and the immediate
    neighbors, chapter N-1 and N+1, to judge continuity

## Criticize
- Read `.claude/skills/text.criticize/SKILL.md` for general review approaches

- Evaluate these axes, reporting only high-confidence issues:
  - **Internal flow**:
    - Order of the `### Topics` bullets
    - Prerequisite ordering
    - Redundant or overlapping bullets
    - A bullet that is really two topics
  - **Cross-chapter flow**:
    - Overlap with neighbors or others in the same Part
    - A topic that belongs earlier or later
    - Forward references to concepts not yet introduced
  - **Part fit**:
    - Does the chapter match the scope description of its `# Part` (foundations
      vs. advanced theory vs. deployment)
    - Flag misplaced chapters
  - **Structure conformance**:
    - Compare the structure to `.claude/templates/book_map.template.md`
    - Report:
      - Parts that don't follow the subsections
      - Lessons without a FULL/PART/WEAK tag
      - References not following `.claude/skills/references.rules.md`
  - **Audience fit**:
    - Matches the stated audience
    - Level too high or low
    - Assumed background
    - Unexplained jargon
  - **Scope and balance**:
    - Too much or too little content for one chapter
    - Candidates to split or merge

- Rank each issue by severity:
  - **CRITICAL**: breaks the chapter's logic or misplaces it
  - **HIGH**: misleads or confuses the reader
  - **MEDIUM**: hurts clarity or completeness
  - **LOW**: minor polish

## Write Result
- Write results using the same format and file as in
  `## Step 4: Write the Results` in `.claude/skills/text.criticize/SKILL.md`

## Wait for Approval
- Present the criticism to the user
- Wait for the user to select items by index and give corrections
- Only then edit `book_map.md`, updating every section it affects (Topics,
  Lessons, Tutorials, Related packages, Related books, Related papers)

# Verification
- [ ] Confirm each reported issue cites the exact `### Topics` bullet or
      chapter it refers to
- [ ] Confirm no edit to `book_map.md` was made before the user approved it
- [ ] Confirm applied corrections update every affected section (Topics,
      Lessons, Tutorials, Related packages, Related books, Related papers)
