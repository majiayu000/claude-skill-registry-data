---
name: github-copilot-hooks
description: >-
  Use for creating, reviewing, debugging, or testing GitHub Copilot agent hooks in Visual Studio Code, including .github/hooks JSON, lifecycle events, Python handlers, permissions, and structured stdin/stdout. Do not use for advisory instructions, one-off commands, CI workflows, or shell profile hooks.
argument-hint: "[lifecycle event, enforced behavior, platforms, and failure policy]"
---

# GitHub Copilot hooks

Hooks are preview functionality and execute with VS Code's permissions. Use
them only when behavior must execute deterministically at an agent lifecycle
event. Inspect the installed version and active hook schema before authoring.

## Workflow

1. Inspect the active host's hook schema, policies, event payload, extension
   platform, and Agent Debug Logs.
2. Choose the narrowest event: `SessionStart`, `UserPromptSubmit`, `PreToolUse`,
   `PostToolUse`, `PreCompact`, `SubagentStart`, `SubagentStop`, or `Stop`.
3. Put workspace configuration in `.github/hooks/<purpose>.json`. Use a narrow
   Python 3.11+ handler when input-dependent logic is required.
4. Read one JSON object from stdin; validate event name and required fields;
   treat prompts and tool inputs as untrusted data.
5. Emit only documented JSON to stdout. Put diagnostics on stderr, bound runtime
   with a timeout, and choose fail-open/fail-closed behavior explicitly.
6. Test synthetic allow, deny, malformed, unrelated-tool, and timeout payloads
   before enabling the hook.

## Rules

- Do not interpolate untrusted hook fields into a shell command.
- Do not hardcode credentials or parse the unstable transcript format when a
  documented input field suffices.
- Do not rely on matcher filtering across hosts; validate `tool_name` yourself.
- Use `PreToolUse` for a single permission decision; reserve session stopping
  for a genuine session-wide condition.
- Never enable or distribute a hook without making its executable behavior visible.

Read [events and results](references/artifact-contracts.md), use [safe handler
patterns](references/patterns.md), and run [verification](references/verification.md).

## Completion

JSON parses, the handler is injection-safe and bounded, all branches have
offline tests, platform commands are explicit, no secret is stored, preview
status is stated, and a separately authorized VS Code smoke confirms the event.
