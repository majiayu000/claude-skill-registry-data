---
name: create-project-docs
description: Creates comprehensive GitHub project documentation including README, CONTRIBUTING, CODE_OF_CONDUCT, CHANGELOG, architecture docs, and API documentation. Analyzes codebase to generate accurate, well-styled documentation with modern GitHub aesthetics. Use when setting up a new project, improving existing documentation, or generating missing docs.
---

<essential_principles>

<principle name="code-first-documentation">
Always analyze the actual codebase before writing documentation. Read source files, understand project structure, extract function signatures, and infer purpose from code. Never write documentation based on assumptions.
</principle>

<principle name="aesthetic-consistency">
All documentation follows modern GitHub conventions:
- Badges at top of README (build status, version, license, coverage)
- Table of contents for documents > 100 lines
- Collapsible sections for verbose content using `<details>`
- Emoji as section markers (use sparingly, consistently)
- Proper heading hierarchy (never skip levels)
- Code blocks with language identifiers
</principle>

<principle name="practical-examples">
Every feature documented must include a working example. Examples should be:
- Copy-pasteable (complete, not snippets)
- Tested against actual codebase
- Ordered from simple to complex
</principle>

<principle name="progressive-detail">
Start with what users need most, hide complexity:
1. Installation (first 30 seconds)
2. Quick example (first 2 minutes)
3. Common use cases (first 10 minutes)
4. Advanced topics (when needed)
</principle>

</essential_principles>

<intake>
What would you like to document?

1. **Generate full documentation suite** - README, CONTRIBUTING, CODE_OF_CONDUCT, CHANGELOG, architecture, API docs
2. **Generate a single document** - Create or replace one specific document
3. **Update existing documentation** - Refresh docs based on code changes
4. **Audit documentation** - Check what's missing or outdated

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "full", "suite", "all", "complete" | `workflows/generate-full-suite.md` |
| 2, "single", "readme", "contributing", "one" | `workflows/generate-single-doc.md` |
| 3, "update", "refresh", "sync" | `workflows/update-docs.md` |
| 4, "audit", "check", "missing" | `workflows/audit-docs.md` |

**After reading the workflow, follow it exactly.**
</routing>

<reference_index>
All domain knowledge in `references/`:

**Styling:** github-styling.md (badges, emoji, collapsible sections, modern conventions)
**Document Types:** doc-types.md (what each document should contain, best practices)
**Code Analysis:** code-analysis.md (how to extract info from source files)
</reference_index>

<template_index>
Output templates in `templates/`:

| Template | Purpose |
|----------|---------|
| readme-template.md | Modern README with all sections |
| contributing-template.md | Contribution guidelines |
| code-of-conduct-template.md | Community standards |
| changelog-template.md | Version history format |
| architecture-template.md | System design documentation |
| api-docs-template.md | API reference format |
</template_index>

<workflows_index>
| Workflow | Purpose |
|----------|---------|
| generate-full-suite.md | Create complete documentation set |
| generate-single-doc.md | Create one specific document |
| update-docs.md | Refresh existing docs from code |
| audit-docs.md | Check documentation completeness |
</workflows_index>

<success_criteria>
Documentation is complete when:
- All generated docs accurately reflect the codebase
- README provides working quick-start example
- Installation instructions are tested
- API documentation covers all public interfaces
- Styling is consistent across all documents
- Links between documents work correctly
</success_criteria>
