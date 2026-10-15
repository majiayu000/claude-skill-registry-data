---
name: recall
description: Cross-session search combining claude-mem semantic vector search with conversation history grep for comprehensive memory recall
type: skill
triggers:
  - /recall
  - When user asks to remember, recall, or search past conversations
  - When user references something from a previous session
---

# Cross-Session Recall

Search across all past conversations and memory to find context from any previous session.

## Search Strategy (3-Layer)

### Layer 1: claude-mem Semantic Search (Fastest, Most Relevant)
Use the `mcp__plugin_claude-mem_mcp-search__search` tool:
```
search(query="<user's search term>", limit=10)
```
Then fetch details for matching IDs:
```
get_observations([id1, id2, ...])
```
This searches the vector-indexed semantic memory (ChromaDB) for conceptually similar content.

### Layer 2: Memory File Search (Structured Facts)
Search the memory index at `~/.claude/projects/-Users-<YOUR_USER>/memory/MEMORY.md`:
- Grep MEMORY.md for keyword matches
- Read matching memory files for full context
- Check confidence-scored facts table for relevant entries

### Layer 3: Conversation History Search (Raw Transcripts)
Search session history files:
```bash
# Find all history files across projects
find ~/.claude/projects/ -name "history.jsonl" -type f 2>/dev/null

# Search for keyword matches (most recent first)
grep -l "<search_term>" ~/.claude/projects/*/history.jsonl 2>/dev/null
```

Note: history.jsonl files can be very large. Use grep to find matching lines, don't read entire files.

## Usage

```
/recall <search query>
```

### Examples
- `/recall security audit results from last week`
- `/recall what did we decide about the database migration`
- `/recall aster trading configuration`
- `/recall coremind architecture decisions`

## Output Format

For each result, show:
1. **Source**: claude-mem | memory-file | history
2. **Date**: When it was recorded
3. **Relevance**: How well it matches the query
4. **Content**: The actual recalled information
5. **Context**: Link to the memory file or session where it originated

## Rules

1. Always start with claude-mem semantic search (fastest, best relevance)
2. Fall back to memory files if semantic search returns <3 results
3. Only search history.jsonl as last resort (expensive, noisy)
4. Deduplicate results across layers
5. Sort by relevance, then recency
6. Show max 10 results unless user asks for more
7. If the user says to ignore memory, skip all layers and say so
