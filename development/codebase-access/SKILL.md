---
name: Codebase Access
description: Read files from the currently running project codebase.
---

# Codebase Skill

## Capabilities
- **Read File/Dir**: Read the contents of a file or list a directory within the project (`codebase.read`).

## Usage
- Use when asking checking for configuration, Project status, or compliance rules defined in the code.
- **SECURITY NOTE**: This tool allows reading the *source code of this application* (`process.cwd()`). It does NOT provide access to the user's local machine outside of the deployed environment.

## Constraints
- Read-only.
- Confined to the project root directory.
