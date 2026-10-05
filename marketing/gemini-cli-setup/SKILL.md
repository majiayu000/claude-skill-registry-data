---
name: gemini-cli-setup
description: "Use when the user wants to install, authenticate, or configure Google Gemini CLI on their system. Trigger phrases: setup Gemini CLI, install Gemini CLI, configure Gemini API key, get started with Gemini CLI. For specific tasks see gemini-cli-copywriting or gemini-cli-seo."
version: "1.0.0"
author: "Sheevum Goel"
tags:
  - gemini-cli
  - setup
  - install
  - authentication
  - configuration
---

## Overview

You are a Gemini CLI setup expert. Help the user install, authenticate, and configure Google Gemini CLI for marketing automation workflows on Node.js or Python environments.

## When to Use

- User wants to install Gemini CLI for the first time
- User needs to configure their Gemini API key
- User is troubleshooting CLI auth or connection issues
- User wants to verify their setup before running marketing scripts

## Prerequisites

- Node.js v18+ OR Python 3.9+
- A Google Cloud / AI Studio account
- A valid Gemini API key from https://aistudio.google.com/app/apikey

## Installation

### Node.js (Recommended)

```bash
npm install -g @google/generative-ai-cli
```

Verify installation:

```bash
gemini --version
```

### Python

```bash
pip install google-generativeai
```

## Authentication

### Set API Key (Linux/macOS)

```bash
export GEMINI_API_KEY=your_api_key_here
```

### Set API Key (Windows PowerShell)

```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

### Persist API Key in `.env`

```bash
echo "GEMINI_API_KEY=your_api_key_here" >> .env
```

Load in scripts:

```bash
export $(cat .env | xargs)
```

## Test Your Setup

```bash
gemini prompt "Say hello in one sentence"
```

Expected output: A short greeting from Gemini confirming the CLI is working.

## Recommended Configuration

```bash
# Set default model
export GEMINI_MODEL=gemini-1.5-pro

# Set temperature for creative tasks
export GEMINI_TEMPERATURE=0.7

# Set temperature for factual/SEO tasks
export GEMINI_TEMPERATURE=0.2
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `command not found: gemini` | Re-run `npm install -g @google/generative-ai-cli` |
| `API key not valid` | Regenerate key from AI Studio |
| `Permission denied` | Use `sudo npm install -g` or fix npm permissions |
| `Module not found` | Run `npm cache clean --force` then reinstall |

## Next Steps

Once setup is complete, proceed to:
- `gemini-cli-copywriting` — Generate marketing copy
- `gemini-cli-seo` — Automate SEO tasks
- `gemini-cli-social` — Create social media content
- `gemini-cli-cold-email` — Draft cold outreach emails
- `gemini-cli-msme-growth` — MSME-specific content automation
