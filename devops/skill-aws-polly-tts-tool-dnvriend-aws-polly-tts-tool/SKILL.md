---
name: skill-aws-polly-tts-tool
description: AWS Polly TTS CLI for text-to-speech synthesis
---

# When to use
- Converting text to lifelike speech using AWS Polly
- Working with multiple voice engines and output formats
- Tracking TTS costs and AWS billing
- Implementing TTS in automation pipelines

# AWS Polly TTS Tool Skill

## Purpose

Professional AWS Polly text-to-speech CLI and library with agent-friendly design, enabling conversion of text to lifelike speech using Amazon Polly's deep learning technology. Supports 60+ voices in 30+ languages across four quality tiers with comprehensive cost tracking.

## When to Use This Skill

**Use this skill when:**
- You need to convert text to speech using AWS Polly
- You want to explore available voices and engines
- You need to track TTS costs or query billing data
- You're building automation with TTS capabilities
- You need SSML support for advanced speech control
- You want to work with different audio formats

**Do NOT use this skill for:**
- Non-AWS TTS services (Google, Azure, etc.)
- Real-time streaming TTS (use AWS SDK directly)
- Voice cloning or training (Polly doesn't support this)

## CLI Tool: aws-polly-tts-tool

Professional AWS Polly TTS CLI and Python library designed with CLI-first philosophy for both command-line and programmatic use.

### Installation

```bash
# Clone repository
git clone https://github.com/dnvriend/aws-polly-tts-tool.git
cd aws-polly-tts-tool

# Install with uv (Python 3.12)
uv tool install . --python 3.12

# Verify installation
aws-polly-tts-tool --version
```

### Prerequisites

- **Python 3.12+** (Python 3.13+ has pydub compatibility issues)
- AWS credentials configured
- **ffmpeg** for audio playback (not required for file output)
- IAM permissions: `polly:DescribeVoices`, `polly:SynthesizeSpeech`, `ce:GetCostAndUsage`

### Quick Start

```bash
# Play text with default voice
aws-polly-tts-tool synthesize "Hello world"

# Save to file
aws-polly-tts-tool synthesize "Hello world" --output speech.mp3

# List available voices
aws-polly-tts-tool list-voices

# Show pricing
aws-polly-tts-tool pricing
```

## Progressive Disclosure

<details>
<summary><strong>📖 Core Commands (Click to expand)</strong></summary>

### synthesize - Convert Text to Speech

Main TTS command with full feature support including multiple engines, voices, and output formats.

**Usage:**
```bash
aws-polly-tts-tool synthesize "TEXT" [OPTIONS]
```

**Arguments:**
- `TEXT`: Text to synthesize (required, or use `--stdin`)
- `--stdin` / `-s`: Read text from stdin (enables piping)
- `--voice TEXT`: Voice ID (default: Joanna)
- `--output PATH` / `-o PATH`: Save audio to file instead of playing
- `--format TEXT` / `-f TEXT`: Output format (mp3, ogg_vorbis, pcm) - default: mp3
- `--engine TEXT` / `-e TEXT`: Voice engine (standard, neural, generative, long-form) - default: neural
- `--ssml`: Treat input as SSML markup
- `--show-cost`: Display character count and cost estimate
- `--region TEXT` / `-r TEXT`: AWS region override
- `-V/-VV/-VVV`: Verbosity (INFO/DEBUG/TRACE with AWS SDK details)

**Examples:**
```bash
# Basic synthesis with default voice (Joanna, neural)
aws-polly-tts-tool synthesize "Hello world"

# Use different voice and engine
aws-polly-tts-tool synthesize "Hello" --voice Matthew --engine generative

# Save to file with specific format
aws-polly-tts-tool synthesize "Hello world" --output speech.mp3 --format mp3

# Read from stdin
echo "Hello world" | aws-polly-tts-tool synthesize --stdin

# Read from file
cat article.txt | aws-polly-tts-tool synthesize --stdin --output article.mp3

# Use SSML for advanced control
aws-polly-tts-tool synthesize '<speak>Hello <break time="500ms"/> world</speak>' --ssml

# Show cost estimate
aws-polly-tts-tool synthesize "Hello world" --show-cost

# Multiple options combined with debugging
cat article.txt | aws-polly-tts-tool synthesize --stdin \
    --voice Joanna \
    --engine neural \
    --output article.mp3 \
    --show-cost \
    -VV
```

**Output:**
- Audio played through speakers (default) or saved to file
- Character count and cost estimate (with `--show-cost`)
- Logs to stderr, keeping stdout clean for piping

---

### list-voices - Discover Available Voices

List and filter AWS Polly voices by engine, language, and gender.

**Usage:**
```bash
aws-polly-tts-tool list-voices [OPTIONS]
```

**Options:**
- `--engine TEXT` / `-e TEXT`: Filter by engine (standard, neural, generative, long-form)
- `--language TEXT` / `-l TEXT`: Filter by language code (e.g., en-US, es-ES, fr-FR)
- `--gender TEXT` / `-g TEXT`: Filter by gender (Female, Male)
- `--region TEXT` / `-r TEXT`: AWS region override
- `-V/-VV/-VVV`: Verbosity levels

**Examples:**
```bash
# List all voices
aws-polly-tts-tool list-voices

# Filter by engine
aws-polly-tts-tool list-voices --engine neural

# Filter by language
aws-polly-tts-tool list-voices --language en-US

# Combine filters
aws-polly-tts-tool list-voices --engine neural --language en --gender Female

# Use with grep for searching
aws-polly-tts-tool list-voices | grep British
aws-polly-tts-tool list-voices --engine generative | grep Spanish
```

**Output:**
Table with Voice, Gender, Language, Engines (supported), and Description columns. Dynamically fetched from Polly API (always up-to-date).

---

### list-engines - Display Voice Engines

Show all available voice engines with technology, pricing, and best use cases.

**Usage:**
```bash
aws-polly-tts-tool list-engines
```

**Examples:**
```bash
# Show all engines with details
aws-polly-tts-tool list-engines
```

**Output:**
Table showing:
- **Standard** ($4/1M chars) - Traditional concatenative TTS, 3000 char limit
- **Neural** ($16/1M chars) - Natural human-like voices, 3000 char limit
- **Generative** ($30/1M chars) - Most advanced emotionally engaged, 3000 char limit
- **Long-form** ($100/1M chars) - Optimized for audiobooks, 100,000 char limit

---

### billing - Query AWS Costs

Query AWS Cost Explorer for actual Polly usage costs with engine breakdown.

**Usage:**
```bash
aws-polly-tts-tool billing [OPTIONS]
```

**Options:**
- `--days INT` / `-d INT`: Number of days to query (default: 30)
- `--start-date TEXT`: Custom start date (YYYY-MM-DD)
- `--end-date TEXT`: Custom end date (YYYY-MM-DD)
- `--region TEXT` / `-r TEXT`: AWS region for Cost Explorer
- `-V/-VV/-VVV`: Verbosity levels

**Examples:**
```bash
# Last 30 days of Polly costs
aws-polly-tts-tool billing

# Last 7 days
aws-polly-tts-tool billing --days 7

# Custom date range
aws-polly-tts-tool billing --start-date 2025-01-01 --end-date 2025-01-31

# With verbose output
aws-polly-tts-tool billing --days 7 -V
```

**Output:**
Total cost and breakdown by engine (Standard, Neural, Generative, Long-form) in USD.

**Note:** Requires IAM permission `ce:GetCostAndUsage`

---

### pricing - Show Pricing Information

Display static pricing information for all Polly engines with cost examples.

**Usage:**
```bash
aws-polly-tts-tool pricing
```

**Examples:**
```bash
# Show pricing table and examples
aws-polly-tts-tool pricing
```

**Output:**
Comprehensive pricing with:
- Cost per 1M characters for each engine
- Technology type and quality level
- Character limits per request
- Concurrent request limits
- Free tier information
- Best use cases
- Cost examples (1,000 words, audiobooks)

---

### info - Tool Configuration

Display AWS credentials status and tool configuration.

**Usage:**
```bash
aws-polly-tts-tool info
```

**Examples:**
```bash
# Verify AWS authentication and show config
aws-polly-tts-tool info
```

**Output:**
- AWS credential status (Valid/Invalid)
- Account ID, User ID, ARN
- Available engines
- Output formats
- Useful command examples

---

### completion - Shell Completion

Generate shell completion scripts for bash, zsh, or fish.

**Usage:**
```bash
aws-polly-tts-tool completion [bash|zsh|fish]
```

**Arguments:**
- `SHELL`: Shell type (bash, zsh, or fish) - required

**Examples:**
```bash
# Generate bash completion
aws-polly-tts-tool completion bash

# Install for bash (add to ~/.bashrc)
eval "$(aws-polly-tts-tool completion bash)"

# Install for zsh (add to ~/.zshrc)
eval "$(aws-polly-tts-tool completion zsh)"

# Install for fish
aws-polly-tts-tool completion fish > ~/.config/fish/completions/aws-polly-tts-tool.fish

# File-based installation (recommended)
aws-polly-tts-tool completion bash > ~/.aws-polly-tts-tool-complete.bash
echo 'source ~/.aws-polly-tts-tool-complete.bash' >> ~/.bashrc
```

**Output:**
Shell-specific completion script. After installation, restart shell or source config file.

</details>

<details>
<summary><strong>⚙️ Advanced Features (Click to expand)</strong></summary>

### SSML Support

Full SSML (Speech Synthesis Markup Language) support for advanced speech control.

**Features:**
- **Prosody**: Control rate, pitch, volume
- **Breaks**: Add pauses of specific duration
- **Emphasis**: Add emphasis to words
- **Speaking styles**: Newscaster, conversational (select voices)
- **Phonemes**: Control pronunciation

**Examples:**
```bash
# Basic pause
aws-polly-tts-tool synthesize '<speak>Hello <break time="500ms"/> world</speak>' --ssml

# Prosody control (speed, pitch, volume)
aws-polly-tts-tool synthesize '<speak><prosody rate="slow" pitch="low">Deep voice</prosody></speak>' --ssml

# Emphasis
aws-polly-tts-tool synthesize '<speak>I <emphasis level="strong">really</emphasis> like this</speak>' --ssml

# Newscaster style (Matthew, Joanna only)
aws-polly-tts-tool synthesize '<speak><amazon:domain name="news">Breaking news today</amazon:domain></speak>' --ssml --voice Matthew

# Multiple prosody attributes
aws-polly-tts-tool synthesize '<speak><prosody rate="fast" pitch="high" volume="loud">Excited announcement!</prosody></speak>' --ssml
```

**SSML Resources:**
- [AWS Polly SSML Reference](https://docs.aws.amazon.com/polly/latest/dg/supportedtags.html)

---

### Multi-Level Verbosity

Progressive logging detail for debugging without code changes.

**Levels:**
- **Default**: Errors and warnings only (clean output)
- **`-V`** (INFO): High-level operations (voice selection, file operations)
- **`-VV`** (DEBUG): Detailed steps (validation, API calls, character counts)
- **`-VVV`** (TRACE): Full AWS SDK internals (credentials, HTTP requests, boto3 events)

**Examples:**
```bash
# Default: No verbose output
aws-polly-tts-tool synthesize "Hello world" --output test.mp3

# INFO level (-V)
aws-polly-tts-tool synthesize "Hello world" -V --output test.mp3
# [INFO] Using voice: Joanna (neural engine)
# [INFO] Synthesizing audio to file: test.mp3

# DEBUG level (-VV)
aws-polly-tts-tool synthesize "Hello world" -VV --output test.mp3
# [DEBUG] Validating engine: neural
# [DEBUG] Validating output format: mp3
# [DEBUG] Initializing AWS Polly client
# [INFO] Using voice: Joanna (neural engine)
# [DEBUG] Synthesized 11 characters

# TRACE level (-VVV) - Full AWS SDK details
aws-polly-tts-tool synthesize "Hello world" -VVV --output test.mp3
# [DEBUG] Looking for credentials via: env
# [INFO] Found credentials in shared credentials file: ~/.aws/credentials
# [DEBUG] Starting new HTTPS connection (1): polly.eu-central-1.amazonaws.com:443
# [DEBUG] https://polly.eu-central-1.amazonaws.com:443 "POST /v1/speech HTTP/1.1" 200
```

**Note:** All logs go to stderr, keeping stdout clean for data/piping.

---

### Library Usage

Import and use as a Python library for programmatic access.

**Basic Usage:**
```python
from aws_polly_tts_tool import (
    get_polly_client,
    synthesize_audio,
    save_speech,
    VoiceManager,
    calculate_cost,
)

# Initialize client
client = get_polly_client(region="us-east-1")

# Synthesize audio
audio_bytes, char_count = synthesize_audio(
    client=client,
    text="Hello world",
    voice_id="Joanna",
    output_format="mp3",
    engine="neural"
)

# Save to file
save_speech(
    client=client,
    text="Hello world",
    voice_id="Joanna",
    output_path=Path("output.mp3"),
    engine="neural"
)

# List voices
voice_manager = VoiceManager(client)
voices = voice_manager.list_voices(engine="neural", language="en")

# Calculate cost
cost = calculate_cost(character_count=5000, engine="neural")
print(f"Estimated cost: ${cost:.4f}")
```

**Public API:**
- `get_polly_client(region=None)` - Initialize boto3 Polly client
- `synthesize_audio(client, text, voice_id, output_format, engine, text_type)` - Synthesize audio
- `save_speech(client, text, voice_id, output_path, ...)` - Save to file
- `play_speech(client, text, voice_id, ...)` - Play through speakers
- `VoiceManager(client)` - Voice discovery and management
- `calculate_cost(char_count, engine)` - Cost estimation

---

### Voice Engine Selection Guide

**Standard Engine** ($4/1M chars)
- **Technology**: Traditional concatenative TTS
- **Quality**: Basic synthetic sound
- **Limit**: 3,000 chars/request
- **Best for**: Cost-sensitive applications, basic announcements
- **Free tier**: 5M chars/month (12 months)

**Neural Engine** ($16/1M chars)
- **Technology**: Deep learning neural networks
- **Quality**: Natural, human-like voices
- **Limit**: 3,000 chars/request
- **Best for**: General-purpose TTS, recommended for most use cases
- **Free tier**: 1M chars/month (12 months)

**Generative Engine** ($30/1M chars)
- **Technology**: Advanced generative AI
- **Quality**: Most lifelike, emotionally engaged
- **Limit**: 3,000 chars/request
- **Best for**: High-quality content, brand voices, engaging experiences
- **Free tier**: None

**Long-form Engine** ($100/1M chars)
- **Technology**: Neural with long-context optimization
- **Quality**: Consistent over long passages
- **Limit**: 100,000 chars/request
- **Best for**: Audiobooks, long articles, consistent narration
- **Free tier**: None

**Decision Matrix:**
- Budget-conscious → Standard
- General use → Neural (recommended)
- Premium quality → Generative
- Audiobooks/articles → Long-form

---

### Cost Tracking Strategies

**Immediate Estimates:**
```bash
# Use --show-cost for instant character count and cost
aws-polly-tts-tool synthesize "Text" --show-cost
```

**Actual Billing:**
```bash
# Query real AWS costs with Cost Explorer
aws-polly-tts-tool billing --days 30
```

**Cost Optimization Tips:**
1. Use Standard engine for non-critical audio
2. Cache synthesized audio files to avoid re-synthesis
3. Batch process text for efficiency
4. Use Long-form engine only for actual long content
5. Monitor with `billing` command regularly

**Cost Examples:**
- 1,000 words (~5,000 chars):
  - Standard: $0.02
  - Neural: $0.08
  - Generative: $0.15
  - Long-form: $0.50
- 50,000 word audiobook:
  - Standard: $1.00
  - Neural: $4.00
  - Generative: $7.50
  - Long-form: $25.00

</details>

<details>
<summary><strong>🔧 Troubleshooting (Click to expand)</strong></summary>

### Common Issues

**Issue: No AWS credentials found**
```bash
# Symptom
Error: Unable to locate credentials
```

**Solution:**
```bash
# Configure AWS credentials
aws configure

# Or set environment variables
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="us-east-1"

# Verify with
aws-polly-tts-tool info
```

---

**Issue: Audio playback fails on Python 3.13+**
```bash
# Symptom
Error: No module named 'audioop'
```

**Solution:**
Option 1: Use Python 3.12 (recommended)
```bash
mise use python@3.12
uv tool install . --python 3.12
```

Option 2: Save to file instead (works on all Python versions)
```bash
aws-polly-tts-tool synthesize "Hello" --output speech.mp3
```

---

**Issue: Voice not found**
```bash
# Symptom
Error: Voice 'invalid' not found
```

**Solution:**
```bash
# List available voices
aws-polly-tts-tool list-voices

# Filter by engine
aws-polly-tts-tool list-voices --engine neural

# Case-sensitive voice names
aws-polly-tts-tool synthesize "Hello" --voice Joanna  # Correct
```

---

**Issue: Engine not supported by voice**
```bash
# Symptom
Error: Voice doesn't support this engine
```

**Solution:**
```bash
# Check which engines a voice supports
aws-polly-tts-tool list-voices | grep "VoiceName"

# Not all voices support all engines
# Example: Standard voices don't support neural engine
```

---

**Issue: Cost Explorer access denied**
```bash
# Symptom
Error: AccessDeniedException when calling GetCostAndUsage
```

**Solution:**
Add IAM permission `ce:GetCostAndUsage`:
```json
{
  "Effect": "Allow",
  "Action": ["ce:GetCostAndUsage"],
  "Resource": "*"
}
```

---

**Issue: Text too long for engine**
```bash
# Symptom
Error: Text exceeds character limit
```

**Solution:**
- Standard/Neural/Generative: Max 3,000 chars per request
- Long-form: Max 100,000 chars per request
- Split long text into chunks or use Long-form engine

---

### Getting Help

```bash
# General help
aws-polly-tts-tool --help

# Command-specific help
aws-polly-tts-tool synthesize --help
aws-polly-tts-tool list-voices --help

# Show version
aws-polly-tts-tool --version

# Verify configuration
aws-polly-tts-tool info
```

### Debug Mode

Use progressive verbosity to diagnose issues:
```bash
# Basic debug info
aws-polly-tts-tool synthesize "Hello" -V

# Detailed debug info
aws-polly-tts-tool synthesize "Hello" -VV

# Full AWS SDK trace
aws-polly-tts-tool synthesize "Hello" -VVV
```

</details>

## Best Practices

1. **Default to Neural Engine**: Best balance of quality and cost for most use cases
2. **Use SSML for Control**: Add pauses, emphasis, and prosody for natural speech
3. **Cache Audio Files**: Save synthesized audio to avoid repeated API calls and costs
4. **Monitor Costs**: Use `billing` command to track actual spending
5. **Validate Voice Support**: Use `list-voices` to check engine compatibility before synthesis
6. **Save Critical Audio**: Use `--output` to save important audio for offline use
7. **Use Verbosity**: Add `-V/-VV/-VVV` when debugging issues
8. **Leverage stdin**: Pipe text from files or commands for automation

## Resources

- **GitHub**: https://github.com/dnvriend/aws-polly-tts-tool
- **Amazon Polly Docs**: https://docs.aws.amazon.com/polly/
- **Polly Pricing**: https://aws.amazon.com/polly/pricing/
- **SSML Reference**: https://docs.aws.amazon.com/polly/latest/dg/supportedtags.html
- **Boto3 Polly API**: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html
