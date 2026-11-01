---
name: writing-rules
description: Create, inspect or update Hookify project rules for inputs, tool calls and completion checks.
---

# Hookify project rules

Rules live in the current Workspace at `.nosis/hookify.<name>.json`. Read existing
rules before editing. Use the ordinary Nosis file tools to create or update rules;
creating a rule does not bypass their permissions. Each hook reads rules again,
so rule edits apply to the next checkpoint without a runtime refresh.

Required fields: `name`, `event`, `conditions`, `message`. Optional: `enabled`
(default true), `action` (`warn` by default, or `block`), and `tools` (exact names).
Events: `InputSubmitted`, `PreToolUse`, `PostToolUse`, `Stop`. PostToolUse supports
warnings only because the tool has already executed.

Each condition has `field`, `operator`, `value`; all conditions must match.
Operators: `equals`, `regex_match`, `contains`, `not_contains`.
Use Nosis paths such as `tool_call.arguments.path`, `tool_call.arguments.content`,
`tool_call.arguments.new_text`, `tool_call.arguments.patch`,
`tool_call.arguments.command`, `input.text`, or `response`.
At Stop, the boolean field `tests_passed` checks current-turn execution facts:
a recognized test command must have completed with exit code zero, without timing out.
A background submission handle, transcript mention, or a previous turn does not count.
This checks successful command completion, not test coverage or the contents of a test suite.

Inspect `examples/` in this skill's plugin root for complete rule files.
To analyze conversation patterns, delegate to `repo-review-kit:conversation-analyzer` and
include the relevant conversation excerpts explicitly in its task.
