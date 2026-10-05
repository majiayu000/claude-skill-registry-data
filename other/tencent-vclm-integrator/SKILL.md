---
name: tencent-vclm-integrator
description: Integrate Tencent Cloud VCLM for text-to-video and image-to-video generation. Use this skill when the application needs AI video generation from text, animated video from images, or automated video content creation. Triggers on requests for video generation, text-to-video, image animation, or AI video creation.
_meta_type: sdk
---

# Tencent Cloud VCLM SDK Integration

## Scenarios

- **Text-to-Video**: Generate video content from text descriptions
- **Image-to-Video**: Animate static images into dynamic videos
- **AI Video Creation**: Automated video content generation
- **Marketing Content**: Quick video creation for promotional materials
- **Social Media**: Generate short video clips from descriptions

**Not recommended for:**
- Direct frontend usage (should be called through backend API)
- Real-time streaming operations
- Scenarios requiring immediate results (video generation takes time)
- High-frequency generation (default 1 concurrent job)

## Setup

### 1. Install Dependencies

```bash
npm install tencentcloud-sdk-nodejs@^4.0.0
```

### 2. Copy SDK Wrapper

Read `lib/tencent-vclm.ts` from this skill and copy it to the project, then use it directly.

## Configuration

### Zero Configuration (Default)

Genie provides default zero-configuration support using `vclm.tencent_cloud.auth-proxy.local` as the endpoint. **No environment variables are required** - Genie has integrated authentication in the proxy gateway by default.

Simply use:

```typescript
import { createClient } from './lib/tencent-vclm';
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
import { createClient } from './lib/tencent-vclm';

const client = createClient();

// Submit video generation job
const job = await client.submitVideoJob('A cat running on grassland, realistic style');
console.log('Job submitted:', job.jobId);

// Wait for completion
const result = await client.waitForJobCompletion(job.jobId);
console.log('Video generated:', result.resultVideoUrl);

// Download video
await client.downloadVideo(result.resultVideoUrl!, './output.mp4');
```

### Text-to-Video with Options

```typescript
const job = await client.submitVideoJob('A dog dancing', {
  resolution: '720p',
  logoAdd: 0  // 0 = no watermark, 1 = add watermark
});

const result = await client.waitForJobCompletion(job.jobId, {
  pollInterval: 5000,   // Check every 5 seconds
  timeout: 600000,      // 10 minutes max
  onProgress: (status) => console.log('Status:', status)
});
```

### Image-to-Video

```typescript
// Generate video from input image
const job = await client.submitVideoJob('Make this cat run', {
  image: { url: 'https://example.com/cat.jpg' },
  logoAdd: 0
});

// Or use base64 encoded image
const job2 = await client.submitVideoJob('Animate this scene', {
  image: { base64: base64ImageData }
});
```

### Convenience Method

```typescript
// Submit and wait in one call
const result = await client.generateVideo('A dog dancing', {
  logoAdd: 0
}, {
  onProgress: (status) => console.log('Status:', status)
});

console.log('Video URL:', result.resultVideoUrl);
```

## Response Structure

```typescript
// Submit Job Result
{
  jobId: string;      // Job ID for status queries
  requestId: string;  // Request ID
}

// Job Detail
{
  status: 'WAIT' | 'RUN' | 'FAIL' | 'DONE';
  errorCode?: string;        // Error code (when FAIL)
  errorMessage?: string;     // Error message (when FAIL)
  resultVideoUrl?: string;   // Video URL (when DONE, valid 24 hours)
  requestId: string;
}
```

## Architecture Integration

### Service Layer Pattern (Recommended)

```typescript
// src/services/video.service.ts
import { createClient } from '../lib/tencent-vclm';

export class VideoService {
  private vclmClient = createClient();
  
  async generateVideoFromText(prompt: string, userId: string): Promise<string> {
    const job = await this.vclmClient.submitVideoJob(prompt);
    const result = await this.vclmClient.waitForJobCompletion(job.jobId);
    
    // Download video
    const videoPath = `videos/${userId}/${Date.now()}.mp4`;
    await this.vclmClient.downloadVideo(result.resultVideoUrl!, videoPath);
    
    return videoPath;
  }
  
  async generateVideoFromImage(
    prompt: string, 
    imageUrl: string
  ): Promise<string> {
    const result = await this.vclmClient.generateVideo(prompt, {
      image: { url: imageUrl }
    });
    
    return result.resultVideoUrl!;
  }
}
```

## Limitations

| Constraint | Value |
|------------|-------|
| Max prompt length | 200 characters |
| Video resolution | 720p only |
| Concurrent jobs | 1 (default) |
| Video URL validity | 24 hours |
| Max wait time | 10 minutes (default) |

## Security Best Practices

1. **Never commit credentials**: Add `.env` to `.gitignore`
2. **Use environment variables**: Store all sensitive configuration in `.env`
3. **Video URL expiration**: Download videos promptly (URLs valid 24 hours only)
4. **Backend calls only**: Never expose credentials to frontend

## Troubleshooting

**Authentication Errors**
- Verify credentials in `.env` file if using custom configuration
- Check if API key is active in the console
- Ensure no extra spaces in credential values

**Job Failures**
- Check if prompt meets requirements (max 200 characters)
- Verify input image format and size meet requirements
- Review error message for specific failure reason

**Network Errors**
- Check firewall/proxy settings
- Verify service endpoint is accessible

**Video Download Failures**
- Confirm video URL has not expired (24-hour validity)
- Check if local storage path has write permissions

**Timeout Issues**
- Increase timeout in `waitForJobCompletion` options
- Video generation typically takes 1-5 minutes

## Resources

- **SDK Wrapper Source**: `lib/tencent-vclm.ts`
- **Official Documentation**: https://cloud.tencent.com/document/product/1616
- **API Reference - Submit Job**: https://cloud.tencent.com/document/product/1616/126160
- **API Reference - Query Job**: https://cloud.tencent.com/document/product/1616/126162
- **Console**: https://console.cloud.tencent.com/vclm
