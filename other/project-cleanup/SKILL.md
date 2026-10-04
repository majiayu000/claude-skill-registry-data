---
name: project-cleanup
description: Inspect a project and propose safe cleanup of generated or cache files.
risk: medium
required_tools:
  - file.list
  - project.cleanup_safe
  - git.status
---

# Project Cleanup

Use this skill when the user asks to clean a project, remove generated files, clear caches, or prepare a tidy workspace.

Rules:
- Inspect before proposing cleanup.
- Use `project.cleanup_safe` for cleanup actions.
- Never propose source, config, secrets, package manifests, or repository control files.
- Move approved cleanup items to backup; do not permanently delete them.
