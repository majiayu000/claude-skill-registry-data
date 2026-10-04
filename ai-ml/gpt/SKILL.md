---
name: gpt
description: "Generate GPT API request payloads. Use when building chat completions, embeddings, fine-tuning data, or estimating API costs."
version: "3.4.0"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
tags:
  - gpt
  - openai
  - api
  - chat-completion
  - embeddings
  - fine-tuning
---

# gpt

GPT API calling assistant. Build chat completion requests, generate embedding payloads, prepare fine-tuning data, estimate costs, batch requests, and convert between formats.

## Commands

### chat

Build a chat completion request JSON payload from messages.

```bash
bash scripts/script.sh chat --system "You are a translator" --user "Translate: hello"
bash scripts/script.sh chat --system "Helper" --user "Hi" --model gpt-4o --temperature 0.7
```

### embed

Generate an embedding API request payload.

```bash
bash scripts/script.sh embed --input "Text to embed"
bash scripts/script.sh embed --file texts.txt --model text-embedding-3-small
```

### finetune

Prepare and validate fine-tuning JSONL data from source files.

```bash
bash scripts/script.sh finetune --input pairs.csv --output training.jsonl
bash scripts/script.sh finetune --validate training.jsonl
```

### cost

Estimate API costs based on token count and model pricing.

```bash
bash scripts/script.sh cost --tokens 5000 --model gpt-4o
bash scripts/script.sh cost --file input.txt --model gpt-4-turbo
```

### batch

Generate multiple API request payloads from a list of inputs.

```bash
bash scripts/script.sh batch --file prompts.txt --model gpt-4o --output batch_requests.jsonl
```

### convert

Convert between JSONL and CSV data formats.

```bash
bash scripts/script.sh convert --input data.csv --to jsonl --output data.jsonl
bash scripts/script.sh convert --input data.jsonl --to csv --output data.csv
```

## Output

All commands output JSON request bodies or JSONL to stdout by default. Use `--output` to write to a file. Cost estimates print a breakdown table with per-model pricing.


## Requirements
- bash 4+

## Feedback

Report issues or suggestions: https://bytesagain.com/feedback/

---

Powered by BytesAgain | bytesagain.com
