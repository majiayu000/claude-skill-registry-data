---
name: research-reporter
description: This skill should be used when users request research on topics with compiled results saved to a file. It handles web searches, fetching authoritative sources, synthesizing information, and generating structured reports. Trigger phrases include "research and save", "search and summarize", "compile information about", or requests to investigate topics and save results.
---

# Research Reporter

## Overview

Automate the process of researching topics through web search and authoritative sources, then synthesize findings into well-structured reports saved to user-specified locations.

## When to Use This Skill

Use this skill when the user requests:
- Research on a topic with results saved to a file
- Web searches combined with report generation
- Information compilation from multiple sources
- Trend analysis or competitive research saved as documents
- Any "search and save" or "research and write" workflow

**Example trigger phrases:**
- "Research TypeScript trends and save to a file"
- "Search for information about X and compile it into a report"
- "Find the latest news on Y and save the summary"
- "Investigate Z and create a document with your findings"

## Research & Report Workflow

Follow this sequential workflow to execute research and reporting tasks effectively.

### Step 1: Identify Research Parameters

Extract the following from the user request:
- **Topic**: What to research (e.g., "TypeScript trends 2025")
- **Output Path**: Where to save the report (e.g., `/Users/user/Desktop/report.txt`)
- **Scope**: How comprehensive the research should be (default: 5-10 sources)
- **Format**: Report structure preference (default: structured markdown)

### Step 2: Execute Web Search

Use the `web_search` tool from `mcp_server_search` to gather initial information.

**Search strategy:**
1. Craft a comprehensive search query including:
   - Main topic keywords
   - Time qualifiers if relevant ("2024", "2025", "latest")
   - Specificity terms ("trends", "new features", "best practices")
2. Request 5-10 results for breadth
3. Review search results for relevant sources

**Code pattern:**
```python
import asyncio
from extensions.wrapped_mcp.mcp_server_search import web_search

async def main():
    search_results = await web_search({
        "query": "topic keywords with time qualifiers",
        "num_results": 5
    })
    print(search_results)

asyncio.run(main())
```

### Step 3: Fetch Authoritative Sources

Use the `fetch` tool from `mcp_server_fetch` to retrieve content from official or authoritative sources.

**Fetching strategy:**
1. Identify 1-3 authoritative URLs (official sites, documentation, reputable publishers)
2. Fetch each with appropriate `max_length` (5000-10000 characters)
3. Handle errors gracefully with try-except blocks

**Code pattern:**
```python
from extensions.wrapped_mcp.mcp_server_fetch import fetch

async def fetch_official_info():
    try:
        result = await fetch({
            "url": "https://official-source.com",
            "max_length": 10000
        })
        return result
    except Exception as e:
        print(f"Error fetching: {e}")
        return None
```

### Step 4: Synthesize Information

Combine search results and fetched content into a structured report.

**Report structure:**
```
# [Topic] Research Report

Date: [YYYY-MM-DD HH:MM:SS]

## 🔍 Web Search Results

[Search results with numbered sources, titles, descriptions, and URLs]

## 📚 Authoritative Sources

[Content from official sites and primary sources]

## 💡 Key Insights

[Synthesized summary of main findings, trends, or patterns]
```

**Best practices:**
- Include timestamps for time-sensitive research
- Organize sources clearly with titles and URLs
- Provide a synthesized summary beyond raw data
- Use clear section headers and formatting

### Step 5: Save Report to File

Write the compiled report to the user-specified file path.

**File operations:**
```python
from datetime import datetime

# Create report content
report = f"""# {topic} Research Report

Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🔍 Web Search Results

{search_results}

## 📚 Authoritative Sources

{fetched_content}

## 💡 Key Insights

{synthesized_summary}
"""

# Save to file
with open(output_path, "w", encoding="utf-8") as f:
    f.write(report)

print(f"✅ Report saved to {output_path}")
print(f"📊 File size: {len(report)} characters")
```

### Step 6: Confirm Completion

Provide clear feedback about:
- Successful completion
- File location (full path)
- Number of sources consulted
- File size or content summary

## Complete Implementation Script

The `scripts/research_and_report.py` script provides a complete, reusable implementation of this workflow that can be executed directly or customized as needed.

**Usage:**
```python
python scripts/research_and_report.py
```

Then modify the script parameters:
- `topic`: Research topic
- `output_path`: Where to save the report
- `num_search_results`: How many search results to gather
- `official_urls`: List of authoritative sources to fetch

## Error Handling

Handle common errors gracefully:

**Network errors:**
```python
try:
    result = await fetch({"url": url})
except Exception as e:
    print(f"⚠️ Could not fetch {url}: {e}")
    # Continue with available data
```

**File path errors:**
```python
import os

# Ensure directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Write with proper encoding
with open(output_path, "w", encoding="utf-8") as f:
    f.write(report)
```

## Tips for Effective Research

1. **Search query optimization**: Include time qualifiers, specific terms, and context
2. **Source diversity**: Mix web search results with official documentation
3. **Content limits**: Use appropriate `max_length` values (5000-10000 for most pages)
4. **Structured output**: Use clear headers, emojis, and formatting for readability
5. **Synthesis**: Don't just concatenate sources—provide insights and summaries
