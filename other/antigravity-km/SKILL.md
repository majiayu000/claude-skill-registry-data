---
name: antigravity
description: Load when an agent should call Google Antigravity CLI (`agy`) as an external agent lane for quick coding, research, UI/helper tasks, Gemini-style agent work, or migration from Gemini CLI. Covers `agy -p`, `agy -i`, continuing conversations, sandbox/permissions, and skill visibility.
metadata:
  targets:
    - codex
    - claude
    - hermes-default
    - hermes-gpt
---
# Antigravity CLI lane

Use this when the current agent wants Antigravity (`agy`) to act as a lightweight external worker.

## Local shape

- Binary: `~/.local/bin/agy`
- Auth is expected to work silently for Kosta's Google account.
- State root: `~/.gemini/antigravity-cli/`
- Skillshare target: `~/.gemini/antigravity/skills/`

## Default patterns

```bash
# One-shot / noninteractive
agy -p "<self-contained task prompt>"

# Interactive session with initial prompt
agy -i "<task prompt>"

# Continue most recent conversation for this cwd
agy --continue -p "Continue from where we left off: <next instruction>"

# Resume exact conversation
agy --conversation <conversation-id> -p "<next instruction>"

# Add another workspace root
agy --add-dir ~/LocalDev/some-repo -p "<task prompt>"
```

Use `--sandbox` when the lane should investigate safely. Use `--dangerously-skip-permissions` only when Kosta explicitly wants high-autonomy/YOLO behavior in a bounded workspace.

`--print-timeout` is a duration flag, not the prompt. Put the prompt after `-p` / `--print`.

## Fit

Good for quick run-and-done helper tasks, Gemini-flavored research, visual/UI helper passes, and independent implementation spikes. For architecture/adversarial review, Claude usually wins. For careful backend implementation and release mechanics, Codex usually wins.

Do not assume `agy -p` can attach local image paths; use Antigravity IDE or SDK paths for image-heavy work unless CLI image syntax has been verified live.
