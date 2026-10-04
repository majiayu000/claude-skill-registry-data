---
name: headroom
description: Context compression layer for AI agents. Reduces tokens sent to and received from LLMs by 60–95% with zero accuracy loss. Use when token costs are high, context windows are filling up, or tool outputs / logs / RAG chunks are bloating prompts. Triggers include "compress context", "reduce tokens", "save on API costs", "context window full", "token limit", "optimize prompts", or any task involving large tool outputs, log files, RAG results, or conversation history. Also provides `headroom learn` which mines failed sessions and writes corrections to CLAUDE.md automatically.
---

# Headroom — Context Compression for AI Agents

60–95% fewer tokens. Same answers. Library, proxy, MCP server, or agent wrap.
Local-first, Apache 2.0. Originals always retrievable (CCR — reversible compression).

## Install (60 seconds)

```bash
# Python
pip install headroom-ai            # core
pip install "headroom-ai[all]"     # + proxy, ML compressor, proxy extras

# TypeScript / Node
npm install headroom-ai

# Or wrap Claude Code directly (zero code changes)
headroom proxy --port 8787
ANTHROPIC_BASE_URL=http://localhost:8787 claude
```

## Modes

### 1. Proxy (recommended for Claude Code — zero code changes)

```bash
headroom proxy --port 8787 --code-aware   # --code-aware for coding sessions
ANTHROPIC_BASE_URL=http://localhost:8787 claude
```

Or use the one-liner:
```bash
headroom wrap claude   # starts proxy + launches claude with correct env vars
```

Check compression is working:
```bash
curl -s http://localhost:8787/stats | python3 -m json.tool
# Look for tokens_saved > 0
```

### 2. Python / TypeScript library (inline in your app)

```python
from headroom import HeadroomClient
from anthropic import Anthropic

client = HeadroomClient(Anthropic())
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": large_tool_output}]
)
```

TypeScript:
```typescript
import { withHeadroom } from 'headroom-ai';
import Anthropic from '@anthropic-ai/sdk';

const client = withHeadroom(new Anthropic());
```

### 3. MCP server (for Claude Code / Cursor / any MCP host)

```bash
headroom mcp   # starts the MCP server
```

Injects 3 tools: `headroom_compress`, `headroom_retrieve`, `headroom_stats`.

### 4. Output token reduction (cuts what the model writes back)

Output tokens cost 5× more than input on Opus-class models. Enable:

```bash
export HEADROOM_OUTPUT_SHAPER=1
export HEADROOM_VERBOSITY_LEVEL=2   # 0=off, 1-4 (4=maximum savings)
headroom proxy --port 8787
```

Verbosity levels:
- **1** — skip intro/outro chit-chat
- **2** — also skip restating code/output already on screen (default safe)
- **3** — conclusions only, skip reasoning
- **4** — bare minimum, fragments OK

## What gets compressed

| Content type | Compressor | Typical savings |
|---|---|---|
| JSON arrays (tool outputs, search results) | SmartCrusher (statistical) | 70–90% |
| Source code | CodeCompressor (AST via tree-sitter) | 60–85% |
| Log files | Pattern deduplication | 75–90% |
| Text / RAG chunks | Kompress-v2-base (ML, HuggingFace) | 60–80% |
| Images | DCT + format optimization | 50–80% |

All compression is **reversible** via CCR (Compress-Cache-Retrieve): the agent gets a
`headroom_retrieve` tool to fetch the original. Originals never deleted during session.

## headroom learn — writes corrections to CLAUDE.md

Mine failed sessions and write learned corrections back to project memory:

```bash
headroom learn                     # analyse all recent sessions
headroom learn --project .         # scope to current project
headroom learn --apply             # auto-write corrections to CLAUDE.md / AGENTS.md
```

Learns from: failed commands, corrected outputs, repeated errors, and patterns
where the agent had to retry. Distils them into `CLAUDE.md` rules.

## Cross-agent shared memory

```python
from headroom.memory import SharedContext

ctx = SharedContext(project_id="arshad-ai")
ctx.store("calendar_data", compressed_output)  # agent A stores
data = ctx.retrieve("calendar_data")           # agent B retrieves
```

Per-project SQLite + HNSW vector store. Auto-dedup. No cross-project bleed.

## Cache TTL analysis (analyse Claude Code spending)

The `scripts/claude_analysis_ttl.py` script in this repo analyses your
`~/.claude/projects/` sessions and prints a cost comparison table showing
whether extending prompt cache TTL from 5 min to 1 h would save money:

```bash
python3 scripts/claude_analysis_ttl.py
```

## Claude Code + Vertex AI integration

See `docs/claude-code-vertex-headroom.md` in the headroom repo for the
working tested setup. Key points:
- Run headroom proxy as the Anthropic-mode intermediary
- Set `ANTHROPIC_BASE_URL=http://127.0.0.1:8787` (NOT Vertex mode)
- Add `--code-aware` flag or compression no-ops on code
- Add `--backend litellm-vertex_ai` for Vertex routing

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `ANTHROPIC_BASE_URL` | — | Point Claude Code at the proxy |
| `HEADROOM_OUTPUT_SHAPER` | `0` | Enable output token reduction |
| `HEADROOM_VERBOSITY_LEVEL` | `2` | 0–4 verbosity steering level |
| `HEADROOM_EXCLUDE_TOOLS` | — | Comma-separated tools to skip compression (e.g. `Read,Grep`) |
| `HEADROOM_TELEMETRY` | `on` | Set to `off` to disable anonymous telemetry |

## References

- Canonical llms.txt: see `llms.txt` in this skill directory
- Full docs: https://headroom-docs.vercel.app/docs
- PyPI: https://pypi.org/project/headroom-ai/
- npm: https://www.npmjs.com/package/headroom-ai/
