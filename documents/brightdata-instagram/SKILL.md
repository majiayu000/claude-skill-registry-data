---
name: brightdata-instagram
description: Discover Instagram influencers by keyword search using Bright Data API
---

# Bright Data Instagram Scraper

Discover Instagram influencers using Bright Data's web scraping API.

## When to Use

Use this skill when you need to:
- Find Instagram influencers in a specific niche
- Discover content creators for collaboration
- Search Instagram profiles by keyword
- Get influencer profile photos for portrait generation

## How to Use

### Step 1: Trigger the Scrape

```bash
$CLAUDE_CONFIG_DIR/skills/brightdata-instagram/scripts/trigger-scrape.sh "search_keyword"
```

**Parameters:**
- `search_keyword`: The keyword to search for (e.g., "fitness", "photography")

**Returns:** A `snapshot_id` used to fetch results

**Example:**
```bash
$CLAUDE_CONFIG_DIR/skills/brightdata-instagram/scripts/trigger-scrape.sh "fitness trainer"
# Output: snapshot_id=abc123xyz
```

### Step 2: Wait for Scraping

Bright Data needs approximately **2-3 minutes** to complete the scrape. Wait before fetching results.

### Step 3: Fetch Results

```bash
$CLAUDE_CONFIG_DIR/skills/brightdata-instagram/scripts/get-snapshot.sh "snapshot_id"
```

**Parameters:**
- `snapshot_id`: The ID returned from trigger-scrape.sh

**Example:**
```bash
$CLAUDE_CONFIG_DIR/skills/brightdata-instagram/scripts/get-snapshot.sh "abc123xyz"
```

**Output file:** `/tmp/data/instagram_[timestamp].json`

## Output Data Structure

Each profile in the results includes:

| Field | Description |
|-------|-------------|
| `username` | Instagram username |
| `url` | Direct link to the profile |
| `followers` | Number of followers |
| `biography` | Profile bio/description |
| `profile_pic_url` | URL to profile picture |
| `posts` | Array of recent posts with images |

## Environment Variables

- `BRIGHTDATA_API_KEY`: Required. Your Bright Data API key.

## Guidelines

1. Start with broad keywords, then narrow down if needed
2. The API returns up to 5 profiles per search by default
3. If the snapshot is not ready, wait and retry
4. Always check for errors in the API response
5. Profile photos can be downloaded for portrait generation

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "running" status | Snapshot still being prepared | Wait 1-2 minutes and retry |
| 401 error | Invalid API key | Verify BRIGHTDATA_API_KEY is set correctly |
| Empty results | No matches found | Try a different or broader keyword |
