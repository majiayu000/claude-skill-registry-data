---
name: hunyuan-chat-integrator
description: Integrate Tencent Cloud Hunyuan LLM for text generation and conversations. Use this skill when the application needs AI chatbots, content generation, code assistance, image analysis, or streaming text output. Triggers on requests for chat completion, AI conversation, content creation, or vision analysis.
_meta_type: sdk
---

# Tencent Cloud Hunyuan LLM SDK Integration

## Scenarios

- **Text Generation**: Generate high-quality text content based on prompts
- **Conversation Systems**: Build intelligent chatbots and customer service systems
- **Content Creation**: Automatically generate articles, summaries, translations
- **Code Assistance**: Code generation, explanation, and optimization
- **Streaming Output**: Real-time content generation for improved UX

**Not recommended for:**
- Direct frontend browser use (credential security issues)
- Real-time voice conversations
- Scenarios requiring extremely low latency (< 100ms)

## Setup

### 1. Install Dependencies

```bash
npm install tencentcloud-sdk-nodejs-hunyuan
```

### 2. Copy SDK Wrapper

Read `lib/hunyuan-chat.ts` from this skill and copy it to the project, then use it directly.

## Configuration

### Zero Configuration (Default)

Genie provides default zero-configuration support using `hunyuan.tencent_cloud.auth-proxy.local` as the endpoint. **No environment variables are required** - Genie has integrated authentication in the proxy gateway by default.

Simply use:

```typescript
import { createClient } from './lib/hunyuan-chat';
const client = createClient();
```

### Custom Configuration (Optional)

Users can optionally configure environment variables. When configured, Genie will use user-provided credentials instead of the default proxy:

```env
# Optional - Only configure if you want to use your own credentials
TENCENTCLOUD_SECRET_ID=your-secret-id-here
TENCENTCLOUD_SECRET_KEY=your-secret-key-here
TENCENTCLOUD_REGION=ap-guangzhou
```

**Obtaining Credentials** (if needed):
1. Visit [Tencent Cloud Console - Access Keys](https://console.cloud.tencent.com/cam/capi)
2. Click "Create Key" to create API credentials
3. Copy **SecretId** and **SecretKey**

### Custom Region and Endpoint

Users can customize region and endpoint:

```typescript
import { HunyuanClient, createClient } from './lib/hunyuan-chat';

// Custom region only
const client = createClient();
// Set TENCENTCLOUD_REGION=ap-beijing in .env

// Custom endpoint
const client = new HunyuanClient({
  secretId: process.env.TENCENTCLOUD_SECRET_ID!,
  secretKey: process.env.TENCENTCLOUD_SECRET_KEY!,
  region: 'ap-beijing',
  endpoint: 'custom-endpoint.example.com'
});
```

## Quick Start

### Basic Usage

```typescript
import { createClient } from './lib/hunyuan-chat';

const client = createClient();

// Single-turn conversation
const result = await client.chatCompletions([
  { Role: 'user', Content: 'Hello, please introduce yourself' }
]);
console.log(result.Choices[0].Message.Content);

// With parameters
const result = await client.chatCompletions(
  [{ Role: 'user', Content: 'Write a poem' }],
  { Temperature: 0.8, TopP: 0.9 }
);
```

### Multi-turn Conversation

```typescript
const result = await client.chatCompletions([
  { Role: 'user', Content: 'Hello' },
  { Role: 'assistant', Content: 'Hello! I am Hunyuan Assistant' },
  { Role: 'user', Content: 'What can you do?' }
]);
```

### Streaming Output

```typescript
const result = await client.chatCompletionsStream(
  [{ Role: 'user', Content: 'Tell a story' }],
  {},
  (chunk) => process.stdout.write(chunk.Delta.Content)
);
```

### Image Analysis

**Note:** Set request timeout to at least 60 seconds (recommended: 120 seconds).

```typescript
import * as fs from 'fs';

const imageBuffer = fs.readFileSync('sample-image.jpg');
const imageBase64 = imageBuffer.toString('base64');

const result = await client.chatWithImage(
  imageBase64,
  'Please describe what you see in this image.',
  'You are a helpful assistant that analyzes images.'
);
```

## Architecture Integration

### Service Layer Pattern (Recommended)

```typescript
// src/services/ai.service.ts
import { createClient } from '../lib/hunyuan-chat';

export class AIService {
  private hunyuanClient = createClient();
  
  async generateText(prompt: string): Promise<string> {
    const result = await this.hunyuanClient.chatCompletions([
      { Role: 'user', Content: prompt }
    ]);
    return result.Choices[0].Message.Content;
  }
  
  async chatWithHistory(
    userMessage: string,
    history: Array<{ role: string; content: string }>
  ): Promise<string> {
    const messages = [
      ...history.map(h => ({ Role: h.role, Content: h.content })),
      { Role: 'user', Content: userMessage }
    ];
    const result = await this.hunyuanClient.chatCompletions(messages);
    return result.Choices[0].Message.Content;
  }
}
```

## Security Best Practices

1. **Never commit credentials**: Add `.env` to `.gitignore`
2. **Use environment variables**: Store sensitive configuration via environment variables
3. **Principle of least privilege**: Use sub-accounts with only necessary API permissions
4. **Rotate credentials regularly**: Recommend changing API credentials every 90 days

## Troubleshooting

**Authentication Errors**
- Verify credentials in `.env` file if using custom configuration
- Confirm API credentials are enabled in Tencent Cloud Console

**Network Errors**
- Check firewall and proxy settings
- Confirm access to `hunyuan.tencentcloudapi.com` or proxy endpoint
- Try setting longer timeout

**Parameter Errors**
- Ensure Messages array format is correct
- Check Temperature [0.0, 2.0] and TopP [0.0, 1.0] ranges

## Resources

- **SDK Wrapper Source**: `lib/hunyuan-chat.ts`
- **Official Documentation**: https://cloud.tencent.com/document/product/1729/105701
- **API Reference**: https://cloud.tencent.com/document/api/1729/105701
- **Console**: https://console.cloud.tencent.com/hunyuan
