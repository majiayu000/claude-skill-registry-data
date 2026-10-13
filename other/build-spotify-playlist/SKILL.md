---
name: build-spotify-playlist
description: "Generates Spotify playlists using MCP spotify tools. Use when user wants to create a playlist based on mood, genre, similar artists, or any theme. Handles auth, track discovery, playlist creation, and adding tracks."
---

# Build Spotify Playlist

## When to Use
- User asks to create, build, or generate a Spotify playlist
- User describes a mood, genre, artist, or theme they want a playlist for
- User says "make me a playlist", "playlist like X", "songs similar to Y"

## Workflow

### Step 1: Load Tools
Always load spotify MCP tools first:
```
ToolSearch "+spotify auth search create playlist add tracks"
```

### Step 2: Authenticate
Always call `mcp__spotify__auth-spotify` before any other spotify tool. This must happen every session.

### Step 3: Generate Track List (Claude as Recommender)
DO NOT use `get-recommendations` -- it returns 404 (Spotify deprecated it Nov 2024).

Instead, use your own knowledge to generate a list of ~20-25 artist/track pairs based on the user's request. Guidelines:
- If user names an artist, include 3-4 tracks from that artist plus 8-12 similar artists with 1-2 tracks each
- Cycle through artists for variety (don't group all tracks by one artist together)
- Mix well-known tracks with deeper cuts
- Consider the mood/energy arc of the playlist

### Step 4: Search for Tracks
Search for each track using `mcp__spotify__search-spotify`:
- Use `"Artist Name Track Title"` as the query
- Set `type: "track"` and `limit: 3`
- Pick the first result that matches the correct artist -- search results often include unrelated tracks
- Run searches in parallel batches (4-5 at a time) for speed
- If a track isn't found, skip it and move on

### Step 5: Create Playlist
Use `mcp__spotify__create-playlist` with:
- A descriptive name based on the user's request
- A short description mentioning the featured artists
- `public: false` by default (ask user if they want it public)

### Step 6: Add Tracks
Use `mcp__spotify__add-tracks-to-playlist`:
- Add all found track IDs in one or two calls (max ~50 per call)
- Pass the playlist ID from the create step

### Step 7: Present Results
Show the user:
- Playlist name with Spotify URL
- Numbered track listing with artist names
- Note any tracks that couldn't be found

## API Endpoint Notes (Critical)
These were patched in ~/Code/mcp-claude-spotify to fix 403 errors:
- `create-playlist` uses `POST /me/playlists` (not the deprecated `/users/{userId}/playlists`)
- `add-tracks-to-playlist` uses `POST /playlists/{id}/items` (not the deprecated `/playlists/{id}/tracks`)

If either returns 403, check that the build/index.js has the correct endpoints.

## Example Flow

User: "Make me a playlist of chill acoustic folk"

1. ToolSearch "+spotify auth search create playlist add tracks"
2. auth-spotify
3. Generate list: Iron & Wine - Naked As We Came, Nick Drake - Pink Moon, Fleet Foxes - Mykonos, etc.
4. Search each in parallel batches
5. create-playlist: name="Chill Acoustic Folk", description="Warm acoustic folk -- Iron & Wine, Nick Drake, Fleet Foxes, and more"
6. add-tracks-to-playlist with all found track IDs
7. Present the playlist with link and track listing
