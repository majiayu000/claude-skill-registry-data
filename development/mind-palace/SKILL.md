---
name: mind-palace
description: Navigate Mind Palace to query entity knowledge about codebase subsystems. Use when understanding architecture, exploring how systems work, or checking for hazards/gotchas before modifying code.
allowed-tools: Read, Glob, Grep
---

# Mind Palace Navigation

Query keeper entities for codebase knowledge. Each entity guards a subsystem and knows HOW it works, WHY it's designed that way, and WATCH_OUT warnings.

## Quick Reference

**List entities**: Read `.mind-palace/palace.yaml` for entity names

**Query an entity**: Read `.mind-palace/entities/<entityname>.yaml` (lowercase)

**Available Keepers** (22 total):
- MemoryKeeper - ChromaDB, summaries, retrieval
- SchedulingKeeper - Day phases, decision engine
- AgentKeeper - Claude SDK, Temple-Codex, tool execution
- SelfModelKeeper - Identity, observations, growth edges
- GoalsKeeper - Unified goals, hierarchies, approval workflow
- ConversationKeeper - Message persistence, threading
- And 16 more...

## Entity Format

Each entity YAML contains:
```yaml
name: MemoryKeeper
slug: memorykeeper          # Deterministic ID for cross-agent refs
location: memory
role: "Guardian of hierarchical vector memory..."
topics:
  - name: semantic search
    how: "Vector-based memory using ChromaDB..."
    why: "Finding relevant context requires semantic understanding..."
    watch_out: "Attractor basins use specific marker format..."
```

## Slug System

All palace elements have deterministic slugs for cross-agent communication:
- **Entities**: `memorykeeper`, `schedulingkeeper`
- **Rooms**: `memory-add-message` (file-function pattern)
- **Buildings**: `memory` (file stem)
- **Regions**: `backend` (directory)

Path format: `{region}/{building}/{room}` → `backend/memory/memory-add-message`

Slugs survive regeneration - same codebase produces same slugs.

## Sub-Palaces

Each major directory has its own sub-palace:
- `backend/.mind-palace/` - Python backend
- `admin-frontend/.mind-palace/` - React admin UI
- `tui-frontend/.mind-palace/` - Textual TUI
- `mobile-frontend/.mind-palace/` - React Native mobile

Root `.mind-palace/` contains shared entities (Keepers). Sub-palaces contain regions/buildings/rooms for their scope.

## Usage Examples

**Before modifying the scheduler:**
1. Read `.mind-palace/entities/schedulingkeeper.yaml`
2. Check topics for "day phases", "phase queues", "decision engine"
3. Note the WATCH_OUT warnings

**Understanding memory system:**
1. Read `.mind-palace/entities/memorykeeper.yaml`
2. Topics cover semantic search, hierarchical retrieval, journals, context sources

**Finding the right entity:**
1. Grep `.mind-palace/entities/*.yaml` for keyword
2. Read matched entity for full context

## Files

- `.mind-palace/palace.yaml` - Palace index with entity list
- `.mind-palace/entities/*.yaml` - Individual entity definitions
- `backend/mind_palace/` - Palace implementation code
