---
name: llm-mux-test
description: Test llm-mux IR translator - cross-format API translation
---

## Quick Start

Run server in background

```
pkill -f llm-mux; go build -o llm-mux ./cmd/server && ./llm-mux
```

Run test

```
bun .opencode/skill/llm-mux-test/sdk_tests.ts
```
