---
name: firebase-ai-logic
description: Guide for integrating Gemini AI models with Firebase using Firebase AI Logic SDK. This skill should be used when implementing Gemini features (chat, content generation, structured JSON output), configuring security (App Check), or troubleshooting issues (rate limits, schema errors).
---

# Firebase AI Logic

## Overview

Firebase AI Logic enables secure, client-side integration with Google's Gemini AI models through Firebase SDKs. This skill provides production-ready patterns for implementing AI features including chat, structured output (JSON), streaming responses, cost optimization, and security best practices. Renamed from "Vertex AI in Firebase" in May 2025.

## When to Use This Skill

This skill should be used when working with:
- Gemini API integration via Firebase (Web, Android, iOS, Flutter, React Native, Unity)
- Structured JSON output with responseSchema (saving to Firestore/databases)
- Multi-turn chat conversations with automatic history management
- Streaming responses for real-time UI updates
- System instructions for model behavior customization
- Security configuration (App Check, API key protection, rate limiting)
- Cost optimization (token counting, prompt optimization, batch processing)
- Troubleshooting AI Logic errors (429 rate limits, schema validation, location mismatches)

## Core Setup & Security

### Initialize Firebase AI Logic

```typescript
import { initializeApp } from 'firebase/app';
import { getAI, getGenerativeModel } from 'firebase/ai';

const app = initializeApp({
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  // ... other config
});

const ai = getAI(app);
const model = getGenerativeModel(ai, {
  model: 'gemini-2.5-flash-lite',
});
```

### Security Setup (CRITICAL for Production)

**Enable App Check to prevent API abuse:**

```typescript
import { initializeAppCheck, ReCaptchaV3Provider } from 'firebase/app-check';

const appCheck = initializeAppCheck(app, {
  provider: new ReCaptchaV3Provider('YOUR_RECAPTCHA_SITE_KEY'),
  isTokenAutoRefreshEnabled: true,
});
```

**Why App Check is critical:**
- Prevents abuse of Gemini API quota
- Verifies requests come from legitimate app and authentic devices
- Protects against unauthorized API usage and unexpected costs
- Supports both Gemini Developer API and Vertex AI Gemini API
- Future: Replay protection with limited-use tokens

**Platform-Specific Configuration:**

**Web:**
```typescript
import { initializeAppCheck, ReCaptchaV3Provider } from 'firebase/app-check';

const appCheck = initializeAppCheck(app, {
  provider: new ReCaptchaV3Provider('YOUR_RECAPTCHA_SITE_KEY'),
  isTokenAutoRefreshEnabled: true,
});
```

**Flutter (requires explicit App Check passing):**
```dart
// Flutter requires passing App Check during AI initialization
final appCheck = FirebaseAppCheck.instance;
await appCheck.activate();
```

**Development Mode:**
```typescript
if (process.env.NODE_ENV === 'development') {
  (window as any).FIREBASE_APPCHECK_DEBUG_TOKEN = true;
}
// Add debug token from console to Firebase Console → App Check → Debug tokens
```

**API Key Security Rules:**
- NEVER add "Generative Language API" to Firebase API key allowlist (exposes key to abuse)
- API key stays on Firebase backend (never in client code)
- Review API restrictions regularly in Firebase Console
- App Check keeps your Gemini API key on the server, not embedded in app code

## Key Implementation Patterns

### 1. Structured Output (JSON Schema)

Generate consistent JSON for Firestore/database storage:

```typescript
import { Schema } from 'firebase/ai';

const reviewAnalysisSchema = Schema.object({
  properties: {
    sentiment: Schema.string(),
    rating: Schema.number(),
    categories: Schema.array({ items: Schema.string() }),
    summary: Schema.string(),
  },
  optionalProperties: ["summary"],
});

const model = getGenerativeModel(ai, {
  model: 'gemini-2.5-flash-lite',
  generationConfig: {
    responseMimeType: 'application/json',
    responseSchema: reviewAnalysisSchema,
  },
});

const result = await model.generateContent('Great product! Fast shipping.');
const analysis = JSON.parse(result.response.text());
await setDoc(doc(db, 'reviews', id), analysis);
```

**Schema Constraints (CRITICAL):**

AVOID these (cause InvalidArgument errors):
- ❌ Union types: `["string", "null"]`
- ❌ Conditionals: `if`, `then`, `allOf`, `oneOf`, `not`
- ❌ String constraints: `minLength`, `pattern`, `maxLength`
- ❌ `$ref` references
- ❌ Default values

USE only:
- ✅ Basic types: `string`, `number`, `boolean`, `array`, `object`
- ✅ `optionalProperties` array for optional fields
- ✅ Simple nested objects and arrays
- ✅ Enums (keep values list short, <10 items)

**For complex validation, combine simple schema with Zod:**

```typescript
import { z } from 'zod';

// Simple schema for Gemini
const simpleSchema = Schema.object({
  properties: {
    categories: Schema.array({ items: Schema.string() }),
    summary: Schema.string(),
  }
});

// Detailed validation with Zod
const Validator = z.object({
  categories: z.array(z.enum(['tech', 'business', 'sports', 'other'])),
  summary: z.string().min(20).max(200),
});

const result = await model.generateContent(prompt);
const raw = JSON.parse(result.response.text());
const validated = Validator.parse(raw); // Throws if invalid
```

### 2. Multi-turn Chat with History

```typescript
const chat = model.startChat({
  history: [
    { role: 'user', parts: [{ text: 'Hi!' }] },
    { role: 'model', parts: [{ text: 'Hello! How can I help?' }] },
  ],
});

const result = await chat.sendMessage('How are you?');
console.log(result.response.text());
```

**Cost optimization - limit history:**

```typescript
// ✅ GOOD: Keep recent context only
const chat = model.startChat({
  history: recentMessages.slice(-20) // Last 20 messages
});
```

### 3. Streaming Responses

```typescript
const result = await chat.sendMessageStream('Write a long response...');

for await (const chunk of result.stream) {
  console.log(chunk.text()); // Display in real-time UI
}

const finalResponse = await result.response;
```

**When to use streaming:**
- ✅ Chat UI (word-by-word text appearance)
- ✅ Long responses (reduces perceived latency)
- ✅ Better UX for real-time interactions
- ❌ Skip if full response needed before processing

### 4. System Instructions

Define model behavior before any user prompts:

```typescript
const model = getGenerativeModel(ai, {
  model: 'gemini-2.5-flash-lite',
  systemInstruction: `You are a customer support assistant.
Be helpful, patient, and professional.
Escalate complex issues to human agents.`,
});
```

**Best practices:**
- System instructions act as a "preamble" to all prompts
- Do NOT put sensitive data in system instructions (not jailbreak-proof)
- Use Remote Config to update instructions without app rebuild
- Keep instructions concise (reduces token cost)

### 5. Error Handling & Rate Limits

Handle 429 (Rate Limit Exceeded) with exponential backoff:

```typescript
async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  maxRetries = 3
): Promise<T> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error: any) {
      if (error.code === 429 && i < maxRetries - 1) {
        const delay = Math.pow(2, i) * 1000 + Math.random() * 1000;
        await new Promise(resolve => setTimeout(resolve, delay));
      } else {
        throw error;
      }
    }
  }
  throw new Error('Max retries exceeded');
}

const result = await retryWithBackoff(() => model.generateContent(prompt));
```

## Cost Optimization Strategies

### 1. Count Tokens Before Requests

```typescript
// countTokens is a METHOD on the model, not a standalone function
const response = await model.countTokens(prompt);
const totalTokens = response.totalTokens;

console.log(`Estimated: ${totalTokens} tokens`);

if (totalTokens > 10000) {
  console.warn('High token usage - consider shortening prompt');
}

// Alternative: count tokens for structured request
const response2 = await model.countTokens({
  contents: [{ role: 'user', parts: [{ text: prompt }] }],
});
```

### 2. Optimize Prompts (40-50% Reduction)

```typescript
// ❌ BAD: Verbose
const badPrompt = `I would like you to carefully analyze...
Please provide detailed analysis... "${text}"`;

// ✅ GOOD: Concise
const goodPrompt = `Analyze sentiment:\n"${text}"`;
```

### 3. Batch Processing

```typescript
// ✅ GOOD: Process multiple items in one request
const prompt = `Classify these articles:
1. "${article1}"
2. "${article2}"
3. "${article3}"
Return JSON array.`;
```

## New Features (2025)

### 1. Thinking Models & Thinking Budget

Gemini 2.5 Flash Lite is a reasoning model with configurable thinking budget:

```typescript
const model = getGenerativeModel(ai, {
  model: 'gemini-2.5-flash-lite',
  generationConfig: {
    thinkingBudget: 'low',  // 'low', 'medium', 'high', or off (default)
  },
});
```

**Thinking Budget Guidelines:**
- **Off (default):** Fastest, lowest cost - use for simple tasks
- **Low:** Quick classification, basic analysis
- **Medium:** Moderate complexity reasoning
- **High:** Complex multi-step planning (slower, more expensive)

### 2. Gemini Live API

Natural voice conversations with real-time interruption support:

**Features:**
- Bidirectional voice streaming
- Interrupt model mid-response
- Low-latency audio processing
- No-cost option via Gemini Developer API

**Supported Platforms:**
- Web, Flutter, Unity, Android SDKs

### 3. Unity SDK Support

Official Firebase AI Logic SDK for Unity:

**Use Cases:**
- Game development
- Android XR experiences
- Interactive 3D applications

**Status:** Preview (2025)

## Production Checklist

**Security:**
- [ ] App Check enabled (reCAPTCHA for Web, Play Integrity/DeviceCheck for mobile)
- [ ] API restrictions reviewed (Gemini Developer API NOT in Firebase API key allowlist)
- [ ] Rate limits customized per user tier
- [ ] System instructions do not contain sensitive data

**Performance:**
- [ ] Use stable model version: `gemini-2.5-flash-lite`
- [ ] Model name managed via Remote Config (update without rebuild)
- [ ] Streaming enabled for long responses
- [ ] On-device inference enabled where appropriate
- [ ] Thinking budget configured appropriately (off by default for speed)

**Cost:**
- [ ] AI Monitoring enabled (track tokens, requests, errors)
- [ ] Budget alerts configured in Cloud Console
- [ ] Token counting implemented for large operations
- [ ] Prompts optimized (concise, no duplication)
- [ ] Chat history limited to recent context

**Quality:**
- [ ] System instructions tested with real use cases
- [ ] Response schemas validated (no unions, conditionals, or constraints)
- [ ] Output validated with Zod or similar library
- [ ] Error handling with retry + exponential backoff

**Location Configuration:**
- [ ] gemini-2.5-flash-lite uses default location (us-central1)
- [ ] No location override needed for stable models

## Official Model - Gemini 2.5 Flash Lite

**gemini-2.5-flash-lite** is the recommended model for this project:

**Specifications:**
- Context window: 1M tokens
- Max output: 65.5K tokens
- Knowledge cutoff: January 1, 2025
- Thinking budget: Configurable (off by default for speed/cost)

**Pricing (2025):**
- **Standard Tier:**
  - Input: $0.10/1M tokens (text/image/video) or $0.30/1M (audio)
  - Output: $0.40/1M tokens
- **Batch Tier:**
  - Input: $0.05/1M tokens (text/image/video) or $0.15/1M (audio)
  - Output: $0.20/1M tokens

**FREE Tier Limits (2025):**
- 1,000 requests per day (RPD)
- 15 requests per minute (RPM)
- 250,000 tokens per minute (TPM)

**Ideal for:**
- High-volume applications
- Low-latency requirements
- Cost-conscious deployments
- Real-time interactions

**Retired Models (NEVER USE):**
All Gemini 1.0 and 1.5 models return 404 errors:
- ❌ gemini-1.5-pro
- ❌ gemini-1.5-flash
- ❌ gemini-1.0-pro

**MUST migrate to:**
- ✅ gemini-2.5-flash-lite (ONLY model used)

## Advanced Features

### features/vision-multimodal.md
Image analysis capabilities including OCR, object detection, captions, and categorization. Supports PNG, JPEG, WebP formats.

**Load when needed:**
```
Read features/vision-multimodal.md for image analysis implementation
```

### features/structured-output.md
Comprehensive guide for enforcing deterministic JSON/enums with `responseSchema`. Highlights schema patterns, optional vs. required fields, and limitations such as the incompatibility with `generateContentStream` when `responseMimeType` is `application/json`.

**Load when needed:**
```
Read features/structured-output.md for schema design, validation tips, and fallback strategies
```

### features/function-calling.md
Enable Gemini to call external APIs, Cloud Functions, and tools. Implement dynamic integrations with real-time data sources.

**Load when needed:**
```
Read features/function-calling.md for tool use and API integration
```

### features/grounding.md
Connect Gemini to real-time Google Search for up-to-date information, fact-checking, and source attribution.

**Load when needed:**
```
Read features/grounding.md for Google Search grounding implementation
```

### features/code-execution.md
Let Gemini generate and execute Python code iteratively for mathematical calculations, data analysis, and visualizations.

**Load when needed:**
```
Read features/code-execution.md for Python code execution
```

### features/imagen.md
Generate and edit images using Imagen models. Text-to-image, inpainting, outpainting, and style customization.

**Load when needed:**
```
Read features/imagen.md for image generation and editing
```

### features/video-audio.md
Process video, audio, and PDF content. Video analysis, audio transcription, and document understanding.

**Load when needed:**
```
Read features/video-audio.md for multimodal content processing
```

### features/hybrid-inference.md
Automatic fallback between on-device Gemini Nano and cloud models for privacy, offline capability, and cost savings.

**Load when needed:**
```
Read features/hybrid-inference.md for on-device inference
```

### features/gemini-live.md
Real-time voice conversations with bidirectional streaming, natural speech, and interruption support.

**Load when needed:**
```
Read features/gemini-live.md for voice conversation implementation
```

### features/file-upload.md
Handle large files (videos, PDFs, audio) via Cloud Storage URLs for Vertex AI Gemini API.

**Load when needed:**
```
Read features/file-upload.md for large file handling
```

## Bundled Resources

### references/examples.md
Complete production-ready code examples:
- Content analysis with Firestore integration
- Multi-turn conversational chat
- Batch processing multiple items
- On-device privacy-first classification
- Cost-optimized implementations
- Customer support chatbot
- Product review analyzer

**Load when needed:**
```
Read references/examples.md for complete implementation examples
```

### references/troubleshooting.md
Solutions for common issues:
- Schema validation errors (InvalidArgument: 400)
- Rate limit exceeded (429) handling
- Location mismatch errors
- App Check configuration
- Token optimization strategies
- Model response quality issues
- Firestore integration errors

**Load when needed:**
```
Read references/troubleshooting.md for error solutions
```

### references/anti-patterns.md
Common mistakes to avoid:
- Location mismatch (preview models need `location: 'global'`)
- Exposing API key in allowlist
- No App Check in production
- Duplicating schema in prompt
- Not handling 429 errors
- Sensitive data in system instructions
- Using auto-updated aliases in production
- Not monitoring costs
- Unlimited chat history
- Not validating model output

**Load when needed:**
```
Read references/anti-patterns.md for common mistakes and solutions
```

## Quick Reference

**Key Imports:**
```typescript
import { getAI, getGenerativeModel, Schema } from 'firebase/ai';
import { initializeAppCheck, ReCaptchaV3Provider } from 'firebase/app-check';

// Note: countTokens is a METHOD on the model instance, not an exported function
// Usage: await model.countTokens(prompt)
```

**Official Documentation:**
- https://firebase.google.com/docs/ai-logic
- https://firebase.google.com/docs/ai-logic/get-started
- https://firebase.google.com/docs/ai-logic/generate-structured-output
- https://firebase.google.com/docs/ai-logic/chat
- https://firebase.google.com/docs/ai-logic/production-checklist
