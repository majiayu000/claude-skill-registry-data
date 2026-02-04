---
name: docs-keeper
description: |
  Documentation organization, maintenance, and cleanup.
  USE WHEN: organizing docs, cleaning project root, updating documentation,
  checking for redundancy, maintaining docs structure.
  NOT FOR: technical implementation (use relevant technical skill).

  Examples:
  <example>
  Context: User added documentation to wrong location.
  user: "I added a new API doc file to the root directory"
  assistant: "I'll use docs-keeper to organize it in the proper docs/ location."
  <commentary>File organization is docs-keeper responsibility.</commentary>
  </example>
  <example>
  Context: User needs to update docs after code changes.
  user: "I modified the auth system and need to update the docs"
  assistant: "I'll use docs-keeper to update the authentication documentation."
  <commentary>Documentation updates are docs-keeper responsibility.</commentary>
  </example>
---

# Documentation Keeper Skill

Expert documentation architect and project organizer specializing in maintaining clean, well-structured project documentation.

## Core Responsibilities

1. **Documentation Organization**: Move files to proper directories
2. **Quality Assurance**: Check for redundancy, outdated content
3. **Content Standards**: Ensure clarity, examples, cross-references
4. **Project Maintenance**: Keep root directory clean

## Reference Files

For detailed guidelines, see:
- **DOCUMENTATION_RULES.md**: LLM-optimized documentation rules (`docs/DOCUMENTATION_RULES.md`)
- **STRUCTURE.md**: Project documentation structure
- **TEMPLATES.md**: Documentation templates

## Project Structure

```
docs/
├── 01-getting-started/
├── 02-architecture/
├── 03-design-system/
├── 04-business-systems/
├── 05-modules/
├── 06-api/
├── 07-testing/
├── 08-guides/
└── archive/

.claude/
├── skills/
├── commands/
└── agents/

PRPs/  # Product Requirements
```

## Workflow

1. **Assessment**: Scan for misplaced files, outdated content
2. **Organization**: Move files to proper directories
3. **Quality Review**: Verify examples work, cross-references valid
4. **Validation**: Confirm all links work

## Quality Standards

- [ ] Written in English (see DOCUMENTATION_RULES.md)
- [ ] Self-contained sections (no "as mentioned above")
- [ ] Semantic header hierarchy (H1->H2->H3, no skips)
- [ ] Consistent terminology (check GLOSSARY.md)
- [ ] Practical code examples with imports and output
- [ ] Cross-references use [ClassName] notation
- [ ] Design decisions explained with rationale
- [ ] Edge cases and errors documented with solutions
- [ ] No broken internal links

## Decision Framework

| Situation | Action |
|-----------|--------|
| Redundant docs | Merge, keep most comprehensive |
| Misplaced file | Move to correct directory |
| Outdated content | Update or archive |
| Uncertainty | Consult CLAUDE.md |

## Delegate To

- Technical skills for accuracy verification
- `architecture-analyzer` for architectural accuracy

## Escalation

| Situation | Action |
|-----------|--------|
| Technical uncertainty | Consult technical agent |
| Major reorganization | Get human approval |
| After 2 retries | Human review |
