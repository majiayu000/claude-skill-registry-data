---
name: cc-insights
version: 0.2.1
description: Use PROACTIVELY when searching past Claude Code conversations, analyzing development patterns, or generating activity reports. Automatically processes conversation history from the project, enables RAG-powered semantic search, and generates insight reports with pattern detection. Provides optional dashboard for visualization. Not for real-time analysis or cross-project searches.
---

# Claude Code Insights

Unlock the hidden value in your Claude Code conversation history through automatic processing, semantic search, and intelligent insight generation.

## Overview

This skill automatically analyzes your project's Claude Code conversations (stored in `~/.claude/projects/[project]/*.jsonl`) to provide:

- **RAG-Powered Semantic Search**: Find conversations by meaning, not just keywords
- **Automatic Insight Reports**: Pattern detection, file hotspots, tool usage analytics
- **Activity Trends**: Understand your development patterns over time
- **Knowledge Extraction**: Surface recurring topics, solutions, and best practices
- **Zero Manual Effort**: Fully automatic processing of existing conversations

## When to Use This Skill

**Trigger Phrases**:
- "Find conversations about [topic]"
- "Generate weekly insights report"
- "What files do I modify most often?"
- "Launch the insights dashboard"
- "Export insights as [format]"

**Use Cases**:
- Search past conversations by topic or file
- Generate activity reports and insights
- Understand development patterns over time
- Extract knowledge and recurring solutions
- Visualize activity with interactive dashboard

**NOT for**:
- Real-time conversation analysis (analyzes history only)
- Conversations from other projects (project-specific)
- Manual conversation logging (automatic only)

## Response Style

**Informative and Visual**: Present search results with relevance scores and snippets. Generate reports with clear metrics and ASCII visualizations. Offer to save or export results.

## Mode Selection

| User Request | Mode | Reference |
|--------------|------|-----------|
| "Find conversations about X" | Search | `modes/mode-1-search.md` |
| "Generate insights report" | Insights | `modes/mode-2-insights.md` |
| "Launch dashboard" | Dashboard | `modes/mode-3-dashboard.md` |
| "Export as JSON/CSV/HTML" | Export | `modes/mode-4-export.md` |

## Mode Overview

### Mode 1: Search Conversations
Find past conversations using semantic search (by meaning) or metadata search (by files/tools).
→ **Details**: `modes/mode-1-search.md`

### Mode 2: Generate Insights
Analyze patterns and generate reports with file hotspots, tool usage, and knowledge highlights.
→ **Details**: `modes/mode-2-insights.md`

### Mode 3: Interactive Dashboard
Launch a Next.js web dashboard for rich visualization and exploration.
→ **Details**: `modes/mode-3-dashboard.md`

### Mode 4: Export and Integration
Export insights as Markdown, JSON, CSV, or HTML for sharing and integration.
→ **Details**: `modes/mode-4-export.md`

## Initial Setup

**First time usage**:
1. Install dependencies: `pip install -r requirements.txt`
2. Run initial processing (automatic on first use)
3. Build embeddings (one-time, ~1-2 min)
4. Ready to search and analyze!

**What happens automatically**:
- Scans `~/.claude/projects/[current-project]/*.jsonl`
- Extracts and indexes conversation metadata
- Builds vector embeddings for semantic search
- Creates SQLite database for fast queries

## Important Reminders

- **Automatic processing**: Skill updates index on each use (incremental)
- **First run is slow**: Embedding creation takes 1-2 minutes
- **Project-specific**: Analyzes only current project's conversations
- **Dashboard requires Node.js**: v18+ for the Next.js dashboard
- **ChromaDB for search**: Vector similarity search for semantic queries

## Limitations

- Only analyzes JSONL conversation files from Claude Code
- Requires sentence-transformers for embedding creation
- Dashboard is local only (localhost:3000)
- Large conversation histories may take longer to process initially

## Reference Materials

| Resource | Purpose |
|----------|---------|
| `modes/*.md` | Detailed mode instructions |
| `reference/troubleshooting.md` | Common issues and fixes |
| `scripts/` | Processing and indexing scripts |
| `dashboard/` | Next.js dashboard application |

## Success Criteria

- [ ] Conversations processed and indexed
- [ ] Embeddings built for semantic search
- [ ] Search returns relevant results
- [ ] Insights reports generated correctly
- [ ] Dashboard launches and displays data

---

**Tech Stack**: Python (processing), SQLite (metadata), ChromaDB (vectors), Next.js (dashboard)
