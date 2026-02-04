---
name: zotero-search
description: Search and retrieve documents from the user's local Zotero library using the Pyzotero CLI. **Claude code only** - requires connection to local Zotero instance. This skill should be used when the user asks to search their Zotero library, find papers or references, or query their personal research collection. Returns rich metadata including titles, authors, dates, abstracts, and bibliographic information with local file paths.
---

# Zotero Search

## Overview

**⚠️ CLAUDE CODE ONLY** - This skill requires Claude code as it connects to a local Zotero instance running on localhost. It will not work in web Claude at claude.ai.

This skill enables searching and retrieving documents from the user's local Zotero library using the Pyzotero command-line interface. It provides comprehensive search capabilities across titles, full-text content, metadata, authors, collections, and item types.

**Future possibility:** The skill could be extended to support Zotero's Web API for use in web Claude, but this would require API credentials (library ID and API key).

## Prerequisites

**Requirements:**
- Python ≥3.9
- Python 3.14 is not yet supported
- Pyzotero ≥1.7.3 with CLI support
- Claude Code (this skill does not work in web Claude)
- Zotero desktop application running locally with local API enabled

**Installation check:**
```bash
pyzotero test
```

If Pyzotero is not installed, or if the version is too low (`pyzotero --version` to check), install it using:
```bash
uv tool install "pyzotero[cli]" --upgrade
```

**Alternative:** Run without permanent installation using:
```bash
uvx --from "pyzotero[cli]" pyzotero search -q "your query"
pipx run --spec "pyzotero[cli]" pyzotero search -q "your query"
```
The second prerequisite is the Zotero desktop application running locally, with local API enabled. Test by calling:

```bash
pyzotero test
```
The response will be either success:

```text
✓ Connection successful: Zotero is running and listening locally.
  Received expected empty settings response.
```
or failure:

```text
✗ Connection failed: Could not connect to Zotero.

Possible causes:
  • Zotero might not be running
  • Local connections might not be enabled

To enable local connections:
  Zotero > Settings > Advanced > Allow other applications on this computer to communicate with Zotero
```

In case of failure, **pass the failure message on the user and ask them to tell you when they've fixed the problem, then try again**. In case of success, the skill is ready to use.

If the user is on web Claude, inform them that this skill requires Claude Code to access the local Zotero library. Do not continue after this as the skill cannot run.

## Quick Start

When the user asks to search their Zotero library, use the `pyzotero` CLI with appropriate commands. The CLI can output either human-readable text or JSON format. It will output a 'count' field showing the number of returned results.

**Basic search example:**
```bash
pyzotero search -q "climate adaptation"
```

**JSON output for structured data:**
```bash
pyzotero search -q "climate adaptation" --json
```

## Search Capabilities

### 1. Basic Query Search

Search across titles and metadata using the `-q` parameter.

**When to use:** User provides a topic, keyword, or phrase to search for.

**Examples:**
```bash
# Basic search
pyzotero search -q "machine learning"

# Get JSON output for structured processing
pyzotero search -q "machine learning" --json
```

### 2. Full-Text Search

Search across all content including full-text of PDFs using the `--fulltext` flag.

**When to use:** User wants to search within document contents, not just titles and metadata.

**Example:**
```bash
pyzotero search -q "climate change" --fulltext
```

**Note:** Full-text search is more comprehensive but may be slower and requires Zotero to have indexed the document contents.

### 3. Filter by Item Type

Restrict search to specific document types using `--itemtype` (can be specified multiple times).

**When to use:** User specifies "articles", "books", "papers", or other document types.

**Common item types:**
- `journalArticle` - Journal articles
- `book` - Books
- `bookSection` - Book chapters
- `conferencePaper` - Conference papers
- `report` - Technical reports
- `thesis` - Theses and dissertations

**List all available item types:**
```bash
pyzotero itemtypes
```

**Examples:**
```bash
# Search only journal articles
pyzotero search -q "neural networks" --itemtype journalArticle

# Search books and book chapters
pyzotero search -q "methodology" --itemtype book --itemtype bookSection

# Multiple types with JSON output
pyzotero search -q "climate" --itemtype journalArticle --itemtype conferencePaper --json
```

**Important:** If the user doesn't specify an item type, prompt them whether they want to search all items or filter by type (articles, books, etc.). Consider running `pyzotero itemtypes` first to show available options.

### 4. Search Within Collections

Search within a specific Zotero collection using `--collection`.

**When to use:** User mentions searching within a specific collection or folder.

**Example:**
```bash
# Search within a collection (requires collection key)
pyzotero search --collection ABC123 -q "adaptation"
```

**Finding collection keys:**
```bash
# List all collections with their keys
pyzotero listcollections
```

**Workflow:** If user mentions a collection by name, first run `pyzotero listcollections` to find the collection key, then search within it.

### 5. Limiting Results

Control the number of results with the `--limit` parameter.

**When to use:** User wants more/fewer results, or initial search returns too many items.

**Example:**
```bash
pyzotero search -q "adaptation" --limit 10
```

### 6. Combining Search Parameters

All search parameters can be combined for precise queries.

**Examples:**
```bash
# Full-text search in journal articles, limited results
pyzotero search -q "CRISPR" --fulltext --itemtype journalArticle --limit 20

# Search within collection with item type filter
pyzotero search --collection ABC123 -q "climate" --itemtype book --json

# Multiple item types with full-text search
pyzotero search -q "renewable energy" --fulltext --itemtype journalArticle --itemtype conferencePaper
```

## Output Format

### Human-Readable Output (Default)

By default, the CLI outputs formatted text with:
- Title, authors, date, publication
- Volume, issue, DOI, URL
- PDF attachments with **local file paths**
- Key metadata fields

**When to use:** For casual queries or when user wants readable output.

### JSON Output (`--json` flag)

Structured JSON with complete metadata for each item. It has the following structure:

```
{
    "count": len(output_items),
    "items": output_items
}
```

**When to use:** 
- Need to process results programmatically
- Want complete metadata
- Need to extract specific fields
- Building reports or analyses

**Example JSON structure:**
```json
{
  "key": "ABCD1234",
  "itemType": "journalArticle",
  "title": "Article Title",
  "creators": [
    {"creatorType": "author", "firstName": "John", "lastName": "Doe"}
  ],
  "date": "2023-05-15",
  "publicationTitle": "Journal Name",
  "volume": "42",
  "issue": "3",
  "pages": "123-145",
  "DOI": "10.1234/example",
  "abstractNote": "Full abstract text...",
  "tags": [{"tag": "keyword1"}, {"tag": "keyword2"}],
  "url": "https://...",
  "attachments": [
    {"path": "/path/to/local/file.pdf", "title": "Full Text PDF"}
  ]
}
```

## Presenting Results to User

Format search results for readability based on result count:

**For 1-10 results:** Show full details for each
- Title (with author, year)
- Publication venue
- Abstract (first 2-3 sentences if lengthy)
- DOI or URL
- Local file path (if available)
- If it wasn't a full-text search, point out that this may yield more results

**For 11-20 results:** Show condensed format
- Title, authors, year
- Publication venue
- Local file path

**For 21+ results:** Provide overview
- Total count and brief summary
- Group by theme/category if applicable
- Show top 5-10 most relevant results
- Offer to show more details or refine search

**Always include:**
1. Total result count at the start ("Found 12 journal articles")
2. Local file paths when PDFs are attached (highly useful for user)
3. Offer to refine search if results seem too broad or narrow

Adapt format based on context and user needs — these are sensible defaults.

## After Initial Search: Proactive Analysis

After presenting search results, analyze findings and suggest productive next steps. Initially, offer to act as a research assistant, not just a command executor.

**Pattern Recognition - Always do this:**
1. Identify themes or clusters in results
2. Notice temporal patterns (date ranges, gaps)
3. Check for missing expected work or authors
4. Assess coverage (methodologies, perspectives, geographies)

**Suggest Next Steps Based on Findings:**

**If results show clear themes:**
- "These 15 papers cluster into 3 approaches: [A], [B], [C]. Want me to break down each cluster?"
- "I notice 2 distinct debates here. Want to explore each separately?"

**If temporal patterns emerge:**
- "Most papers are from 2020-2023. Want to search for earlier foundational work?"
- "There's a gap from 2015-2018. Want to search that period specifically?"

**If coverage seems incomplete:**
- "These are all quantitative studies. Want to search for qualitative approaches?"
- "All papers are from Western contexts. Want to search for [other region] research?"
- "I see methodological papers but few empirical applications. Want to find applications?"

**If specific authors dominate:**
- "5 papers by [Author]. Want to find other perspectives or critiques?"
- "Several papers cite [Key Author]. Want to search for their work?"

**If PDFs are missing:**
- "Only 4 of 12 papers have PDFs attached. Want me to identify which are missing?"

**If results are too broad:**
- "Got 47 results. Want to filter by time period, item type, or add more specific terms?"

**If results are too narrow:**
- "Only 2 results. Try broader terms, remove filters, or use full-text search?"

**Research workflow suggestions:**
- "Ready to do a thematic analysis of these results?"
- "Want me to identify gaps in this literature?"
- "Should we create a reading priority list?"
- "Want to track how thinking evolved over time?"

**Remember user feedback*:*
- Don't be too pushy, overeager, or obseqious. Act like a diligent postdoc
- Remember the user's directives in this regard: they may want you to "just" act as a search conduit, or do extensive analysis, or anything in between – respect their choice, but allow them to change their mind.

## Advanced Research Workflows

For comprehensive research analysis patterns, set operations, processing recipes, and full-text integration workflows, see **[references/research-workflows.md](references/research-workflows.md)**.

That reference file provides detailed guidance on:

**Research Analysis Patterns:**
- Thematic Clustering - Group papers by theme/approach
- Gap Analysis - Identify what's missing or underexplored
- Research Trajectory Analysis - Track how thinking evolved over time
- Methodological Survey - Understand research approaches in the field
- Reading List Prioritization - Create tiered reading lists

**Set Operations:**
- Intersection (papers about BOTH A AND B)
- Union (papers about A OR B)
- Difference (papers about A but NOT B)
- Temporal filtering

**Processing Recipes:**
- Group by year, author, item type
- Find papers without PDFs
- Extract unique authors
- Identify collaborative work

**Full-Text Integration:**
- Evidence extraction workflows
- Comparative deep dives
- Methodology learning
- When to read PDFs vs. stay with metadata

Use these workflows when basic search + proactive suggestions aren't sufficient for the user's research needs.

## Workflow Decision Tree

1. **User mentions searching Zotero?** → Use this skill
2. **Verify Desktop Claude** → If web Claude, inform limitation and stop
3. **Check Pyzotero and Zotero availability** → Run `pyzotero test`. If it fails, inform user
4. **Determine search parameters:**
   - What is the query/topic?
   - Should search be full-text or metadata-only?
   - Should results be filtered by item type?
   - Is this within a specific collection?
   - How many results needed?
   - JSON output or human-readable?
5. **Execute search** using `pyzotero search` with appropriate flags
6. **Present results** following the "Presenting Results to User" guidelines
7. **Analyze patterns** (see "After Initial Search: Proactive Analysis"):
   - Identify themes, temporal patterns, coverage
   - Note what's present and what's missing
8. **Suggest next steps** based on analysis:
   - Refinement options if too broad/narrow
   - Research analysis patterns if appropriate
   - Set operations if comparing concepts
   - Reading prioritization if many results
9. **Iterate** based on user's chosen direction

## Common Usage Patterns

**Pattern 1: Basic exploratory search**
```
User: "Search my Zotero for papers about ocean acidification"
→ pyzotero search -q "ocean acidification" --itemtype journalArticle --json
→ Present results
→ Analyze: "Found 12 papers. I notice 3 focus on coral reefs, 8 on broader marine ecosystems, 
   and 1 on economic impacts. Most are from 2018-2023. Want me to break down each cluster?"
```

**Pattern 2: Full-text search with gap analysis**
```
User: "Find everything in my library that mentions 'adaptation strategies'"
→ pyzotero search -q "adaptation strategies" --fulltext --json
→ Present results
→ Analyze: "Found 23 papers, but all are from developed countries. Want to search for 
   developing world contexts? Also, these are all climate-focused—want to broaden to other risks?"
```

**Pattern 3: Advanced research workflow**
```
User: "What do I have about neural networks? I need to understand the landscape."
→ pyzotero search -q "neural networks" --json
→ Present results with initial analysis
→ Suggest: "Found 18 papers. Want me to do a thematic clustering? Or track how thinking 
   evolved over time? Or create a prioritized reading list?"
→ If user wants any advanced analysis, use patterns from references/research-workflows.md
```

**For more complex research workflows** (comparative searches, set operations, thematic analysis, reading list prioritization, etc.), see patterns in **references/research-workflows.md**.

## Helper Commands

### List Collections
```bash
pyzotero listcollections
```
Shows all collections with their keys and names. Use this when user refers to a collection by name to find its key.

### List Item Types
```bash
pyzotero itemtypes
```
Shows all available item types that can be used with `--itemtype`. Use this when user is unsure what types to search for.

## Error Handling

If commands fail:
- **"Connection error"** → Check if Zotero desktop application is running
- **"Command not found"** → Verify Pyzotero CLI is installed: `uv tool install "pyzotero[cli]" --upgrade`
- **"No results"** → Try:
  - Removing item type filters
  - Using full-text search with `--fulltext`
  - Broadening the query
  - Checking collection key with `pyzotero listcollections`

## Tips for Research-Focused Use

1. **Act as research assistant, not just command executor**: After searches, analyze patterns, suggest next steps, offer insights

2. **Start broad, then narrow iteratively**: Initial search reveals landscape, then refine based on what you find

3. **Combine search with analysis**: Don't just return results—identify themes, gaps, trajectories

4. **Use advanced workflows when appropriate**: For complex research tasks, consult **references/research-workflows.md** for set operations, thematic analysis, reading prioritization, and more

5. **Always use `--json` for analysis workflows**: Processing recipes require structured data

6. **Leverage local file paths for deep dives**: When key papers emerge, read the PDFs directly using the local paths

7. **Suggest rather than wait**: Offer thematic analysis, gap identification, prioritization—don't wait to be asked

8. **Track patterns across searches**: Note what appears repeatedly, what's surprisingly absent, what conflicts

9. **Group and count everything**: When categorizing, always show counts per category

10. **Be proactive about next steps**: Every search result should include suggested follow-up directions.
