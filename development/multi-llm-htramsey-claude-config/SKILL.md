---
name: multi-llm
description: Route tasks to optimal LLM provider (Gemini, Codex, Copilot, Claude)
---

# Multi-LLM Routing

Route tasks to the optimal LLM provider for cost efficiency and capability matching.

## Quick Reference

| Trigger | Provider | Why |
|---------|----------|-----|
| Input >100KB | Gemini | 1M token context |
| "entire codebase" | Gemini | Large context |
| generate/scaffold/CRUD | Codex | Cost-optimized |
| security/architecture/debug | Claude | Best reasoning |
| shell/command/CLI | Copilot | Shell expertise |
| Default | Claude | Primary tool |

## Provider Status

Check installed providers and authentication:

```bash
~/.claude/scripts/diagnostics/llm-status.sh
```

## Scripts

### llm-route.sh - Routing Decisions

```bash
# Auto-detect best provider
~/.claude/scripts/automation/llm-route.sh "analyze this large log"

# Force specific provider
~/.claude/scripts/automation/llm-route.sh -p gemini "summarize"

# With file input (checks size for routing)
~/.claude/scripts/automation/llm-route.sh -f large.log "what errors?"

# List providers with auth status
~/.claude/scripts/automation/llm-route.sh --list
```

### llm-delegate.sh - Execute with Fallback

```bash
# Delegate to Gemini (falls back if unavailable)
~/.claude/scripts/automation/llm-delegate.sh gemini "summarize 500KB log"

# With timeout
~/.claude/scripts/automation/llm-delegate.sh -t 180 gemini "analyze codebase"

# Pipe content
cat large.log | ~/.claude/scripts/automation/llm-delegate.sh gemini "summarize"

# Disable fallback (fail if provider unavailable)
~/.claude/scripts/automation/llm-delegate.sh --no-fallback codex "generate API"

# Large prompts (>100KB) automatically use temp files to avoid ARG_MAX
~/.claude/scripts/automation/llm-delegate.sh gemini "$(cat large-codebase.py)"

# Multi-file content: use semicolons (NOT brace groups with newlines)
cat file1.py file2.py | ~/.claude/scripts/automation/llm-delegate.sh gemini "review"

# Or use command substitution for complex gathering
~/.claude/scripts/automation/llm-delegate.sh gemini "analyze: $(cat src/*.py)"
```

### llm-logging.sh - Routing Analytics

```bash
# View recent routing decisions
~/.claude/scripts/lib/llm-logging.sh recent 10

# Today's stats by provider
~/.claude/scripts/lib/llm-logging.sh stats

# Rotate logs if >10MB
~/.claude/scripts/lib/llm-logging.sh rotate
```

## Fallback Chain

When preferred provider fails:
```
Best-fit → Claude → Gemini → Codex → Copilot
```

## Provider Capabilities

### Gemini
| Attribute | Value |
|-----------|-------|
| Binary | `gemini` |
| Context | 1M tokens (2M coming) |
| Auth | `GEMINI_API_KEY` or `GOOGLE_API_KEY` |
| Best for | Large files, whole codebase, long documents |

```bash
gemini "summarize this" --output-format json
gemini -m gemini-2.5-pro "complex task"
```

### Codex
| Attribute | Value |
|-----------|-------|
| Binary | `codex` |
| Context | 200K tokens |
| Auth | `OPENAI_API_KEY` |
| Best for | Code generation, CRUD, boilerplate |

```bash
codex exec --json "generate REST API"
codex exec --full-auto -s workspace-write "run tests"
codex exec -o output.txt "generate code"  # Save last message to file
```

### Copilot
| Attribute | Value |
|-----------|-------|
| Binary | `copilot` (standalone) |
| Auth | `GH_TOKEN` or `GITHUB_TOKEN` |
| Best for | Shell commands, quick explanations |

```bash
copilot -p "explain find -exec" --allow-all-tools
copilot -p "how to grep recursively" --allow-all-tools
copilot -i "interactive session"  # Start interactive with initial prompt
```

### Claude
| Attribute | Value |
|-----------|-------|
| Binary | `claude` |
| Context | 200K tokens |
| Best for | Architecture, security, debugging, review |

```bash
claude -p "review security" --output-format text
```

## Cost Comparison

| Provider | Input (per 1M) | Output (per 1M) | Context |
|----------|----------------|-----------------|---------|
| Claude Opus | $15 | $75 | 200K |
| Claude Sonnet | $3 | $15 | 200K |
| Gemini 2.5 Pro | $1.25 | $5 | 1M |
| Codex (GPT-5) | ~$2.50 | ~$10 | 200K |
| Copilot | Subscription | - | Limited |

### Savings Strategy

- Large context → Gemini: **10x cheaper** on input
- Boilerplate → Codex: Lower per-token cost
- Reasoning → Claude: Best quality for complex tasks

## Usage Examples

### Large Log Analysis

```bash
# Gemini handles large context efficiently
~/.claude/scripts/automation/llm-delegate.sh gemini "Analyze errors in:
$(cat /path/to/large.log)"
```

### Boilerplate Generation

```bash
# Codex optimized for code generation
~/.claude/scripts/automation/llm-delegate.sh codex "Generate TypeScript REST API for User model with CRUD, validation, OpenAPI docs"
```

### Shell Command Help

```bash
# Copilot excels at shell explanations
~/.claude/scripts/automation/llm-delegate.sh copilot "explain: find . -type f -exec grep -l 'TODO' {} +"
```

### Hybrid Approach

1. Delegate boilerplate to Codex
2. Review generated code with Claude
3. Apply Claude's security insights
4. Combine for best result

## Configuration

### Environment Variables

```bash
# Delegation timeout (seconds)
export LLM_DELEGATE_TIMEOUT=120

# Provider-specific models
export GEMINI_MODEL="gemini-2.5-pro"
export CODEX_MODEL="gpt-5.1-codex-max"
```

### Provider Installation

```bash
# Gemini (npm)
npm install -g @google/gemini-cli

# Codex (bun or npm)
bun install -g @openai/codex
# or: npm install -g @openai/codex

# Copilot (standalone binary)
# Download from: https://github.com/github/copilot-cli/releases

# Claude
npm install -g @anthropic-ai/claude-code
```

## Log Files

| File | Content |
|------|---------|
| `~/.claude/data/logs/llm-routing.jsonl` | Detailed routing decisions |
| `~/.claude/data/hook-events.jsonl` | Summary events |

### Log Schema

```json
{
  "timestamp": "2026-01-01T12:00:00Z",
  "provider": "gemini",
  "prompt": "summarize this 500KB log...",
  "status": "success",
  "reason": "large_context_512000_bytes",
  "latency_ms": 3500
}
```

## Troubleshooting

### Provider Not Found

```bash
# Check all providers
~/.claude/scripts/diagnostics/llm-status.sh

# Verify specific provider
command -v gemini && gemini --version
```

### Authentication Failed

```bash
# Check environment variables
echo $GEMINI_API_KEY
echo $OPENAI_API_KEY
echo $GH_TOKEN

# Or check config files
cat ~/.gemini/.env
```

### Delegation Timeout

```bash
# Increase timeout
~/.claude/scripts/automation/llm-delegate.sh -t 300 gemini "large task"

# Or set globally
export LLM_DELEGATE_TIMEOUT=300
```

### View Routing History

```bash
# Recent decisions
~/.claude/scripts/lib/llm-logging.sh recent 20

# Today's stats
~/.claude/scripts/lib/llm-logging.sh stats
```

### Shell Syntax Errors

If you see `{: command not found` or similar errors when piping to llm-delegate:

**Problem**: Multi-line brace groups `{ ... }` don't work in Claude's Bash tool.

**Solutions**:
```bash
# Use cat with multiple files
cat file1.py file2.py | llm-delegate.sh gemini "review"

# Use command substitution
llm-delegate.sh gemini "$(cat file1.py; echo '---'; cat file2.py)"

# Use semicolons for multiple commands
(echo "Header"; cat file.py; echo "Footer") | llm-delegate.sh gemini "analyze"
```

## Integration

- **batch-operations**: Delegate multiple tasks in parallel
- **context-optimizer**: Suggest delegation when context bloated
- **using-tmux**: Foundation for CLI delegation
