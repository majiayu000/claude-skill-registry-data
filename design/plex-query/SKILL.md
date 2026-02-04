---
name: plex-query
description: This skill should be used when the user asks questions about their Plex media library, such as "what movies can I watch on Plex", "find romantic movies under 100 minutes", "show me Tom Cruise films from the 90s", "how many unwatched episodes of Always Sunny do I have", "give me a British comedy show I haven't watched", or "shows with episodes under 30 minutes that I've started". Use whenever user mentions Plex in combination with movies, TV shows, or media queries.
version: 0.4.0
---

# Plex Query Skill

## Purpose

This skill enables querying a Plex Media Server to answer natural language questions about available movies and TV shows. Use the provided CLI tools to filter media by duration, genre, ratings, actors, directors, year, and watch status. The tools are optimized for LLM use with JSON output and sensible defaults.

## When to Use This Skill

Use this skill when users ask questions about their Plex library, including:

- Finding movies or shows based on specific criteria (genre, duration, ratings, actors)
- Checking watch status ("what haven't I seen", "shows I've started")
- Time-constrained viewing ("I have 90 minutes, what can I watch")
- Recommendations based on ratings or awards
- Queries about specific shows or actors

## Available Tools

Three Python CLI tools are provided in the skill's `scripts/` directory. All tools use PEP 723 inline script metadata with uv for automatic dependency management, output JSON by default, and accept standard filtering parameters optimized for LLM patterns.

The scripts can be run directly:

```bash
cd scripts/
./plex-movie [options]
./plex-tv [options]
./plex-genres [options]
```

Or with uv explicitly:

```bash
uv run --no-project --script scripts/plex-movie [options]
```

### plex-movie

Search and filter movies in the Plex library.

**Common parameters:**

- `--max-duration MINUTES` - Maximum runtime in minutes (e.g., 120 for 2 hours)
- `--genre GENRE` - Filter by genre with OR logic (fuzzy matching, case-insensitive, can be specified multiple times - at least one must match)
- `--genre-and GENRE` - Filter by genre with AND logic (all specified genres must match, can be repeated)
- `--exclude-genre GENRE` - Exclude genre with NOT logic (none of the specified genres can match, can be repeated)
- `--actor NAME` - Filter by actor name (partial matching)
- `--director NAME` - Filter by director name (partial matching)
- `--year YEAR` - Exact year (e.g., 1995)
- `--decade DECADE` - Decade filter (e.g., "90s", "1990s", "1990")
- `--min-rating RATING` - Minimum rating (0-10 scale, checks all available ratings)
- `--unwatched` - Only show unwatched movies (default behavior)
- `--watched` - Only show watched movies
- `--all` - Show all movies regardless of watch status
- `--limit N` - Maximum results (default: 20)
- `--library NAME` - Specific library to search (uses config default if not specified)

**Output fields:**
Each movie object includes: title, year, duration (minutes), genres (array), rating (best available), actors (array), directors (array), summary, watch status, added date, and more.

**Example usage:**

```bash
# Find romantic movies under 100 minutes
plex-movie --genre romance --max-duration 100

# Tom Cruise movies from the 90s
plex-movie --actor "Tom Cruise" --decade 90s

# High-rated unwatched movies
plex-movie --min-rating 8.0 --unwatched

# Comedy OR action movies (at least one genre must match)
plex-movie --genre comedy --genre action --unwatched

# Movies that are BOTH sci-fi AND thriller
plex-movie --genre-and "sci-fi" --genre-and thriller --min-rating 7.0

# Action movies but NOT horror
plex-movie --genre action --exclude-genre horror

# Complex: (Comedy OR Action) AND British AND NOT Sci-Fi
plex-movie --genre comedy --genre action --genre-and british --exclude-genre scifi
```

### plex-tv

Search and filter TV shows in the Plex library.

**Show-level parameters:**

- `--genre GENRE` - Filter by genre with OR logic (fuzzy matching, can be specified multiple times - at least one must match)
- `--genre-and GENRE` - Filter by genre with AND logic (all specified genres must match, can be repeated)
- `--exclude-genre GENRE` - Exclude genre with NOT logic (none of the specified genres can match, can be repeated)
- `--actor NAME` - Filter by actor
- `--year YEAR` - Show release year
- `--decade DECADE` - Decade filter
- `--min-rating RATING` - Minimum rating (0-10 scale)
- `--max-episode-duration MINUTES` - Maximum typical episode length
- `--unwatched-only` - Only shows with 0 episodes watched
- `--started` - Only shows with >0 episodes watched AND unwatched episodes remaining
- `--in-progress` - Alias for --started
- `--completed` - Only fully watched shows
- `--all` - All shows regardless of watch status
- `--limit N` - Maximum results (default: 20)
- `--library NAME` - Specific library to search

**Show-specific queries:**

- `--show-title TITLE` - Get details about a specific show (partial matching)
- `--unwatched-episodes` - When used with --show-title, returns count and list of unwatched episodes

**Output fields:**
Each show object includes: title, year, genres (array), rating, actors (array), episode count (total, watched, unwatched), typical episode duration, seasons, summary, watch progress percentage, and more.

**Example usage:**

```bash
# British comedy shows not yet started
plex-tv --genre comedy --genre-and british --unwatched-only

# Shows with short episodes that user has started
plex-tv --max-episode-duration 30 --started

# Unwatched episodes of a specific show
plex-tv --show-title "Always Sunny" --unwatched-episodes

# All sci-fi shows from the 2010s
plex-tv --genre "sci-fi" --decade 2010s --all

# Comedy OR Drama shows (at least one must match)
plex-tv --genre comedy --genre drama --unwatched-only

# Shows that are BOTH crime AND drama
plex-tv --genre-and crime --genre-and drama --min-rating 8.0

# Any genre except reality TV
plex-tv --exclude-genre reality --exclude-genre "reality-tv"

# Complex: (Comedy OR Action) AND British AND NOT Sci-Fi
plex-tv --genre comedy --genre action --genre-and british --exclude-genre scifi
```

### plex-genres

List all available genres in the Plex library.

**Parameters:**

- `--type movies` - List movie genres (default)
- `--type tv` - List TV show genres
- `--type all` - List all genres

**Output:**
JSON array of genre names found in the library.

**Example usage:**

```bash
# List movie genres
plex-genres

# List TV genres
plex-genres --type tv
```

Use this tool when the user's genre query doesn't match exactly, or to discover available genres for better filtering.

## Workflow for Answering Queries

### Step 1: Parse User Intent

Identify the key filtering criteria from the user's question:

- Media type (movie vs TV show)
- Duration constraints ("I have 100 minutes")
- Genre preferences ("romantic", "comedy", "sci-fi")
- People (actors, directors)
- Time period (year, decade)
- Watch status ("haven't seen", "already started", "unwatched episodes")
- Rating requirements ("highly rated", "90%+", "award-winning")

### Step 2: Select the Appropriate Tool

- Use `plex-movie` for movie queries
- Use `plex-tv` for TV show queries
- Use `plex-genres` if genre matching might be ambiguous

### Step 3: Construct the Command

Map user criteria to CLI parameters. Common mappings:

- "I have X minutes" → `--max-duration X` (for movies) or `--max-episode-duration X` (for TV)
- "romantic" → `--genre romance`
- "Tom Cruise" → `--actor "Tom Cruise"`
- "from the 90s" → `--decade 90s`
- "haven't seen" → `--unwatched` (movies) or `--unwatched-only` (TV)
- "already started" → `--started` (TV shows)
- "highly rated" → `--min-rating 8.0`

### Step 4: Execute and Parse Results

Run the CLI tool using the Bash tool. The output will be JSON with comprehensive metadata.

### Step 5: Present Results

Format the results for the user:

- Summarize the count ("I found 5 movies matching your criteria")
- List recommendations with relevant details (title, year, duration, rating, brief summary)
- Highlight why each recommendation matches the criteria
- Note watch status if relevant

## Handling Edge Cases

### No Results Found

If the query returns no results:

1. Try relaxing constraints (e.g., increase duration limit, remove genre filter)
2. Use `plex-genres` to verify genre spelling
3. Suggest alternative criteria to the user

### Ambiguous Genres

If a genre term might not match exactly:

1. First try the query with the user's term
2. If results are empty or sparse, run `plex-genres` to see available genres
3. Use fuzzy matching to find the closest genre
4. Retry with the corrected genre

### Multiple Criteria

When users specify multiple criteria, combine parameters in a single command:

```bash
plex-movie --genre action --actor "Keanu Reeves" --decade 90s --max-duration 120 --min-rating 7.0
```

### TV Show Episode Queries

For questions about specific shows and episodes:

1. Use `--show-title` with the show name
2. Add `--unwatched-episodes` to get episode details
3. Parse the episode list to answer questions like "how many episodes" or "which season"

## Prerequisites

The scripts use PEP 723 inline script metadata with uv for automatic dependency management. The only requirement is having [uv](https://github.com/astral-sh/uv) installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

The `plexapi` dependency is automatically installed when you run any script for the first time.

**Running the scripts:**

Direct execution (recommended):

```bash
cd scripts/
./plex-movie --help
./plex-tv --help
./plex-genres --help
```

Or using uv explicitly:

```bash
uv run --no-project --script scripts/plex-movie --help
```

## Configuration

The tools read configuration from environment variables with optional file override:

**Required:**

- `PLEX_URL` - Plex server URL (e.g., "<http://192.168.1.100:32400>")
- `PLEX_TOKEN` - Plex authentication token

**Optional:**

- `PLEX_DEFAULT_MOVIE_LIBRARIES` - Comma-separated library names for movies
- `PLEX_DEFAULT_TV_LIBRARIES` - Comma-separated library names for TV shows
- `PLEX_DEFAULT_LIMIT` - Default result limit (default: 20)
- `PLEX_CACHE_EXPIRY` - Cache expiration in seconds (default: 3600)

If configuration is missing or connection fails, the tools will return JSON error objects with details.

## Example Queries

### Simple Examples

**User:** "I want to watch a romantic movie but only have 100 minutes"
**Command:** `plex-movie --genre romance --max-duration 100`

**User:** "Show me Tom Cruise movies from the 90s"
**Command:** `plex-movie --actor "Tom Cruise" --decade 90s`

**User:** "How many unwatched episodes of Always Sunny do I have?"
**Command:** `plex-tv --show-title "Always Sunny" --unwatched-episodes`

**User:** "Give me a British comedy show I haven't watched at all"
**Command:** `plex-tv --genre british --genre comedy --unwatched-only --limit 5`

### Complex Examples

For more complex query examples, see the `examples/` directory:

- **`examples/complex-movie-queries.md`** - Advanced movie filtering scenarios
- **`examples/complex-tv-queries.md`** - Advanced TV show and episode queries
- **`examples/multi-criteria-searches.md`** - Combining multiple filters effectively

## Error Handling

All tools return JSON error objects on failure:

```json
{
  "error": "ConnectionError",
  "message": "Could not connect to Plex server at http://...",
  "details": "Connection refused. Check PLEX_URL and ensure server is running.",
  "recovery": "Verify PLEX_URL and PLEX_TOKEN environment variables"
}
```

When encountering errors:

1. Parse the error JSON to understand the issue
2. Check if it's a configuration problem (missing URL/token)
3. Inform the user of the specific issue and recovery steps
4. If it's a connection issue, suggest verifying the Plex server is accessible

## Best Practices

### Optimize for User Intent

**IMPORTANT - Different Default Behaviors:**

- **Movies (`plex-movie`)**: Defaults to `--unwatched` (users typically want new content to watch)
- **TV Shows (`plex-tv`)**: Defaults to `--all` (shows entire library unless filtered)

**Watch Status Guidelines:**

- For movie recommendations, the default `--unwatched` is usually correct
- For TV shows, explicitly specify watch status based on user intent:
  - New shows to start → `--unwatched-only`
  - Shows to continue → `--started`
  - Shows they've finished → `--completed`
  - Entire library overview → `--all` (or omit the flag)
- Use `--all` when the user explicitly asks about their entire library

**Genre Boolean Operations - When to Use:**

- **OR logic (`--genre`)**: Use when user wants variety or alternatives
  - "comedy or action movies" → `--genre comedy --genre action`
  - "I want something funny or exciting" → `--genre comedy --genre action`
  - At least ONE of the specified genres must match

- **AND logic (`--genre-and`)**: Use when user wants multiple characteristics
  - "British comedy" → `--genre-and british --genre-and comedy`
  - "crime drama" → `--genre-and crime --genre-and drama`
  - ALL specified genres must match (very restrictive)

- **NOT logic (`--exclude-genre`)**: Use when user wants to avoid genres
  - "anything but horror" → `--exclude-genre horror`
  - "no reality TV" → `--exclude-genre reality`
  - NONE of the excluded genres can match

- **Combined logic**: For complex queries like "(comedy OR action) AND british NOT scifi"
  ```bash
  --genre comedy --genre action --genre-and british --exclude-genre scifi
  ```
  This reads as: (At least comedy OR action) AND british AND NOT scifi

### Progressive Filtering

If a query returns too many results:

1. Add rating filters to prioritize quality content
2. Limit by time period if relevant
3. Use `--limit` to control result count

If a query returns too few results:

1. Remove strict filters (genre, rating) one at a time
2. Broaden the search with `--all` for watch status
3. Suggest alternative genres using `plex-genres`

### Provide Context

When presenting results:

- Mention how many total results were found
- Explain why recommendations match the criteria
- Note watch status prominently for relevant queries
- Include duration and episode information for time-constrained queries

## Additional Resources

### Example Files

See `examples/` directory for detailed query scenarios:

- Complex multi-criteria searches
- Episode-level queries
- Genre exploration and matching
- Rating and award-based filtering

### Scripts

All CLI tools are in `scripts/` directory:

- **`plex-movie`** - Movie search and filtering
- **`plex-tv`** - TV show search and filtering
- **`plex-genres`** - Genre discovery

The scripts use PEP 723 inline metadata with `#!/usr/bin/env -S uv run --script` for automatic dependency management. They're executable and handle authentication, caching, and output formatting automatically. Dependencies are installed on first run by uv.
