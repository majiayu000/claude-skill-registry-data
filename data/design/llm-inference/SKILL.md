---
name: llm-inference
description: "Use when wanting to interact with any LLM - Explains available inference endpoints so the agent selects suitable models."
---

## LLM Inference

The Cloudflare Pages function `functions/cerebras-chat.ts` provides OpenAI-compatible LLM inference. See `tools/cerebras-llm-inference/index.html` for a working example.

### Available models

| Model | Max context tokens | Requests / minute | Tokens / minute |
| --- | --- | --- | --- |
| gpt-oss-120b | 65,536 | 30 | 64,000 |
| llama-3.3-70b | 65,536 | 30 | 64,000 |
| llama3.1-8b | 8,192 | 30 | 60,000 |
| qwen-3-235b-a22b-instruct-2507 | 65,536 | 30 | 64,000 |
| qwen-3-235b-a22b-thinking-2507 | 65,536 | 30 | 60,000 |
| qwen-3-32b | 65,536 | 30 | 64,000 |
| zai-glm-4.6 | 64,000 | 10 | 150,000 |

- `llama3.1-8b` is the fastest option.
- `zai-glm-4.6` is the most powerful option.
- `gpt-oss-120b` remains the best all rounder.

LLMs are not just for chat: they can be used to process any string in any arbitrary way. If making a tool that requires the LLM to respond in a specific way or format then be very clear and explicit in its system prompt; eg what to include/exclude, plain/markdown formatting, length, etc.
