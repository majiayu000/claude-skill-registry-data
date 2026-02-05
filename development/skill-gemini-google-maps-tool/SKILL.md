---
name: skill-gemini-google-maps-tool
description: Query Gemini with Google Maps grounding
---

# When to use
- When you need location-aware AI responses about places
- When you need recommendations for restaurants, hotels, attractions
- When you need accurate, up-to-date information from Google Maps

# Gemini Google Maps Tool Skill

## Purpose

Comprehensive guide for using gemini-google-maps-tool, a CLI and Python library that connects Gemini to Google Maps' database of 250+ million places worldwide for location-aware responses with accurate, up-to-date information.

## When to Use This Skill

**Use this skill when:**
- Querying for location-based recommendations (restaurants, hotels, attractions)
- Generating itineraries with place-specific information
- Building applications that need location-aware AI responses
- Integrating Google Maps data into AI workflows
- Creating travel, food, or local business applications

**Do NOT use this skill for:**
- General Gemini queries without location context
- Tasks that don't involve places or geographical information
- Direct Google Maps API queries (this uses Gemini with Maps grounding)

## CLI Tool: gemini-google-maps-tool

A production-ready CLI and Python library for querying Gemini with Google Maps grounding.

### Installation

```bash
# Install globally with uv tool
uv tool install gemini-google-maps-tool

# Or from source
git clone https://github.com/dnvriend/gemini-google-maps-tool.git
cd gemini-google-maps-tool
uv tool install .
```

### Prerequisites

- Python 3.14+
- [uv](https://github.com/astral-sh/uv) package manager
- Gemini API Key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### Quick Start

```bash
# Set API key
export GEMINI_API_KEY="your-api-key"

# Basic query
gemini-google-maps-tool query "Best coffee shops in Amsterdam"

# With location context
gemini-google-maps-tool query "Italian restaurants nearby" \
  --lat-lon "52.37,4.89"

# Markdown output with sources
gemini-google-maps-tool query "Museums in Paris" --text
```

## Progressive Disclosure

<details>
<summary><strong>📖 Core Commands (Click to expand)</strong></summary>

### query - Query Gemini with Google Maps Grounding

Query Gemini with Google Maps integration for location-aware information about places, businesses, directions, and attractions.

**Usage:**
```bash
gemini-google-maps-tool query "QUERY" [OPTIONS]
```

**Arguments:**
- `QUERY`: The search query (required unless using --stdin)
- `--lat-lon LAT,LON`: Location coordinates in format "lat,lon" (e.g., "37.78193,-122.40476")
- `--model {flash|flash-lite}`: Model selection
  - `flash`: gemini-2.5-flash (more powerful, higher cost)
  - `flash-lite`: gemini-2.5-flash-lite (default, faster, cost-effective)
- `-v, --verbose`: Enable INFO logging (operation-level details)
- `-vv`: Enable DEBUG logging (detailed API calls, validation)
- `-vvv`: Enable TRACE logging (full HTTP traces, library internals)
- `--text` / `-t`: Output markdown text instead of JSON
- `--stdin` / `-s`: Read query from stdin

**Examples:**
```bash
# Basic query
gemini-google-maps-tool query "Best coffee shops in Amsterdam"

# With location context
gemini-google-maps-tool query "Italian restaurants nearby" \
  --lat-lon "52.37,4.89"

# Using different model
gemini-google-maps-tool query "Plan a day in NYC" --model flash

# Markdown output with sources
gemini-google-maps-tool query "Best museums in Paris" --text

# Verbose mode with grounding metadata
gemini-google-maps-tool query "Sushi restaurants" -v

# Debug mode with full details
gemini-google-maps-tool query "Hotels in London" -vv

# Trace mode with HTTP details
gemini-google-maps-tool query "Attractions in Rome" -vvv

# Reading from stdin (for pipelines)
echo "Best bakeries in San Francisco" | \
  gemini-google-maps-tool query --stdin

# Pipeline with jq
gemini-google-maps-tool query "Coffee shops" | \
  jq '.response_text'
```

**Output Formats:**

JSON (default):
```json
{
  "response_text": "Here are some great coffee shops...",
  "grounding_metadata": {
    "grounding_chunks": [
      {
        "title": "Blue Bottle Coffee",
        "uri": "https://maps.google.com/?cid=...",
        "place_id": "places/ChIJ..."
      }
    ]
  }
}
```

Markdown (with --text):
```markdown
Here are some great coffee shops...

---

## Sources

1. [Blue Bottle Coffee](https://maps.google.com/?cid=...)
2. [Philz Coffee](https://maps.google.com/?cid=...)
```

---

### completion - Generate Shell Completion Scripts

Generate shell completion scripts for Bash, Zsh, or Fish to enable tab-completion for commands and options.

**Usage:**
```bash
gemini-google-maps-tool completion {bash|zsh|fish}
```

**Arguments:**
- `SHELL`: Shell type (required) - bash, zsh, or fish

**Examples:**
```bash
# Bash - temporary (current session)
eval "$(gemini-google-maps-tool completion bash)"

# Bash - persistent
echo 'eval "$(gemini-google-maps-tool completion bash)"' >> ~/.bashrc

# Zsh - temporary
eval "$(gemini-google-maps-tool completion zsh)"

# Zsh - persistent
echo 'eval "$(gemini-google-maps-tool completion zsh)"' >> ~/.zshrc

# Fish - install to completions directory
gemini-google-maps-tool completion fish > \
  ~/.config/fish/completions/gemini-google-maps-tool.fish

# File-based (better performance)
gemini-google-maps-tool completion bash > \
  ~/.gemini-google-maps-tool-complete.bash
echo 'source ~/.gemini-google-maps-tool-complete.bash' >> ~/.bashrc
```

**Output:**
Shell-specific completion script that can be evaluated or saved to a file.

</details>

<details>
<summary><strong>⚙️ Advanced Features (Click to expand)</strong></summary>

### Multi-Level Verbosity Logging

Progressive detail control for debugging and monitoring:

- **No flag (default)**: WARNING level - only critical issues
- **`-v`**: INFO level - high-level operations, important events
- **`-vv`**: DEBUG level - detailed operations, API calls, validation steps
- **`-vvv`**: TRACE level - full request/response, library internals, HTTP traces

**Examples:**
```bash
# INFO: See which files are processed
gemini-google-maps-tool query "Best restaurants" -v

# DEBUG: See API call details and validation
gemini-google-maps-tool query "Hotels nearby" -vv

# TRACE: See full HTTP requests/responses
gemini-google-maps-tool query "Museums" -vvv
```

---

### Google Maps Grounding

**What is it?**
Google Maps grounding connects Gemini to Google Maps' database of 250+ million places worldwide, providing:
- Location-aware responses with accurate, up-to-date information
- Personalized recommendations tailored to specific areas
- Automatic citation generation with structured sources
- Seamless integration via Gemini's API

**Grounding Metadata:**
With `-v` or `--text`, responses include:
- **Grounding Chunks**: Google Maps sources (title, URI, place_id)
- **Grounding Supports**: Text segments linked to sources
- **Widget Context Token**: For interactive maps integration

**Example:**
```bash
gemini-google-maps-tool query "Best pizza in Brooklyn" -v
```

Returns JSON with:
```json
{
  "response_text": "...",
  "grounding_metadata": {
    "grounding_chunks": [
      {
        "title": "Roberta's Pizza",
        "uri": "https://maps.google.com/?cid=...",
        "place_id": "places/ChIJ..."
      }
    ],
    "grounding_supports": [...],
    "google_maps_widget_context_token": "..."
  }
}
```

---

### Location Context

Provide location coordinates for personalized, location-aware responses:

**Format:** `--lat-lon "latitude,longitude"`

**Examples:**
```bash
# Amsterdam center
gemini-google-maps-tool query "Coffee shops nearby" \
  --lat-lon "52.37,4.89"

# San Francisco
gemini-google-maps-tool query "Italian restaurants" \
  --lat-lon "37.78,-122.40"

# Tokyo
gemini-google-maps-tool query "Sushi restaurants" \
  --lat-lon "35.68,139.76"
```

**Coordinate Ranges:**
- Latitude: -90 to 90
- Longitude: -180 to 180

---

### Model Selection

Choose between two Gemini models:

**flash-lite (default):**
- Model: gemini-2.5-flash-lite
- Faster, more cost-effective
- Best for simple location queries
- Recommended for most use cases

**flash:**
- Model: gemini-2.5-flash
- More powerful and capable
- Best for complex queries and itinerary planning
- Higher cost

**Examples:**
```bash
# Default (flash-lite)
gemini-google-maps-tool query "Best restaurants"

# Explicit flash-lite
gemini-google-maps-tool query "Hotels" --model flash-lite

# Use flash for complex queries
gemini-google-maps-tool query "Plan a 3-day trip to Paris" \
  --model flash
```

---

### Python Library Usage

Import and use programmatically in Python applications:

**Basic Usage:**
```python
from gemini_google_maps_tool import get_client, query_maps

# Initialize client
client = get_client()

# Execute query
result = query_maps(
    client=client,
    query="Best coffee shops near me",
)

print(result.response_text)
```

**With Location and Grounding:**
```python
from gemini_google_maps_tool import get_client, query_maps

client = get_client()

result = query_maps(
    client=client,
    query="Italian restaurants nearby",
    lat_lon=(37.78193, -122.40476),
    model="gemini-2.5-flash",
    include_grounding=True,
)

# Access response
print(result.response_text)

# Access grounding metadata
if result.grounding_metadata:
    for chunk in result.grounding_metadata.grounding_chunks:
        print(f"Source: {chunk.title} - {chunk.uri}")
```

**Error Handling:**
```python
from gemini_google_maps_tool import (
    get_client,
    query_maps,
    ClientError,
    QueryError,
)

try:
    client = get_client()
    result = query_maps(client, "Best restaurants")
    print(result.response_text)
except ClientError as e:
    print(f"Client error: {e}")
except QueryError as e:
    print(f"Query error: {e}")
```

</details>

<details>
<summary><strong>🔧 Troubleshooting (Click to expand)</strong></summary>

### Common Issues

**Issue: GEMINI_API_KEY not set**
```bash
Error: GEMINI_API_KEY environment variable is required.
```

**Solution:**
```bash
# Set for current session
export GEMINI_API_KEY="your-api-key"

# Or add to shell profile
echo 'export GEMINI_API_KEY="your-api-key"' >> ~/.zshrc
source ~/.zshrc

# Or retrieve from macOS Keychain
export GEMINI_API_KEY=$(security find-generic-password \
  -a "production" -s "GEMINI_API_KEY" -w)
```

---

**Issue: Invalid lat-lon format**
```bash
ValueError: Invalid lat-lon format
```

**Solution:**
- Use format: "latitude,longitude"
- Latitude range: -90 to 90
- Longitude range: -180 to 180
```bash
# Correct
gemini-google-maps-tool query "restaurants" --lat-lon "52.37,4.89"

# Incorrect
gemini-google-maps-tool query "restaurants" --lat-lon "52.37 4.89"
gemini-google-maps-tool query "restaurants" --lat-lon "200,50"
```

---

**Issue: API returns no response candidates**
```bash
QueryError: API returned no response candidates
```

**Possible causes:**
- Rate limiting (too many requests)
- API service issues
- Query content filtering
- Insufficient API quota

**Solution:**
- Wait a few seconds and retry
- Rephrase your query
- Check API quota in Google Cloud Console
- Verify API key is valid and active

---

**Issue: Empty response text**
```bash
QueryError: API returned empty response text
```

**Possible causes:**
- Content filtering or safety blocks
- Query processing issues
- Incomplete API response

**Solution:**
- Rephrase query with different wording
- Try simpler or more specific query
- Wait and retry
- Check if query violates content policies

---

### Getting Help

```bash
# Main help
gemini-google-maps-tool --help

# Command-specific help
gemini-google-maps-tool query --help
gemini-google-maps-tool completion --help

# Version information
gemini-google-maps-tool --version
```

### Debug Mode

Enable verbose logging to diagnose issues:

```bash
# INFO level
gemini-google-maps-tool query "test" -v

# DEBUG level (detailed)
gemini-google-maps-tool query "test" -vv

# TRACE level (full HTTP traces)
gemini-google-maps-tool query "test" -vvv
```

</details>

## Output Formats

**JSON (default):**
- Structured data with `response_text` field
- Optional `grounding_metadata` with `-v`
- Easy to parse and pipe to other tools
- Logs to stderr, JSON to stdout

**Markdown (--text):**
- Human-readable text
- Automatic source citations
- Clean formatting
- Includes "Sources" section with links

## Best Practices

1. **Use location context for better results**: Provide `--lat-lon` when asking about specific areas
2. **Choose appropriate model**: Use `flash-lite` (default) for simple queries, `flash` for complex tasks
3. **Enable verbosity for debugging**: Use `-v`, `-vv`, or `-vvv` to understand what's happening
4. **Secure API key storage**: Use environment variables or keychain instead of hardcoding
5. **Monitor API usage**: Google Maps grounding costs $25 per 1,000 prompts
6. **Use JSON for automation**: Default JSON output is perfect for scripts and pipelines
7. **Cache completion scripts**: Generate to file instead of eval for better performance

## Pricing

- **Google Maps Grounding**: $25 per 1,000 grounded prompts
- **Free Tier**: Up to 500 requests per day
- **Monitor usage**: [Google Cloud Console](https://console.cloud.google.com/)

Learn more: [Gemini API Pricing](https://ai.google.dev/pricing)

## Resources

- **GitHub**: https://github.com/dnvriend/gemini-google-maps-tool
- **Google Maps Grounding Docs**: https://ai.google.dev/gemini-api/docs/maps-grounding
- **Gemini API Documentation**: https://ai.google.dev/gemini-api/docs
- **Get API Key**: https://aistudio.google.com/app/apikey
- **Google AI Studio**: https://aistudio.google.com/
