---
name: cheahjs--free-llm-api
description: "Danh sách free LLM API providers có rate limits cụ thể — OpenRouter, Groq, Cerebras, Google AI Studio, GitHub Models, Fireworks... Reference khi cần backup API."
allowed-tools: Read
user-invocable: true
---

Curated list free LLM inference APIs với rate limits thực tế — dùng làm reference khi cần backup provider hoặc test model mới.

## Top Free Providers

```
OpenRouter
  Models: Llama 3.3 70B, Hermes 3 405B, DeepSeek V4 Flash
  Limits: 20 req/min, 50 req/day (free tier)
  Top-up: $10 lifetime cho unlimited free models

Groq (anh đang dùng cho aider-groq)
  Models: Llama 3.1 8B → 14,400 req/day, 6,000 tokens/min
  Speciality: fastest inference (hardware accelerated)

Google AI Studio
  Models: Gemini 3.5 Flash → 250,000 tokens/min, 20 req/day
  Caveat: data dùng cho training (ngoài EU/UK/EEA)

Cerebras
  Models: gpt-oss-120b, Llama 3.1 8B
  Limits: 30 req/min, 60,000 tokens/min per model

GitHub Models
  Models: GPT-4o, Claude, Llama, DeepSeek
  Access: cần GitHub Copilot subscription
  Note: "extremely restrictive token limits"
```

## Trial Credit Providers

```
Fireworks, Baseten, AI21, Modal — $1-$30 initial credits
```

## Khi nào dùng

- YAMTAM_BACKUP_STACK: khi Claude hết quota → check list này
- Testing: thử model mới không tốn tiền
- Groq confirmed: anh đang dùng aider-groq với Llama 3.3 70B (14,400 req/day)

## Source

https://github.com/cheahjs/free-llm-api-resources · MIT · +83⭐/day
