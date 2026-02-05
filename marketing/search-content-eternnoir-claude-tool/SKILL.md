---
name: search-content
description: Search and navigate knowledge base using README.md indexes, pattern matching, and directory tree analysis. Use when user searches for files, topics, mentions "where is", "find", "search for", or asks content location queries.
---

# Search Content Skill

Navigate and search the knowledge base efficiently using AkashicRecords directory governance structure.

## When to use this Skill

- User asks "where is", "find", "search for"
- User queries file locations
- User looks for specific topics or content
- User needs to navigate knowledge base
- User asks "do I have notes about..."

## Workflow

### 1. Analyze Query

**Parse user request**:
- Extract keywords and topics
- Identify search scope (specific directory or entire knowledge base)
- Determine search type (filename, content, topic, date-based)
- Assess query specificity (exact match vs fuzzy search)

**Examples**:
```
"Where are my transformer notes?" → Topic search, keyword: "transformer"
"Find files modified last week" → Date-based search
"Search for 'attention mechanism' in Research" → Content search, scoped to Research/
"List all meeting notes from October" → Category + date search
```

### 2. Choose Search Strategy

Select appropriate strategy based on query:

#### Strategy 1: Structured Navigation (Preferred)
**When to use**:
- Query mentions directory names (Work, Research, Personal, etc.)
- Looking for specific categories or types
- Query has clear organizational clues

**Method**:
- Start at root README.md or specified directory
- Follow directory index structure
- Use README.md files as curated navigation guides
- Narrow down systematically

**Advantages**:
- Fast and efficient
- Leverages existing organization
- Follows curated structure

#### Strategy 2: Pattern Search
**When to use**:
- Looking for filenames matching patterns
- User provides specific naming clues
- Need to find files by naming convention

**Method**:
- Use Glob for filename patterns: `**/*keyword*.md`
- Filter by date if needed: files modified in last N days
- Use multiple patterns for comprehensive search

**Advantages**:
- Direct filename matching
- Fast for filename-based queries
- Good for date-based searches

#### Strategy 3: Deep Content Search
**When to use**:
- Looking for specific text or code within files
- Pattern/structured search insufficient
- Need comprehensive text search

**Method**:
- Use Grep for content search: `grep -r "keyword" .`
- Search within specific file types
- Use Task subagent for complex multi-step searches

**Advantages**:
- Finds content regardless of organization
- Comprehensive coverage
- Good for forgotten file locations

### 3. Execute Search

**Structured Navigation example**:
```
User: "Find my AI research notes"

1. Start at root, read README.md
2. Identify Research/ directory (purpose: "Technical and academic research")
3. Read Research/README.md
4. Find AI/ or DeepLearning/ subdirectories
5. Read Research/AI/README.md
6. List all files in index
7. Filter by relevance
8. Return matching files
```

**Pattern Search example**:
```
User: "Find files about transformers"

1. Use Glob: `**/*transformer*.md`
2. Results:
   - Research/AI/2025-10-28-transformer-architecture.md
   - Research/AI/2025-10-20-transformer-applications.md
   - Work/Projects/transformer-project.md
3. Rank by modification date (most recent first)
4. Return results
```

**Deep Content Search example**:
```
User: "Search for 'attention mechanism'"

1. Use Grep: grep -r "attention mechanism" . --include="*.md"
2. Results (with context):
   - Research/AI/transformer-architecture.md (3 matches)
   - Research/AI/neural-networks.md (1 match)
3. Extract surrounding context for each match
4. Rank by relevance (match count, recency)
5. Return results with context snippets
```

### 4. Check Governance

**For each result**:
1. Check directory RULE.md for read permissions
2. Skip files in restricted directories
3. Note if file requires special access

**Permission check**:
```
RULE.md says: "Restricted access - confidential"
→ Skip this file or warn user about restrictions
```

**Privacy considerations**:
- Respect RULE.md access restrictions
- Don't expose content from restricted directories
- Warn if search includes restricted areas

### 5. Rank Results

**Ranking criteria**:
1. **Relevance**: Keyword matches, topic similarity
2. **Recency**: Recently modified files ranked higher
3. **Location**: Files in expected directories ranked higher
4. **Completeness**: README.md-indexed files ranked higher (curated)

**Scoring example**:
```
File A: transformer-architecture.md
- Title match: +50
- Recent (3 days): +30
- In expected directory (Research/AI): +20
- Listed in README: +10
- Total: 110

File B: old-notes.md
- Content match only: +30
- Old (3 months): +5
- In Miscellaneous: +10
- Not in README: +0
- Total: 45

Result order: File A, then File B
```

### 6. Present Results

**Clear result format**:
```
📚 Search results for "[query]"

Found [X] matches:

1. [filename.md](path/to/file.md) ★★★★☆
   Location: [directory path]
   Last modified: [date]
   Description: [from README.md or first line]
   Match: [Context snippet if content search]

2. [another-file.md](path/to/another.md) ★★★☆☆
   Location: [directory path]
   Last modified: [date]
   Description: [description]
   Match: [Context snippet]

[More results...]

Didn't find what you need?
- Try broader keywords
- Search in specific directory
- Check Archive/ for old content
```

**Include helpful metadata**:
- File location (full path)
- Last modified date
- Brief description from README.md
- Relevance score (stars or percentage)
- Context snippet (for content searches)

### 7. Follow-up Options

**After presenting results**:
```
What would you like to do?
- Read [filename]
- Search within these results
- Refine search with different keywords
- Search in different directory
- Show more results
```

**Interactive refinement**:
- User can narrow down results
- Ask follow-up questions
- Navigate to related files
- Explore directory structure

## Search Strategies in Detail

### Structured Navigation

**Step-by-step process**:
1. Identify starting point (root or specific directory)
2. Read starting README.md
3. Parse directory structure from README.md
4. Match query keywords to directory names/descriptions
5. Descend into most relevant subdirectory
6. Repeat until finding target files
7. List files from README.md index

**Example**:
```
Query: "Find meeting notes from October"

1. Read root README.md
2. Find Work/ directory
3. Read Work/README.md
4. Find Meetings/ subdirectory
5. Read Work/Meetings/README.md
6. Filter entries by date (October)
7. Return matching files
```

**Advantages**:
- Leverages human-curated organization
- Fast and efficient
- Follows logical structure

**Limitations**:
- Requires good README.md maintenance
- May miss files not indexed
- Depends on consistent organization

### Pattern Search

**Glob patterns**:
```
**/*keyword*.md           → Find files with "keyword" in name
**/*YYYY-MM-DD*.md       → Find files with specific date format
Research/**/*.md          → Find all markdown in Research/
Work/Projects/**/*.md     → Find all markdown in Work/Projects/
```

**Advanced patterns**:
```
**/{transformer,attention,neural}*.md  → Multiple keywords
**/*2025-10*.md                        → October 2025 files
**/*.{md,txt}                          → Multiple extensions
```

**Date-based search**:
```bash
# Files modified in last 7 days
find . -name "*.md" -mtime -7

# Files modified in October 2025
find . -name "*2025-10*.md"
```

**Advantages**:
- Direct filename matching
- Fast execution
- Good for date/name patterns

**Limitations**:
- Only searches filenames
- Misses content matches
- Requires knowing naming conventions

### Deep Content Search

**Grep search**:
```bash
# Basic content search
grep -r "keyword" . --include="*.md"

# Case-insensitive
grep -ri "keyword" . --include="*.md"

# Multiple keywords (OR)
grep -rE "keyword1|keyword2" . --include="*.md"

# With context lines
grep -r "keyword" . --include="*.md" -A 2 -B 2
```

**Task subagent for complex searches**:
```
User: "Find all notes about transformers that mention attention mechanism and were created in the last month"

→ Too complex for single grep
→ Invoke Task subagent:
  1. Grep for "transformer"
  2. Filter results by "attention mechanism"
  3. Filter by date (last month)
  4. Return consolidated results
```

**Advantages**:
- Comprehensive text search
- Finds content regardless of location
- Good for forgotten file locations

**Limitations**:
- Slower than other methods
- May return too many results
- High context consumption (use Task subagent for complex cases)

## Search Optimization

### Start Specific, Expand if Needed

**Progression**:
1. Try structured navigation first (if logical directory exists)
2. If no results: try pattern search
3. If still no results: try deep content search
4. If still nothing: suggest broader keywords or check Archive/

**Example**:
```
Query: "Find transformer notes"

1. Structured: Check Research/AI/README.md → Found 2 files ✅
2. Pattern: Not needed (found with structured)
3. Content: Not needed

vs.

Query: "Find notes about neural attention"

1. Structured: Check Research/AI/README.md → No exact match
2. Pattern: **/*attention*.md → Found 1 file
3. Content: grep "neural attention" → Found 3 more files
4. Combined results, ranked by relevance
```

### Use README.md as Primary Index

**README.md advantages**:
- Curated by user (most important files listed)
- Includes descriptions (better context)
- Organized logically (related files grouped)
- Faster than filesystem traversal

**Always check README.md first** before deep searches.

### Minimize Context Consumption

**For simple searches**:
- Use Glob/Grep directly
- Return results without reading full files
- Only read files user wants to open

**For complex searches**:
- Use Task subagent to handle complexity
- Subagent consumes context, not main agent
- Return only summarized results to user

## Error Handling

### No Results Found
```
Query: "Find transformer notes"
→ No matches in any strategy

→ Response:
"I couldn't find notes about transformers.

Suggestions:
- Try broader keywords (AI, neural networks)
- Search in Archive/ for old content
- Check if files use different terminology
- Create new note if content doesn't exist"
```

### Too Many Results
```
Query: "Find notes"
→ Returns 500+ matches

→ Response:
"Found 500+ files matching 'notes'.

Please narrow your search:
- Add more specific keywords
- Specify directory (Research, Work, Personal)
- Add date filter (from last week, October, etc.)
- Provide more context about what you're looking for"
```

### Ambiguous Query
```
Query: "Find it"
→ Query too vague

→ Response:
"Could you provide more details?

What are you looking for?
- File name or topic keywords
- Approximate date or time period
- Which directory (Research, Work, etc.)
- Type of content (meeting notes, research, etc.)"
```

### Permission Denied
```
Search encounters restricted directory
RULE.md: "Access restricted"

→ Skip directory in results
→ Note: "Some directories were excluded due to access restrictions"
```

## Integration with Governance

This Skill respects directory governance:

**Before searching**:
- Check RULE.md for search permissions
- Respect access restrictions
- Note privacy constraints

**During search**:
- Skip restricted directories
- Follow governance rules
- Maintain confidentiality

**In results**:
- Only show accessible files
- Note if restricted areas skipped
- Respect RULE.md read permissions

## Examples

### Example 1: Topic Search

**User**: "Where are my transformer architecture notes?"

**Skill workflow**:
1. Analyzes query → Topic: transformer architecture
2. Chooses structured navigation (research topic)
3. Reads root README.md → Finds Research/
4. Reads Research/README.md → Finds AI/
5. Reads Research/AI/README.md
6. Finds 2 matches:
   - transformer-architecture.md (3 days ago)
   - transformer-applications.md (2 weeks ago)
7. Ranks by recency
8. Presents results with descriptions

### Example 2: Date-Based Search

**User**: "Find my meeting notes from last week"

**Skill workflow**:
1. Analyzes query → Category: meetings, Date: last week
2. Chooses structured navigation + date filter
3. Reads root README.md → Finds Work/
4. Reads Work/README.md → Finds Meetings/
5. Reads Work/Meetings/README.md
6. Filters entries by date (last 7 days)
7. Finds 3 meetings
8. Presents chronologically

### Example 3: Content Search

**User**: "Search for 'attention mechanism' in my notes"

**Skill workflow**:
1. Analyzes query → Content search, keyword: "attention mechanism"
2. Chooses deep content search
3. Executes: `grep -ri "attention mechanism" . --include="*.md"`
4. Finds 5 matches across 3 files
5. Extracts context snippets
6. Checks RULE.md permissions for each file
7. Ranks by relevance (match count + recency)
8. Presents with context snippets

## Best Practices

1. **Start with structured navigation** - Fastest and most relevant
2. **Use README.md indexes** - Curated by user, most important
3. **Minimize context** - Don't read files unless needed
4. **Rank results meaningfully** - Relevance + recency + location
5. **Provide context** - Show why files matched
6. **Offer follow-up** - Help user refine search
7. **Respect governance** - Check RULE.md permissions
8. **Handle edge cases** - No results, too many results, ambiguous queries

## Notes

- This Skill works with any directory structure
- Leverages README.md indexes for curated navigation
- Uses multiple search strategies for comprehensive coverage
- Respects RULE.md governance and access restrictions
- Minimizes context consumption with Task subagent for complex searches
- Works in parallel with CLAUDE.md subagents independently
- Provides interactive refinement for better results
