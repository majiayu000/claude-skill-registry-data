---
name: all-folders
description: Run one task or workflow across every folder in the project until the scope is covered
argument-hint: "[scope]"
related:
  - deep-analyze
  - scan-codebase
  - deep-validate
  - resolve-errors
  - report
---

## Goal

Work through every folder in the project following the specified workflow

## Scope

Use when a task must process multiple folders in the project according to a given workflow or pattern

## Execute

### 1. Discover Folders

> Goal: Find out which folders the project has and how to order them

1. Run `/deep-analyze` to inspect the main structure.
2. Run `/scan-codebase` to find the relevant directories.
3. Use `glob` or `find_file_by_name` to locate folders by pattern.
4. Record the folder list together with the processing order.

### 2. Process Each Folder

> Goal: Process each folder per the workflow without leaving conflicts

1. Read folder contents with `exec` using `ls` or `Get-ChildItem`.
2. Pick the workflow that fits the folder.
3. Process sequentially in order: foundation → dependent folders.
4. Record the status of each folder.

### 3. Verify

> Goal: Confirm every folder was processed completely and correctly

1. Confirm every folder in scope has been processed.
2. Run `/deep-validate`.
3. If there are errors, run `/resolve-errors`.
4. Run `/report` to summarize the results.

## Rules

### 1. Processing Order

- Process foundation folders first (root, config, types)
- Process folders with complex dependencies later

### 2. Batch Operations

- Read folders in parallel
- Process folders sequentially to avoid conflicts

### 3. Error Handling

- Record folders that had problems
- Run `/resolve-errors` for folders with issues
- If the error rate is high → stop and report before continuing

## Expected Outcome

- Every folder in scope is fully processed
- No broken references or missing folders
- Passes `/deep-validate`
- A summary report exists
