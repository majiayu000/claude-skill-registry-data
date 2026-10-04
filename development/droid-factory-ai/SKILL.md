---
description: Use when delegating a self-contained coding task to Factory AI's Droid CLI is a better fit than native subagents, especially for alternate models, isolated git worktrees, adjustable autonomy, or Droid multi-agent missions. Do not use when the task depends on Codex-local tools, memory, or rich session context.
metadata:
    targets:
        - antigravity
name: droid_Factory_AI
---
# Droid — Factory AI Coding Agent

Delegate coding and analysis tasks to Droid (`/Users/kosta/.local/bin/droid`) when its strengths outweigh native Craft Agent subagents.

## When to Use Droid vs Native Subagents

| Use Droid | Use Native (Claude Code / spawn_session) |
|---|---|
| Want GPT-5.x Codex or Gemini for a coding task | Task needs Craft Agent sources (gog, bird, mem0, MCP) |
| Self-contained coding job, no Craft Agent context needed | Need the spec + quality review cycle (SDD skill) |
| Want built-in git worktree isolation (`--worktree`) | Task is small (<5 tool calls, do it yourself) |
| Running a multi-agent "mission" for a large refactor | Need inline streaming results in conversation |
| Want read-only codebase analysis with zero risk (default mode) | Need MCP server access or browser tools |
| Need fine-grained autonomy control (4 tiers) | Need cross-source orchestration |

**Do NOT use Droid when:** the task requires Craft Agent context (sources, skills, labels, automations, session state).

## Quick Reference

```bash
# Basic (default model = GPT-5.4 Medium, read-only)
droid exec "Analyze this codebase for security issues" --output-format json --cwd /path/to/repo

# With autonomy for dev work
droid exec --auto medium "Fix the failing tests in src/auth" --output-format json --cwd /path/to/repo

# Different model
droid exec -m "custom:GPT-5.3-Spark-(High)-8" "Implement the feature" --output-format json --auto medium --cwd /path

# Git worktree isolation (CANNOT combine with --cwd)
cd /path/to/repo && droid exec --worktree --branch feat-name "Implement X" --output-format json --auto medium

# Multi-agent mission (requires --auto high or --skip-permissions-unsafe)
droid exec --mission --auto high "Build a complete auth system" --output-format json --cwd /path

# Resume a session
droid exec -s SESSION_ID "Follow-up instruction" --output-format json

# File input (long prompts)
droid exec -f /path/to/prompt.md --output-format json --auto medium --cwd /path

# Pipe input
echo "What does this code do?" | droid exec --output-format json --cwd /path

# Tool filtering (limit what Droid can use)
droid exec --enabled-tools "Read,Execute" "Read and explain this file" --output-format json

# Session tagging
droid exec --tag "craft-agent" --tag '{"name":"task","metadata":{"source":"skill"}}' "Do X" --output-format json
```

## Models — ALL via vibeproxy (localhost:8317)

**CRITICAL:** NEVER use native Droid model IDs (`claude-opus-4-6`, `gpt-5.4`, `gemini-3.1-pro`, etc.). ALL models MUST use the `custom:` prefixed vibeproxy IDs below. Native IDs are blocked by org policy and will fail or use wrong billing.

**Default behavior:** When no `-m` flag is passed, Droid uses `custom:GPT-5.4-(Medium)-2` (configured in `~/.factory/settings.json` as `sessionDefaultSettings.model`). This is a good general-purpose default — only override when you have a reason.

### GPT-5.4 (Flagship — best general coding)

| Display Name | Custom ID | Reasoning | Use When |
|---|---|---|---|
| GPT-5.4 (Default) | `custom:GPT-5.4-(Default)-0` | None | Quick tasks, no thinking needed |
| GPT-5.4 (Low) | `custom:GPT-5.4-(Low)-1` | Low | Light reasoning, fast |
| **GPT-5.4 (Medium)** | `custom:GPT-5.4-(Medium)-2` | Medium | **SESSION DEFAULT — general coding** |
| GPT-5.4 (High) | `custom:GPT-5.4-(High)-3` | High | Complex multi-step reasoning |
| GPT-5.4 (xHigh) | `custom:GPT-5.4-(xHigh)-4` | Max | Hardest problems, validation, spec mode |

### GPT-5.3 Spark (Codex — fast, code-optimized)

| Display Name | Custom ID | Reasoning | Use When |
|---|---|---|---|
| GPT-5.3 Spark (Default) | `custom:GPT-5.3-Spark-(Default)-5` | None | Quick code gen, boilerplate |
| GPT-5.3 Spark (Low) | `custom:GPT-5.3-Spark-(Low)-6` | Low | Fast iteration, small fixes |
| GPT-5.3 Spark (Medium) | `custom:GPT-5.3-Spark-(Medium)-7` | Medium | Balanced code tasks |
| GPT-5.3 Spark (High) | `custom:GPT-5.3-Spark-(High)-8` | High | Quality code with reasoning |
| GPT-5.3 Spark (xHigh) | `custom:GPT-5.3-Spark-(xHigh)-9` | Max | Deep code reasoning |

### Claude (via vibeproxy — CURRENTLY BROKEN)

| Display Name | Custom ID | Status |
|---|---|---|
| Claude Opus 4.6 | `custom:Claude-Opus-4.6-10` | **FAILS** — use native Craft Agent subagents instead |
| Claude Sonnet 4.6 | `custom:Claude-Sonnet-4.6-11` | **FAILS** — use native Craft Agent subagents instead |
| Claude Opus 4.5 | `custom:Claude-Opus-4.5-12` | **FAILS** — use native Craft Agent subagents instead |
| Claude Haiku 4.5 | `custom:Claude-Haiku-4.5-13` | **FAILS** — use native Craft Agent subagents instead |

> Claude models through Droid+vibeproxy currently return "Exec failed". For any Claude-based work, use Craft Agent's native subagents (Agent tool, spawn_session, call_llm). Periodically re-test — this may get fixed.

### Gemini (via vibeproxy)

| Display Name | Custom ID | Reasoning | Use When |
|---|---|---|---|
| Gemini 3.1 Pro (Low) | `custom:Gemini-3.1-Pro-(Low)-14` | Low | Quick Gemini tasks, large context |
| Gemini 3.1 Pro (High) | `custom:Gemini-3.1-Pro-(High)-15` | High | Complex Gemini tasks, long docs |

### Model Selection Guide

| Task Type | Recommended Model | Why |
|---|---|---|
| General coding (default) | GPT-5.4 Medium (no `-m` needed) | Best all-around, session default |
| Fast iteration / small fixes | GPT-5.3 Spark Medium or Low | Code-optimized, faster |
| Hard problems / architecture | GPT-5.4 High or xHigh | More thinking budget |
| Spec validation / review | GPT-5.4 xHigh | Maximum reasoning for correctness |
| Large context / long docs | Gemini 3.1 Pro High | Gemini's context window advantage |
| Claude-quality reasoning | **Don't use Droid** — use native Craft Agent subagents | Claude via vibeproxy is broken |

## Autonomy Levels

| Level | Flag | What's Allowed | Use When |
|---|---|---|---|
| **Read-only** | *(default, no flag)* | Read files, git status/log/diff, ls, info gathering | Analysis, code review, security audit |
| **Low** | `--auto low` | + File creation/modification (non-system dirs) | Docs, comments, formatting |
| **Medium** | `--auto medium` | + npm/pip install, curl, git commit, builds | **Standard dev work** |
| **High** | `--auto high` | + git push, deployments, arbitrary code execution | CI/CD, deployment (user must explicitly request) |

**Default to read-only or `--auto medium`.** Only use `--auto high` when the user explicitly asks for push/deploy operations.

## Output Formats

| Format | Flag | Use When |
|---|---|---|
| **JSON** | `--output-format json` | **Always use this** — structured, parseable |
| Text | `--output-format text` | Simple one-line answers only |
| Stream JSON | `--output-format stream-json` | Debugging / monitoring tool calls in detail |

### JSON Output Structure

```json
{
  "type": "result",
  "subtype": "success",       // or "failure"
  "is_error": false,          // true on failure
  "duration_ms": 27442,
  "num_turns": 4,
  "result": "...",            // May be EMPTY when Droid uses tools (files, commands)
  "session_id": "uuid",      // Save this for session resume
  "usage": {
    "input_tokens": 57392,
    "output_tokens": 771,
    "thinking_tokens": 136
  }
}
```

**CRITICAL:** The `result` field is often **empty** when Droid performs tool actions (creating files, running commands). This is normal — the work was done, the files exist. Always verify by checking the filesystem or git status after tool-using tasks.

## Edge Cases & Gotchas

1. **`--worktree` and `--cwd` cannot be combined** — use `cd` into the repo first, then `--worktree`
2. **Bad model IDs produce no output** (exit code 1, no JSON) — always use verified custom IDs
3. **Bad `--cwd` paths give non-JSON errors** (ENOENT on stderr, exit code 1)
4. **Exit codes:** 0 = success, 1 = failure — check `$?` for quick validation
5. **Worktree output wraps JSON** — worktree creation/preservation messages appear outside the JSON on stdout
6. **Session resume requires a new prompt** — `--session-id` loads history but needs new input
7. **Droid invokes its own skills** (Using Superpowers, Brainstorming) which add overhead for simple tasks — for quick tasks, consider using `--enabled-tools` to limit scope

## Patterns for Craft Agent Integration

### Simple Dispatch (Most Common)
```bash
RESULT=$(droid exec --auto medium "Your task here" --output-format json --cwd /path/to/repo 2>&1)
echo "$RESULT" | python3 -c "import json,sys; d=json.load(sys.stdin); print('Session:', d.get('session_id','?')); print('Success:', not d.get('is_error',True)); print('Result:', d.get('result','(tool actions performed)'))"
```

### Long Task with Monitoring
For tasks expected to take >60 seconds, use stream-json to monitor progress:
```bash
droid exec --auto medium "Complex refactoring task" --output-format stream-json --cwd /path 2>&1 | while IFS= read -r line; do
  echo "$line" | python3 -c "import json,sys; d=json.load(sys.stdin); t=d.get('type',''); print(f'[{t}]', d.get('toolName','') or d.get('text','')[:80] if t in ('tool_call','message') else '')" 2>/dev/null
done
```

### Session Continuity
Save the session_id from the first call, pass it back for follow-ups:
```bash
# First call
SID=$(droid exec --auto medium "Start implementing feature X" --output-format json --cwd /path 2>&1 | python3 -c "import json,sys; print(json.load(sys.stdin).get('session_id',''))")
# Follow-up
droid exec -s "$SID" "Now add tests for what you just built" --output-format json --auto medium 2>&1
```

### Worktree Isolation
```bash
cd /path/to/repo
droid exec --worktree --branch feat-my-feature --auto medium "Implement the feature described in SPEC.md" --output-format json 2>&1
# Worktree is at /path/to/repo-wt-feat-my-feature (preserved if changes were made)
```

### Search Past Sessions
```bash
droid search "keyword" --json --limit-sessions 5
```

## Mission Mode (Multi-Agent)

Missions spawn parallel worker sessions for large tasks. **Only use for substantial multi-file work.**

```bash
droid exec --mission --auto high "Build a complete REST API with auth, CRUD, and tests" --output-format json --cwd /path
```

- Default worker model: GPT-5.4 Medium
- Default validation model: Claude Opus 4.6
- These are configured in `~/.factory/settings.json` under `missionModelSettings`
- Missions are stored in `~/.factory/missions/`

## Droid's Own Ecosystem

Droid has its own subagents ("droids"), skills, plugins, and MCP servers configured at `~/.factory/`. Notable custom droids: `code-reviewer`, `debugger`, `correctness-bug-hunter`, `refactor-safety-auditor`, `worker`. These are automatically used by Droid when relevant — you don't need to invoke them manually.

## Decision Flowchart

```
Is this a coding/analysis task? ──no──> Use Craft Agent normally
         │yes
Does it need Craft Agent sources/context? ──yes──> Use native subagents
         │no
Do you want a non-Claude model (GPT-5.x, Gemini)? ──yes──> Use Droid
         │no
Is it a large multi-file refactor? ──yes──> Use Droid --mission
         │no
Do you want guaranteed worktree isolation? ──yes──> Use Droid --worktree
         │no
Is it read-only analysis with zero risk? ──yes──> Use Droid (default mode)
         │no
Use native Craft Agent subagents (simpler, integrated)
```
