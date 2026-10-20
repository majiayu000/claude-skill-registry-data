---
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up.
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
---

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save to the temporary directory of the user's OS - not the current workspace.

Include a "suggested skills" section in the document, naming which skills the next agent should call the Skill tool for.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.

## Travel-Tool context

Vendored from mattpocock/skills (see `.claude/ECC.md`, section *Also vendored*).

- **In a Claude Code cloud session** (claude.ai/code), the OS temp directory is wiped with the container, so a handoff saved there is lost. Save it under `docs/handoffs/YYYY-MM-DD-<topic>.md` in the repo and commit it on the working branch instead. On a local machine, the temp directory is fine.
