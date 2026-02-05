---
name: streaming-patterns
description: Configure ADK bidi-streaming for real-time multimodal interactions. Use when building live voice/video agents, implementing real-time streaming, configuring LiveRequestQueue, setting up audio/video processing, or when user mentions bidi-streaming, real-time agents, streaming tools, multimodal streaming, or Gemini Live API.
allowed-tools: Read, Write, Bash
---

# ADK Streaming Patterns

Comprehensive patterns for configuring Google ADK bidi-streaming (bidirectional streaming) to build real-time, multimodal AI agents with voice, video, and streaming tool capabilities.

## Core Concepts

ADK bidi-streaming enables low-latency, bidirectional communication between users and AI agents with:

- **Real-time interaction**: Process and respond while user is still providing input
- **Natural interruption**: User can interrupt agent mid-response
- **Multimodal support**: Text, audio, and video inputs/outputs
- **Streaming tools**: Tools that yield intermediate results over time
- **Session persistence**: Maintain context across ~10-minute connection timeouts

## Quick Start Patterns

### 1. Basic Bidi-Streaming Setup

```python
from google.adk.agents import Agent
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.genai import types

# Configure for audio streaming
run_config = RunConfig(
    response_modalities=["AUDIO"],
    streaming_mode=StreamingMode.BIDI
)

# Run agent with bidi-streaming
async for event in agent.run_live(request_queue, run_config=run_config):
    if event.server_content:
        # Handle streaming response
        handle_response(event)
```

### 2. LiveRequestQueue Pattern

```python
from google.adk.agents import LiveRequestQueue

# Create queue for multimodal inputs
request_queue = LiveRequestQueue()

# Enqueue text
await request_queue.put("What's the weather?")

# Enqueue audio chunks
await request_queue.put(audio_bytes)

# Signal activity boundaries
await request_queue.put(types.LiveClientRealtimeInput(
    media_chunks=[types.LiveClientRealtimeInputMediaChunk(
        data=audio_chunk
    )]
))
```

## Configuration Patterns

### Response Modalities

**CRITICAL**: Only ONE response modality per session. Cannot switch mid-session.

```python
# Audio output (voice agent)
RunConfig(response_modalities=["AUDIO"])

# Text output (chat agent)
RunConfig(response_modalities=["TEXT"])
```

### Session Management

**Session Resumption** (automatic reconnection):

```python
RunConfig(
    session_resumption=types.SessionResumptionConfig()
)
```

**Context Window Compression** (unlimited sessions):

```python
RunConfig(
    context_window_compression=types.ContextWindowCompressionConfig(
        trigger_tokens=100000,
        sliding_window=types.SlidingWindow(target_tokens=80000)
    )
)
```

### Audio Configuration

See templates/audio-config.py for speech and transcription settings.

### Platform Selection

Use environment variable (no code changes needed):

```bash
# Google AI Studio (Gemini Live API)
export GOOGLE_GENAI_USE_VERTEXAI=FALSE

# Vertex AI (Live API)
export GOOGLE_GENAI_USE_VERTEXAI=TRUE
```

## Streaming Tools Pattern

Define tools as async generators for continuous results:

```python
@streaming_tool
async def monitor_stock(symbol: str):
    """Stream real-time stock price updates."""
    while True:
        price = await fetch_current_price(symbol)
        yield f"Current price: ${price}"
        await asyncio.sleep(1)
```

See templates/streaming-tool-template.py for complete pattern.

## Event Handling

Process events from run_live():

```python
async for event in agent.run_live(request_queue, run_config=run_config):
    # Server content (agent responses)
    if event.server_content:
        if event.server_content.model_turn:
            # Text/audio from model
            process_model_response(event.server_content.model_turn)

        if event.server_content.turn_complete:
            # Agent finished speaking
            handle_turn_complete()

    # Tool calls
    if event.tool_call:
        # ADK executes tools automatically
        log_tool_execution(event.tool_call)

    # Interruptions
    if event.interrupted:
        handle_interruption()
```

## Multi-Agent Streaming

Transfer stateful sessions between agents:

```python
# Agent 1 creates session
session = await agent1.run_live(request_queue, run_config=config)

# Transfer to Agent 2 (seamless handoff)
await agent2.run_live(
    request_queue,
    run_config=config,
    session=session  # Maintains conversation context
)
```

## Workflows

### Complete Bidi-Streaming Agent Workflow

1. **Configure RunConfig**
   - Choose response modality (AUDIO or TEXT)
   - Enable session resumption
   - Configure context window compression (optional)
   - Set audio/speech configs (for audio modality)

2. **Create LiveRequestQueue**
   - Initialize queue for multimodal inputs
   - Enqueue messages as they arrive
   - Use activity markers for segmentation

3. **Implement Event Handling**
   - Process server_content for agent responses
   - Handle tool_call events
   - Manage interruption events
   - Track turn_complete signals

4. **Define Streaming Tools** (optional)
   - Use async generators for continuous output
   - Yield intermediate results over time
   - Support real-time monitoring/analysis

5. **Test and Deploy**
   - Validate audio/video processing
   - Test interruption handling
   - Verify session resumption
   - Monitor quota usage

### Audio/Video Workflow

See examples/audio-video-agent.py for complete multimodal setup including:
- Audio input processing
- Video frame handling
- Speech configuration
- Transcription settings

## Templates

All templates use placeholders only (no hardcoded API keys):

- **templates/bidi-streaming-config.py**: Complete RunConfig patterns
- **templates/streaming-tool-template.py**: Async generator tool pattern
- **templates/audio-config.py**: Speech and transcription setup
- **templates/video-config.py**: Video frame processing
- **templates/liverequest-queue.py**: Queue management patterns
- **templates/event-handler.py**: Event processing patterns

## Scripts

Utility scripts for validation and setup:

- **scripts/validate-streaming-config.py**: Validate RunConfig settings
- **scripts/test-liverequest-queue.py**: Test queue functionality
- **scripts/check-modality-support.py**: Verify modality compatibility

## Examples

Real-world streaming agent implementations:

- **examples/voice-agent.py**: Complete audio streaming agent
- **examples/video-agent.py**: Multimodal video processing agent
- **examples/streaming-tool-agent.py**: Agent with streaming tools
- **examples/multi-agent-handoff.py**: Session transfer between agents

## Best Practices

1. **Choose Modality Carefully**: Cannot switch response modality mid-session
2. **Use Session Resumption**: Prevent disconnection issues
3. **Enable Context Compression**: For extended conversations
4. **Implement Streaming Tools**: For real-time monitoring/analysis
5. **Handle Interruptions**: Natural conversation requires interruption support
6. **Segment Context**: Use activity markers for logical event boundaries
7. **Test Platform Switch**: Verify behavior on both AI Studio and Vertex AI

## Common Patterns

### Pattern 1: Voice Agent with Interruption

See examples/voice-agent.py

### Pattern 2: Streaming Analysis Tool

See examples/streaming-tool-agent.py

### Pattern 3: Multi-Agent Coordination

See examples/multi-agent-handoff.py

## References

- [ADK Bidi-streaming Docs](https://google.github.io/adk-docs/streaming/)
- [RunConfig Guide (Part 4)](https://google.github.io/adk-docs/streaming/dev-guide/part4/)
- [Audio/Video Guide (Part 5)](https://google.github.io/adk-docs/streaming/dev-guide/part5/)
- [Real-Time Multi-Agent Architecture](https://developers.googleblog.com/beyond-request-response-architecting-real-time-bidirectional-streaming-multi-agent-system/)

## Security Compliance

This skill follows strict security rules:
- All code examples use placeholder values only
- No real API keys, passwords, or secrets
- Environment variable references in all code
- `.gitignore` protection documented
