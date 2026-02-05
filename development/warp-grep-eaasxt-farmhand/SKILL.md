---
name: warp-grep
description: Parallel code search with Warp-Grep MCP. Use for codebase discovery, understanding how things work, data flow analysis, or when the user asks "how does X work" about the codebase.
---

# Warp-Grep (MCP Server)

Parallel codebase search. Runs 8 searches per turn for efficient discovery.

## When This Applies

| Signal | Action |
|--------|--------|
| "How does X work?" | Use Warp-Grep |
| Data flow across files | Use Warp-Grep |
| Cross-cutting concerns | Use Warp-Grep |
| Understanding architecture | Use Warp-Grep |

---

## How It Works

Warp-Grep is an MCP tool that activates automatically for natural language code questions. It:

1. Interprets your question
2. Runs up to 8 parallel searches
3. Returns relevant code snippets with context

---

## When to Use Warp-Grep

| Use Case | Use Warp-Grep? |
|----------|---------------|
| "How does authentication work?" | **YES** |
| Data flow analysis | **YES** |
| Understanding module interactions | **YES** |
| Finding all usages of a pattern | **YES** |

---

## When NOT to Use Warp-Grep

| Use Case | Use Instead |
|----------|-------------|
| Known function name | `rg` (ripgrep) or Grep tool |
| Known exact file | Just open it with Read |
| Simple existence check | Glob or `rg` |
| Single specific search | Grep tool |

---

## Query Tips

**Good queries:**
- "How does the payment processing flow work?"
- "Where are user sessions managed?"
- "How is error handling done in the API layer?"
- "What happens when a request comes in?"

**Less effective:**
- "Find function X" → Use `rg` or Grep instead
- "Open file Y" → Use Read tool

---

## Integration with Other Tools

| Need | Tool |
|------|------|
| Codebase discovery | Warp-Grep |
| Specific pattern search | Grep / `rg` |
| Past session content | CASS |
| Current documentation | Exa |
| Task graph | bv |

---

## Requirements

Requires Morph API key configured:

```bash
claude mcp add morph-fast-tools -s user \
  -e MORPH_API_KEY=your-key \
  -e ALL_TOOLS=true \
  -- npx -y @morphllm/morphmcp
```

---

## See Also

- `external-docs/` — Grounding with web sources via Exa
- `cass-search/` — Past session search
