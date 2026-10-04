---
name: mcp-tool-change
description: Use when adding, renaming, or changing PubTator-Link MCP tools, resources, prompts, or schemas.
---

# MCP Tool Change

Follow `AGENTS.md` first.

## Workflow

1. Inspect the existing domain module under `pubtator_link/mcp/` and reuse its registration pattern.
2. Keep hosted public tools research-use scoped; do not add clinical decision support, destructive cache operations, or broad filesystem/network powers.
3. Prefer typed Pydantic input/output models and stable error codes over raw dictionaries or string-inferred failures.
4. Update MCP unit tests under `tests/unit/mcp/` and route/service tests when REST behavior is also affected.
5. Update runtime-facing docs if tool names, arguments, response modes, or safety language change.
6. Run focused MCP tests, then `make ci-local` before handoff.
