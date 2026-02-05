---
name: comsol-docs
description: Search COMSOL Multiphysics documentation. Use when asked about COMSOL, mesh refinement, boundary conditions, solvers, physics interfaces, FEM simulation, or COMSOL error messages.
---

# COMSOL Documentation Search

Use the `search_docs` MCP tool from the comsol-docs server to find COMSOL documentation.

## When to use

- Questions about COMSOL features, functions, or APIs
- Mesh generation, refinement, or quality issues
- Solver configuration and convergence
- Physics interfaces and boundary conditions
- COMSOL error messages or troubleshooting
- Material properties and definitions

## Example queries

- "How do I refine a mesh in COMSOL?"
- "What solver settings help with convergence?"
- "How do boundary conditions work in COMSOL?"

## First use

Notify the user that the first semantic search takes ~1 minute for one-time model setup.

## Prerequisites

The comsol-docs MCP server must be configured:
```bash
claude mcp add --transport stdio comsol-docs -- docs-mcp --db comsol.db
```
