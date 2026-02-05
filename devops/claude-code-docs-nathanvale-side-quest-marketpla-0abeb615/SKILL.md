---
name: claude-code-docs
description: Answers questions about Claude Code features, configuration, and usage from local documentation synced from code.claude.com. Use when users ask about hooks, plugins, skills, MCP servers, slash commands, sub-agents, settings, permissions, sandboxing, CLAUDE.md memory files, model selection, costs, IDE integrations (VS Code, JetBrains), CI/CD (GitHub Actions, GitLab), or cloud providers (Bedrock, Vertex, Azure).
---

# Claude Code Documentation Expert

Answer questions about Claude Code using local docs synced from code.claude.com.

## Docs Location

`plugins/claude-code-docs/docs/` - 46 markdown files covering all Claude Code features.

## Workflow

1. **Find the right doc**: Read `reference/doc-topics.md` for topic-to-file mapping
2. **Read the doc**: Read the relevant file from `plugins/claude-code-docs/docs/`
3. **Answer with citations**: Quote relevant sections, cite the doc filename

## Quick Lookup

If unsure which doc to read, check `docs/INDEX.md` for a full list.

For detailed topic mapping, see [reference/doc-topics.md](reference/doc-topics.md).

## Response Guidelines

- Only state what's in the docs
- Always cite doc filenames
- Say "not covered in docs" if info isn't available
- Suggest `/claude-code-docs:update` if docs seem outdated
