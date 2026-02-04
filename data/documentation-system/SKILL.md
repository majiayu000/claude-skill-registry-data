---
name: Documentation System
description: Standards for documenting codebases. Use when writing documentation, deciding where docs should go, reviewing doc quality, or updating docs after code changes. Covers folder structure, content guidelines, and maintenance workflows.
---

# Documentation System

A system for writing clear, maintainable documentation optimized for both humans and AI navigation.

## Core Philosophy

1. **Document logic, not syntax** - Explain how things work together, not what's obvious from code
2. **Progressive disclosure** - Overview first, details on demand
3. **AI-navigable** - Clear structure so AI can find and update the right docs
4. **Minimal but complete** - Include what's needed, nothing more

## Folder Structure

Documentation lives in `docs/` with three top-level folders:

```
docs/
├── index.md          # Entry point: what is this codebase, how to navigate
├── system/           # How the system works (capabilities, concepts, flows)
├── packages/         # Per-package documentation
└── guides/           # Task-oriented how-tos
```

| Folder | Question It Answers |
|--------|---------------------|
| `system/` | "What does this system do? How does X work?" |
| `packages/` | "What does package Y do internally?" |
| `guides/` | "How do I accomplish Z?" |

Each folder has an `index.md` with navigation links and descriptions.

## When to Use Each Reference

Read these for detailed guidance:

| Reference | When to Read |
|-----------|--------------|
| [structure.md](references/structure.md) | Creating new docs, reorganizing, deciding where something goes |
| [content.md](references/content.md) | Writing or reviewing doc content, style questions |
| [maintenance.md](references/maintenance.md) | Code changed, checking if docs need updates |
| [templates/](references/templates/) | Starting a new doc, need a concrete starting point |

## Quick Reference

### Creating a New Doc

1. Determine type: system concept, package doc, or guide
2. Check if it should extend an existing doc instead
3. Use appropriate template from `references/templates/`
4. Add to relevant `index.md` navigation

### Finding Existing Docs

1. Start at `docs/index.md` for overview
2. System-level concepts → `docs/system/`
3. Package specifics → `docs/packages/[package-name].md`
4. How-to instructions → `docs/guides/`

### Updating Docs After Code Changes

1. Identify which docs reference the changed code
2. Check if descriptions are still accurate
3. Update code references (file paths, line numbers if used)
4. Don't remove content without checking cross-references

## What NOT to Document

- Implementation details that change frequently
- Information obvious from well-named code
- Auto-generatable content (API signatures, type definitions)
- Speculative future plans (use project tracking instead)
