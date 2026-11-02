---
name: agent-workspace-isolation
description: "Use when checking that an agent's file operations remain inside the assigned workspace and artifact boundaries; not for general repository architecture mapping."
---

# Agent Workspace Isolation

## Purpose

Detect path traversal, symlink, temporary-file, and tool-routing cases that could let an agent touch unintended files.

## Required inputs

Declared workspace root, allowed output paths, file tool permissions, symlink policy, temp/cache behavior, and a non-sensitive fixture repository.

## Workflow

1. Define the canonical workspace root and normalize allowed paths before any operation; specify whether links may point outside that root.
2. Test relative traversal, absolute paths, mixed separators, symlinks, case normalization, nested worktrees, and temporary-file cleanup.
3. Inspect tool wrappers and subprocess working directories to ensure path checks apply after normalization and to every delegated command.
4. Run denied-path tests and confirm the agent stops with a clear reason rather than silently switching to a broader directory.

## Verification checklist

- [ ] Path containment is verified after canonicalization, not with string-prefix checks alone.
- [ ] Symlink and junction behavior is explicit for the target operating system.
- [ ] Subprocesses inherit the intended working directory and limited permissions.
- [ ] Failed operations do not leave partial files outside the approved root.

## Required output

A workspace boundary model, path-attack test matrix, observed results, and smallest corrective controls.

## Boundaries and failure handling

Use synthetic paths and canary files. Do not probe unrelated user directories or modify files outside the authorized workspace.

When required evidence, permissions, or environment details are unavailable, stop at the supported analysis, record the missing prerequisite, and do not report an unexecuted validation as passing.

## Trigger examples

- **Positive:** An agent tool accepts a file path generated from repository text.
- **Negative:** Mapping packages and dependencies across a repository when path containment is already established.
