---
name: codex-execpolicy
description: Create or edit Codex execpolicy .rules files (allow/prompt/forbid commands, define prefix_rule patterns, add match/not_match tests) and validate them with codex execpolicy check. Use when a user mentions Codex rules, execpolicy, command policies, allowlists/denylists, or controlling which commands Codex can run, and when scope (global vs project) must be clarified.
---

# Codex Execpolicy

## Overview

Define and maintain Codex execpolicy rules so the agent can allow, prompt, or forbid command prefixes, and validate the policy before use.

## Workflow

1. Clarify scope and location.
   - Ask: “Should this be a global rule or project-specific?”
   - If global: default to `~/.codex/rules/default.rules` unless the user provides another path or uses a different Codex home.
   - If project-specific: ask for the exact file path; a common pattern is `.codex/rules/default.rules` at repo root.
   - If the file already exists, inspect it before editing.

2. Clarify intent.
   - Ask for the decision: `allow`, `prompt`, or `forbidden`.
   - Ask for the command prefix and any alternatives.
   - Ask for at least one “should match” and “should not match” example if the rule is non-trivial.

3. Implement the rule.
   - Use `prefix_rule(...)` with a precise `pattern` list.
   - Use union lists for alternatives when only one argument varies.
   - Add `match` / `not_match` as inline tests when the rule is tricky.

4. Validate before finishing.
   - Run `codex execpolicy check --pretty --rules <path> -- <command>` using realistic examples.
   - If validation fails, adjust `pattern` or tests and re-check.

5. Summarize outcomes.
   - State what command prefixes are allowed/prompted/blocked and where the rule lives.

## Examples

Block all git commands:

```starlark
prefix_rule(
  pattern = ["git"],
  decision = "forbidden",
)
```

Prompt for either `gh pr view` or `gh pr list`:

```starlark
prefix_rule(
  pattern = ["gh", "pr", ["view", "list"]],
  decision = "prompt",
)
```

## Resources

- See `references/execpolicy.md` for syntax notes, decision precedence, and validation commands.
