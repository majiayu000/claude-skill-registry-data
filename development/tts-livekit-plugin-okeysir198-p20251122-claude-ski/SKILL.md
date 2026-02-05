---
name: tts-livekit-plugin
description: "Build self-hosted TTS APIs using HuggingFace models (Parler-TTS, F5-TTS, XTTS-v2) and create LiveKit voice agent plugins with streaming support. Use when creating production-ready text-to-speech systems that need: (1) Self-hosted TTS with full control, (2) LiveKit voice agent integration, (3) Streaming audio for low-latency conversations, (4) Custom voice characteristics, (5) Cost-effective alternatives to cloud TTS providers like ElevenLabs or Google TTS."
---

# Self-Hosted TTS API and LiveKit Plugin

Build production-ready self-hosted Text-to-Speech APIs using HuggingFace models and integrate them with LiveKit voice agents through custom plugins.

---

## Overview

This skill enables you to:
- **Build TTS APIs** using state-of-the-art HuggingFace models (Parler-TTS, F5-TTS, XTTS-v2)
- **Create LiveKit plugins** that connect voice agents to your self-hosted TTS
- **Implement streaming** for low-latency real-time synthesis
- **Deploy to production** with Docker, Kubernetes, or cloud platforms

**When to use this skill:**
- Creating cost-effective voice agents without cloud TTS fees
- Requiring custom voice characteristics or multilingual support
- Building privacy-focused systems with on-premise TTS
- Developing voice agents that need streaming audio synthesis

---

## Implementation Process

### Step 1: Choose Your TTS Model

Select the best model for your use case from the HuggingFace ecosystem.

**Load model comparison:** [TTS Models Reference](./references/tts-models.md)

**Quick Selection Guide:**

| Use Case | Recommended Model | Why |
|----------|------------------|-----|
| Production voice agents | Parler-TTS Mini | Fast, CPU-friendly, text-based voice control |
| High-quality synthesis | Parler-TTS Large / F5-TTS | Superior natural quality |
| Multilingual support | XTTS-v2 | 17+ languages, voice cloning |
| Cost optimization | Parler-TTS Mini on CPU | Runs efficiently without GPU |

**Example decision:**
- User needs: "Fast, conversational voice for customer support agent"
- Model: `parler-tts/parler-tts-mini-v1`
- Device: CPU (for cost) or GPU (for speed)
- Voice description: `"A friendly, professional voice with moderate pace"`

---

### Step 2: Build the TTS API Server

Create a FastAPI server that hosts the TTS model with both batch and streaming endpoints.

**Use the provided implementation:**

The skill includes a complete TTS API server at `tts-api/main.py` that supports:
- **Batch synthesis**: POST `/synthesize` for simple text-to-speech
- **Streaming synthesis**: WebSocket `/ws/synthesize` for real-time incremental synthesis
- **Multiple models**: Parler-TTS, F5-TTS, XTTS-v2 (configurable)
- **Optimizations**: Model caching, async synthesis, sentence-level streaming

**Quick start:**

```bash
# Navigate to TTS API directory
cd tts-api

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env to set:
#   TTS_MODEL_TYPE=parler
#   TTS_MODEL_NAME=parler-tts/parler-tts-mini-v1
#   TTS_DEVICE=cpu

# Run the server
python main.py
```

The server will:
1. Load the model on startup (may take 1-2 minutes)
2. Listen on port 8001
3. Provide health check at `GET /health`
4. Accept synthesis requests at `POST /synthesize` and `WS /ws/synthesize`

**Test the API:**

```bash
# Test batch synthesis
curl -X POST http://localhost:8001/synthesize \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello! This is a test.", "format": "wav"}' \
  --output test.wav

# Check health
curl http://localhost:8001/health
```

**For detailed implementation patterns and best practices:**
- [API Implementation Guide](./references/api-implementation.md)

**Key implementation details:**

The provided `tts-api/main.py` includes:
- **Model loading**: Singleton pattern with startup event
- **Sentence-level streaming**: Splits text at sentence boundaries for natural prosody
- **Keepalive messages**: Prevents WebSocket timeouts (5s interval)
- **End-of-stream signaling**: Explicit completion messages
- **Error handling**: Graceful failures with detailed error messages
- **Audio formats**: PCM int16 (streaming), WAV, MP3 (batch)

---

### Step 3: Create the LiveKit TTS Plugin

Build a LiveKit plugin that connects your voice agents to the self-hosted TTS API.

**Use the provided plugin implementation:**

The skill includes a complete LiveKit plugin at `livekit-plugin-custom-tts/` with:
- **TTS class**: Main plugin interface
- **ChunkedStream**: Streaming synthesis session
- **WebSocket communication**: Bi-directional streaming
- **Examples**: Voice agent integration and standalone usage

**Install the plugin:**

```bash
# Navigate to plugin directory
cd livekit-plugin-custom-tts

# Install in development mode
pip install -e .

# Or install from source
pip install .
```

**Use in a voice agent:**

```python
from livekit import agents
from livekit.agents import AgentSession
from livekit.plugins import openai, deepgram, silero
from livekit.plugins import custom_tts

async def entrypoint(ctx: agents.JobContext):
    # Initialize session with custom TTS
    session = AgentSession(
        vad=silero.VAD.load(),
        stt=deepgram.STT(model="nova-2-general"),
        llm=openai.LLM(model="gpt-4o-mini"),
        # Use custom self-hosted TTS
        tts=custom_tts.TTS(
            api_url="http://localhost:8001",
            options=custom_tts.TTSOptions(
                voice_description="A friendly, conversational voice.",
                sample_rate=24000,
            ),
        ),
    )

    await ctx.connect()
    await session.start(agent=YourAgent(), room=ctx.room)
```

**For detailed plugin development patterns:**
- [Plugin Development Guide](./references/plugin-development.md)

**Key plugin features:**

The provided implementation includes:
- **Streaming synthesis**: Iterates over audio chunks as they're generated
- **Keepalive**: Maintains long-running WebSocket connections
- **Error recovery**: Graceful handling of connection failures
- **Resource cleanup**: Proper task cancellation and WebSocket closure
- **LiveKit integration**: Follows LiveKit TTS plugin interface exactly

---

### Step 4: Test the Integration

Verify that the TTS API and plugin work together correctly.

**Testing levels:**

**1. API-level testing:**

```bash
# Start the TTS API
cd tts-api
python main.py

# In another terminal, test synthesis
curl -X POST http://localhost:8001/synthesize \
  -H "Content-Type: application/json" \
  -d '{"text": "Testing TTS API", "format": "wav"}' \
  --output test.wav

# Play the audio
ffplay test.wav  # or open test.wav
```

**2. Plugin-level testing:**

Use the provided example script:

```bash
cd livekit-plugin-custom-tts/examples
python basic_usage.py
```

This will:
- Connect to the TTS API
- Synthesize test text
- Save audio to `output.wav`

**3. Voice agent testing:**

Use the provided voice agent example:

```bash
# Set environment variables
export LIVEKIT_URL="wss://your-livekit.cloud"
export LIVEKIT_API_KEY="your-api-key"
export LIVEKIT_API_SECRET="your-api-secret"
export OPENAI_API_KEY="your-openai-key"
export DEEPGRAM_API_KEY="your-deepgram-key"

# Run the voice agent
cd livekit-plugin-custom-tts/examples
python voice_agent.py start
```

**Verification checklist:**

- [ ] TTS API health endpoint returns OK
- [ ] Batch synthesis produces audio files
- [ ] WebSocket streaming works without disconnections
- [ ] Plugin synthesizes text successfully
- [ ] Voice agent speaks using custom TTS
- [ ] Audio quality is acceptable
- [ ] Latency is reasonable (<1 second for short sentences)

---

### Step 5: Deploy to Production

Deploy the TTS API and voice agent to production infrastructure.

**Deployment options:**

**Option 1: Docker Compose (Quick Start)**

Use the provided configuration:

```bash
# Create deployment directory
mkdir deployment
cd deployment

# Copy TTS API
cp -r ../tts-api .

# Set environment variables
export LIVEKIT_URL="wss://your-livekit.cloud"
export LIVEKIT_API_KEY="your-api-key"
# ... other vars

# Run docker-compose
docker-compose up -d
```

**Option 2: Kubernetes (Production Scale)**

Use the provided Kubernetes manifests in the deployment guide.

**For comprehensive deployment instructions:**
- [Deployment Guide](./references/deployment.md)

**Production deployment includes:**
- Docker containerization for both API and agent
- GPU allocation for faster synthesis
- Health checks and monitoring
- Horizontal scaling with load balancing
- Secrets management
- Persistent model caching
- Logging and metrics collection

**Production checklist:**

- [ ] GPU properly allocated (if using GPU)
- [ ] Model cache persisted (avoid re-downloading)
- [ ] Health checks implemented
- [ ] Monitoring and alerting set up
- [ ] Autoscaling configured (if using Kubernetes)
- [ ] Secrets properly managed
- [ ] Network policies applied (if using Kubernetes)
- [ ] Load testing completed
- [ ] Backup strategy in place

---

## Common Patterns

### Pattern 1: Multiple Voice Characteristics

Create different agents with different voices:

```python
# Customer support agent
support_agent = AgentSession(
    tts=custom_tts.TTS(
        api_url="http://localhost:8001",
        options=custom_tts.TTSOptions(
            voice_description="A professional, clear voice with measured pace.",
        ),
    ),
)

# Sales agent
sales_agent = AgentSession(
    tts=custom_tts.TTS(
        api_url="http://localhost:8001",
        options=custom_tts.TTSOptions(
            voice_description="An energetic, friendly voice with upbeat delivery.",
        ),
    ),
)
```

### Pattern 2: Multilingual Voice Agent

Use XTTS-v2 for multilingual support:

```bash
# Configure TTS API for XTTS
TTS_MODEL_TYPE=xtts
TTS_MODEL_NAME=tts_models/multilingual/multi-dataset/xtts_v2
```

```python
# In your agent
tts=custom_tts.TTS(
    api_url="http://localhost:8001",
    options=custom_tts.TTSOptions(
        voice_description="Multilingual voice",
        sample_rate=24000,
    ),
)
```

### Pattern 3: Failover to Cloud TTS

Implement fallback to cloud TTS on self-hosted failure:

```python
async def create_tts():
    """Create TTS with fallback."""
    try:
        # Try self-hosted first
        return custom_tts.TTS(api_url="http://localhost:8001")
    except Exception as e:
        logger.warning(f"Self-hosted TTS unavailable: {e}")
        # Fallback to cloud provider
        return openai.TTS(voice="alloy")

session = AgentSession(
    tts=await create_tts(),
    # ... other config
)
```

### Pattern 4: Response Caching

Cache common phrases to reduce synthesis latency:

```python
from functools import lru_cache

@lru_cache(maxsize=100)
async def synthesize_cached(text: str) -> bytes:
    """Synthesize with caching for common phrases."""
    # First time: synthesize and cache
    # Subsequent times: return cached audio
    return await synthesize_async(text)

# Common greetings, confirmations, etc. are cached
audio = await synthesize_cached("Hello! How can I help you today?")
```

---

## Troubleshooting

### Issue: TTS API is slow

**Symptoms:** High latency (>2 seconds per sentence)

**Solutions:**
1. **Use GPU acceleration:**
   - Set `TTS_DEVICE=cuda` in environment
   - Ensure GPU is available (`nvidia-smi`)
   - Allocate GPU in Docker/Kubernetes

2. **Use faster model:**
   - Switch from `parler-tts-large-v1` to `parler-tts-mini-v1`
   - Consider CPU-optimized models

3. **Optimize inference:**
   ```python
   # Add to TTS API startup
   import torch
   model = torch.compile(model, mode="reduce-overhead")
   ```

4. **Implement sentence-level streaming:**
   - Already included in provided implementation
   - Reduces perceived latency

### Issue: WebSocket connection drops

**Symptoms:** Connection lost during long syntheses

**Solutions:**
1. **Verify keepalive is enabled:**
   - Check plugin implementation has `_keepalive_loop()`
   - Ensure 5-second interval

2. **Increase timeouts:**
   ```python
   # In plugin
   async with asyncio.timeout(60):  # 60 second timeout
       message = await self._ws.recv()
   ```

3. **Check network policies:**
   - Verify firewall allows WebSocket connections
   - Test direct connection without proxies

### Issue: Audio quality is poor

**Symptoms:** Robotic voice, artifacts, glitches

**Solutions:**
1. **Use larger model:**
   - Switch to `parler-tts-large-v1` or `F5-TTS`

2. **Adjust voice description:**
   ```python
   # More detailed description = better quality
   voice_description="A warm, natural voice speaking clearly with good articulation and moderate pace"
   ```

3. **Check audio format:**
   - Ensure sample rate matches (24kHz)
   - Verify PCM int16 encoding

### Issue: High memory usage

**Symptoms:** Server runs out of memory, crashes

**Solutions:**
1. **Use smaller model:**
   - `parler-tts-mini-v1` uses ~880M parameters vs. ~2.4B for large

2. **Limit concurrent requests:**
   ```python
   MAX_CONCURRENT = 5
   semaphore = asyncio.Semaphore(MAX_CONCURRENT)

   @app.post("/synthesize")
   async def synthesize(request: TTSRequest):
       async with semaphore:
           return await synthesize_async(request)
   ```

3. **Clear audio buffers:**
   - Ensure buffers are released after sending
   - Already handled in provided implementation

### Issue: Model download fails

**Symptoms:** Error loading model from HuggingFace

**Solutions:**
1. **Check internet connectivity:**
   ```bash
   curl -I https://huggingface.co
   ```

2. **Use authentication token (if needed):**
   ```bash
   export HF_TOKEN="your-huggingface-token"
   ```

3. **Pre-download models:**
   ```python
   from huggingface_hub import snapshot_download
   snapshot_download("parler-tts/parler-tts-mini-v1")
   ```

---

## Best Practices

### API Development

✅ **DO:**
- Load model once at startup, not per request
- Implement health checks for monitoring
- Use sentence-level streaming for natural prosody
- Send keepalive messages every 5 seconds
- Explicitly signal end-of-stream
- Handle errors gracefully with detailed messages
- Use async synthesis to avoid blocking

❌ **DON'T:**
- Load model for each request (very slow)
- Block event loop with synchronous synthesis
- Split text mid-word (breaks natural speech)
- Forget keepalive (causes timeouts)
- Close connections without signaling

### Plugin Development

✅ **DO:**
- Follow LiveKit TTS plugin interface exactly
- Implement proper cleanup in `aclose()`
- Use async iterators for streaming
- Handle WebSocket disconnections gracefully
- Log errors for debugging
- Test with various text lengths

❌ **DON'T:**
- Modify LiveKit interfaces
- Leave WebSocket connections open
- Use synchronous code in async context
- Ignore errors or exceptions
- Skip testing edge cases

### Deployment

✅ **DO:**
- Persist model cache to avoid re-downloading
- Use GPU for production (faster synthesis)
- Implement monitoring and alerting
- Use horizontal scaling for high traffic
- Secure API with authentication
- Test failover scenarios
- Document configuration

❌ **DON'T:**
- Re-download models on each restart
- Run production on CPU only (too slow)
- Deploy without monitoring
- Use single instance for production
- Expose API publicly without auth
- Skip disaster recovery planning

---

## Reference Files

### Core Documentation

Load these resources as needed for detailed information:

- **[TTS Models Comparison](./references/tts-models.md)**: Comprehensive comparison of HuggingFace TTS models (Parler-TTS, F5-TTS, XTTS-v2) with performance benchmarks, code examples, and selection guide.

- **[API Implementation Guide](./references/api-implementation.md)**: Best practices for building TTS APIs including streaming patterns, model management, audio format handling, security, and optimization strategies.

- **[Plugin Development Guide](./references/plugin-development.md)**: Detailed guide for implementing LiveKit TTS plugins including WebSocket communication, async patterns, error handling, and testing.

- **[Deployment Guide](./references/deployment.md)**: Production deployment with Docker Compose, Kubernetes, scaling strategies, monitoring, and security best practices.

### Code Resources

**TTS API Server:**
- `tts-api/main.py`: Complete FastAPI server with batch and streaming endpoints
- `tts-api/requirements.txt`: Python dependencies
- `tts-api/Dockerfile`: Container configuration
- `tts-api/.env.example`: Environment variables template

**LiveKit Plugin:**
- `livekit-plugin-custom-tts/`: Complete plugin package
- `livekit-plugin-custom-tts/livekit/plugins/custom_tts/tts.py`: Plugin implementation
- `livekit-plugin-custom-tts/examples/voice_agent.py`: Voice agent integration example
- `livekit-plugin-custom-tts/examples/basic_usage.py`: Standalone usage example

---

## Quick Reference

### TTS API Endpoints

```
GET  /              - Health check and info
GET  /health        - Health status
POST /synthesize    - Batch synthesis
WS   /ws/synthesize - Streaming synthesis
```

### Environment Variables

```bash
# TTS API
TTS_MODEL_TYPE=parler          # parler, f5, xtts
TTS_MODEL_NAME=parler-tts/parler-tts-mini-v1
TTS_DEVICE=cuda                # cuda or cpu

# LiveKit Agent
LIVEKIT_URL=wss://your-livekit.cloud
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret
TTS_API_URL=http://localhost:8001
```

### Model Selection

| Model | Size | Speed | Quality | Multilingual |
|-------|------|-------|---------|--------------|
| parler-tts-mini-v1 | 880M | ★★★★★ | ★★★★☆ | Limited |
| parler-tts-large-v1 | 2.4B | ★★★☆☆ | ★★★★★ | Limited |
| F5-TTS | Varies | ★★★☆☆ | ★★★★★ | Good |
| XTTS-v2 | 1.2B | ★★★★☆ | ★★★★★ | Excellent |

### Voice Description Examples

```
"A friendly, conversational voice with moderate pace."
"A professional, clear voice speaking slowly and deliberately."
"An energetic, upbeat voice with fast delivery and enthusiasm."
"A calm, soothing voice with gentle, measured speech."
```

---

## Additional Resources

- **HuggingFace TTS**: https://huggingface.co/tasks/text-to-speech
- **LiveKit Agents Docs**: https://docs.livekit.io/agents/
- **Parler-TTS Repository**: https://github.com/huggingface/parler-tts
- **F5-TTS Repository**: https://github.com/SWivid/F5-TTS
- **XTTS-v2 Model**: https://huggingface.co/coqui/XTTS-v2
- **Modal Blog on TTS**: https://modal.com/blog/open-source-tts
