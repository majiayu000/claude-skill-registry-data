---
name: patent-search
description: Advanced prior art search using the PatentsView API. Use this skill when users need to search for patents, perform prior art searches, analyze patent landscapes, or find patents by inventor, title, date range, or technical fields. Helps with patent research, freedom to operate analysis, and competitive intelligence.
---

# Patent Search Skill

This skill provides advanced patent search capabilities using the PatentsView Search API, enabling comprehensive prior art searches and patent landscape analysis.

## Overview

The PatentsView API provides access to millions of US patents with rich metadata including inventors, assignees, classifications, citations, and full text. This skill helps construct sophisticated queries for patent research.

## Authentication & Rate Limits

**IMPORTANT**: All API requests require an API key passed via the `X-Api-Key` header.

- **Rate Limit**: 45 requests per minute per API key
- **API Key**: Users should have `PATENTSVIEW_API_KEY` environment variable set
- If not configured, refer them to [docs/PATENTSVIEW_API_SETUP.md](../../../docs/PATENTSVIEW_API_SETUP.md)

## API Endpoint

Base URL: `https://search.patentsview.org/api/v1/patent/`

## Query Construction

### Request Parameters

All requests include these components:

1. **q** (query): JSON object with search criteria (REQUIRED)
2. **f** (fields): JSON array of fields to return (optional, defaults to basic fields)
3. **s** (sort): JSON array of sort specifications (optional)
4. **o** (options): JSON object with pagination and other settings (optional)

### Query Operators

**Comparison Operators:**
- `_eq`: Equal to (exact match)
- `_neq`: Not equal to
- `_gt`: Greater than
- `_gte`: Greater than or equal
- `_lt`: Less than
- `_lte`: Less than or equal
- `_begins`: String begins with
- `_contains`: String contains (case-insensitive)

**Text Search Operators:**
- `_text_all`: All words must be present
- `_text_any`: Any word can be present
- `_text_phrase`: Exact phrase match

**Logical Operators:**
- `_and`: All conditions must be true
- `_or`: At least one condition must be true
- `_not`: Negates a condition

**Date Format:** ISO 8601 (YYYY-MM-DD)

## Common Search Patterns

### 1. Search by Title Keywords

For finding patents with specific terms in the title:

```json
{
  "q": {"_text_any": {"patent_title": "machine learning artificial intelligence"}},
  "f": ["patent_id", "patent_title", "patent_date", "inventors.inventor_name_first", "inventors.inventor_name_last"],
  "s": [{"patent_date": "desc"}],
  "o": {"size": 100}
}
```

### 2. Search by Inventor

Find patents by a specific inventor:

```json
{
  "q": {
    "_and": [
      {"inventors.inventor_name_last": "Smith"},
      {"inventors.inventor_name_first": "John"}
    ]
  },
  "f": ["patent_id", "patent_title", "patent_date", "inventors.inventor_name_last"],
  "s": [{"patent_date": "desc"}]
}
```

### 3. Search by Date Range

Find patents within a specific time period:

```json
{
  "q": {
    "_and": [
      {"_gte": {"patent_date": "2020-01-01"}},
      {"_lte": {"patent_date": "2023-12-31"}},
      {"_text_any": {"patent_abstract": "neural network"}}
    ]
  },
  "f": ["patent_id", "patent_title", "patent_date", "patent_abstract"],
  "s": [{"patent_date": "desc"}]
}
```

### 4. Search by Assignee (Company)

Find patents assigned to a specific organization:

```json
{
  "q": {
    "_and": [
      {"assignees.assignee_organization": {"_contains": "Google"}},
      {"_gte": {"patent_date": "2020-01-01"}}
    ]
  },
  "f": ["patent_id", "patent_title", "patent_date", "assignees.assignee_organization"],
  "s": [{"patent_date": "desc"}]
}
```

### 5. Search by CPC Classification

Find patents in specific technology areas using Cooperative Patent Classification:

```json
{
  "q": {
    "_and": [
      {"cpc_current.cpc_section_id": "G"},
      {"cpc_current.cpc_subsection_id": "G06F"}
    ]
  },
  "f": ["patent_id", "patent_title", "cpc_current.cpc_section_id", "cpc_current.cpc_subsection_id"],
  "s": [{"patent_date": "desc"}]
}
```

### 6. Complex Prior Art Search

Combining multiple criteria for comprehensive prior art search:

```json
{
  "q": {
    "_and": [
      {
        "_or": [
          {"_text_phrase": {"patent_title": "wireless charging"}},
          {"_text_all": {"patent_abstract": "wireless power transfer"}}
        ]
      },
      {"_lt": {"patent_date": "2023-01-01"}},
      {"patent_type": "utility"}
    ]
  },
  "f": ["patent_id", "patent_title", "patent_abstract", "patent_date", "inventors.inventor_name_last", "assignees.assignee_organization", "cpc_current.cpc_group_id"],
  "s": [{"patent_date": "desc"}],
  "o": {"size": 100}
}
```

## Useful Fields

**Patent Information:**
- `patent_id`: Patent number
- `patent_title`: Title
- `patent_abstract`: Abstract
- `patent_date`: Grant date
- `patent_type`: utility, design, plant, reissue, etc.
- `patent_num_claims`: Number of claims

**People & Organizations:**
- `inventors.inventor_name_first`: Inventor first name
- `inventors.inventor_name_last`: Inventor last name
- `assignees.assignee_organization`: Company/org name
- `assignees.assignee_individual_name_first`: Individual assignee first name
- `assignees.assignee_individual_name_last`: Individual assignee last name

**Classifications:**
- `cpc_current.cpc_section_id`: CPC section (A-H)
- `cpc_current.cpc_subsection_id`: CPC subsection (e.g., G06F)
- `cpc_current.cpc_group_id`: CPC group
- `uspc.uspc_mainclass_id`: US Patent Classification main class
- `uspc.uspc_subclass_id`: US Patent Classification subclass

**Citations:**
- `cited_patents.cited_patent_number`: Patents this patent cites
- `citedby_patents.citedby_patent_number`: Patents that cite this patent

**Location:**
- `inventors.inventor_city`: Inventor city
- `inventors.inventor_state`: Inventor state
- `inventors.inventor_country`: Inventor country

## Pagination

The API supports cursor-based pagination:

```json
{
  "o": {
    "size": 100,
    "after": ["2023-01-15", "10234567"]
  }
}
```

Use the sort field values from the last record of the previous page as the `after` cursor.

## Making API Calls

### Using curl

```bash
curl -X POST 'https://search.patentsview.org/api/v1/patent/' \
  -H 'X-Api-Key: YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "q": {"_text_any": {"patent_title": "blockchain"}},
    "f": ["patent_id", "patent_title", "patent_date"],
    "s": [{"patent_date": "desc"}],
    "o": {"size": 10}
  }'
```

### Response Format

```json
{
  "error": false,
  "count": 10,
  "total_hits": 5234,
  "patents": [
    {
      "patent_id": "11234567",
      "patent_title": "BLOCKCHAIN-BASED SYSTEM FOR...",
      "patent_date": "2023-05-15"
    }
  ]
}
```

## Best Practices for Prior Art Searches

### 1. Start Broad, Then Narrow

Begin with general keyword searches, then add filters:
- First: Search title/abstract for key concepts
- Then: Add date range to focus on relevant time period
- Finally: Add classification or assignee filters if needed

### 2. Use Multiple Search Strategies

- **Keyword searches**: Title and abstract text
- **Classification searches**: CPC/USPC codes for technology areas
- **Citation searches**: Forward and backward citations
- **Inventor/Assignee searches**: Find related work by same parties

### 3. Consider Synonyms and Variants

Use `_text_any` with multiple terms:
```json
{"_text_any": {"patent_abstract": "automobile vehicle car automotive"}}
```

### 4. Date Range Considerations

- For prior art: Search patents granted BEFORE your priority date
- Consider application dates vs grant dates
- Allow margin for publication delays

### 5. Export and Document Results

- Save search queries for reproducibility
- Export relevant patent numbers for detailed review
- Document search strategy for legal purposes

## Error Handling

**HTTP Status Codes:**
- `200`: Success
- `400`: Invalid request (check query syntax)
- `403`: Invalid/missing API key (check PATENTSVIEW_API_KEY environment variable)
- `429`: Rate limit exceeded (wait 60 seconds)
- `500`: Server error (retry after delay)

## Instructions for Claude

When a user requests patent searches:

1. **Understand the Search Goal**: Ask clarifying questions about:
   - What technology/invention are they researching?
   - What time period is relevant?
   - Are they looking for prior art, competitive analysis, or general research?

2. **Check for API Key**: Ensure the user has a PatentsView API key, or guide them to obtain one.

3. **Construct Appropriate Query**: Based on the search goal, build a query using:
   - Relevant operators and fields
   - Appropriate date ranges
   - Logical combinations of criteria

4. **Make the API Call**: Use curl or appropriate HTTP method with:
   - Proper headers (X-Api-Key)
   - Well-formed JSON query
   - Requested fields for efficient response

5. **Process and Present Results**:
   - Parse the JSON response
   - Present results in readable format
   - Highlight key information (patent numbers, titles, dates, inventors, assignees)
   - Provide patent URLs for further review: `https://patents.google.com/patent/US{patent_id}`

6. **Offer Next Steps**:
   - Suggest refinements to narrow/broaden search
   - Offer to search related classifications
   - Provide citation analysis if relevant
   - Help export results for further review

7. **Handle Pagination**: If results exceed one page:
   - Inform user of total hits
   - Offer to retrieve additional pages
   - Use cursor-based pagination with `after` parameter

8. **Respect Rate Limits**:
   - Stay within 45 requests/minute
   - If rate limited, wait for retry-after period
   - Batch operations when possible

## Example Workflows

### Prior Art Search Workflow

1. User describes invention concept
2. Extract key technical terms and concepts
3. Construct initial broad search using title/abstract keywords
4. Review results and identify relevant CPC classifications
5. Refine search with classifications and date ranges
6. Analyze top results and cited patents
7. Provide summary with most relevant patents

### Competitive Intelligence Workflow

1. Identify target company/assignee
2. Search patents by assignee name
3. Add date range for recent activity
4. Group by technology classifications
5. Analyze trends and focus areas
6. Identify key inventors and recent innovations

### Technology Landscape Analysis

1. Define technology area (keywords or CPC codes)
2. Search across multiple years
3. Aggregate by assignee to see major players
4. Analyze citation patterns
5. Identify emerging trends and key patents
6. Generate summary report

## Notes

- The API covers US patents only
- Data updated regularly (may lag recent publications by a few weeks)
- Always verify critical findings with official USPTO records
