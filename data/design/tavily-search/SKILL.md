---
name: tavily-search
description: Use Tavily Search API for optimized, real-time web search results for RAG. Requires TAVILY_API_KEY.
---

# Tavily Search Skill

This skill utilizes the Tavily Search API, providing clean, real-time web search results optimized for LLMs and RAG pipelines.

## Setup

1.  **Dependencies:** Requires `tavily-python`.
    ```bash
    pip install tavily-python python-dotenv
    ```

2.  **API Key Configuration:** Requires `TAVILY_API_KEY`.

    ```bash
    # If the script fails due to a missing key, run the following:
    echo "It seems the Tavily API key is not set up."
    read -p "Enter your Tavily API key: " TAVILY_KEY
    echo "TAVILY_API_KEY=$TAVILY_KEY" >> .env
    if [ -f .gitignore ] && ! grep -q ".env" .gitignore; then echo ".env" >> .gitignore; fi
    echo "API key saved to .env."
    ```

## Usage

Use the `scripts/tavily_search.py` script.

### Command

```bash
python3 scripts/tavily_search.py --query "<query>" [--max-results <N>] [--search-depth <basic|advanced>]
```

### Parameters

* `--query` (Required): The search query.
* `--search-depth` (Optional): Default `basic`. Use `advanced` for intensive research (higher quality, slower).
* `--max-results` (Optional): Default 10.

### Example

```bash
python3 scripts/tavily_search.py --query "autonomous research agents comparison" --search-depth advanced
```

## Output

The script outputs JSON containing a synthesized `answer` (if requested by the script) and a list of `results` (URL, title, content snippets).
