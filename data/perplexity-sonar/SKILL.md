---

name: perplexity-sonar
description: Use Perplexity Sonar API for real-time, citation-backed answers. Ideal for up-to-date information and quick synthesis. Requires PERPLEXITY_API_KEY
---

# Perplexity Sonar Skill

This skill utilizes the Perplexity Sonar API to provide synthesized answers backed by real-time web sources. It uses the OpenAI Python library for compatibility.

## Setup

1. **Dependencies:**

    ```bash
    pip install openai python-dotenv
    ```

2. **API Key Configuration:** The skill requires the `PERPLEXITY_API_KEY`. Ensure it is set in a `.env` file in the project root.

    ```bash
    # If the script fails due to a missing key, run the following:
    echo "It seems the Perplexity API key is not set up."
    read -p "Enter your Perplexity API key: " PPLX_KEY
    echo "PERPLEXITY_API_KEY=$PPLX_KEY" >> .env
    # Ensure .env is ignored by git
    if [ -f .gitignore ] && ! grep -q ".env" .gitignore; then echo ".env" >> .gitignore; fi
    echo "API key saved to .env."
    ```

## Usage

Use the `scripts/ask.py` script to query the Sonar API.

### Command

```bash
python3 scripts/ask.py --prompt "<your_research_question>" [--model <model_name>]
````

### Parameters

* `--prompt` (Required): The research question.
* `--model` (Optional): Defaults to `sonar-medium-online`. Use `sonar-large-online` for comprehensive analysis.

### Example

```bash
python3 scripts/ask.py --prompt "What are the latest developments in the EV market in Q4 2025?" --model sonar-large-online
```

## Output

The script outputs the synthesized answer directly to stdout, with citations integrated by the Perplexity model.
