---
name: Generate project artifact
description: Creates an antifact following the project's patterns and methods. Use when you need to create a new artifact in a bounded context/module. Use to create new entities, services, repositories, or any other artifact in the application. It internally uses the /generate command.
---

# Usage

`/generate [artifact] [bounded-context] [name]`

# Instructions

- The `/generate` command will tell you if you choose correctly an existent and valid artifact. Careful with this.
- [MUST DO] You must call the `code_understander` skill if you didn't make it yet. This file contains the artifact implementation details and rules, and you MUST READ the respective artifact reference before calling the /generate command.
- [MUST DO] Use the `structure_understander` skill, if you didn't make it yet, to read and understand the folder structure of the project, before starting implementing.
