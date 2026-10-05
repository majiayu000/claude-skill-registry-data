---
name: handoff
description: Compact the current conversation into a handoff document so a fresh agent can continue the work.
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
---

Write a handoff document summarising the current conversation so a fresh agent can continue the work.

Save it to `.plan/handoffs/<YYYY-MM-DD>-<slug>.md` at the repository root, creating the directory if needed (`.plan/` is committed to version control — it is the project's shared planning memory). If not working inside a repository, save to the OS temporary directory instead and tell the user the absolute path.

Include a "suggested skills" section, listing skills the next agent should invoke — by name, with a one-line reason each — noting they apply only if available in that agent's environment.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.
