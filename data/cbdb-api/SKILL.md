---
name: cbdb-api
description: Query the China Biographical Database (CBDB) API to retrieve comprehensive biographical data about historical Chinese figures. Use this skill when searching for information about Chinese historical figures, scholars, officials, or literary figures from the 7th century BCE through the 19th century CE. Applicable for queries about biographical details, social relationships, official positions, or when users mention specific Chinese names or CBDB person IDs.
version: 1.0.0
license: MIT
creator: AI
author: Kwok-leong Tang
contributors:
  - Claude (AI Assistant)
  - Z.ai (AI Platform)
---

# CBDB API

## Overview

The China Biographical Database (CBDB) is a comprehensive relational database containing biographical information about approximately 500,000 individuals from Chinese history, primarily from the 7th century BCE through the 19th century CE. The CBDB API provides access to this rich biographical data through simple HTTP queries.

This skill enables querying the CBDB API to retrieve detailed information about historical Chinese figures including their names, dates, places, social relationships, official positions, and literary works.

## When to Use This Skill

Use the CBDB API skill when:

- User asks about a historical Chinese figure or scholar
- User mentions a Chinese name (in characters or Pinyin) from pre-modern China
- User requests biographical information about Chinese officials, literati, or historical persons
- User has a CBDB person ID and wants to retrieve associated data
- User asks about relationships between historical Chinese figures
- User requests information about official positions, titles, or appointments in Chinese history
- Research involves Chinese biographical data, prosopography, or social network analysis

## Quick Start

### Basic Query Process

1. **Identify the query type**: Determine if searching by person ID or by name
2. **Choose output format**: Select JSON (most common), XML, or HTML
3. **Construct the URL**: Build the API query with appropriate parameters
4. **Fetch the data**: Use web_fetch to retrieve the biographical information
5. **Parse and present**: Extract relevant information and present to user

### Example Queries

**Query by Chinese name:**
```
https://cbdb.fas.harvard.edu/cbdbapi/person.php?name=王安石&o=json
```

**Query by Pinyin name:**
```
https://cbdb.fas.harvard.edu/cbdbapi/person.php?name=Wang%20Anshi&o=json
```

**Query by CBDB ID:**
```
https://cbdb.fas.harvard.edu/cbdbapi/person.php?id=1762&o=json
```

## Workflow

### Step 1: Determine Query Parameters

**If user provides CBDB ID:**
- Use ID-based query (most precise)
- Format: `?id={person_id}&o=json`

**If user provides Chinese name:**
- Use name-based query with Chinese characters
- URL-encode the Chinese characters
- Format: `?name={chinese_name}&o=json`

**If user provides Pinyin/romanized name:**
- Use name-based query with Pinyin
- URL-encode spaces as %20
- Format: `?name={pinyin_name}&o=json`
- Note: May return multiple results if names are similar

### Step 2: Select Output Format

**Recommended: JSON format (`&o=json`)**
- Easiest to parse programmatically
- Well-structured data
- Use for most queries

**Alternative: XML format (`&o=xml`)**
- Use when XML structure is specifically needed
- Suitable for data interchange with XML-based systems

**Alternative: HTML format (default, no `&o` parameter)**
- Use when displaying directly to user in a browser
- Not recommended for programmatic extraction

### Step 3: Construct and Execute Query

1. Build the complete URL with proper encoding
2. Use the `web_fetch` tool to retrieve the data
3. Handle the response based on format selected

**Example implementation:**
```
# For Chinese name query
url = "https://cbdb.fas.harvard.edu/cbdbapi/person.php?name=蘇軾&o=json"

# For Pinyin name query  
url = "https://cbdb.fas.harvard.edu/cbdbapi/person.php?name=Su%20Shi&o=json"

# For ID query
url = "https://cbdb.fas.harvard.edu/cbdbapi/person.php?id=6191&o=json"
```

### Step 4: Parse and Present Results

Extract relevant information from the response:

- **Basic details**: Name (in Chinese and Pinyin), alternative names, dynasty, gender
- **Dates and places**: Birth/death dates and locations
- **Biographical context**: Historical notes, significance
- **Relationships**: Family, teachers, students, colleagues, friends
- **Official positions**: Government roles, titles, appointments
- **Literary works**: Writings, publications, contributions
- **Geographic associations**: Places lived, worked, or visited

Present the information in a clear, organized format appropriate to the user's query.

## Best Practices

### URL Encoding

Always URL-encode query parameters:
- Chinese characters must be properly encoded
- Spaces in Pinyin names should be encoded as `%20`
- Use proper encoding functions in bash or Python when constructing URLs

### Handling Ambiguous Results

When querying by name (especially Pinyin):
- Results may include multiple people with similar names
- Check the response carefully for the correct individual
- Consider dates, dynasty, or other contextual information to identify the right person
- If ambiguous, present multiple matches to the user and ask for clarification

### Preferred Query Methods

**Priority order:**
1. **CBDB ID** (when known) - most precise, fastest
2. **Chinese characters** - more accurate than Pinyin
3. **Pinyin/romanization** - convenient but may be ambiguous

### Error Handling

If a query returns no results:
- Try alternative name forms (Chinese vs. Pinyin)
- Check for spelling variations in romanization
- Consider alternative names or courtesy names (字, 號)
- Inform user that the person may not be in CBDB or may be listed under a different name

## Data Interpretation

### Dates in CBDB

- Dates are typically given in Chinese calendar format
- May include reign periods and cyclical year designations
- Some dates are approximate or have ranges
- Always present dates with appropriate uncertainty indicators

### Dynasty Context

CBDB covers multiple dynasties and periods. Always provide dynastic context when presenting biographical information as it helps users understand the historical timeframe.

### Relationships and Social Networks

CBDB contains extensive relationship data. When presenting relationships:
- Specify the type of relationship (family, teacher-student, colleague, etc.)
- Include relevant dates for the relationship when available
- Note the direction of the relationship (who is teacher, who is student, etc.)

## Resources

### references/api_reference.md

Contains detailed API documentation including:
- Complete endpoint specifications
- All query parameters with examples
- Response data structure details
- Additional query examples
- Comprehensive best practices

Load this reference when needing detailed technical information about API calls, troubleshooting queries, or understanding response data structures.
