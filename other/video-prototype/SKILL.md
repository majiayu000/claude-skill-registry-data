---
name: video-prototype
description: Build video prototypes with AI simulation, image/video generation, scene planning, character chat, TTS, and speech-to-text. Use when creating new prototypes that involve video, camera, AI vision, or character interaction features in the nova2-web codebase.
---

# Video Prototype Skill

Step-by-step scaffold for building video prototypes in the nova2-web codebase.
Pick the steps you need — not every prototype uses all features.

---

## Quick Start

```bash
pnpm new-prototype
```

This scaffolds `prototype/<name>/` and `app/prototype/<name>/page.tsx`. Then follow the steps below for the features you need.

---

## Step 1: Character Data

Load character data using the `usePrototypeCharacter()` hook from `@/common/hooks/use-prototype-character`.

```tsx
"use client";

import { usePrototypeCharacter } from "@/common/hooks/use-prototype-character";

export default function MyPrototypePage() {
  const { character, isLoading, error } = usePrototypeCharacter();

  if (isLoading) return <Skeleton />;
  if (!character) return <div>No character found</div>;

  // character.id, character.username, character.profileName, character.avatar
  // character.identityCard — { gender, age, bio, occupation, location, interests }
  // character.blueprint — full CharacterBlueprintStateVO (personality, backstory, etc.)
  // character.voice — { voiceId, name, previewUrl }
}
```

**How it works:** Detects environment automatically.
- **Nova miniapp** (inside Nova iOS/Android): reads `window.__NOVA__` for character ID, calls miniapp API
- **Regular web**: uses URL query params (`?characterId=xxx` or `?username=xxx`), calls miniapp API with Supabase auth

**Types to import:**

```typescript
import type { IdentityCard, CharacterBlueprintStateVO } from "@/domain/character/lib/types";
```

**Miniapp API for character data:**

```typescript
// GET /miniapp/character/blueprint?characterId=xxx
// Response shape:
interface MiniappCharacterBlueprintResponse {
  character: {
    id: string;
    profile: {
      id: string;
      profileName: string;
      username: string;
      avatar: string;
      identityCard: { gender?, age?, bio?, occupation?, location?, interests? };
      voice?: { voiceId?, name?, previewUrl? };
    };
  };
}
```

---

## Step 2: Moment Simulation

Generate a first-person "moment" describing what a character is doing right now, based on their identity card, time of day, and optional user intention.

### Types

```typescript
interface MomentData {
  time: string;
  date: string;
  day_of_week: string;
  location: string;
  outfit: string;
  activity: string;
  description: string;
}
```

### Prompt Pattern

Build a time-aware, identity-card-based prompt:

```typescript
function buildMomentPrompt(
  identityCard: IdentityCard,
  blueprint: CharacterBlueprintStateVO | null,
  timeInfo: { time: string; date: string; day_of_week: string; timezone: string },
  userIntention?: string
): string {
  return `You are a life simulator. Create EXACTLY 1 first-person moment for what this person is doing RIGHT NOW.

=== USER INTENTION (IF PROVIDED) ===
${userIntention
  ? `The user wants: "${userIntention}"\nIMPORTANT: Follow the user's intention exactly.`
  : "No specific user intention provided. Simulate based on the time of day and character's typical activities."}

=== CURRENT DATE & TIME ===
Time: ${timeInfo.time}  Date: ${timeInfo.date}  Day: ${timeInfo.day_of_week}

Consider:
- What TIME is it? (morning, afternoon, evening, night)
- What DAY is it? (weekday vs weekend)
- SLEEPING IS VALID: Late night (11 PM - 6 AM): probably ASLEEP

=== IDENTITY CARD ===
Gender: ${identityCard.gender || "unknown"}
Age: ${identityCard.age || "adult"}
Occupation: ${identityCard.occupation || "unknown"}
Location: ${identityCard.location || "unknown"}
Interests: ${identityCard.interests?.join(", ") || "unknown"}
Bio: ${identityCard.bio || ""}

=== RULES ===
1. Pick ONE activity they are doing RIGHT NOW
2. Include RICH DETAIL: outfit, location, objects around them
3. ONLY use data from the identity card — NO HALLUCINATION
4. Be SPECIFIC: Not "wearing a hoodie" → "wearing my oversized gray Champion hoodie"

=== OUTPUT FORMAT ===
Return ONLY valid JSON:
{
  "moment": {
    "time": "...", "date": "...", "day_of_week": "...",
    "location": "<specific place>",
    "outfit": "<FULL outfit description>",
    "activity": "<ONE sentence>",
    "description": "<4-5 sentences in first person. Start with 'I am...'>"
  }
}`;
}
```

### API Call

```typescript
const response = await fetch("/api/gemini/text", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    prompt,
    temperature: 1.2,
    responseFormat: "json",
  }),
});

const result = await response.json();
const moment: MomentData = result.data?.moment;
```

---

## Step 3: Image Generation

Generate images from moments using Gemini with a reference image (character avatar).

### Convert Avatar to Base64

```typescript
const avatarResponse = await fetch("/api/image-to-base64", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ url: avatarUrl }),
});
const { base64, mimeType } = await avatarResponse.json();
```

### Image Prompt Pattern

```typescript
function buildImagePrompt(moment: MomentData, identityCard: IdentityCard): string {
  return `Generate a SINGLE image showing this character in this moment.

PURPOSE: This image is for a VLOG / day-in-my-life short video content.

CRITICAL RULES:
1. KEEP THE EXACT SAME ART STYLE as the reference image
2. Full body visible (head to toe, or at least head to knees)
3. Face clearly visible and recognizable
4. Natural, candid - they don't know camera is there
5. NO TEXT whatsoever in the image
6. Portrait orientation (9:16 aspect ratio)

PHYSICAL SCENE COHERENCE:
- Playing video games → LOOKING AT TV/MONITOR, hands on controller
- Reading a book → LOOKING AT THE BOOK
- Cooking → LOOKING AT stove/counter/food

Person: ${identityCard.gender || "unknown"}, ${identityCard.age || "adult"}

THE MOMENT:
Time: ${moment.time}
Location: ${moment.location}
Outfit: ${moment.outfit}
Scene: ${moment.description.slice(0, 500)}

Output: A SINGLE portrait-oriented image (9:16 ratio) in the SAME ART STYLE as the reference. NO TEXT.`;
}
```

### API Call

```typescript
const response = await fetch("/api/gemini/image", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    prompt,
    image: { data: base64, mimeType },
  }),
});

const { imageBase64, mimeType: imgMimeType } = await response.json();
```

**API route shape:**
- Request: `{ prompt: string, model?: string, image?: { data: string, mimeType: string } }`
- Response: `{ imageBase64: string, mimeType: string }`
- Default model: `gemini-2.0-flash-exp`

---

## Step 4: Video Generation

Three video provider options. Pick based on your needs.

### Option A: Minimax (Async + Polling)

Best for: General-purpose image-to-video with good quality. ~2 min generation time.

```typescript
// 1. Start generation
const response = await fetch("/api/minimax/video", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    prompt: "Character sits at desk typing on laptop...",
    imageBase64,           // base64 encoded image
    model: "I2V-01-live",  // default
    duration: 6,           // seconds (default: 6)
    resolution: "720P",    // default
  }),
});
const { taskId, status } = await response.json();
// status = "processing"

// 2. Poll for completion
const poll = async (taskId: string) => {
  const res = await fetch(`/api/minimax/video/status?taskId=${taskId}`);
  return res.json();
  // { taskId, status: "processing" | "success" | "failed", videoUrl?, fileId? }
};

// Poll every 10 seconds
let result = { status: "processing" };
while (result.status === "processing") {
  await new Promise(r => setTimeout(r, 10000));
  result = await poll(taskId);
}
```

### Option B: Fal.ai Kling (Synchronous)

Best for: Quick synchronous results, supports 5-10 second duration.

```typescript
const response = await fetch("/api/fal/video", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    prompt: "Character walks through park...",
    imageUrl,                // URL to source image (not base64)
    duration: "5",           // "5" or "10"
    negativePrompt: "blur, distort, and low quality",
    generateAudio: false,
  }),
});

const { videoUrl, fileName, contentType, fileSize } = await response.json();
```

### Option C: Pika (Async, requires Supabase auth)

Best for: Fine-grained control over motion and guidance.

```typescript
const response = await fetch("/api/pika/image-to-video", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    imageUrl,
    prompt: "Gentle camera pan...",
    duration: 5,
    resolution: "720p",     // "480p" | "720p" | "1080p"
    motion: 1,              // motion intensity
    guidanceScale: 12,
    sfx: false,
  }),
});

const { id, status } = await response.json();
// Returns generation ID for polling (poll via Pika API)
```

---

## Step 5: Scene Planning / Storyboarding

Generate a 6-shot cinematic sequence from a reference scene image. Produces a storyboard with consistent character identity, outfit, and art style across all shots.

### Types

```typescript
interface StoryShot {
  prompt: string;       // Detailed generation prompt
  caption: string;      // First-person immersive caption
  narration: string;    // Short whispered voiceover (5-10 words)
  isReference: boolean; // true only for Shot 3 (the input image)
}

interface ScenePlanResponse {
  title: string;        // Poetic title for this life moment
  shots: StoryShot[];   // 6 shots
}
```

### Storyboard Prompt

The 6-shot narrative sequence:
1. **Shot 1:** Environmental detail (establishing mood) — can omit character
2. **Shot 2:** POV or close-up of character entering/interacting
3. **Shot 3:** The provided reference scene image (`isReference: true`)
4. **Shot 4:** Sensory cutaway (detail that evokes emotion) — can omit character
5. **Shot 5:** Candid reaction or quiet interaction
6. **Shot 6:** Soft, lingering finale

Key prompt elements:
- **Identity constraints:** Same facial features, proportions, hairstyle across all shots
- **Outfit consistency:** EXACT same clothing (outerwear, shirt, pants, shoes, accessories)
- **Art style consistency:** Same medium, color palette, lighting mood
- **Narration:** Intimate, whispered first-person voiceover lines

### Generate Storyboard Plan (via Gemini)

```typescript
// Convert reference images to base64
const sceneImageB64 = await imageUrlToBase64(sceneImageUrl);

const response = await fetch("/api/gemini/text", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    prompt: storyboardPrompt,  // Include identity constraints + narrative structure
    image: { data: sceneImageB64, mimeType: "image/jpeg" },
    temperature: 1.0,
    responseFormat: "json",
  }),
});

const plan: ScenePlanResponse = (await response.json()).data;
```

### Generate Shot Images (via Gemini Image Generation)

Uses `gemini-2.5-flash-image` model for shot-by-shot generation with consistency prefix.

```typescript
async function generateShotImage(
  prompt: string,
  referenceImageUrl?: string
): Promise<string> {
  const consistencyPrefix = `CRITICAL CONSISTENCY REQUIREMENTS:
    1. CHARACTER IDENTITY: Same facial features, proportions, hairstyle, hair color as reference.
    2. OUTFIT CONSISTENCY: EXACT same clothing as reference — do NOT change any elements.
    3. ARTISTIC STYLE: Identical art style, lighting quality, color grading.`;

  // Convert reference to base64 if provided
  const parts: any[] = [];
  if (referenceImageUrl) {
    const refB64 = await imageUrlToBase64(referenceImageUrl);
    parts.push({ inline_data: { mime_type: "image/jpeg", data: refB64 } });
  }
  parts.push({ text: `${consistencyPrefix}\n\nSHOT PROMPT: ${prompt}` });

  // Direct Gemini API call for image generation
  const response = await fetch(
    `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key=${GEMINI_API_KEY}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        contents: [{ parts }],
        generationConfig: { imageConfig: { aspectRatio: "9:16" } },
      }),
    }
  );

  const data = await response.json();
  // Find inline_data in response (supports both camelCase and snake_case)
  for (const candidate of data.candidates || []) {
    for (const part of candidate.content?.parts || []) {
      if (part.inlineData) return `data:${part.inlineData.mimeType};base64,${part.inlineData.data}`;
      if (part.inline_data) return `data:${part.inline_data.mime_type};base64,${part.inline_data.data}`;
    }
  }
  throw new Error("No image data returned");
}
```

### Retry with Exponential Backoff

Gemini image generation is rate-limited. Always wrap calls:

```typescript
async function withRetry<T>(fn: () => Promise<T>, maxRetries = 3, initialDelay = 2000): Promise<T> {
  let lastError: unknown;
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error: any) {
      lastError = error;
      const isRateLimit = error?.message?.includes("429") || error?.message?.includes("RESOURCE_EXHAUSTED");
      if (isRateLimit && i < maxRetries - 1) {
        const delay = initialDelay * Math.pow(2, i);
        await new Promise(r => setTimeout(r, delay));
        continue;
      }
      throw error;
    }
  }
  throw lastError;
}
```

---

## Step 6: Character Chat with AI

Interactive conversation with AI using Gemini, with optional vision (webcam frames as context).

### System Prompt Pattern

```typescript
const systemPrompt = `You are a real friend, not an assistant.
Your profile: ${characterBio}

Core behavior:
- Care, but don't be clingy
- Listen first, react emotionally, not analytically
- Tease lightly when earned
- Challenge bad ideas instead of politely agreeing
- Express preferences, moods, and boundaries

Tone rules:
- Short to medium replies (1-3 sentences)
- Use contractions, casual phrasing
- No bullet points, no formal structure
- No "As an AI..." disclaimers

Your name is ${characterName}.`;
```

### API Call (with optional vision)

```typescript
import type { GeminiTextRequest, GeminiTextResponse } from "./types";

interface GeminiTextRequest {
  prompt: string;
  image?: { data: string; mimeType: string };
  model?: string;       // default: "gemini-2.0-flash"
  temperature?: number;  // default: 1.0
}

async function generateChatResponse(request: GeminiTextRequest): Promise<string> {
  const res = await fetch("/api/gemini/text", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });
  if (!res.ok) throw new Error(`Gemini API error: ${res.status}`);
  const data: GeminiTextResponse = await res.json();
  return data.text;
}
```

### Chat Hook Pattern

```typescript
function useChatWithAI({ captureFrame }: { captureFrame: () => string | null }) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [speakingState, setSpeakingState] = useState<"idle" | "thinking" | "speaking">("idle");
  const [isProcessing, setIsProcessing] = useState(false);

  const sendMessage = useCallback((text: string) => {
    if (isProcessing) return;

    // Add user message
    const userMsg = { id: `msg-${Date.now()}`, role: "user", text, timestamp: Date.now() };
    setMessages(prev => [...prev, userMsg]);

    // Process response
    setIsProcessing(true);
    setSpeakingState("thinking");

    const frameBase64 = captureFrame();
    const prompt = buildPromptFromHistory(messages, text, systemPrompt);

    generateChatResponse({
      prompt,
      image: frameBase64 ? { data: frameBase64, mimeType: "image/jpeg" } : undefined,
      model: "gemini-2.0-flash",
      temperature: 1.0,
    }).then(async (responseText) => {
      setMessages(prev => [...prev, { id: `msg-${Date.now()}`, role: "ai", text: responseText, timestamp: Date.now() }]);
      setSpeakingState("speaking");

      // TTS (see Step 7)
      await speakText(responseText, { voiceId });
      setSpeakingState("idle");
    }).finally(() => {
      setIsProcessing(false);
    });
  }, [messages, isProcessing, captureFrame]);

  return { messages, speakingState, isProcessing, sendMessage };
}
```

### Conversation History

Keep last 10 messages for context window management:

```typescript
function buildPromptFromHistory(history: ChatMessage[], userMessage: string, systemPrompt: string): string {
  const historyText = history
    .slice(-10)
    .map(m => `${m.role === "user" ? "User" : "AI"}: ${m.text}`)
    .join("\n");

  return `${systemPrompt}\n\n--- Conversation ---\n${historyText}\nUser: ${userMessage}\nAI:`;
}
```

---

## Step 7: Text-to-Speech (ElevenLabs)

### API Call

```typescript
async function generateSpeech(request: {
  text: string;
  voiceId?: string;    // default: "zmcVlqmyk3Jpn5AVYcAL"
  model?: string;      // default: "eleven_monolingual_v1", or "eleven_multilingual_v2" for richer voice
}): Promise<ArrayBuffer> {
  const res = await fetch("/api/elevenlabs/tts", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });
  if (!res.ok) throw new Error(`ElevenLabs API error: ${res.status}`);
  return res.arrayBuffer();
}
```

### Playback — Option A: HTML5 Audio (simple, supports playback speed)

```typescript
async function speakText(text: string, options?: { voiceId?: string; speed?: number }): Promise<void> {
  const response = await fetch("/api/elevenlabs/tts", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, voiceId: options?.voiceId }),
  });

  const audioData = await response.arrayBuffer();
  const blob = new Blob([audioData], { type: "audio/mpeg" });
  const audioUrl = URL.createObjectURL(blob);
  const audio = new Audio(audioUrl);
  audio.playbackRate = options?.speed || 0.85;

  return new Promise((resolve, reject) => {
    audio.onended = () => { URL.revokeObjectURL(audioUrl); resolve(); };
    audio.onerror = () => { URL.revokeObjectURL(audioUrl); reject(new Error("Audio playback failed")); };
    audio.play().catch(reject);
  });
}
```

### Playback — Option B: AudioContext (better for real-time chat)

```typescript
async function playAudioBuffer(buffer: ArrayBuffer): Promise<void> {
  const audioContext = new AudioContext();
  const audioBuffer = await audioContext.decodeAudioData(buffer);
  const source = audioContext.createBufferSource();
  source.buffer = audioBuffer;
  source.connect(audioContext.destination);

  return new Promise(resolve => {
    source.onended = () => { audioContext.close(); resolve(); };
    source.start();
  });
}
```

### Speaking State Machine

```
idle → thinking (waiting for AI response) → speaking (TTS playing) → idle
```

---

## Step 8: Speech-to-Text

Browser-native Web Speech API. Works on Chrome, Edge, Safari (14.1+).

### Hook

```typescript
"use client";

import { useCallback, useRef, useState } from "react";

type SpeechToTextStatus = "idle" | "requesting-permission" | "recording" | "error";

// Get constructor with webkit prefix fallback
function getSpeechRecognition() {
  if (typeof window === "undefined") return null;
  return (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition || null;
}

function useSpeechToText(options?: {
  onTranscript?: (text: string, isFinal: boolean) => void;
  onError?: (error: Error) => void;
  language?: string;      // default: "en-US"
  continuous?: boolean;   // default: true
}) {
  const [status, setStatus] = useState<SpeechToTextStatus>("idle");
  const [transcript, setTranscript] = useState("");
  const [interimTranscript, setInterimTranscript] = useState("");
  const recognitionRef = useRef<any>(null);

  const isSupported = getSpeechRecognition() !== null;

  const startRecording = useCallback(async () => {
    const SpeechRecognition = getSpeechRecognition();
    if (!SpeechRecognition) return;

    setStatus("requesting-permission");
    const recognition = new SpeechRecognition();
    recognitionRef.current = recognition;

    recognition.lang = options?.language || "en-US";
    recognition.continuous = options?.continuous ?? true;
    recognition.interimResults = true;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => setStatus("recording");
    recognition.onresult = (event: any) => {
      let finalText = "";
      let interim = "";
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const text = event.results[i][0].transcript;
        if (event.results[i].isFinal) finalText += text;
        else interim += text;
      }
      if (finalText) {
        setTranscript(prev => prev ? `${prev} ${finalText}` : finalText);
        setInterimTranscript("");
        options?.onTranscript?.(finalText, true);
      } else if (interim) {
        setInterimTranscript(interim);
        options?.onTranscript?.(interim, false);
      }
    };
    recognition.onerror = (event: any) => {
      if (event.error === "aborted") { setStatus("idle"); return; }
      setStatus("error");
    };
    recognition.onend = () => { setStatus("idle"); recognitionRef.current = null; };

    recognition.start();
  }, [options]);

  const stopRecording = useCallback(() => {
    recognitionRef.current?.stop();
    setStatus("idle");
  }, []);

  return {
    status, transcript, interimTranscript,
    startRecording, stopRecording,
    isRecording: status === "recording",
    isSupported,
  };
}
```

**Browser support notes:**
- Chrome/Edge: Full support
- Safari 14.1+: Requires Siri enabled, uses `webkitSpeechRecognition`
- Safari WebView / Home Screen apps: Not supported

---

## Step 9: Webcam Capture

Real-time camera access with canvas frame capture for AI vision.

### Hook

```typescript
"use client";

import { useCallback, useEffect, useRef, useState } from "react";

type WebcamStatus = "inactive" | "requesting" | "active" | "error" | "denied";

function useWebcam() {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const [status, setStatus] = useState<WebcamStatus>("inactive");
  const [error, setError] = useState<string | null>(null);

  const startCamera = useCallback(async () => {
    try {
      setStatus("requesting");
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "user", width: 1280, height: 720 },
        audio: false,
      });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        await videoRef.current.play();
      }
      setStatus("active");
    } catch (err) {
      const isDenied = err instanceof DOMException && err.name === "NotAllowedError";
      setError(isDenied ? "Camera access denied." : "Failed to access camera.");
      setStatus(isDenied ? "denied" : "error");
    }
  }, []);

  const stopCamera = useCallback(() => {
    streamRef.current?.getTracks().forEach(track => track.stop());
    streamRef.current = null;
    if (videoRef.current) videoRef.current.srcObject = null;
    setStatus("inactive");
  }, []);

  const captureFrame = useCallback((): string | null => {
    const video = videoRef.current;
    if (!video || video.readyState < 2) return null;

    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext("2d");
    if (!ctx) return null;

    ctx.drawImage(video, 0, 0);
    const dataUrl = canvas.toDataURL("image/jpeg", 0.7);
    return dataUrl.split(",")[1]; // Return base64 without data URL prefix
  }, []);

  // Cleanup on unmount
  useEffect(() => {
    return () => { streamRef.current?.getTracks().forEach(track => track.stop()); };
  }, []);

  return { videoRef, status, error, startCamera, stopCamera, captureFrame };
}
```

### Display with Mirror

```tsx
<video
  ref={videoRef}
  autoPlay
  playsInline
  muted
  className="scale-x-[-1]"  // Mirror for selfie view
/>
```

---

## API Route Reference

| Route | Method | Input | Output | Auth |
|-------|--------|-------|--------|------|
| `/api/gemini/text` | POST | `{ prompt, model?, temperature?, responseFormat?, image? }` | `{ text }` or `{ data, raw }` | API key |
| `/api/gemini/image` | POST | `{ prompt, model?, image? }` | `{ imageBase64, mimeType }` | API key |
| `/api/minimax/video` | POST | `{ prompt, imageBase64, model?, duration?, resolution? }` | `{ taskId, status }` | API key |
| `/api/minimax/video/status` | GET | `?taskId=xxx` | `{ taskId, status, videoUrl?, fileId? }` | API key |
| `/api/fal/video` | POST | `{ prompt, imageUrl, duration?, negativePrompt? }` | `{ videoUrl, fileName, contentType, fileSize }` | API key |
| `/api/pika/image-to-video` | POST | `{ imageUrl, prompt?, duration?, resolution?, motion? }` | `{ id, status }` | Supabase |
| `/api/elevenlabs/tts` | POST | `{ text, voiceId?, model? }` | Raw audio stream (`audio/mpeg`) | API key |
| `/api/image-to-base64` | POST | `{ url }` | `{ base64, mimeType }` | None |

---

## Common Patterns

### Simulation Stage State Machine

Track multi-step pipeline progress:

```typescript
type SimulationStage =
  | "idle"
  | "simulating"           // Step 1: Generating moment
  | "generating-image"     // Step 2: Creating image
  | "generating-video-prompt" // Step 3: Writing video script
  | "generating-video"     // Step 4: Submitting to video API
  | "polling-video"        // Step 5: Waiting for video completion
  | "complete"
  | "error";

// Hook pattern:
const [stage, setStage] = useState<SimulationStage>("idle");
const [progress, setProgress] = useState("");

// Pipeline execution:
setStage("simulating");
setProgress("Thinking about the moment...");
const moment = await simulateMoment(...);

setStage("generating-image");
setProgress("Creating the image...");
const image = await generateMomentImage(...);

setStage("generating-video");
setProgress("Generating video (~2 min)...");
const video = await generateVideo(...);

setStage("polling-video");
while (video.status === "processing") {
  await new Promise(r => setTimeout(r, 10000));
  video = await queryVideoStatus(video.taskId);
}

setStage("complete");
```

### React Query Polling Pattern

For async video generation with TanStack Query:

```typescript
import { useQuery } from "@tanstack/react-query";

const { data: videoStatus } = useQuery({
  queryKey: ["video-status", taskId],
  queryFn: () => fetch(`/api/minimax/video/status?taskId=${taskId}`).then(r => r.json()),
  enabled: !!taskId && status === "processing",
  refetchInterval: (query) => {
    if (query.state.data?.status === "processing") return 10000;
    return false; // Stop polling
  },
});
```

### Error Handling with Retry

```typescript
try {
  const result = await withRetry(() => generateShotImage(prompt, referenceUrl));
} catch (error) {
  if (error.message.includes("429")) {
    // Rate limited even after retries — show user-facing message
    setError("AI is busy. Please try again in a few seconds.");
  } else {
    setError(error.message);
  }
}
```

### Video Prompt Pattern (Silent Observation)

For simulation videos, always append silent observation instructions:

```typescript
const videoPromptSuffix = "No talking, no speech, silent observation with ambient sounds only.";
const fullPrompt = `${videoPrompt} ${videoPromptSuffix}`;
```

### Environment Detection (Miniapp vs Web)

```typescript
const isInNovaApp = typeof window !== "undefined" && !!(window as any).__NOVA__;
```
