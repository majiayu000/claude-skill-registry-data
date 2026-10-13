---
name: example-skill
description: A sample skill that greets the user and summarizes the current project
model: haiku
allowed-tools: Read, Glob
---

# Example Skill

Greet the user and provide a brief summary of the current project.

## Instructions

1. Read the project's `README.md` or `package.json` (if they exist) to understand what the project does.
2. List the top-level directory structure using `Glob`.
3. Respond with:
   - A friendly greeting
   - The project name and a one-sentence summary
   - The primary language/framework detected
   - A count of files by type

Keep the response concise — no more than 10 lines.
