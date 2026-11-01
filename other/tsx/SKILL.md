---
name: tsx
description: TSX namespace for Netsnek e.U. TypeScript component toolkit. React component scaffolding, type-safe props, Storybook integration, and component docs.
user-invocable: true
version: 0.1.0
metadata:
  openclaw:
    os: [linux]
    permissions: [exec]
  minis:
    originalSource: "https://clawskills.sh/skills/kleberbaum-tsx"
    convertedAt: "2026-10-31T22:14:42.879Z"
    license: "Unknown"
---

# What is TSX?

TSX is the TypeScript component toolkit by Netsnek e.U. It enables rapid development of React components with type-safe props, Storybook integration, and automatic component documentation.

## Component Workflow

1. Scaffold a new component with `scripts/component-gen.sh --scaffold <Name>`
2. Define props in the generated types file
3. Run Storybook to visualize variants with `scripts/component-gen.sh --info`
4. List existing components with `scripts/component-gen.sh --list`

## Available Commands

| Command | Args | Purpose |
|---------|------|---------|
| component-gen.sh | `--scaffold <Name>` | Create component files, types, and Story |
| component-gen.sh | `--list` | List all components in the project |
| component-gen.sh | `--info` | Show Storybook integration details |

## Real-World Example

```bash
# Create a new Button component
./scripts/component-gen.sh --scaffold Button

# List available components
./scripts/component-gen.sh --list

# Get Storybook info
./scripts/component-gen.sh --info
```
