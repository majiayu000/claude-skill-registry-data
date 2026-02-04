---
name: dockerignore-generator
description: Generate .dockerignore files to exclude unnecessary files from Docker builds. Triggers on "create dockerignore", "generate docker ignore", "dockerignore for", "docker exclude files".
---

# Dockerignore Generator

Generate .dockerignore files to optimize Docker builds by excluding unnecessary files.

## Output Requirements

**File Output:** `.dockerignore`
**Format:** Docker ignore file syntax
**Standards:** Docker best practices

## When Invoked

Immediately generate a complete .dockerignore file appropriate for the project type.

## Example Invocations

**Prompt:** "Create dockerignore for Node.js project"
**Output:** Complete `.dockerignore` excluding node_modules, tests, docs.
