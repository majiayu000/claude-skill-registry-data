---
name: tencent-hunyuan-video-integrator
description: Integrate Tencent Cloud Hunyuan for text-to-video and image-to-video generation. Use this skill when the application needs AI video generation from text descriptions or static images. Triggers on requests for video generation, text-to-video, image-to-video, image animation, or AI video creation.
_meta_type: sdk
---

# Tencent Cloud Hunyuan Video Generation SDK Integration

## Scenarios

- **文生视频（Text-to-Video）**：根据文字描述生成视频内容，适用于营销素材、社交媒体短视频、内容创作
- **图生视频（Image-to-Video）**：将静态图片动画化，适用于产品展示、创意内容、图片动效
- **AI 视频内容生产**：自动化批量生成视频内容

**Not recommended for:**
- 直接在前端调用（需要暴露密钥）
- 需要实时结果的场景（视频生成为异步任务，通常需要 1-5 分钟）
- 高并发场景（默认并发数为 1）

## Setup

### 1. Install Dependencies

```bash
npm install tencentcloud-sdk-nodejs@^4.0.0
```

### 2. Copy SDK Wrapper

Read `lib/tencent-hunyuan-video.ts` from this skill and copy it to the project, then use it directly.

```
your-project/
├── src/
│   ├── lib/
│   │   └── tencent-hunyuan-video.ts  ← Copy here
│   └── ...
└── package.json
```

## Configuration

### Zero Configuration (Default)

Genie provides default zero-configuration support using `vclm.tencent_cloud.auth-proxy.local` as the endpoint. **No environment variables are required** - Genie has integrated authentication in the proxy gateway by default.

Simply use:

```typescript
import { createClient } from './lib/tencent-hunyuan-video';
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

### Text-to-Video（文生视频）

```typescript
import { createClient } from './lib/tencent-hunyuan-video';

const client = createClient();

// 提交任务
const job = await client.submitTextToVideoJob('一只猫在草地上奔跑，写实风格');
console.log('任务 ID:', job.jobId);

// 等待完成
const result = await client.waitForJobCompletion(job.jobId, 'text', {
  pollInterval: 5000,   // 每 5 秒查询一次
  timeout: 600000,      // 最多等待 10 分钟
  onProgress: (status) => console.log('当前状态:', status)
});
console.log('视频 URL:', result.resultVideoUrl);

// 下载视频（URL 24 小时内有效）
await client.downloadVideo(result.resultVideoUrl!, './output/video.mp4');
```

### Image-to-Video（图生视频）

```typescript
// 使用图片 URL
const job = await client.submitImageToVideoJob(
  { url: 'https://example.com/cat.jpg' },
  {
    prompt: '让这只猫动起来',  // 可选描述
    resolution: '720p',
    fps: 24
  }
);

// 使用 base64 图片
const job2 = await client.submitImageToVideoJob(
  { base64: base64ImageData },
  { resolution: '1080p', fps: 30 }
);

const result = await client.waitForJobCompletion(job.jobId, 'image');
console.log('视频 URL:', result.resultVideoUrl);
```

### Convenience Methods（一体化方法）

```typescript
// 文生视频：提交 + 等待一步完成
const result = await client.generateTextToVideo(
  '一只猫在草地上奔跑',
  { logoAdd: 0 },  // 不添加水印（需平台已申请关闭）
  { onProgress: (status) => console.log('状态:', status) }
);
console.log('视频 URL:', result.resultVideoUrl);

// 图生视频：提交 + 等待一步完成
const result2 = await client.generateImageToVideo(
  { url: 'https://example.com/cat.jpg' },
  { resolution: '720p', fps: 24 }
);
console.log('视频 URL:', result2.resultVideoUrl);
```

## Response Structure

```typescript
// 提交任务结果
{
  jobId: string;      // 任务 ID，用于后续查询
  requestId: string;  // 请求 ID
}

// 任务状态（文生视频 / 图生视频通用）
{
  status: 'WAIT' | 'RUN' | 'FAIL' | 'DONE';
  errorCode?: string;        // 错误码（FAIL 时有值）
  errorMessage?: string;     // 错误信息（FAIL 时有值）
  resultVideoUrl?: string;   // 视频 URL（DONE 时有值，24 小时内有效）
  requestId: string;
}
```

## API Capabilities

| 能力 | 提交接口 | 查询接口 | 说明 |
|------|----------|----------|------|
| 文生视频 | `SubmitHunyuanToVideoJob` | `DescribeHunyuanToVideoJob` | Prompt 必填，仅支持 720p |
| 图生视频 | `SubmitImageToVideoGeneralJob` | `DescribeImageToVideoGeneralJob` | 图片必填，支持 480p/720p/1080p，Fps 可选（16/24/30） |

## Architecture Integration

### Service Layer Pattern (Recommended)

```typescript
// src/services/video.service.ts
import { createClient } from '../lib/tencent-hunyuan-video';

export class VideoService {
  private client = createClient();

  /**
   * 文生视频：根据文字描述生成视频
   */
  async generateFromText(prompt: string): Promise<string> {
    const result = await this.client.generateTextToVideo(prompt, {
      logoAdd: 1,
    });

    if (!result.resultVideoUrl) {
      throw new Error('视频生成成功但未返回 URL');
    }

    return result.resultVideoUrl;
  }

  /**
   * 图生视频：将图片动画化
   */
  async generateFromImage(
    imageUrl: string,
    options?: { prompt?: string; resolution?: '480p' | '720p' | '1080p' }
  ): Promise<string> {
    const result = await this.client.generateImageToVideo(
      { url: imageUrl },
      {
        prompt: options?.prompt,
        resolution: options?.resolution || '720p',
        fps: 30,
      }
    );

    if (!result.resultVideoUrl) {
      throw new Error('视频生成成功但未返回 URL');
    }

    return result.resultVideoUrl;
  }

  /**
   * 提交任务并异步轮询（适合需要展示进度的场景）
   */
  async submitAndPoll(
    type: 'text' | 'image',
    input: string,
    onProgress: (status: string) => void
  ): Promise<string> {
    let jobId: string;

    if (type === 'text') {
      const job = await this.client.submitTextToVideoJob(input);
      jobId = job.jobId;
    } else {
      const job = await this.client.submitImageToVideoJob({ url: input });
      jobId = job.jobId;
    }

    const result = await this.client.waitForJobCompletion(jobId, type, {
      pollInterval: 5000,
      timeout: 600000,
      onProgress,
    });

    return result.resultVideoUrl!;
  }
}
```

## Limitations

| 限制项 | 文生视频 | 图生视频 |
|--------|----------|----------|
| Prompt 最大长度 | 200 字符 | 可选，无强制限制 |
| 分辨率 | 仅 720p | 480p / 720p / 1080p |
| 帧率 | 不支持配置 | 16 / 24 / 30（默认 30） |
| 并发任务数 | 1（默认） | 1（默认） |
| 视频 URL 有效期 | 24 小时 | 24 小时 |
| 最大等待时间 | 10 分钟（默认） | 10 分钟（默认） |

## Security Best Practices

1. **Never commit credentials**: Add `.env` to `.gitignore`
2. **Use environment variables**: Store all sensitive configuration in `.env`
3. **Video URL expiration**: Download videos promptly (URLs valid 24 hours only)
4. **Backend calls only**: Never expose credentials to frontend
5. **LogoAdd parameter**: Default is `1` (add watermark). Set to `0` only if the platform account has applied to disable the watermark in the Tencent Cloud console.

## Troubleshooting

**Authentication Errors**
- Verify credentials in `.env` file if using custom configuration
- Check if API key is active in the console
- Ensure no extra spaces in credential values

**Job Failures**
- Check if prompt meets requirements (max 200 characters for text-to-video)
- Verify input image format and size meet requirements
- Review `errorCode` and `errorMessage` for specific failure reason

**Network Errors**
- Check firewall/proxy settings
- Verify service endpoint is accessible

**Video Download Failures**
- Confirm video URL has not expired (24-hour validity)
- Check if local storage path has write permissions

**Timeout Issues**
- Increase `timeout` in `waitForJobCompletion` options
- Video generation typically takes 1-5 minutes

## Resources

- **SDK Wrapper Source**: `lib/tencent-hunyuan-video.ts`
- **Official Documentation**: https://cloud.tencent.com/document/product/1616
- **API Reference - 文生视频提交**: https://cloud.tencent.com/document/product/1616/126160
- **API Reference - 文生视频查询**: https://cloud.tencent.com/document/product/1616/126162
- **API Reference - 图生视频提交**: https://cloud.tencent.com/document/product/1616/126163
- **API Reference - 图生视频查询**: https://cloud.tencent.com/document/product/1616/126164
- **Console**: https://console.cloud.tencent.com/vclm
