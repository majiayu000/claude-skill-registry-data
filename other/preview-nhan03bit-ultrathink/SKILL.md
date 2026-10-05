---
name: preview
description: Render, summarize, and present markdown documents and structured content in multiple output modes
layer: hub
category: workflow
triggers:
  - "/preview"
  - "preview this"
  - "show me the doc"
  - "render this markdown"
  - "summarize this document"
  - "present this"
inputs:
  - source: File path, URL, or inline content to preview
  - mode: full | summary | outline | diff | presentation (optional, defaults to full)
  - audience: Who the preview is for -- technical, executive, user (optional)
outputs:
  - renderedContent: The document presented in the requested mode
  - metadata: Document stats (word count, sections, reading time)
  - suggestions: Improvement recommendations for the document (optional)
linksTo:
  - research
  - scout
linkedFrom:
  - cook
  - team
  - ship
  - plan
  - plan-archive
preferredNextSkills:
  - code-review
  - plan
fallbackSkills:
  - research
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: selective
sideEffects:
  - Reads files
  - Does NOT modify any files
---

# Preview Skill

## Purpose

Render, summarize, and present documents and structured content in formats optimized for different audiences and purposes. This skill transforms raw documents into consumable presentations without altering the source material.

Preview is the read-only presentation layer. It helps people understand documents quickly, verify content before publishing, and adapt material for different audiences.

## Workflow

### Mode 1: Full Preview

Renders the complete document with enhanced formatting and metadata.

1. **Read the source** -- Load the file, URL content, or inline text.
2. **Analyze the structure**:
   - Count sections, subsections, paragraphs
   - Identify document type (technical doc, plan, report, tutorial, etc.)
   - Calculate reading time (avg 200 words/minute)
   - List all headings as a navigation aid
3. **Present the full content** with:
   - Table of contents (for documents with 3+ sections)
   - Section dividers for visual clarity
   - Code blocks properly identified by language
   - Tables properly aligned
   - Links validated (exist or broken)
4. **Append metadata footer**:
   ```
   ---
   Words: [count] | Sections: [count] | Reading time: [N] min
   Last modified: [date if available]
   ```

### Mode 2: Summary

Produces a concise summary of the document, preserving key information.

1. **Read the full document**.
2. **Identify the document's purpose** -- What is the main point?
3. **Extract key points** -- One bullet per major section.
4. **Produce a summary** with:
   - **One-line TL;DR**: The document's essence in a single sentence
   - **Key points**: 3-7 bullet points covering the main content
   - **Action items**: Any tasks, decisions, or follow-ups mentioned
   - **Notable details**: Important specifics (numbers, dates, names) that should not be lost
5. **Tailor to audience**:
   - **Technical**: Preserve technical details, code references, architecture decisions
   - **Executive**: Focus on outcomes, timelines, risks, decisions needed
   - **User**: Focus on what changed, what they need to do, what they need to know

### Mode 3: Outline

Produces a hierarchical outline of the document's structure.

1. **Read the full document**.
2. **Extract the heading hierarchy**.
3. **For each section, add a one-line summary** of its content.
4. **Present as an indented outline**:
   ```markdown
   # Document Title
   ## Section 1 — [brief summary]
     ### Subsection 1.1 — [brief summary]
     ### Subsection 1.2 — [brief summary]
   ## Section 2 — [brief summary]
   ...
   ```
5. **Flag structural issues** (if any):
   - Orphan subsections (subsection without a parent section)
   - Inconsistent heading levels (jumping from H1 to H3)
   - Overly long sections that should be split
   - Duplicate section names

### Mode 4: Diff Preview

Compares two versions of a document and highlights changes.

1. **Read both versions** (old and new, or current and proposed).
2. **Identify changes**:
   - Added sections/paragraphs
   - Removed sections/paragraphs
   - Modified content
   - Structural changes (reordering, nesting changes)
3. **Present the diff** with:
   - Summary of changes (N additions, M removals, P modifications)
   - Section-by-section comparison
   - Highlighted additions and removals
4. **Assess the change significance**:
   - Minor: Typos, formatting, small clarifications
   - Moderate: New sections, significant rewording
   - Major: Structural changes, meaning changes, scope changes

### Mode 5: Presentation

Transforms a document into a presentation-friendly format (slide-like sections).

1. **Read the full document**.
2. **Break into presentation sections** (one "slide" per major point):
   - Each section gets a title and 3-5 bullet points MAX
   - Strip lengthy explanations -- keep only key messages
   - Preserve important visuals (tables, diagrams references)
3. **Add speaker notes** -- The detail that was stripped from the slides, presented as notes.
4. **Structure**:
   ```markdown
   ## Slide 1: [Title]
   - Point 1
   - Point 2
   - Point 3

   > Speaker notes: [expanded detail]

   ---

   ## Slide 2: [Title]
   ...
   ```

## Usage

### Full preview of a file
```
/preview docs/architecture.md
```

### Summary for executive audience
```
/preview summary docs/migration-plan.md --audience executive
```

### Document outline
```
/preview outline docs/api-reference.md
```

### Compare two versions
```
/preview diff docs/spec-v1.md docs/spec-v2.md
```

### Presentation mode
```
/preview presentation docs/quarterly-review.md
```

### Preview inline content
```
/preview
# My Document
Here is some content I want to preview...
```

## Examples

### Example: Summary of a technical plan

**Input**: 2000-word migration plan document
**Mode**: summary, audience: technical

**Output**:
```markdown
## TL;DR
Migrate from REST to tRPC over 3 phases, maintaining backwards compatibility throughout.

## Key Points
- Phase 1 (Week 1-2): Set up tRPC alongside existing REST endpoints
- Phase 2 (Week 3-4): Migrate client components one by one, starting with non-critical paths
- Phase 3 (Week 5): Remove REST endpoints after all clients are migrated
- Rollback: Each phase can be reverted independently via feature flags

## Action Items
- [ ] Review tRPC schema by Friday
- [ ] Set up feature flags for gradual rollout
- [ ] Update API documentation

## Notable Details
- Estimated 30% reduction in API boilerplate
- Breaking change in User response shape (Phase 2)
- Requires Node 18+ (currently on 16 -- upgrade first)
```

### Example: Document outline with issues

**Input**: Large API reference document
**Mode**: outline

**Output**:
```markdown
# API Reference
## Authentication — JWT-based auth with refresh tokens
  ### Token Format — Standard JWT with custom claims
  ### Endpoints — Login, register, refresh, logout
## Users — CRUD operations for user management
  #### Profile — (WARNING: H4 under H2, missing H3)
## Orders — Order lifecycle management
  ### Create — POST /orders with items array
  ### Update — PATCH /orders/:id (partial updates)
  ### (Missing: Delete/cancel endpoint documented elsewhere but not here)

## Structural Issues
- Line 45: H4 heading directly under H2 (skipped H3)
- Orders section: No DELETE endpoint documented
- No error response format section
```

## Guidelines

- **Read-only always** -- Preview never modifies source files.
- **Preserve fidelity** -- In full mode, represent the document accurately. Do not editorialize.
- **Adapt to audience** -- The same document needs different emphasis for developers vs. executives.
- **Flag issues gently** -- If the document has structural problems, note them as suggestions, not errors.
- **Keep summaries honest** -- Do not add information that is not in the source. If something is unclear, say so.
- **Reading time matters** -- Always include it. It helps people decide when to read the full document vs. the summary.
- **Prefer structure over prose** -- Bullets, tables, and headings are easier to scan than paragraphs.
- **Support iterative review** -- Preview is often the first step before editing. Make it easy to identify what needs work.
