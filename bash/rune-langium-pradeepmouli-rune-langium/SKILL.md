---
name: rune-langium
description: "Router skill for the rune-langium monorepo. Use it to choose the right package skill before working in core, cli, lsp-server, codegen, or visual-editor."
license: SEE LICENSE IN LICENSE
---

# rune-langium

Use this router when the task spans the monorepo or you are not yet sure which package owns the behavior.

## Route by task

1. Parsing, ASTs, serializers, or `.rosetta` validation → `rune-langium-core`
2. CLI commands or terminal workflows → `rune-langium-cli`
3. Language-server integration, WebSocket LSP, diagnostics, hover, or completion → `rune-langium-lsp-server`
4. Code generation, preview schemas, or exported source maps → `rune-langium-codegen`
5. Graph rendering, React Flow nodes, layout, or visual-editor state → `rune-langium-visual-editor`

## Quick package guide

### core → `rune-langium-core`

- Parse a single file or a full workspace
- Validate cross-file references
- Serialize models back to Rune/Rosetta text

### cli → `rune-langium-cli`

- Run the `rune-dsl` command
- Wire parser/codegen flows into shell scripts or local tooling

### lsp-server → `rune-langium-lsp-server`

- Embed or host the Rune DSL language server
- Bridge Monaco/CodeMirror/browser editors to LSP features

### codegen → `rune-langium-codegen`

- Generate derived artifacts from parsed documents
- Build or consume form-preview schemas and code-preview source maps

### visual-editor → `rune-langium-visual-editor`

- Render and interact with Rune graphs in React
- Work on node rendering, layout, or store behavior

## Rules

- Do not load every package skill at once; start with the owning package.
- If a task crosses package boundaries, begin with the foundational package and then move outward.
