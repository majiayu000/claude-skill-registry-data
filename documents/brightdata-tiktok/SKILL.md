---
name: brightdata-tiktok
description: Discover TikTok influencers by keyword search using Bright Data API
---

# Bright Data TikTok Scraper

Discover TikTok influencers using Bright Data's web scraping API.

## When to Use

Use this skill when you need to:
- Find TikTok influencers in a specific niche
- Discover content creators for collaboration
- Search TikTok profiles by keyword

## How to Use

### Step 1: Trigger the Scrape

```bash
$CLAUDE_CONFIG_DIR/skills/brightdata-tiktok/scripts/trigger-scrape.sh "search_keyword"
```

**Parameters:**
- `search_keyword`: The keyword to search for (e.g., "fitness trainer", "cooking")

**Returns:** A `snapshot_id` used to fetch results

**Example:**
```bash
$CLAUDE_CONFIG_DIR/skills/brightdata-tiktok/scripts/trigger-scrape.sh "fitness trainer"
# Output: snapshot_id=abc123xyz
```

### Step 2: Wait for Scraping

Bright Data needs approximately **2-3 minutes** to complete the scrape. Wait before fetching results.

### Step 3: Fetch Results

```bash
$CLAUDE_CONFIG_DIR/skills/brightdata-tiktok/scripts/get-snapshot.sh "snapshot_id"
```

**Parameters:**
- `snapshot_id`: The ID returned from trigger-scrape.sh

**Example:**
```bash
$CLAUDE_CONFIG_DIR/skills/brightdata-tiktok/scripts/get-snapshot.sh "abc123xyz"
```

**Output file:** `/tmp/data/tiktok_[timestamp].json`

## Output Data Structure

Each profile in the results includes:

| Field | Description |
|-------|-------------|
| `profile_id` | Unique TikTok profile ID |
| `profile_username` | TikTok username (e.g., @username) |
| `profile_url` | Direct link to the profile |
| `profile_followers` | Number of followers |
| `description` | Profile/video description |
| `url` | Video URL |

## Environment Variables

- `BRIGHTDATA_API_KEY`: Required. Your Bright Data API key.

## Guidelines

1. Start with broad keywords, then narrow down if needed
2. The API returns up to 5 profiles per search by default
3. If the snapshot is not ready, wait and retry
4. Always check for errors in the API response

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "running" status | Snapshot still being prepared | Wait 1-2 minutes and retry |
| 401 error | Invalid API key | Verify BRIGHTDATA_API_KEY is set correctly |
| Empty results | No matches found | Try a different or broader keyword |
