---
name: architecture
description: Map a codebase's modules, responsibilities, and dependencies.
trigger: when the user asks about architecture, structure, or how modules relate
---
## When to use
The user asks about architecture, structure, layering, or how the parts relate.

## How
1. List the tree; group files into modules/layers (UI, API, core, data…).
2. For each module: one line on its responsibility and what it depends on.
3. Identify the boundaries (where modules talk) and tangled spots — a file doing
   too much, circular-looking imports.
4. Prefer a short arrows diagram (module → depends-on) plus a few sentences.

## Avoid
- Claims about files you didn't read — flag what you skipped.
- Restating the folder tree as if it were the architecture.

## Done well
A clear mental model: the main modules, who depends on whom, and where the risky
coupling is.
