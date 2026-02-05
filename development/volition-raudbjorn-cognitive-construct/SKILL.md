---
name: volition
description: Agency and execution. Edit code semantically, invoke LLMs, search the web, query security services, and discover relevant skills.
version: 5.1.0
license: MIT
metadata:
  phase: 5
  dependencies: python>=3.10, httpx, pydantic, sentence-transformers
---

# Volition: The Will to Act

> "Action without agency is reaction. Agency without action is paralysis. Volition is the synthesis."

## Overview

**Volition** is the executive skill of the Cognitive Construct. It transforms intent into action: editing code semantically via LSP tools, invoking specialized LLMs for expert consultation, searching the web for current information, and querying security services with appropriate safeguards.

## Commands

### `act "<action>"`
Execute a general action. Volition routes to the appropriate handler based on intent classification.

```bash
python3 volition.py act "refactor the authentication module for better security"
```

**Output:**
```json
{"status": "completed", "handler": "code_edit", "summary": "Refactored auth module..."}
```

### `edit "<symbol>" "<change>"`
Perform semantic code edits using LSP-powered tools. Finds symbols by name and applies changes contextually.

```bash
python3 volition.py edit "UserAuth.validate" "add rate limiting check at start"
```

**Options:**
- `--project <path>`: Project root (default: current directory)
- `--fallback`: Allow text-based editing if LSP unavailable

**Output:**
```json
{"status": "success", "symbol": "UserAuth.validate", "file": "src/auth.py", "changes": 1}
```

### `query "<service>" "<query>"`
Query external services for information.

**Services:**
- `web`: General web search via openai-websearch-mcp
- `security`: Security reconnaissance via Shodan (requires confirmation)
- `llm`: Consult an LLM for expert advice

```bash
# Web search
python3 volition.py query web "latest Python 3.13 features"

# Security query (prompts for confirmation)
python3 volition.py query security "exposed MongoDB instances in AS12345"

# LLM consultation
python3 volition.py query llm "best practices for JWT token rotation" --tag coding
```

**Options:**
- `--provider <name>`: Override LLM provider for `llm` service
- `--tag <tag>`: Task tag for LLM routing (coding, reasoning, creative, general)
- `--confirm`: Pre-confirm security queries (use with caution)

### `capabilities`
List available capabilities and their status.

```bash
python3 volition.py capabilities
```

**Output:**
```json
{
  "code_editing": {"status": "available", "backend": "serena", "languages": ["python", "typescript", "rust"]},
  "llm_consultation": {"status": "available", "providers": ["openai", "anthropic", "deepseek"]},
  "web_search": {"status": "available", "backend": "openai-websearch"},
  "security_queries": {"status": "restricted", "backend": "shodan", "rate_limit": "10/hour"}
}
```

## Skill Discovery

Volition includes a skill index for finding relevant Claude Agent Skills. Use these commands to discover and load skills dynamically.

### `skill search "<query>"`
Find skills relevant to a task description using semantic search.

```bash
python3 volition.py skill search "debug Python API errors" --top_k 3
```

**Output:**
```json
{
  "success": true,
  "data": [
    {"name": "python-debugging", "description": "Debug Python applications...", "relevance": 0.8234},
    {"name": "api-troubleshooting", "description": "Diagnose API issues...", "relevance": 0.7891}
  ],
  "message": "Found 2 relevant skill(s)"
}
```

**Options:**
- `--top_k N`: Number of results to return (default: 3)
- `--list_docs`: Include document list in results

### `skill read <name> [document]`
Read a skill's content or specific documents.

```bash
# Read skill instructions (SKILL.md)
python3 volition.py skill read python-debugging

# Read a specific document
python3 volition.py skill read python-debugging scripts/debugger.py
```

**Output:**
```json
{
  "success": true,
  "data": {"name": "python-debugging", "content": "...", "documents": ["scripts/debugger.py", "references/common-errors.md"]},
  "message": "Loaded skill: python-debugging"
}
```

### `skill list`
List all available skills in the index.

```bash
python3 volition.py skill list
```

**Output:**
```json
{
  "success": true,
  "data": [
    {"name": "python-debugging", "description": "Debug Python applications...", "document_count": 5},
    {"name": "api-troubleshooting", "description": "Diagnose API issues...", "document_count": 3}
  ],
  "message": "Found 42 indexed skill(s)"
}
```

### `skill status`
Check if the skill index is available.

```bash
python3 volition.py skill status
```

**Output:**
```json
{
  "success": true,
  "data": {"available": true, "skill_count": 42, "model": "all-MiniLM-L6-v2"},
  "message": "Skill index ready"
}
```

**Note:** The skill index uses vector embeddings internally. Implementation details (model names, search algorithms, data sources) are opaque - you interact only through these commands.

## Security Constraints (R.22-R.23)

### Shodan Queries

Shodan queries are **restricted operations** with mandatory safeguards per requirements R.22-R.23:

1. **Explicit --confirm Flag Required (R.22.1)**: Every Shodan query requires the `--confirm` flag. No interactive prompts bypass this requirement:
   ```bash
   # This will prompt for confirmation (returns confirmation_required status)
   python3 volition.py query security "exposed MongoDB instances"

   # Explicitly confirm (use with caution)
   python3 volition.py query security "exposed MongoDB instances" --confirm
   ```

2. **Disable Flag (R.22.2)**: Shodan can be completely disabled via environment variable:
   ```bash
   VOLITION_DISABLE_SHODAN=true  # Disables all Shodan queries
   NOCP_FLAG_SHODAN_ENABLED=false  # Feature flag alternative
   ```

3. **Data Redaction (R.22.3)**: IP addresses in results are partially redacted for privacy:
   ```json
   {"ip": "192.168.xxx.xxx", "port": 27017, "org": "Example Org"}
   ```

4. **Audit Logging with Severity (R.22.4)**: All queries logged with governance metadata:
   - File: `~/.volition/shodan_audit.jsonl`
   - Fields: requester, target, query, justification, result, severity, timestamp

5. **Rate Limiting (R.23.1)**: Maximum 10 queries per hour. Exceeding returns error.

6. **Clear Error on Unconfirmed (R.23.2)**: Unconfirmed queries return explicit error with guidance.

## Configuration

### Required Environment Variables

Set in `.env.local`:

```bash
# Code Editing (Serena)
# No API key required - uses local LSP servers

# LLM Consultation (at least one required)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
DEEPSEEK_API_KEY=sk-...

# Web Search
OPENAI_API_KEY=sk-...  # Shared with LLM

# Security Queries
SHODAN_API_KEY=...  # Optional, enables security queries
```

### Credential Validation

Volition validates credentials at startup and returns clear errors:
- Missing: `"SHODAN_API_KEY not found - security queries disabled"`
- Invalid format: `"OPENAI_API_KEY has invalid format (expected sk-...)"`

## Action Routing

When using `act`, Volition classifies intent and routes to the appropriate handler:

| Category | Keywords | Handler |
|----------|----------|---------|
| `code_edit` | refactor, edit, modify, add, remove, fix | Serena LSP |
| `llm_call` | explain, analyze, review, suggest, consult | cross-llm-mcp |
| `web_search` | search, find, lookup, what is, latest | openai-websearch |
| `security` | scan, expose, vulnerability, shodan | mcp-shodan |

Override automatic routing with `--handler`:
```bash
python3 volition.py act "find security issues" --handler llm_call
```

## Backends

Volition uses these libraries internally (implementation details are **opaque**):

- **Serena**: LSP-powered semantic code editing
- **cross-llm**: Multi-provider LLM access
- **openai-websearch**: Web search with reasoning
- **shodan-client**: Security reconnaissance
- **skill-search**: Vector similarity search for skill discovery

You interact only through Volition's unified command interface. The underlying protocols (MCP, LSP, HTTP APIs) are hidden - you never see tool schemas, JSON-RPC, or protocol-level details.

## Error Handling

Volition returns structured errors without exposing internal details:

```json
{"status": "error", "code": 2, "message": "Symbol not found: UserAuth.validate"}
```

Error codes:
- `1`: Invalid input
- `2`: Resource not found
- `3`: Backend unavailable
- `4`: Permission denied (e.g., unconfirmed security query)

## Synergies

Volition optionally integrates with other Cognitive Construct skills:

- **→ Inland Empire**: Actions are logged as memories for future recall
- **← Rhetoric**: Complex actions can trigger deliberation before execution
- **← Encyclopedia**: Code edits can fetch documentation context

Enable synergies via `--synergy` flag or `VOLITION_SYNERGY=true` environment variable.

## Files

- `~/.volition/audit.log`: General audit trail for all actions
- `~/.volition/shodan_audit.jsonl`: Shodan-specific audit log with severity metadata (R.22.4)
- `~/.volition/rate_limits.json`: Rate limit state
- `~/.volition/preferences.json`: User preferences and defaults

## Synergies (Requirement 8.2)

Volition logs all actions to Inland Empire via the SkillMessage bus for future recall:

```python
# Actions automatically logged to memory:
# - code_edit: symbol, file, result
# - llm_call: tag, prompt summary
# - web_search: query
# - security_query: target, matches

# Control via feature flag:
NOCP_FLAG_VOLITION_INLAND_EMPIRE_SYNERGY=true
```

Synergies operate transparently (R.8.5) - if Inland Empire is unavailable, actions complete without error.
