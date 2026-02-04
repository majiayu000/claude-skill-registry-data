---
name: youtube-manager
description: Expert in managing YouTube content using YouTube Data API v3 and yt-dlp. **Use this skill whenever the user mentions 'YouTube', 'video download', 'playlist', 'YouTube videos', 'download from YouTube', or requests to list playlists, search videos, download videos, manage playlists, or any YouTube-related operations.** Handles authentication via OAuth, listing playlists (including Watch Later and Liked Videos), getting playlist items, downloading videos with yt-dlp, searching videos, getting video details, creating/deleting playlists, and adding/removing videos from playlists. (project, gitignored)
---

# YouTube Manager Skill

Expert in managing YouTube content with comprehensive operations including playlist management, video downloads, search, and YouTube Data API v3 integration.

## Core Capabilities

- List user's playlists (including special playlists like Watch Later, Liked Videos)
- Get videos from any playlist
- Download videos using yt-dlp (video or audio-only)
- Search for videos on YouTube
- Get detailed video information
- Create and delete playlists
- Add videos to playlists
- OAuth 2.0 authentication with automatic token management

## When to Use This Skill

Use this skill when users request:
- "List my YouTube playlists"
- "Show me videos from my Watch Later playlist"
- "Download this YouTube video"
- "Search for Alan Walker videos"
- "Get information about video ID xyz"
- "Create a new playlist called 'Favorites'"
- "Add this video to my playlist"
- "Download audio only from this video"

**IMPORTANT:** When the user provides a YouTube URL or video ID, this skill can download the video, get its information, or add it to playlists.

## Available Tools

### YouTube Manager Binary

**Location:** `~/.claude/skills/youtube-manager/scripts/youtube-manager`

**Binary:** Pre-compiled Go executable (no dependencies required)

**Usage:**
```bash
# List playlists
~/.claude/skills/youtube-manager/scripts/youtube-manager list-playlists [--limit N]

# Get playlist videos
~/.claude/skills/youtube-manager/scripts/youtube-manager get-playlist <playlist_id> [--limit N]

# Download video
~/.claude/skills/youtube-manager/scripts/youtube-manager download <url> [--output DIR] [--format FORMAT] [--audio-only]

# Search videos
~/.claude/skills/youtube-manager/scripts/youtube-manager search <query> [--limit N]

# Get video info
~/.claude/skills/youtube-manager/scripts/youtube-manager get-video <video_id>

# Create playlist
~/.claude/skills/youtube-manager/scripts/youtube-manager create-playlist <title> [--description DESC] [--privacy private|public|unlisted]

# Delete playlist
~/.claude/skills/youtube-manager/scripts/youtube-manager delete-playlist <playlist_id>

# Add video to playlist
~/.claude/skills/youtube-manager/scripts/youtube-manager add-to-playlist <playlist_id> <video_id>
```

**Examples:**
```bash
# List all playlists
~/.claude/skills/youtube-manager/scripts/youtube-manager list-playlists

# Get videos from a specific playlist
~/.claude/skills/youtube-manager/scripts/youtube-manager get-playlist PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf

# Download a video
~/.claude/skills/youtube-manager/scripts/youtube-manager download "https://youtube.com/watch?v=dQw4w9WgXcQ"

# Download audio only as MP3
~/.claude/skills/youtube-manager/scripts/youtube-manager download "https://youtube.com/watch?v=dQw4w9WgXcQ" --audio-only

# Search for videos
~/.claude/skills/youtube-manager/scripts/youtube-manager search "Alan Walker EDM"

# Get detailed video information
~/.claude/skills/youtube-manager/scripts/youtube-manager get-video dQw4w9WgXcQ

# Create a new private playlist
~/.claude/skills/youtube-manager/scripts/youtube-manager create-playlist "My Favorites" --description "Best videos" --privacy private

# Add video to playlist
~/.claude/skills/youtube-manager/scripts/youtube-manager add-to-playlist PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf dQw4w9WgXcQ
```

**How It Works:**
The binary is a self-contained Go executable that:
- Requires no Python installation or virtual environment
- Has all dependencies compiled in
- Executes directly without any setup
- Provides instant execution with no overhead

**Operations:**

1. **List Playlists**: Fetch all user playlists with video counts and links
2. **Get Playlist Items**: Retrieve all videos from a specific playlist
3. **Download Video**: Download videos using yt-dlp with format selection (video or audio-only)
4. **Search Videos**: Search YouTube for videos by keyword
5. **Get Video Info**: Fetch detailed information including views, likes, duration, description
6. **Create Playlist**: Create new playlists with privacy settings
7. **Delete Playlist**: Remove playlists from account
8. **Add to Playlist**: Add videos to existing playlists

## Prerequisites

### System Requirements
- **GCP Project** with YouTube Data API v3 enabled
- **Google OAuth Credentials** stored in `~/.credentials/google_credentials.json`
- **yt-dlp** (must be installed separately on the system)

### Google Cloud Setup

1. **Enable YouTube Data API v3:**
   ```bash
   gcloud services enable youtube.googleapis.com
   ```

2. **OAuth Credentials:**
   - Credentials should already exist at `~/.credentials/google_credentials.json`
   - Format:
     ```json
     {
       "installed": {
         "client_id": "...",
         "client_secret": "...",
         "redirect_uris": ["http://localhost"]
       }
     }
     ```

3. **First-time Authentication:**
   ```bash
   # Run any command - will open browser for OAuth consent
   ~/.claude/skills/youtube-manager/scripts/youtube-manager list-playlists

   # Token saved to ~/.credentials/google_token.json for future use
   ```

4. **Subsequent Runs:**
   - Token automatically refreshed when expired
   - No browser interaction needed
   - Seamless authentication

### Installation
**No installation required!** The binary is pre-compiled and ready to use:
- Self-contained Go executable
- No dependencies to install
- No virtual environments needed
- Instant execution

## Common Workflows

### 1. List and Explore Playlists

```bash
# List all playlists
~/.claude/skills/youtube-manager/scripts/youtube-manager list-playlists

# Get videos from a playlist
~/.claude/skills/youtube-manager/scripts/youtube-manager get-playlist PLxxx
```

### 2. Download Videos

```bash
# Download best quality video
~/.claude/skills/youtube-manager/scripts/youtube-manager download "https://youtube.com/watch?v=VIDEO_ID"

# Download to specific directory
~/.claude/skills/youtube-manager/scripts/youtube-manager download "URL" --output ~/Downloads

# Download audio only (MP3)
~/.claude/skills/youtube-manager/scripts/youtube-manager download "URL" --audio-only
```

### 3. Search and Discover

```bash
# Search for videos
~/.claude/skills/youtube-manager/scripts/youtube-manager search "Alan Walker"

# Get detailed video information
~/.claude/skills/youtube-manager/scripts/youtube-manager get-video VIDEO_ID
```

### 4. Manage Playlists

```bash
# Create a new playlist
~/.claude/skills/youtube-manager/scripts/youtube-manager create-playlist "My Collection"

# Add video to playlist
~/.claude/skills/youtube-manager/scripts/youtube-manager add-to-playlist PLAYLIST_ID VIDEO_ID

# Delete playlist
~/.claude/skills/youtube-manager/scripts/youtube-manager delete-playlist PLAYLIST_ID
```

## Best Practices

### Authentication
- **First run:** Browser will open for OAuth consent
- **Token storage:** Credentials saved to `~/.credentials/google_token.json`
- **Auto-refresh:** Token automatically refreshed when expired

### Video Downloads
- **Format selection:** Use `--format best` for highest quality (default)
- **Audio extraction:** Use `--audio-only` for MP3 extraction
- **Output directory:** Specify custom download location with `--output`

### Playlist Management
- **Privacy settings:** Choose private, public, or unlisted when creating
- **Special playlists:** Watch Later and Liked Videos are available
- **Batch operations:** Use shell loops for bulk operations

## How to Respond to YouTube Requests

When users request YouTube operations:

1. **Identify the operation:**
   - List playlists, get playlist items, download, search, get video info, create/delete playlist, add to playlist

2. **Gather required parameters:**
   - Playlist IDs (from list-playlists or provided by user)
   - Video IDs or URLs (from search or provided by user)
   - Download options (format, output directory, audio-only)

3. **Run the appropriate command:**
   - Execute the script with proper arguments
   - Monitor output for progress and errors
   - Report results to user

4. **Handle video IDs and URLs:**
   - Extract video ID from URLs if needed (format: watch?v=VIDEO_ID)
   - Use search to find videos if user provides description

5. **Handle errors:**
   - Check authentication if OAuth errors occur
   - Verify video/playlist IDs if not found
   - Confirm API access if permission errors occur

## Security & Privacy

- **OAuth authentication:** Uses secure OAuth 2.0 flow
- **Local credentials:** Stores credentials in `~/.credentials/`
- **API access:** Only requests minimum required scopes
- **No logging:** Binary does not log or store video content
- **Secure transfer:** All transfers use HTTPS

## Dependencies

The binary is self-contained with all Go dependencies compiled in. External requirements:
- `yt-dlp` - Must be installed separately for video downloads

## Response Approach

To accomplish YouTube management tasks:

1. Identify the specific operation requested
2. Gather required parameters (video IDs, playlist IDs, search queries, etc.)
3. Execute the appropriate command
4. Monitor output for progress and errors
5. Report results with relevant video/playlist information
6. Handle errors with appropriate troubleshooting steps
