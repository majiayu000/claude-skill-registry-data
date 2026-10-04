---
name: speed-line-delivery
description: Deliver terminal instructions with shell-labeled lanes and one-line command blocks so users can execute quickly without context confusion. Use when users are working across multiple terminals, mixing chat and shell actions, hitting PowerShell parsing errors, or asking to learn while still completing setup/ops tasks fast.
---

# Speed Line Delivery

## Overview

Run command coaching with minimal ambiguity.
Label every command with an execution lane and provide one copy-paste line at a time.

## Workflow

### Step 1: Declare lanes first

Declare active lanes before giving commands:
1. `[CHAT]` for setup/config/git.
2. `[SERVER]` for long-running services.
3. `[OPS]` for API calls/tests.

If only one terminal is used, map all commands to `[CHAT]`.

### Step 2: Use speed-line command format

For each step, output exactly:
1. Objective: one short sentence.
2. Lane: one of `[CHAT]`, `[SERVER]`, `[OPS]`.
3. Command: one line only in a fenced code block.
4. Success signal: one line describing expected output.

Never split command flags onto a second line unless explicitly teaching multiline syntax.

### Step 3: Enforce one-line copy/paste discipline

Use these rules:
1. Put full command on one line.
2. Quote paths with spaces.
3. Use `$repo = "C:\\path"` once, then reuse variable.
4. Avoid trailing prose on command lines.
5. Do not prepend command with conversational text.

### Step 4: Recover from parse/context errors fast

If user gets parse errors or wrong working directory:
1. Re-anchor directory first: `cd <repo>`.
2. Reissue the same command as a single line.
3. If command was line-wrapped, replace with variable form.
4. Ask for exact terminal output after each command before giving next.

### Step 5: Keep learning active while shipping

When user asks to learn and move quickly:
1. Give command first.
2. Add one-line explanation after success signal.
3. Move to next command immediately.

### Step 6: Use standard response template

Use this template:

```text
Objective: <what this step does>
Lane: [CHAT|SERVER|OPS]
Command:
<single-line command>
Success signal: <what user should see>
```

## References

1. Quick command patterns: `references/command-patterns.md`
