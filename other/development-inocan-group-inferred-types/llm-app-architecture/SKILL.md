---
name: llm-app-architecture
description: Automatically applies when building LLM applications. Ensures proper async patterns for LLM calls, streaming responses, token management, retry logic, and error handling.
category: ai-llm
---

# LLM Application Architecture Patterns

When building applications with LLM APIs (Claude, OpenAI, etc.), follow these patterns for reliable, efficient, and maintainable systems.

**Trigger Keywords**: LLM, AI application, model API, Claude, OpenAI, GPT, language model, LLM call, completion, chat completion, embeddings

**Agent Integration**: Used by `ml-system-architect`, `llm-app-engineer`, `agent-orchestrator-engineer`, `rag-architect`, `performance-and-cost-engineer-llm`

## ✅ Correct Pattern: Async LLM Calls

```python
import httpx
import anthropic
from typing import AsyncIterator
import asyncio

class LLMClient:
    """Async LLM client with proper error handling."""

    def __init__(self, api_key: str, timeout: int = 60):
        self.client = anthropic.AsyncAnthropic(
            api_key=api_key,
            timeout=httpx.Timeout(timeout, connect=5.0)
        )
        self.model = "claude-sonnet-4-20250514"

    async def complete(
        self,
        prompt: str,
        system: str | None = None,
        max_tokens: int = 1024,
        temperature: float = 1.0
    ) -> str:
        """
        Generate completion from LLM.

        Args:
            prompt: User message content
            system: Optional system prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0-1)

        Returns:
            Generated text response

        Raises:
            LLMError: If API call fails
        """
        try:
            message = await self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system if system else anthropic.NOT_GIVEN,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text

        except anthropic.APITimeoutError as e:
            raise LLMTimeoutError("LLM request timed out") from e
        except anthropic.APIConnectionError as e:
            raise LLMConnectionError("Failed to connect to LLM API") from e
        except anthropic.RateLimitError as e:
            raise LLMRateLimitError("Rate limit exceeded") from e
        except anthropic.APIStatusError as e:
            raise LLMError(f"LLM API error: {e.status_code}") from e


# Custom exceptions
class LLMError(Exception):
    """Base LLM error."""
    pass


class LLMTimeoutError(LLMError):
    """LLM request timeout."""
    pass


class LLMConnectionError(LLMError):
    """LLM connection error."""
    pass


class LLMRateLimitError(LLMError):
    """LLM rate limit exceeded."""
    pass
```

## Streaming Responses

```python
from typing import AsyncIterator

async def stream_completion(
    self,
    prompt: str,
    system: str | None = None,
    max_tokens: int = 1024
) -> AsyncIterator[str]:
    """
    Stream completion from LLM token by token.

    Yields:
        Individual text chunks as they arrive

    Usage:
        async for chunk in client.stream_completion("Hello"):
            print(chunk, end="", flush=True)
    """
    try:
        async with self.client.messages.stream(
            model=self.model,
            max_tokens=max_tokens,
            system=system if system else anthropic.NOT_GIVEN,
            messages=[{"role": "user", "content": prompt}]
        ) as stream:
            async for text in stream.text_stream:
                yield text

    except anthropic.APIError as e:
        raise LLMError(f"Streaming error: {str(e)}") from e


# Use in FastAPI endpoint
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post("/stream")
async def stream_endpoint(prompt: str) -> StreamingResponse:
    """Stream LLM response to client."""
    client = LLMClient(api_key=settings.anthropic_api_key)

    async def generate():
        async for chunk in client.stream_completion(prompt):
            yield chunk

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )
```

## Token Counting and Management

```python
from anthropic import Anthropic
from typing import List, Dict

class TokenCounter:
    """Token counting utilities for LLM calls."""

    def __init__(self):
        self.client = Anthropic()

    def count_tokens(self, text: str) -> int:
        """
        Count tokens in text using Claude's tokenizer.

        Args:
            text: Input text to count

        Returns:
            Number of tokens
        """
        return self.client.count_tokens(text)

    def count_message_tokens(
        self,
        messages: List[Dict[str, str]],
        system: str | None = None
    ) -> int:
        """
        Count tokens for a full message exchange.

        Args:
            messages: List of message dicts with role and content
            system: Optional system prompt

        Returns:
            Total token count including message formatting overhead
        """
        total = 0

        # System prompt
        if system:
            total += self.count_tokens(system)

        # Messages (include role tokens)
        for msg in messages:
            total += self.count_tokens(msg["content"])
            total += 4  # Overhead for role and formatting

        return total

    def estimate_cost(
        self,
        input_tokens: int,
        output_tokens: int,
        model: str = "claude-sonnet-4-20250514"
    ) -> float:
        """
        Estimate cost for LLM call.

        Args:
            input_tokens: Input token count
            output_tokens: Output token count
            model: Model name

        Returns:
            Estimated cost in USD
        """
        # Pricing as of 2025 (update as needed)
        pricing = {
            "claude-sonnet-4-20250514": {
                "input": 3.00 / 1_000_000,   # $3/MTok
                "output": 15.00 / 1_000_000  # $15/MTok
            },
            "claude-opus-4-20250514": {
                "input": 15.00 / 1_000_000,
                "output": 75.00 / 1_000_000
            },
            "claude-haiku-3-5-20250514": {
                "input": 0.80 / 1_000_000,
                "output": 4.00 / 1_000_000
            }
        }

        rates = pricing.get(model, pricing["claude-sonnet-4-20250514"])
        return (input_tokens * rates["input"]) + (output_tokens * rates["output"])
```

## Retry Logic with Exponential Backoff

```python
import asyncio
from typing import TypeVar, Callable, Any
from functools import wraps
import random

T = TypeVar('T')


def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True
):
    """
    Retry decorator with exponential backoff for LLM calls.

    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        exponential_base: Base for exponential calculation
        jitter: Add random jitter to prevent thundering herd
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)

                except (LLMTimeoutError, LLMConnectionError, LLMRateLimitError) as e:
                    last_exception = e

                    if attempt == max_retries:
                        raise

                    # Calculate delay with exponential backoff
                    delay = min(
                        base_delay * (exponential_base ** attempt),
                        max_delay
                    )

                    # Add jitter
                    if jitter:
                        delay *= (0.5 + random.random() * 0.5)

                    await asyncio.sleep(delay)

            raise last_exception

        return wrapper
    return decorator


class RobustLLMClient(LLMClient):
    """LLM client with automatic retries."""

    @retry_with_backoff(max_retries=3, base_delay=1.0)
    async def complete(self, prompt: str, **kwargs) -> str:
        """Complete with automatic retries."""
        return await super().complete(prompt, **kwargs)
```

## Caching and Prompt Optimization

```python
from functools import lru_cache
import hashlib
from typing import Optional

class CachedLLMClient(LLMClient):
    """LLM client with response caching."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cache: dict[str, str] = {}

    def _cache_key(self, prompt: str, system: str | None = None) -> str:
        """Generate cache key from prompt and system."""
        content = f"{system or ''}||{prompt}"
        return hashlib.sha256(content.encode()).hexdigest()

    async def complete(
        self,
        prompt: str,
        system: str | None = None,
        use_cache: bool = True,
        **kwargs
    ) -> str:
        """Complete with caching support."""
        if use_cache:
            cache_key = self._cache_key(prompt, system)
            if cache_key in self._cache:
                return self._cache[cache_key]

        response = await super().complete(prompt, system=system, **kwargs)

        if use_cache:
            self._cache[cache_key] = response

        return response

    def clear_cache(self):
        """Clear response cache."""
        self._cache.clear()


# Use Claude prompt caching for repeated system prompts
async def complete_with_prompt_caching(
    self,
    prompt: str,
    system: str,
    max_tokens: int = 1024
) -> str:
    """
    Use Claude's prompt caching for repeated system prompts.

    Caches system prompt on Claude's servers for 5 minutes,
    reducing cost for repeated calls with same system prompt.
    """
    message = await self.client.messages.create(
        model=self.model,
        max_tokens=max_tokens,
        system=[
            {
                "type": "text",
                "text": system,
                "cache_control": {"type": "ephemeral"}  # Cache this
            }
        ],
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text
```

## Batch Processing

```python
from typing import List
import asyncio

async def batch_complete(
    self,
    prompts: List[str],
    system: str | None = None,
    max_concurrent: int = 5
) -> List[str]:
    """
    Process multiple prompts concurrently with concurrency limit.

    Args:
        prompts: List of prompts to process
        system: Optional system prompt
        max_concurrent: Maximum concurrent requests

    Returns:
        List of responses in same order as prompts
    """
    semaphore = asyncio.Semaphore(max_concurrent)

    async def process_one(prompt: str) -> str:
        async with semaphore:
            return await self.complete(prompt, system=system)

    tasks = [process_one(p) for p in prompts]
    return await asyncio.gather(*tasks)


# Example usage
async def process_documents():
    """Process multiple documents with LLM."""
    client = LLMClient(api_key=settings.anthropic_api_key)
    documents = ["doc1 text", "doc2 text", "doc3 text"]

    # Process in batches of 5
    results = await client.batch_complete(
        prompts=documents,
        system="Summarize this document in 2 sentences.",
        max_concurrent=5
    )

    return results
```

## Observability and Logging

```python
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class ObservableLLMClient(LLMClient):
    """LLM client with comprehensive logging."""

    async def complete(self, prompt: str, **kwargs) -> str:
        """Complete with observability."""
        request_id = str(uuid.uuid4())
        start_time = datetime.utcnow()

        # Log request (redact if needed)
        logger.info(
            "LLM request started",
            extra={
                "request_id": request_id,
                "model": self.model,
                "prompt_length": len(prompt),
                "max_tokens": kwargs.get("max_tokens", 1024),
                "temperature": kwargs.get("temperature", 1.0)
            }
        )

        try:
            response = await super().complete(prompt, **kwargs)

            # Count tokens
            counter = TokenCounter()
            input_tokens = counter.count_tokens(prompt)
            output_tokens = counter.count_tokens(response)
            cost = counter.estimate_cost(input_tokens, output_tokens, self.model)

            # Log success
            duration = (datetime.utcnow() - start_time).total_seconds()
            logger.info(
                "LLM request completed",
                extra={
                    "request_id": request_id,
                    "duration_seconds": duration,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": input_tokens + output_tokens,
                    "estimated_cost_usd": cost,
                    "response_length": len(response)
                }
            )

            return response

        except Exception as e:
            # Log error
            duration = (datetime.utcnow() - start_time).total_seconds()
            logger.error(
                "LLM request failed",
                extra={
                    "request_id": request_id,
                    "duration_seconds": duration,
                    "error_type": type(e).__name__,
                    "error_message": str(e)
                },
                exc_info=True
            )
            raise
```

## ❌ Anti-Patterns

```python
# ❌ Synchronous API calls in async code
def complete(prompt: str) -> str:  # Should be async!
    response = anthropic.Anthropic().messages.create(...)
    return response.content[0].text

# ✅ Better: Use async client
async def complete(prompt: str) -> str:
    async_client = anthropic.AsyncAnthropic()
    response = await async_client.messages.create(...)
    return response.content[0].text


# ❌ No timeout
client = anthropic.AsyncAnthropic()  # No timeout!

# ✅ Better: Set reasonable timeout
client = anthropic.AsyncAnthropic(
    timeout=httpx.Timeout(60.0, connect=5.0)
)


# ❌ No error handling
async def complete(prompt: str) -> str:
    response = await client.messages.create(...)  # Can fail!
    return response.content[0].text

# ✅ Better: Handle specific errors
async def complete(prompt: str) -> str:
    try:
        response = await client.messages.create(...)
        return response.content[0].text
    except anthropic.RateLimitError:
        # Handle rate limit
        raise LLMRateLimitError("Rate limit exceeded")
    except anthropic.APITimeoutError:
        # Handle timeout
        raise LLMTimeoutError("Request timed out")


# ❌ No token tracking
async def complete(prompt: str) -> str:
    return await client.messages.create(...)  # No idea of cost!

# ✅ Better: Track tokens and cost
async def complete(prompt: str) -> str:
    response = await client.messages.create(...)
    logger.info(
        "LLM call",
        extra={
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
            "cost": estimate_cost(response.usage)
        }
    )
    return response.content[0].text


# ❌ Sequential processing
async def process_many(prompts: List[str]) -> List[str]:
    results = []
    for prompt in prompts:  # Sequential!
        result = await complete(prompt)
        results.append(result)
    return results

# ✅ Better: Concurrent processing with limits
async def process_many(prompts: List[str]) -> List[str]:
    semaphore = asyncio.Semaphore(5)  # Max 5 concurrent

    async def process_one(prompt):
        async with semaphore:
            return await complete(prompt)

    return await asyncio.gather(*[process_one(p) for p in prompts])
```

## Best Practices Checklist

- ✅ Use async/await for all LLM API calls
- ✅ Set reasonable timeouts (30-60 seconds)
- ✅ Implement retry logic with exponential backoff
- ✅ Handle specific API exceptions (rate limit, timeout, connection)
- ✅ Track token usage and estimated cost
- ✅ Log all LLM calls with request IDs
- ✅ Use streaming for long responses
- ✅ Implement prompt caching for repeated system prompts
- ✅ Process multiple requests concurrently with semaphores
- ✅ Redact sensitive data in logs
- ✅ Set max_tokens to prevent runaway costs
- ✅ Use appropriate temperature for task (0 for deterministic, 1 for creative)

## Auto-Apply

When making LLM API calls:
1. Use async client (AsyncAnthropic, AsyncOpenAI)
2. Add timeout configuration
3. Implement retry logic for transient errors
4. Track tokens and cost
5. Log requests with structured logging
6. Use streaming for real-time responses
7. Handle rate limits gracefully

## Related Skills

- `async-await-checker` - For async/await patterns
- `structured-errors` - For error handling
- `observability-logging` - For logging and tracing
- `pydantic-models` - For request/response validation
- `fastapi-patterns` - For building LLM API endpoints
