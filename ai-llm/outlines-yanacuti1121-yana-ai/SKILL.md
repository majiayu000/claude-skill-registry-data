---
name: outlines
description: Outlines — structured generation with guaranteed JSON/regex output from local LLMs
triggers:
  - outlines
  - structured generation
  - guaranteed json llm
  - outlines library
  - json schema generation llm
  - regex constrained generation
  - outlines pydantic
  - llm structured output local
  - outlines vllm
  - outlines transformers
do_not_use_for:
  - cloud API structured output — use claude response_format or openai json_mode
  - evaluation — use ragas/deepeval
  - prompt management — use langfuse/portkey
see_also:
  - pydantic-ai
  - dspy
  - ollama-patterns
  - vllm-paged-attention
---

# Outlines — Structured Generation

## Core: JSON from Pydantic

```python
from outlines import models, generate
from pydantic import BaseModel, Field
from typing import Literal

class Character(BaseModel):
    name: str
    age: int = Field(ge=0, le=150)
    profession: Literal["warrior", "mage", "rogue"]
    backstory: str = Field(max_length=200)

# Load model (HuggingFace transformers)
model = models.transformers("meta-llama/Llama-3.2-3B-Instruct")

# Generator guaranteed to return valid Character JSON
generator = generate.json(model, Character)
character = generator("Create a fantasy character")

print(character.name, character.profession)     # typed Python object
print(type(character))                          # <class 'Character'>
```

## Regex-Constrained Generation

```python
import outlines

model = models.transformers("Qwen/Qwen2.5-1.5B-Instruct")

# Date pattern — only valid date formats generated
date_gen = generate.regex(model, r"\d{4}-\d{2}-\d{2}")
date = date_gen("What is today's date?")
print(date)   # "2024-11-15"

# Phone number
phone_gen = generate.regex(model, r"\+1-\d{3}-\d{3}-\d{4}")
phone = phone_gen("Generate a US phone number")

# Semantic version
semver_gen = generate.regex(model, r"\d+\.\d+\.\d+")
version = semver_gen("What version should we release?")
```

## Choice Selection

```python
# Force model to pick from a fixed set of options
sentiment_gen = generate.choice(model, ["positive", "negative", "neutral"])
result = sentiment_gen("Classify: 'This product is amazing!'")
print(result)   # always exactly "positive", "negative", or "neutral"

# Type-enforced choice
integer_gen = generate.choice(model, [1, 2, 3, 4, 5])
rating = integer_gen("Rate this 1-5")
print(type(rating))   # int
```

## JSON Schema (dict-based)

```python
schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "summary": {"type": "string", "maxLength": 100},
        "sentiment": {"type": "string", "enum": ["positive", "negative", "neutral"]},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
    },
    "required": ["title", "summary", "sentiment", "confidence"],
}

import json
gen = generate.json(model, json.dumps(schema))
result = gen("Analyze this news article: ...")
```

## Batched Generation

```python
from outlines.generate import json as gen_json

generator = gen_json(model, Character)

# Generate multiple at once
prompts = [
    "Create a warrior character",
    "Create a mage character",
    "Create a rogue character",
]
characters = generator(prompts)   # List[Character]
for c in characters:
    print(c.name, c.profession)
```

## With vLLM (Production)

```python
from outlines import models, generate

# vLLM backend for high-throughput production
model = models.vllm("meta-llama/Llama-3.1-8B-Instruct")
gen = generate.json(model, Character)
result = gen("Create a character")
```

## With Ollama

```python
# Use outlines via openai-compatible API
from outlines import models, generate
model = models.openai(
    "ollama/llama3.2",
    api_key="ollama",
    base_url="http://localhost:11434/v1",
)
gen = generate.json(model, Character)
```

## Streaming

```python
from outlines.generate import json as gen_json

generator = gen_json(model, Character)
stream = generator.stream("Create a fantasy character")
for token in stream:
    print(token, end="", flush=True)
```

## Anti-Fake-Pass Checks

- `generate.json` with Pydantic model enforces schema at token level — no post-hoc parsing needed
- `Field(ge=0, le=150)` constraints are honored — model cannot generate out-of-range int
- `Literal["a","b"]` fields become `choice` constraints automatically
- Model must be loaded with `models.transformers()` — not raw HuggingFace pipeline
- vLLM requires `outlines[vllm]` extra — `pip install outlines[vllm]`
- `maxLength` in JSON schema is soft hint for some backends — test with actual model
- Batched generation requires GPU for performance — CPU is too slow for prod
