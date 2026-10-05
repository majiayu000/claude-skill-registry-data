---
name: tencent-tts-integrator
description: Integrate Tencent Cloud TTS for text-to-speech synthesis. Use this skill when the application needs article narration, word pronunciation, voice output, or audio content generation. Triggers on requests for text-to-speech, voice synthesis, audio generation, or pronunciation features.
_meta_type: sdk
---

# Tencent Cloud TTS SDK Integration

## Scenarios

- **Article Narration**: Convert long articles to audio for listening
- **Word Pronunciation**: Click-to-play pronunciation for language learning apps
- **News Broadcasting**: Convert news content to voice broadcasts
- **Audiobooks**: Batch generation of audio content
- **Notification Voice**: Convert notifications to voice alerts

**Not recommended for:**
- Real-time conversation (latency may be high)
- Super long text over 100,000 characters (requires segmentation)
- Direct frontend calls (API credentials must be protected)

## Setup

### 1. Install Dependencies

```bash
npm install tencentcloud-sdk-nodejs-tts@latest
```

### 2. Copy SDK Wrapper

Read `lib/tencent-tts.ts` from this skill and copy it to the project, then use it directly.

## Configuration

### Zero Configuration (Default)

Genie provides default zero-configuration support using `tts.tencent_cloud.auth-proxy.local` as the endpoint. **No environment variables are required** - Genie has integrated authentication in the proxy gateway by default.

Simply use:

```typescript
import { createClient } from './lib/tencent-tts';
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
3. Enable [TTS Service](https://console.cloud.tencent.com/tts)

## Quick Start

### Smart Synthesis (Auto Short/Long Text)

```typescript
import { createClient, LARGE_MODEL_VOICES } from './lib/tencent-tts';
import * as fs from 'fs';

const client = createClient();

const result = await client.synthesize(text, {
  voiceType: LARGE_MODEL_VOICES.ZHI_LAN,
  codec: 'mp3'
});

if (result.type === 'audio') {
  // Short text: returns audio Buffer directly
  fs.writeFileSync('output.mp3', result.audio);
} else {
  // Long text: returns download URL
  console.log('Download URL:', result.url);
}
```

### Short Text Synthesis

```typescript
// Direct synthesis for short text (max 150 Chinese chars)
const result = await client.textToVoice('Hello world', {
  voiceType: LARGE_MODEL_VOICES.ZHI_LAN,
  speed: 0,
  volume: 0,
  codec: 'mp3'
});

// Save audio file
const audioBuffer = Buffer.from(result.audio, 'base64');
fs.writeFileSync('output.mp3', audioBuffer);
```

### Long Text Synthesis

```typescript
// Async synthesis for long text (max 100,000 chars)
const task = await client.createLongTextTask(longArticle, {
  voiceType: LARGE_MODEL_VOICES.AI_XIAO_HE,
  codec: 'mp3'
});

// Wait for completion
const result = await client.waitForLongTextComplete(task.taskId);
console.log('Download URL:', result.resultUrl);
```

### Emotional Synthesis

```typescript
import { EMOTION_CATEGORIES } from './lib/tencent-tts';

// Synthesis with emotion (only for supported voices)
await client.textToVoice('Great weather today!', {
  voiceType: LARGE_MODEL_VOICES.AI_XIAO_XI,
  emotionCategory: EMOTION_CATEGORIES.HAPPY,
  emotionIntensity: 150
});
```

## Voice Selection

### Recommended Voices

| Use Case | Voice | Voice ID |
|----------|-------|----------|
| Chinese article narration | Ai Xiaohe (reading female) | 601003 |
| English article narration | WeJames (English male) | 501008 |
| News broadcasting | Zhilan (news female) | 501001 |
| Children's content | Zhi Xiaohu (child voice) | 502007 |
| Chinese word pronunciation | Zhilan | 501001 |
| English word pronunciation | WeJames | 501008 |

### Voice Constants

```typescript
import { 
  SUPER_NATURAL_VOICES,  // Super natural model voices
  LARGE_MODEL_VOICES,    // Large model voices
  PREMIUM_VOICES,        // Premium voices
  EMOTION_CATEGORIES     // Emotion types
} from './lib/tencent-tts';
```

## Text Length Limits

| Type | Chinese | English |
|------|---------|---------|
| Standard (sync) | 150 chars | 500 letters |
| Long text (async) | 100,000 chars | 100,000 chars |

## Architecture Integration

### Service Layer Pattern (Recommended)

```typescript
// src/services/tts.service.ts
import { createClient, LARGE_MODEL_VOICES } from '../lib/tencent-tts';

export class TTSService {
  private ttsClient = createClient();
  
  async pronounceWord(word: string, isEnglish = false): Promise<Buffer> {
    const result = await this.ttsClient.textToVoice(word, {
      voiceType: isEnglish ? LARGE_MODEL_VOICES.WE_JAMES : LARGE_MODEL_VOICES.ZHI_LAN,
      primaryLanguage: isEnglish ? 2 : 1,
      codec: 'mp3',
      speed: -1  // Slightly slower for learning
    });
    return Buffer.from(result.audio, 'base64');
  }
  
  async readArticle(content: string): Promise<string | Buffer> {
    const result = await this.ttsClient.synthesize(content, {
      voiceType: LARGE_MODEL_VOICES.AI_XIAO_HE,
      codec: 'mp3'
    });
    
    if (result.type === 'audio') {
      return result.audio;
    }
    return result.url;  // Long text returns download URL
  }
}
```

### API Route Example

```typescript
// src/routes/tts.routes.ts
import { Router } from 'express';
import { TTSService } from '../services/tts.service';

const router = Router();
const ttsService = new TTSService();

// Word pronunciation endpoint
router.get('/pronounce/:word', async (req, res) => {
  const { word } = req.params;
  const isEnglish = /^[a-zA-Z\s]+$/.test(word);
  
  const audio = await ttsService.pronounceWord(word, isEnglish);
  res.set('Content-Type', 'audio/mpeg');
  res.send(audio);
});

// Article reading endpoint
router.post('/read', async (req, res) => {
  const { content } = req.body;
  const result = await ttsService.readArticle(content);
  
  if (Buffer.isBuffer(result)) {
    res.set('Content-Type', 'audio/mpeg');
    res.send(result);
  } else {
    res.json({ downloadUrl: result });
  }
});
```

## Security Best Practices

1. **Never commit credentials**: Add `.env` to `.gitignore`
2. **Use environment variables**: Store all sensitive configuration in `.env`
3. **Key rotation**: Periodically update API credentials
4. **Backend calls only**: TTS API must be called from backend, never expose credentials to frontend

## Troubleshooting

**Authentication Errors**
- Verify credentials in `.env` file if using custom configuration
- Check SecretId and SecretKey are valid
- Confirm TTS service is enabled

**Audio Format Issues**
- Supported formats: mp3, wav, pcm
- Sample rates: 8000, 16000, 24000 Hz
- Recommend mp3 format for best compatibility

**Long Text Timeout**
- Long text synthesis is async, requires polling for result
- Max synthesis time is 3 hours
- Audio files retained for 24 hours
- **Important**: Set frontend request timeout > 1 minute (recommend 2-3 minutes)

## Resources

- **SDK Wrapper Source**: `lib/tencent-tts.ts`
- **Official Documentation**: https://cloud.tencent.com/document/product/1073
- **API Reference**: https://cloud.tencent.com/document/api/1073
- **Console**: https://console.cloud.tencent.com/tts
- **Voice List**: https://cloud.tencent.com/document/product/1073/92668
