---
description:  >
  Assists in the creation of a headless Claude Code batch script that runs an isolated micro-session per item
  (file, line, task) for ad-hoc automation such as bulk migrations, lint-fix loops, or doc generation.
disable-model-invocation: true
user-invocable: true
---

# Claude Code Headless Batch Setup

Your goal is to help the user assemble a small shell script that drives `claude -p` over many inputs,
running one ephemeral micro-session per item. The result usually lives under `.claude/headless/` and pairs
a driver script (`*.sh`) with a system prompt file (`*.md`) and potentially an input list file.

**Additional user arguments**: $ARGUMENTS

**Language hint**: Always create all generated script content and comments in English
for consistency across the codebase, while continuing to speak to the user in the language of their choice.

**Platform hint**: Instructions and templates assume a Linux host with GNU coreutils. Adapt to the detected user OS.
- macOS   — Substitute BSD equivalents for GNU-only utilities.
- Windows — Still use `.sh` files (skip irrelevant `chmod +x`), assuming Git Bash is available at runtime.

# Workflow

1. Ensure the user intent is clear. If user arguments are absent or ambiguous,
   especially regarding the [upcoming decisions](#decisions-to-make),
   elicit the necessary information via informal conversation with the user.
2. Advise the user on a sensible strategy using the [given background](#background-knowledge) as reference.
   Push back on choices that are likely to cause token usage escalation, contention, or silent failures.
3. Pick the best suited template and copy it to `.claude/headless/<descriptive-name>.sh` and `chmod +x` it.
   - [foreach-file.sh](./templates/foreach-file.sh) — one invocation per file matching a glob argument.
   - [foreach-line.sh](./templates/foreach-line.sh) — one invocation per line of stdin (PR numbers, IDs, URLs).
   - [foreach-task.sh](./templates/foreach-task.sh) — one invocation per unchecked item in a sibling checklist file.
     This is the most powerful driver script, capable of ingesting, tracking and resuming progress on arbitrary items.
     Use when the user wants to prepare and iterate on hand-curated task list (in this or a separate session).
   - [foreach-task-parallel.sh](./templates/foreach-task-parallel.sh) — same as `foreach-task.sh` but
     runs `BATCH_SIZE` tasks concurrently per batch. However, tasks with overlapping access scope will race.
     Check the assumptions block at the top of the script for compatibility before suggesting this option.
4. Copy the matching prompt template to `.claude/headless/<descriptive-name>.md`.
   - [foreach-file.md](./templates/foreach-file.md)
   - [foreach-line.md](./templates/foreach-line.md)
   - [foreach-task.md](./templates/foreach-task.md) (also used for the parallel variant)
   For task-based scripts, also create a task file based on [foreach-task.tasks.md](./templates/foreach-task.tasks.md).
   Tailor all of these files to the user's needs, falling back to interactive feedback as required.
5. Tune the parameters in the script such as `CLAUDE_ARGS` and `BATCH_SIZE` per the decisions below.
6. Review the generated content and flag relevant [pitfalls](#pitfalls) that apply to this setup.
7. Remind the user how to run the script from the current working directory,
   suggesting a test run on the first items (script can be aborted at any time using `Ctrl+C`).

## Decisions to Make

These are the variables that determine the right approach, as well as tweaks to the scripts and prompts.

- **Input shape** — File glob, lines on stdin, fixed custom checkbox-list file (resumable).
- **Per-item task** — Specific, mechanical description. What inputs, what outputs, when to exit without action.
- **Tool surface** — Smaller is cheaper, faster, safer. Whitelist (preferred) or blacklist.
  Common shapes: `Read,Grep,Glob` (analysis), `Read,Edit` (single-file rewrite), add `Write` only if needed.
- **Model** — `sonnet` for common tasks; `haiku` for simple tasks, `opus` only when reasoning genuinely demands it.
- **Turn cap** — Set `--max-turns` low (10-20 for mechanical edits, 30-50 for harder tasks).
- **Concurrency** — Sequential by default. Only `foreach-task-parallel.sh` allows parallel execution
                    when time is the larger constraint over cost control and concurrency conflicts are not an issue.
- **Run target** — Local dev workstation (OAuth works) vs. unattended/CI (needs `ANTHROPIC_API_KEY`).

---

# Background Knowledge

## Context Isolation

Each `claude -p` invocation is a fresh agent with no memory of the previous one.
The advantages: predictable cost, parallel-friendly, clean recovery from individual failures, no context contamination.
The trade-off: the agent cannot accumulate cross-item learning. Every item must be self-contained. If the task benefits
from cumulative context (exploring a codebase, building up a plan), headless batching is the wrong tool.

## Custom System Prompt

A headless run with `--system-prompt-file` is mechanically equivalent to a subagent invocation via the
`Agent` tool from the main session. Same isolated context, same custom prompt, same tool restrictions.
The difference is only the entry point: a shell driver iterating over items vs. a parent agent dispatching tasks.

The CLI docs make `--system-prompt` and `--system-prompt-file` sound drastic — as if they replace the entire
system prompt. They don't. Claude Code's system prompt is segmented and conditional.
The injected content only replaces the conversational/persona segments that govern how the agent talks to a user in
an interactive session. The structural parts — tool definitions, environment block, harness rules, hook
contracts, etc. — remain in place. This is exactly how subagents are configured.

## Permissions

Non-interactive `-p` mode cannot display permission dialogs, so the effective tool surface is determined entirely by
`permissions.allow` and `permissions.deny` settings, modified by the command arguments.
Permission directives are evaluated in the order **deny → ask → allow**, where `ask` equals `deny` when non-interactive.

The most important general command argument is `--permission-mode`:
- **`dontAsk`** (recommended for unattended runs) — Auto-denies anything not in `permissions.allow`
  or the built-in read-only whitelist for the `Bash` tool. Error messages explicitly inform agent of this mode.
- **`acceptEdits`** — Auto-allows *any* file edits and common filesystem `Bash` tool ops (`mkdir`, `mv`, `cp`).
- **`bypassPermissions`** (same as `--dangerously-skip-permissions`) — Skips checks entirely.
  Only use under strict isolation (container, worktree, throwaway environment).
- **`auto`** uses a security classifier model to decide — not recommended.
- **`plan`** exposes read-only tools but also some that control plan mode — not recommended.
- **`default`** effectively equivalent to `dontAsk` but with less explanatory error messages — not recommended.

The arguments `--allowedTools` and `--disallowedTools` act exactly as if their content was
added to `permissions.allow` / `permissions.deny` and also take the same syntax (comma separated).
Warning: Listing a bare tool name (e.g. `Bash`) as allowed will allow *every* invocation of the tool,
except for those listed explicitly as denied. Narrow with patterns like `Bash(git:*)` when possible.

Also note that `--allowedTools` must not be confused with `--tools`:
The latter controls which tools are *available* to the model but has no impact on per-invocation permission.
So `--tools` is an effective way to define a tool whitelist, but each must also be allowed to be invoked successfully.

The interaction between `--disallowedTools` and `--tools` is even more nuanced.
If a bare tool name is listed in `--disallowedTools` or the deny settings, it is removed from the *available* tools.
When only certain argument patterns of a tool are denied, the tool in general remains available.
So `--disallowedTools` is an effective way to define a tool blacklist when use of `--tools` is impractical.

## Agent Content Principles

When generating or reviewing content for `.md` prompt files, you are writing for other AI coding agents.
Follow these principles to optimally tailor your instructions and flag violations to the user:

- **Concise** — Minimize token usage. Prefer keywords and terse bullet points over prose.
- **Structured** — Use compact Markdown to delineate connected aspects.
- **Actionable** — Generate concrete operational directives, not abstract guidelines.
  A headless agent in particular has no one to ask for clarification. Be very prescriptive and leave no ambiguities.
  Clear exhaustive instructions further help reduce costs by facilitating execution by a cheaper model.
- **Referential** — Provide `@<path>` pointers to contextual code files that are relevant for all runs.
  This ensures these files are read deterministically and do not require Read tool calls by the model.
- **Scoped** — Consider which instructions are already ingested by the model via CLAUDE.md or path-based rules.
  Rules and agent instructions progressively disclose domain- and task-specific knowledge.
- **Durable** — Consider the projected lifetime of the generated content.
  For ad-hoc throw-away scripting, duplicating context and code information can save additional reads.
  For recurring batch tasks, only reference related code by path and search terms to avoid drift.


## Pitfalls

- **Cost blowup** — A large batch and many turns each item can very quickly drain rate limits or rack up API costs.
  Pilot first, monitor usage rate at the beginning; cap with `--max-turns` and optionally `--max-budget-usd`.
- **Context bloat** — A large CLAUDE.md, path rules, or many tools adds significant token cost to every micro-session.
- **MCP overhead** — Custom MCP servers start and tool schemas inject every session.
  To prevent this cost in execution time and tokens, substituting an empty `--mcp-config` is advisable if unneeded.
- **Harness applies** — Without `--bare`, project hooks, rules and CLAUDE.md still apply to each session.
  Instructions desired for interactive global scope sessions can have unexpected effects during batch processing
  (e.g. instructions to run test suites, automatically commit to git, update documentation...).
- **Concurrency** — Parallel runs share `.git/index.lock`, the working tree, and any project MCP state.
- **Idempotency** — If the driver script crashes or a second run with improved instructions becomes desirable,
  re-running will process items a second time, leading to overhead cost and potential unexpected behavior.
  Ensure the agent instructions are suitable to detect already processed items and exit or use the task driver script.
- **Authentication** — `--bare` ignores `CLAUDE_CODE_OAUTH_TOKEN` and the local developers OAuth login,
  so it requires `ANTHROPIC_API_KEY`, an equivalent cloud provider or `apiKeyHelper` in settings.

## References

- [Headless mode overview](https://docs.claude.com/en/docs/claude-code/headless)
- [CLI reference](https://docs.claude.com/en/docs/claude-code/cli-reference)
- [Permission Modes](https://code.claude.com/docs/en/permission-modes)
- [Claude Code System Prompt](https://www.dbreunig.com/2026/04/04/how-claude-code-builds-a-system-prompt.html)
