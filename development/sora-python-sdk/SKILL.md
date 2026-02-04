---
name: sora-python-sdk
description: Python SDK for WebRTC SFU Sora - real-time video/audio streaming and communication. Use when working with Sora connections, WebRTC streams, video/audio sources/sinks, hardware encoding/decoding (Intel VPL, NVIDIA, Apple VideoToolbox, AMD AMF, Raspberry Pi), data channels, simulcast, encoded transforms, VAD, or building real-time communication applications. Supports sendonly, recvonly, and sendrecv roles.
---

# Sora Python SDK

Python SDK for WebRTC SFU Sora - enables real-time video and audio streaming with hardware acceleration support.

## Core Concepts

**Roles**: 
- `sendonly` - Send audio/video to Sora
- `recvonly` - Receive audio/video from Sora  
- `sendrecv` - Both send and receive

**Key Objects**:
- `Sora` - Main SDK instance, creates connections and sources
- `SoraConnection` - Manages connection to Sora server
- `SoraAudioSource` / `SoraVideoSource` - Send audio/video data
- `SoraAudioSink` / `SoraVideoSink` - Receive audio/video data

## Installation

```bash
# Standard package
uv add sora-sdk
# or
pip install sora-sdk

# Raspberry Pi
uv add sora-sdk-rpi
```

## Quick Start Examples

### Sendonly (Camera/Mic to Sora)

```python
import cv2
import numpy as np
from sora_sdk import Sora

# Initialize
sora = Sora()
audio_source = sora.create_audio_source(channels=1, sample_rate=16000)
video_source = sora.create_video_source()

# Create connection
connection = sora.create_connection(
    signaling_urls=["wss://sora.example.com/signaling"],
    role="sendonly",
    channel_id="my-channel",
    audio_source=audio_source,
    video_source=video_source
)

# Connect and send frames
connection.connect()

# Send audio (16-bit PCM)
audio_data = np.zeros((320, 1), dtype=np.int16)
audio_source.on_data(audio_data)

# Send video (BGR format)
frame = np.zeros((480, 640, 3), dtype=np.uint8)
video_source.on_captured(frame)

connection.disconnect()
```

### Recvonly (Receive from Sora)

```python
from sora_sdk import Sora, SoraAudioSink, SoraVideoSink

sora = Sora()
connection = sora.create_connection(
    signaling_urls=["wss://sora.example.com/signaling"],
    role="recvonly",
    channel_id="my-channel"
)

# Handle incoming tracks
def on_track(track):
    if track.kind == "audio":
        audio_sink = SoraAudioSink(track, output_frequency=16000, output_channels=1)
        # Read audio: success, data = audio_sink.read(frames=320)
    
    elif track.kind == "video":
        video_sink = SoraVideoSink(track)
        
        def on_frame(frame):
            # frame.data() returns numpy array (H x W x 3 BGR)
            image = frame.data()
            print(f"Received frame: {image.shape}")
        
        video_sink.on_frame = on_frame

connection.on_track = on_track
connection.connect()
```

## Hardware Acceleration

Specify hardware encoders/decoders via `SoraVideoCodecPreference`:

```python
from sora_sdk import (
    Sora, 
    SoraVideoCodecPreference,
    SoraVideoCodecType,
    SoraVideoCodecImplementation
)

# Intel VPL example
preference = SoraVideoCodecPreference(
    codecs=[
        SoraVideoCodecPreference.Codec(
            type=SoraVideoCodecType.H264,
            encoder=SoraVideoCodecImplementation.INTEL_VPL,
            decoder=SoraVideoCodecImplementation.INTEL_VPL
        )
    ]
)

sora = Sora(video_codec_preference=preference)

# Available implementations:
# - INTEL_VPL (VP9, AV1, H264, H265)
# - NVIDIA_VIDEO_CODEC_SDK (VP8/VP9 decode only, AV1, H264, H265)
# - APPLE_VIDEO_TOOLBOX (H264, H265)
# - AMD_AMF (VP9 decode, AV1, H264, H265)
# - RASPI_V4L2M2M (H264 only)
# - CISCO_OPENH264 (H264 software)
```

## Data Channels (Messaging)

```python
# Setup data channels
connection = sora.create_connection(
    signaling_urls=["wss://..."],
    role="sendrecv",
    channel_id="my-channel",
    data_channel_signaling=True,
    data_channels=[
        {"label": "#messaging", "direction": "sendrecv"}
    ]
)

# Send message
def on_data_channel(label):
    connection.send_data_channel(label, b"Hello")

# Receive message
def on_message(label, data):
    print(f"Received on {label}: {data.decode('utf-8')}")

connection.on_data_channel = on_data_channel
connection.on_message = on_message
```

## Simulcast

Enable multiple quality streams:

```python
connection = sora.create_connection(
    signaling_urls=["wss://..."],
    role="sendonly",
    channel_id="my-channel",
    simulcast=True,
    video_bit_rate=5550,  # Total bitrate for all streams
    video_source=video_source
)
```

## Encoded Transform (E2EE)

Process encoded frames before transmission:

```python
from sora_sdk import SoraVideoFrameTransformer

transformer = SoraVideoFrameTransformer()

def on_transform(frame):
    # Modify encoded frame data
    data = frame.get_data()
    # ... encrypt/modify data ...
    frame.set_data(modified_data)
    transformer.enqueue(frame)

transformer.on_transform = on_transform

connection = sora.create_connection(
    ...,
    video_frame_transformer=transformer
)
```

## Voice Activity Detection

```python
from sora_sdk import SoraVAD, SoraAudioStreamSink

vad = SoraVAD()

def on_frame(audio_frame):
    probability = vad.analyze(audio_frame)
    if probability > 0.95:  # Likely voice
        print("Voice detected!")

# Use with SoraAudioStreamSink
audio_stream_sink = SoraAudioStreamSink(track, 16000, 1)
audio_stream_sink.on_frame = on_frame
```

## Connection Events

```python
import json

def on_notify(raw_message):
    msg = json.loads(raw_message)
    if msg["type"] == "notify":
        print(f"Event: {msg['event_type']}")

def on_disconnect(error_code, message):
    print(f"Disconnected: {error_code} - {message}")

connection.on_notify = on_notify
connection.on_disconnect = on_disconnect
```

## Statistics

```python
import json

raw_stats = connection.get_stats()
stats = json.loads(raw_stats)

for stat in stats:
    if stat.get("type") == "outbound-rtp":
        print(f"Sent: {stat['bytesSent']} bytes")
        print(f"Codec: {stat.get('encoderImplementation')}")
```

## Common Patterns

**Audio/Video from Device**:
- Use `sounddevice` for audio capture: `sounddevice.InputStream(callback=...)`
- Use `cv2.VideoCapture` for camera: `cap.read()` → `video_source.on_captured(frame)`

**Metadata & Authentication**:
```python
metadata = {"access_token": "...", "custom_field": "value"}
connection = sora.create_connection(..., metadata=metadata)
```

**Multiple Connections**: Create multiple `SoraConnection` objects from same `Sora` instance to share sources.

## Reference Documentation

- **API Reference**: See [references/api_reference.md](references/api_reference.md) for complete API details
- **Examples**: See [references/examples.md](references/examples.md) for full working examples
- **Hardware Acceleration**: See [references/hardware_acceleration.md](references/hardware_acceleration.md) for platform-specific setup
