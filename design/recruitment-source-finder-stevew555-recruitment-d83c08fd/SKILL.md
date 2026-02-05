---
name: recruitment-source-finder
description: This skill should be used when users need to find relevant sources from the sources.md knowledge base for recruitment-related topics. Parses and filters the comprehensive sources.md file to return targeted sub-lists of resources based on topic queries, making research more efficient.
---

# Recruitment Source Finder

## Purpose

This skill enables efficient discovery of relevant resources from the ProActive People recruitment knowledge base (sources.md). When users need information on specific recruitment topics—such as GDPR compliance, candidate sourcing, ATS software, or business development strategies—this skill parses the sources.md file and returns a filtered list of the most relevant sources.

The skill is particularly valuable because sources.md contains 157+ curated sources across 13 categories. Rather than manually searching through the entire document, this skill intelligently matches user queries to relevant sources using keyword matching, category analysis, and contextual relevance.

## When to Use This Skill

Use this skill when:

- Users ask for "sources about [topic]" or "resources on [topic]"
- Users need research materials on specific recruitment topics (e.g., "What sources cover GDPR?", "Find information about ATS software")
- Users want to explore what's available in the knowledge base for a particular area
- Users need citations or references for recruitment best practices, legal requirements, or industry standards
- The conversation requires authoritative sources to support recommendations or decisions

Examples of triggering queries:
- "Find sources about candidate sourcing strategies"
- "What resources do we have on GDPR compliance?"
- "Show me information about recruitment software and ATS systems"
- "I need sources on business development for recruitment agencies"
- "What do we have about retained vs contingency recruitment models?"

## How to Use This Skill

### Step 1: Parse the User Query

Identify the core topic(s) the user is asking about. Extract key terms and concepts that will be used for matching.

Examples:
- "Find GDPR sources" → key terms: ["GDPR", "data protection", "privacy", "compliance"]
- "Sources on ATS software" → key terms: ["ATS", "applicant tracking", "recruitment software", "CRM"]
- "Business development strategies" → key terms: ["business development", "client acquisition", "BD", "sales"]

### Step 2: Execute the Source Finder Script

Run the Python script with the user's query:

```bash
python scripts/find_sources.py "user query here"
```

The script automatically:
1. Loads and parses sources.md from the project root (d:\Recruitment\sources.md)
2. Matches the query against section headers, source titles, and source descriptions
3. Scores matches based on relevance
4. Returns a ranked list of relevant sources with their categories

### Step 3: Present Results to the User

Format the script output in a clear, actionable way:

- **Group sources by category** for better organization
- **Include the source title, URL, and category** for each match
- **Show the most relevant sources first** (the script handles ranking)
- **Provide context** about why these sources are relevant
- **Suggest related topics** if the search is too narrow or too broad

Example output format:

```markdown
I found [X] relevant sources on [topic]:

## [Category Name]
- **[Source Title]** - [URL]
- **[Source Title]** - [URL]

## [Another Category]
- **[Source Title]** - [URL]

These sources cover [brief explanation of what they contain].
```

### Step 4: Offer Follow-up Actions

After presenting sources, offer to:
- Fetch and summarize content from specific URLs (using WebFetch tool)
- Narrow or broaden the search based on user needs
- Find sources on related topics
- Explain how different sources complement each other

## Script Reference

### `scripts/find_sources.py`

**Purpose:** Intelligently parses sources.md and returns relevant sources based on query matching.

**Usage:**
```bash
python scripts/find_sources.py "query text" [--limit N] [--min-score S]
```

**Arguments:**
- `query` (required): The search query or topic
- `--limit N` (optional): Maximum number of sources to return (default: 20)
- `--min-score S` (optional): Minimum relevance score 0-100 (default: 30)

**Output:** JSON array of matching sources with:
```json
[
  {
    "title": "Source Title",
    "url": "https://example.com",
    "category": "Category Name",
    "score": 85,
    "match_reasons": ["matched in title", "matched in category"]
  }
]
```

**Matching Logic:**
- Section headers (categories): high weight
- Source titles: medium-high weight
- Source descriptions (if available): medium weight
- Semantic synonyms and related terms: included via keyword expansion
- Common abbreviations handled (e.g., "GDPR" matches "data protection")

## Common Topics and Keywords

To improve matching accuracy, the script recognizes these common recruitment domain synonyms:

- **GDPR / Data Protection / Privacy** → All match each other
- **ATS / Applicant Tracking System / Recruitment Software / CRM**
- **CV / Resume / Candidate Profile**
- **Business Development / BD / Client Acquisition / Sales**
- **Sourcing / Candidate Sourcing / Talent Acquisition**
- **Retained / Contingency / Recruitment Models**
- **Compliance / Legal / Regulations / Conduct Regulations**

## Limitations

- The skill searches only sources.md in the project root (d:\Recruitment\sources.md)
- It does not fetch or analyze the actual content of the source URLs
- Matching is based on text in sources.md only (titles, categories, descriptions)
- For content analysis from sources, use the WebFetch tool separately after identifying relevant URLs

## Examples

**Example 1:**
```
User: "Find sources about GDPR and data protection"
Action: python scripts/find_sources.py "GDPR data protection"
Result: Returns ~7 sources from "Legal & Compliance → GDPR & Data Protection"
```

**Example 2:**
```
User: "What resources do we have on choosing recruitment software?"
Action: python scripts/find_sources.py "recruitment software ATS"
Result: Returns ~11 sources from "Operations, Tech & Outsourcing → Recruitment Software / ATS / CRM"
```

**Example 3:**
```
User: "I need information about starting a recruitment agency"
Action: python scripts/find_sources.py "starting recruitment agency setup"
Result: Returns sources from "Starting a Recruitment Agency" category
```
