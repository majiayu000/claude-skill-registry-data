---
name: technical-writer
description: Professional technical writing expertise for clear, audience-appropriate documentation. Use when producing user-facing docs, API guides, onboarding.
---

# Technical Writer

Apply the principles and practices of professional technical writing to produce documentation that is clear, accurate, accessible, and maintainable. This skill covers the full lifecycle of documentation, from audience research through publishing and maintenance.

## When to Use This Skill

Use this skill when you need to:

- Write user-facing documentation (installation guides, tutorials, how-tos, reference pages)
- Produce API guides, SDK quickstarts, or developer onboarding materials
- Draft release notes, changelogs, or migration guides
- Create internal knowledge base articles or runbooks
- Establish a style guide or terminology glossary for a project
- Review existing documentation for quality, accuracy, and readability
- Plan information architecture for a documentation site

**Trigger phrases**: "write documentation", "user guide", "API guide", "release notes", "style guide", "docs review", "onboarding material", "technical writing"

## What This Skill Does NOT Cover

This skill focuses on the craft of writing and the documentation lifecycle. For architecture-specific artifacts (ADRs, design documents, system architecture overviews), use the `technical-documentation` skill instead.

## Instructions

### Step 1: Audience Analysis and Content Strategy

Before writing a single word, identify who will read the document and what they need to accomplish.

#### Reader Persona Identification

Define at least one reader persona for every document. A persona captures:

- **Role**: Developer, operator, end user, manager, or mixed audience
- **Knowledge level**: Beginner (needs every concept explained), intermediate (understands fundamentals, needs specifics), expert (needs reference-only, skip basics)
- **Goal**: What the reader is trying to accomplish after reading
- **Context**: Where and when they will read (during an incident, while onboarding, at a desk, on mobile)

#### Knowledge Level Assessment

Map each topic in your document to one of three tiers:

| Tier | Reader knows | Document provides |
|------|-------------|-------------------|
| Prerequisite | Nothing about the topic | Conceptual introduction, glossary links, and "before you begin" checklist |
| Working | Core concepts but not your system | Task-oriented instructions with brief context |
| Expert | Your system well | Reference tables, configuration options, edge cases |

Write for the lowest tier in your audience unless the document is explicitly scoped to a higher tier (for example, an "Advanced Configuration" page).

#### Task-Oriented vs Concept-Oriented Content

Separate task content ("how to do X") from concept content ("what X is and why it matters"). Mixing the two forces readers to scan past theory when they need steps, or past steps when they need understanding.

- **Task content**: Numbered steps, prerequisites, expected outcomes, troubleshooting
- **Concept content**: Definitions, architecture explanations, design rationale, comparisons

#### Information Architecture Planning

Before drafting, create a content map that answers:

1. What documents exist today, and what gaps remain?
2. What is the logical reading order for a new user?
3. Which documents are standalone and which require prerequisites?
4. How will readers discover content (search, sidebar navigation, in-product links)?

Use the Document Planning Template at the end of this skill to structure this analysis.

### Step 2: Document Structure and Navigation

Good structure makes documentation scannable, navigable, and maintainable.

#### Progressive Disclosure

Present information in layers of increasing detail:

1. **Title and summary**: One sentence that tells the reader whether this page answers their question
2. **Overview section**: A short paragraph (3-5 sentences) covering what, why, and who
3. **Prerequisites or "Before you begin"**: What the reader needs before starting
4. **Core content**: The main body, organized by task or concept
5. **Next steps**: Links to related pages, deeper dives, or the next logical action
6. **Reference appendix** (optional): Tables, configuration options, or exhaustive lists

#### Heading Hierarchy

Follow these rules for headings:

- Use exactly one H1 per page (the document title)
- Never skip heading levels (do not jump from H2 to H4)
- Make headings descriptive and scannable: prefer "Configure database connections" over "Configuration"
- Keep headings under 8 words when possible
- Use sentence case for headings, not title case (unless a project style guide mandates otherwise)

#### Table of Contents Design

For documents longer than three screen-heights, include a table of contents (TOC). If your publishing system generates one automatically, ensure it includes H2 and H3 levels only. Deeper headings in the TOC create noise.

#### Cross-Referencing

- Link to prerequisite concepts on first mention, not on every mention
- Use descriptive link text: "see the authentication guide" rather than "click here"
- Prefer relative links within a documentation set so they survive domain changes
- Maintain a cross-reference inventory for large doc sets to detect broken links during updates

#### Modular Content Architecture

Design documents as independent modules that can be:

- Read in isolation (each page has enough context to stand alone)
- Composed into learning paths (a sequence of modules for onboarding)
- Reused across contexts (a "prerequisites" module shared by multiple guides)

Avoid duplicating content across pages. Instead, link to a single source of truth and summarize only when the reader needs a brief reminder.

### Step 3: Writing Style and Voice

Consistent style builds reader trust and reduces cognitive load.

#### Active Voice

Write in active voice. Active voice clarifies who performs the action and produces shorter sentences.

| Passive (avoid) | Active (prefer) |
|-----------------|-----------------|
| The configuration file is loaded by the server | The server loads the configuration file |
| Errors are returned when validation fails | The API returns errors when validation fails |
| The button should be clicked | Click the button |

Use imperative mood for instructions: "Run the install script" rather than "You should run the install script".

#### Concise Sentences

- Target 15-25 words per sentence for instructional content
- One idea per sentence; split compound sentences with "and" into two sentences when the ideas are independent
- Cut filler words: "In order to" becomes "To"; "It is important to note that" becomes nothing (just state the fact)
- Replace noun phrases with verbs: "perform an analysis of" becomes "analyze"

#### Consistent Terminology

- Choose one term for each concept and use it everywhere (do not alternate between "repo", "repository", and "codebase" for the same thing)
- Define project-specific terms in a glossary
- Capitalize product names consistently; do not capitalize generic concepts

#### Glossary Management

Maintain a glossary file alongside your documentation. Each entry includes:

- **Term**: The canonical name
- **Definition**: One to two sentences
- **Synonyms**: Other names readers might search for
- **See also**: Related terms

Update the glossary whenever you introduce a new term.

#### Style Guide Creation

For any documentation set with more than one author, create a project style guide. Use the Style Guide Template at the end of this skill as a starting point.

#### Readability Scoring

Measure readability using the Flesch-Kincaid Grade Level or the Hemingway readability score. Targets:

- Developer documentation: Grade 8-10 (accessible to non-native English speakers)
- End-user documentation: Grade 6-8
- Executive summaries: Grade 6-8

Test readability on a sample of paragraphs, not just the full document average.

### Step 4: Code Documentation

Code-adjacent documentation has its own conventions.

#### API Reference Structure

Every API endpoint or public function reference should include:

1. **Endpoint or signature**: The method, path, or function name
2. **Description**: One sentence explaining what it does
3. **Parameters**: Name, type, required/optional, default value, description
4. **Request body** (for APIs): Schema or example with field descriptions
5. **Response**: Schema or example, including error responses
6. **Code example**: A minimal working example in the primary SDK language
7. **Rate limits and quotas** (if applicable)
8. **Changelog**: When the endpoint was added, modified, or deprecated

#### Code Examples Best Practices

- Every code example must be complete enough to copy, paste, and run (or clearly indicate which parts are pseudocode)
- Include the language identifier in fenced code blocks for syntax highlighting
- Show expected output alongside the code when the output is not obvious
- Use realistic variable names: prefer `user_email` over `x` or `foo`
- Keep examples minimal; demonstrate one concept per example
- Test all code examples as part of your documentation CI pipeline

#### Input/Output Documentation

For functions and CLI tools, document:

- **Input constraints**: Accepted types, value ranges, required formats, maximum sizes
- **Output shape**: Return type, possible values, structure
- **Side effects**: Files created, network calls made, state changes
- **Error conditions**: What triggers errors and what the error messages look like

#### Error Code Catalogs

For systems that return error codes, maintain a catalog with:

| Code | Name | Description | Common Cause | Resolution |
|------|------|-------------|-------------|------------|
| 1001 | AUTH_EXPIRED | Authentication token has expired | Token not refreshed before TTL | Re-authenticate using the login endpoint |
| 1002 | RATE_LIMITED | Request rate exceeded | Too many requests in the window | Wait for the reset time indicated in the Retry-After header |

#### Versioned Documentation

When your API or product has multiple live versions:

- Maintain separate doc versions for each supported release
- Clearly display the version selector on every page
- Mark deprecated features with a visible banner and a removal timeline
- Include migration guides between consecutive versions

### Step 5: Visual Communication

Visuals reduce reading time for complex relationships, flows, and comparisons.

#### Diagram Selection Guide

| Information type | Best visual format |
|------------------|--------------------|
| System components and their relationships | Architecture diagram (boxes and arrows) |
| Sequential process or workflow | Flowchart or sequence diagram |
| Decision logic | Decision tree or flowchart with branches |
| Data relationships | Entity-relationship diagram |
| Timeline or phases | Gantt chart or timeline graphic |
| Comparison of options | Table |
| Hierarchical structure | Tree diagram |
| Quantitative data | Bar chart, line chart, or pie chart |

#### Screenshot Annotation

When using screenshots:

- Crop to show only the relevant area
- Add numbered callouts for each element you reference in the text
- Include alt text for accessibility
- Update screenshots when the UI changes (flag them in your freshness audit)

#### Flowchart Design

- Use consistent shapes: rectangles for steps, diamonds for decisions, rounded rectangles for start/end
- Limit each flowchart to 10-15 nodes; break larger flows into sub-diagrams
- Label every arrow with the condition or transition
- Read top-to-bottom or left-to-right; avoid crossing lines

#### Table Formatting

- Use tables for structured comparisons, configuration options, or parameter lists
- Include a header row with descriptive column names
- Left-align text columns; right-align numeric columns
- Keep cell content concise (no multi-paragraph cells)
- Add a caption or introductory sentence before each table

#### When to Use Visuals vs Text

Use a visual when:

- The content describes spatial relationships, flows, or hierarchies
- A table would replace three or more paragraphs of comparison text
- The reader needs to see what a UI looks like

Use text when:

- The content is a simple instruction or definition
- The information changes frequently (text is cheaper to update than diagrams)
- The reader may be using a screen reader (always provide text alternatives for visuals)

### Step 6: Review and Quality Assurance

Documentation requires the same rigor as code review.

#### Technical Review Checklist

A subject-matter expert should verify:

- [ ] All technical facts are accurate (commands, endpoints, config values)
- [ ] Code examples execute without errors
- [ ] Prerequisites are complete and in the correct order
- [ ] Edge cases and limitations are documented
- [ ] Version numbers and compatibility statements are correct
- [ ] Security warnings are present where needed
- [ ] Error messages and troubleshooting steps are current

#### Editorial Review Checklist

A peer or editor should verify:

- [ ] The document follows the project style guide
- [ ] Headings are descriptive and correctly nested
- [ ] Spelling and grammar are correct
- [ ] Terminology is consistent throughout
- [ ] Links are valid and use descriptive text
- [ ] Alt text is present on all images
- [ ] The document is scannable (short paragraphs, bullet lists, tables)
- [ ] The introduction sets clear expectations for what the reader will learn
- [ ] Next steps or related links are provided at the end

#### Freshness Audits

Schedule periodic reviews to catch drift between documentation and the product:

- **Quarterly**: Review all "getting started" and onboarding content
- **Each release**: Review all pages that reference changed features
- **Annually**: Audit the full documentation set for orphaned pages, broken links, and outdated screenshots

#### Link Checking

Automate link checking in CI. Tools such as `markdown-link-check`, `htmltest`, or `linkinator` catch broken internal and external links before they reach readers.

#### Accessibility Compliance

Ensure documentation meets WCAG 2.1 AA guidelines:

- All images have descriptive alt text
- Color is not the only means of conveying information
- Tables have header rows and are not used for layout
- Headings form a logical outline for screen readers
- Interactive elements are keyboard-navigable

#### Readability Metrics

Track readability over time. After each major revision:

1. Run a readability analysis on the revised pages
2. Compare the score to the target range for that document type
3. Flag pages that have drifted above the target grade level

### Step 7: Publishing and Maintenance

Documentation is a living product, not a one-time deliverable.

#### Docs-as-Code Workflow

Treat documentation like source code:

- Store docs in the same repository as the code they describe (or in a dedicated docs repo)
- Use pull requests for all doc changes, with mandatory review
- Run linters (markdownlint, vale) and link checkers in CI
- Preview builds for every PR so reviewers see the rendered output

#### Version-Controlled Documentation

- Tag doc versions alongside code releases
- Use branches or directories to maintain docs for multiple supported versions
- Never silently update published docs without a changelog entry

#### Automated Publishing

Set up a CI/CD pipeline for documentation:

1. Lint Markdown or source files
2. Check links
3. Build the static site (using tools like MkDocs, Docusaurus, Hugo, or Sphinx)
4. Deploy to staging for review
5. Promote to production on merge to the main branch

#### Changelog Writing

For each release, write a changelog entry using these categories: **Added**, **Changed**, **Deprecated**, **Removed**, **Fixed**, **Security**. Write entries for the reader, not the developer. "Users can now export reports as PDF" is better than "Added PDF export handler in reports module".

#### Deprecation Notices

When deprecating a feature or API:

- Add a visible deprecation banner to the relevant documentation page
- State the deprecation date and the planned removal date
- Provide a migration path or alternative
- Link to the migration guide

#### Content Lifecycle

Every document moves through these stages: **Draft** (in progress), **Published** (live and current), **Stale** (needs review), **Deprecated** (scheduled for removal), **Archived** (removed from navigation but accessible via direct link). Track lifecycle status in frontmatter or a content inventory spreadsheet.

---

## Templates

### Document Planning Template

```markdown
# Document Plan: [Document Title]

## Target Audience
- **Primary persona**: [Role, knowledge level, goal]
- **Secondary persona**: [Role, knowledge level, goal]

## Content Type
- [ ] Tutorial (learning-oriented, follows a path)
- [ ] How-to guide (task-oriented, solves a specific problem)
- [ ] Reference (information-oriented, describes the system)
- [ ] Explanation (understanding-oriented, provides context)

## Scope
- **In scope**: [What this document covers]
- **Out of scope**: [What it does NOT cover, with links to where those topics live]

## Prerequisites
- [What the reader must know or have installed before starting]

## Outline
1. [Section title and one-sentence summary]
2. [Section title and one-sentence summary]

## Review Plan
- **Technical reviewer**: [Name] | **Editorial reviewer**: [Name] | **Target date**: [Date]
```

### Style Guide Template

```markdown
# Documentation Style Guide

## Voice and Tone
- **Voice**: [e.g., Authoritative but approachable. Write as a knowledgeable colleague, not a textbook.]
- **Tone shifts**: [e.g., Neutral for reference pages. Encouraging for tutorials. Direct and calm for troubleshooting.]

## Language Rules
- Use active voice for instructions
- Use present tense ("The server returns an error") not future tense ("The server will return an error")
- Use second person ("you") for task-oriented content
- Avoid jargon unless the term is defined in the glossary
- Spell out acronyms on first use: "command-line interface (CLI)"

## Formatting Standards
- **Headings**: Sentence case, no trailing punctuation
- **Lists**: Use numbered lists for sequential steps, bullet lists for unordered items
- **Code**: Inline code for identifiers, fenced blocks for multi-line examples
- **File paths**: Inline code format (`/etc/config.yaml`)
- **UI elements**: Bold for button labels and menu items ("Click **Save**")
- **Keyboard shortcuts**: Kbd format where supported, otherwise inline code (`Ctrl+C`)

## Terminology
| Use | Do not use | Reason |
|-----|-----------|--------|
| [Canonical term] | [Rejected alternatives] | [Why] |

## Code Example Standards
- Include the language identifier on every fenced code block
- Use realistic variable names
- Show expected output when non-obvious
- Test every example before publishing

## Image and Diagram Standards
- Maximum width: 800px
- Include alt text on every image
- Use SVG or PNG for diagrams (no JPEG for line art)
- Store source files for diagrams alongside the image (e.g., `.drawio` next to the exported `.png`)
```

### Review Checklist Template

```markdown
# Documentation Review Checklist

## Document: [Title] | Reviewer: [Name] | Date: [Date]

### Accuracy
- [ ] Technical facts verified against the current product version
- [ ] Code examples tested and confirmed working
- [ ] Version numbers and compatibility ranges correct
- [ ] Links resolve to the intended destination

### Structure and Clarity
- [ ] Title clearly describes the document purpose
- [ ] Headings are descriptive and logically nested
- [ ] Active voice used; sentences average under 25 words
- [ ] Terminology consistent with the project glossary
- [ ] Prerequisites listed before the first step; next steps provided at the end

### Accessibility and Maintenance
- [ ] All images have alt text; tables have header rows
- [ ] Frontmatter includes last-reviewed date
- [ ] Deprecation notices present where applicable

### Verdict: [ ] Approved | [ ] Minor changes needed | [ ] Revisions required
```

---

## Quality Checklist

- [ ] Audience personas defined before drafting
- [ ] Document structure follows progressive disclosure
- [ ] Headings are descriptive and correctly nested
- [ ] Writing uses active voice and concise sentences
- [ ] Terminology is consistent; glossary is up to date
- [ ] Code examples are complete, tested, and realistic
- [ ] Visuals are appropriate and accessible
- [ ] Technical review completed by a subject-matter expert
- [ ] Editorial review completed for style and clarity
- [ ] Links checked and valid
- [ ] Publishing pipeline configured and tested
- [ ] Freshness audit schedule established

## Common Issues and Solutions

### Issue: Documentation falls out of date quickly
**Solution**: Embed doc updates into the definition of done for feature work. No feature ships without updated docs.

### Issue: Multiple authors produce inconsistent content
**Solution**: Create a style guide and enforce it through editorial review. Run a prose linter such as Vale in CI.

### Issue: Readers cannot find the information they need
**Solution**: Conduct card sorts or tree tests with real users to validate information architecture. Improve search, labels, and cross-references.

### Issue: Code examples do not work
**Solution**: Test code examples in CI. Treat broken examples as build failures.

### Issue: Documentation is inaccessible to non-native English speakers
**Solution**: Target Flesch-Kincaid Grade Level 8-10. Avoid idioms and unnecessarily complex vocabulary.

## Related Skills

- `technical-documentation` - Architecture docs, ADRs, and design documents
- `code-quality` - Code review and quality standards
- `project-management` - Planning and tracking documentation projects

---

**Version**: 1.0.0
**Last Updated**: March 2026

### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets are not met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
