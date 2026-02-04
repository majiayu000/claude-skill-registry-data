---
name: skill-kokoro-tts-tool
description: Local text-to-speech using Kokoro TTS
---

# When to use
- When you need to convert text to speech locally (no API keys)
- When you need to generate audio from long documents (books, articles)
- When you need seamless audiobook rendering without pop artifacts
- When you need fast offline TTS rendering (20-50x real-time)

# kokoro-tts-tool Skill

## Purpose

This skill provides access to the `kokoro-tts-tool` CLI for local text-to-speech synthesis using the Kokoro-82M model. Runs entirely on-device with ONNX runtime, optimized for Apple Silicon.

## When to Use This Skill

**Use this skill when:**
- Converting text to speech without cloud APIs
- Generating audio from markdown/text documents
- Creating audiobooks from long-form content
- Needing 60+ voices across 8 languages

**Do NOT use this skill for:**
- Cloud-based TTS services
- Real-time voice conversion
- Speech-to-text (transcription)

## CLI Tool: kokoro-tts-tool

Local text-to-speech CLI using Kokoro-82M (82 million parameters).

### Installation

```bash
# Clone and install
git clone https://github.com/dnvriend/kokoro-tts-tool.git
cd kokoro-tts-tool
uv tool install .
```

### Prerequisites

- Python 3.14+
- [uv](https://github.com/astral-sh/uv) package manager
- Apple Silicon Mac (recommended)

### Quick Start

```bash
# Initialize (downloads ~350MB models)
kokoro-tts-tool init

# Synthesize text to speakers
kokoro-tts-tool synthesize "Hello world"

# Save to file
kokoro-tts-tool synthesize "Hello" --output speech.wav

# Stream a document
kokoro-tts-tool infinite --input book.md
```

## Progressive Disclosure

<details>
<summary><strong>📖 Core Commands (Click to expand)</strong></summary>

### init - Download TTS Models

Downloads the Kokoro ONNX model (~300MB) and voice embeddings (~50MB).

**Usage:**
```bash
kokoro-tts-tool init [OPTIONS]
```

**Options:**
- `--force`, `-f`: Re-download models even if they exist

**Examples:**
```bash
# Download models (skips if already present)
kokoro-tts-tool init

# Force re-download
kokoro-tts-tool init --force
```

---

### synthesize - Convert Text to Speech

Synthesizes text using the Kokoro TTS model. Audio can be played through speakers or saved to file.

**Usage:**
```bash
kokoro-tts-tool synthesize [TEXT] [OPTIONS]
```

**Arguments:**
- `TEXT`: Text to synthesize (optional if using --stdin)

**Options:**
- `--stdin`, `-s`: Read text from stdin
- `--voice`, `-v VALUE`: Voice ID (default: af_heart)
- `--output`, `-o PATH`: Save to WAV file
- `--speed FLOAT`: Speech speed 0.5-2.0 (default: 1.0)
- `--silence INT`: Trailing silence in ms (default: 200)

**Examples:**
```bash
# Play text with default voice
kokoro-tts-tool synthesize "Hello world"

# Use different voice
kokoro-tts-tool synthesize "Hello" --voice am_adam

# Save to file
kokoro-tts-tool synthesize "Hello" --output speech.wav

# Read from stdin
echo "Hello world" | kokoro-tts-tool synthesize --stdin

# Adjust speed
kokoro-tts-tool synthesize "Hello" --speed 1.5

# Multiple options
cat article.txt | kokoro-tts-tool synthesize --stdin \
    --voice bf_emma \
    --output article.wav \
    --speed 0.9
```

**Output:**
Audio played through speakers (default) or saved as WAV file (24kHz, mono, 16-bit).

---

### infinite - Stream Long Documents

Reads markdown or plain text, splits intelligently into chunks, and streams to speakers or renders to file.

**Usage:**
```bash
kokoro-tts-tool infinite [OPTIONS]
```

**Options:**
- `--input`, `-i PATH`: Input text/markdown file
- `--stdin`, `-s`: Read text from stdin
- `--output`, `-o PATH`: Save to WAV file (fast offline mode)
- `--voice VALUE`: Voice ID (default: af_heart)
- `--speed FLOAT`: Speech speed 0.5-2.0 (default: 1.0)
- `--chunk-size INT`: Target words per chunk 50-1000 (default: 200)
- `--pause INT`: Pause between chunks in ms 0-2000 (default: 150)
- `--no-markdown`: Treat input as plain text

**Examples:**
```bash
# Stream to speakers
kokoro-tts-tool infinite --input book.md

# Render to WAV (fast, ~2-3min for 1hr audio)
kokoro-tts-tool infinite --input book.md --output audiobook.wav

# Pipe from stdin
cat chapter.md | kokoro-tts-tool infinite --stdin

# With custom voice and speed
kokoro-tts-tool infinite --input notes.md \
    --voice am_adam \
    --speed 1.2

# Render audiobook with narrator voice
kokoro-tts-tool infinite --input book.md \
    --output book.wav \
    --voice bm_george \
    --speed 0.95

# Shorter chunks for studying
kokoro-tts-tool infinite --input study.md \
    --chunk-size 200 \
    --pause 600
```

**Output:**
- Speaker mode: Real-time playback, seamless audio
- File mode: Fast offline rendering (20-50x real-time on M4)

---

### list-voices - List Available Voices

Lists voice information including ID, name, gender, accent, quality grade, and description.

**Usage:**
```bash
kokoro-tts-tool list-voices [OPTIONS]
```

**Options:**
- `--language`, `-l VALUE`: Filter by language (English, Japanese, etc.)
- `--gender`, `-g VALUE`: Filter by gender (Male, Female)
- `--json`: Output as JSON for scripting

**Examples:**
```bash
# List all voices
kokoro-tts-tool list-voices

# Filter by language
kokoro-tts-tool list-voices --language English

# Filter by gender
kokoro-tts-tool list-voices --gender Female

# Combined filters
kokoro-tts-tool list-voices --language English --gender Male

# JSON output for scripting
kokoro-tts-tool list-voices --json
```

**Voice ID Format:**
- Pattern: `[language][gender]_[name]`
- First letter: language (a=American, b=British, j=Japanese, etc.)
- Second letter: gender (f=Female, m=Male)

**Quality Grades:**
- A/A-: Highest quality (af_heart, af_bella, am_adam)
- B+/B: Good quality
- B-: Acceptable quality

---

### info - Display Configuration

Shows information about the Kokoro TTS installation.

**Usage:**
```bash
kokoro-tts-tool info
```

**Examples:**
```bash
kokoro-tts-tool info
```

**Output:**
- Model status (Ready/Not downloaded)
- Model file locations
- Default settings
- Supported languages

---

### completion - Shell Completion

Generate shell completion scripts for bash, zsh, or fish.

**Usage:**
```bash
kokoro-tts-tool completion SHELL
```

**Arguments:**
- `SHELL`: Shell type (bash, zsh, fish)

**Examples:**
```bash
# Bash (add to ~/.bashrc)
eval "$(kokoro-tts-tool completion bash)"

# Zsh (add to ~/.zshrc)
eval "$(kokoro-tts-tool completion zsh)"

# Fish
kokoro-tts-tool completion fish > ~/.config/fish/completions/kokoro-tts-tool.fish
```

</details>

<details>
<summary><strong>⚙️ Advanced Features (Click to expand)</strong></summary>

### Multi-Level Verbosity Logging

Control logging detail with progressive verbosity levels. All logs output to stderr.

**Logging Levels:**

| Flag | Level | Output | Use Case |
|------|-------|--------|----------|
| (none) | WARNING | Errors and warnings only | Production, quiet mode |
| `-v` | INFO | + High-level operations | Normal debugging |
| `-vv` | DEBUG | + Detailed info, full tracebacks | Development |
| `-vvv` | TRACE | + Library internals | Deep debugging |

**Examples:**
```bash
# INFO level
kokoro-tts-tool -v synthesize "Hello"

# DEBUG level
kokoro-tts-tool -vv infinite --input book.md

# TRACE level
kokoro-tts-tool -vvv synthesize "Hello"
```

---

### Pipeline Composition

Compose commands with Unix pipes for workflows.

**Examples:**
```bash
# Get voice IDs as JSON and filter
kokoro-tts-tool list-voices --json | jq '.[].id'

# Read from another command
cat document.md | kokoro-tts-tool infinite --stdin

# Chain with file processing
find . -name "*.md" -exec cat {} \; | kokoro-tts-tool infinite --stdin
```

</details>

<details>
<summary><strong>🔧 Troubleshooting (Click to expand)</strong></summary>

### Common Issues

**Issue: Command not found**
```bash
# Verify installation
kokoro-tts-tool --version

# Reinstall if needed
cd kokoro-tts-tool
uv tool install . --reinstall
```

**Issue: Models not downloaded**
```bash
# Initialize models
kokoro-tts-tool init

# Force re-download
kokoro-tts-tool init --force
```

**Issue: Audio not playing**
- Check system volume
- Try saving to file: `--output test.wav`
- Check with verbose: `-vv`

**Issue: Voice not found**
```bash
# List available voices
kokoro-tts-tool list-voices

# Check voice ID format
kokoro-tts-tool list-voices --json | jq '.[].id'
```

### Getting Help

```bash
# General help
kokoro-tts-tool --help

# Command-specific help
kokoro-tts-tool synthesize --help
kokoro-tts-tool infinite --help
```

</details>

## Exit Codes

- `0`: Success
- `1`: Error (validation, runtime, or unexpected)

## Output Formats

**Default Output:**
- Human-readable formatted output
- Audio played through speakers

**File Output (`--output`):**
- WAV format (24kHz, mono, 16-bit)

**JSON Output (`--json` on list-voices):**
- Machine-readable voice data
- Perfect for pipelines and processing

## Best Practices

1. **Initialize first**: Run `kokoro-tts-tool init` before synthesis
2. **Use appropriate voices**: Match voice to content (am_adam for audiobooks, bf_emma for education)
3. **Leverage infinite for documents**: Better than synthesize for long content
4. **Use file output for production**: `--output` for consistent results
5. **Check voice quality grades**: A/A- voices recommended for production

## Resources

- **GitHub**: https://github.com/dnvriend/kokoro-tts-tool
- **Kokoro-82M Model**: https://huggingface.co/hexgrad/Kokoro-82M
- **kokoro-onnx**: https://github.com/thewh1teagle/kokoro-onnx
