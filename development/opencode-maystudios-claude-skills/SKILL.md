---
name: opencode
description: >
  Invoke OpenCode CLI as a sub-agent to leverage alternative AI models (GPT-5.x, Codex,
  local models) for code implementation, review, debugging, research, and second opinions.
  Use when the user asks to "use opencode", "get a second opinion from GPT/Codex",
  "implement with opencode", "review with opencode", "let opencode handle this",
  "use a different model", or wants cross-model validation. Also triggers when the user
  explicitly names an OpenCode model (e.g., "use gpt-5.4", "use codex")
  or wants to delegate a task to a non-Claude AI system. Supports all providers configured
  in the user's OpenCode installation (OpenAI, GitHub Copilot, local models via
  Ollama/LM Studio, and OpenCode's own free-tier models).
---

# OpenCode Sub-Agent Protocol

This is an executable protocol for delegating work to OpenCode agents. Follow it precisely.

## Prerequisites

- `opencode` CLI installed and in PATH (verify: `opencode --version`)
- At least one provider authenticated (`opencode providers list`)
- Available models listed via `opencode models`

## Core Command

```bash
OPENCODE_DISABLE_AUTOUPDATE=true opencode run --format json --model <provider/model> --agent <build|plan> --dir "<working-dir>" --dangerously-skip-permissions [options] "<prompt>" 2>/dev/null
```

Key flags:
- `--format json` -- machine-parseable ndjson output (always use this)
- `--model provider/model` -- e.g., `openai/gpt-5.4`, `openai/gpt-5.3-codex`
- `--variant <level>` -- reasoning effort: `minimal`, `medium`, `high`, `xhigh` (provider-specific)
- `--dir <path>` -- working directory for the task
- `--dangerously-skip-permissions` -- auto-approve tool calls (required for headless)
- `-f/--file <path>` -- attach file(s) to the prompt
- `--agent <name>` -- `build` for implementation (filesystem+bash), `plan` for analysis (read-only)
- `-c/--continue` -- continue last session
- `-s/--session <id>` -- continue specific session

## Output Parsing

The `--format json` flag emits ndjson (one JSON object per line):

| type | Contains |
|------|----------|
| `text` | `.part.text` -- model's text response |
| `tool_call` | `.part.name`, `.part.input` -- tool invocations |
| `tool_result` | `.part.output` -- tool execution results |
| `step_start` | Session/message IDs |
| `step_finish` | `.part.tokens` (usage), `.part.cost`, `.part.reason` |

Parse with the helper script (always redirect stderr):
```bash
opencode run --format json ... 2>/dev/null | python .claude/skills/opencode/scripts/parse_output.py [--mode text|full|tools|cost|session|diff|summary]
```

Parse modes:
- `text` -- model's text response (default)
- `full` -- text + tool calls + tool results
- `tools` -- tool calls and results only
- `cost` -- token usage and cost breakdown
- `session` -- extract session ID for continuation
- `diff` -- extract file modifications from tool calls
- `summary` -- one-line summary (status, tokens, cost, duration)

---

## Task Protocols

Determine the task type from the user's request, then follow the matching protocol.

### Protocol 1: Implement

Use when the user wants OpenCode to write or modify code.

**Steps:**
1. **Scope** -- identify exactly which files to create/modify. List them explicitly.
2. **Context** -- gather files the agent needs to see. Attach with `-f`.
3. **Constraints** -- build the constraint block (see Prompt Engineering below).
4. **Execute** -- run with `--agent build`:
   ```bash
   OPENCODE_DISABLE_AUTOUPDATE=true opencode run --format json \
     --model openai/gpt-5.4 --agent build \
     --dir "C:/UnrealEngine/VHS" --dangerously-skip-permissions \
     -f <file1> -f <file2> \
     "<prompt>" 2>/dev/null | python .claude/skills/opencode/scripts/parse_output.py --mode full
   ```
5. **Validate** -- read every modified file. Check correctness, conventions, compilation.
6. **Report** -- summarize what changed, flag anything suspicious.

**Default model:** `openai/gpt-5.4` | **Timeout:** `timeout: 300000`

### Protocol 2: Review

Use when the user wants a second opinion on code quality, bugs, or correctness.

**Steps:**
1. **Target** -- identify files to review.
2. **Execute** -- run with `--agent plan` (read-only):
   ```bash
   OPENCODE_DISABLE_AUTOUPDATE=true opencode run --format json \
     --model openai/gpt-5.4 --variant high --agent plan \
     --dir "C:/UnrealEngine/VHS" --dangerously-skip-permissions \
     -f <file1> "<review prompt>" 2>/dev/null | python .claude/skills/opencode/scripts/parse_output.py
   ```
3. **Present** -- relay findings to user with file:line references.

**Default model:** `openai/gpt-5.4` + `--variant high` | **Timeout:** `timeout: 300000`

### Protocol 3: Debug

Use when the user wants OpenCode to investigate a bug or error.

**Steps:**
1. **Evidence** -- gather error messages, stack traces, relevant code.
2. **GAS context** -- for GAS bugs, instruct the agent to check: tag blocking/requirements, effect application/removal ordering, MMC dependencies, ASC initialization timing.
3. **Execute** -- run with `--agent plan`:
   ```bash
   OPENCODE_DISABLE_AUTOUPDATE=true opencode run --format json \
     --model openai/gpt-5.3-codex --variant high --agent plan \
     --dir "C:/UnrealEngine/VHS" --dangerously-skip-permissions \
     "<diagnostic prompt>" 2>/dev/null | python .claude/skills/opencode/scripts/parse_output.py
   ```
4. **Analyze** -- cross-reference findings with actual code before presenting.

**Default model:** `openai/gpt-5.3-codex` + `--variant high` | **Timeout:** `timeout: 300000`

### Protocol 4: Research

Use when the user wants OpenCode to explore and analyze the codebase.

**Steps:**
1. **Question** -- formulate a clear, bounded research question.
2. **Execute** -- run with `--agent plan`:
   ```bash
   OPENCODE_DISABLE_AUTOUPDATE=true opencode run --format json \
     --model openai/gpt-5.4-mini-fast --agent plan \
     --dir "C:/UnrealEngine/VHS" --dangerously-skip-permissions \
     "<research question>" 2>/dev/null | python .claude/skills/opencode/scripts/parse_output.py
   ```
3. **Verify** -- spot-check claims by reading referenced files yourself.

**Default model:** `openai/gpt-5.4-mini-fast` | **Timeout:** `timeout: 300000`

---

## Orchestration Patterns

These patterns compose the basic protocols above into more powerful workflows.
Use them when the task benefits from multi-step validation or parallel execution.

### Pattern A: Implement-Then-Review Pipeline

**When:** Implementation tasks where quality matters. This is the default for non-trivial implementation.

**Protocol:**
1. Run **Protocol 1 (Implement)** with `--agent build`
2. Read and verify the changes yourself (quick sanity check)
3. Run **Protocol 2 (Review)** on the changed files, using a DIFFERENT model:
   - If implementation used `openai/gpt-5.4`, review with `openai/gpt-5.3-codex`
   - Cross-model review catches model-specific blind spots
4. **Quality gate:** If review finds critical issues, fix them (either yourself or re-run implement with fix instructions)
5. Report both the implementation and review results to user

### Pattern B: Parallel Multi-Model Review

**When:** The user wants thorough validation, or says "get multiple opinions".

**Protocol:**
1. Construct the review prompt once
2. Spawn parallel Bash commands (use `run_in_background` or `&`):
   ```bash
   # Run in parallel -- each to a temp file
   PROMPT="<review prompt>"
   DIR="C:/UnrealEngine/VHS"

   OPENCODE_DISABLE_AUTOUPDATE=true opencode run --format json \
     --model openai/gpt-5.4 --variant high --agent plan \
     --dir "$DIR" --dangerously-skip-permissions "$PROMPT" \
     2>/dev/null > /tmp/review_gpt54.txt &

   OPENCODE_DISABLE_AUTOUPDATE=true opencode run --format json \
     --model openai/gpt-5.3-codex --variant high --agent plan \
     --dir "$DIR" --dangerously-skip-permissions "$PROMPT" \
     2>/dev/null > /tmp/review_codex.txt &

   wait
   ```
3. Parse each result separately:
   ```bash
   cat /tmp/review_gpt54.txt | python .claude/skills/opencode/scripts/parse_output.py
   cat /tmp/review_codex.txt | python .claude/skills/opencode/scripts/parse_output.py
   ```
4. **Synthesize** -- identify issues raised by multiple models (high confidence) vs. single model (lower confidence). Present a unified report.

### Pattern C: Autonomous Improvement Loop

**When:** The user wants iterative code improvement, or says "keep improving this", "optimize", "polish".

Inspired by autoresearch's iterative experiment loop. The agent makes changes, validates them, keeps improvements, and reverts failures.

**Protocol:**
```
LOOP (max N iterations, default 3):
  1. Identify the current quality baseline (read code, note issues)
  2. Construct an improvement prompt targeting the worst issue
  3. Run Protocol 1 (Implement) with --agent build
  4. Validate: read changed files, check for regressions
  5. Run Protocol 2 (Review) on changed files with a different model
  6. QUALITY GATE:
     - If review passes (no critical issues) → keep changes, report improvement
     - If review fails (critical issues found) → revert changes (git checkout the files), report why
  7. If no more meaningful improvements found → STOP
  8. Continue to next iteration
```

**Important constraints:**
- Always set a maximum iteration count (default 3, user can specify more)
- Each iteration must target a specific, measurable improvement
- Revert on failure -- never accumulate broken changes
- Stop early if improvements become marginal
- Report each iteration's outcome so the user can follow progress

### Pattern D: Background Agent

**When:** Claude Code wants to continue other work while OpenCode runs. Use for long-running tasks that don't block the conversation.

**Protocol:**
1. Run the OpenCode command using Bash with `run_in_background: true`:
   ```bash
   OPENCODE_DISABLE_AUTOUPDATE=true opencode run --format json \
     --model openai/gpt-5.4 --agent plan \
     --dir "C:/UnrealEngine/VHS" --dangerously-skip-permissions \
     "<prompt>" 2>/dev/null > /tmp/opencode_result.txt
   ```
2. Continue with other work while waiting for notification
3. When notified, parse the result:
   ```bash
   cat /tmp/opencode_result.txt | python .claude/skills/opencode/scripts/parse_output.py
   ```
4. Present findings to user

### Pattern E: Session Continuation (Multi-Step Workflow)

**When:** Complex tasks that benefit from building context across multiple exchanges.

**Protocol:**
1. Run the first task and capture the session ID:
   ```bash
   OPENCODE_DISABLE_AUTOUPDATE=true opencode run --format json \
     --model openai/gpt-5.4 --agent plan \
     --dir "C:/UnrealEngine/VHS" --dangerously-skip-permissions \
     "<first task>" 2>/dev/null | tee /tmp/oc_step1.txt | python .claude/skills/opencode/scripts/parse_output.py --mode session
   ```
2. Use the session ID for follow-up tasks:
   ```bash
   OPENCODE_DISABLE_AUTOUPDATE=true opencode run --format json \
     --session "<session-id>" --dangerously-skip-permissions \
     "<follow-up task>" 2>/dev/null | python .claude/skills/opencode/scripts/parse_output.py
   ```
   Or use `--continue` for the last session:
   ```bash
   OPENCODE_DISABLE_AUTOUPDATE=true opencode run --format json \
     --continue --dangerously-skip-permissions \
     "<follow-up task>" 2>/dev/null | python .claude/skills/opencode/scripts/parse_output.py
   ```

### Pattern F: Git-Checkpoint Implementation

**When:** Risky implementations where rollback safety is important.

Inspired by autoresearch's git-as-state-machine pattern.

**Protocol:**
1. **Checkpoint** -- note the current git state:
   ```bash
   git stash  # or commit current work
   ```
2. Run **Protocol 1 (Implement)** with `--agent build`
3. **Validate** -- read all changed files, run build/tests if applicable
4. **Gate:**
   - If changes are correct → keep them, report success
   - If changes are wrong → revert:
     ```bash
     git checkout -- <modified-files>
     ```
   - Report what went wrong and why the revert happened
5. **Never leave broken changes** -- if validation fails, always revert before reporting

---

## Prompt Engineering

OpenCode has NO access to this conversation's context. Every prompt must be **fully self-contained**.

Do NOT use OpenCode to invoke Claude/Anthropic models or Google/Gemini models -- these providers are
not available in OpenCode. Only use OpenAI, GitHub Copilot, local, and OpenCode's own models.

### Prompt Structure (Required)

Every prompt sent to OpenCode must follow this structure:

```
[CONTEXT BLOCK]
<project type, conventions, key constraints>

[TASK]
<imperative description of what to do>

[SCOPE]
<explicit boundaries: which files/dirs to touch, which to ignore>

[CONSTRAINTS]
<naming conventions, patterns to follow, things to avoid>

[OUTPUT FORMAT]
<what form the response should take>
```

### UE5/VHS Context Block (Always Include for Project Tasks)

```
This is an Unreal Engine 5.7 C++ project (VHS - first-person horror game).
Source: Source/VHS/  |  Module: VHS  |  No Public/Private split (side-by-side .h/.cpp)

Naming conventions:
- UE prefixes: A (actors), U (UObjects), F (structs), E (enums), I (interfaces)
- GAS: GA_ (abilities), GC_ (cues), MMC_ (magnitude calcs), GE_ (effects)
- Booleans: b prefix (bIsRecovering)
- #pragma once, CoreMinimal.h first, .generated.h last

Key systems: GAS (AbilitySystem/), Enhanced Input, StateTree (AI)
Dependencies: GameplayAbilities, GameplayTags, GameplayTasks, EnhancedInput, StateTreeModule
```

### Scope Constraints (Critical for Avoiding Timeouts)

Always set explicit scope boundaries. Broad prompts cause the agent to explore the entire filesystem and timeout.

**Good:**
```
Search ONLY in Source/VHS/AbilitySystem/. Do NOT explore other directories.
Modify ONLY HorrorCharacter.h and HorrorCharacter.cpp. Do NOT touch other files.
```

**Bad:**
```
Look through the project and find issues.  (too broad -- will timeout)
```

### Implementation Prompt Template

```
[CONTEXT]
This is an Unreal Engine 5.7 C++ project (VHS). <conventions block>

[TASK]
Implement <feature> in <file(s)>.
<detailed requirements>

[SCOPE]
- Create/modify ONLY: <explicit file list>
- Reference (read-only): <files to read for context>
- Do NOT touch: <exclusions>

[CONSTRAINTS]
- Follow existing patterns in <reference file>
- Use UPROPERTY(EditDefaultsOnly, Category = "<Category>") for configurable values
- All new UObject classes need UCLASS(ClassGroup=(VHS)) macro
- Header: #pragma once, CoreMinimal.h first, .generated.h last

[OUTPUT]
Write the implementation directly. No explanations needed.
```

### Review Prompt Template

```
[CONTEXT]
This is an Unreal Engine 5.7 C++ project using GAS. <conventions block>

[TASK]
Review the following files for: correctness, bugs, performance, security, UE5 best practices.
Be specific: cite file paths and line numbers. Suggest concrete fixes.

[SCOPE]
Review ONLY: <file list>
Do NOT explore other directories.

[OUTPUT FORMAT]
For each issue found:
- **[SEVERITY]** (critical/warning/info)
- **File:Line** -- specific location
- **Issue** -- what's wrong
- **Fix** -- concrete solution
```

### Debug Prompt Template

```
[CONTEXT]
UE5.7 project (VHS) using GAS. <conventions block>

[BUG REPORT]
<symptom description>
<error messages / stack traces>
<reproduction steps if known>

[TASK]
Investigate root cause. Check:
- <specific things to check based on the bug>
- For GAS bugs: tag blocking, effect ordering, MMC deps, ASC init timing

[SCOPE]
Search ONLY in: <directory>

[OUTPUT FORMAT]
1. Root cause (most likely)
2. Evidence (file:line references)
3. Fix (concrete code changes)
```

---

## Model Selection

Pick the right model for the task. See `references/models.md` for the full guide.

**Quick defaults:**

| Task | Fast | Default | Deep |
|------|------|---------|------|
| Implementation | `openai/gpt-5.4-mini-fast` | `openai/gpt-5.4` | `openai/gpt-5.3-codex` |
| Review | `openai/gpt-5.4-mini` | `openai/gpt-5.4` + `--variant high` | `openai/gpt-5.3-codex` + `--variant high` |
| Debug | `openai/gpt-5.4-mini-fast` | `openai/gpt-5.3-codex` + `--variant high` | `openai/gpt-5.4` + `--variant xhigh` |
| Research | `openai/gpt-5.4-mini-fast` | `openai/gpt-5.4-fast` | `openai/gpt-5.4` |

Use `opencode models` to discover all available models. Only OpenAI, GitHub Copilot, OpenCode's own
free-tier models, and local models (Ollama/LM Studio) are supported.

**Cross-model review pairings** (for Pipeline Pattern A):
- Implement with `openai/gpt-5.4` → Review with `openai/gpt-5.3-codex`
- Implement with `openai/gpt-5.3-codex` → Review with `openai/gpt-5.4`
- Always use a different model for review than implementation

**Cost-sensitive alternatives:**
- `github-copilot/gpt-5.4` -- free with Copilot subscription
- `github-copilot/gpt-5.3-codex` -- free with Copilot subscription
- `opencode/big-pickle` -- OpenCode's own free tier
- Local: `ollama/qwen3-coder:latest` -- zero API cost

---

## Error Handling & Recovery

### Error Detection

| Symptom | Cause | Recovery |
|---------|-------|----------|
| `opencode` not found | Not installed | Tell user: `npm i -g opencode` |
| No providers configured | No auth | Tell user: `opencode providers login` |
| Model not available | Wrong model ID | Run `opencode models`, suggest alternatives |
| Timeout (>3 min) | Scope too broad | Narrow scope constraints, use faster model |
| JSON parse failure | Corrupt output | Retry with `--format default`, read raw text |
| Exit code non-zero | Runtime error | Check stderr (up to 500 chars), retry once |
| Empty text response | Agent did only tool calls | Use `--mode full` to see tool call results |

### Automatic Model Fallback

If a model fails or times out, fall back in this order:
1. `openai/gpt-5.4` (primary)
2. `openai/gpt-5.3-codex` (code-optimized)
3. `openai/gpt-5.4-mini-fast` (fastest, always works)
4. `github-copilot/gpt-5.4` (free tier)
5. `opencode/big-pickle` (OpenCode free tier)

### Crash Recovery

If OpenCode crashes mid-implementation (`--agent build`):
1. Check which files were modified: `git diff --name-only`
2. Read each modified file to assess completeness
3. If changes are partial or broken → `git checkout -- <files>`
4. Retry with a narrower scope or different model
5. Report the crash and recovery to the user

---

## Decision Framework

Use this to decide WHEN and HOW to invoke OpenCode:

```
User request received
  │
  ├─ "use opencode" / names a model → Use OpenCode (user explicit)
  │
  ├─ "second opinion" / "cross-validate" → Pattern B (Parallel Multi-Model)
  │
  ├─ "implement with X" → Protocol 1, optionally Pattern A (Implement-Then-Review)
  │
  ├─ "review with X" → Protocol 2
  │
  ├─ "keep improving" / "optimize" / "polish" → Pattern C (Autonomous Loop)
  │
  ├─ Complex implementation → Pattern A (Implement-Then-Review) by default
  │
  ├─ Risky changes → Pattern F (Git-Checkpoint)
  │
  └─ Long-running task, user wants to continue chatting → Pattern D (Background)
```

## Advanced Patterns

See `references/advanced.md` for:
- Server mode for persistent sessions
- Environment variables for automation
- Export/import sessions
- Stats and cost tracking
