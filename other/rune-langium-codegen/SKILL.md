---
description: "Generate TypeScript, Zod, JSON Schema, and form-preview metadata from parsed\nRune DSL documents."
name: rune-langium-codegen
---

# @rune-langium/codegen

Generate TypeScript, Zod, JSON Schema, and form-preview metadata from parsed
Rune DSL documents.

Import this API from `@rune-langium/codegen/export`; the package root is empty.
Inbound import and Rosetta rendering APIs use separate subpaths.

Use `generate()` when you need emitted files for a concrete target, and
`generatePreviewSchemas()` when UI tooling needs structured field metadata and
source maps for a selected data type. This package expects parsed Langium
documents from `@rune-langium/core`.

## Configuration

9 configuration interfaces — see references/config.md for details.

## Quick Reference

95 exports (37 functions, 3 classes, 49 types, 6 constants) — see references/ for full API.

## References

Load these on demand — do NOT read all at once:

- When calling any function → browse `references/functions/` for grouped indexes, full signatures, parameters, and return types
- When using a class → read `references/classes.md` for properties, methods, and inheritance
- When defining typed variables or function parameters → read `references/types.md`
- When using exported constants → read `references/variables.md`
- When configuring options → read `references/config.md` for all settings and defaults

## Links

- Author: Pradeep Mouli <pmouli@mac.com> (https://github.com/pradeepmouli)