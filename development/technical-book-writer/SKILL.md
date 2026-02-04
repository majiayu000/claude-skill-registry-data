---
name: technical-book-writer
description: Comprehensive guide for writing technical books in Markdown format. Use this skill when creating new chapters, managing code examples, reviewing content for technical accuracy and consistency, or organizing book structure (TOC, cross-references). Provides templates, validation scripts, and best practices for technical writing workflows.
---

# Technical Book Writer

## Overview

Enable systematic and high-quality technical book authoring through structured workflows, reusable templates, validation scripts, and best practices guidance. Support the complete lifecycle from planning to publication.

## Core Capabilities

### 1. Chapter Writing

Create well-structured technical content with consistent depth and reader focus.

**When to use:**
- Starting a new chapter or section
- Expanding existing content
- Restructuring chapter organization

**Process:**
1. Use `assets/chapter_template.md` as the foundation for new chapters
2. Follow the guidelines in `references/writing_guidelines.md` for technical depth and clarity
3. Apply `references/markdown_conventions.md` for consistent formatting
4. Ensure proper cross-references and internal links

**Template structure:**
- Chapter objectives and prerequisites
- Conceptual explanation sections
- Code examples with explanations
- Summary and next steps
- Exercises or challenges (optional)

### 2. Code Example Management

Create, validate, and maintain high-quality code examples that are tested and accurate.

**When to use:**
- Adding new code examples to chapters
- Validating existing code for accuracy
- Extracting code blocks for testing
- Updating code examples across chapters

**Process:**
1. Use templates from `assets/code_example_templates/` for language-specific examples
2. Follow `references/code_examples_guide.md` for naming, comments, and structure
3. Run `scripts/validate_code_examples.py` to extract and validate code
4. Use `scripts/extract_code_blocks.py` to extract code by language for testing

**Scripts:**
- `validate_code_examples.py` - Extract code blocks from markdown and validate syntax
- `extract_code_blocks.py` - Extract code blocks by language for external testing

### 3. Technical Review and Editing

Review content for technical accuracy, consistency, readability, and adherence to standards.

**When to use:**
- Before publishing chapters
- After major content updates
- Regular quality checks
- Consistency audits

**Review checklist:**
1. **Technical accuracy** - Verify code examples, technical explanations, and API usage
2. **Consistency** - Check terminology, code style, formatting across chapters
3. **Readability** - Assess clarity, flow, and reader comprehension
4. **Completeness** - Ensure prerequisites, learning objectives, and summaries are present
5. **Cross-references** - Validate internal links and references

Refer to `references/writing_guidelines.md` for detailed review criteria.

### 4. Book Structure Management

Maintain overall book organization, navigation, and cross-references.

**When to use:**
- Adding new chapters to the book
- Reorganizing chapter sequence
- Checking for broken links
- Validating TOC consistency

**Process:**
1. Use `assets/toc_template.md` to maintain the table of contents
2. Run `scripts/check_book_structure.py` to validate:
   - Broken internal links
   - Chapter numbering consistency
   - TOC alignment with actual chapters
   - Missing or duplicate chapter IDs

**Script:**
- `check_book_structure.py` - Comprehensive structure validation

### 5. Workflow Establishment

Create and maintain a systematic writing workflow for consistency and efficiency.

**Recommended workflow:**
1. **Planning** - Define chapter objectives, outline sections, identify code examples
2. **Drafting** - Use chapter template, write conceptual content, add placeholder code blocks
3. **Code Development** - Implement and test code examples externally
4. **Integration** - Insert validated code into chapter, add explanations
5. **Review** - Self-review using technical review checklist
6. **Validation** - Run validation scripts for code and structure
7. **Revision** - Address issues and improve clarity
8. **Publication** - Finalize and publish chapter

## Resources

### scripts/

**validate_code_examples.py**
Extract code blocks from markdown files and validate syntax. Supports multiple languages.

**check_book_structure.py**
Validate book structure including links, chapter numbering, and TOC consistency.

**extract_code_blocks.py**
Extract code blocks by language for external testing or compilation.

### references/

**writing_guidelines.md**
Comprehensive technical writing best practices including structure, explanations, reader focus, and depth calibration.

**code_examples_guide.md**
Standards for code examples including naming conventions, comments, testability, and integration.

**markdown_conventions.md**
Markdown formatting guidelines for headings, code blocks, links, images, and special formatting.

### assets/

**chapter_template.md**
Standard template for new chapters with sections for objectives, content, examples, and summary.

**code_example_templates/**
Language-specific code example templates (Python, JavaScript, TypeScript, Go, etc.) with proper structure and comments.

**toc_template.md**
Table of contents template for maintaining book organization.

## Best Practices

1. **Write for the reader** - Focus on learning outcomes, not just feature descriptions
2. **Test all code** - Every code example should be validated and tested
3. **Maintain consistency** - Use templates and guidelines to ensure uniform quality
4. **Review regularly** - Run validation scripts frequently to catch issues early
5. **Iterate** - Write, validate, review, and revise in cycles
6. **Document decisions** - Record architectural decisions and design choices in the book
