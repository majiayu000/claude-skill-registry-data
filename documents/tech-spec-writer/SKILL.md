---
name: tech-spec-writer
description: Create comprehensive technical specification documents through interactive Q&A. Use when (1) user asks to write a Tech Spec, (2) user wants to plan a new feature, (3) user needs to create technical documentation for a feature, (4) user mentions "tech spec", "technical specification", or "feature planning document".
---

# Tech Spec Writer

Create structured technical specification documents through an interactive workflow that gathers context before generating the complete document.

## Workflow

### Phase 1: Context Gathering

Ask questions in stages to avoid overwhelming. Start with core questions, then dive deeper based on answers.

**Stage 1 - Core Context:**
1. What is the feature/project name?
2. What problem does this solve? (1-2 sentences)
3. What is the main goal? (measurable outcome)

**Stage 2 - Solution Details:**
4. What is your proposed solution? (high-level approach)
5. What systems/components will be affected?
6. Are there any architectural changes? (new services, APIs, database changes)

**Stage 3 - Technical Specifics:**
7. Schema changes needed? (new tables, fields)
8. API changes? (new/modified endpoints)
9. UI changes? (if applicable)

**Stage 4 - Risks & Planning:**
10. Known risks or technical challenges?
11. Implementation phases or milestones?
12. Key metrics to measure success?

Adapt questions based on previous answers. Skip irrelevant sections.

### Phase 2: Document Generation

After gathering context, generate the complete Tech Spec using the template in [references/template.md](references/template.md).

For section-specific writing guidelines, see [references/section-guide.md](references/section-guide.md).

### Phase 3: Output Formatting

Provide two output formats:

**Option A: Markdown** (default)
- Clean markdown suitable for GitHub, Notion, or general use

**Option B: Confluence**
- Use Confluence wiki markup format
- See [references/confluence-format.md](references/confluence-format.md) for conversion rules
- Ready to paste into Confluence editor (switch to wiki markup mode)

Ask user which format they prefer, or provide both.

## Quick Reference: Template Sections

| Section | Required | Description |
|---------|----------|-------------|
| Metadata | Yes | Start Date, Owner, Version, Change Log |
| Problem Statement | Yes | What problem this solves |
| Goal | Yes | Measurable objectives |
| Proposed Solution | Yes | High-level approach |
| Changes | Yes | Summary of all changes |
| Architectural Diagrams | If applicable | System architecture changes |
| Schema Specification | If applicable | Database changes |
| API Specification | If applicable | Endpoint changes |
| UI Flow Diagrams | If applicable | User interface changes |
| Risk | Yes | Potential challenges and mitigations |
| Security & Privacy | Optional | Security considerations |
| Alternative Solutions | Recommended | Other approaches considered |
| Implementation Plan | Yes | Phases and timeline |
| Metrics | Yes | Success measurement |
| Software Quality Attributes | Optional | Non-functional requirements |
| Follow Up | Yes | Action items |

## Resources

- **Template**: [references/template.md](references/template.md) - Complete Tech Spec template
- **Writing Guide**: [references/section-guide.md](references/section-guide.md) - How to write each section
- **Confluence Format**: [references/confluence-format.md](references/confluence-format.md) - Wiki markup conversion
