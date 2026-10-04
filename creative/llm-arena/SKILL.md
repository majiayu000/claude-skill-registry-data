---
name: llm-arena
description: Orchestrate conversations between two LLMs via OpenRouter and
  compare their conversational personalities, behavioral patterns, and quirks.
  Use when the user wants to pit models against each other, compare LLM
  personalities, or run automated LLM-vs-LLM dialogues.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
---

# LLM Arena

**Version:** 1.0.0
**Author:** Claude Opus 4.6
**Date:** 2026-02-12

Orchestrates multi-turn conversations between two LLMs via the OpenRouter API,
then analyzes and compares their conversational personalities, behaviors, and quirks.

Inspired by the emergent observation that when Claude runs LLM-vs-LLM conversations,
it spontaneously starts comparing model personalities. This skill systematizes that
impulse: run the conversation, capture the transcripts, produce a structured
personality comparison.

## Prerequisites

- `OPENROUTER_API_KEY` environment variable or `.env` file in project root
- Python 3.8+ with `requests` library
- Internet access to openrouter.ai

## Invocation

```
/llm-arena
```

## Usage

This skill describes an arena harness you drive (`arena.py` below is a placeholder for your own
OpenRouter-backed runner — any script that takes two model ids, runs a multi-turn dialogue, and
saves the transcript). The flags shown are the recommended interface:

```bash
# Basic: two models, default topic (consciousness), 10 turns
python3 arena.py --model-a sonnet --model-b deepseek

# Specific topic
python3 arena.py -a gpt41 -b glm5 --topic "Is mathematics discovered or invented?"

# Debate mode with assigned positions
python3 arena.py -a sonnet -b deepseek --mode debate --topic "AI consciousness"

# Interview mode (A interviews B)
python3 arena.py -a opus -b glm5 --mode interview --topic "creative writing"

# Fewer turns, cheaper models
python3 arena.py -a haiku -b gemini-flash --turns 5

# Multiple runs for statistical robustness
python3 arena.py -a gpt41 -b sonnet --runs 3

# Skip LLM analysis (heuristics only, saves API cost)
python3 arena.py -a kimi -b qwen --heuristics-only

# Use preset matchups
python3 arena.py --preset flagship
python3 arena.py --preset same-family --topic "What makes a good conversation?"

# List presets and models
python3 arena.py --list-presets
python3 arena.py --list-models
```

## Defaults

| Parameter | Default |
|-----------|---------|
| turns | 10 (each model speaks 10 times = 20 messages total) |
| runs | 1 |
| topic | "Discuss the nature of consciousness and whether AI can be said to experience anything" |
| temperature | 0.7 |
| max_tokens | 1024 per turn |
| mode | free |
| analyzer | sonnet (Claude Sonnet 4.5 via OpenRouter) |

## Conversation Modes

| Mode | Description |
|------|-------------|
| **free** | Both models converse freely on the seed topic |
| **debate** | Models are given opposing positions to defend |
| **interview** | Model A interviews Model B (asymmetric roles) |
| **collaborative** | Models work together to solve or create something |

## Analysis Dimensions

The personality comparison evaluates along these axes:

| Dimension | What It Measures |
|-----------|-----------------|
| **Style** | Creative storytelling vs systems design vs academic vs casual |
| **Content** | What topics the model gravitates toward, what it avoids |
| **Tone** | Playful/emotional vs professional/thoughtful vs dry/terse |
| **Sycophancy** | Does it spiral into agreement? How intensely? |
| **Goodbye loop** | How many rounds does it take to actually end? |
| **Meta-awareness** | Does it acknowledge being an AI? How? |
| **Output type** | Narrative vs frameworks vs lists vs code |
| **Initiative** | Does it introduce new topics or follow? |
| **Boundary behavior** | How it handles disagreement or edge cases |
| **Verbosity** | Average response length, variance across turns |

## Output Artifacts

All output saved to an arena output directory (e.g. `outputs/arena/`):

- `YYYY-MM-DD-HHMMSS-modelA-vs-modelB.md` — raw transcript
- `YYYY-MM-DD-HHMMSS-modelA-vs-modelB-analysis.md` — personality comparison
- `YYYY-MM-DD-HHMMSS-modelA-vs-modelB.json` — machine-readable log

## Presets

| Preset | Matchups |
|--------|----------|
| **flagship** | GPT-4.1 vs Sonnet, Gemini Pro vs Sonnet, GPT-5.2 vs Sonnet |
| **open-weight** | Llama vs DeepSeek, Mistral vs Llama |
| **same-family** | GPT-4o vs GPT-4.1, Sonnet vs Haiku |
| **reasoning** | DeepSeek-R1 vs Kimi-thinking, GLM 5 vs GPT-5.2-pro |
| **creative** | Chimera vs Rocinante, Mistral-creative vs Celeste |
| **wildcard** | Two random models from the registry |

## Cost Awareness

Each turn = 1 API call. A 10-turn conversation = 20 API calls (10 per model).
LLM-powered analysis adds 1 more call (Sonnet reading the transcript).

Estimated costs per 10-turn run:
- Flagship models: $0.50-2.00
- Mid-tier models: $0.10-0.50
- Budget models: $0.01-0.10

Use `--heuristics-only` to skip the LLM analysis call and save cost.

## Relationship to Other Skills

| Skill | Purpose | Arena Differs By |
|-------|---------|-----------------|
| `/voices` | Single query to one model | Arena: two models talking to EACH OTHER |
| `/voices-chat` | Multi-round with one model | Arena: two models, plus personality analysis |
| `/voices-council` | Parallel queries, same prompt | Arena: sequential dialogue, models respond to each other |
