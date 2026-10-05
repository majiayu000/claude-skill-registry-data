---
name: tencent-ai3d-integrator
description: Integrate Tencent Cloud AI3D for text-to-3D and image-to-3D model generation. Use this skill when the application needs 3D model generation from text descriptions, converting images to 3D models, or automated 3D asset creation. Triggers on requests for 3D modeling, text-to-3D, image-to-3D, or 3D asset generation.
_meta_type: sdk
---

# Tencent Cloud AI3D SDK Integration

## Scenarios

- **Text-to-3D**: Generate 3D models from text descriptions (e.g., "A little cat")
- **Image-to-3D**: Upload 2D images and automatically convert to high-precision 3D models
- **Game Asset Creation**: Automated 3D asset generation for gaming and virtual environments
- **Product Design**: Quick 3D prototyping from descriptions or reference images
- **Film Production**: Batch 3D content generation for visual effects

**Not recommended for:**
- Direct frontend calls (should use backend proxy)
- Real-time interactive modeling
- Ultra-large scale concurrent tasks (default 1 concurrent job)
- Models requiring precise mechanical specifications

## Setup

### Option A: TypeScript (Node.js)

```bash
npm install tencentcloud-sdk-nodejs
```

Read `lib/tencent-ai3d.ts` from this skill and copy it to the project, then use it directly.

### Option B: Python (Script)

```bash
pip install tencentcloud-sdk-python-ai3d requests
```

Use the `scripts/generate_3d.py` script to directly call the API from the command line.

## Configuration

### Zero Configuration (Default)

Genie provides default zero-configuration support using `ai3d.tencent_cloud.auth-proxy.local` as the endpoint. **No environment variables are required** - Genie has integrated authentication in the proxy gateway by default.

Simply use:

```typescript
import { createClient } from './lib/tencent-ai3d';
const client = createClient();
```

Or with Python script:

```bash
python3 scripts/generate_3d.py text "一只可爱的小猫"
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

### Custom Region

```typescript
import { TencentAI3DClient, createClient } from './lib/tencent-ai3d';

// Custom region via environment variable
const client = createClient();
// Set TENCENTCLOUD_REGION=ap-shanghai in .env

// Explicit configuration
const client = new TencentAI3DClient({
  secretId: process.env.TENCENTCLOUD_SECRET_ID!,
  secretKey: process.env.TENCENTCLOUD_SECRET_KEY!,
  region: 'ap-shanghai'
});
```

## Quick Start

### TypeScript Usage

#### Basic Text-to-3D

```typescript
import { createClient } from './lib/tencent-ai3d';

const client = createClient();

// Text-to-3D
const { jobId } = await client.submitTextTo3D('A little cat');
const result = await client.waitForTaskCompletion(jobId);
console.log('3D model URL:', result.files[0].url);
```

#### Text-to-3D with Options

```typescript
const { jobId } = await client.submitTextTo3D('A cute robot', {
  enablePBR: true,           // Enable PBR material generation
  faceCount: 500000,         // Number of faces (40000-1500000)
  generateType: 'Normal'     // Normal, LowPoly, Geometry, or Sketch
});

const result = await client.waitForTaskCompletion(jobId);
```

#### Image-to-3D

```typescript
// Using image URL
const { jobId } = await client.submitImageTo3D(
  'https://example.com/image.jpg',
  { enablePBR: true }
);

// Using base64 encoded image
import * as fs from 'fs';
const imageBuffer = fs.readFileSync('image.jpg');
const base64 = imageBuffer.toString('base64');

const { jobId: jobId2 } = await client.submitImageBase64To3D(base64);
const result = await client.waitForTaskCompletion(jobId2);
```

### Python Script Usage

The `scripts/generate_3d.py` script provides a CLI tool for direct 3D generation without writing code.

**Install dependencies first:**

```bash
pip install tencentcloud-sdk-python-ai3d requests
```

#### Text-to-3D

```bash
# Basic usage - generates model and downloads to current directory
python3 scripts/generate_3d.py text "一只可爱的小猫"

# With PBR material and custom face count
python3 scripts/generate_3d.py text "一个可爱的机器人" --enable-pbr --face-count 500000

# LowPoly style
python3 scripts/generate_3d.py text "一棵大树" --generate-type LowPoly

# Only submit task, don't wait for completion
python3 scripts/generate_3d.py text "一只猫" --no-wait

# Only print URLs, don't download files
python3 scripts/generate_3d.py text "一只猫" --no-download

# Specify download directory
python3 scripts/generate_3d.py text "一只猫" --download-dir ./output
```

#### Image-to-3D

```bash
# From image URL
python3 scripts/generate_3d.py image --image-url "https://example.com/cat.jpg"

# From local file
python3 scripts/generate_3d.py image --image-file ./cat.jpg

# With PBR material
python3 scripts/generate_3d.py image --image-file ./cat.jpg --enable-pbr
```

#### Query Task Status

```bash
python3 scripts/generate_3d.py query <job_id>
```

#### Common Options

| Option | Description | Default |
|--------|-------------|---------|
| `--enable-pbr` | Enable PBR material generation | off |
| `--face-count N` | Number of faces (40000-1500000) | 500000 |
| `--generate-type` | Normal / LowPoly / Geometry / Sketch | Normal |
| `--polygon-type` | triangle / quadrilateral (LowPoly only) | triangle |
| `--download-dir DIR` | Download output directory | current dir |
| `--poll-interval N` | Poll interval in seconds | 5 |
| `--timeout N` | Max wait time in seconds | 300 |
| `--no-download` | Don't download files, only print URLs | off |
| `--no-wait` | Submit only, return jobId immediately | off |
| `--region` | Tencent Cloud region | ap-guangzhou |

## Response Structure

```typescript
// Query Task Result
{
  status: 'WAIT' | 'RUN' | 'FAIL' | 'DONE';
  errorCode?: string;
  errorMessage?: string;
  files: Array<{
    previewImageUrl: string;  // Preview image URL
    type: string;             // File type
    url: string;              // 3D file download URL (ZIP format)
  }>;
  requestId: string;
}
```

## Architecture Integration

### Service Layer Pattern (Recommended)

```typescript
// src/services/ai3d.service.ts
import { createClient } from '../lib/tencent-ai3d';

export class AI3DService {
  private ai3dClient = createClient();
  
  async generateModelFromText(description: string): Promise<string> {
    const { jobId } = await this.ai3dClient.submitTextTo3D(description, {
      enablePBR: true
    });
    
    const result = await this.ai3dClient.waitForTaskCompletion(jobId);
    return result.files[0].url;
  }
  
  async generateModelFromImage(imageUrl: string): Promise<string> {
    const { jobId } = await this.ai3dClient.submitImageTo3D(imageUrl);
    const result = await this.ai3dClient.waitForTaskCompletion(jobId);
    return result.files[0].url;
  }
}
```

## Security Best Practices

1. **Never commit credentials**: Add `.env` to `.gitignore`
2. **Use environment variables**: Store all sensitive configuration in `.env`
3. **Rotate keys regularly**: Periodically update SecretId and SecretKey
4. **Principle of least privilege**: Grant only necessary API permissions

## Troubleshooting

**Authentication Errors**
- Verify credentials in `.env` file if using custom configuration
- Check if API key is active in the console
- Ensure no extra spaces in credential values

**Task Timeout**
- 3D generation may take longer (30 seconds - 2 minutes)
- Adjust timeout using the `timeout` parameter in `waitForTaskCompletion`
- Check if task status is FAIL and review error message

**Concurrency Limits**
- Default supports only 1 concurrent task
- Ensure previous task completes before submitting new one
- Consider implementing task queue management

**Image Format Errors**
- Supported formats: jpg, png, jpeg, webp
- Image size: ≤8MB
- Resolution: 128-5000 pixels

## Resources

- **TypeScript SDK Wrapper**: `lib/tencent-ai3d.ts`
- **Python CLI Script**: `scripts/generate_3d.py`
- **Official Documentation**: https://cloud.tencent.com/document/product/1804
- **API Reference**: https://cloud.tencent.com/document/product/1804/123463
- **Console**: https://console.cloud.tencent.com/ai3d
