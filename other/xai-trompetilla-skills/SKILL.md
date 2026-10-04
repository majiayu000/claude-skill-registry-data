---
name: xai
description: Chat with Grok models via xAI API. Supports Grok-3, Grok-3-mini, vision, and more.
homepage: https://docs.x.ai
user-invocable: true
disable-model-invocation: true
triggers:
  - grok
  - xai
  - ask grok
metadata:
  clawdbot:
    emoji: "🤖"
    primaryEnv: XAI_API_KEY
    requires:
      bins: [node]
      env: [XAI_API_KEY]
---

# xAI / Grok

Chat with xAI's Grok models. Supports text and vision.

## Setup

Set your API key in the skill config:

```bash
# Via clawdbot config
clawdbot config set skills.entries.xai.apiKey "xai-YOUR-KEY"

# Or environment variable
export XAI_API_KEY="xai-YOUR-KEY"
```

Get your API key at: https://console.x.ai

## Commands

### Chat with Grok
```bash
node {baseDir}/scripts/chat.js "What is the meaning of life?"
```

### Use a specific model
```bash
node {baseDir}/scripts/chat.js --model grok-3-mini "Quick question: 2+2?"
```

### Vision (analyze images)
```bash
node {baseDir}/scripts/chat.js --image /path/to/image.jpg "What's in this image?"
```

### 🔍 Search X/Twitter (Real-time!)
```bash
node {baseDir}/scripts/search-x.js "Remotion video framework"
node {baseDir}/scripts/search-x.js --days 7 "Claude AI tips"
node {baseDir}/scripts/search-x.js --handles @remotion_dev "updates"
```

Uses xAI Responses API with x_search tool for real X posts with citations.

### List available models
```bash
node {baseDir}/scripts/models.js
```

## Available Models

- `grok-3` - Most capable, best for complex tasks
- `grok-3-mini` - Fast and efficient
- `grok-3-fast` - Optimized for speed
- `grok-2-vision-1212` - Vision model for image understanding

## Example Usage

**User:** "Ask Grok what it thinks about AI safety"
**Action:** Run chat.js with the prompt

**User:** "Use Grok to analyze this image" (with attached image)
**Action:** Run chat.js with --image flag

**User:** "What Grok models are available?"
**Action:** Run models.js

## API Reference

xAI API Docs: https://docs.x.ai/api

## Environment Variables

- `XAI_API_KEY` - Your xAI API key (required)
- `XAI_MODEL` - Default model (optional, defaults to grok-3)

## Security & Permissions

**What this skill does:**
- Sends chat prompts to xAI's API at `api.x.ai`
- Vision mode sends images to xAI for analysis
- `scripts/models.js` lists available models (read-only)

**What this skill does NOT do:**
- Does not access local files (except images you explicitly pass with `--image`)
- Does not store conversation history or logs
- Does not send credentials to any endpoint other than `api.x.ai`
- Cannot be invoked autonomously by the agent (`disable-model-invocation: true`)

**Bundled scripts:** `scripts/chat.js` (chat), `scripts/models.js` (list models), `scripts/search-x.js` (X search)

Review scripts before first use to verify behavior.
