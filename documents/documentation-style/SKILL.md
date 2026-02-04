---
name: documentation-style
description: Apply consistent documentation standards and style guidelines when creating, reviewing, or improving project documentation (README, architecture docs, guides, references). This skill should be used when writing new documentation, reviewing existing docs for style consistency, or when users request documentation improvements or style guide compliance checks.
---

# Documentation Style Guide

## Overview

This skill provides standards and conventions for writing project documentation. Apply these guidelines to ensure consistent, professional, and maintainable documentation across the project.

## When to Use This Skill

Activate this skill when:
- Writing new documentation (README, guides, architecture docs, etc.)
- Reviewing existing documentation for style consistency
- Improving documentation structure or readability
- Ensuring documentation follows project standards
- Users request "write documentation following style guide" or similar

## Core Guidelines

### Document Structure Principles

Follow these structural standards:
- Start with clear H1 title and one-line description
- Use H2 (`##`) for main sections, H3 (`###`) for subsections
- Separate major sections with horizontal rules (`---`)
- Keep section titles concise and action-oriented

### Writing Style Standards

Apply these writing conventions:
- Use clear, direct language in present tense
- Prefer active voice over passive voice
- Keep content concise and focused
- Start bullet points with action verbs
- Use parallel structure in lists

### Technical Formatting

Apply consistent formatting:
- Use backticks for code elements: `variable`, `function()`, `file.txt`
- Use **bold** for important concepts
- Use *italics* sparingly for subtle emphasis
- Include language identifiers in fenced code blocks
- Keep examples short and focused

### Content Organization

Structure content effectively:
- One main idea per section
- Limit lists to 5-7 items for readability
- Provide concrete examples over abstract concepts
- Link to other documents instead of repeating content
- Keep documents under 200 lines when possible

## Usage Workflow

### Creating New Documentation

When writing new documentation:

1. **Structure**: Start with title, description, and main sections with horizontal rules
2. **Content**: Write in present tense, active voice, with clear bullet points
3. **Formatting**: Apply backticks for code, bold for emphasis, proper code blocks
4. **Examples**: Include concrete, realistic examples with proper formatting
5. **Review**: Check against style guide before finalizing

### Reviewing Existing Documentation

When reviewing documentation:

1. **Load Reference**: Read `references/DOCUMENTATION_STYLE.md` for complete guidelines
2. **Structure Check**: Verify proper heading hierarchy and section separation
3. **Style Check**: Ensure consistent tone, voice, and formatting
4. **Content Check**: Verify clarity, conciseness, and proper organization
5. **Provide Feedback**: List specific improvements with examples

### Common Review Patterns

Search for these common issues:
- Passive voice: "should be used" → "use"
- Inconsistent formatting: missing backticks on code elements
- Overly long sections: break into subsections
- Missing examples: add concrete illustrations
- Redundant content: consolidate or link to other docs

## Resources

### references/DOCUMENTATION_STYLE.md

Complete style guide documentation with detailed sections:
- Document structure templates and examples
- Writing style guidelines and tone standards
- Code formatting conventions
- List organization best practices
- Special sections (benefits, summaries)
- Formatting conventions (emphasis, links, code)
- Content guidelines (specificity, focus, updates)
- Document type patterns (reference, guide, overview)

**When to read**: Load this reference when reviewing documentation, answering detailed style questions, or when more comprehensive guidance is needed beyond the core guidelines in this skill.

**Search patterns**: Use grep to find specific guidance:
- "tone and voice" for writing style
- "code examples" for code formatting
- "list structure" for organizing lists
- "benefits sections" for special formatting

## Examples

### Example 1: Creating New Documentation

User: "Write a new architecture document for the CLI sync component"

Response:
1. Apply document structure with H1 title, description, and `---` separator
2. Organize with H2 main sections (Overview, Architecture, Components)
3. Use backticks for technical terms: `CLISyncer`, `sync_config()`
4. Include concrete code examples with language identifiers
5. Keep sections focused and under 200 lines total

### Example 2: Reviewing Documentation

User: "Review this README for style compliance"

Response:
1. Check structure: proper heading hierarchy, section separators
2. Check style: present tense, active voice, clear bullets
3. Check formatting: code elements in backticks, proper emphasis
4. Provide specific feedback with before/after examples
5. List improvements prioritized by impact

### Example 3: Improving Documentation

User: "Improve the documentation style in this guide"

Response:
1. Load `references/DOCUMENTATION_STYLE.md` for comprehensive guidelines
2. Identify style issues: passive voice, inconsistent formatting, structure
3. Apply corrections following the complete style guide
4. Maintain original meaning while improving clarity
5. Explain changes made and rationale

## Notes

- The complete style guide in `references/` contains comprehensive details
- For quick checks, use the core guidelines in this skill
- For thorough reviews or detailed questions, load the full reference
- Maintain consistency across all project documentation
- Update style guide when new patterns emerge
