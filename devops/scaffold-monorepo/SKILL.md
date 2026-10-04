---
name: scaffold-monorepo
description: Scaffold a monorepo with multiple packages or services
argument-hint: <project-name> [packages...]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: high
---

# Monorepo Scaffold

Create a monorepo structure with multiple packages/services.

## Input

- Project name: `$0`
- Package names: `$1`, `$2`, etc. (or read from architecture doc)

## Process

1. Create root project structure:
   - Root README.md, CLAUDE.md, .gitignore
   - Workspace configuration (npm workspaces, Python namespace packages, or similar)
   - Shared CI configuration
   - Root Makefile with targets for each package
2. For each package/service:
   - Create package directory with its own manifest
   - Stub implementation with proper interfaces
   - Package-level tests
   - Package-level README
3. Set up inter-package references where needed
4. Create shared utilities package if common patterns exist
5. Docker compose with all services
6. Git init + initial commit

## Rules

- Each package must be independently testable
- Shared dependencies managed at root level
- Clear boundaries between packages
- CI runs all packages