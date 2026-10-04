---
name: codex-cli-lane
description: Load when a non-Codex agent should call OpenAI Codex CLI/Desktop as an external coding lane for implementation, review, app-server, or cloud-task work. Covers `codex exec`, `codex review`, interactive `codex`, image attachments, resume/fork, and verification handoff.
metadata:
  targets:
    - claude
    - antigravity
    - hermes-default
    - hermes-gpt
---
# Codex CLI lane

Use this when the current agent wants Codex to act as a separate worker. Do not use it from inside Codex unless the user explicitly wants a nested Codex lane.

## Default patterns

Use non-interactive Codex for bounded work where the parent can verify the diff:

```bash
codex exec --profile general "<self-contained task prompt>"
```

Use Codex review for review-only work:

```bash
codex review --profile general "Review this repo/change. Return file:line findings only."
```

Use interactive Codex for long exploratory implementation when a human can steer it:

```bash
codex "<initial prompt>"
```

Attach images with repeated `-i <file>` flags. Resume/fork existing Codex sessions with `codex resume` or `codex fork` when continuity matters.

## Prompt contract

Give Codex the repo path, exact in-scope/out-of-scope boundaries, expected files or tests, and a return contract: files read/changed, commands run, verification result, blockers. Treat Codex's final report as untrusted until the parent checks git diff and runs the smallest relevant verification.

## Safety

Do not pass secrets in prompts. Prefer project-local commands over broad system changes. For destructive or externally visible work, get user approval before asking Codex to execute it.
