---
name: google-slides-translator
description: Expert in Google Slides translation. Use when translating Google Slides presentations to different languages while preserving formatting, whether entire presentations or specific slide ranges.
---

# Google Slides Translator Skill

Expert in translating Google Slides presentations to different languages while preserving all formatting, styles, and layout.

## Core Capabilities

- Translate entire presentations or specific slide ranges
- Auto-detect source language
- Preserve all formatting, styles, colors, and layout
- In-place translation (updates original presentation)
- Support for 100+ languages via Google Cloud Translation API

## When to Use This Skill

Use when users request:
- "Translate this Google Slides presentation to French"
- "Translate slides 10 to 15 to Spanish"
- "Convert this presentation to German"
- "Translate slides 1,5,10 to Italian"

## Quick Start

### Basic Command Pattern
```bash
~/.claude/skills/google-slides-translator/scripts/run.sh translate_slides <presentation_id> <slide_range> <target_lang>
```

### Common Examples
```bash
# Translate all slides to French
~/.claude/skills/google-slides-translator/scripts/run.sh translate_slides 1abc123xyz all fr

# Translate slides 10-15 to Spanish
~/.claude/skills/google-slides-translator/scripts/run.sh translate_slides 1abc123xyz 10-15 es

# Translate specific slides to German
~/.claude/skills/google-slides-translator/scripts/run.sh translate_slides 1abc123xyz 1,5,10 de
```

## Slide Range Formats

- `all` - All slides in presentation
- `5` - Only slide 5
- `10-15` - Slides 10 through 15
- `1,3,5` - Slides 1, 3, and 5
- `2-4,6-8` - Multiple ranges (slides 2-4 and 6-8)

## Common Language Codes

| Language | Code | Language | Code |
|----------|------|----------|------|
| French | `fr` | Spanish | `es` |
| German | `de` | Italian | `it` |
| Portuguese | `pt` | Japanese | `ja` |
| Chinese | `zh` | Korean | `ko` |
| Arabic | `ar` | Russian | `ru` |

For complete list, see: [references/language-codes.md](references/language-codes.md)

## How It Works

The `run.sh` script automatically:
1. Creates isolated virtual environment (`.venv`)
2. Installs dependencies via `uv`
3. Authenticates with Google APIs (OAuth 2.0)
4. Fetches presentation structure
5. Auto-detects source language
6. Translates text using Cloud Translation API
7. Updates presentation in-place with `replaceAllText` (preserves formatting)
8. Reports progress and statistics

No manual setup required - just run the script.

## Prerequisites

### System Requirements
- **uv** - Python package manager (https://docs.astral.sh/uv/)
- **GCP Project** with Translation API enabled
- **OAuth credentials** in `~/.claude/credentials/google_credentials.json`

### Quick Setup
```bash
# Enable required APIs
gcloud services enable slides.googleapis.com translate.googleapis.com

# Create credentials directory
mkdir -p ~/.claude/credentials

# Download OAuth credentials from Google Cloud Console
# Save to ~/.claude/credentials/google_credentials.json
```

First run opens browser for OAuth consent. Token saved for future use.

See [references/authentication.md](references/authentication.md) for detailed setup.

## Translation Workflow

When users request translation:

1. **Extract presentation ID** from URL
   - URL: `https://docs.google.com/presentation/d/1abc123xyz/edit`
   - ID: `1abc123xyz`

2. **Determine slide range**
   - "All slides" → `all`
   - "Slides 10 to 15" → `10-15`
   - "Slide 5" → `5`
   - "Slides 1, 3, 5" → `1,3,5`

3. **Identify target language** (2-letter code)

4. **Execute translation**
   ```bash
   ~/.claude/skills/google-slides-translator/scripts/run.sh translate_slides <id> <range> <lang>
   ```

5. **Monitor output and report results**

## Example Interaction

**User:** "Translate this Google Slides to French: https://docs.google.com/presentation/d/1abc123xyz/edit"

**Response:**
```
I'll translate your Google Slides presentation to French.

Presentation ID: 1abc123xyz
Target Language: French (fr)
Slides: All

Running translation...
```

**Execute:**
```bash
~/.claude/skills/google-slides-translator/scripts/run.sh translate_slides 1abc123xyz all fr
```

**Report:**
```
✅ Translation complete!

Summary:
- Slides translated: 25/25
- Text elements updated: 150
- Target language: French

Your presentation has been successfully translated to French.
All formatting, styles, and layout have been preserved.
```

## Best Practices

- **Backup first:** Make a copy before translating (in-place updates)
- **Monitor output:** Watch for progress and error messages
- **Check formatting:** Review slides after translation
- **API quotas:** Be mindful of Google Cloud Translation API limits

## What Gets Preserved

Using `replaceAllText` API preserves:
- Text formatting (bold, italic, underline)
- Font families and sizes
- Colors and backgrounds
- Text alignment and spacing
- Hyperlinks and special characters

## Limitations

- **Text only:** Images with text not OCR'd
- **No tables:** Table content not translated
- **In-place:** Updates original (no copy created)
- **Sequential:** Processes slides one at a time

## Reference Documentation

- **[script-usage.md](references/script-usage.md)** - Complete command reference, all arguments, slide range patterns
- **[authentication.md](references/authentication.md)** - Google OAuth setup, credentials, first-time auth flow
- **[workflows.md](references/workflows.md)** - Detailed translation workflows, batch processing, examples
- **[language-codes.md](references/language-codes.md)** - Complete list of 100+ supported language codes
- **[troubleshooting.md](references/troubleshooting.md)** - Common errors, authentication issues, quota problems

## Quick Troubleshooting

### "Google OAuth credentials not found"
```bash
mkdir -p ~/.claude/credentials
# Download from Google Cloud Console and save to:
# ~/.claude/credentials/google_credentials.json
```

### "Permission denied"
```bash
gcloud services enable slides.googleapis.com translate.googleapis.com
```

### "Presentation not found"
- Verify presentation ID from URL
- Check you have view/edit access

### "uv not found"
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

For detailed troubleshooting, see: [references/troubleshooting.md](references/troubleshooting.md)
