---
name: codex
description: Use when the user asks to run Codex CLI (codex exec, codex resume) or references OpenAI Codex for code analysis, refactoring, or automated editing. Uses GPT-5.5 by default for state-of-the-art software engineering.
---

# Codex Skill Guide

## Running a Task
1. Default to `gpt-5.5` model. Ask the user in the normal conversation which reasoning effort to use (`xhigh`, `high`, `medium`, or `low`). User can override model if needed (see Model Options below). If `gpt-5.5` is unavailable in your environment, fall back to `gpt-5.4`.
2. Select the sandbox mode required for the task; default to `--sandbox read-only` unless edits or network access are necessary.
3. Assemble the command with the appropriate options:
   - `-m, --model <MODEL>`
   - `--config model_reasoning_effort="<high|medium|low>"`
   - `--sandbox <read-only|workspace-write|danger-full-access>`
   - `-a never` before `exec` for non-interactive runs
   - `--output-last-message <FILE>` when a clean final response file is needed
   - `-C, --cd <DIR>`
   - `--skip-git-repo-check`
3. Always use --skip-git-repo-check.
4. When continuing a previous session, use `codex exec --skip-git-repo-check resume --last` via stdin. When resuming don't use any configuration flags unless explicitly requested by the user e.g. if he species the model or the reasoning effort when requesting to resume a session. Resume syntax: `echo "your prompt here" | codex exec --skip-git-repo-check resume --last 2>/dev/null`. All flags have to be inserted between exec and resume.
5. **IMPORTANT**: By default, append `2>/dev/null` to all `codex exec` commands to suppress thinking tokens (stderr). Only show stderr if the user explicitly requests to see thinking tokens or if debugging is needed.
6. Run the command, capture stdout/stderr (filtered as appropriate), and summarize the outcome for the user.
7. **After Codex completes**, inform the user: "You can resume this Codex session at any time by saying 'codex resume' or asking me to continue with additional analysis or changes."

### Quick Reference
| Use case | Sandbox mode | Key flags |
| --- | --- | --- |
| Non-blocking automated review or analysis | `workspace-write` | `codex -a never exec --sandbox workspace-write --output-last-message <file>` |
| Read-only review or analysis | `read-only` | `codex -a never exec --sandbox read-only --output-last-message <file>` |
| Apply local edits | `workspace-write` | `codex -a never exec --sandbox workspace-write` |
| Permit network or broad access | `danger-full-access` | `codex -a never exec --sandbox danger-full-access` |
| Resume recent session | Inherited from original | `echo "prompt" \| codex exec --skip-git-repo-check resume --last 2>/dev/null` (no flags allowed) |
| Run from another directory | Match task needs | `-C <DIR>` plus other flags `2>/dev/null` |

## Model Options

| Model | Best for | Notes |
| --- | --- | --- |
| `gpt-5.5` ⭐ | **Newest frontier (default)**: Complex coding, computer use, knowledge work, research workflows | Latest flagship. Available via ChatGPT sign-in and API auth (since 2026-04). Recommended starting point. |
| `gpt-5.4` | Flagship alternative for professional work | Available across all Codex platforms. Use as fallback when `gpt-5.5` is not in the picker. |
| `gpt-5.4-mini` | Fast, efficient mini model for responsive coding tasks and subagents | Lower-cost option for lighter workloads, sub-agents, cleanup tasks. |
| `gpt-5.3-codex` | Industry-leading coding model for complex software engineering | Powers GPT-5.4's coding abilities. Use when coding-specific quality is paramount. |
| `gpt-5.3-codex-spark` | Real-time coding iteration (text-only research preview) | ChatGPT Pro subscribers only. Optimized for near-instant coding iteration. |

**Selection guide**: Start with `gpt-5.5` for most tasks. Drop to `gpt-5.4` when 5.5 isn't available. Use `gpt-5.3-codex` when you need maximum coding quality without 5.5 reasoning overhead. Use `gpt-5.4-mini` for sub-agents and cleanup workloads.

> Verify exact context window / pricing on the official model card — values may shift as preview/stable status changes.

**Reasoning Effort Levels**:
- `xhigh` - Ultra-complex tasks (deep problem analysis, complex reasoning, deep understanding of the problem)
- `high` - Complex tasks (refactoring, architecture, security analysis, performance optimization)
- `medium` - Standard tasks (refactoring, code organization, feature additions, bug fixes)
- `low` - Simple tasks (quick fixes, simple changes, code formatting, documentation)

**Cached Input Discount**: Repeated context is heavily discounted with cache lasting up to 24 hours. Verify current rates on the official OpenAI pricing page.

## Following Up
- After every `codex` command, ask in the normal conversation when confirmation, clarification, or a resume decision is actually needed.
- When resuming, pipe the new prompt via stdin: `echo "new prompt" | codex exec resume --last 2>/dev/null`. The resumed session automatically uses the same model, reasoning effort, and sandbox mode from the original session.
- Restate the chosen model, reasoning effort, and sandbox mode when proposing follow-up actions.

## Error Handling
- Stop and report failures whenever `codex --version` or a `codex exec` command exits non-zero; request direction before retrying.
- Before you use high-impact flags (`--sandbox danger-full-access`, `--skip-git-repo-check`), ask the user in the normal conversation unless permission was already given.
- When output includes warnings or partial results, summarize them and ask in the normal conversation how to adjust.

## CLI Version

Requires a recent Codex CLI version for GPT-5.5 model support. Check version: `codex --version` and update with `npm install -g @openai/codex@latest` if needed. Use `/model` slash command within a session to switch, or set default in `~/.codex/config.toml`.

