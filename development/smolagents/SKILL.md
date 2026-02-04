---
name: smolagents
description: Use Hugging Face Smolagents framework for code-based agentic research with tool support. Supports multiple LLM providers and web search.
---

# Smolagents Skill

This skill leverages Hugging Face's Smolagents framework, a minimalist AI agent library where agents write Python code to accomplish tasks. It's highly efficient (30% token efficiency gain) and supports multiple LLM providers.

## Setup

1. **Dependencies:** Requires `smolagents` with toolkit extensions.

    ```bash
    pip install 'smolagents[toolkit]' python-dotenv
    ```

2. **API Key Configuration:** Supports multiple LLM providers. At minimum, set one:

    ```bash
    # For Hugging Face Inference API (default, free tier available)
    echo "HF_TOKEN=your_huggingface_token" >> .env
    
    # OR for OpenAI
    echo "OPENAI_API_KEY=your_openai_key" >> .env
    
    # OR for Anthropic
    echo "ANTHROPIC_API_KEY=your_anthropic_key" >> .env
    
    if [ -f .gitignore ] && ! grep -q ".env" .gitignore; then echo ".env" >> .gitignore; fi
    ```

## Usage

Use the `scripts/agent.py` script to run research tasks.

### Command

```bash
python3 scripts/agent.py --task "<task_description>" [--model <model_type>] [--model-id <model_name>] [--web-search]
```

### Parameters

* `--task` (Required): The task or research question.
* `--model` (Optional): Model type - `hf` (Hugging Face), `openai`, `anthropic`, or `local` (default: `hf`).
* `--model-id` (Optional): Specific model ID to use.
* `--web-search` (Optional): Enable web search tool (uses DuckDuckGo).
* `--verbose` (Optional): Show detailed execution logs.

### Example

```bash
# Using Hugging Face Inference API with web search
python3 scripts/agent.py --task "Research the latest developments in transformer architecture improvements" --web-search --verbose

# Using a specific model
python3 scripts/agent.py --task "Analyze the impact of RLHF on LLM performance" --model hf --model-id "Qwen/Qwen2.5-72B-Instruct" --web-search
```

## Output

The script outputs:

* Generated Python code (to stderr for visibility)
* Task execution results
* Final answer or research findings

## Features

* **Code-as-Action**: Agents write and execute Python code to solve tasks
* **Tool Support**: Web search, file operations, and custom tools
* **Multi-Model**: Supports HF Inference API, OpenAI, Anthropic, local models
* **Efficient**: 30% token efficiency improvement over traditional approaches
