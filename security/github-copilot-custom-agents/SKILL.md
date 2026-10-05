---
name: github-copilot-custom-agents
description: >-
  Use for creating, reviewing, or debugging GitHub Copilot custom agents in Visual Studio Code, including .agent.md roles, tool restrictions, model selection, subagent permissions, and handoffs. Do not use for a single slash command, automatic coding rules, Agent Skills, or merely changing the selected chat model.
argument-hint: "[agent role, authority, tools, handoffs, and host]"
---

# GitHub Copilot custom agents

Create a role only when its instructions and capability boundary recur. Tool
restriction reduces capability but does not make model output a security boundary.

## Workflow

1. Define the role, non-goals, user/model invocation, allowed mutations,
   evidence, and exit condition.
2. Inspect current tool, model, subagent, and host identifiers.
3. Store workspace agents in `.github/agents/<name>.agent.md`; default to
   workspace scope and `target: vscode` when host specificity matters.
4. Grant least privilege. Planning/audit roles receive read-only tools; editing
   or terminal tools require a stated job.
5. Set `user-invocable` and `disable-model-invocation` independently. Restrict
   `agents` and include the agent tool only when delegation is required.
6. Make handoffs reviewable with `send: false` by default. Verify every target.

## Rules

- Do not freeze a model name unless verified availability is part of the contract.
- Avoid duplicating repository instructions in the body; link to them.
- Keep agent frontmatter host-compatible. IDE-only `handoffs` and
  `argument-hint` can be ignored by other hosts.
- Never grant mutation just because a built-in agent normally has it.

Read [agent fields](references/artifact-contracts.md), use [role patterns](references/patterns.md), and run [verification](references/verification.md).

## Completion

The agent is discoverable in the intended host, hidden/invocable as designed,
cannot access excluded tools, every handoff resolves without auto-submission
unless approved, and artifact-based tests prove its positive and negative role boundaries.
