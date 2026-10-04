---
name: joke-api
description: Fetch random jokes across various categories (Programming, Pun, etc.) via JokeAPI. Use when the user asks for a joke or needs some humor. No API key required.
---

# JokeAPI Skill


Fetch random jokes from the public JokeAPI.

## Usage

```bash
python3 scripts/joke_helper.py [OPTIONS]
```

### Options
- `--category [CATEGORY]`: Programming, Misc, Dark, Pun, Spooky, Christmas, Any (Default: Any)
- `--type [single|twopart]`: Filter by joke format.
- `--blacklist [FLAGS]`: Blacklist specific content flags (comma-separated).
- `--unsafe`: Disable safe-mode (enabled by default).
- `--raw`: Output raw JSON response.

## Examples
- `python3 scripts/joke_helper.py --category Programming`
- `python3 scripts/joke_helper.py --type twopart`

## API Information
- Source: [JokeAPI](https://sv443.net/jokeapi/v2/)
- Auth: No API Key required.
