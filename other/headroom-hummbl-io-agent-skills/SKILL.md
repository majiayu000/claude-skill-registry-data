---
name: headroom
description: >
  Proxy-level context compression for AI agents. Compresses tool outputs, logs,
  RAG chunks, files, and conversation history BEFORE they reach the LLM. 60-95%
  fewer tokens for JSON, 15-20% fewer for coding agents. Same answers.
  Library, proxy, MCP server, agent wrap modes. Local-first, reversible (CCR).
  Use when user says "headroom", "compress context", "proxy compress", "reduce
  input tokens", or wants to cut tool output tokens at the proxy layer (vs
  caveman-mode which cuts output prose, vs ponytail which cuts code LOC).
  Source: headroomlabs-ai/headroom (64K stars, Apache 2.0) — github.com/headroomlabs-ai/headroom
license: Apache-2.0
version: 0.1.0
execution-mode: advisory
category: hummbl-research
status: candidate
---

# Headroom

Proxy-level compression. Sits between tools and LLM. Strips tokens before model sees them. Different layer than caveman (prose) or ponytail (code).

## What it does

Compresses everything agent reads — tool outputs, logs, RAG chunks, files, conversation history — before LLM. Same answers, fraction of tokens.

## Compression layers

| Layer | What | Savings |
|-------|------|---------|
| SmartCrusher | JSON data | 60-95% |
| CodeCompressor | AST-aware code | high |
| Kompress-v2-base | Prose/text (HF model) | moderate |
| CacheAligner | Detects volatile content that busts KV cache | warns, never rewrites |
| CCR | Reversible — originals cached for retrieval | lossless on demand |

## Modes

1. **Library** — `compress(messages)` inline in Python/TypeScript app
2. **Proxy** — `headroom proxy --port 8787`, zero code changes, any language
3. **Agent wrap** — `headroom wrap claude|codex|grok|copilot|cursor|aider|opencode|cline|continue|goose|openhands|openclaw|vibe|omp|zcode` in one command
4. **MCP server** — `headroom_compress`, `headroom_retrieve`, `headroom_stats` for any MCP client
5. **Cross-agent memory** — shared store across Claude, Codex, Gemini, Grok, auto-dedup
6. **headroom learn** — mines failed sessions, writes corrections to CLAUDE.local.md / AGENTS.md / GEMINI.md / GROK.md

## Install

```bash
# Python CLI (recommended — ships headroom command)
uv tool install --python 3.13 "headroom-ai[all]"
# or
pip install "headroom-ai[all]"

# TypeScript SDK only (no CLI)
npm install headroom-ai
```

Requires Python 3.10+. Granular extras: `[proxy]`, `[mcp]`, `[ml]`, `[code]`, `[memory]`, `[vector]`, `[relevance]`, `[image]`, `[agno]`, `[langchain]`, `[evals]`, `[pytorch-mps]`.

## Quick start

```bash
headroom deploy                    # turnkey local deployment + agent config
headroom wrap claude               # wrap a coding agent
headroom proxy --port 8787         # drop-in proxy, zero code changes
headroom doctor                    # health check — confirms routing works
headroom perf                      # performance report
headroom dashboard                 # live savings dashboard (proxy must run)
```

## MCP config (for Codex or any MCP client)

```toml
[mcp_servers.headroom]
command = "/absolute/path/from/command-v/headroom"
args = ["mcp", "serve"]
```

Use `command = "headroom"` only when client PATH includes uv tool dir.

## MCP tools

- `headroom_compress` — compress messages/outputs before sending to LLM
- `headroom_retrieve` — fetch original (uncompressed) content on demand
- `headroom_stats` — compression statistics

## Proven savings (real workloads)

| Workload | Before | After | Savings |
|----------|-------:|------:|--------:|
| Code search (100 results) | 17,765 | 1,408 | 92% |
| SRE incident debugging | 65,694 | 5,118 | 92% |
| GitHub issue triage | 54,174 | 14,761 | 73% |
| Codebase exploration | 78,502 | 41,254 | 47% |

Accuracy preserved: GSM8K ±0.000, TruthfulQA +0.030, SQuAD v2 97%, BFCL 97%.

## When to use

- Tool outputs bloating context (grep with 100 results, long logs, big JSON)
- RAG chunks eating token budget
- Conversation history growing large
- Cross-agent memory dedup needed
- Want reversible compression (not lossy)

## When NOT to use

- Already using rtk for CLI command compression (overlaps — pick one layer)
- Output prose compression only (use caveman-mode)
- Code minimization only (use ponytail)
- Tiny context, no budget pressure

## Pair with

- **caveman-mode** — headroom cuts input tokens, caveman cuts output tokens. Both = max savings.
- **ponytail** — headroom compresses what agent reads, ponytail minimizes what agent writes (code).
- **caveman-ponytail** — all three together = brain big, mouth small, code small, context small.

## Boundaries

Headroom = input/context compression. Does not change what model says (pair with caveman) or what code gets written (pair with ponytail). Reversible via CCR — originals always retrievable.

## Skill Chains
- For compress bridge session output before agent ingestion -> `[cross-runtime-bridge]` (`sessions`)
