---
name: dk-lm-studio-pydantic-ai
description: >
    Use LM Studio as a local LLM backend with Pydantic AI for structured output extraction.
    Provides server setup, agent configuration, and extraction patterns using OpenAI-compatible
    API with local models. Use when user wants local inference, offline AI, or self-hosted LLMs.
license: MIT
compatibility: Requires Python 3.10+, LM Studio, pydantic-ai. The `lmstudio` Python package is optional (CLI-based helpers used by default).
disable-model-invocation: true
metadata:
    version: "1.0.0"
    author: opencode
    opencode/autoinvoke: false
---

# LM Studio with Pydantic AI

Use LM Studio as a local inference backend with Pydantic AI to extract structured data from text using self-hosted LLMs.

## When to Use This Skill

Invoke this skill when:

- User wants to use a local LLM (LM Studio) with Pydantic AI
- User mentions LM Studio, local inference, offline AI, or self-hosted LLMs
- User asks to extract structured data from text (keywords, entities, sentiment)
- Building document processing pipelines
- Need structured output without API calls to OpenAI/Anthropic

Do **not** use this skill for:

- Cloud-based LLM providers (OpenAI, Anthropic, Google)
- General Pydantic AI agent patterns (use `building-pydantic-ai-agents` instead)
- Non-Pydantic AI frameworks

## Prerequisites

```bash
uv add "pydantic-ai-slim[openai]" python-dotenv
```

The `lmstudio` Python package is **optional** — by default, CLI-based helpers are used. If you prefer the Python SDK approach, add it with `uv add lmstudio`.

Ensure LM Studio is installed with a downloaded model.

## Quick-Start Patterns

### Ensure Model is Loaded

Always call this before creating any Pydantic AI agent. The helper functions are in `references/lmstudio_utils.py`:

```python
# lm_server.py (CLI-based, no extra package needed)
import sys
sys.path.insert(0, "path/to/references")
from lmstudio_utils import ensure_model_loaded

def ensure_model_loaded(model_name: str) -> str:
    """Ensure LM Studio server is running and model is loaded. Returns model identifier."""
    from lmstudio_utils import ensure_server_running, load_model
    ensure_server_running()
    return load_model(model_name)
```

### Create a Structured Output Agent

```python
import os
from pydantic import BaseModel
from typing import List

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.settings import ModelSettings
from pydantic_ai.exceptions import UnexpectedModelBehavior

from lm_server import ensure_model_loaded

INFERENCE_MODEL = os.getenv("LOCAL_MODEL_INFERENCE")  # Required - must be set in .env
LMSTUDIO_BASE_URL = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1")


# Define output schema (customize for your use case)
class PersonInfo(BaseModel):
    name: str
    email: str
    skills: List[str]


# Create agent
def extract_person_info(text: str) -> PersonInfo:
    ensure_model_loaded(INFERENCE_MODEL)

    agent = Agent(
        model=OpenAIChatModel(
            INFERENCE_MODEL,
            provider=OpenAIProvider(
                base_url=LMSTUDIO_BASE_URL,
                api_key="x",
            ),
        ),
        model_settings=ModelSettings(
            thinking=False,
            extra_body={"chat_template_kwargs": {"enable_thinking": False}},
        ),
        retries=5,
        output_type=PersonInfo,
        instructions="Extract person information from the text. Return only valid JSON.",
    )

    try:
        return agent.run_sync(user_prompt=text).output
    except UnexpectedModelBehavior as exc:
        raise RuntimeError(f"Extraction failed: {exc}")
```

### Agent Factory Pattern

For reusable agents:

```python
from typing import Type
from pydantic import BaseModel


def create_extractor(output_type: Type[BaseModel], instructions: str):
    """Factory for creating extraction agents."""
    return Agent(
        model=OpenAIChatModel(
            INFERENCE_MODEL,
            provider=OpenAIProvider(
                base_url=LMSTUDIO_BASE_URL,
                api_key="x",
            ),
        ),
        model_settings=ModelSettings(
            thinking=False,
            extra_body={"chat_template_kwargs": {"enable_thinking": False}},
        ),
        retries=5,
        output_type=output_type,
        instructions=instructions,
    )


# Usage: define schema and create agent
class PersonInfo(BaseModel):
    name: str
    email: str
    skills: List[str]


def extract_person_info(text: str) -> PersonInfo:
    ensure_model_loaded(INFERENCE_MODEL)
    agent = create_extractor(
        PersonInfo,
        "Extract person information from the text.",
    )
    return agent.run_sync(user_prompt=text).output
```

## Environment Setup

Create `.env` in your project:

```bash
LMSTUDIO_BASE_URL=http://localhost:1234/v1
LOCAL_MODEL_INFERENCE=your-model-key-here
```

The model key must match a model downloaded in LM Studio. No default fallback — require explicit configuration.

## Configuration Reference

| Parameter           | Purpose                       | Example                                                |
| ------------------- | ----------------------------- | ------------------------------------------------------ |
| `INFERENCE_MODEL`   | Model identifier in LM Studio | `qwen3.5-4b-mlx`                                       |
| `LMSTUDIO_BASE_URL` | API endpoint                  | `http://localhost:1234/v1`                             |
| `thinking=False`    | Disable chain-of-thought      | Clean JSON output                                      |
| `extra_body`        | Model-specific flags          | `{"chat_template_kwargs": {"enable_thinking": False}}` |
| `retries=5`         | Handle output errors          | Graceful failures                                      |

## Common Extraction Patterns

### Extracting Named Entities

```python
from pydantic import BaseModel
from typing import List


class EntityExtraction(BaseModel):
    persons: List[str]
    organizations: List[str]
    locations: List[str]
    dates: List[str]


def extract_entities(text: str) -> EntityExtraction:
    ensure_model_loaded(INFERENCE_MODEL)
    agent = create_extractor(
        EntityExtraction,
        "Extract named entities from the text. Return only valid JSON.",
    )
    return agent.run_sync(user_prompt=text).output
```

### Sentiment Analysis

```python
from pydantic import BaseModel
from typing import List


class SentimentResult(BaseModel):
    sentiment: str  # positive, negative, neutral
    confidence: float
    key_phrases: List[str]


def analyze_sentiment(text: str) -> SentimentResult:
    ensure_model_loaded(INFERENCE_MODEL)
    agent = create_extractor(
        SentimentResult,
        "Analyze the sentiment of the text. Return only valid JSON.",
    )
    return agent.run_sync(user_prompt=text).output
```

### Document Classification

```python
from pydantic import BaseModel
from typing import List


class ClassificationResult(BaseModel):
    category: str
    subcategory: str
    confidence: float
    reasons: List[str]


def classify_document(text: str) -> ClassificationResult:
    ensure_model_loaded(INFERENCE_MODEL)
    agent = create_extractor(
        ClassificationResult,
        "Classify the document into categories. Return only valid JSON.",
    )
    return agent.run_sync(user_prompt=text).output
```

## Troubleshooting

### Server Not Running

```bash
# Start manually
lms server start

# Or use Python
subprocess.run(["lms", "server", "start"])
```

### Model Not Loaded

Ensure the model is downloaded in LM Studio UI and the model key matches exactly (check LM Studio's model list).

### Unexpected Output / Garbage

- Use `thinking=False` in ModelSettings
- Add `"enable_thinking": False` to `extra_body` for Qwen/Gemma models
- Make instructions more explicit: "Return ONLY valid JSON matching the schema."
- Add post-processing: `sorted(set(...))` to deduplicate and sort results

### Permission Denied

LM Studio CLI (`lms`) must be on PATH. On macOS, it should be installed via Homebrew or added to PATH.

### Alternative: Python SDK Approach

If you installed the optional `lmstudio` package, you can use the Python SDK instead:

```bash
uv add lmstudio
```

```python
import lmstudio as lms

def ensure_model_loaded_sdk(model_name: str) -> None:
    """SDK-based model loading (requires lmstudio package)."""
    client = lms.get_default_client()

    if not any(model_name in m.identifier for m in lms.list_loaded_models()):
        client.llm.load_new_instance(model_name)
```

The CLI approach is preferred — it has no extra dependency and provides the same functionality.

## Generic File Structure Template

```
project/
├── .env                    # LMSTUDIO_BASE_URL, LOCAL_MODEL_INFERENCE
├── references/
│   └── lmstudio_utils.py   # ensure_server_running(), load_model()
├── lm_server.py           # ensure_model_loaded() wrapper
├── models.py               # Pydantic output schemas
├── prompts.py             # Agent instructions
├── extractors/
│   ├── entity_extractor.py
│   ├── sentiment_extractor.py
│   └── classifier.py
└── main.py              # Entry point
```

---

## Example Use Case: CV/JD Matching Pipeline

_This section demonstrates a real-world application using the patterns above. It's project-specific — adapt the schemas and logic for your own use case._

### Use Case Overview

Score CVs against job descriptions and generate edit plans to maximize ATS matching:

```python
# models.py - Project-specific schemas
from pydantic import BaseModel
from typing import List

class KeywordExtraction(BaseModel):
    skills_technology: List[str]
    skills_domain: List[str]

class JDMeta(BaseModel):
    role_summary: str
    key_responsibilities: List[str]
    skills_must_have: List[str]
    experience_requirements: List[str]

class ATSScore(BaseModel):
    total: float
    semantic_sim: float
    missing_technology: List[str]
    missing_domain: List[str]

class EditPlan(BaseModel):
    injections: List[str]
    rephrases: List[str]
    new_bullets: List[str]
```

### Pipeline Flow

```python
# 1. Extract CV keywords (one-time)
from cv_extractor import extract_cv, save_extraction

cv = extract_cv("data/cv.yml")
save_extraction(cv, "data/cv.yml")  # Cache to JSON

# 2. Extract JD metadata + keywords (per job)
from jd_extractor import load_all_jd_rows, extract_jd

rows = load_all_jd_rows("data/jobs/")
for row in rows:
    jd = extract_jd(row)
    # Score and generate edit plan...

# 3. Score and tailor
from ats_score import score
from cv_tailor import generate_edit_plan

s = score(cv, jd)
plan = generate_edit_plan(cv, jd, s)
```

### Project File Structure

```
project/
├── .env
├── references/
│   └── lmstudio_utils.py   # Server/model helpers
├── models.py          # Project-specific schemas
├── prompts.py         # Custom instructions per extraction
├── cv_extractor.py    # CV extraction logic
├── jd_extractor.py   # JD extraction logic
├── ats_score.py      # Scoring logic
├── cv_tailor.py       # Edit plan generation
├── data/
│   ├── cv/
│   └── jd/
└── main.py
```

This pattern scales to any document extraction pipeline. Replace the schemas and prompts for your domain.
