---
name: code-review
description: Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes — Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/PRD asked for?). Runs both reviews in parallel sub-agents and reports them side by side. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to "review since X".
---

Two-axis review of the diff between `HEAD` and a fixed point the user supplies:

- **Standards** — does the code conform to this repo's documented coding standards?
- **Spec** — does the code faithfully implement the originating issue / PRD / spec?

Both axes run as **parallel sub-agents** so they don't pollute each other's context, then this skill aggregates their findings.

The issue tracker should have been provided to you — run `/setup-matt-pocock-skills` if `docs/agents/issue-tracker.md` is missing.


## Dynamic Resources (Progressive Disclosure)

This skill is large. To save context, its detailed instructions are split into separate files in the `resources/` directory.
**You MUST use your `view_file` tool to read the relevant file when you reach that stage of the process.**

- **[resources/process.md](file:///D:/GIT/graph-orchestrator-smolagents/skills/code-review/resources/process.md)**: Read this to understand Process.
- **[resources/why_two_axes.md](file:///D:/GIT/graph-orchestrator-smolagents/skills/code-review/resources/why_two_axes.md)**: Read this to understand Why two axes.
