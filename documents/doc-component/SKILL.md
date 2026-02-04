---
name: doc-component
description: Document a single component or module interactively. Use when you want to focus on one specific API.
---

# Document Single Component

Generate or update documentation for a specific source file.

## Usage

```
/doc-component src/components/button.rs
/doc-component Button
```

Accepts either a file path or a component/type name (will search for it).

## Process

1. **Locate**: Find the source file (search if name given)
2. **Read**: Parse the source thoroughly
3. **Check existing**: Read current doc if it exists
4. **Generate**: Write complete documentation following `docs` agent style
5. **Output**: Write to corresponding location in `docs/`

## Interactive Mode

If called without arguments, prompt for:
1. Component name or path
2. Whether to overwrite existing docs or merge

## Does NOT Update State

This skill doesn't update `docs-state.json` since it's for targeted work, not bulk updates. Run `/docs` afterward if you want to mark the codebase as documented.
