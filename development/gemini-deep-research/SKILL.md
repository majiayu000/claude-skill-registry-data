---
name: gemini-deep-research
description: Build Gemini Deep Research agents using the Interactions API. Use when creating autonomous research agents, implementing multi-step information gathering, building research report generators, or integrating Gemini's Deep Research capabilities into applications. Handles polling, streaming, file integration, and report synthesis.
---

# Gemini Deep Research Agent Builder

Build autonomous research agents using Google's Gemini Deep Research API (Interactions API). This skill enables creation of agents that can conduct comprehensive web research, analyze documents, and generate detailed reports with citations.

## Prerequisites

Before building a Gemini Deep Research agent:

1. **API Key**: Obtain a Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)
2. **Python SDK**: Install the Google GenAI SDK:
   ```bash
   pip install google-genai
   ```
3. **Environment Variable**: Set your API key:
   ```bash
   export GEMINI_API_KEY="your-api-key"
   ```

## Core Concepts

### Interactions API vs generate_content

Deep Research is ONLY accessible via the **Interactions API**, NOT through `generate_content()`. The Interactions API provides:
- Long-running async task execution
- Background processing with polling
- Streaming with reconnection support
- Multi-turn research conversations

### Agent Identifier

Always use: `agent='deep-research-pro-preview-12-2025'`

### Research Flow

1. **Submit Query** → Create interaction with `background=True`
2. **Poll/Stream** → Monitor status until completion
3. **Retrieve Results** → Extract synthesized report from outputs

## Implementation Patterns

### Pattern 1: Basic Polling (Simplest)

```python
import time
from google import genai

client = genai.Client()

def research(query: str) -> str:
    """Execute a deep research task with polling."""
    interaction = client.interactions.create(
        input=query,
        agent='deep-research-pro-preview-12-2025',
        background=True
    )

    while True:
        interaction = client.interactions.get(interaction.id)
        if interaction.status == "completed":
            return interaction.outputs[-1].text
        elif interaction.status == "failed":
            raise Exception(f"Research failed: {interaction.error}")
        time.sleep(10)  # Poll every 10 seconds
```

### Pattern 2: Streaming with Thinking Summaries

```python
from google import genai

client = genai.Client()

def research_streaming(query: str):
    """Stream research results with intermediate thinking."""
    stream = client.interactions.create(
        input=query,
        agent='deep-research-pro-preview-12-2025',
        background=True,
        stream=True,
        agent_config={
            "type": "deep-research",
            "thinking_summaries": "auto"
        }
    )

    for event in stream:
        if event.event_type == "content.delta":
            if hasattr(event, 'delta') and hasattr(event.delta, 'text'):
                yield event.delta.text
        elif event.event_type == "interaction.complete":
            break
        elif event.event_type == "error":
            raise Exception(f"Stream error: {event}")
```

### Pattern 3: Robust Streaming with Reconnection

```python
import time
from google import genai

client = genai.Client()

def research_with_reconnection(query: str) -> str:
    """Stream research with automatic reconnection on disconnect."""
    last_event_id = None
    interaction_id = None
    is_complete = False
    result_text = []

    def process_stream(event_stream):
        nonlocal last_event_id, interaction_id, is_complete
        for event in event_stream:
            if event.event_type == "interaction.start":
                interaction_id = event.interaction.id
            if event.event_id:
                last_event_id = event.event_id
            if event.event_type == "content.delta":
                if hasattr(event, 'delta') and hasattr(event.delta, 'text'):
                    result_text.append(event.delta.text)
            if event.event_type in ['interaction.complete', 'error']:
                is_complete = True

    # Initial stream
    try:
        stream = client.interactions.create(
            input=query,
            agent='deep-research-pro-preview-12-2025',
            background=True,
            stream=True,
            agent_config={"type": "deep-research", "thinking_summaries": "auto"}
        )
        process_stream(stream)
    except Exception as e:
        print(f"Initial connection dropped: {e}")

    # Reconnection loop
    while not is_complete and interaction_id:
        time.sleep(2)
        try:
            resume_stream = client.interactions.get(
                id=interaction_id,
                stream=True,
                last_event_id=last_event_id
            )
            process_stream(resume_stream)
        except Exception as e:
            print(f"Reconnection failed: {e}")
            continue

    return "".join(result_text)
```

### Pattern 4: Multi-Turn Research Conversation

```python
from google import genai

client = genai.Client()

def research_conversation(queries: list[str]) -> list[str]:
    """Conduct multi-turn research, building on previous context."""
    results = []
    previous_id = None

    for query in queries:
        params = {
            "input": query,
            "agent": 'deep-research-pro-preview-12-2025',
            "background": True
        }

        if previous_id:
            params["previous_interaction_id"] = previous_id

        interaction = client.interactions.create(**params)

        # Poll for completion
        import time
        while True:
            interaction = client.interactions.get(interaction.id)
            if interaction.status == "completed":
                results.append(interaction.outputs[-1].text)
                previous_id = interaction.id
                break
            elif interaction.status == "failed":
                raise Exception(f"Research failed: {interaction.error}")
            time.sleep(10)

    return results
```

### Pattern 5: File-Enhanced Research

```python
from google import genai

client = genai.Client()

def research_with_files(query: str, file_store_name: str) -> str:
    """Research combining web search with uploaded documents."""
    interaction = client.interactions.create(
        input=query,
        agent='deep-research-pro-preview-12-2025',
        background=True,
        tools=[{
            "type": "file_search",
            "file_search_store_names": [f'fileSearchStores/{file_store_name}']
        }]
    )

    import time
    while True:
        interaction = client.interactions.get(interaction.id)
        if interaction.status == "completed":
            return interaction.outputs[-1].text
        elif interaction.status == "failed":
            raise Exception(f"Research failed: {interaction.error}")
        time.sleep(10)
```

## Building a Complete Research Agent

### Full Agent Class

```python
import time
from dataclasses import dataclass
from typing import Generator, Optional
from google import genai

@dataclass
class ResearchConfig:
    """Configuration for research agent."""
    poll_interval: int = 10
    max_wait_time: int = 3600  # 60 minutes max
    thinking_summaries: str = "auto"

class GeminiDeepResearchAgent:
    """Autonomous research agent using Gemini Deep Research."""

    AGENT_ID = 'deep-research-pro-preview-12-2025'

    def __init__(self, api_key: Optional[str] = None, config: Optional[ResearchConfig] = None):
        self.client = genai.Client(api_key=api_key) if api_key else genai.Client()
        self.config = config or ResearchConfig()
        self.conversation_id: Optional[str] = None

    def research(self, query: str, continue_conversation: bool = False) -> str:
        """Execute synchronous research with polling."""
        params = self._build_params(query, continue_conversation)
        interaction = self.client.interactions.create(**params)
        return self._poll_for_completion(interaction)

    def research_stream(self, query: str) -> Generator[str, None, None]:
        """Stream research results in real-time."""
        params = self._build_params(query, False)
        params["stream"] = True
        params["agent_config"] = {
            "type": "deep-research",
            "thinking_summaries": self.config.thinking_summaries
        }

        stream = self.client.interactions.create(**params)
        for event in stream:
            if event.event_type == "interaction.start":
                self.conversation_id = event.interaction.id
            if event.event_type == "content.delta":
                if hasattr(event, 'delta') and hasattr(event.delta, 'text'):
                    yield event.delta.text
            if event.event_type in ['interaction.complete', 'error']:
                break

    def research_with_context(self, query: str, file_stores: list[str]) -> str:
        """Research with file context."""
        params = self._build_params(query, False)
        params["tools"] = [{
            "type": "file_search",
            "file_search_store_names": [f'fileSearchStores/{store}' for store in file_stores]
        }]
        interaction = self.client.interactions.create(**params)
        return self._poll_for_completion(interaction)

    def _build_params(self, query: str, continue_conversation: bool) -> dict:
        params = {
            "input": query,
            "agent": self.AGENT_ID,
            "background": True
        }
        if continue_conversation and self.conversation_id:
            params["previous_interaction_id"] = self.conversation_id
        return params

    def _poll_for_completion(self, interaction) -> str:
        elapsed = 0
        while elapsed < self.config.max_wait_time:
            interaction = self.client.interactions.get(interaction.id)
            if interaction.status == "completed":
                self.conversation_id = interaction.id
                return interaction.outputs[-1].text
            elif interaction.status == "failed":
                raise Exception(f"Research failed: {interaction.error}")
            time.sleep(self.config.poll_interval)
            elapsed += self.config.poll_interval
        raise TimeoutError(f"Research exceeded {self.config.max_wait_time}s timeout")
```

### Usage Example

```python
# Initialize agent
agent = GeminiDeepResearchAgent()

# Simple research
report = agent.research("What are the latest developments in quantum computing?")
print(report)

# Streaming research
for chunk in agent.research_stream("Analyze the current state of AI regulation"):
    print(chunk, end="", flush=True)

# Multi-turn conversation
initial = agent.research("Explain CRISPR gene editing technology")
followup = agent.research("What are the ethical concerns?", continue_conversation=True)
```

## API Reference

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `input` | string | Yes | Research query/prompt |
| `agent` | string | Yes | Must be `deep-research-pro-preview-12-2025` |
| `background` | boolean | Yes | Must be `True` for async execution |
| `stream` | boolean | No | Enable real-time streaming |
| `agent_config` | object | No | `{"type": "deep-research", "thinking_summaries": "auto"}` |
| `previous_interaction_id` | string | No | Continue from prior research |
| `tools` | array | No | Include `file_search` for document context |

### Response Status Values

| Status | Description |
|--------|-------------|
| `in_progress` | Research actively running |
| `completed` | Task finished successfully |
| `failed` | Task encountered error |

### Stream Event Types

| Event Type | Description |
|------------|-------------|
| `interaction.start` | Contains `interaction.id` for tracking |
| `content.delta` | Text chunks or thinking summaries |
| `interaction.complete` | Research finished |
| `error` | Operation failed |

## Constraints & Limitations

- **Maximum Runtime**: 60 minutes per research task
- **Background Required**: `background=True` is mandatory
- **No Audio**: Audio inputs not supported
- **No Custom Tools**: Function calling tools unavailable
- **No Human Approval**: Automated planning only
- **Pricing**: $2 per million input tokens

## Best Practices

1. **Handle Long Waits**: Research can take 5-30 minutes; implement proper timeout handling
2. **Use Streaming**: For user-facing apps, stream results for better UX
3. **Implement Reconnection**: Network drops are common; always support resume
4. **Leverage Multi-Turn**: Build on previous research for deeper analysis
5. **Combine with Files**: Upload relevant documents to enhance research context
6. **Monitor Costs**: Track token usage, especially for frequent research tasks

## Troubleshooting

### Common Issues

**"Agent not found"**
- Verify agent ID is exactly `deep-research-pro-preview-12-2025`

**"Invalid request"**
- Ensure `background=True` is set
- Don't use `generate_content()` - use Interactions API only

**Timeout Errors**
- Increase poll interval for complex queries
- Implement reconnection logic for streams

**Empty Results**
- Check `interaction.outputs[-1].text` exists
- Verify research completed (not just started)
