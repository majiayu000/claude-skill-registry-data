---
name: ai-chat-app
version: 1.0.1
description: "Generate a mobile AI chat application (HTML) that connects to any OpenAI-compatible API. Supports streaming responses, conversation memory, custom system prompts, and works on any mobile browser."
description_zh: "生成移动端 AI 聊天应用（HTML），可对接任意 OpenAI 兼容 API（如 DeepSeek、通义千问、Ollama 等）。支持流式输出、对话记忆、自定义系统提示词，可在手机浏览器直接使用。"
license: MIT
---

# AI Chat App Generator

Generate a complete mobile AI chat application that users can run in any mobile browser.

## Triggers

- "生成 AI 聊天应用"
- "做一个 AI 对话 App"
- "接 AI 的应用"
- "AI chat app"
- "对接大模型的应用"
- "chatbot 应用"

## Output

Produces a single `ai-chat.html` file that works in any mobile browser (Chrome, Safari, etc.).

## Features

- **Streaming output** — responses appear word-by-word like ChatGPT
- **Multi-model support** — works with any OpenAI-compatible API endpoint
- **Conversation memory** — maintains full context across messages
- **Persistent settings** — API config saved to localStorage
- **Custom system prompt** — users can set AI persona
- **Dark theme** — optimized for mobile viewing
- **Touch-friendly** — swipe and button controls

## API Configuration

Users configure these in the app's settings panel:
- **API URL** — e.g. `https://api.openai.com/v1/chat/completions`
- **API Key** — e.g. `sk-...`
- **Model name** — e.g. `gpt-3.5-turbo`, `deepseek-chat`, etc.
- **System prompt** (optional)

### Supported APIs

| Provider | API URL |
|----------|---------|
| OpenAI | `https://api.openai.com/v1/chat/completions` |
| DeepSeek | `https://api.deepseek.com/v1/chat/completions` |
| 通义千问 | `https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions` |
| Ollama (local) | `http://localhost:11434/v1/chat/completions` |

## Usage

1. Generate the `ai-chat.html` file using the template in `assets/ai-chat.html`
2. Deliver it to the user
3. Instruct user to open it in their mobile browser
4. User clicks the settings button to configure API, then starts chatting

## File Structure

```
ai-chat-app/
── SKILL.md
└── assets/
    └── ai-chat.html
```
