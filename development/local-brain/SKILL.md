---
name: local-brain
description: Delegate complex, multi-step codebase exploration to local Ollama models. Best for analysis, review, and understanding tasks that require reasoning across multiple files.
version: 0.9.0
---

# Local Brain

Delegate complex codebase exploration to local Ollama models. Local Brain excels at multi-step tasks requiring reasoning, not simple commands.

## When to Use Local Brain

Local Brain adds 10-70 seconds of LLM inference overhead per query. Use it for tasks where AI reasoning provides value, not for simple commands.

**Use Local Brain for:**
- Multi-step exploration ("Find all error handlers and explain how they work")
- Code review and analysis ("Review recent changes for potential issues")
- Understanding unfamiliar code ("Explain how authentication flows through the system")
- Tasks requiring judgment ("What patterns does this codebase use?")
- When you don't know which files or commands to look at

**Do NOT use Local Brain for:**
- Simple file listing (use `ls` or `find` directly — 1000x faster)
- Git status/log (use `git log` directly — 1000x faster)
- Reading a specific known file (use `cat` or your editor)
- Any single-command operation where you know what to run

**Performance reality:** A simple "list files" query takes 12-70 seconds via Local Brain vs 5ms via `ls`. The value is in the reasoning, not the tool execution.

## Installation

Install local-brain:
```bash
uv pip install local-brain
```

Or with pipx:
```bash
pipx install local-brain
```

**Requirements:**
- Ollama running locally (https://ollama.ai)
- A model pulled (e.g., `ollama pull qwen3`)

## Usage

```bash
local-brain "prompt"                    # Ask anything (auto-selects best model)
local-brain -v "prompt"                 # Show tool calls
local-brain -d "prompt"                 # Show step-by-step debug output
local-brain -m qwen3-coder:30b "prompt" # Specific model
local-brain --trace "prompt"            # Enable OTEL tracing
local-brain --list-models               # Show available models
local-brain --root /path/to/project "prompt"  # Set project root
local-brain doctor                      # Check system health
```

## Health Check

Verify your setup is working correctly:

```bash
local-brain doctor
```

This checks:
- Ollama is installed and running
- Recommended models are available
- Tools execute correctly
- Optional tracing dependencies

Example output:
```
🔍 Local Brain Health Check

Checking Ollama...
  ✅ Ollama is installed (ollama version is 0.13.1)

Checking Ollama server...
  ✅ Ollama server is running (9 models)

Checking recommended models...
  ✅ Recommended models installed: qwen3:latest

Checking tools...
  ✅ Tools working (9 tools available)

Checking optional features...
  ✅ OTEL tracing available (--trace flag)

========================================
✅ All checks passed! Local Brain is ready.
```

## Examples

Focus on tasks where AI reasoning adds value:

```bash
# Code review and analysis (good use case)
local-brain "Review the recent git changes and identify potential issues"
local-brain "Analyze the error handling patterns in this codebase"

# Understanding unfamiliar code (good use case)
local-brain "Explain how the authentication system works end-to-end"
local-brain "What design patterns does this codebase use?"

# Multi-step exploration (good use case)
local-brain "Find all TODO comments and categorize them by urgency"
local-brain "Trace how user input flows through the validation layer"

# Generate content requiring context (good use case)
local-brain "Generate a commit message based on the staged changes"
local-brain "Summarize what changed in the last 5 commits"
```

## Model Selection Guide

Choose the right model for your task:

### For Code Exploration (Recommended)

Use `qwen3-coder:30b` for faster exploration tasks:

```bash
local-brain -m qwen3-coder:30b "Find all error handlers and explain how they work"
local-brain -m qwen3-coder:30b "What validation patterns are used in this codebase?"
local-brain -m qwen3-coder:30b "Trace the data flow from API endpoint to database"
```

Why: 2.5x faster than qwen3:30b (12-20s vs 35-70s per query), direct tool usage.

### For Complex Reasoning

Use `qwen3:30b` for tasks requiring deeper analysis:

```bash
local-brain -m qwen3:30b "Analyze the architecture and suggest improvements"
local-brain -m qwen3:30b "Review recent changes for security vulnerabilities"
local-brain -m qwen3:30b "Explain how authentication works end-to-end"
```

Why: More thorough reasoning, better at synthesis and review tasks.

### Tips for Better Results

Use --debug to see what the model is doing step-by-step:
```bash
local-brain -d -m qwen3-coder:30b "Analyze the test coverage gaps"
```

**Avoid these models** (broken or unreliable tool calling):
- `qwen2.5-coder:*` - Outputs JSON instead of executing tools
- `llama3.2:1b` - Too small, hallucinates paths
- `deepseek-r1:*` - No tool support at architecture level

If no model is specified, Local Brain auto-selects the best installed model.

## Observability

### Debug Mode (--debug or -d)

See step-by-step progress with the `--debug` flag:

```bash
local-brain --debug "Analyze error handling in the auth module"
```

This shows:
- Step number and duration
- Tool calls with arguments
- Result preview (truncated)
- Token usage per step

Example output:
```
[debug] Model: qwen3-coder:30b
[debug] Project root: /path/to/project

[Step 1] (4.2s)
  Tool: list_directory(path='.', pattern='**/*')
  Result:
    src/main.py
    src/utils.py
    ... (15 lines total)
  Tokens: 2634 in / 42 out
```

### OTEL Tracing (--trace)

Enable OpenTelemetry tracing to visualize agent execution with detailed timing and metrics:

```bash
local-brain --trace "Review recent changes and identify potential issues"
```

This captures:
- Agent execution timeline (total duration)
- Individual steps (planning, execution, final answer)
- LLM calls with token counts
- Tool invocations with inputs/outputs
- Timing for each operation

#### Visualizing Traces with Jaeger (Recommended)

For real-time visualization of agent execution, use Jaeger:

**1. Start Jaeger (one-time setup):**
```bash
docker run -d \
  --name jaeger \
  -p 16686:16686 \
  -p 4318:4318 \
  jaegertracing/all-in-one
```

**2. Run local-brain with tracing:**
```bash
local-brain --trace -m qwen3-coder:30b "Analyze the test patterns in this codebase"
```

**3. View in Jaeger UI:**
Open http://localhost:16686 and select:
- Service: `local-brain`
- Operation: `CodeAgent.run`

You'll see a waterfall timeline showing:
```
CodeAgent.run (5.1s total)
├── Step 1 (2.04s)
│   ├── LiteLLMModel.generate (2.03s) ← LLM latency
│   └── list_directory (1.5ms) ← Tool execution
└── Step 2 (3.09s)
    ├── LiteLLMModel.generate (3.09s)
    └── FinalAnswerTool (0.1ms)
```

Click any span to see details: tokens used, arguments, outputs, errors.

#### Install Tracing Dependencies

For JSON console output only (no Jaeger):
```bash
pip install local-brain[tracing]
```

For Jaeger visualization, also install:
```bash
pip install opentelemetry-exporter-otlp
```

#### Combining Flags for Maximum Insight

Use all three flags together for complete visibility:
```bash
local-brain --trace --debug -m qwen3-coder:30b "Review recent changes for security issues"
```

This gives:
- `--trace` → OTEL spans in Jaeger (timing, tokens, architecture)
- `--debug` → Real-time step progress to stderr (what's happening now)
- `--verbose` → Tool calls in main output (what was called)

Note: `--debug` and `--trace` can be combined.

## Security

All file operations are **restricted to the project root** (path jailing):

- Files outside the project directory cannot be read
- Shell commands execute within the project root
- Sensitive files (`.env`, `.pem`, SSH keys) are blocked
- Only read-only shell commands are allowed
- All tool outputs are truncated (200 lines / 20K chars max)
- Tool calls have timeouts (30 seconds default)

## Available Tools

The model assumes these tools are available and uses them directly:

### File Tools
- `read_file(path)` - Read file contents at a given `path`. Large files are truncated (200 lines / 20K chars). Has 30s timeout. **Restricted to project root.**
- `list_directory(path, pattern)` - List files in `path` matching a glob `pattern`. Supports recursive patterns:
  - `*` - files in directory only
  - `**/*` - ALL files recursively (use this to discover nested structures)
  - `**/*.py` - all Python files recursively
  - `src/**/*.js` - all JS files under src/
  Excludes hidden files and common ignored directories. Returns up to 100 files. Has 30s timeout.
- `file_info(path)` - Get file metadata (size, type, modified time) for a given `path`. Has 30s timeout.

### Code Navigation Tools (New in v0.6.0)
- `search_code(pattern, file_path, ignore_case)` - **AST-aware code search**. Unlike simple grep, shows intelligent context around matches (function/class boundaries). Supports Python, JavaScript, TypeScript, Go, Rust, Ruby, Java, C/C++.
- `list_definitions(file_path)` - **Extract class/function definitions** from a source file. Shows signatures and docstrings without full implementation code. Great for understanding file structure quickly.

### Git Tools
- `git_diff(staged, file_path)` - Show code changes. Use `staged=True` for staged changes. Optionally provide a `file_path`. Output is truncated.
- `git_status()` - Check repo status. Output is truncated.
- `git_changed_files(staged, include_untracked)` - List changed files. Use `staged=True` for staged files, `include_untracked=True` to include untracked files. Output is truncated.
- `git_log(count)` - View commit history. `count` specifies number of commits (max 50). Output is truncated.

All tools return human-readable output or error messages on failure.
