---
name: livekit-stt-selfhosted
description: Build self-hosted speech-to-text APIs using Hugging Face models (Whisper, Wav2Vec2) and create LiveKit voice agent plugins. Use when building STT infrastructure, creating custom LiveKit plugins, deploying self-hosted transcription services, or integrating Whisper/HF models with LiveKit agents. Includes FastAPI server templates, LiveKit plugin implementation, model selection guides, and production deployment patterns.
---

# LiveKit Self-Hosted STT Plugin

Build self-hosted speech-to-text APIs and LiveKit voice agent plugins using Hugging Face models.

## Overview

This skill provides templates and guidance for:
1. Building a self-hosted STT API server using FastAPI + Whisper/HF models
2. Creating a LiveKit plugin that connects to your self-hosted API
3. Deploying and scaling in production

## Quick Start

### Option 1: Build Both (API + Plugin)

When user wants complete setup:

1. **Create API Server**:
```bash
python scripts/setup_api_server.py my-stt-server --model openai/whisper-medium
cd my-stt-server
pip install -r requirements.txt
python main.py
```

2. **Create Plugin**:
```bash
python scripts/setup_plugin.py custom-stt
cd livekit-plugins-custom-stt
pip install -e .
```

3. **Use in LiveKit Agent**:
```python
from livekit.plugins import custom_stt

stt=custom_stt.STT(api_url="ws://localhost:8000/ws/transcribe")
```

### Option 2: API Server Only

When user only needs the API server:
- Use `scripts/setup_api_server.py` with desired model
- See `references/api_server_guide.md` for implementation details
- Template in `assets/api-server/`

### Option 3: Plugin Only

When user has existing API and needs LiveKit plugin:
- Use `scripts/setup_plugin.py` with plugin name
- See `references/plugin_implementation.md` for details
- Template in `assets/plugin-template/`

## Model Selection

Help user choose the right model:

| Use Case | Recommended Model | Rationale |
|----------|------------------|-----------|
| Best accuracy | `openai/whisper-large-v3` | SOTA quality, requires GPU |
| Production balance | `openai/whisper-medium` | Good quality, reasonable speed |
| Real-time/fast | `openai/whisper-small` | Fast, acceptable quality |
| CPU-only | `openai/whisper-tiny` | Can run without GPU |
| English-only | `facebook/wav2vec2-large-960h` | Optimized for English |

For detailed comparison and optimization tips, see `references/models_comparison.md`.

## Implementation Workflow

### Building the API Server

1. **Use the template**: Start with `assets/api-server/main.py`
2. **Key components**:
   - FastAPI app with WebSocket endpoint
   - Model loading at startup (kept in memory)
   - Audio buffer management
   - WebSocket protocol for streaming

3. **Customization points**:
   - Model selection (change `MODEL_ID` in .env)
   - Audio processing parameters
   - Batch size and optimization
   - Error handling

For complete implementation guide, see `references/api_server_guide.md`.

### Building the LiveKit Plugin

1. **Use the template**: Start with `assets/plugin-template/`
2. **Required implementations**:
   - `_recognize_impl()` - Non-streaming recognition
   - `stream()` - Return SpeechStream instance
   - `SpeechStream` class - Handle streaming

3. **Key considerations**:
   - Audio format conversion (16kHz, mono, 16-bit PCM)
   - WebSocket connection management
   - Event emission (interim/final transcripts)
   - Error handling and cleanup

For complete implementation guide, see `references/plugin_implementation.md`.

## Deployment

### Development
```bash
# API Server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Test WebSocket
ws://localhost:8000/ws/transcribe
```

### Production

**Docker** (Recommended):
```bash
docker-compose up
```

**Kubernetes**: Use manifests in deployment guide

**Cloud Platforms**: AWS ECS, GCP Cloud Run, Azure Container Instances

For complete deployment guide including scaling, monitoring, and security, see `references/deployment.md`.

## WebSocket Protocol

### Client → Server
- **Audio**: Binary (16-bit PCM, 16kHz)
- **Config**: `{"type": "config", "language": "en"}`
- **End**: `{"type": "end"}`

### Server → Client
- **Interim**: `{"type": "interim", "text": "..."}`
- **Final**: `{"type": "final", "text": "...", "language": "en"}`
- **Error**: `{"type": "error", "message": "..."}`

## Common Tasks

### Change Model
Edit `.env`:
```bash
MODEL_ID=openai/whisper-small  # Faster model
```

### Add Language Support
In plugin usage:
```python
stt=custom_stt.STT(language="es")  # Spanish
stt=custom_stt.STT(detect_language=True)  # Auto-detect
```

### Enable GPU
In API server:
```bash
DEVICE=cuda:0  # Use GPU
```

### Scale Horizontally
Deploy multiple API server instances behind load balancer. See `references/deployment.md` for Nginx configuration.

## Troubleshooting

### Out of Memory
- Use smaller model (`whisper-small` or `whisper-tiny`)
- Reduce `batch_size` in pipeline
- Enable `low_cpu_mem_usage=True`

### Slow Transcription
- Ensure GPU is enabled (`DEVICE=cuda:0`)
- Use FP16 precision (automatic on GPU)
- Increase `batch_size`
- Use smaller model

### Connection Issues
- Verify WebSocket support in load balancer
- Check firewall rules
- Increase timeout settings

## Scripts

- `scripts/setup_api_server.py` - Generate API server from template
- `scripts/setup_plugin.py` - Generate LiveKit plugin from template

## References

Load these as needed for detailed information:

- `references/api_server_guide.md` - Complete API implementation guide
- `references/plugin_implementation.md` - LiveKit plugin development
- `references/models_comparison.md` - Model selection and optimization
- `references/deployment.md` - Production deployment best practices

## Assets

Ready-to-use templates:

- `assets/api-server/` - Complete FastAPI server with Whisper
- `assets/plugin-template/` - LiveKit STT plugin structure

## Best Practices

1. **Keep models in memory** - Load once at startup, not per request
2. **Use appropriate model size** - Balance quality vs. speed for your use case
3. **Process audio in chunks** - 1-second chunks work well for streaming
4. **Implement proper cleanup** - Close WebSocket connections gracefully
5. **Monitor metrics** - Track latency, throughput, GPU utilization
6. **Use Docker** - Ensures consistent deployments
7. **Enable authentication** - Secure production APIs
8. **Scale horizontally** - Use load balancer for high availability
