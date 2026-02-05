---
name: Ollama Local Models
description: Expert guidance for integrating Ollama local AI models with Python applications, including installation, configuration, model management, and production deployment
version: 1.0.0
---

# Ollama Local Models Integration

Complete guide for working with Ollama - running open-source LLMs locally with Python integration.

## Installation and Setup

### Install Ollama

```bash
# Linux
curl -fsSL https://ollama.com/install.sh | sh

# macOS
brew install ollama

# Windows
# Download from https://ollama.com/download/windows

# Verify installation
ollama --version

# Start Ollama service
ollama serve
```

### Install Python Library

```bash
# Install Ollama Python library
pip install ollama

# Or with additional dependencies
pip install ollama aiohttp pydantic
```

## Basic Usage

### Simple Text Generation

```python
import ollama

# Generate text
response = ollama.generate(
    model='llama3.2',
    prompt='Explain quantum computing in simple terms'
)
print(response['response'])

# With options
response = ollama.generate(
    model='llama3.2',
    prompt='Write a Python function to calculate fibonacci',
    options={
        'temperature': 0.7,
        'top_p': 0.9,
        'top_k': 40,
        'num_predict': 500
    }
)
```

### Streaming Responses

```python
import ollama

def stream_generate(prompt: str, model: str = 'llama3.2'):
    """Generate with streaming"""
    stream = ollama.generate(
        model=model,
        prompt=prompt,
        stream=True
    )

    for chunk in stream:
        print(chunk['response'], end='', flush=True)

# Usage
stream_generate("Tell me a story about AI")
```

### Chat Interface

```python
import ollama

def chat_conversation():
    """Multi-turn conversation"""
    messages = [
        {
            'role': 'system',
            'content': 'You are a helpful AI assistant specialized in Python programming.'
        },
        {
            'role': 'user',
            'content': 'How do I read a CSV file in Python?'
        }
    ]

    response = ollama.chat(
        model='llama3.2',
        messages=messages
    )

    print(response['message']['content'])

    # Continue conversation
    messages.append(response['message'])
    messages.append({
        'role': 'user',
        'content': 'Can you show me an example with error handling?'
    })

    response = ollama.chat(
        model='llama3.2',
        messages=messages
    )

    print(response['message']['content'])
```

### Streaming Chat

```python
def chat_stream(messages: list[dict], model: str = 'llama3.2'):
    """Chat with streaming"""
    stream = ollama.chat(
        model=model,
        messages=messages,
        stream=True
    )

    full_response = ""
    for chunk in stream:
        content = chunk['message']['content']
        print(content, end='', flush=True)
        full_response += content

    return full_response
```

## Advanced Features

### Embeddings

```python
import ollama
import numpy as np

def get_embeddings(text: str, model: str = 'nomic-embed-text') -> list[float]:
    """Generate embeddings for text"""
    response = ollama.embed(
        model=model,
        input=text
    )
    return response['embeddings'][0]

# Calculate similarity
def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    """Calculate cosine similarity between vectors"""
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# Usage
text1 = "Machine learning is a subset of AI"
text2 = "AI includes machine learning techniques"
text3 = "I like pizza"

emb1 = get_embeddings(text1)
emb2 = get_embeddings(text2)
emb3 = get_embeddings(text3)

print(f"Similarity 1-2: {cosine_similarity(emb1, emb2):.3f}")
print(f"Similarity 1-3: {cosine_similarity(emb1, emb3):.3f}")
```

### Vision Models

```python
import ollama

def analyze_image(image_path: str, prompt: str = "Describe this image"):
    """Analyze image with vision model"""
    with open(image_path, 'rb') as f:
        image_data = f.read()

    response = ollama.generate(
        model='llava',
        prompt=prompt,
        images=[image_data]
    )

    return response['response']

# Usage
description = analyze_image('photo.jpg', 'What objects are in this image?')
print(description)
```

## Async Implementation

### Async Client

```python
import asyncio
import ollama

async def async_generate(prompt: str, model: str = 'llama3.2'):
    """Async text generation"""
    response = await ollama.AsyncClient().generate(
        model=model,
        prompt=prompt
    )
    return response['response']

async def async_chat(messages: list[dict], model: str = 'llama3.2'):
    """Async chat"""
    response = await ollama.AsyncClient().chat(
        model=model,
        messages=messages
    )
    return response['message']['content']

# Run async code
async def main():
    result = await async_generate("Explain async programming in Python")
    print(result)

asyncio.run(main())
```

### Concurrent Requests

```python
import asyncio
import ollama

async def process_batch(prompts: list[str], model: str = 'llama3.2'):
    """Process multiple prompts concurrently"""
    client = ollama.AsyncClient()

    async def process_one(prompt: str):
        response = await client.generate(model=model, prompt=prompt)
        return response['response']

    tasks = [process_one(prompt) for prompt in prompts]
    results = await asyncio.gather(*tasks)
    return results

# Usage
async def main():
    prompts = [
        "What is Python?",
        "What is JavaScript?",
        "What is Rust?"
    ]
    results = await process_batch(prompts)
    for prompt, result in zip(prompts, results):
        print(f"\nPrompt: {prompt}")
        print(f"Response: {result[:100]}...")

asyncio.run(main())
```

## Model Management

### List and Pull Models

```python
import ollama

# List installed models
models = ollama.list()
for model in models['models']:
    print(f"Name: {model['name']}")
    print(f"Size: {model['size'] / 1e9:.2f} GB")
    print(f"Modified: {model['modified_at']}")
    print()

# Pull a new model
ollama.pull('llama3.2')
ollama.pull('codellama')
ollama.pull('mistral')

# Check if model exists
def model_exists(model_name: str) -> bool:
    """Check if model is installed"""
    models = ollama.list()
    return any(m['name'] == model_name for m in models['models'])
```

### Show Model Information

```python
# Get model details
info = ollama.show('llama3.2')
print(f"Model: {info['modelfile']}")
print(f"Parameters: {info['parameters']}")
print(f"Template: {info['template']}")
```

### Delete Models

```python
# Delete a model
ollama.delete('old-model')
```

## Custom Models and Modelfiles

### Create Custom Model

```python
# Create Modelfile
modelfile = """
FROM llama3.2

PARAMETER temperature 0.8
PARAMETER top_p 0.9
PARAMETER top_k 40

SYSTEM You are a Python expert assistant. You provide clear, concise code examples with explanations.
"""

# Save Modelfile
with open('Modelfile', 'w') as f:
    f.write(modelfile)

# Create custom model
ollama.create(model='python-expert', modelfile=modelfile)
```

### Advanced Modelfile

```python
modelfile = """
FROM codellama

# Parameters
PARAMETER temperature 0.7
PARAMETER num_predict 2000
PARAMETER stop "```"

# System prompt
SYSTEM You are an expert software engineer specialized in writing clean, efficient, and well-documented code. Always include type hints and docstrings.

# Template
TEMPLATE \"\"\"
{{ if .System }}System: {{ .System }}{{ end }}
{{ if .Prompt }}User: {{ .Prompt }}{{ end }}
Assistant:
\"\"\"
"""

ollama.create(model='code-assistant', modelfile=modelfile)
```

## Production Integration

### FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import ollama
from typing import Optional

app = FastAPI(title="Ollama API")

class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    model: str = Field(default='llama3.2')
    temperature: float = Field(default=0.7, ge=0, le=2)
    max_tokens: Optional[int] = Field(None, ge=1)

class GenerateResponse(BaseModel):
    response: str
    model: str
    total_duration: int

@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    """Generate text completion"""
    try:
        response = await ollama.AsyncClient().generate(
            model=request.model,
            prompt=request.prompt,
            options={
                'temperature': request.temperature,
                'num_predict': request.max_tokens or 500
            }
        )

        return GenerateResponse(
            response=response['response'],
            model=response['model'],
            total_duration=response['total_duration']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class ChatMessage(BaseModel):
    role: str = Field(..., pattern="^(system|user|assistant)$")
    content: str

class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    model: str = Field(default='llama3.2')
    stream: bool = Field(default=False)

@app.post("/chat")
async def chat(request: ChatRequest):
    """Chat completion"""
    try:
        messages = [msg.dict() for msg in request.messages]

        if request.stream:
            from fastapi.responses import StreamingResponse

            async def generate_stream():
                stream = await ollama.AsyncClient().chat(
                    model=request.model,
                    messages=messages,
                    stream=True
                )
                async for chunk in stream:
                    yield chunk['message']['content']

            return StreamingResponse(
                generate_stream(),
                media_type='text/event-stream'
            )
        else:
            response = await ollama.AsyncClient().chat(
                model=request.model,
                messages=messages
            )
            return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models")
async def list_models():
    """List available models"""
    try:
        models = ollama.list()
        return models
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### RAG (Retrieval Augmented Generation)

```python
import ollama
from typing import List
import numpy as np

class SimpleRAG:
    """Simple RAG implementation with Ollama"""

    def __init__(self, model: str = 'llama3.2', embed_model: str = 'nomic-embed-text'):
        self.model = model
        self.embed_model = embed_model
        self.documents = []
        self.embeddings = []

    def add_document(self, text: str):
        """Add document to knowledge base"""
        embedding = ollama.embed(model=self.embed_model, input=text)
        self.documents.append(text)
        self.embeddings.append(embedding['embeddings'][0])

    def add_documents(self, texts: List[str]):
        """Add multiple documents"""
        for text in texts:
            self.add_document(text)

    def search(self, query: str, top_k: int = 3) -> List[str]:
        """Search for relevant documents"""
        query_embedding = ollama.embed(
            model=self.embed_model,
            input=query
        )['embeddings'][0]

        # Calculate similarities
        similarities = []
        for doc_embedding in self.embeddings:
            similarity = np.dot(query_embedding, doc_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
            )
            similarities.append(similarity)

        # Get top k documents
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        return [self.documents[i] for i in top_indices]

    def query(self, question: str, top_k: int = 3) -> str:
        """Query with RAG"""
        # Retrieve relevant documents
        relevant_docs = self.search(question, top_k)

        # Create context
        context = "\n\n".join(relevant_docs)

        # Generate response
        prompt = f"""Based on the following context, answer the question.

Context:
{context}

Question: {question}

Answer:"""

        response = ollama.generate(
            model=self.model,
            prompt=prompt
        )

        return response['response']

# Usage
rag = SimpleRAG()

# Add knowledge
documents = [
    "Python is a high-level programming language known for its simplicity.",
    "FastAPI is a modern web framework for building APIs with Python.",
    "Ollama allows running large language models locally on your machine.",
]

rag.add_documents(documents)

# Query
answer = rag.query("What is FastAPI?")
print(answer)
```

## Error Handling and Retry Logic

```python
import ollama
import time
from functools import wraps

def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """Retry decorator for Ollama operations"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except ollama.ResponseError as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(delay * (2 ** attempt))
                    else:
                        raise
        return wrapper
    return decorator

@retry_on_failure(max_retries=3)
def generate_with_retry(prompt: str, model: str = 'llama3.2'):
    """Generate with automatic retry"""
    return ollama.generate(model=model, prompt=prompt)
```

## Performance Optimization

### Batch Processing

```python
def batch_process(prompts: List[str], batch_size: int = 5, model: str = 'llama3.2'):
    """Process prompts in batches"""
    results = []

    for i in range(0, len(prompts), batch_size):
        batch = prompts[i:i + batch_size]
        print(f"Processing batch {i//batch_size + 1}...")

        for prompt in batch:
            response = ollama.generate(model=model, prompt=prompt)
            results.append(response['response'])

    return results
```

### Model Warmup

```python
def warmup_model(model: str = 'llama3.2'):
    """Warm up model for faster subsequent requests"""
    print(f"Warming up {model}...")
    ollama.generate(
        model=model,
        prompt="Hello",
        options={'num_predict': 1}
    )
    print("Model ready!")
```

## Best Available Models

### Recommended Models by Use Case

```python
RECOMMENDED_MODELS = {
    'general': 'llama3.2',           # Best general purpose
    'coding': 'codellama',            # Code generation
    'fast': 'llama3.2:1b',           # Fast, small model
    'quality': 'llama3.2:70b',       # High quality, slow
    'vision': 'llava',                # Image understanding
    'embeddings': 'nomic-embed-text', # Text embeddings
    'chat': 'mistral',                # Conversational
    'instruction': 'llama3.2',        # Instruction following
}

def get_model_for_task(task: str) -> str:
    """Get recommended model for task"""
    return RECOMMENDED_MODELS.get(task, 'llama3.2')
```

## Monitoring and Logging

```python
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_with_logging(prompt: str, model: str = 'llama3.2'):
    """Generate with comprehensive logging"""
    start_time = datetime.now()

    logger.info(f"Starting generation with {model}")
    logger.info(f"Prompt: {prompt[:100]}...")

    try:
        response = ollama.generate(model=model, prompt=prompt)

        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"Generation completed in {duration:.2f}s")
        logger.info(f"Response length: {len(response['response'])} chars")

        return response['response']

    except Exception as e:
        logger.error(f"Generation failed: {e}")
        raise
```

## Key Principles

1. **Use streaming for long responses** - Better UX
2. **Implement retry logic** - Handle transient failures
3. **Warm up models** - Faster first response
4. **Choose appropriate models** - Balance speed vs quality
5. **Use async for concurrent requests** - Better performance
6. **Monitor resource usage** - Ollama is resource-intensive
7. **Cache embeddings** - Avoid recomputing
8. **Set reasonable timeouts** - Prevent hanging requests
9. **Log comprehensively** - Debug production issues
10. **Handle errors gracefully** - Provide fallbacks

## Resources

- Ollama: https://ollama.com/
- Ollama GitHub: https://github.com/ollama/ollama
- Python Library: https://github.com/ollama/ollama-python
- Model Library: https://ollama.com/library
- API Documentation: https://github.com/ollama/ollama/blob/main/docs/api.md
