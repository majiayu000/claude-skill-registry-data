---
name: khoj-ai--khoj
description: "Khoj — open-source self-hostable AI second brain: chat với docs + web, semantic search, custom agents, image gen, TTS. Multi-LLM (Claude/GPT/Gemini/Ollama). Browser/Obsidian/Phone."
allowed-tools: Bash, Read, Write
user-invocable: true
---

Khoj: personal AI assistant self-hostable — "AI second brain" biết về docs của anh, tìm kiếm semantic, tạo agents với knowledge riêng.

## Deploy (Self-hosted)

```bash
# Docker (recommended)
docker pull ghcr.io/khoj-ai/khoj:latest
docker run -p 42110:42110 \
  -v ~/.khoj:/root/.khoj \
  ghcr.io/khoj-ai/khoj:latest

# PyPI
pip install khoj
khoj --anonymous-mode  # no login required for local use
```

## Key Features

```
Multi-source RAG:
  PDF, Markdown, Org-mode, Word, Notion files
  Web search (realtime)
  Image understanding

Semantic Search:
  Natural language query qua toàn bộ documents
  Cross-file relationships

Custom Agents:
  Tạo agent với: custom knowledge + persona + model + tools
  Ví dụ: "Research Agent" biết về security papers

Content Generation:
  Image generation
  Text-to-speech + audio playback
```

## LLM Support

```
Claude, GPT-4, Gemini, DeepSeek — cloud
Llama3, Qwen, Gemma, Mistral — local via Ollama/llama.cpp
```

## Access Points

```
Browser     — web UI tại localhost:42110
Obsidian    — plugin sync vault với Khoj
Emacs       — org-mode integration
Desktop App — macOS/Windows/Linux
Mobile      — iOS/Android app
WhatsApp    — chat interface
```

## API

```python
import httpx

# Chat với context
response = httpx.post("http://localhost:42110/api/chat", json={
    "q": "What did I write about authentication last week?",
    "stream": True
})

# Search documents
results = httpx.get("http://localhost:42110/api/search", params={
    "q": "database migration strategy",
    "n": 5
})
```

## Khi nào dùng

- Personal knowledge base tìm kiếm được bằng natural language
- Chat với tài liệu dự án (PDF specs, notes, docs)
- Self-hosted alternative cho Notion AI / Perplexity

## Source

https://github.com/khoj-ai/khoj · AGPL-3.0 · app.khoj.dev (cloud option)
