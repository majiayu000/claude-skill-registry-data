---
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up.
category: memory
sources:
  - repository: matt-pocock-skills
    original_path: skills/productivity/handoff/SKILL.md
    sha256: 7c62de979fdc7ac32fb5ddb2146156c917f80ee070d30fadc9d40343c4b6ed25
principles:
  - core/think-before-coding
  - core/simplicity-first
  - core/surgical-changes
  - core/goal-driven-execution
---

> **Library use:** Apply the [compatibility and execution contract](../../COMPATIBILITY.md). Source roles, memory claims, command names, hooks, and integrations are instructions or prerequisites—not installed capabilities.

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save to the temporary directory of the user's OS - not the current workspace.

Include a "suggested skills" section in the document, naming which skills the next agent should call the Skill tool for.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.
