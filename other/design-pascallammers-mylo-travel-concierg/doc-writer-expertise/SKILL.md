---
name: doc-writer-expertise
description: Deep expertise for documentation content creation. Templates, platform formatting guides, and style principles. Auto-loads for doc-writer agent.
---

# Doc-Writer Expertise

You have access to professional technical writing knowledge. Use these references when you need detailed guidance.

## Quick Reference

| Topic | Reference | When to Use |
|-------|-----------|-------------|
| Templates | [templates.md](references/templates.md) | Writing API docs, guides, tutorials |
| MkDocs | [platform-mkdocs.md](references/platform-mkdocs.md) | MkDocs formatting |
| Sphinx | [platform-sphinx.md](references/platform-sphinx.md) | Sphinx/RST formatting |
| Docusaurus | [platform-docusaurus.md](references/platform-docusaurus.md) | Docusaurus/MDX formatting |
| Style | [style-guide.md](references/style-guide.md) | Writing principles |

## Documentation Types

### API Documentation
For functions, classes, methods:
- Parameters with types
- Return values
- Exceptions/errors
- Code examples

See [templates.md](references/templates.md) for templates.

### Guides & Tutorials
For learning content:
- Step-by-step instructions
- Conceptual explanations
- Working examples

### Reference Documentation
For comprehensive coverage:
- All options documented
- Default values noted
- Cross-references

## Platform Quick Reference

| Platform | Admonitions | Code Blocks | Special |
|----------|-------------|-------------|---------|
| MkDocs | `!!! type` | ` ```lang ` | Material extensions |
| Sphinx | `.. type::` | `.. code-block::` | RST directives |
| Docusaurus | `:::type` | ` ```lang ` | MDX components |
| Hugo | Shortcodes | ` ```lang ` | Front matter |

See platform-specific guides for detailed formatting.

## Core Writing Principles

1. **Clarity**: Simple, precise language
2. **Accuracy**: Match code exactly
3. **Consistency**: Follow existing patterns
4. **Examples**: Show, don't just tell
5. **Completeness**: Cover common use cases

See [style-guide.md](references/style-guide.md) for comprehensive principles.

## Workflow Reminder

1. Read source code first
2. Follow platform formatting
3. Match existing style
4. Validate before returning
5. Report results clearly
