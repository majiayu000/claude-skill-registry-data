---
name: parallel-work
description: Coordinate multiple agents working simultaneously. Use when splitting tasks across agents or when avoiding overlapping diffs with shared files.
---

# Parallel Work

## Overview

Coordinate multi-agent work with strict file ownership and lock rules.

## Workflow

### 1) Split the work

- Break tasks into non-overlapping file areas.
- Assign each agent a clear scope and output.

### 2) Lock files

- Claim file/area locks in `docs/company/locks.md` before edits.
- Refuse to edit locked files; choose a different area or wait.

### 3) Execute in parallel

- Keep diffs localized to the assigned scope.
- Share progress and risks in short status notes.

### 4) Release

- Remove locks after changes are merged or abandoned.
