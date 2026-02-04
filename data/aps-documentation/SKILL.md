---
name: aps-documentation
description: |
  Comprehensive skill for working with Agile Protocol Specification documentation.
  Automatically activates when creating, editing, or reviewing APS content.
  Provides templates, naming conventions, and document lifecycle guidance.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# APS Documentation Skill

This skill provides comprehensive guidance for working with the Agile Protocol Specification documentation system.

## When This Skill Activates

- Creating new documentation chapters or sections
- Editing existing APS content
- Reviewing documents for compliance
- Managing document lifecycle transitions
- Working with metadata-rich filenames

## Key Concepts

### Document States

**Mutable States** (open to changes):
- **Draft**: Initial creation, open for major edits
- **Provisional**: Temporary acceptance, awaiting full review
- **In Review**: Under formal review process

**Immutable States** (locked):
- **Accepted**: Approved by stakeholders
- **Final**: Officially complete, archived

### Metadata-Rich Naming

Pattern: `{Type}_{Version}_{State}_{Date}_{Author}.ext`

Examples:
- `requirements_v1.0.0_draft_2024-03-22_SC.md`
- `architecture_v2.1.0_accepted_2024-04-15_Team.md`

## Templates

### New Chapter
```markdown
# [Chapter Title]

[Introduction explaining purpose]

## [Main Section]

[Content]

## Conclusion

[Key takeaways]

---
```

### Context File
```yaml
---
module-name: [Name]
version: 1.0.0
description: |
  [Purpose and content description]
related-modules:
  - name: [Related]
    path: ./path/to/module.md
technologies:
  - Markdown
  - mdBook
conventions:
  - Follow APS naming conventions
  - Include metadata headers
---
```

## Best Practices

1. **Structure First**: Plan document hierarchy before writing
2. **Clear Headings**: Use descriptive section titles
3. **Cross-Reference**: Link related content
4. **Context Files**: Create for new modules
5. **Update SUMMARY.md**: Add new chapters to navigation
6. **Build Test**: Run `mdbook build` to verify

## Resources

- Main SUMMARY: `specification-guide/src/SUMMARY.md`
- Glossary: `specification-guide/src/appendices/glossary.md`
- Templates: `specification-guide/src/appendices/templates_examples.md`
