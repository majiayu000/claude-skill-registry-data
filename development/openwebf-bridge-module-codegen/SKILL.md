---
name: openwebf-bridge-module-codegen
description: Build a WebF bridge module/native plugin using the module-codegen workflow (*.module.d.ts → codegen → Dart implementation → registration → JS usage). Use when the user mentions module-codegen, bridge module, native plugin, *.module.d.ts, or registering a module.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, mcp__openwebf__docs_search, mcp__openwebf__docs_get_section, mcp__openwebf__docs_related, mcp__openwebf__templates_get, mcp__openwebf__templates_render
---

# OpenWebF Bridge: Module Codegen Workflow

## Instructions

1. Confirm the desired API surface and keep it minimal, typed, and versioned.
2. Follow the official flow:
   - TypeScript `*.module.d.ts`
   - `webf module-codegen`
   - Dart module implementation
   - Registration in the host
   - JS usage example
3. Add guardrails: availability checks, permission handling, explicit errors.
4. Use MCP docs for authoritative steps and templates for scaffolding.

More:
- [reference.md](reference.md)
- [doc-queries.md](doc-queries.md)
- [examples.md](examples.md)
