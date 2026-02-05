---
name: wavecap-search
description: Search WaveCap transcriptions with text queries and filters. Use when the user wants to find specific transcriptions, search for keywords, or query transcription history.
---

# WaveCap Search Skill

Use this skill to search through transcription history in WaveCap.

## Search Transcriptions for a Stream

### Basic Search

```bash
curl -s "http://localhost:8000/api/streams/{STREAM_ID}/transcriptions?search=fire&limit=20" | jq
```

### Search Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `search` | string | - | Text to search for in transcriptions |
| `limit` | int | 100 | Maximum results to return |
| `before` | ISO8601 | - | Get transcriptions before this timestamp |
| `after` | ISO8601 | - | Get transcriptions after this timestamp |
| `order` | string | desc | Sort order: `asc` or `desc` |

### Search with Time Range

```bash
# Search in the last hour
AFTER=$(date -u -v-1H +"%Y-%m-%dT%H:%M:%SZ")
curl -s "http://localhost:8000/api/streams/{STREAM_ID}/transcriptions?search=emergency&after=$AFTER" | jq
```

```bash
# Search within a specific date range
curl -s "http://localhost:8000/api/streams/{STREAM_ID}/transcriptions?search=incident&after=2025-01-15T00:00:00Z&before=2025-01-16T00:00:00Z" | jq
```

### Pagination

The response includes pagination hints:

```json
{
  "transcriptions": [...],
  "hasMoreBefore": true,
  "hasMoreAfter": false
}
```

To get the next page:
```bash
# Get the timestamp of the last result, then use it as 'before'
LAST_TIMESTAMP="2025-01-15T12:30:00Z"
curl -s "http://localhost:8000/api/streams/{STREAM_ID}/transcriptions?before=$LAST_TIMESTAMP&limit=20" | jq
```

## Search Across All Streams

To search across all streams, first get the stream list, then query each:

```bash
# Get all stream IDs
STREAMS=$(curl -s "http://localhost:8000/api/streams?includeTranscriptions=false" | jq -r '.[].id')

# Search each stream
for STREAM_ID in $STREAMS; do
  echo "=== Stream: $STREAM_ID ==="
  curl -s "http://localhost:8000/api/streams/$STREAM_ID/transcriptions?search=YOUR_QUERY&limit=5" | jq '.transcriptions[] | {timestamp, text}'
done
```

## Format Search Results

### Show just text and timestamps
```bash
curl -s "http://localhost:8000/api/streams/{STREAM_ID}/transcriptions?search=fire" | \
  jq '.transcriptions[] | "\(.timestamp): \(.text)"' -r
```

### Show with confidence scores
```bash
curl -s "http://localhost:8000/api/streams/{STREAM_ID}/transcriptions?search=ambulance" | \
  jq '.transcriptions[] | {time: .timestamp, text, confidence: (.confidence * 100 | floor | tostring + "%")}'
```

### Filter by confidence threshold
```bash
curl -s "http://localhost:8000/api/streams/{STREAM_ID}/transcriptions?limit=50" | \
  jq '[.transcriptions[] | select(.confidence > 0.8)] | length'
```

## Transcription Fields

Each transcription contains:
```json
{
  "id": "uuid",
  "streamId": "stream-id",
  "text": "transcribed text",
  "timestamp": "2025-01-15T12:30:00Z",
  "confidence": 0.95,
  "duration": 30.5,
  "segments": [...],
  "recordingUrl": "/recordings/file.wav",
  "reviewStatus": "pending",
  "correctedText": null,
  "alerts": [...]
}
```

## Tips

- The search is case-insensitive
- Use `order=asc` to get oldest results first (useful for timeline analysis)
- Combine `after` and `before` for precise time windows
- Large result sets should use pagination to avoid timeouts
