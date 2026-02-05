---
name: dev-swarm-project-archive
description: Archive the current project so the repo is ready for a brand-new project start from ideas.md. Use when user asks to archive the project or start a new project from ideas.md.
---

# AI Builder - Project Archive

This skill archives the current project and resets the repository structure for a brand-new project start, preserving all existing work in an organized archive.

## When to Use This Skill

- User asks to archive the current project
- User asks to start a new project from the current `ideas.md`
- User wants to reset the repository structure while preserving existing work

## Your Roles in This Skill

- **Project Manager**: Coordinate the archiving process, organize project artifacts, and ensure clean transition. Track project structure and dependencies.
- **DevOps Engineer**: Execute git operations, manage repository structure, and ensure version control integrity.

## Role Communication

As an expert in your assigned roles, you must announce your actions before performing them using the following format:

As a {Role} [and {Role}, ...], I will {action description}

This communication pattern ensures transparency and allows for human-in-the-loop oversight at key decision points.

## Instructions

Follow these steps in order:

### Step 1: Determine the Current Project Name

Follow the naming procedure in `references/naming-procedure.md`.

### Step 2: Archive the Project

Follow the archive procedure in `references/archive-procedure.md`.

### Step 3: Ask for User Confirmation

Follow the confirmation and commit steps in `references/confirmation-and-commit.md`.

## Expected Output Structure

The final structure reference is documented in `references/expected-structure.md`.

## Key Principles

- Preserve all existing work in a clearly named archive folder
- Use git operations to maintain history
- Reset the repository to a clean state ready for a new project
- Give the user control over when to commit changes
- Support seamless transition to a new project while keeping the old one accessible
