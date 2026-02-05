---
name: github-kernel
description: foundational definitions for GitHub skills, safety rules, tool escalation, and security boundaries
---

## What is it?

The **GitHub Kernel** is the foundational skill that defines the "laws of physics" for all other GitHub capability skills. It provides the central source of truth for:

- Tool selection strategy (Escalation Ladder).
- Safety boundaries and non-negotiable rules.
- Conventions for interactions with the GitHub platform.
- Mapping of abstract capabilities to concrete MCP tools.

## Success Criteria
- Foundational rules are applied across all other GitHub skills.
- The Tool Escalation Ladder is followed consistently.
- Safety rules for destructive operations are respected.
- Interaction conventions (naming, commits) are maintained.

## When to use this skill

- Consult this skill for **foundational knowledge** when initializing a GitHub-related session.
- Refer to this skill whenever you are unsure about which tool to use (MCP vs. CLI vs. API).
- Consult this skill to check if an action is considered "safe" or requires user confirmation.

## What this skill can do

- Explain the [Tool Escalation Ladder](references/TOOL_ESCALATION.md).
- Define [Safety Rules](references/SAFETY_RULES.md) for destructive operations.
- Map capabilities to specific [MCP Tools](references/MCP_TOOL_MAP.md).
- Establish consistent conventions for branch naming, commit messages, and PR titles (see [CONVENTIONAL_COMMITS.md](references/CONVENTIONAL_COMMITS.md)).

## What this skill will NOT do

- **Execute any GitHub actions.** This skill is purely informational.
- Create issues or PRs.
- Modify repository state.
- Interact with the API directly.

## How to use this skill

This skill is a **passive reference**.

1. **Read** the reference documents to understand the operating parameters.
2. **Apply** the rules when executing other skills like `github-issues` or `github-pr-flow`.

## Tool usage rules

All GitHub skills must adhere to the **Escalation Ladder**:

1. **Primary**: Use **GitHub MCP Tools** (fast, safe, context-aware).
2. **Fallback**: Use **`gh` CLI** (if MCP is missing/broken).
3. **Last Resort**: Use **REST API** (only for edge cases like metadata fields).

See [TOOL_ESCALATION.md](references/TOOL_ESCALATION.md) for detailed logic.

## Examples

### Determining Tool Safety

> "I need to delete a file. Is this safe?"
> _Check `SAFETY_RULES.md` -> Destructive operation -> Requires explicit confirmation._

### Selecting the Right Tool

> "I need to comment on an issue."
> _Check `MCP_TOOL_MAP.md` -> `add_issue_comment` is available -> Use MCP._

## Limitations

- Does not enforce rules programmatically; agents must voluntarily adhere to these guidelines.
- Does not contain specific workflow logic for complex tasks (like "release management").
