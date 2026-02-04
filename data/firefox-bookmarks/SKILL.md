---
name: firefox-bookmarks
description: Analyze Firefox bookmarks and tags directly from the places.sqlite database. Extract recent bookmarks, analyze tag popularity, find bookmark statistics, and explore bookmark metadata. Use when working with Firefox bookmarks, analyzing bookmark usage, organizing tags, or extracting bookmark data from Firefox profiles.
---

# Firefox Bookmarks Analyzer

## Overview

This Skill provides direct access to Firefox bookmark data by querying the places.sqlite database. It includes utilities for extracting bookmarks, analyzing tags, and generating insights about bookmark usage.

## Capabilities

- **Extract recent bookmarks** with metadata (URL, title, date added, last visited)
- **Analyze bookmark tags** to find most popular tags and tag usage statistics
- **Query Firefox database** directly using SQLite
- **Database schema exploration** to understand Firefox's bookmark structure
- **Cross-platform support** for macOS, Linux, and Windows Firefox profiles

## Prerequisites

- Ruby (system Ruby is sufficient)
- sqlite3 gem (usually pre-installed on macOS)
- Firefox installed with existing bookmarks

## Instructions

When the user asks to work with Firefox bookmarks, follow these steps:

### 1. Understanding User Intent

Determine what the user wants:
- **List recent bookmarks**: Use the bookmark extraction script
- **Analyze tags**: Use the tag analysis script
- **Explore database**: Use database exploration utilities
- **Custom queries**: Help write SQLite queries against places.sqlite

### 2. Locate Firefox Profile

The scripts automatically find the Firefox profile using these paths:
- **macOS**: `~/Library/Application Support/Firefox/Profiles/*default*`
- **Linux**: `~/.mozilla/firefox/*default*`
- **Windows**: `~/AppData/Roaming/Mozilla/Firefox/Profiles/*default*`

### 3. Run Appropriate Script

Use the scripts located in `~/.claude/skills/firefox-bookmarks/scripts/`:

**Extract Recent Bookmarks:**
```bash
ruby ~/.claude/skills/firefox-bookmarks/scripts/extract_bookmarks.rb [limit]
```

**Analyze Tags:**
```bash
ruby ~/.claude/skills/firefox-bookmarks/scripts/analyze_tags.rb
```

**Explore Database:**
```bash
ruby ~/.claude/skills/firefox-bookmarks/scripts/explore_db.rb
```

### 4. Present Results

- Format the output clearly for the user
- Highlight key insights (most used tags, recently added bookmarks, etc.)
- Suggest follow-up actions or analyses

## Common Use Cases

### Use Case 1: Find Recent Bookmarks
User asks: "What are my most recent Firefox bookmarks?"

Response: Run `extract_bookmarks.rb` with default limit (50) and show the results.

### Use Case 2: Tag Analysis
User asks: "What are my most popular bookmark tags?"

Response: Run `analyze_tags.rb` and present the top tags with usage counts.

### Use Case 3: Custom Analysis
User asks: "Show me all bookmarks tagged with 'ruby'"

Response: Write a custom SQLite query to filter by specific tag.

### Use Case 4: Database Exploration
User asks: "How does Firefox store bookmarks?"

Response: Run `explore_db.rb` to show the database schema and explain the structure.

## Database Structure Reference

Firefox stores bookmarks in `places.sqlite` with these key tables:

- **moz_bookmarks**: Bookmark entries, folders, and tags
  - `id`: Unique identifier
  - `type`: 1=bookmark, 2=folder
  - `fk`: Foreign key to moz_places (NULL for folders/tags)
  - `parent`: Parent folder ID
  - `title`: Bookmark/folder/tag name
  - `dateAdded`: Timestamp in microseconds
  - `lastModified`: Last modification timestamp

- **moz_places**: URL and visit data
  - `id`: Unique identifier
  - `url`: The URL
  - `title`: Page title
  - `visit_count`: Number of visits
  - `last_visit_date`: Last visit timestamp

- **Tags Structure**: Tags are stored as folders with parent ID 4
  - Tag folder: `parent=4, fk=NULL, title=tag_name`
  - Tagged bookmarks: Children of tag folder

## Safety Features

All scripts create temporary copies of places.sqlite to avoid:
- Database locking issues (Firefox may have the DB open)
- Accidental data corruption
- Read-only access ensures no modifications

## Error Handling

If scripts fail:
1. **Firefox not found**: Check Firefox installation and profile location
2. **Database locked**: Close Firefox and retry
3. **Missing dependencies**: Install sqlite3 gem (`gem install sqlite3 --user-install`)
4. **Permission errors**: Check file permissions on Firefox profile directory

## Advanced Usage

### Custom Queries

Help users write custom SQLite queries:

```sql
-- Find bookmarks by keyword in title
SELECT url, title, datetime(dateAdded/1000000, 'unixepoch') as added
FROM moz_bookmarks b
JOIN moz_places p ON b.fk = p.id
WHERE p.title LIKE '%keyword%'
ORDER BY dateAdded DESC;
```

### Filtering and Aggregation

Examples of useful analyses:
- Bookmarks added in last 30 days
- Most visited bookmarked pages
- Untagged bookmarks
- Bookmark folder depth analysis
- Duplicate URL detection

## Limitations

- Read-only access (cannot modify bookmarks)
- Requires Firefox to be closed for reliable database access (scripts use temp copies)
- Tag analysis only works if user has created tags in Firefox

## See Also

- REFERENCE.md: Detailed database schema documentation
- EXAMPLES.md: Complete usage examples with sample outputs
- scripts/: Ruby implementation files
