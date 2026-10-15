---
name: doc-consolidator
description: >-
  Consolidate multiple related documents (markdown, technical references, guides, policies) into one unified reference, keeping all unique content and removing redundancy. Triggers: "consolidate these docs", "merge these files into one", "combine these references", "unified documentation".
---

# Document Consolidator

Merge multiple related documents into a single, well-organized reference while preserving all unique content and eliminating redundancy.

## Workflow

1. **Inventory** — List all input documents with paths
2. **Analyze** — Read each document completely, noting structure and topics
3. **Map** — Identify overlapping sections and unique content per document
4. **Outline** — Create merged structure before writing
5. **Consolidate** — Write unified document following the outline
6. **Deliver** — Save to outputs directory and present to user

## Analysis Phase

Read each document and create a mental map:

```
Document A:
- Section 1: [topic] — unique/overlaps with Doc B Section X
- Section 2: [topic] — unique
- Section 3: [topic] — overlaps with Doc B Section Y (Doc A more complete)

Document B:
- Section X: [topic] — overlaps with Doc A Section 1 (Doc B more complete)
- Section Y: [topic] — overlaps with Doc A Section 3
- Section Z: [topic] — unique
```

## Merge Rules

**Overlapping content:**
- Keep the most complete/accurate version
- If both add value, synthesize into single comprehensive section
- Preserve all technical details, code examples, tables

**Unique content:**
- Include everything — do not discard unless exact duplicate
- Maintain original technical accuracy (no paraphrasing specs/code)

**Conflicts:**
- If documents contradict, note both perspectives or keep most recent
- For technical specs, prefer the more detailed version

## Output Structure

Standard document flow:

```
1. Title (indicate consolidated nature)
2. Table of Contents (if >500 lines)
3. Executive Summary / Overview
4. Core Concepts / Architecture
5. Implementation / How-To Sections
6. Reference Tables / Quick References
7. Troubleshooting / Common Issues
8. Sources / References
```

Adapt structure to document type — technical references differ from policy documents.

## Formatting Standards

- Consistent heading levels (H1 title, H2 major sections, H3 subsections)
- Uniform code block language tags
- Standardized table formatting
- Consistent list styles (bullets vs numbers)
- Preserve all original code examples verbatim

## Constraints

- **Do NOT** summarize or condense technical details
- **Do NOT** add information not in source documents
- **Do NOT** remove content unless exact duplication
- **Do NOT** paraphrase code, configurations, or specifications
- **Preserve** all tables, diagrams-as-text, structured data

## Output Location

Save consolidated document to `/mnt/user-data/outputs/` with descriptive filename indicating consolidated nature (e.g., `Topic_Consolidated_Reference.md`).

## Quality Checklist

Before delivering:
- [ ] All source documents fully read
- [ ] No unique content lost
- [ ] Overlapping content merged (not duplicated)
- [ ] Logical section ordering
- [ ] Consistent formatting throughout
- [ ] Table of contents if >500 lines
- [ ] File saved to outputs directory
