---
name: local-brain
description: Chat with local Ollama models that can explore your codebase using tools.
version: 0.7.1
---

# Local Brain

Chat with local Ollama models that have tools to explore your codebase.

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
local-brain -m qwen2.5:3b "prompt"        # Specific model
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

```bash
local-brain "What's in this repo?"
local-brain "Review the git changes"
local-brain "Generate a commit message"
local-brain "Explain how src/main.py works"
local-brain "Find all TODO comments"
local-brain "What functions are defined in utils.py?"
local-brain "Search for 'validate' in the auth module"
```

## Model Discovery

Local Brain automatically detects installed Ollama models and selects the best one for tool-calling tasks:

```bash
# See what models are available
local-brain --list-models
```

**Recommended models** (verified tool support):
- `qwen3:latest` - General purpose, default choice (Tier 1)
- `qwen2.5:3b` - Resource-constrained environments (Tier 1)

**Avoid these models** (broken or unreliable tool calling):
- `qwen2.5-coder:*` - Broken with Smolagents
- `llama3.2:1b` - Hallucinations
- `deepseek-r1:*` - No tool support

If no model is specified, Local Brain auto-selects the best installed model.

## Observability

Enable OpenTelemetry tracing with the `--trace` flag:

```bash
local-brain --trace "What files are here?"
```

This traces:
- Agent execution steps
- LLM calls with token counts
- Tool invocations with inputs/outputs

Install tracing dependencies:
```bash
pip install local-brain[tracing]
```

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
- `list_directory(path, pattern)` - List files in `path` matching a glob `pattern` (e.g., `*.py`, `src/**/*.js`). Excludes hidden files and common ignored directories. Returns up to 100 files. Has 30s timeout.
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
