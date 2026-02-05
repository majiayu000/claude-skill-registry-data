---
name: kit
description: Fetch Kit (ConvertKit) newsletter broadcasts for writing context. Use when asked to download newsletters, get past email content for style reference, or fetch broadcasts for analysis.
---

# Kit Broadcasts Fetcher

Use the `kit-broadcasts` CLI to fetch newsletters from Kit (ConvertKit). Useful for retrieving past newsletter content as context for writing new newsletters in a consistent style.

## Usage

```bash
# Fetch all broadcasts to stdout (JSON format)
kit-broadcasts

# Save to file
kit-broadcasts -o broadcasts.json

# Verbose mode shows progress
kit-broadcasts -v -o broadcasts.json

# Include all fields (not just simplified data)
kit-broadcasts --full -o broadcasts.json

# Use specific API key
kit-broadcasts --api-key "your-key"
```

## Arguments

| Argument | Short | Description |
|----------|-------|-------------|
| `--output` | `-o` | Output file path (default: stdout) |
| `--api-key` | `-k` | Kit API key (or set KIT_API_KEY env var) |
| `--full` | | Include all fields, not just subject/preview/content |
| `--verbose` | `-v` | Show progress info |

## Output Format

Default (simplified):
```json
[
  {
    "id": 123,
    "subject": "Newsletter Subject",
    "preview_text": "Preview text...",
    "content": "<html>...</html>",
    "created_at": "2024-01-15T10:00:00Z",
    "send_at": "2024-01-15T12:00:00Z",
    "stats": {"open_rate": 45.2, "click_rate": 3.1}
  }
]
```

## Requirements

1. **Install the hamel package:**
   ```bash
   pip install hamel
   ```

2. **Set environment variable:**
   ```bash
   export KIT_API_KEY="your-v4-api-key"
   ```
   
   Get your V4 API key from [Kit Developer Settings](https://app.kit.com/account_settings/developer_settings). The API key is tied to your Kit account - no separate account ID needed.

## Examples

**Fetch newsletters as writing context:**
```bash
kit-broadcasts -o newsletters.json
# Use the content field as examples for writing new newsletters
```

**Get recent newsletters for style reference:**
```bash
kit-broadcasts | jq '.[0:5]'  # First 5 (most recent) newsletters
```

**Analyze newsletter performance:**
```bash
kit-broadcasts -o newsletters.json
# Check stats.open_rate and stats.click_rate to identify best-performing content
```

**Pipe to AI for summarization:**
```bash
kit-broadcasts | ai-gem "List the main topics covered in these newsletters"
```
