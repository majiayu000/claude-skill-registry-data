---
name: tencent-aiart-integrator
description: Integrate Tencent Cloud AI Art for text-to-image and image-to-image generation. Use this skill when the application needs AI artwork generation, image style transfer, or batch visual content creation. Triggers on requests for AI image generation, text-to-image, image styling, or automated artwork creation.
_meta_type: sdk
---

# Tencent Cloud AI Art SDK Integration

## Scenarios

- **Text-to-Image**: Generate artistic images based on text descriptions
- **Image-to-Image**: Generate new images based on reference images and text descriptions
- **AI Creation Tools**: Integrate into content creation platforms
- **Batch Image Generation**: Automate generation of large amounts of image content
- **Style Transfer**: Apply artistic styles to existing images

**Not recommended for:**
- Direct frontend calls (requires exposing credentials)
- Real-time interactive applications (has concurrency limits)
- Ultra-high concurrency scenarios (default concurrency is 1)
- Generating content that violates content policies

## Setup

### 1. Install Dependencies

```bash
npm install tencentcloud-sdk-nodejs
```

### 2. Copy SDK Wrapper

Read `lib/tencent-aiart.ts` from this skill and copy it to the project, then use it directly.

## Configuration

### Zero Configuration (Default)

Genie provides default zero-configuration support using `aiart.tencent_cloud.auth-proxy.local` as the endpoint. **No environment variables are required** - Genie has integrated authentication in the proxy gateway by default.

Simply use:

```typescript
import { createClient } from './lib/tencent-aiart';
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

## Quick Start

### Basic Usage

```typescript
import { createClient } from './lib/tencent-aiart';

const client = createClient();

// Text-to-image (async)
const job = await client.textToImage('A cute little cat', {
  resolution: '1024:1024',
  style: '1' // Miyazaki style
});

console.log('Job ID:', job.jobId);

// Query result
const result = await client.queryJob(job.jobId);
console.log('Image URL:', result.imageUrl);
```

### Text-to-Image with Waiting

```typescript
// Synchronous version - waits for completion
const imageUrl = await client.textToImageSync('A beautiful sunset over mountains', {
  resolution: '1024:1024',
  seed: 12345
});

console.log('Image URL:', imageUrl);
```

### Image-to-Image

```typescript
// Generate new image based on reference
const result = await client.imageToImage(
  'Turn this cat into cartoon style',
  'https://example.com/cat.jpg',
  {
    resolution: '1024:1024',
    rspImgType: 'url'
  }
);

console.log('Generated image:', result.resultImage);
```

## Response Structure

```typescript
// Text-to-Image Result
{
  jobId: string;      // Job ID for querying status
  requestId: string;  // Request ID
}

// Query Job Result
{
  status: 'PENDING' | 'RUNNING' | 'SUCCESS' | 'FAILED';
  imageUrl?: string;       // Image URL (when job succeeds)
  errorMessage?: string;   // Error message (when job fails)
  requestId: string;
}

// Image-to-Image Result
{
  resultImage: string;  // Generated image URL or Base64
  requestId: string;
}
```

## Architecture Integration

### Service Layer Pattern (Recommended)

```typescript
// src/services/ai-art.service.ts
import { createClient } from '../lib/tencent-aiart';

export class AIArtService {
  private aiArtClient = createClient();
  
  async generateImage(prompt: string, userId: string): Promise<string> {
    const result = await this.aiArtClient.textToImage(prompt, {
      resolution: '1024:1024',
      seed: Date.now()
    });
    
    // Save job ID to database
    await this.saveJobToDatabase(userId, result.jobId);
    return result.jobId;
  }
  
  async checkImageStatus(jobId: string): Promise<string | null> {
    const result = await this.aiArtClient.queryJob(jobId);
    
    if (result.status === 'SUCCESS') {
      return result.imageUrl;
    }
    return null;
  }
  
  async generateImageSync(prompt: string): Promise<string> {
    return this.aiArtClient.textToImageSync(prompt, {
      resolution: '1024:1024'
    });
  }
}
```

## Security Best Practices

1. **Never commit credentials**: Add `.env` to `.gitignore`
2. **Use environment variables**: Store all sensitive configuration in `.env`
3. **Rotate keys regularly**: Periodically update SecretId and SecretKey
4. **Principle of least privilege**: Assign minimum necessary permissions to API keys
5. **Content moderation**: Validate prompts before sending to API

## Troubleshooting

**Authentication Errors**
- Verify credentials in `.env` file if using custom configuration
- Check if API key is active in the console
- Ensure no extra spaces in credential values

**Network Errors**
- Check firewall/proxy settings
- Verify service endpoint is accessible
- Confirm region configuration is correct

**Content Moderation Failures**
- Check if prompt content is compliant
- Avoid using sensitive words
- Reference images must comply with content standards

**Concurrency Limits**
- Default concurrency is 1, requires queuing
- Implement task queue mechanism
- Consider upgrading concurrency quota

## Resources

- **SDK Wrapper Source**: `lib/tencent-aiart.ts`
- **Official Documentation**: https://cloud.tencent.com/document/product/1668
- **API Reference**: https://cloud.tencent.com/document/product/1668/124632
- **Console**: https://console.cloud.tencent.com/aiart
