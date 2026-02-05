---
name: shownotes
description: "Extract transcripts from podcasts and YouTube videos, then create shareable show notes and summaries. Use when the user wants to: (1) Get transcripts from Apple Podcasts or podcast audio files, (2) Extract transcripts from YouTube videos, (3) Create show notes or summaries from audio/video content, (4) Search for podcast episodes or YouTube videos to transcribe, or (5) Turn any audio or video content into structured notes."
---

# Shownotes

## Overview

Facilitate podcast discovery and transcription by helping users find, transcribe, and analyze podcast episodes from Apple Podcasts and YouTube. Extract transcripts using the shownotes.io API service, then create well-formatted show notes, summaries, and shareable content.

## Network Configuration Required

**IMPORTANT:** The shownotes.io API domain must be added to the allowed network domains before this skill can function. The user needs to add `plugins.shownotes.io` to their network settings.

If API calls fail with proxy or connection errors, inform the user they need to update their network settings to allow `plugins.shownotes.io`.

## Core Operations

### 1. Apple Podcast Search

**Purpose:** Search for podcast episodes on Apple Podcasts

**When to use:** User requests a podcast episode by name, topic, or show

**Workflow:**
1. Ask user what podcast episode they're looking for (if not already provided)
2. Use the helper script or make API call to `/apple.php` with query parameter
3. Present up to 3 matching episodes with:
   - Podcast name
   - Episode title
   - Release date
   - Episode description
   - Artwork (display if available, 160px)
   - Audio file URL (enclosure) - allow user to click to listen
4. Ask user to select which episode they want to transcribe
5. **CRITICAL:** Check `protect` field - if `true`, do NOT allow transcription

**Example API Call:**
```bash
python scripts/shownotes_api.py search-apple "Lex Fridman AI"
```

**Response handling:**
- Present search results in organized, scannable format
- Include visual elements (artwork) when available
- If no episodes found, suggest alternative search terms
- Provide clear call-to-action for next steps

### 2. Audio Transcription Request

**Purpose:** Request transcription of selected podcast episode

**When to use:** After user selects an episode from Apple Podcast Search results

**Workflow:**
1. Verify episode is not protected (`protect: false`)
2. Use parameters directly from the selected AppleSearch result:
   - `enclosure`: Audio file URL
   - `podcast`: Podcast name
   - `title`: Episode title
3. Make API call to `/airplugin.php` with these parameters
4. Inform user: "This may take a few minutes and you'll receive an email when ready"
5. Return the `audiolink` where transcript will appear
6. Guide user to check the link for their transcript

**Example API Call:**
```bash
python scripts/shownotes_api.py transcribe "https://audio-url.mp3" "Podcast Name" "Episode Title"
```

**Error handling:**
- If episode is protected, explain transcription is not available
- Set proper expectations about delivery time
- Provide helpful next steps

### 3. Search Existing Transcripts

**Purpose:** Search for existing transcripts on shownotes.io database

**When to use:** User asks if a transcript already exists or wants to retrieve a previously transcribed episode

**Workflow:**
1. Use show name as search parameter
2. Call `/captions-shownotes.php` endpoint
3. Transcript returns with two chunks: `chunk1` and `chunk2`
4. Combine chunks for full transcript

**Example API Call:**
```bash
python scripts/shownotes_api.py get-transcript "Show Name"
```

### 4. YouTube Video Search

**Purpose:** Search YouTube for podcast episodes or videos

**When to use:** User wants to transcribe content from YouTube

**Workflow:**
1. Ask user what show or video they're looking for (if not provided)
2. Use show name to search YouTube via `/search-youtube.php`
3. Return array of 3 video results with name and videoid
4. Present results to user
5. Ask user to select which video to transcribe

**Example API Call:**
```bash
python scripts/shownotes_api.py search-youtube "Huberman Lab"
```

### 5. YouTube Transcript Extraction

**Purpose:** Extract transcript from YouTube video

**When to use:** After user selects a video from YouTube search results, or provides a YouTube video ID directly

**Workflow:**
1. Verify video ID is exactly 11 characters
2. Call `/captions-youtube.php` with videoid parameter
3. Transcript returns in two chunks: `chunk1` and `chunk2`
4. Combine chunks for complete transcript
5. Inform user: "We've also sent an email summary to your inbox"

**CRITICAL RULES:**
- ONLY use the returned transcript content when making summaries or answering questions
- Do NOT embellish or add content beyond what's in the transcript
- Be factual and stick to the source material
- Acknowledge when working with chunked transcript structure

**Example API Call:**
```bash
python scripts/shownotes_api.py get-youtube "dQw4w9WgXcQ"
```

## Creating Show Notes and Summaries

Once transcript is obtained, create well-formatted content:

**Standard Show Notes Format:**
- Title and episode information
- Brief overview/summary (2-3 sentences)
- Key topics covered (bullet points)
- Notable quotes (if applicable)
- Timestamps for major sections (if available in transcript)
- Key takeaways
- Resources mentioned

**Alternative Formats:**
- Executive summary
- Detailed notes with sections
- Q&A format
- Topic-based breakdown
- Action items and insights

**Guidelines:**
- Only work with actual transcript content returned by API
- Do not create content beyond what the API provides
- Maintain professional but friendly tone
- Present information in organized, scannable format
- Be conversational and helpful

## Response Guidelines

**User Interaction:**
- Be conversational and helpful throughout
- Present search results in organized, scannable format
- Include visual elements (artwork) when available
- Provide clear calls-to-action for next steps
- Maintain professional but friendly tone

**Error Handling:**
- If no episodes/videos found, suggest alternative search terms
- If episode is protected, explain transcription is not available
- If transcript extraction fails, guide user to try alternative methods
- Always provide helpful next steps

**Formatting:**
- Use clear headers and sections
- Include relevant metadata (dates, names, etc.)
- Make content scannable with bullet points where appropriate
- Bold key information for emphasis

## API Helper Script

Use `scripts/shownotes_api.py` for all API interactions. The script provides convenience functions for:
- `search-apple <query>` - Search Apple Podcasts
- `transcribe <enclosure> <podcast> <title>` - Request transcription
- `get-transcript <show>` - Get existing transcript
- `search-youtube <show>` - Search YouTube
- `get-youtube <videoid>` - Get YouTube transcript

## Additional Resources

For complete API documentation, see `references/api_reference.md` 
