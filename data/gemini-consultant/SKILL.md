---
name: gemini-consultant
description: Get a second opinion from Gemini 3 Pro with Google Search grounding and vision. Use when you need real-time web information, want to verify facts, need a different perspective on a technical question, want to consult another AI model, or need to analyze images.
allowed-tools: Bash, Read
---

# Gemini Consultant

Get a second opinion from Google's Gemini 3 Pro (`gemini-3-pro-preview`) with real-time Google Search grounding and vision capabilities.

## Prerequisites

The user must have `GEMINI_API_KEY` environment variable set with a valid Google AI API key.

## Usage

The script is located in the same directory as this SKILL.md file. Run it with `uv run`:

```bash
uv run /path/to/skills/gemini-consultant/consult.py "your question here"
```

When this skill is invoked, locate `consult.py` in the skill directory and run it.

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `question` | Yes | The question to ask Gemini |
| `-c`, `--context` | No | Additional context to include (code snippets, background info) |
| `-i`, `--image` | No | Image file(s) to analyze (can be used multiple times) |
| `--media-resolution` | No | Image resolution: `low` (280 tokens), `medium` (560, default), `high` (1120), `ultra_high` |
| `--no-search` | No | Disable Google Search grounding (use pure model knowledge) |
| `--thinking` | No | Reasoning depth: `low` (faster) or `high` (deeper, default) |

### Examples

Simple question with web search:
```bash
uv run consult.py "What is the latest version of Python and its new features?"
```

Question with context:
```bash
uv run consult.py "What could cause this error?" -c "TypeError: Cannot read property 'map' of undefined"
```

Fast response without deep reasoning:
```bash
uv run consult.py "Quick summary of REST vs GraphQL" --thinking low
```

Without web search (pure model knowledge):
```bash
uv run consult.py "Explain the CAP theorem" --no-search
```

Analyze an image:
```bash
uv run consult.py "What's in this image?" -i screenshot.png
```

Analyze multiple images:
```bash
uv run consult.py "Compare these two diagrams" -i diagram1.png -i diagram2.png
```

High-resolution image analysis (for fine text or small details):
```bash
uv run consult.py "Read the text in this image" -i document.png --media-resolution high
```

## When to Use

- **Real-time information**: Current events, latest releases, recent updates
- **Fact verification**: Double-check information with web sources
- **Second opinion**: Get an alternative perspective on technical decisions
- **Web research**: Find current documentation, tutorials, or solutions
- **Image analysis**: Analyze screenshots, diagrams, photos, or any visual content
- **Compare images**: Analyze multiple images together

## Output

The script prints:
- The model's response
- Sources/citations from Google Search (when grounding is enabled)
