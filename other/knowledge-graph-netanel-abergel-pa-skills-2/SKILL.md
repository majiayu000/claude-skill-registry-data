---
name: knowledge-graph
description: "Knowledge graph and smart memory management using graphify + Obsidian-inspired patterns. Use when: setting up a knowledge graph, managing memory health, cross-linking notes, compiling wiki pages from scattered notes, adding structured frontmatter, or running memory health checks. Triggers on: 'knowledge graph', 'graphify', 'wiki', 'cross-link', 'memory health', 'frontmatter', 'compile notes', 'wikilinks'."
---

# Knowledge Graph Skill

Turn any workspace into a queryable knowledge graph with smart memory management.
Combines graphify (code/doc graph) with three Obsidian-inspired patterns.

## Installation

In pa-skills repo, the skill is at the *root*: `pa-skills/knowledge-graph/`
(not under `skills/`). Copy it to your workspace:

```bash
# From your pa-skills clone
cp -r knowledge-graph/ /path/to/your/workspace/skills/knowledge-graph/
```

## Prerequisites

```bash
pip install graphifyy
graphify claw install  # ⚠️ This MODIFIES your AGENTS.md — adds graphify query rules
```

**Important:** `graphify claw install` appends a `## graphify` section to your AGENTS.md.
This is intentional — it tells your agent to check the graph before reading raw files.
Review the changes after running it.

## .graphifyignore

Create `.graphifyignore` in your workspace root to exclude noise:

```
node_modules/
.git/
media/
.tmp/
tmp/
graphify-out/
pa-skills/
skills-external/
*.pdf
*.ogg
*.jpg
*.png
```

**Critical:** If you have both `pa-skills/knowledge-graph/` and `skills/knowledge-graph/`
on disk, add `pa-skills/` to `.graphifyignore` to avoid duplicate nodes in the graph.
If your repo clone lives under `.tmp/pa-skills/`, exclude `.tmp/` too or the duplicate noise will still leak in.

## Components

### 1. Knowledge Graph (graphify)

Build and query a knowledge graph from code + docs.

```bash
# Initial setup (AST-only, free)
graphify update .

# Query the graph
graphify query "how does X connect to Y"
graphify path "ModuleA" "ModuleB"
graphify explain "concept"

# After code changes
graphify update .
```

Full semantic extraction (with LLM) produces richer cross-doc connections.
See `graphify claw install` output for AGENTS.md integration rules.

### 2. Auto Cross-Linker

Scans notes and adds [[wikilinks]] for known concepts from the graph.

```bash
# Build concept index from graph nodes + skills + projects
python3 scripts/wiki_crosslinker.py --build-index

# Cross-link today's daily note
python3 scripts/wiki_crosslinker.py --daily

# Cross-link all daily notes
python3 scripts/wiki_crosslinker.py --all-daily
```

Concepts come from: graphify nodes, skill names, project names, contacts.
Only links document-type nodes with 4+ character names. Skips code internals.

### 3. Wiki Compiler (Karpathy Pattern)

"Compile once, query forever" — instead of RAG every time, compile scattered
mentions into structured wiki pages per topic.

```bash
# See what needs compiling
python3 scripts/wiki_compiler.py --scan

# Compile all topics with 3+ mentions
python3 scripts/wiki_compiler.py --compile

# Compile one specific topic
python3 scripts/wiki_compiler.py --compile "onboarding"

# Check wiki status
python3 scripts/wiki_compiler.py --status
```

Output: `wiki/<topic>.md` with frontmatter, timeline of mentions, and graph connections.
Each page is a self-contained summary — query it directly instead of scanning raw notes.

### 4. Structured Frontmatter

Adds YAML frontmatter with auto-detected tags to notes.

```bash
# Add frontmatter to all daily notes
python3 scripts/note_frontmatter.py --all-daily

# Add frontmatter to project docs
python3 scripts/note_frontmatter.py --projects

# Query by frontmatter
python3 scripts/note_frontmatter.py --query tag=onboarding
python3 scripts/note_frontmatter.py --query type=project
```

Auto-tags: graphify, crons, ops, whatsapp, calendar, content, monday,
onboarding, pa-network, infra, memory, eval, self-improve, skills, owner.

### 5. Memory Health Checker

Runs on the knowledge graph to detect memory problems.

```bash
# Full report
python3 scripts/memory_health.py

# Quick summary
python3 scripts/memory_health.py --quick
```

Checks: orphan nodes, daily note gaps, stale MEMORY.md entries,
weak communities, unreferenced skills, recent vs old activity.

## Recommended Crons

```
# Daily: memory health check (04:00 UTC)
daily-memory-health: python3 scripts/memory_health.py --quick

# Weekly: wiki compilation + cross-linking (Sun 03:00 UTC)
weekly-wiki-compile:
  1. python3 scripts/wiki_crosslinker.py --build-index
  2. python3 scripts/wiki_compiler.py --compile
  3. python3 scripts/note_frontmatter.py --all-daily
  4. python3 scripts/note_frontmatter.py --projects
  5. graphify update .
```

## Token Impact

| Operation | Without | With | Reduction |
|-----------|---------|------|-----------|
| Topic recall | ~15K tokens (scan daily notes) | ~200 tokens (wiki page) | 75x |
| Architecture query | ~411K tokens (read all files) | ~155 tokens (graph query) | 2,655x |
| "What happened with X" | grep all notes | frontmatter query + wiki page | ~50x |
