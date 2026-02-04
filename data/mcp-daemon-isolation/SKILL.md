---
name: mcp-daemon-isolation
description: Context isolation for query-type MCP tools (LSP, search, database) via external CLI. Use when MCP query results consume too many context tokens.
allowed-tools: ["Read", "Bash", "Grep", "Glob"]
---

# MCP Daemon Isolation for Query-Type MCPs

External CLI pattern for isolating **query-type MCP** tool results from main context.

## Query-Type MCP 정의

| Type | Examples | 특징 |
|------|----------|------|
| **Query-type** | Serena (LSP), Database, Search | 결과 크기 예측 불가, 수천 토큰 가능 |
| **Action-type** | File write, Git, Deploy | 결과 작음, 성공/실패 위주 |

**식별 기준:** `find_*`, `search_*`, `get_*`, `list_*` 패턴 도구

---

## Problem

```
Claude Session
├── mcp__serena__find_symbol("UserService")
│   └── Result: 2,500 tokens (full JSON)    ← CONSUMED
└── Context budget: rapidly depleting
```

**Daemon isolates tool definitions** (~350 tokens × tools), but **results still consume context**.

---

## Solution: External CLI + Structured Extraction

```
Claude Session
├── Bash: serena-query find_symbol UserService
│   └── stdout: "• UserService [Class] @ src/user.py:42"
│       (~50 tokens)                      ← MINIMAL
└── Full result stored: /tmp/serena-result.json
```

**Key insight**: Claude IS the LLM. Structured extraction provides 95%+ token savings.

---

## Architecture

```
┌──────────────┐     ┌──────────────────┐     ┌──────────────┐
│ Claude       │────▶│ serena-query     │────▶│ Serena       │
│ Session      │     │ (external CLI)   │     │ Daemon :8765 │
└──────────────┘     └──────────────────┘     └──────────────┘
     Bash (~50 tok)     SSE + MCP Protocol       29 tools
```

For protocol details: `Read("references/mcp-sse-protocol.md")`

---

## Structured Extractors

| Tool | Full JSON | Extracted Output | Savings |
|------|-----------|------------------|---------|
| `list_dir` | ~800 | `📁 Dirs(12): hooks... 📄 Files(11)` | 95% |
| `get_symbols_overview` | ~1,200 | `Class(2): Config... Function(5)` | 96% |
| `find_symbol` | ~2,000 | `• UserService [Class] @ src/user.py:42-98` | 97% |
| `search_for_pattern` | ~1,500 | `Matches(15) in 8 files` | 95% |

For formatter code: `Read("references/extractors-and-examples.md")`

---

## Usage

### Output Modes

```bash
serena-query find_symbol UserService                    # summary (기본)
serena-query find_symbol UserService --mode location    # 위치만 (Read 연계)
serena-query find_symbol UserService --mode full        # 전체 JSON
```

### Basic Commands

```bash
serena-query list_dir .
serena-query get_symbols_overview src/main.py --depth 1
serena-query find_symbol UserService --path src/
serena-query search_for_pattern "class.*Service" --path src/
serena-query find_symbol UserService --output /tmp/result.json
```

---

## 최적 워크플로우: 탐색-위치-읽기

```
1. 탐색 (--mode summary)     ~25 토큰   "어떤 심볼이 있지?"
2. 위치 (--mode location)    ~15 토큰   "정확히 어디있지?"
3. 읽기 (Read 도구)          실제 크기   필요한 코드만
```

| 시나리오 | stdio 방식 | daemon+Read | 절감률 |
|---------|-----------|-------------|--------|
| 클래스 분석 | ~525 | ~240 | 54% |
| 11개 함수 분석 | ~4,300 | ~665 | 85% |
| 대규모 검색 | ~10,000+ | ~500 | 95% |

For detailed examples: `Read("references/extractors-and-examples.md")`

---

## Installation

```bash
pip install httpx
cp scripts/serena-query ~/.local/bin/
chmod +x ~/.local/bin/serena-query
```

### Daemon Setup

```bash
uvx --from git+https://github.com/oraios/serena \
  serena start-mcp-server --transport sse --port 8765 --project-from-cwd
```

---

## Decision: Structured vs LLM Summarization

| Aspect | LLM Summarization | Structured Extraction |
|--------|-------------------|----------------------|
| Latency | +2-5 seconds | ~0ms |
| Cost | API call per query | Zero |
| Consistency | Variable | Deterministic |

Claude IS the LLM consuming the output - no need for additional summarization.

---

## 격리 전략 가이드

| 시나리오 | 권장 | 이유 |
|---------|------|------|
| 단일 심볼 편집 | stdio | 즉각적인 수정 |
| 코드베이스 탐색 | daemon | 대량 결과 예상 |
| 참조 추적 | daemon + location | 위치만 필요 |
| 리팩토링 계획 | daemon + full | 전체 구조 분석 |

---

## Common Issues

| 증상 | 원인 | 해결 |
|------|------|------|
| "Received request before initialization" | 핸드셰이크 누락 | `initialize` → `notifications/initialized` → `tools/call` 순서 |
| "Connection refused on 8765" | Daemon 미실행 | `systemctl --user start serena-daemon` |
| "Empty result" | 구조 불일치 | `--output`으로 raw JSON 저장 후 확인 |

---

## References

### Implementation
- [serena-query CLI](../../scripts/serena-query)
- [Implementation Details](references/serena-query-implementation.md)
- [v2 Design](references/serena-query-v2-design.md)

### Protocol & Examples
- [MCP-SSE Protocol](references/mcp-sse-protocol.md)
- [Extractors & Examples](references/extractors-and-examples.md)
- [Integration Guide](references/integration-guide.md)

### Related
- [MCP Gateway Patterns](../mcp-gateway-patterns/SKILL.md)
