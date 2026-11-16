---
name: ollama-patterns
description: Ollama local LLM — pull models, generate, chat, embeddings, REST API, Python client, structured output
triggers:
  - ollama
  - local llm ollama
  - ollama python
  - ollama chat
  - ollama generate
  - ollama embeddings
  - ollama structured output
  - ollama model pull
  - ollama api
  - run llm locally
do_not_use_for:
  - cloud LLM APIs — use litellm/portkey
  - structured generation with local models — use outlines for guaranteed schema
  - vector database — use qdrant
see_also:
  - outlines
  - litellm
  - portkey
  - vllm-paged-attention
---

# Ollama — Local LLM

## Setup & Pull Models

```bash
# Install
curl -fsSL https://ollama.ai/install.sh -o /tmp/ollama-install.sh
# Inspect first: head -40 /tmp/ollama-install.sh — then run if safe:
sh /tmp/ollama-install.sh

# Pull models
ollama pull llama3.2             # 3B — fast, good for dev
ollama pull llama3.1:8b          # 8B — balanced quality
ollama pull mistral-nemo         # 12B — strong reasoning
ollama pull deepseek-r1:8b       # reasoning model
ollama pull nomic-embed-text     # embeddings
ollama pull mxbai-embed-large    # better embeddings

# List, remove
ollama list
ollama rm llama3.2
ollama show llama3.2             # model info, parameters
```

## Python Client

```python
import ollama

# Simple chat
response = ollama.chat(
    model="llama3.2",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum entanglement briefly."},
    ],
)
print(response["message"]["content"])

# Streaming
for chunk in ollama.chat(
    model="llama3.2",
    messages=[{"role": "user", "content": "Write a haiku"}],
    stream=True,
):
    print(chunk["message"]["content"], end="", flush=True)

# Generate (no chat format)
response = ollama.generate(
    model="llama3.2",
    prompt="Complete this: The sky is",
    options={"temperature": 0.8, "top_p": 0.9, "num_predict": 100},
)
print(response["response"])
```

## Embeddings

```python
import ollama

# Single embedding
result = ollama.embeddings(
    model="nomic-embed-text",
    prompt="Machine learning is fascinating",
)
vector = result["embedding"]   # List[float], dim=768

# Batch embeddings (loop — no native batch API)
texts = ["text1", "text2", "text3"]
embeddings = [
    ollama.embeddings(model="nomic-embed-text", prompt=t)["embedding"]
    for t in texts
]

# With async client
import asyncio

async def embed_batch(texts: list[str]) -> list[list[float]]:
    client = ollama.AsyncClient()
    tasks = [client.embeddings(model="nomic-embed-text", prompt=t) for t in texts]
    results = await asyncio.gather(*tasks)
    return [r["embedding"] for r in results]
```

## Async Client

```python
import asyncio
import ollama

async def main():
    client = ollama.AsyncClient()

    # Async chat
    response = await client.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": "Hello"}],
    )
    print(response["message"]["content"])

    # Async streaming
    async for chunk in await client.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": "Tell me a story"}],
        stream=True,
    ):
        print(chunk["message"]["content"], end="", flush=True)

asyncio.run(main())
```

## Structured Output (JSON mode)

```python
import ollama
import json

response = ollama.chat(
    model="llama3.2",
    messages=[{
        "role": "user",
        "content": "Extract: name, age, profession from: 'John is a 30-year-old engineer'",
    }],
    format="json",                  # forces JSON output
)
data = json.loads(response["message"]["content"])
print(data["name"], data["age"])    # "John", 30

# With Pydantic schema
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int
    profession: str

response = ollama.chat(
    model="llama3.2",
    messages=[{"role": "user", "content": "Extract from: 'Alice is a 25-year-old designer'"}],
    format=Person.model_json_schema(),   # enforce schema
)
person = Person.model_validate_json(response["message"]["content"])
```

## REST API (curl / direct)

```bash
# Generate
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Why is the sky blue?",
  "stream": false
}'

# Chat
curl http://localhost:11434/api/chat -d '{
  "model": "llama3.2",
  "messages": [{"role": "user", "content": "Hello"}],
  "stream": false
}'

# Embeddings
curl http://localhost:11434/api/embeddings -d '{
  "model": "nomic-embed-text",
  "prompt": "Here is an article about llamas"
}'
```

## OpenAI-Compatible API

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",               # required but ignored
)

response = client.chat.completions.create(
    model="llama3.2",
    messages=[{"role": "user", "content": "Say hello"}],
)
print(response.choices[0].message.content)

# Works with any OpenAI-compatible library
```

## Modelfile — Custom Models

```dockerfile
# Modelfile
FROM llama3.2

SYSTEM """You are a Python expert. Always include type hints and docstrings."""

PARAMETER temperature 0.3
PARAMETER top_p 0.9
PARAMETER num_predict 2048
```

```bash
ollama create python-expert -f Modelfile
ollama run python-expert "Write a binary search function"
```

## Anti-Fake-Pass Checks

- Ollama server must be running: `ollama serve` or daemon auto-start on macOS/Linux
- `stream=False` in REST API — without it, response is streaming NDJSON, not single JSON
- `format="json"` encourages but doesn't guarantee valid JSON — use outlines for guaranteed schema
- Embeddings are model-specific dimension — `nomic-embed-text`=768, `mxbai-embed-large`=1024
- `num_predict=-1` means unlimited tokens — set a limit to avoid runaway generation
- Async client returns coroutines — must `await` every call inside `async def`
- OpenAI-compatible API at `/v1` — base_url must include `/v1` path
