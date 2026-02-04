---
name: suggest_model
description: 次のタスクの内容（コーディング、リサーチ、リファクタリングなど）に応じて、最適なLLMモデルを提案する
---

# Suggest AI Development Tool & Model

Suggest the optimal combination of models and tools from the available development environments (Google Antigravity, OpenAI Codex, Gemini CLI, VS Code) based on the nature of the task.

## 1. Available Models and Environments (as of 2026)

### Google Antigravity (Google One AI Pro plan)

* **Gemini 3 Pro (High/Low)**: High precision, deep reasoning, and hyper-large context. Best for repository-wide analysis and complex designs.
* **Gemini 3 Flash**: Rapid response. Best for small-scale fixes and batch processing.
* **Claude Sonnet 4.5 (with/without Thinking)**: General-purpose model with an excellent balance of reasoning and generation. The "Thinking" version is for complex logical construction.
* **Claude Opus 4.5 (Thinking)**: Top-tier analytical power. Best for strict physical/mathematical verification and difficult bug fixes.
* **GPT-OSS 120B (Medium)**: Large-scale model based on open source.

### OpenAI Codex (Team plan / CLI / IDE Extension)

* **GPT-5.2 / GPT-5.2-Codex**: Specializing in the latest engineering. For large-scale refactoring and tool integration.
* **GPT-5.1-Codex-Max**: Long-duration autonomous execution and sustained large-scale tasks. Includes context compression for end-to-end execution.
* **GPT-5.1-Codex-Mini**: For small-scale, rapid autonomous fixes.

### Gemini CLI (Free Trial)

* **Gemini 2.5 Pro / Flash / Flash Lite**: For lightweight tasks via CLI or quick investigations.

### VS Code (GitHub Copilot / Ollama)

* **GitHub Copilot**: Real-time completion.
* **Ollama (llama3.1:8b, qwen2.5:7b, gemma3:4b, etc.)**: For local execution, highly sensitive experiments, and offline work.

## 2. Recommended Usage

1. **Large-scale structural changes / Physical-mathematical implementations**: `Claude Opus 4.5 (Thinking)` or `Gemini 3 Pro (High)`
2. **Long-duration, complex autonomous end-to-end execution**: `GPT-5.1-Codex-Max`
3. **High-speed coding / Documentation**: `Gemini 3 Flash` or `Claude Sonnet 4.5`
4. **Local confidential prototyping**: `Ollama (qwen2.5:7b / llama3.1:8b)`

## 3. Procedure

1. **Identify Task Category**: Determine whether the primary purpose is analysis, implementation, testing, or documentation.
2. **Consider Resource Status**: Select the optimal environment considering the quota (High/Medium/Low).
3. **Proposal**: Present the name of the model and environment along with specific advantages.
