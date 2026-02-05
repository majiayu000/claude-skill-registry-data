---
name: osay
description: AI-powered text-to-speech CLI tool. Use for pronunciation queries, reading text aloud, generating audio files, or language practice. Triggers on "how to pronounce", "say this", "read aloud", "TTS", "text to speech", "speak", or audio generation requests.
---

# osay - AI Text-to-Speech

A CLI tool for AI-powered speech synthesis. Convert text to natural-sounding speech for various use cases.

## Quick Reference

```bash
# Show all available options
osay --help

# Basic usage - speak text
osay "Hello, world!"

# Check pronunciation of unfamiliar words
osay "ephemeral"
osay "Nietzsche"
osay "queue"

# With specific voice
osay -v coral "Welcome to the presentation."

# Save as audio file
osay -o output.mp3 "This will be saved to a file."

# Replay last audio
osay -p
```

## Use Cases

### 1. Pronunciation Queries

Quickly hear correct pronunciation of unfamiliar words:

```bash
# English words
osay "pronunciation"
osay "worcestershire"

# Names and proper nouns
osay "Dostoevsky"
osay "Nguyen"

# Technical terms
osay "asynchronous"
osay "kubernetes"
```

### 2. Content Reading

Read articles, documentation, or text content aloud:

```bash
# Read a paragraph
osay "The quick brown fox jumps over the lazy dog."

# With neutral tone (no default cheerfulness)
osay --no-instructions "This is a factual news report."

# Slow and clear for comprehension
osay --instructions "Speak slowly and clearly" "Complex technical content here."
```

### 3. Audio Generation

Create audio files for various purposes:

```bash
# Podcast intro
osay -v onyx -o intro.mp3 "Welcome to the show."

# Notification sounds
osay -o alert.mp3 "Task completed successfully."

# Voice memo
osay -o memo.mp3 "Remember to review the pull request tomorrow."
```

### 4. Language Learning

Practice pronunciation and listening comprehension:

```bash
# Practice sentences
osay -v coral "I'd like a cup of coffee, please."

# Slow speed for beginners
osay --instructions "Speak slowly, pausing between phrases" \
  "Could you repeat that more slowly?"

# Natural native speed
osay --instructions "Speak at natural native speed" \
  "I'm gonna grab a coffee real quick."
```

See [examples/english/SENTENCES.md](examples/english/SENTENCES.md) for practice sentence collections.

## Voices

List available voices with `osay -v '?'`

| Voice   | Characteristics                    |
|---------|-----------------------------------|
| alloy   | Neutral, balanced                 |
| ash     | Soft, gentle                      |
| ballad  | Melodic, smooth                   |
| coral   | Warm, conversational              |
| echo    | Resonant, clear                   |
| fable   | Storytelling, narrative           |
| nova    | Clear, standard                   |
| onyx    | Deeper, formal                    |
| sage    | Calm, wise                        |
| shimmer | Expressive, emotional             |

## Speech Instructions

Control tone and delivery style:

```bash
# Natural conversation
osay --instructions "Speak naturally, like talking to a friend" "Hey, what's up?"

# Professional presentation
osay --instructions "Speak clearly and professionally" "Q4 results exceeded expectations."

# Emphatic
osay --instructions "Speak with enthusiasm" "This is amazing news!"

# Neutral (disable default tone)
osay --no-instructions "Objective statement."
```

## Cache Management

Audio files are cached automatically in `~/.osay/audios/`:

```bash
# List cached audio with metadata
osay --list-cached

# Replay most recent
osay -p
osay --prev

# Select from cache interactively (with fzf)
osay --play-cached

# Play specific cached audio by ID
osay --play-cached abc123
```

## Output Formats

Use `--format` to specify audio format:

| Format | Use Case                          |
|--------|-----------------------------------|
| mp3    | Default, general purpose          |
| opus   | Efficient storage, streaming      |
| aac    | Apple ecosystem, good compression |
| flac   | Lossless, archival quality        |
| wav    | Lossless, editing                 |
| pcm    | Raw audio, processing             |

```bash
osay -o output.mp3 "Default format"
osay -o speech.wav --format wav "High quality audio"
osay -o compressed.opus --format opus "Small file size"
```

## Input Methods

Multiple ways to provide text:

```bash
# Direct text argument
osay "Hello, world!"

# Read from file
osay -f mytext.txt
osay -f document.txt -v nova

# Pipe from stdin
echo "Hello from a pipe" | osay
cat article.txt | osay -v coral

# Combine with other commands
curl -s https://example.com/quote.txt | osay
```

## Streaming Mode

Use `--no-cache` for lowest latency (live streaming, no cache):

```bash
# Quick response without caching
osay --no-cache "Instant playback!"

# Useful for real-time applications
osay --no-cache -v coral "This plays immediately"
```

## Batch Processing

Process multiple texts:

```bash
# From file (one per line)
while IFS= read -r line; do
  osay "$line"
  sleep 0.5
done < texts.txt

# Generate multiple files
osay -o file1.mp3 "First message"
osay -o file2.mp3 "Second message"
```

## Configuration

### API Key Management

```bash
# Setup OpenAI API key interactively
osay --setup

# Check if key is configured
osay --show-key

# Remove stored key
osay --remove-key
```

### Environment

- **Config file**: `~/.config/osay/config`
- **Audio cache**: `~/.osay/audios/`
- **Environment variable**: `OPENAI_API_KEY` (overrides config file)

Falls back to macOS `say` command if no OpenAI key is available.
