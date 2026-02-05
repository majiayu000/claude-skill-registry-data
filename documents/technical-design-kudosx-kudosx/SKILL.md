---
name: technical-design
description: |
  Review and create technical design documents or technical blogs for the Moni Assistant project. Use this skill when:
  - Creating new technical design documents in docs/technical-design/
  - Creating technical blog posts in blog/
  - Reviewing existing technical designs or blogs for completeness and quality
  - Ensuring documents follow the project's documentation standards
  - Writing architecture overviews, system designs, or feature specifications
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Technical Design Skill

This skill helps create and review technical design documents and technical blogs following the Moni Assistant documentation standards.

## Document Types

| Type | Location | Purpose |
|------|----------|---------|
| **Technical Design Document** | `docs/technical-design/` | Formal specification for system implementation |
| **Technical Blog** | `blog/` | Share knowledge, architecture decisions, lessons learned |

---

# Part 1: Technical Design Document

## Document Structure

All technical design documents must follow this structure:

### 1. Title & Introduction
- Clear, descriptive title using `#` heading
- Problem statement explaining why this design is needed
- Core problems being solved (bullet points)

### 2. Requirements Section
```markdown
## 1. Requirements

### 1.1. Functional Requirements
* List of what the system must do

### 1.2. Non-Functional Requirements
* **Performance**: Latency, throughput requirements
* **Accuracy**: Quality metrics and targets
* **Scalability**: Resource optimization considerations
```

### 3. Architecture Overview
- High-level system diagram (use `<div style={{textAlign: 'center'}}>` for centering images)
- Description of main components and their responsibilities
- Data flow between components

### 4. Detailed Design
- Subsections for each major component or flow
- Sequence diagrams or flow charts where appropriate
- Data models and schemas (use code blocks)
- API designs if applicable

### 5. Related Resources
- Links to external documentation
- References to related internal docs

### 6. Appendix
- Glossary of terms used in the document
- Use table format for term definitions

## Language Guidelines

- Write in Vietnamese for consistency with existing docs
- Use technical English terms for concepts (e.g., "Memory Fragment", "Vector Database")
- Include English translations in parentheses where helpful

## Image References

Use this format for images:
```jsx
<div style={{textAlign: 'center'}}>
  <img src={require('@site/docs/img/technical-design/[folder]/[image].png').default} height="500" />
  <p style={{fontSize: 'small', fontStyle: 'italic', marginTop: '8px'}}>Caption here</p>
</div>
```

## Code Examples

- Use fenced code blocks with language specification
- Include realistic examples with comments
- For database schemas, show CREATE TABLE statements
- For data models, show Python/TypeScript type definitions

## Quality Checklist

When reviewing or creating technical designs, ensure:

- [ ] Problem statement is clear and well-defined
- [ ] Requirements are specific and measurable
- [ ] Architecture diagram is included
- [ ] All components are described with their responsibilities
- [ ] Data models/schemas are documented
- [ ] Error handling approach is mentioned (even if TBD)
- [ ] Related resources are linked
- [ ] Glossary includes all domain-specific terms

## File Location

Technical design documents go in: `docs/technical-design/[feature-name].md`

After creating a document:
1. Add entry to `technicalDesignSidebar.ts`
2. Update `CHANGELOG.md` with the addition

---

# Part 2: Technical Blog

Technical blogs do not require a fixed structure. Authors are free to choose the format that best suits their content.

## Required Elements

### 1. Frontmatter
```yaml
---
slug: feature-name
title: "Descriptive Title"
authors: [author-id]
tags: [relevant, tags, for, discovery]
jira: https://jira-link (optional)
---
```

### 2. Truncate Marker
Place `<!-- truncate -->` after the introduction to show preview on the blog list page.

## Review Criteria

When reviewing technical blogs, check the following:

### Technical Content
- [ ] Technical problem is clearly presented
- [ ] Solution/architecture is adequately described
- [ ] Code blocks have language specification

### Consistency
- [ ] Component names are consistent between diagrams and tables
- [ ] Information across diagrams does not contradict
- [ ] Components shown in diagrams are described in tables/text

## Knowledge Base

- Diagrams, Mermaidjs → `references/mermaidjs.md`
- Mermaidjs Best Practices → `references/mermaidjs-best-practices.md`

## Mermaid Diagram Rendering

### Rendering Script

Use `scripts/render_mermaid_diagram.py` to convert Mermaid diagrams in markdown files to PNG/SVG images.

#### Usage

```bash
# Render first diagram to PNG (default)
uv run .claude/skills/technical-design/scripts/render_mermaid_diagram.py blog/my-post.md

# Render to specific output file
uv run .claude/skills/technical-design/scripts/render_mermaid_diagram.py blog/my-post.md -o blog/diagram.png

# Render to SVG format
uv run .claude/skills/technical-design/scripts/render_mermaid_diagram.py blog/my-post.md -f svg

# Render all diagrams in file (adds index suffix: _1.png, _2.png, etc.)
uv run .claude/skills/technical-design/scripts/render_mermaid_diagram.py blog/my-post.md --all
```

#### Features

- Extracts all Mermaid code blocks from markdown files
- Renders using mermaid.ink service (no local dependencies)
- Supports PNG and SVG output formats
- Can render single or all diagrams in a file
- Auto-generates filenames for multiple diagrams

#### When to Use

- Generating static images for documentation
- Creating diagrams for external sharing
- Converting architecture-beta diagrams that use Iconify icons
- Producing high-resolution images for presentations

#### Notes

- The script uses mermaid.ink service, so internet connection is required
- For architecture-beta diagrams with Iconify icons, PNG format is recommended
- Output files are saved in the same directory as input by default

## File Location

Technical blogs go in: `blog/YYYY-MM-DD-feature-name.md`
