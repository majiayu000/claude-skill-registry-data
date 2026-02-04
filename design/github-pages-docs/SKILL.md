---
name: github-pages-docs
description: Create and maintain GitHub Pages documentation for administrative guides, ubiquitous language definitions, and domain-driven design artifacts. Use when writing or updating documentation for admin procedures, domain terminology, DDD concepts, or user guides that will be published to GitHub Pages.
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, WebFetch
---

# GitHub Pages Documentation Writer

This skill helps create high-quality, well-structured documentation for GitHub Pages, specifically focused on:
- Administrative website manuals and how-to guides
- Ubiquitous Language definitions from the domain model
- Domain-Driven Design (DDD) artifacts and architecture documentation
- User guides and tutorials

## Documentation Principles

### 1. Structure and Organization
- Use clear hierarchical structure with proper heading levels (H1 for title, H2 for sections, H3 for subsections)
- Include a table of contents for documents longer than 3 sections
- Organize content logically: overview first, then details, then examples
- Use consistent file naming: kebab-case for URLs (e.g., `admin-tournament-setup.md`)

### 2. Content Guidelines

#### For Administrative Guides
- Start with "What you'll learn" or "Purpose" section
- Include prerequisites (required permissions, data, or setup)
- Provide step-by-step instructions with numbered lists
- Add screenshots or diagrams where helpful (reference images in `/docs/assets/images/`)
- Include common troubleshooting scenarios
- Link to related documentation
- End with "Next Steps" or "Related Tasks"

#### For Ubiquitous Language Definitions
- Organize by bounded context or domain area
- Define each term clearly and concisely
- Include the context where the term applies
- Provide examples of usage
- Cross-reference related terms
- Note any synonyms or terms that should be avoided
- Reference the source code location where the term is implemented

#### For DDD Artifacts
- Document bounded contexts with clear boundaries
- List aggregates, entities, and value objects with their responsibilities
- Describe domain events and their triggers
- Include diagrams (Mermaid.js is supported in GitHub Pages)
- Show relationships between domain concepts
- Provide code examples from the actual implementation

### 3. Markdown Best Practices

#### Formatting
- Use **bold** for emphasis and UI element names (e.g., "Click the **Save** button")
- Use `code formatting` for technical terms, file paths, and code snippets
- Use > blockquotes for important notes or warnings
- Use tables for structured data comparison
- Use fenced code blocks with language identifiers for syntax highlighting

#### Links
- Use relative links for internal documentation: `[Error Codes](./error-code-standards.md)`
- Use descriptive link text (not "click here")
- Verify all links work before publishing
- Link to source code on GitHub when referencing implementation: `[Name.cs](../../src/backend/Neba.Domain/Bowlers/Name.cs)`

#### Code Snippets
```csharp
// Show realistic, working examples from the codebase
public static Error FirstNameRequired => Error.Validation(
    code: "Name.FirstName.Required",
    description: "First name is required."
);
```

### 4. GitHub Pages Configuration

#### Front Matter
Include YAML front matter for Jekyll processing:
```yaml
---
layout: default
title: Page Title
nav_order: 2
parent: Parent Page Name (if applicable)
---
```

#### Navigation
- Use `nav_order` to control sidebar ordering
- Group related pages under a parent page
- Keep navigation hierarchy shallow (max 2-3 levels)

### 5. Documentation Templates

#### Administrative How-To Template
```markdown
---
layout: default
title: [Task Name]
nav_order: [number]
parent: Admin Guides
---

# [Task Name]

## Overview
Brief description of what this task accomplishes and why it's needed.

## Prerequisites
- Required permissions
- Required data or preparation
- Related setup that must be completed first

## Steps

### 1. [First Step]
Detailed instructions...

### 2. [Second Step]
More instructions...

## Verification
How to confirm the task completed successfully.

## Troubleshooting

### Issue: [Common Problem]
**Cause:** Why this happens
**Solution:** How to fix it

## Related Tasks
- [Related Task 1](./related-task.md)
- [Related Task 2](./another-task.md)
```

#### Ubiquitous Language Entry Template
```markdown
---
layout: default
title: [Domain Context] Terms
nav_order: [number]
parent: Ubiquitous Language
---

# [Domain Context] Terms

## [Term Name]

**Definition:** Clear, concise definition of the term.

**Context:** Where this term is used (e.g., "Tournament Management bounded context")

**Examples:**
- Example 1 of how the term is used
- Example 2 in a sentence or scenario

**Implementation:** [`ClassName.cs`](../../src/backend/Neba.Domain/Context/ClassName.cs)

**Related Terms:** [OtherTerm](#otherterm), [AnotherTerm](./other-context-terms.md#anotherterm)

---

## [Next Term]
...
```

## Workflow

When creating documentation:

1. **Understand the context**
   - Read existing source code, domain models, or admin code
   - Review the Error Code Standards document for terminology
   - Check existing documentation for consistency

2. **Identify the audience**
   - Administrators who need step-by-step guides
   - Developers who need to understand the domain
   - Future maintainers who need architecture context

3. **Extract information**
   - Use Grep to find domain models, entities, and value objects
   - Read source code to understand implementation details
   - Look for XML documentation comments in the code

4. **Structure the content**
   - Choose the appropriate template
   - Organize information hierarchically
   - Add front matter for Jekyll

5. **Write clearly**
   - Use active voice ("Click Save" not "Save should be clicked")
   - Be specific and actionable
   - Include examples from the actual codebase

6. **Review and validate**
   - Check all code references are accurate
   - Verify file paths and links work
   - Ensure consistent terminology with existing docs

## File Organization

Suggested documentation structure:
```
docs/
├── index.md                    # Documentation home
├── admin/
│   ├── index.md               # Admin guide overview
│   ├── tournament-setup.md
│   ├── member-management.md
│   └── awards-management.md
├── domain/
│   ├── index.md               # Domain documentation overview
│   ├── ubiquitous-language.md
│   ├── bounded-contexts.md
│   ├── aggregates.md
│   └── error-codes.md         # Reference Error Code Standards.md
├── api/
│   └── index.md               # API reference
└── assets/
    └── images/                # Screenshots and diagrams
```

## Integration with Existing Standards

### Error Code Standards
When documenting error codes, always reference the [Error Code Standards](../../src/backend/Neba.Domain/Error%20Code%20Standards.md):
- Use the format: `<DomainContext>.<Object>.<Member>.<Rule>`
- Show the ErrorOr library usage
- Include metadata examples
- Cross-reference to domain model documentation

### Domain-Driven Design
- Reference bounded contexts from the codebase structure
- Document aggregates as defined in the Domain layer
- Use the same terminology as the source code
- Link documentation to actual implementation files

## Quick Reference

### Common Tasks
- **Create admin guide:** Use Administrative How-To template
- **Document domain terms:** Use Ubiquitous Language Entry template
- **Add DDD artifact:** Include diagrams, code examples, and relationships
- **Update existing doc:** Maintain consistent format and front matter

### Resources
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [Markdown Guide](https://www.markdownguide.org/)
- [Mermaid.js for Diagrams](https://mermaid.js.org/)
