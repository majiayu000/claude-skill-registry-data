---
name: calibre
description: Search and query Calibre library databases. Use when the user asks about books, TBR (to-be-read), reading lists, Calibre library queries, book searches, or mentions Calibre. Also use for queries about book ratings, authors, reading status, or library statistics.
---

# Calibre Library Search Skill

You are helping the user search and query their Calibre library using `calibredb`.

## Library Setup

**Library URL**: `http://killington.home.bitbin.de:8454/#`

**calibredb Location**: `/Applications/calibre.app/Contents/MacOS/calibredb`

**Authentication**:
- Username: `calibre`
- Password: `calibre`

**Note**: Using Calibre Content Server means no database locking issues - queries work even while Calibre GUI is running.

## Custom Fields

The Calibre library has these custom fields:

| Field      | Search Name | Display Name | Type     | Values       |
|------------|-------------|--------------|----------|--------------|
| read       | #read       | *read        | Boolean  | Yes/No       |
| dateread   | #dateread   | *dateread    | Datetime | ISO date     |
| archived   | #archived   | *archived    | Boolean  | Yes/No       |
| goodreads  | #goodreads  | *goodreads   | Float    | 0.0-5.0      |
| pages      | #pages      | *pages       | Integer  | page count   |
| priority   | #priority   | *priority    | Text     | varies       |
| words      | #words      | *words       | Integer  | word count   |

**IMPORTANT - Boolean Field Syntax**:
- Use `#field` syntax in searches with `Yes` or `No` (capitalized): e.g., `#read:Yes`, `#read:No`
- Use `*field` syntax when displaying fields (e.g., `*read`)
- Boolean values are **NOT** `true`/`false` - they are `Yes`/`No`

## calibredb Command Pattern

Always use this pattern:

```bash
/Applications/calibre.app/Contents/MacOS/calibredb list \
  --with-library='http://killington.home.bitbin.de:8454/#' \
  --username='calibre' \
  --password='calibre' \
  --fields='field1,field2,*customfield' \
  --search='search query' \
  --for-machine | python3 -m json.tool
```

### Common Options

- `--fields='field1,field2'` - Comma-separated list of fields to display
- `--search='query'` - Search query using Calibre's search syntax
- `--sort-by='field'` - Sort results by field
- `--limit=N` - Limit results to N books
- `--for-machine` - Output as JSON (always use this for parsing)

### Available Built-in Fields

- `title`, `authors`, `series`, `series_index`
- `timestamp` (when added to library)
- `last_modified` (when book record was last modified)
- `pubdate`, `publisher`, `isbn`
- `rating`, `tags`, `comments`
- `formats`, `size`, `uuid`

## Search Query Syntax

### Basic Searches

```bash
# Search by title
--search='title:"Book Title"'

# Search by author
--search='authors:"Author Name"'

# Search in series
--search='series:"Series Name"'

# Combine searches with AND
--search='authors:"Sanderson" and series:"Mistborn"'

# Combine searches with OR
--search='authors:"Sanderson" or authors:"Wells"'

# NOT operator
--search='not #archived:Yes'
```

### Custom Field Searches

```bash
# Books marked as read
--search='#read:Yes'

# Books NOT read
--search='#read:No'

# Books not archived and not read (TBR)
--search='#read:No and #archived:No'

# Highly rated books (>= 4.0)
--search='#goodreads:">4"'

# Books with specific page count
--search='#pages:"<300"'

# Empty/not set custom fields
--search='#goodreads:""'

# Books read in a specific date range
--search='#dateread:">=2024-01-01" and #dateread:"<2025-01-01"'

# Books read in the last 30 days
--search='#dateread:">=30daysago"'
```

## Common Query Examples

### To-Be-Read List

Get unread, non-archived books:

```bash
/Applications/calibre.app/Contents/MacOS/calibredb list \
  --with-library='http://killington.home.bitbin.de:8454/#' \
  --username='calibre' \
  --password='calibre' \
  --fields='title,authors,series,series_index,*goodreads,*pages' \
  --search='#read:No and #archived:No' \
  --for-machine | python3 -m json.tool
```

### Recently Added Books

```bash
/Applications/calibre.app/Contents/MacOS/calibredb list \
  --with-library='http://killington.home.bitbin.de:8454/#' \
  --username='calibre' \
  --password='calibre' \
  --fields='title,authors,*goodreads,*pages,timestamp' \
  --search='#read:No and #archived:No' \
  --sort-by='timestamp' \
  --limit=10 \
  --for-machine | python3 -m json.tool
```

### Recently Read Books

Use the `*dateread` field to see when books were actually finished:

```bash
/Applications/calibre.app/Contents/MacOS/calibredb list \
  --with-library='http://killington.home.bitbin.de:8454/#' \
  --username='calibre' \
  --password='calibre' \
  --fields='title,authors,series,series_index,*goodreads,*pages,*dateread' \
  --search='#read:Yes' \
  --sort-by='*dateread' \
  --limit=15 \
  --for-machine | python3 -m json.tool
```

### Highly Rated Unread Books

```bash
/Applications/calibre.app/Contents/MacOS/calibredb list \
  --with-library='http://killington.home.bitbin.de:8454/#' \
  --username='calibre' \
  --password='calibre' \
  --fields='title,authors,series,*goodreads,*pages' \
  --search='#read:No and #archived:No and #goodreads:">4"' \
  --sort-by='*goodreads' \
  --for-machine | python3 -m json.tool
```

### Books by Specific Author

```bash
/Applications/calibre.app/Contents/MacOS/calibredb list \
  --with-library='http://killington.home.bitbin.de:8454/#' \
  --username='calibre' \
  --password='calibre' \
  --fields='title,authors,series,*read,*goodreads,*pages' \
  --search='authors:"Sanderson" and #archived:No' \
  --for-machine | python3 -m json.tool
```

### Quick Reads (< 300 pages)

```bash
/Applications/calibre.app/Contents/MacOS/calibredb list \
  --with-library='http://killington.home.bitbin.de:8454/#' \
  --username='calibre' \
  --password='calibre' \
  --fields='title,authors,*pages,*goodreads' \
  --search='#read:No and #archived:No and #pages:"<300"' \
  --sort-by='*goodreads' \
  --for-machine | python3 -m json.tool
```

### Unread Books in a Series

```bash
/Applications/calibre.app/Contents/MacOS/calibredb list \
  --with-library='http://killington.home.bitbin.de:8454/#' \
  --username='calibre' \
  --password='calibre' \
  --fields='title,authors,series,series_index,*goodreads,*pages,timestamp' \
  --search='series:"Between Earth and Sky" and #read:No and #archived:No' \
  --sort-by='series_index' \
  --for-machine | python3 -m json.tool
```

### Books Read in a Time Period

```bash
# Books read in October 2024
/Applications/calibre.app/Contents/MacOS/calibredb list \
  --with-library='http://killington.home.bitbin.de:8454/#' \
  --username='calibre' \
  --password='calibre' \
  --fields='title,authors,*dateread,*goodreads,*pages' \
  --search='#dateread:">=2024-10-01" and #dateread:"<2024-11-01"' \
  --sort-by='*dateread' \
  --for-machine | python3 -m json.tool

# Books read this year
/Applications/calibre.app/Contents/MacOS/calibredb list \
  --with-library='http://killington.home.bitbin.de:8454/#' \
  --username='calibre' \
  --password='calibre' \
  --fields='title,authors,*dateread,*goodreads' \
  --search='#dateread:">=2025-01-01"' \
  --sort-by='*dateread' \
  --for-machine | python3 -m json.tool
```

## Usage Instructions

When the user asks to search their Calibre library:

1. **Determine** what they're looking for (to-be-read, specific book, by rating, etc.)
2. **Construct** the appropriate calibredb command based on examples above
3. **Execute** the command using the Bash tool
4. **Parse** the JSON output and present results in a readable format

## Query Tips

- **Always exclude archived books** unless specifically requested: add `and #archived:No` to searches
- Use `--for-machine` to get JSON output that's easier to parse
- The `timestamp` field shows when a book was added to the library
- The `*dateread` field shows when a book was actually finished reading (synced from Goodreads)
- The `last_modified` field shows when a book record was last changed (not reliable for "recently read")
- When a custom field is not set, it won't appear in the JSON output
- Use `python3 -m json.tool` to pretty-print JSON for readability
- Search queries are case-insensitive
- Use quotes around field values that contain spaces
- **Boolean fields**: In search queries use `Yes`/`No` (e.g., `#read:Yes`), but in JSON output they appear as `true`/`false` (lowercase)
- **Date fields**: Use `*dateread` to sort by when books were actually read (more accurate than `last_modified`)

## Examples

**User**: "Show me my to-be-read list"
→ Search with `#read:No and #archived:No`

**User**: "Find books by Sanderson"
→ Search with `authors:"Sanderson" and #archived:No`

**User**: "Show highly rated unread books"
→ Search with `#read:No and #archived:No and #goodreads:">4"`

**User**: "What did I read recently?"
→ Search with `#read:Yes`, sort by `*dateread` (descending), limit to 10-15

**User**: "What's next in the series I'm reading?"
→ Find series from recent reads, then search for unread books in that series

**User**: "What did I read in October?" or "Show me books I read this year"
→ Use date range searches with `#dateread:">=2024-10-01" and #dateread:"<2024-11-01"` or `#dateread:">=2025-01-01"`

## Safety Notes

- **Read-only access**: calibredb list is a read-only operation
- **Never use**: `calibredb add`, `calibredb set_metadata`, `calibredb remove` unless explicitly requested by user
- **No locking issues**: Using the Content Server means the Calibre GUI can remain open during queries
