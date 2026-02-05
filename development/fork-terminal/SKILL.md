---
name: fork-terminal
description: Spawn new terminal windows to run Claude Code, Gemini CLI, or raw CLI commands in parallel. Use when the user wants to fork a task, spawn an agent, run parallel work, delegate a task to a new terminal, or mentions "fork", "spawn", "new terminal", "parallel agent".
---

# Fork Terminal Skill

Spawn new terminal windows to run AI agents or CLI commands in parallel sessions.
Enables "out-of-loop" agentic coding where forked agents handle routine tasks independently.

## Variables

```yaml
# Feature Flags
enable_gemini_cli: false          # Set to true to enable Gemini CLI support
enable_raw_cli: true              # Enable raw CLI command execution
auto_context_handoff: true        # Automatically pass context summary
capture_output: true              # Save output to logs/forks/

# Defaults
default_model: sonnet             # haiku | sonnet | opus

# Model Mapping
model_haiku: claude-3-5-haiku-20241022
model_sonnet: claude-sonnet-4-20250514
model_opus: claude-opus-4-20250514
```

## When to Use

Activate this skill when the user:
- Says "fork", "spawn agent", "run in new terminal", "delegate", "parallel"
- Wants to run Claude Code or Gemini in a separate session
- Needs parallel work on different tasks
- Mentions "new window", "background task", "separate agent"
- Wants to delegate routine tasks (bug fixes, tests, research)

## Quick Reference (Natural Language)

| User Says | What Happens |
|-----------|--------------|
| "Fork a Claude agent to [task]" | Spawn Claude Code agent with task |
| "Fork Gemini to [task]" | Spawn Gemini CLI (if enabled) |
| "Fork a raw terminal to run [command]" | Run CLI command in new terminal |
| "Show fork status" | Show running/completed tasks |
| "List all forked tasks" | List all tracked forks |
| "Kill fork [id]" | Terminate a running fork |
| "Kill all forks" | Terminate all running forks |
| "Fork a bugfix agent for [desc]" | Preset: spawn bugfix agent |
| "Fork a research agent to explore [topic]" | Preset: spawn research agent |
| "Fork to run tests" | Preset: run and fix tests |
| "Fork a review agent" | Preset: code review agent |

## Flags

All commands support these flags:

| Flag | Purpose |
|------|---------|
| `--model haiku\|sonnet\|opus` | Select model tier |
| `--with-context` | Pass condensed context summary to forked agent |
| `--worktree` | Create git worktree for isolation |
| `--no-output` | Don't capture output to logs |
| `--skip-permissions` | Add --dangerously-skip-permissions (trusted automation) |
| `--new-window` | Force new window instead of tab (Windows Terminal only) |

## Instructions

### Step 1: Parse Request

Determine the fork type from user's message:

1. **Check for preset names first:**
   - "bugfix", "research", "tests", "review" → Route to preset handling
   - Read `cookbook/presets.md` for preset configuration

2. **Determine fork type:**
   - Mentions "claude", "code", or no specific CLI → Claude Code fork
   - Mentions "gemini" AND `enable_gemini_cli=true` → Gemini CLI fork
   - Mentions "raw", "cli", "command", "run" → Raw CLI fork
   - Mentions "status", "list", "kill" → Management command (no spawn)

3. **Extract the task:**
   - The task is whatever the user wants the forked agent to do
   - Be specific and actionable

### Step 2: Handle Management Commands

If request is a management command (status, list, kill):

**For "show fork status":**
```bash
uv run tools/task_registry.py status
```

**For "list forked tasks":**
```bash
uv run tools/task_registry.py list
```

**For "kill fork [id]":**
```bash
uv run tools/task_registry.py update --id <id> --status failed --notes "Manually killed"
```
Note: This marks the task as failed but doesn't actually terminate the terminal.
Inform user they may need to close the terminal manually.

**For "kill all forks":**
```bash
uv run tools/task_registry.py clear --status running
```

Skip remaining steps for management commands.

### Step 3: Parse Flags

Extract flags from the request:

| If user says... | Flag |
|-----------------|------|
| "--model X" or "use X model" | `--model X` |
| "--with-context" or "pass context" or "include context" | `--with-context` |
| "--worktree" or "use worktree" or "isolate" | `--worktree` |
| "--no-output" or "no logs" | `--no-output` |
| "skip permissions" or "trusted" | `--skip-permissions` |

### Step 4: Context Handoff (if --with-context)

If context handoff is requested:

1. **Read the fork summary user prompt:**
   Read `prompts/fork_summary_user_prompt.md` to understand how to generate a summary.

2. **Generate a condensed context summary:**
   Following the prompt's instructions, create a summary including:
   - The delegated task (most important)
   - What you've been working on
   - Key files touched
   - Important decisions made
   - Current state/blockers

3. **Save the context:**
   ```bash
   uv run tools/context_builder.py --task "<delegated task>" --context "<background>" --files <file1> <file2>
   ```

4. **Note the context file path** for passing to fork_terminal.py

### Step 5: Create Worktree (if --worktree)

If worktree isolation is requested:

1. **Read worktree guide:**
   Read `cookbook/worktree-guide.md` for patterns.

2. **Create worktree:**
   ```bash
   uv run tools/worktree_manager.py create --branch fork/<task-name> --task "<task>"
   ```

3. **Note the worktree path** - use it as the CWD for fork_terminal.py

### Step 6: Execute Fork

Run the fork terminal script:

```bash
uv run tools/fork_terminal.py \
  --type <claude|gemini|raw> \
  --task "<task>" \
  --model <haiku|sonnet|opus> \
  --cwd "<working-directory>" \
  [--with-context <context-file>] \
  [--no-output] \
  [--skip-permissions]
```

### Step 7: Register Task

The fork_terminal.py script returns a JSON result. Extract the task_id and register it:

```bash
uv run tools/task_registry.py add \
  --id <task_id> \
  --task "<task>" \
  --type <claude|gemini|raw> \
  --model <model> \
  --cwd "<cwd>" \
  --output-file "<output-file>" \
  [--context-file "<context-file>"] \
  [--preset "<preset-name>"]
```

### Step 8: Confirm to User

Report back to the user:

1. **Task ID** for tracking
2. **Command** being executed
3. **Output location** if capturing
4. **How to check status** (say "show fork status")

Example confirmation:
```
Forked Claude Code agent (task: abc123)
- Task: Fix the null pointer in user.email validation
- Model: sonnet
- Working directory: C:\project
- Output: logs/forks/2024-12-27_fix-null-pointer_abc123.md

Say "show fork status" or "list forked tasks" to check progress.
```

## Progressive Disclosure

### If fork type is Claude Code:
Read `cookbook/claude-code.md` for Claude CLI flags, patterns, and best practices.

### If fork type is Gemini CLI:
Read `cookbook/gemini-cli.md` for Gemini CLI usage.
Note: Only available if `enable_gemini_cli=true` in variables.

### If using a preset:
Read `cookbook/presets.md` and apply the matching preset configuration.
Presets define model tier, context settings, and task templates.

### If --worktree flag used:
Read `cookbook/worktree-guide.md` for worktree creation and management.

## Error Handling

| Error | Action |
|-------|--------|
| Windows Terminal not found | Fall back to PowerShell (automatic) |
| Task fails to spawn | Report error, don't register task |
| Output capture fails | Continue without capture, warn user |
| Git worktree creation fails | Abort, report error to user |
| Not in git repo (worktree) | Inform user worktree requires git repo |
| Gemini CLI requested but disabled | Inform user to enable in variables |

## Key Principles

From IndyDevDan's agentic coding philosophy:

1. **Fresh context windows are essential** - Forked agents start clean, avoiding context pollution
2. **In-loop vs Out-of-loop** - Complex work = in-loop (current session); routine tasks = out-of-loop (forked)
3. **Simple solutions are better** - Don't over-engineer the fork; let the agent figure things out
4. **Eliminate confusion** - Be specific about what the forked agent should do
5. **There's no reason to manually fix small bugs** when agents can handle them out-of-loop

## Files Reference

| File | Purpose |
|------|---------|
| `tools/fork_terminal.py` | Core cross-platform terminal spawning |
| `tools/task_registry.py` | Track running/completed tasks |
| `tools/context_builder.py` | Build context handoff files |
| `tools/worktree_manager.py` | Git worktree management |
| `prompts/fork_summary_user_prompt.md` | How to generate context summary |
| `prompts/fork-summary.md` | Template forked agent receives |
| `cookbook/claude-code.md` | Claude CLI reference |
| `cookbook/presets.md` | Preset definitions |
| `cookbook/worktree-guide.md` | Worktree patterns |
| `data/forked-tasks.json` | Task registry (auto-created) |
| `logs/forks/` | Output logs from forked agents |
