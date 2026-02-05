---
name: video-processing
description: Use when processing YouTube videos, extracting subtitles, parsing VTT files, analyzing video content, generating timestamps, or creating video summaries
---

# Video Processing & Analysis

**When to use**: YouTube video automation, subtitle extraction, transcript analysis, video content indexing, or generating show notes.

## Overview

Production-ready tools for video content processing with subtitle extraction, timestamp handling, and AI-powered analysis.

## Key Capabilities

- ✅ YouTube subtitle download (multiple languages)
- ✅ VTT subtitle parsing with timestamp preservation
- ✅ Video duration checking
- ✅ Timestamp validation
- ✅ Batch screenshot generation
- ✅ Video metadata extraction

## Prerequisites

```bash
# Install required tools
npm install -g yt-dlp  # or: pip install yt-dlp

# Install ffmpeg (for video processing)
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows
# Download from: https://ffmpeg.org/download.html
```

## Core Operations

### 1. Download YouTube Subtitles

```bash
# Download auto-generated English subtitles
yt-dlp --write-auto-sub --sub-lang en --skip-download \
  --sub-format vtt -o "subtitle.%(ext)s" \
  "https://www.youtube.com/watch?v=VIDEO_ID"

# Download manual subtitles (if available)
yt-dlp --write-sub --sub-lang en --skip-download \
  --sub-format vtt -o "subtitle.%(ext)s" \
  "https://www.youtube.com/watch?v=VIDEO_ID"

# Multiple languages
yt-dlp --write-auto-sub --sub-lang en,zh,ja --skip-download \
  --sub-format vtt -o "subtitle.%(ext)s" \
  "VIDEO_URL"
```

### 2. Parse VTT Subtitles with Timestamps

**Key Feature**: Preserves timing information for quote attribution.

```javascript
// VTT Parser (ES5 compatible)
function parseVTT(vttContent) {
  var lines = vttContent.split('\n');
  var segments = [];
  var currentSegment = null;

  for (var i = 0; i < lines.length; i++) {
    var line = lines[i].trim();

    // Timestamp line: 00:01:23.456 --> 00:01:26.789
    if (line.match(/^\d{2}:\d{2}:\d{2}\.\d{3}/)) {
      var timestamps = line.split(' --> ');
      currentSegment = {
        start: timestamps[0],
        end: timestamps[1],
        text: ''
      };
    }
    // Text line
    else if (currentSegment && line.length > 0 && !line.match(/^\d+$/)) {
      currentSegment.text += (currentSegment.text ? ' ' : '') + line;
    }
    // Empty line (segment end)
    else if (currentSegment && line.length === 0) {
      segments.push(currentSegment);
      currentSegment = null;
    }
  }

  return segments;
}

// Convert to timestamped text
function formatWithTimestamps(segments) {
  var result = '';
  for (var i = 0; i < segments.length; i++) {
    var seg = segments[i];
    result += '[' + seg.start.substring(0, 8) + '] ' + seg.text + '\n';
  }
  return result;
}

// Usage
var vttContent = $input.item.binary.data.toString('utf-8');
var segments = parseVTT(vttContent);
var timestampedText = formatWithTimestamps(segments);

return {
  json: {
    transcript: timestampedText,
    segments: segments,
    segmentCount: segments.length
  }
};
```

### 3. Video Duration Check

```bash
# Get video duration
ffprobe -v error -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 \
  video.mp4

# Get duration in HH:MM:SS format
ffprobe -v error -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 \
  -sexagesimal video.mp4
```

```javascript
// Validate timestamp against video duration
function validateTimestamp(timestamp, videoDuration) {
  // Parse timestamp: 00:01:23 or 01:23
  var parts = timestamp.split(':').map(function(p) {
    return parseInt(p, 10);
  });

  var seconds;
  if (parts.length === 3) {
    seconds = parts[0] * 3600 + parts[1] * 60 + parts[2];
  } else if (parts.length === 2) {
    seconds = parts[0] * 60 + parts[1];
  } else {
    return false;
  }

  return seconds <= videoDuration;
}
```

### 4. Batch Screenshot Generation

```bash
# Single screenshot at timestamp
ffmpeg -ss 00:01:23 -i video.mp4 -vframes 1 -q:v 2 screenshot.jpg

# Multiple screenshots
# timestamps.txt:
# 00:00:30
# 00:01:45
# 00:03:20

while read timestamp; do
  filename="screenshot_${timestamp//:/}.jpg"
  ffmpeg -ss $timestamp -i video.mp4 -vframes 1 -q:v 2 $filename
done < timestamps.txt
```

```javascript
// Generate screenshot filenames for batch
function generateScreenshotBatch(timestamps, videoFile) {
  var commands = [];

  for (var i = 0; i < timestamps.length; i++) {
    var ts = timestamps[i];
    var filename = 'screenshot_' + ts.replace(/:/g, '') + '.jpg';
    var command = 'ffmpeg -ss ' + ts + ' -i ' + videoFile +
                  ' -vframes 1 -q:v 2 ' + filename;
    commands.push({
      timestamp: ts,
      filename: filename,
      command: command
    });
  }

  return commands;
}
```

### 5. Extract Video Metadata

```bash
# Get all metadata
ffprobe -v quiet -print_format json -show_format -show_streams video.mp4

# Get specific fields
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,codec_name,bit_rate \
  -of json video.mp4
```

## Complete Workflow: YouTube → Analysis → Notion

```
[Manual/Webhook Trigger]
    Video URL
    ↓
[Download Subtitle]
    yt-dlp --write-auto-sub
    ↓
[Parse VTT]
    Extract segments with timestamps
    ↓
[AI Analysis]
    Generate summary, quotes, tags
    ↓
[Validate Timestamps]
    Check quotes are within video duration
    ↓
[Download Video]
    (if screenshots needed)
    ↓
[Generate Screenshots]
    For key moments/quotes
    ↓
[Save to Notion]
    Structured data with timestamps
```

## n8n Implementation

### Workflow Structure

```javascript
// Node 1: Download Subtitle
var execSync = require('child_process').execSync;
var videoUrl = $input.item.json.url;
var outputPath = '/tmp/subtitle.vtt';

var command = 'yt-dlp --write-auto-sub --sub-lang en ' +
              '--skip-download --sub-format vtt ' +
              '-o "' + outputPath + '" "' + videoUrl + '"';

execSync(command);

return {
  json: {
    videoUrl: videoUrl,
    subtitlePath: outputPath
  }
};
```

```javascript
// Node 2: Parse VTT
var fs = require('fs');
var vttContent = fs.readFileSync($input.item.json.subtitlePath, 'utf8');

var segments = parseVTT(vttContent);
var fullTranscript = formatWithTimestamps(segments);

return {
  json: Object.assign({}, $input.item.json, {
    transcript: fullTranscript,
    segments: segments
  })
};
```

```javascript
// Node 3: AI Analysis (use ai-integration skill)
var prompt = 'Analyze this video transcript and extract:\n' +
             '1. Summary (2-3 sentences)\n' +
             '2. Key quotes with their timestamps\n' +
             '3. Main topics/tags\n\n' +
             'Transcript:\n' + $input.item.json.transcript;

// Call AI API...
```

```javascript
// Node 4: Validate Timestamps
var quotes = $input.item.json.aiAnalysis.quotes;
var videoDuration = $input.item.json.duration;

var validQuotes = [];
for (var i = 0; i < quotes.length; i++) {
  var quote = quotes[i];
  if (validateTimestamp(quote.timestamp, videoDuration)) {
    validQuotes.push(quote);
  } else {
    // Adjust or skip invalid timestamps
    console.log('Invalid timestamp: ' + quote.timestamp);
  }
}

return {
  json: Object.assign({}, $input.item.json, {
    validatedQuotes: validQuotes
  })
};
```

## Best Practices

1. **Language Detection**: Try auto-generated subtitles first, fall back to manual
2. **Timestamp Format**: Always use HH:MM:SS format for consistency
3. **Validation**: Check timestamps against video duration before using
4. **Caching**: Save downloaded subtitles to avoid re-downloading
5. **Error Handling**: Not all videos have subtitles, handle gracefully
6. **File Cleanup**: Delete temporary files after processing

## Common Patterns

### Pattern 1: Video Indexing
```
YouTube Channel → Get New Videos → Download Subtitles →
Parse & Index → Searchable Database
```

### Pattern 2: Show Notes Generation
```
Video URL → Subtitles → AI Analysis →
Generate Summary + Timestamps → Export Markdown
```

### Pattern 3: Quote Attribution
```
Transcript with Timestamps → AI Extract Quotes →
Validate Timestamps → Generate Screenshots →
Create Social Media Posts
```

## Troubleshooting

### No subtitles available
```javascript
// Try both auto and manual
try {
  execSync('yt-dlp --write-sub ...');  // Manual first
} catch (e) {
  execSync('yt-dlp --write-auto-sub ...');  // Fallback to auto
}
```

### VTT parsing errors
```javascript
// Handle malformed VTT
if (!line.match(/^WEBVTT/) && i === 0) {
  throw new Error('Invalid VTT format');
}
```

### Timestamp validation fails
```javascript
// Adjust out-of-range timestamps to video end
if (seconds > videoDuration) {
  seconds = videoDuration - 5;  // 5 seconds before end
}
```

### ffmpeg not found
```bash
# Check PATH includes ffmpeg
export PATH="/usr/local/bin:/opt/homebrew/bin:$PATH"
```

## Integration with Other Skills

- **oauth-automation**: Authenticate YouTube API
- **ai-integration**: Analyze transcript content
- **notion-operations**: Save structured video data
- **error-handling**: Retry on download failures

## Full Code and Documentation

Complete implementations:
`/mnt/d/work/n8n_agent/n8n-skills/video-processing/`

Files:
- `vtt-subtitle-parser.js` - VTT parsing with timestamps
- `video-duration-checker.js` - Duration validation
- `batch-screenshot.js` - Screenshot generation
- `youtube-downloader.js` - Download wrapper
- `README.md` - Complete guide and examples
