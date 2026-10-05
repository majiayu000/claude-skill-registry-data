---
name: wiki-query
description: "Query the wiki to answer questions. Searches wiki pages, synthesizes answers with citations, and optionally files valuable answers back as new wiki pages. Use when the user asks a question about the knowledge base."
allowed-tools: Read Write Edit Glob Grep
---

# Wiki Query

Answer questions by searching and synthesizing from the wiki.

## Workflow

### Step 1: Search the wiki
1. Read `memory/wiki/index.md` to find relevant pages
2. Use Grep to search for specific terms across `memory/wiki/`
3. Read the most relevant pages (usually 3-10)

### Step 2: Synthesize an answer
- Combine information from multiple wiki pages
- Cite sources: reference both wiki pages and the underlying raw documents
- Note confidence level — distinguish well-sourced claims from inferences
- Flag if the wiki has gaps on this topic

### Step 3: Present the answer
Format depends on the question:
- **Factual question** — direct answer with citations
- **Comparison** — markdown table comparing entities/concepts
- **Overview** — structured summary with sections
- **Analysis** — synthesis with explicit reasoning chain

### Step 4: File back (if valuable)
If the answer represents a useful synthesis that doesn't exist as a wiki page:

1. Ask the user: "This answer synthesizes information that isn't captured in the wiki yet. Should I file it as a new page?"
2. If yes: create a new wiki page in `memory/wiki/`
3. Update `memory/wiki/index.md`
4. Append to `memory/log.md`:
   ```
   ## [YYYY-MM-DD] query-filed | Page Title
   - Question: [original question]
   - Pages referenced: [list]
   - New page: memory/wiki/page-name.md
   ```

## Key Insight
Good answers should not disappear into chat history. A comparison you asked for, an analysis, a connection you discovered — these are valuable wiki content. Filing them back means your explorations compound in the knowledge base just like ingested sources do.
