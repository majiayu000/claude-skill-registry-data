---
name: gem
description: Multimodal AI processing using Google Gemini. Use for analyzing PDFs, images, videos, YouTube links, and other large documents. Ideal when you need to extract information from files that require vision or multimodal understanding.
---

# Gemini Multimodal Tool

Use the `ai-gem` CLI tool for multimodal AI processing via Google's Gemini API.

## Usage

```bash
# Text queries
ai-gem "Write a haiku about Python programming"

# Analyze documents
ai-gem "Summarize this document" document.pdf

# Analyze images
ai-gem "What's in this image?" photo.jpg

# Process YouTube videos
ai-gem "Create a 5-point summary" "https://youtu.be/VIDEO_ID"

# Compare multiple files
ai-gem "Compare these files" file1.pdf file2.png

# Web search
ai-gem "Current AI news" --search
```

## Requirements

- `GEMINI_API_KEY` environment variable must be set
- The `hamel` package must be installed: `pip install hamel`

## Supported Input Types

- PDFs
- Images (PNG, JPEG, GIF, WebP)
- Videos (MP4, etc.)
- YouTube URLs
- Plain text files
- Multiple files for comparison
