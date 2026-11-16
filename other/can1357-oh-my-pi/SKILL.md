---
name: can1357--oh-my-pi
description: "omp — AI coding agent viết bằng Rust (27K lines), hash-anchored edits (-61% output tokens), LSP+debugger tích hợp, 32 tools, 40+ LLM providers. Fork của Pi platform."
allowed-tools: Bash, Read, Write
user-invocable: true
---

omp (oh-my-pi): coding agent terminal-first với LSP và debugger wired in — không phải wrapper của IDE, mà là agent hiểu code như IDE hiểu.

## Install

```bash
# macOS/Linux
curl -fsSL https://omp.sh/install -o /tmp/omp-install.sh
# Inspect first: head -40 /tmp/omp-install.sh — then run if safe:
sh /tmp/omp-install.sh

# Bun
bun install -g @oh-my-pi/pi-coding-agent

# Windows
irm https://omp.sh/install.ps1 | iex
```

## Core Innovation: Hash-Anchored Edits

```
Thay vì: model rewrite dòng code (nhiều tokens, dễ lỗi whitespace)
omp dùng: content-hash anchors → model CHỈ point tới anchor + thay đổi cần làm

Kết quả: -61% output tokens trên same task
```

## LSP Integration

```
Rename symbol → omp route qua workspace/willRenameFiles
→ tự động update re-exports, barrel files, aliased imports
→ agent biết mọi thứ IDE biết: go-to-definition, references, diagnostics
```

## Debugger Support

```
Supports: lldb (C/C++/Rust), dlv (Go), debugpy (Python)
- Attach to segfaulting binaries
- Step through code, inspect frames
- Analyze goroutines in hanging services
```

## 32 Tools (8 categories)

```
File:     read, write, edit, ast_edit, search
Runtime:  bash, eval, ssh
Code:     lsp, debug
Coord:    task, irc, todo
External: browser, web_search, github
Memory:   retain, recall, reflect
```

## Multi-Provider (40+)

```
Anthropic, OpenAI, Gemini, xAI Grok, Mistral, Ollama, llama.cpp
Role-based routing:
  default → standard turns
  smol    → cost-effective subagents
  slow    → deep reasoning
  plan    → strategic planning
```

## Subagents trong isolated worktrees

```typescript
// spawn subagent, results là schema-validated objects
const result = await agent.task({
  prompt: "analyze this module",
  worktree: true  // isolated, no merge conflicts
})
```

## Import config tự động

Tự nhận: Cursor MDC, Cline rules, Codex AGENTS.md, Copilot settings — không cần migrate.

## Source

https://github.com/can1357/oh-my-pi · MIT · +2318⭐/week
