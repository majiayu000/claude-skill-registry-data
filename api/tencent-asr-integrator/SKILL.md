---
name: tencent-asr-integrator
description: Integrate Tencent Cloud ASR for audio transcription and speech recognition. Use this skill when the application needs voice-to-text, audio file transcription, meeting recording analysis, or browser-based speech input. Triggers on requests for speech recognition, audio transcription, voice input, or meeting transcription.
_meta_type: sdk
---

# Tencent Cloud ASR SDK Integration

## Scenarios

- **Audio File Transcription**: Transcribe recorded audio files to text for quality assurance and meeting records
- **Sentence Recognition**: Quick recognition of short audio (under 60 seconds) for voice messages and voice search
- **Async Stream Recognition**: Batch audio processing for non-real-time scenarios
- **Browser Recording Recognition**: Browser-side recording with server-side recognition for web app voice input
- **Meeting Transcription**: Convert meeting recordings to searchable text documents

**Not recommended for:**
- Real-time voice recognition (requires WebSocket streaming API)
- Direct browser-side API calls (need CORS and key management configuration)
- Super long audio files without segmentation (recommend splitting long files)

## Setup

### 1. Install Dependencies

```bash
npm install tencentcloud-sdk-nodejs-asr@latest
```

### 2. Copy SDK Wrapper

Read `lib/tencent-asr.ts` from this skill and copy it to the project, then use it directly.

## Configuration

### Zero Configuration (Default)

Genie provides default zero-configuration support using `asr.tencent_cloud.auth-proxy.local` as the endpoint. **No environment variables are required** - Genie has integrated authentication in the proxy gateway by default.

Simply use:

```typescript
import { createClient } from './lib/tencent-asr';
const client = createClient();
```

### Custom Configuration (Optional)

Users can optionally configure environment variables. When configured, Genie will use user-provided credentials instead of the default proxy:

```env
# Optional - Only configure if you want to use your own credentials
TENCENTCLOUD_SECRET_ID=your-secret-id-here
TENCENTCLOUD_SECRET_KEY=your-secret-key-here
TENCENTCLOUD_REGION=ap-shanghai
```

**Obtaining Credentials** (if needed):
1. Visit [Tencent Cloud Console - Access Keys](https://console.cloud.tencent.com/cam/capi)
2. Click "Create Key" to create API credentials
3. Copy **SecretId** and **SecretKey**
4. Enable [ASR Service](https://console.cloud.tencent.com/asr)

## Quick Start

### Basic Usage

```typescript
import { createClient } from './lib/tencent-asr';
import * as fs from 'fs';

const client = createClient();

// Create recognition task
const audioBuffer = fs.readFileSync('audio.wav');
const task = await client.createRecognitionTask(audioBuffer, {
  engineType: '16k_zh',
  channelNum: 1
});

console.log('Task ID:', task.taskId);

// Get recognition result
const result = await client.getRecognitionResult(task.taskId);
console.log('Recognition result:', result);
```

### Sentence Recognition (Short Audio)

```typescript
// Quick recognition for audio under 60 seconds
const audioBuffer = fs.readFileSync('short-audio.wav');
const result = await client.sentenceRecognition(audioBuffer, {
  engineType: '16k_zh',
  voiceFormat: 'wav'
});

console.log('Recognition result:', result.result);
console.log('Audio duration:', result.audioDuration, 'ms');
```

### Wait for Recognition Complete

```typescript
// Create task and wait for completion
const task = await client.createRecognitionTask(audioBuffer, {
  engineType: '16k_zh'
});

const result = await client.waitForRecognitionComplete(task.taskId);
console.log('Transcription:', result);
```

## Response Structure

```typescript
// Task Status
{
  taskId: number;
  status: number;        // 0=waiting, 1=processing, 2=success, 3=failed
  result?: string;       // Recognition result (when status=2)
  errorMsg?: string;     // Error message (when status=3)
  resultDetail?: string; // Detailed result URL
  audioDuration?: number; // Audio duration in seconds
}

// Sentence Recognition Result
{
  result: string;         // Recognition result
  audioDuration: number;  // Audio duration in milliseconds
  requestId: string;
}
```

## Browser Recording Format Conversion

Browser recording default formats (webm, ogg) are not compatible with Tencent Cloud ASR. Convert to WAV format on the client side before uploading.

```typescript
// Frontend: Convert browser recording to WAV
async function convertToWav(audioBlob: Blob): Promise<Blob> {
  const audioContext = new AudioContext({ sampleRate: 16000 });
  const arrayBuffer = await audioBlob.arrayBuffer();
  const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
  const wavBlob = audioBufferToWav(audioBuffer);
  await audioContext.close();
  return wavBlob;
}
```

## Architecture Integration

### Service Layer Pattern (Recommended)

```typescript
// src/services/speech.service.ts
import { createClient } from '../lib/tencent-asr';
import * as fs from 'fs';

export class SpeechRecognitionService {
  private asrClient = createClient();
  
  async recognizeLocalFile(filePath: string): Promise<string> {
    const audioBuffer = fs.readFileSync(filePath);
    
    const task = await this.asrClient.createRecognitionTask(audioBuffer, {
      engineType: '16k_zh',
      channelNum: 1,
      resTextFormat: 0
    });
    
    return this.asrClient.waitForRecognitionComplete(task.taskId);
  }
  
  async recognizeShortAudio(audioBuffer: Buffer): Promise<string> {
    const result = await this.asrClient.sentenceRecognition(audioBuffer, {
      engineType: '16k_zh'
    });
    return result.result;
  }
}
```

## Security Best Practices

1. **Never commit credentials**: Add `.env` to `.gitignore`
2. **Use environment variables**: Store all sensitive configuration in `.env`
3. **Key rotation**: Periodically update API credentials
4. **Principle of least privilege**: Only grant ASR service permissions

## Troubleshooting

**Authentication Errors**
- Verify credentials in `.env` file if using custom configuration
- Check SecretId and SecretKey are valid
- Confirm API key is not disabled

**Recognition Failed**
- Confirm audio format is supported (WAV/PCM/MP3)
- Check audio sample rate (8000Hz or 16000Hz)
- Verify audio file size is within limits (file recognition: 512MB, sentence recognition: 5MB)

**Timeout Errors**
- Increase request timeout configuration
- Check network connection stability
- Verify region configuration is correct

## Resources

- **SDK Wrapper Source**: `lib/tencent-asr.ts`
- **Official Documentation**: https://cloud.tencent.com/document/product/1093
- **API Reference**: https://cloud.tencent.com/document/api/1093
- **Console**: https://console.cloud.tencent.com/asr
