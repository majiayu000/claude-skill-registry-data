---
name: codecompanion-memory
description: Search through previous CodeCompanion chat conversations using semantic search. Use this skill when the user mentions past conversations, asks "do you remember", or when historical context from previous sessions would help solve the current problem.
allowed-tools: Bash, mcp__acp__Read, Skill
---

# CodeCompanion Memory Skill

This skill provides access to a searchable history of previous CodeCompanion conversations stored in a ChromaDB vector database. It uses semantic search to find relevant past conversations based on natural language queries.

## When to Use This Skill

Invoke this skill when:

- **User references past conversations**: Phrases like "we discussed this before", "remember when", "last time we talked about"
- **Recurring problems**: The user encounters an issue that might have been solved previously
- **Context would be helpful**: Previous solutions, decisions, or architectural discussions could inform the current task
- **User asks about their codebase**: Questions about past work, project history, or previous implementations
- **Building on previous work**: Extending or modifying solutions from past conversations

## Usage

```bash
~/.claude/skills/codecompanion-memory/query.sh --query "your search query"
```

### Parameters

- `--query TEXT` or `-q TEXT`: The search query (required)
  - Use natural language
  - Be specific but not too narrow
  - Examples: "fixing Docker networking", "Go error handling patterns", "setting up ChromaDB"

- `--count NUMBER` or `-n NUMBER`: Number of results to return (default: 5)
  - More results = more context but also more noise
  - Recommended: 3-5 for focused queries, 10+ for exploratory searches

- `--verbose` or `-v`: Show full document content
  - Without this flag, only previews (first 200 chars) are shown
  - Use when you need to read the full conversation summary

- `--project PATH` or `-p PATH`: Override default project root (default: ~/codecompanion-history/summaries)

- `--help` or `-h`: Show help message

## Example Queries

### Finding Past Solutions

```bash
# User: "I'm getting a CORS error, have we dealt with this before?"
~/.claude/skills/codecompanion-memory/query.sh \
  --query "CORS error HTTP request" \
  --count 3
```

### Architectural Decisions

```bash
# User: "What database did we choose for the user service?"
~/.claude/skills/codecompanion-memory/query.sh \
  --query "database choice user service" \
  --count 5 \
  --verbose
```

### Code Patterns

```bash
# User: "How did I implement authentication last time?"
~/.claude/skills/codecompanion-memory/query.sh \
  --query "authentication implementation pattern" \
  --count 3 \
  --verbose
```

## Output Format

Results are displayed in order of relevance:

```
Searching in: /home/djipey/codecompanion-history/summaries
Query: Arduino

--- Result 1 ---
Path: 1759511459.md
Preview: ## Code Context
**Files Modified**: ardoise.ino (main focus: refactoring BLE write logic)...

--- Result 2 ---
Path: 1759512219.md
Preview: ## Code Context
**Files Modified**: ardoise.ino (main Arduino sketch)...
```

Each result includes:
- **Path**: The markdown file containing the full conversation summary
- **Preview/Document**: Either a short preview or full content (with `--verbose`)

You can read the full conversation summary files at:
`~/codecompanion-history/summaries/<chat_id>.md`

## How It Works

```
User Query
    ↓
Bash Script (query.sh)
    ↓
VectorCode CLI
    ↓
ChromaDB (local instance)
    ↓
Semantic Search Results
```

The skill:
1. Wraps the VectorCode CLI tool
2. Queries a local ChromaDB database
3. Uses semantic embeddings (SentenceTransformer)
4. Returns results sorted by relevance

## Database Information

- **Database Location**: `~/.local/share/vectorcode/chromadb/chroma.sqlite3`
- **Summaries**: `~/codecompanion-history/summaries/*.md`
- **Embedding Model**: SentenceTransformer (all-MiniLM-L6-v2)

The database uses **semantic embeddings**, meaning:
- Queries find conceptually similar content, not just keyword matches
- Synonyms and related terms are automatically understood
- Context and meaning are preserved across different phrasings

## Installation

The skill is installed at `~/.claude/skills/codecompanion-memory/`.

If you need to reinstall or update:

```bash
mkdir -p ~/.claude/skills/codecompanion-memory

# Copy required files from source
cp /path/to/source/SKILL.md \
   ~/.claude/skills/codecompanion-memory/
cp /path/to/source/query.sh \
   ~/.claude/skills/codecompanion-memory/

# Make script executable
chmod +x ~/.claude/skills/codecompanion-memory/query.sh
```

## Dependencies

- `bash`: Shell interpreter
- `python3`: For JSON parsing in the script
- `vectorcode`: CLI tool for querying ChromaDB

### Installing VectorCode

If VectorCode is not installed:

```bash
# Using pipx (recommended)
pipx install vectorcode

# Or using pip
pip install --user vectorcode

# Verify installation
which vectorcode
```

## Performance

- **First query**: ~3s (VectorCode cold start)
- **Subsequent queries**: ~1-2s
- **Memory usage**: ~150MB (VectorCode + ChromaDB server)
- **Disk space**: ~3KB (just the script)

## Troubleshooting

### "vectorcode command not found"

```bash
# Install VectorCode
pipx install vectorcode

# Or check installation
which vectorcode
```

### "No results found"

- Try broader queries: "Docker" instead of "Docker Compose networking with custom bridge"
- Check if conversations are indexed: `ls ~/codecompanion-history/summaries/`
- Verify database exists: `ls ~/.local/share/vectorcode/chromadb/`

### VectorCode configuration

If you have a ChromaDB Docker container and want VectorCode to use it, create:

```bash
# ~/codecompanion-history/summaries/.vectorcode.toml
[default]
db_url = "http://localhost:8001"
db_path = ""
```

Note: The skill works fine with VectorCode's default local database.

## Best Practices

1. **Start broad, then narrow**: Begin with general queries, then refine based on results
2. **Use verbose mode selectively**: Only when you need full context to answer the user's question
3. **Combine with code search**: This skill finds conversations; use code search tools to find actual implementations
4. **Cite your sources**: Tell the user which conversation(s) you found the information in
5. **Verify information**: Past solutions might be outdated; always validate before applying

## Example Workflow

```
User: "I'm stuck on the same authentication bug we had last month"

Step 1: Search for relevant conversations
→ ./query.sh --query "authentication bug fix" --count 5

Step 2: Review results, identify the most relevant conversation
→ Result 3 seems most relevant (Path: 1763841695.md)

Step 3: Read full summary if needed
→ cat ~/codecompanion-history/summaries/1763841695.md

Step 4: Apply the solution or adapt it to current context

Step 5: Inform user
→ "I found a similar issue we solved in conversation 1763841695. 
   The problem was related to session token expiration. 
   Here's what we did..."
```

## Technical Details

### Script Implementation

The skill is a simple Bash wrapper that:
1. Validates and parses command-line arguments
2. Calls `vectorcode query` with appropriate parameters
3. Formats the JSON output for display
4. Handles errors gracefully

### Why VectorCode?

VectorCode handles:
- ChromaDB connection and configuration
- Embedding generation for queries
- Collection management
- Query execution

This makes the skill implementation simple and reliable.

## Integration Notes

This skill is designed to work seamlessly with Claude Code's skill system:
- Automatically loaded when referenced or when the user mentions past conversations
- Runs independently without blocking other operations
- Returns structured data that can be easily parsed and presented to the user

---

**Status**: ✅ Production ready  
**Location**: `~/.claude/skills/codecompanion-memory/`  
**Last Updated**: 2025-12-15
