---
name: comment-budget
description: This skill should be used when the user asks to "enforce a comment budget",
  "prevent overcommenting", or modify comment-budget policy. Its hooks are automatic.
---

# comment-budget

This plugin enforces comment discipline via three hooks:

- **SessionStart**: injects the full comment doctrine into context
- **UserPromptSubmit**: resets per-prompt counters and emits a short reminder
- **PreToolUse** (Edit/Write/MultiEdit): deterministic gate that denies editor writes containing banned comment patterns (changelog/provenance graffiti, step banners, external pointers, long comment blocks).

The lexical gate intentionally does not judge semantic redundancy, narration inside Python docstring bodies, or arbitrary Bash-generated writes; the preflight doctrine covers those cases.

No skill invocation needed — the hooks run automatically.

After modifying this plugin, run `/reload-plugins` before evaluating hook behavior. Reloading picks up hook changes without restarting, but it does not emit SessionStart; trigger startup, resume, clear, compact, or fork when testing doctrine injection.
