---
name: google-search-skill
description: Perform Google searches to retrieve up-to-date information from the web. Use when users need current information, latest news, technical trends, documentation lookups, or general web searches that require real-time data beyond your knowledge cutoff.
allowed-tools: Bash(python:*)
---

# Google Search Skill

## Overview

This Skill enables Claude to perform Google searches using the `google_search_tool` command-line interface. It retrieves current web information, making it ideal for answering questions that require up-to-date data, recent news, or information beyond Claude's knowledge cutoff.

## When to Use This Skill

Use this Skill when:
- Users ask for current events, news, or recent information
- Questions require the latest technical documentation or API references
- Looking up current prices, statistics, or data
- Finding resources, tutorials, or guides on specific topics
- Verifying facts or getting multiple perspectives from web sources
- Users explicitly request a web search or Google search

## Instructions

When performing a web search, follow these steps:

### 1. Identify the Search Query

- Extract the key search terms from the user's request
- Formulate a clear, concise search query
- Use specific keywords for better results
- Include relevant technical terms, product names, or specific phrases

### 2. Execute the Search

Run the search using the google_search_tool:

```bash
python -m google_search_tool "your search query" --pretty
```

**Options:**
- Use `--pretty` for formatted JSON output (easier to read)
- Use `-n <number>` to specify number of results (1-10, default: 10)
- For focused searches, use `-n 3` or `-n 5`

**Examples:**
```bash
# General search with 5 results
python -m google_search_tool "Python 3.13 new features" -n 5 --pretty

# Focused search with 3 results
python -m google_search_tool "React hooks tutorial" -n 3 --pretty

# Full search with 10 results
python -m google_search_tool "machine learning frameworks comparison" --pretty
```

### 3. Parse and Present Results

After receiving the search results:

1. **Check for errors**: If the output contains `"error"`, explain the error to the user
2. **Extract key information**: Parse the JSON output for `title`, `link`, and `snippet`
3. **Summarize findings**: Provide a concise summary of what you found
4. **Present sources**: List relevant results with titles and links
5. **Answer the question**: Use the search results to answer the user's original question

**Presentation format:**

```
Based on my search for "[query]", here's what I found:

[Summary of findings based on search results]

Key resources:
1. **[Title 1]** - [Brief description from snippet]
   [URL]

2. **[Title 2]** - [Brief description from snippet]
   [URL]

[Additional context or recommendations]
```

### 4. Handle Edge Cases

**No results found:**
```json
{
  "results": [],
  "count": 0
}
```
- Inform the user that no results were found
- Suggest trying different search terms
- Offer to search with alternative queries

**API error:**
```json
{
  "error": "Error message"
}
```
- Check if environment variables are set (GOOGLE_API_KEY, GOOGLE_CSE_ID)
- Explain the error to the user
- Suggest troubleshooting steps if applicable

**Timeout or network error:**
- Inform the user of the issue
- Offer to retry the search
- Suggest checking network connectivity

### 5. Follow-up Searches

If the initial search doesn't fully answer the question:
- Refine the search query based on initial results
- Perform additional targeted searches
- Combine information from multiple searches

## Examples

### Example 1: Current Events

**User request:** "What are the latest developments in AI this week?"

**Steps:**
1. Search: `python -m google_search_tool "latest AI developments 2025" -n 5 --pretty`
2. Parse the JSON results
3. Summarize key developments from the snippets
4. Present with source links

### Example 2: Technical Documentation

**User request:** "How do I use React Server Components?"

**Steps:**
1. Search: `python -m google_search_tool "React Server Components guide" -n 5 --pretty`
2. Identify official documentation and tutorials
3. Extract key concepts from snippets
4. Provide overview with links to detailed resources

### Example 3: Comparison Research

**User request:** "Compare PostgreSQL vs MySQL for large-scale applications"

**Steps:**
1. Search: `python -m google_search_tool "PostgreSQL vs MySQL large scale comparison" -n 5 --pretty`
2. Gather multiple perspectives from results
3. Synthesize comparisons from different sources
4. Present balanced view with source attribution

## Important Notes

### Environment Setup

The google_search_tool requires:
- `GOOGLE_API_KEY`: Google Cloud API key
- `GOOGLE_CSE_ID`: Custom Search Engine ID
- These should be set in the `.env` file in the project root

### Limitations

- Maximum 10 results per search
- API rate limits apply (check Google CSE quotas)
- Results depend on Google's indexing and ranking
- Snippets are truncated (may not contain full context)

### Best Practices

1. **Be specific**: Use precise search terms for better results
2. **Verify sources**: Check that URLs and snippets are relevant before citing
3. **Cite properly**: Always include source URLs when presenting information
4. **Respect recency**: Recent results may be more relevant for time-sensitive queries
5. **Multiple searches**: For complex topics, perform several targeted searches rather than one broad search

## Troubleshooting

If searches fail:
1. Verify the google_search_tool is installed: `pip show google-search-mcp`
2. Check environment variables are set in `.env`
3. Test manually: `python -m google_search_tool "test query" --pretty`
4. Review API quota limits in Google Cloud Console
5. Check network connectivity

## Integration with Other Tools

This Skill works well alongside:
- **Read** tool: After finding URLs, read local documentation
- **WebFetch** tool: Retrieve full content from found URLs
- **Write** tool: Save search results for later reference
