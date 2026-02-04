---
name: subtitle-to-document
description: "Convert subtitle files (WebVTT .vtt and SubRip .srt) into clean, readable text documents with multi-language support (English, Traditional Chinese, Simplified Chinese). Auto-detects format and language, removes timestamps and formatting, merges captions into natural paragraphs, strips annotations, and fixes spacing appropriately for each language. Use when the user provides a subtitle file or asks to convert captions to text."
---

# Subtitles to Document

Convert WebVTT (.vtt) and SubRip (.srt) subtitle files into clean, readable text documents with natural paragraph flow and multi-language support.

## Supported Languages

- **English (en)** - Automatic capitalization, space-based word separation
- **Traditional Chinese (zh_tw / \u7e41\u9ad4\u4e2d\u6587)** - Chinese punctuation detection, no spaces between characters
- **Simplified Chinese (zh_cn / \u7b80\u4f53\u4e2d\u6587)** - Chinese punctuation detection, no spaces between characters

The script auto-detects the subtitle format (VTT or SRT) and the language by default.

## Quick Start

### Auto-detect Format and Language (Default)

When the user provides a subtitle file path, run the conversion script:

```bash
python scripts/subtitle_to_text.py input.vtt
# or
python scripts/subtitle_to_text.py input.srt
```

This creates `input.txt` in the same directory with cleaned, formatted text.

### Specify Language or Format

```bash
# English
python scripts/subtitle_to_text.py input.srt --lang en

# Traditional Chinese
python scripts/subtitle_to_text.py input.vtt --lang zh_tw

# Force SRT parsing
python scripts/subtitle_to_text.py input.srt --format srt
```

### Specify Custom Output Path

```bash
python scripts/subtitle_to_text.py input.srt output.txt --lang zh_tw
```

## What the Script Does

The `subtitle_to_text.py` script automatically performs format- and language-aware processing:

### All Formats
1. **Removes timestamps** - Strips VTT/SRT timing information (e.g., `00:00:00.000 --> 00:00:02.500` or `00:00:00,000 --> 00:00:02,500`)
2. **Removes subtitle formatting** - Strips tags like `<v Speaker>`, `<c>`, `<i>`, etc.
3. **Removes duplicates** - Detects and removes consecutive duplicate captions

### Language-Specific Processing

#### English (en)
- **Sentence detection**: `.`, `!`, `?`
- **Annotations removed**: `[Music]`, `[Applause]`, `[Laughter]`, `[Inaudible]`
- **Capitalization**: Auto-capitalizes sentences and fixes `i` -> `I`
- **Spacing**: Adds spaces between words, fixes punctuation spacing

#### Traditional Chinese (zh_tw)
- **Sentence detection**: `\u3002`, `\uff01`, `\uff1f`
- **Annotations removed**: `[...]` (Chinese and English annotations)
- **Capitalization**: Not applicable
- **Spacing**: Removes spaces between Chinese characters, preserves spacing around embedded English words

#### Simplified Chinese (zh_cn)
- Same behavior as Traditional Chinese, using simplified character indicators for detection

## Format Detection

Format detection uses file extension (`.vtt` / `.srt`) and content heuristics (`WEBVTT` header, presence of `-->` timestamps). You can override detection with `--format`.

If auto-detection is incorrect, override with `--format srt` or `--format vtt`, or set `--lang` to force language.

## Workflow

When a user requests subtitle conversion:

1. Confirm the input subtitle file path exists
2. Determine the format (auto-detect or ask user to override)
3. Determine language (auto-detect or ask user to override)
4. Run the script with appropriate flags if needed
5. Display a preview of the converted text
6. Confirm the output file location

## Examples

### Example 1: SRT (English)

**Input SRT:**

```
1
00:00:00,000 --> 00:00:02,500
Hello and welcome to this tutorial.

2
00:00:02,500 --> 00:00:05,000
Today we're going to learn

3
00:00:05,000 --> 00:00:07,500
about video text tracks.
```

**Output Text:**

```
Hello and welcome to this tutorial.

Today we're going to learn about video text tracks.
```

### Example 2: VTT (Traditional Chinese)

Use `--lang zh_tw` or allow auto-detection.

## Using from Python

The script can also be imported as a module:

```python
from scripts.subtitle_to_text import convert_subtitles_to_text

# Auto-detect format & language
text = convert_subtitles_to_text('input.srt', 'output.txt')

# Specify language or format
text = convert_subtitles_to_text('input.vtt', 'output.txt', lang='zh_tw', fmt='vtt')

# Backwards-compatible alias
from scripts.subtitle_to_text import convert_vtt_to_text
text = convert_vtt_to_text('input.vtt', 'output.txt')
```

## Troubleshooting

**Wrong format detected**: Use `--format srt` or `--format vtt` to override:

```bash
python scripts/subtitle_to_text.py input.srt --format srt
```

**Wrong language detected**: Use `--lang` to override:

```bash
python scripts/subtitle_to_text.py input.srt --lang zh_tw
```

**Encoding errors**: The script uses UTF-8 encoding by default. If the subtitle file uses a different encoding, convert it to UTF-8 first.

**Missing paragraphs**: The script merges based on language-specific sentence-ending punctuation. If captions lack proper punctuation they may merge into larger paragraphs.

**Mixed language content**: The script works best with single-language files. For mixed English/Chinese content consider processing separately.

## CLI Reference

```
Usage: python subtitle_to_text.py <input.vtt|input.srt> [output.txt] [--lang en|zh_tw|zh_cn] [--format auto|vtt|srt]

Language options:
  --lang auto    Auto-detect language (default)
  --lang en      English
  --lang zh_tw   Traditional Chinese (\u7e41\u9ad4\u4e2d\u6587)
  --lang zh_cn   Simplified Chinese (\u7b80\u4f53\u4e2d\u6587)

Format options:
  --format auto  Auto-detect subtitle format (default)
  --format vtt   Force VTT parsing
  --format srt   Force SRT parsing

If output path is not specified, a .txt file will be created next to input.
```
