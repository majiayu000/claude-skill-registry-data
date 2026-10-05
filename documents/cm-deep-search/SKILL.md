---
name: cm-deep-search
description: "Optional power-up — detects oversized codebases/docs and suggests tobi/qmd for local semantic search. Bridges cm-continuity (working memory) with long-term document retrieval. Zero-config detection, non-intrusive suggestion."
---

# Deep Search — Semantic Memory Power-Up

> **When your project outgrows AI's context window, bring the search engine to your docs.**
> Optional integration with [tobi/qmd](https://github.com/tobi/qmd) — BM25 + Vector + LLM re-ranking, 100% local.

## When to Trigger

**This skill is NOT invoked directly.** It is triggered automatically by other skills when they detect an oversized project.

### Detection Thresholds

During codebase scan (Phase 1a of `cm-brainstorm-idea`, Step 2 of `cm-dockit`, etc.), check:

```
TRIGGER if ANY of these are true:
  → docs/ folder contains >50 markdown files
  → Project has >200 source files total
  → User mentions "meeting notes", "historical PRDs", "old specs"
  → User asks "find that file that talked about X from before"
  → cm-dockit just generated >30 doc files
```

### What to Say (Non-Intrusive)

When threshold is met, suggest naturally — DO NOT block or force:

```markdown
💡 **Pro Tip: Deep Search**

This project has [X doc files / Y source files] — quite large for AI to read directly.
You can install **[qmd](https://github.com/tobi/qmd)** to create semantic search
across all your documentation, helping AI find the right context faster.

Quick install:
\`\`\`bash
npm install -g @tobilu/qmd
qmd collection add ./docs --name project-docs
qmd context add qmd://project-docs "Project documentation for [project-name]"
qmd embed
\`\`\`

Then AI can search using: `qmd query "your question"`
```

---

## Setup Guide (when user agrees to install)

### Step 1: Install

```bash
# Node.js
npm install -g @tobilu/qmd

# Or Bun
bun install -g @tobilu/qmd
```

### Step 2: Index project docs

```bash
# Add collections
qmd collection add ./docs --name docs
qmd collection add ./src --name source --mask "**/*.{ts,tsx,js,jsx,py,go,rs}"

# Add context (helps AI understand each collection's purpose)
qmd context add qmd://docs "Technical documentation for [project-name]"
qmd context add qmd://source "Source code for [project-name]"

# Create vector embeddings
qmd embed
```

### Step 3: Setup MCP Server (for Claude/Cursor/Antigravity)

Add to MCP config:

```json
{
  "mcpServers": {
    "qmd": {
      "command": "qmd",
      "args": ["mcp"]
    }
  }
}
```

Or run HTTP mode for shared server:

```bash
qmd mcp --http --daemon
```

### Step 4: Verify

```bash
# Check index
qmd status

# Test search
qmd query "authentication flow"
```

---

## Usage with CodyMaster Skills

### With `cm-brainstorm-idea` (Phase 1: DISCOVER)

When AI needs to understand the full picture of a large project:

```bash
# Find all docs related to the topic being brainstormed
qmd query "user authentication redesign" --json -n 10

# Get full content of important docs
qmd get "docs/architecture.md" --full
```

### With `cm-planning` (Phase A: Brainstorm)

When searching for specs, PRDs, or past decisions related to the feature being planned:

```bash
qmd query "payment integration decisions" --files --min-score 0.4
```

### With `cm-dockit` (Post-generation)

After `cm-dockit` finishes generating docs, index them so AI can search from any session:

```bash
qmd collection add ./docs --name project-knowledge
qmd embed
```

### With `cm-continuity` (Tier 4: External Memory)

`cm-continuity` manages working memory (500 words). `qmd` extends it with long-term semantic search:

```
Tier 1: Sensory Memory     → temporary variables in session (not persisted)
Tier 2: Working Memory      → CONTINUITY.md (~500 words)
Tier 3: Long-Term Memory    → learnings.json, decisions.json
Tier 4: External Semantic   → qmd (optional, text search for large docs)
Tier 5: Structural Code     → CodeGraph (optional, AST graph for code — see cm-codeintell)
```

> **qmd** finds text across docs/code. **CodeGraph** finds symbols, call graphs, and impact.
> They complement each other — use both for maximum intelligence on large projects.

---

## 🛑 Staleness Prevention

The biggest risk of Semantic Search is **stale index / new source**. If AI reads outdated docs and generates incorrect code, the consequences are severe.

CodyMaster handles this with 3 mechanisms:

### 1. The "Post-Execution" Sync
Whenever AI completes a task that changes/creates a large number of files (e.g., `cm-dockit` generates docs, `cm-execution` refactors source code):
```bash
# This runs quickly because qmd only embeds changed files (incremental)
qmd embed
```
> **AI Rule:** If the project has qmd enabled, AI must automatically run `qmd embed` via terminal before finishing a task.

### 2. The "Pre-Flight" Check
Before starting `cm-brainstorm-idea` or `cm-planning` on a project using qmd, AI calls the MCP tool to perform a health check:
```json
// AI auto-runs this MCP tool
{
  "name": "status",
  "arguments": {}
}
```
If status reports files pending/un-embedded, AI will run `qmd embed` in terminal before searching.

### 3. Git Hook (Recommended for User)
For 100% safety beyond AI's control (when end-user modifies code directly):
AI should suggest the user install a **Git Post-Commit Hook**:
```bash
# Add file .git/hooks/post-commit
#!/bin/sh
qmd embed > /dev/null 2>&1 &
```
This ensures every commit triggers QMD to silently update the index in the background.

---

## Position in CodyMaster Lifecycle

```
cm-continuity (memory) ─────────────── always active
cm-deep-search (search) ──── optional ─┤
                                       ├── feeds context to ──→ cm-brainstorm-idea
                                       │                   ──→ cm-planning
cm-dockit (generate docs) ── produces ─┤                   ──→ cm-execution
```

## Integration

| Skill | Relationship |
|-------|-------------|
| `cm-continuity` | COMPLEMENT: continuity = RAM, qmd = semantic disk search |
| `cm-brainstorm-idea` | TRIGGERED BY: Phase 1a codebase scan detects large corpus |
| `cm-dockit` | TRIGGERED AFTER: docs generated, suggest indexing |
| `cm-planning` | CONSUMER: uses qmd results for context during planning |
| `cm-execution` | CONSUMER: searches for related code/docs during execution |

---

## Requirements

```
System: macOS / Linux / Windows (WSL)
Runtime: Node.js 20+ or Bun 1.0+
VRAM: ~2-4GB for GGUF models (embedding + reranking)
Disk: ~2-5GB for models (downloaded on first run)
```

## Rules

```
✅ DO:
- Suggest qmd ONLY when detection threshold is met
- Keep suggestion non-intrusive (Pro Tip format, never blocking)
- Always include context command (qmd context add) — this is qmd's killer feature
- Guide user to setup MCP server for seamless AI integration

❌ DON'T:
- Force installation on every project
- Suggest qmd for small projects (<50 docs, <200 src files)
- Replace cm-continuity — they solve DIFFERENT problems
- Assume qmd is installed — always check first
```

## The Bottom Line

**`cm-continuity` = "remembers what you're doing." `cm-deep-search` = "finds what was written before." Together = complete memory system.**
