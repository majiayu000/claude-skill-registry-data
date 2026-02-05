---
name: stanford-storm
description: Run Stanford STORM (knowledge-storm) to generate comprehensive, Wikipedia-style articles with citations. Requires LLM and Search API keys (Bing or You.com).
---

# Stanford STORM Skill

This skill allows you to use Stanford STORM, an LLM-powered system for generating detailed, Wikipedia-style articles. It uses `litellm` for flexible LLM configuration.

## Setup

1.  **Dependencies:** Requires `knowledge-storm` and `litellm`.
    ```bash
    pip install knowledge-storm dspy-ai litellm python-dotenv
    ```

2.  **Configuration:** STORM needs API keys for the LLM (e.g., OPENAI_API_KEY, ANTHROPIC_API_KEY) and a Search Provider (BING_SEARCH_API_KEY or YDC_API_KEY). LiteLLM reads these standard environment variable names.

    ```bash
    # Ensure keys are set. Example for OpenAI and Bing:
    if [ -z "$OPENAI_API_KEY" ] || [ -z "$BING_SEARCH_API_KEY" ]; then
        echo "STORM requires API keys."
        echo "Ensure your LLM key (e.g., OPENAI_API_KEY) and Search key (BING_SEARCH_API_KEY or YDC_API_KEY) are set in .env."
        # Add interactive setup here if desired, ensuring the correct variable names are used.
    fi
    ```

## Usage

Use the `scripts/run_storm.py` script to generate an article.

### Command

```bash
python3 scripts/run_storm.py --topic "<topic>" [--rm-name <bing|you>] [--fast-model <model>] [--strong-model <model>]
```

### Parameters

* `--topic` (Required): The subject to research.
* `--rm-name` (Optional): Retriever module (default `bing`). Ensure the corresponding API key is set.
* `--fast-model` (Optional): LLM for simulation/questions (e.g., `gpt-3.5-turbo`).
* `--strong-model` (Optional): LLM for outline/writing (e.g., `gpt-4o`, `claude-3-5-sonnet-20240620`).

### Example

```bash
python3 scripts/run_storm.py --topic "The History of Quantum Computing" --strong-model gpt-4o --rm-name bing
```

## Output

The script outputs the final article in Markdown format to stdout. Intermediate files (outline, raw research) are saved in the `storm_output/` directory (logged to stderr). The process can take several minutes.
