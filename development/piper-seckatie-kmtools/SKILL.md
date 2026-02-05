---
name: piper
description: Convert text to speech using Piper, a fast, local, neural text-to-speech system with natural sounding voices. This skill is triggered when the user says things like "convert text to speech", "text to audio", "read this aloud", "create audio from text", "generate speech from text", "make an audio file from this text", or "use piper TTS".
---

# Piper Text-to-Speech Skill

This skill enables you to use Piper TTS to convert text files or text input into natural-sounding speech audio files.

## Installation

Piper has been installed via uv with Python 3.13:
```bash
uv tool install --python 3.13 piper-tts
```

The piper executable is located at: `/Users/katiemulliken/.local/bin/piper`

## Voice Models

Voice models are stored in `~/piper-voices/`.

Currently installed voices:
- **en_US-amy-medium**: Natural-sounding US English female voice

### Downloading Additional Voices

To download more voices from Hugging Face:

```bash
# List available voices at: https://huggingface.co/rhasspy/piper-voices
# Preview samples at: https://rhasspy.github.io/piper-samples/

# Download a voice (example: en_US-lessac-medium)
cd ~/piper-voices
curl -L "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx" -o en_US-lessac-medium.onnx
curl -L "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json" -o en_US-lessac-medium.onnx.json
```

## Basic Usage

**IMPORTANT: When working with Obsidian markdown files (.md), ALWAYS use the `clean_obsidian_for_tts.py` script first to remove formatting, frontmatter, and other non-speech content before converting to audio. See the "Cleaning Obsidian Files for TTS" section below.**

### Convert text to audio file

```bash
# From text input
echo "Hello, this is a test." | piper -m ~/piper-voices/en_US-amy-medium.onnx -f output.wav

# From a text file
piper -m ~/piper-voices/en_US-amy-medium.onnx -f output.wav < input.txt

# Using --input-file flag
piper -m ~/piper-voices/en_US-amy-medium.onnx -i input.txt -f output.wav
```

### Play audio immediately (requires ffplay)

```bash
echo "This will play on your speakers." | piper -m ~/piper-voices/en_US-amy-medium.onnx | ffplay -
```

## Advanced Options

### Speed Control
```bash
# Default speed (1.5x faster - length-scale 0.67)
piper -m ~/piper-voices/en_US-amy-medium.onnx --length-scale 0.67 -f output.wav < input.txt

# Normal speech (1.0 is normal)
piper -m ~/piper-voices/en_US-amy-medium.onnx --length-scale 1.0 -f output.wav < input.txt

# Slower speech
piper -m ~/piper-voices/en_US-amy-medium.onnx --length-scale 1.2 -f output.wav < input.txt
```

### Volume Control
```bash
piper -m ~/piper-voices/en_US-amy-medium.onnx --volume 1.5 -f output.wav < input.txt
```

### Sentence Pauses
```bash
# Add 0.5 seconds of silence between sentences
piper -m ~/piper-voices/en_US-amy-medium.onnx --sentence-silence 0.5 -f output.wav < input.txt
```

### GPU Acceleration
```bash
piper -m ~/piper-voices/en_US-amy-medium.onnx --cuda -f output.wav < input.txt
```

## Cleaning Obsidian Files for TTS

A Python script is included to clean Obsidian markdown files for optimal text-to-speech conversion.

**Script location**: This skill includes `clean_obsidian_for_tts.py` in the same directory as this documentation.

### What it removes:
- YAML frontmatter
- Markdown formatting (headers, bold, italic, strikethrough)
- Links and URLs (keeps link text)
- Obsidian wiki links `[[link]]`
- Images (but preserves alt-text)
- Code blocks
- HTML tags
- Emojis and special Unicode characters
- List markers
- Excessive whitespace

### Enhanced Workflow: Including Image Transcriptions

For articles with images, you can create a richer audio experience by transcribing image content:

1. **Download and examine images** from the article using curl or web tools
2. **Transcribe image content** into a cleaned text file, replacing image references with detailed descriptions
3. **Insert transcriptions** at the image locations in your cleaned file
4. **Convert to audio** with piper

This ensures images are properly represented in the audio narration, making the content accessible even without visual context.

### Usage:

```bash
# Clean a file and save to a new file
python3 clean_obsidian_for_tts.py input.md -o output.txt

# Clean and show statistics
python3 clean_obsidian_for_tts.py input.md -o output.txt --stats

# Clean to stdout (for piping)
python3 clean_obsidian_for_tts.py input.md

# Clean from stdin
cat input.md | python3 clean_obsidian_for_tts.py > output.txt
```

### Complete workflow for Obsidian to audio (with default 1.5x speed):

```bash
# Step 1: Clean the markdown file
python3 clean_obsidian_for_tts.py "My Note.md" -o "My Note - Clean.txt" --stats

# Step 2: Convert to audio with piper
piper -m ~/piper-voices/en_US-amy-medium.onnx \
  -i "My Note - Clean.txt" \
  -f "My Note.wav" \
  --sentence-silence 0.3 \
  --length-scale 0.67

# Or combine in one line:
python3 clean_obsidian_for_tts.py "My Note.md" | \
  piper -m ~/piper-voices/en_US-amy-medium.onnx \
  -f "My Note.wav" \
  --sentence-silence 0.3 \
  --length-scale 0.67
```

## Common Command Patterns

### Convert a markdown file to audio
```bash
# For Obsidian/markdown files, ALWAYS clean first with the script:
python3 clean_obsidian_for_tts.py document.md | \
  piper -m ~/piper-voices/en_US-amy-medium.onnx \
  -f document.wav \
  --sentence-silence 0.3 \
  --length-scale 0.67

# Or save the cleaned version first:
python3 clean_obsidian_for_tts.py document.md -o document-clean.txt
piper -m ~/piper-voices/en_US-amy-medium.onnx -i document-clean.txt -f document.wav
```

### Batch process multiple files
```bash
for file in *.txt; do
  piper -m ~/piper-voices/en_US-amy-medium.onnx -i "$file" -f "${file%.txt}.wav"
done
```

### Batch convert Obsidian notes to audio
```bash
for file in *.md; do
  python3 clean_obsidian_for_tts.py "$file" | \
    piper -m ~/piper-voices/en_US-amy-medium.onnx \
    -f "${file%.md}.wav" \
    --sentence-silence 0.3 \
    --length-scale 0.67
done
```

### Convert articles with image transcriptions to audio

For articles containing images (like screenshots, diagrams, or referenced images):

```bash
# Step 1: Download images from the article
mkdir -p /tmp/article_images
cd /tmp/article_images
curl -L "https://example.com/image1.png" -o image1.png
curl -L "https://example.com/image2.png" -o image2.png

# Step 2: View images and manually transcribe their content
# (Use your image viewer or convert images to text using OCR tools if available)

# Step 3: Create an enhanced cleaned text file
# Start with the cleaned markdown, then replace image references with detailed transcriptions
python3 clean_obsidian_for_tts.py "article.md" > cleaned_base.txt

# Edit cleaned_base.txt to insert transcriptions like:
# Image 1: [Detailed description of what appears in image1.png]
# Image 2: [Detailed description of what appears in image2.png]

# Step 4: Convert the enhanced cleaned file to audio
piper -m ~/piper-voices/en_US-amy-medium.onnx \
  -i cleaned_with_transcriptions.txt \
  -f "article_with_images.wav" \
  --sentence-silence 0.3 \
  --length-scale 0.67
```

**Example transcription format:**

Original markdown:
```
![Screenshot of error message](https://example.com/error.png)
```

In cleaned text:
```
Image 1: Screenshot of error message

This image shows a red error dialog box with the message "File not found error 404". The dialog contains an OK button in the bottom right. The background appears to be a Windows desktop environment.
```

This approach ensures all visual content is represented in the audio version, making your content fully accessible to audio listeners.

### Output to a specific directory
```bash
piper -m ~/piper-voices/en_US-amy-medium.onnx -i input.txt -d ~/audio-outputs -f output.wav
```

## Available Options

- `-m, --model`: Path to ONNX model file (required)
- `-c, --config`: Path to model config file (optional, auto-detected from .onnx.json)
- `-i, --input-file`: Path to input text file
- `-f, --output-file`: Path to output WAV file (default: stdout)
- `-d, --output-dir`: Directory for output files (default: current directory)
- `--output-raw`: Stream raw audio to stdout instead of WAV
- `-s, --speaker`: Speaker ID for multi-speaker models (default: 0)
- `--length-scale`: Speech speed multiplier (default: 1.0)
- `--noise-scale`: Generator noise level
- `--noise-w-scale`: Phoneme width noise level
- `--cuda`: Enable GPU acceleration
- `--sentence-silence`: Seconds of silence between sentences (default: 0.0)
- `--volume`: Volume multiplier (default: 1.0)
- `--no-normalize`: Disable automatic volume normalization
- `--data-dir`: Directory to search for voice models
- `--debug`: Enable debug output

## Tips

1. **Large files**: For very large text files, consider splitting them into smaller chunks to avoid memory issues
2. **Quality vs Speed**: Medium quality voices offer a good balance; high quality voices are slower but more natural
3. **Preprocessing**: Remove special characters or formatting that might not be pronounced well
4. **Performance**: The CLI loads the model each time; for repeated use, consider the HTTP API server mode

## Troubleshooting

### Command not found
Make sure `/Users/katiemulliken/.local/bin` is in your PATH:
```bash
export PATH="/Users/katiemulliken/.local/bin:$PATH"
```

Or use the full path:
```bash
/Users/katiemulliken/.local/bin/piper [options]
```

### Model file errors
Ensure both the `.onnx` model file and `.onnx.json` config file are in the same directory with matching names.

## Resources

- Voice samples: https://rhasspy.github.io/piper-samples/
- Voice models: https://huggingface.co/rhasspy/piper-voices
- Documentation: https://github.com/OHF-Voice/piper1-gpl
- CLI docs: https://github.com/OHF-Voice/piper1-gpl/blob/main/docs/CLI.md
