---
name: openwebf-bridge
description: DEPRECATED umbrella Skill (backward compatibility). Use only for broad bridge-module orchestration across codegen + Dart + registration + JS usage. Prefer the focused bridge module codegen Skill.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, mcp__openwebf__docs_search, mcp__openwebf__docs_get_section, mcp__openwebf__docs_related, mcp__openwebf__templates_get, mcp__openwebf__templates_render
---

# OpenWebF Bridge Skill

## Deprecated

Prefer:
- `openwebf-bridge-module-codegen`

## Instructions

If this umbrella Skill is active, route to `openwebf-bridge-module-codegen` and follow its workflow. Keep APIs minimal and explicitly handle permissions and errors.

If repo context is missing, start with `/webf:doctor` and then route to the focused Skill.

## Examples

- “Create a DeepLink module (Dart + TypeScript types) and show usage from React.”
