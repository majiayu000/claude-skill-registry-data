---
name: daily
description: Documentation and capabilities reference for Daily 
category: Document Processing
source: antigravity
tags: [python, javascript, typescript, react, api, ai, agent, llm, workflow, design]
url: https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/daily
---


## When to Use
- You are building a real-time voice or multimodal AI application that uses Daily or Pipecat-style transports.
- You need guidance on low-latency audio, video, text, and AI service orchestration in one pipeline.
- You want a capability reference before choosing services, transports, or workflow patterns for an interactive agent.

## Capabilities

Pipecat enables agents to build production-ready voice and multimodal AI applications with real-time processing. Agents can orchestrate complex AI service pipelines that handle audio, video, and text simultaneously while maintaining ultra-low latency (500-800ms round-trip). The framework abstracts away the complexity of coordinating multiple AI services, network transports, and audio processing, allowing agents to focus on application logic.

Key capabilities include:

- Real-time voice conversations with natural turn-taking and interruption handling
- Multimodal processing combining audio, video, images, and text
- Integration with 50+ AI services (LLMs, speech recognition, text-to-speech, vision models)
- Function calling for external API integration and tool use
- Automatic conversation context management with optional summarization
- Multiple transport options (WebRTC, WebSocket, Daily, Twilio, Telnyx, etc.)
- Production deployment across cloud platforms with built-in scaling

## Skills

### Pipeline Architecture & Frame Processing

Agents can construct pipelines that connect frame processors in sequence to handle real-time data flow:

```python
pipeline = Pipeline([
    transport.input(),              # Receives user audio
    stt,                            # Speech-to-text conversion
    context_aggregator.user(),      # Collect user responses
    llm,                            # Language model processing
    tts,                            # Text-to-speech conversion
    transport.output(),             # Sends audio to user
    context_aggregator.assistant(), # Collect assistant responses
])
```

Agents can create custom frame processors to handle specialized logic, work with parallel pipelines for conditional processing, and manage frame types (SystemFrames for immediate processing, DataFrames for ordered queuing).

### Speech Recognition & Audio Input

Agents can integrate 15+ speech-to-text providers including OpenAI, Google Cloud, Deepgram, AssemblyAI, Azure, and Whisper. Services support:

- Real-time streaming transcription via WebSocket connections
- Voice Activity Detection (VAD) for automatic speech detection
- Multiple language support (125+ languages with Google Cloud)
- Word-level confidence scores and automatic punctuation
- Configurable latency tuning for optimal performance

### Text-to-Speech & Audio Output

Agents can choose from 30+ text-to-speech providers including OpenAI, Google Cloud, ElevenLabs, Cartesia, LMNT, and PlayHT. Features include:

- Real-time streaming synthesis with ultra-low latency
- Multiple voice options and speaking styles per provider
- Automatic interruption handling for natural conversations
- Audio format flexibility (WAV, PCM, MP3)
- Word-level output for precise context tracking

### Language Model Integration

Agents can integrate with 20+ LLM providers including OpenAI, Anthropic, Google Gemini, Groq, Perplexity, and open-source models via Ollama. Capabilities include:

- Streaming response generation for real-time output
- Function calling (tool use) for external API integration
- Context management with automatic message history tracking
- Token usage monitoring and cost tracking
- Support for vision models and multimodal inputs

### Function Calling & Tool Integration

Agents can enable LLMs to call external functions and APIs during conversations:

```python
# Define functions using standard schema
weather_function = FunctionSchema(
    name="get_current_weather",
    description="Get the current weather in a location",
    properties={"location": {"type": "string"}},
    required=["location"]
)

# Register function handlers
async def fetch_weather(params: FunctionCallParams):
    location = params.arguments.get("location")
    weather_data = await weather_api.get_weather(location)
    await params.result_callback(weather_data)

llm.register_function("get_current_weather", fetch_weather)
```

Function results are automatically stored in conversation context, enabling multi-step interactions and real-time data access.

### Context Management & Conversation History

Agents can manage conversation context automatically or manually:

- Automatic context aggregation from transcriptions and TTS output
- Manual context manipulation via `LLMMessagesAppendFrame` and `LLMMessagesUpdateFrame`
- Automatic context summarization for long conversations to reduce token usage
- Tool definitions and function call results stored in context
- Word-level precision for context accuracy during interruptions

### Voice Activity Detection & Turn Management

Agents can configure sophisticated turn-taking strategies
