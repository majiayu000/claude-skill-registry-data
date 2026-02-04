---
name: user-manual-generator
description: Generate comprehensive end-user documentation from application codebases
version: 2.0.0
allowed-tools: [Read, Write, Glob, Grep, Bash, Edit]
tags: [documentation, user-manual, static-site, markdown]
---

# User Manual Generator

Generate comprehensive, deployment-ready user documentation from application codebases using intelligent code analysis and documentation best practices.

## Overview

This skill analyzes your codebase to automatically generate user-focused documentation (not developer/API docs). It creates deployment-ready static sites compatible with GitHub Pages, Netlify, and Vercel, following the Diataxis framework (tutorials, how-to guides, reference, explanation).

**Use this skill when you need to:**
- Create end-user documentation for web apps, APIs, CLI tools, or desktop applications
- Generate documentation that helps users accomplish tasks, not just understand code
- Deploy professional documentation sites quickly
- Establish a documentation foundation that evolves with your code

**Don't use this skill for:**
- API-only documentation (use OpenAPI/Swagger generators instead)
- Internal developer documentation (use JSDoc/Sphinx/Godoc)
- Simple README files (write those manually)

## Workflow

When invoked, follow these phases in order. **Load each phase's context file only when you reach that phase** to minimize context usage:

### Phase 1: Discovery & Requirements
> **Context:** Read `phases/01-discovery.md`

Ask clarifying questions and analyze the codebase to understand:
- Application type (web, API, CLI, desktop)
- Target audience
- Preferred static site generator
- Documentation depth needed

### Phase 2: Feature Extraction
> **Context:** Read `phases/02-feature-extraction.md`

Extract user-facing features from code:
- Routes and navigation (web apps)
- Endpoints and schemas (APIs)
- Commands and options (CLI)
- Menus and settings (desktop)

### Phase 3: Structure Planning
> **Context:** Read `phases/03-structure-planning.md`

Plan documentation structure using Diataxis framework:
- Tutorials (learning-oriented)
- How-to guides (task-oriented)
- Reference (information-oriented)
- Explanation (understanding-oriented)

### Phase 4: Content Generation
> **Context:** Read `phases/04-content-generation.md`
> **Templates:** Read from `templates/` directory as needed

Generate documentation content using templates:
- Writing guidelines for user-focused content
- Templates for each documentation type
- Example formats and placeholders

### Phase 5: Static Site Setup
> **Context:** Read `phases/05-static-site-setup.md`
> **SSG Config:** Read from `ssg/` directory based on user's choice

Set up the chosen static site generator:
- MkDocs Material (`ssg/mkdocs.md`)
- Docusaurus (`ssg/docusaurus.md`)
- VitePress (`ssg/vitepress.md`)
- Plain Markdown (`ssg/plain-markdown.md`)

### Phase 6: Quality Assurance
> **Context:** Read `phases/06-quality-assurance.md`

Perform quality checks:
- Completeness verification
- Link validation
- Code sample verification
- Accessibility checks

### Phase 7: Handoff
> **Context:** Read `phases/07-handoff.md`

Generate final deliverables:
- Generation report
- TODO list for manual work
- Deployment instructions
- Summary message for user

## Reference Materials

Load these only when needed for specific situations:

| Context Needed | File to Read |
|---------------|--------------|
| React, Express, Django, etc. patterns | `reference/tech-patterns.md` |
| Multi-language, versioning, API integration | `reference/advanced-features.md` |
| Do's and don'ts summary | `reference/best-practices.md` |
| Issues running this skill | `reference/skill-troubleshooting.md` |

## Quick Reference: Templates

| Template | Use For |
|----------|---------|
| `templates/installation.md` | Installation guide |
| `templates/quick-start.md` | Quick start guide |
| `templates/how-to-guide.md` | Task-oriented guides |
| `templates/configuration-reference.md` | Config options reference |
| `templates/api-reference.md` | API endpoint documentation |
| `templates/cli-reference.md` | CLI command reference |
| `templates/troubleshooting.md` | Error messages and FAQ |

## Expected Outcome

- 70-80% time saved vs manual documentation
- Deployment-ready site in minutes
- Solid foundation requiring ~20% manual refinement
- Maintainable docs that evolve with code

## Success Criteria

- Non-technical users can complete tasks using docs
- All major features covered
- Zero build errors
- Passes basic accessibility checks
- Deployable to chosen hosting platform
