---
name: music-discover
description: Music news and recommendations based on Spotify listening history. Use for music news, new releases, recommendations, what to listen to in specific situations (commute, workout, travel), artist updates, or concert announcements.
---

# Music Discover

Personalized music news and recommendations using Spotify data and listening history.

**TOOL RESTRICTION:** Never use the `webFetch` tool for web searching. Use the model's built-in web search if available.

## Workflow

### Step 1: Fetch User's Music Profile

Use `spotifyUser` tool:
- `get_top_tracks` (timeRange: `short_term`) → recent favorites
- `get_top_artists` (timeRange: `medium_term`) → overall taste

### Step 2: Find New Releases

Use `spotifyArtists` tool on top 2-3 artists:
- `get_artist_albums` (includeGroups: `["album", "single"]`, limit: 5) → recent releases from favorite artists

### Step 3: Enhance with Search

Use `spotifySearch` tool for specific queries:
- `search` (query: "[users mood, genre or interests]", types: `["track", "artist"]`) → find music matching specific moods or genres

### Step 4: Search for News

**If web search is available:** Search for recent news about the user's top artists:

- New album releases (last 4 weeks)
- Upcoming album announcements
- Concert tour announcements (especially Berlin/Germany)
- Major artist news (collaborations, announcements)

Skip the news section if no relevant news found.

**If web search is NOT available:**

1. Tell the user: "Web search is not enabled. Enable it in settings for current music news."
2. Continue without news section.

### Step 5: Generate Recommendations

Provide 3-5 recommendations based on:

1. **New releases** from favorite artists (from Step 2)
2. **Deep cuts** from known artists (lesser-known albums)
3. **Genre exploration** based on top artists' genres
4. **Search results** using `spotifySearch` tool for specific queries or mood-based searches

Tailor to context if specified (e.g., "long train ride" → longer, atmospheric albums).

### Step 6: Offer Actions (Optional)

After showing recommendations, ask if user wants to:
- **Play now** or **add to queue** → use `spotifyPlayback` (play) or `spotifyQueue` (add_to_queue)
- **Create a "Discoveries" playlist** → use `spotifyPlaylists` (create_playlist + add_tracks)

## Output Format

```
[Brief excited intro with emoji]

News: (only if web search available and news found)
- Artist - "Title/Event" (Date) - Brief description [Link]
...

Recommendations:
- Artist - "Album/Song" - Why this fits [Link if available]
...

[Optional: Offer to play, queue, or create playlist]
```

**Keep it short:** Readable in under 30 seconds.

## Error handling

If you are trying to use a spotify tool and it fails, guide the user to check their settings:
- Tell user to check if Spotify is connected. The user can connect it from the sidebar menu
- Tell user to check if spotify tools for discovery and research are enabled. The user can enable them in the chat input options
- Tell the user to try again after they have done the above