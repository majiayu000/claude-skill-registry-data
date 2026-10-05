---
name: agora
description: Build real-time communication apps using Agora SDKs (agora.io). Covers RTC (video/voice calling, live streaming, screen sharing), RTM (signaling, messaging, presence), Conversational AI (voice agents), Cloud Recording, Server Gateway, and token generation. Supports Web JS/TS, React, iOS Swift, Android Kotlin/Java, Go, Python. Triggers on Agora, agora.io, RTC, RTM, video calling, voice calling, real-time communication, screen sharing, Cloud Recording, agora-rtc-sdk-ng, agora-rtc-react, agora-rtm, Agora token generation, agora-agent-client-toolkit, AgoraVoiceAI, AgoraClient, useConversationalAI.
layer: domain
category: ai-ml
triggers:
  - "agora"
  - "voice ai"
  - "voice chat"
  - "conversational ai"
  - "real-time voice"
  - "voice assistant"
  - "speech to speech"
  - "voice agent"
  - "rtc voice"
  - "agora rtc"
inputs:
  - "Voice AI feature requirements"
  - "Real-time audio channel configuration"
  - "Conversational AI agent setup"
  - "TTS/ASR provider selection"
outputs:
  - "Agora RTC integration code"
  - "Conversational AI agent configurations"
  - "Voice pipeline architectures"
  - "Token generation and channel management"
linksTo:
  - websockets
  - ai-agents
  - nextjs
  - api-designer
  - authentication
linkedFrom:
  - ai-multimodal
preferredNextSkills:
  - ai-agents
  - websockets
  - nextjs
fallbackSkills:
  - ai-sdk
  - streaming
riskLevel: medium
memoryReadPolicy: selective
memoryWritePolicy: selective
sideEffects:
  - "Connects to Agora RTC cloud"
  - "Starts/stops voice AI agents via REST API"
  - "Generates RTC tokens"
---

# Agora Conversational AI Engine

## Purpose

Build real-time voice AI features using Agora's Conversational AI Engine. This skill covers the full pipeline: RTC channel management, ASR (speech recognition), LLM integration, TTS (text-to-speech), and voice activity detection (VAD). Supports both standalone voice apps and voice features embedded in existing applications.

## Architecture

```
User (mic) → Agora RTC Channel → Conversational AI Engine
                                    ├─ ASR (speech → text)
                                    ├─ LLM (reasoning)
                                    ├─ TTS (text → speech)
                                    └─ VAD (interruption detection)
                                 → Agora RTC Channel → User (speaker)
```

**Latency**: ~650ms voice-to-voice (ASR + LLM + TTS combined)
**Interruption**: User can interrupt AI mid-sentence; VAD detects speech overlap

## Core Concepts

| Concept | Description |
|---------|-------------|
| **App ID** | Project identifier from console.agora.io |
| **App Certificate** | Secret for token generation (never expose client-side) |
| **Customer ID/Secret** | REST API auth (Basic auth, base64 encoded) |
| **Channel** | Named audio room; users and agents join the same channel |
| **RTC Token** | Short-lived token granting channel access for a specific UID |
| **Agent UID** | The AI agent's identity in the channel (string or numeric) |

## Required Credentials

```bash
# Server-side only (never NEXT_PUBLIC_)
AGORA_APP_ID=            # From console.agora.io
AGORA_APP_CERTIFICATE=   # From console.agora.io
AGORA_CUSTOMER_ID=       # RESTful API credentials
AGORA_CUSTOMER_SECRET=   # RESTful API credentials

# Client-side (safe to expose)
NEXT_PUBLIC_AGORA_APP_ID=         # Same as AGORA_APP_ID
NEXT_PUBLIC_AGORA_AGENT_UID=333   # Agent's channel UID
```

Get credentials at: https://console.agora.io
- Create project → Get App ID + Certificate
- Account → RESTful API → Get Customer ID + Secret
- Free tier: 10,000 RTC min/mo + 300 Conversational AI min/mo

## NPM Packages

```bash
npm install agora-rtc-react agora-token
```

| Package | Purpose |
|---------|---------|
| `agora-rtc-react` | React hooks for RTC (useJoin, useLocalMicrophoneTrack, usePublish, useRemoteUsers) |
| `agora-token` | Server-side RTC token generation (RtcTokenBuilder) |

## Key Patterns

### 1. Token Generation (Server-Side)

```typescript
import { RtcTokenBuilder, RtcRole } from "agora-token";

function generateToken(appId: string, cert: string, channel: string, uid: number | string) {
  const expiry = Math.floor(Date.now() / 1000) + 3600;
  return RtcTokenBuilder.buildTokenWithUid(
    appId, cert, channel, uid, RtcRole.PUBLISHER, expiry, expiry
  );
}
```

### 2. Start Conversational AI Agent (REST API)

```
POST {baseUrl}/{appId}/join
Authorization: Basic base64(customerId:customerSecret)
Content-Type: application/json
```

Base URL: `https://api.agora.io/api/conversational-ai-agent/v2/projects`

```json
{
  "name": "unique-session-name",
  "properties": {
    "channel": "channel-name",
    "token": "agent-rtc-token",
    "agent_rtc_uid": "333",
    "remote_rtc_uids": ["user-uid"],
    "enable_string_uid": false,
    "idle_timeout": 30,
    "asr": {
      "language": "en-US",
      "task": "conversation"
    },
    "llm": {
      "url": "https://api.groq.com/openai/v1/chat/completions",
      "api_key": "groq-key",
      "system_messages": [{"role": "system", "content": "You are a helpful assistant."}],
      "greeting_message": "Hello! How can I help?",
      "failure_message": "Please wait a moment.",
      "max_history": 10,
      "params": {
        "model": "llama-3.3-70b-versatile",
        "max_tokens": 1024,
        "temperature": 0.7
      },
      "input_modalities": ["text"],
      "output_modalities": ["text", "audio"]
    },
    "vad": {
      "silence_duration_ms": 480,
      "speech_duration_ms": 15000,
      "threshold": 0.5,
      "interrupt_duration_ms": 160,
      "prefix_padding_ms": 300
    },
    "tts": {
      "vendor": "microsoft",
      "params": {
        "key": "azure-speech-key",
        "region": "eastus",
        "voice_name": "en-US-AndrewMultilingualNeural",
        "rate": 1.1,
        "volume": 70
      }
    }
  }
}
```

Response: `{ "agent_id": "xxx", "create_ts": 123, "state": "running" }`

### 3. Stop Agent (REST API)

```
POST {baseUrl}/{appId}/agents/{agent_id}/leave
Authorization: Basic base64(customerId:customerSecret)
```

### 4. Next.js Client Component (SSR-Disabled)

Agora uses WebRTC (`window` APIs) — must disable SSR:

```typescript
import dynamic from "next/dynamic";

const AgoraProvider = dynamic(async () => {
  const { AgoraRTCProvider, default: AgoraRTC } = await import("agora-rtc-react");
  return {
    default: ({ children }) => {
      const client = useMemo(
        () => AgoraRTC.createClient({ mode: "rtc", codec: "vp8" }), []
      );
      return <AgoraRTCProvider client={client}>{children}</AgoraRTCProvider>;
    },
  };
}, { ssr: false });

const VoiceChat = dynamic(() => import("./VoiceChat"), { ssr: false });
```

### 5. Voice Chat Component Hooks

```typescript
import {
  useRTCClient, useLocalMicrophoneTrack, useRemoteUsers,
  useClientEvent, useIsConnected, useJoin, usePublish, RemoteUser
} from "agora-rtc-react";

// Join channel
useJoin({ appid: APP_ID, channel, token, uid }, true);

// Publish local mic
const { localMicrophoneTrack } = useLocalMicrophoneTrack(true);
usePublish([localMicrophoneTrack]);

// Listen for agent
const remoteUsers = useRemoteUsers();
useClientEvent(client, "user-joined", (user) => { /* agent connected */ });
useClientEvent(client, "user-left", (user) => { /* agent disconnected */ });

// Token renewal
useClientEvent(client, "token-privilege-will-expire", async () => {
  const newToken = await fetchNewToken();
  await client.renewToken(newToken);
});

// Render remote audio
remoteUsers.map(user => <RemoteUser key={user.uid} user={user} />);
```

## TTS Providers

| Provider | Config Key | Voices |
|----------|-----------|--------|
| **Microsoft Azure** | `vendor: "microsoft"` | en-US-AndrewMultilingualNeural, en-US-AriaNeural |
| **ElevenLabs** | `vendor: "elevenlabs"` | Custom voice IDs, eleven_flash_v2_5 model |

### Microsoft TTS Config
```json
{ "vendor": "microsoft", "params": { "key": "...", "region": "eastus", "voice_name": "en-US-AndrewMultilingualNeural", "rate": 1.1, "volume": 70 } }
```

### ElevenLabs TTS Config
```json
{ "vendor": "elevenlabs", "params": { "key": "...", "voice_id": "XrExE9yKIg1WjnnlVkGX", "model_id": "eleven_flash_v2_5" } }
```

## LLM Providers for Voice Agent

Any OpenAI-compatible API works:

| Provider | URL | Model |
|----------|-----|-------|
| **Groq** | `https://api.groq.com/openai/v1/chat/completions` | llama-3.3-70b-versatile |
| **OpenAI** | `https://api.openai.com/v1/chat/completions` | gpt-4o-mini |
| **Together** | `https://api.together.xyz/v1/chat/completions` | meta-llama/Meta-Llama-3.1-70B |

## VAD (Voice Activity Detection) Tuning

| Parameter | Default | Purpose |
|-----------|---------|---------|
| `silence_duration_ms` | 480 | Silence before AI responds |
| `speech_duration_ms` | 15000 | Max user speech duration |
| `threshold` | 0.5 | Voice detection sensitivity (0-1) |
| `interrupt_duration_ms` | 160 | How quickly user can interrupt AI |
| `prefix_padding_ms` | 300 | Audio captured before speech detected |

Lower `silence_duration_ms` = faster responses but more false triggers.
Lower `interrupt_duration_ms` = easier to interrupt AI mid-sentence.

## Best Practices

1. **Never expose App Certificate or Customer Secret client-side** — generate tokens server-side only
2. **Use numeric UIDs** for simplicity; string UIDs require `enable_string_uid: true`
3. **Set idle_timeout** to auto-disconnect agents after silence (saves Conversational AI minutes)
4. **Keep system prompts voice-optimized** — short responses, no markdown, conversational tone
5. **Use `dynamic()` with `ssr: false`** for all Agora components in Next.js
6. **Implement token renewal** via `token-privilege-will-expire` event to avoid disconnections
7. **Test with the Agora Web Demo** at [webdemo.agora.io](https://webdemo.agora.io) before building custom UI
8. **Monitor usage** at console.agora.io to stay within free tier limits

## Common Pitfalls

| Pitfall | Impact | Fix |
|---------|--------|-----|
| SSR rendering Agora components | `window is not defined` crash | `dynamic(() => import(...), { ssr: false })` |
| Expired tokens | Silent disconnection | Listen for `token-privilege-will-expire`, renew proactively |
| Agent UID collision | Agent can't join channel | Use unique agent UIDs per session |
| No idle_timeout | Agent runs forever, burns minutes | Set `idle_timeout: 30` (seconds) |
| Long LLM responses | Slow voice replies, bad UX | Set `max_tokens: 256-512` for voice, use fast models |
| Missing `enable_string_uid` | Agent join fails silently | Set to `true` if agent UID contains letters |

## Reference Implementation

- Blog: https://www.agora.io/en/blog/build-a-conversational-ai-app-with-nextjs-and-agora/
- Repo: https://github.com/AgoraIO-Community/conversational-ai-nextjs-client
- Docs: https://docs.agora.io/en/conversational-ai/overview/product-overview
