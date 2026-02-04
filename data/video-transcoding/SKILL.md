---
name: Video Transcoding
description: Converting videos to different formats, resolutions, and bitrates using FFmpeg, cloud services, and optimization techniques for efficient video delivery across devices and networks.
---

# Video Transcoding

> **Current Level:** Advanced  
> **Domain:** Video Streaming / Media Processing

---

## Overview

Video transcoding converts videos to different formats, resolutions, and bitrates. This guide covers FFmpeg, cloud services, and optimization for building video processing pipelines that create multiple quality levels for adaptive streaming.

## Transcoding Concepts

```
Source Video → Decode → Process → Encode → Output Video
```

**Key Parameters:**
- **Resolution**: 1080p, 720p, 480p, 360p
- **Codec**: H.264, H.265 (HEVC), VP9, AV1
- **Bitrate**: Quality vs file size
- **Container**: MP4, WebM, MKV

## FFmpeg Transcoding

### Basic Transcoding

```bash
# H.264 transcoding
ffmpeg -i input.mp4 \
  -c:v libx264 \
  -preset medium \
  -crf 23 \
  -c:a aac \
  -b:a 128k \
  output.mp4

# H.265 (HEVC) for better compression
ffmpeg -i input.mp4 \
  -c:v libx265 \
  -preset medium \
  -crf 28 \
  -c:a aac \
  -b:a 128k \
  output_hevc.mp4

# VP9 (WebM)
ffmpeg -i input.mp4 \
  -c:v libvpx-vp9 \
  -b:v 2M \
  -c:a libopus \
  -b:a 128k \
  output.webm

# AV1 (next-gen codec)
ffmpeg -i input.mp4 \
  -c:v libaom-av1 \
  -crf 30 \
  -b:v 0 \
  -strict experimental \
  output_av1.mp4
```

### Multiple Resolutions

```typescript
// services/transcoding.service.ts
import ffmpeg from 'fluent-ffmpeg';
import { Queue, Worker } from 'bullmq';

export class TranscodingService {
  private queue: Queue;

  constructor() {
    this.queue = new Queue('transcoding', {
      connection: {
        host: process.env.REDIS_HOST,
        port: parseInt(process.env.REDIS_PORT || '6379')
      }
    });
  }

  async transcodeVideo(videoId: string, inputPath: string): Promise<void> {
    const resolutions = [
      { name: '1080p', width: 1920, height: 1080, bitrate: '5000k' },
      { name: '720p', width: 1280, height: 720, bitrate: '3000k' },
      { name: '480p', width: 854, height: 480, bitrate: '1500k' },
      { name: '360p', width: 640, height: 360, bitrate: '800k' }
    ];

    for (const resolution of resolutions) {
      await this.queue.add('transcode', {
        videoId,
        inputPath,
        resolution
      });
    }
  }
}

// Worker
const worker = new Worker('transcoding', async (job) => {
  const { videoId, inputPath, resolution } = job.data;

  const outputPath = `/tmp/${videoId}-${resolution.name}.mp4`;

  await transcodeToResolution(inputPath, outputPath, resolution);

  // Upload to S3
  const s3Key = `videos/${videoId}/${resolution.name}.mp4`;
  await uploadToS3(outputPath, s3Key, 'video/mp4');

  // Update database
  await db.videoVariant.create({
    data: {
      videoId,
      resolution: resolution.name,
      width: resolution.width,
      height: resolution.height,
      bitrate: resolution.bitrate,
      s3Key,
      url: `${process.env.CDN_URL}/${s3Key}`
    }
  });

  return { success: true, resolution: resolution.name };
});

async function transcodeToResolution(
  inputPath: string,
  outputPath: string,
  resolution: any
): Promise<void> {
  return new Promise((resolve, reject) => {
    ffmpeg(inputPath)
      .size(`${resolution.width}x${resolution.height}`)
      .videoBitrate(resolution.bitrate)
      .videoCodec('libx264')
      .audioCodec('aac')
      .audioBitrate('128k')
      .outputOptions([
        '-preset medium',
        '-profile:v main',
        '-movflags +faststart'
      ])
      .output(outputPath)
      .on('progress', (progress) => {
        console.log(`Processing: ${progress.percent}% done`);
      })
      .on('end', () => resolve())
      .on('error', reject)
      .run();
  });
}
```

## Audio Transcoding

```bash
# Extract audio
ffmpeg -i input.mp4 -vn -c:a copy audio.aac

# Transcode audio to different formats
ffmpeg -i input.mp4 -vn -c:a libmp3lame -b:a 192k audio.mp3
ffmpeg -i input.mp4 -vn -c:a libopus -b:a 128k audio.opus
ffmpeg -i input.mp4 -vn -c:a libvorbis -b:a 128k audio.ogg

# Normalize audio
ffmpeg -i input.mp4 -af loudnorm output.mp4
```

## Codec Selection

```typescript
// Codec comparison
const codecComparison = {
  'H.264': {
    quality: 'Good',
    compression: 'Good',
    compatibility: 'Excellent',
    encoding_speed: 'Fast',
    use_case: 'General purpose, best compatibility'
  },
  'H.265 (HEVC)': {
    quality: 'Excellent',
    compression: 'Excellent',
    compatibility: 'Good',
    encoding_speed: 'Slow',
    use_case: '4K video, bandwidth-constrained'
  },
  'VP9': {
    quality: 'Excellent',
    compression: 'Excellent',
    compatibility: 'Good',
    encoding_speed: 'Very Slow',
    use_case: 'YouTube, WebM'
  },
  'AV1': {
    quality: 'Excellent',
    compression: 'Best',
    compatibility: 'Limited',
    encoding_speed: 'Extremely Slow',
    use_case: 'Future-proof, best compression'
  }
};

function selectCodec(requirements: CodecRequirements): string {
  if (requirements.prioritize === 'compatibility') {
    return 'libx264'; // H.264
  }
  
  if (requirements.prioritize === 'quality' && requirements.resolution === '4K') {
    return 'libx265'; // H.265
  }
  
  if (requirements.prioritize === 'compression') {
    return 'libaom-av1'; // AV1
  }
  
  return 'libx264'; // Default
}

interface CodecRequirements {
  prioritize: 'compatibility' | 'quality' | 'compression' | 'speed';
  resolution: string;
}
```

## Quality vs Size Optimization

```bash
# CRF (Constant Rate Factor) - balance quality and size
# Lower CRF = better quality, larger file
# Higher CRF = lower quality, smaller file

# High quality (CRF 18-23)
ffmpeg -i input.mp4 -c:v libx264 -crf 20 -preset slow output_hq.mp4

# Balanced (CRF 23-28)
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset medium output_balanced.mp4

# Small file (CRF 28-35)
ffmpeg -i input.mp4 -c:v libx264 -crf 30 -preset fast output_small.mp4

# Two-pass encoding for precise bitrate control
ffmpeg -i input.mp4 -c:v libx264 -b:v 2M -pass 1 -f null /dev/null
ffmpeg -i input.mp4 -c:v libx264 -b:v 2M -pass 2 output_2pass.mp4
```

## Hardware Acceleration

```bash
# NVIDIA GPU (NVENC)
ffmpeg -hwaccel cuda -i input.mp4 \
  -c:v h264_nvenc \
  -preset fast \
  -b:v 5M \
  output_nvenc.mp4

# Intel Quick Sync (QSV)
ffmpeg -hwaccel qsv -c:v h264_qsv -i input.mp4 \
  -c:v h264_qsv \
  -preset medium \
  -b:v 5M \
  output_qsv.mp4

# AMD GPU (AMF)
ffmpeg -hwaccel d3d11va -i input.mp4 \
  -c:v h264_amf \
  -b:v 5M \
  output_amf.mp4

# Apple VideoToolbox (macOS)
ffmpeg -i input.mp4 \
  -c:v h264_videotoolbox \
  -b:v 5M \
  output_vt.mp4
```

## AWS Elemental MediaConvert

```typescript
// services/aws-mediaconvert.service.ts
import {
  MediaConvertClient,
  CreateJobCommand,
  GetJobCommand
} from '@aws-sdk/client-mediaconvert';

export class AWSMediaConvertService {
  private client: MediaConvertClient;

  constructor() {
    this.client = new MediaConvertClient({
      region: process.env.AWS_REGION!,
      endpoint: process.env.MEDIACONVERT_ENDPOINT
    });
  }

  async createTranscodingJob(inputS3Uri: string, outputS3Uri: string): Promise<string> {
    const command = new CreateJobCommand({
      Role: process.env.MEDIACONVERT_ROLE!,
      Settings: {
        Inputs: [{
          FileInput: inputS3Uri,
          AudioSelectors: {
            'Audio Selector 1': {
              DefaultSelection: 'DEFAULT'
            }
          }
        }],
        OutputGroups: [{
          Name: 'File Group',
          OutputGroupSettings: {
            Type: 'FILE_GROUP_SETTINGS',
            FileGroupSettings: {
              Destination: outputS3Uri
            }
          },
          Outputs: [
            this.create1080pOutput(),
            this.create720pOutput(),
            this.create480pOutput()
          ]
        }]
      }
    });

    const response = await this.client.send(command);
    return response.Job?.Id!;
  }

  private create1080pOutput() {
    return {
      NameModifier: '_1080p',
      VideoDescription: {
        Width: 1920,
        Height: 1080,
        CodecSettings: {
          Codec: 'H_264',
          H264Settings: {
            Bitrate: 5000000,
            RateControlMode: 'CBR'
          }
        }
      },
      AudioDescriptions: [{
        CodecSettings: {
          Codec: 'AAC',
          AacSettings: {
            Bitrate: 128000,
            SampleRate: 48000
          }
        }
      }],
      ContainerSettings: {
        Container: 'MP4'
      }
    };
  }

  private create720pOutput() {
    return {
      NameModifier: '_720p',
      VideoDescription: {
        Width: 1280,
        Height: 720,
        CodecSettings: {
          Codec: 'H_264',
          H264Settings: {
            Bitrate: 3000000,
            RateControlMode: 'CBR'
          }
        }
      },
      AudioDescriptions: [{
        CodecSettings: {
          Codec: 'AAC',
          AacSettings: {
            Bitrate: 128000,
            SampleRate: 48000
          }
        }
      }],
      ContainerSettings: {
        Container: 'MP4'
      }
    };
  }

  async getJobStatus(jobId: string): Promise<string> {
    const command = new GetJobCommand({ Id: jobId });
    const response = await this.client.send(command);
    return response.Job?.Status!;
  }
}
```

## Progress Monitoring

```typescript
// services/transcoding-monitor.service.ts
export class TranscodingMonitorService {
  async monitorProgress(jobId: string): Promise<void> {
    const interval = setInterval(async () => {
      const progress = await this.getProgress(jobId);

      // Update database
      await db.transcodingJob.update({
        where: { id: jobId },
        data: { progress: progress.percent }
      });

      // Emit WebSocket event
      io.emit('transcoding-progress', {
        jobId,
        progress: progress.percent,
        status: progress.status
      });

      if (progress.status === 'COMPLETE' || progress.status === 'ERROR') {
        clearInterval(interval);
      }
    }, 5000); // Check every 5 seconds
  }

  private async getProgress(jobId: string): Promise<TranscodingProgress> {
    // Implementation depends on transcoding service
    return {
      percent: 0,
      status: 'PROGRESSING'
    };
  }
}

interface TranscodingProgress {
  percent: number;
  status: string;
}
```

## Cost Optimization

```typescript
// Cost optimization strategies
export class TranscodingCostOptimizer {
  async optimizeCosts(videoId: string): Promise<void> {
    const video = await db.video.findUnique({ where: { id: videoId } });

    if (!video) return;

    // Only transcode popular videos to all resolutions
    if (video.views < 100) {
      // Only create 720p and 480p
      await this.transcodeToResolutions(videoId, ['720p', '480p']);
    } else {
      // Create all resolutions
      await this.transcodeToResolutions(videoId, ['1080p', '720p', '480p', '360p']);
    }

    // Use spot instances for batch transcoding
    // Schedule transcoding during off-peak hours
    // Use hardware acceleration when available
  }

  private async transcodeToResolutions(videoId: string, resolutions: string[]): Promise<void> {
    // Implementation
  }
}
```

---

## Quick Start

### FFmpeg Transcoding

```bash
# Transcode to multiple resolutions
ffmpeg -i input.mp4 \
  -c:v libx264 -preset medium -crf 23 \
  -vf "scale=1920:1080" -b:v 5M \
  -c:a aac -b:a 128k \
  output_1080p.mp4

ffmpeg -i input.mp4 \
  -c:v libx264 -preset medium -crf 23 \
  -vf "scale=1280:720" -b:v 2.5M \
  -c:a aac -b:a 128k \
  output_720p.mp4
```

### Cloud Transcoding (AWS MediaConvert)

```typescript
const mediaConvert = new AWS.MediaConvert()

async function transcodeVideo(inputUri: string) {
  const job = await mediaConvert.createJob({
    Settings: {
      Inputs: [{
        FileInput: inputUri
      }],
      OutputGroups: [{
        Outputs: [
          { Preset: 'System-Ott_Hls_Ts_Avc_Aac_16x9_1280x720p_30Hz_4.5Mbps' },
          { Preset: 'System-Ott_Hls_Ts_Avc_Aac_16x9_1920x1080p_30Hz_6Mbps' }
        ]
      }]
    }
  })
  
  return job.Job.Id
}
```

---

## Production Checklist

- [ ] **Codec Selection**: Choose appropriate codec (H.264, H.265, VP9)
- [ ] **Quality Control**: Use CRF for quality control
- [ ] **Hardware Acceleration**: Use GPU when available
- [ ] **Multiple Resolutions**: Support adaptive streaming
- [ ] **Format Support**: Support multiple formats (MP4, WebM)
- [ ] **Processing**: Efficient processing pipeline
- [ ] **Storage**: Temporary file management
- [ ] **Monitoring**: Monitor transcoding jobs
- [ ] **Error Handling**: Handle transcoding errors
- [ ] **Testing**: Test output quality
- [ ] **Documentation**: Document transcoding settings
- [ ] **Optimization**: Optimize for speed and quality

---

## Anti-patterns

### ❌ Don't: Single Resolution

```bash
# ❌ Bad - One resolution only
ffmpeg -i input.mp4 output.mp4
# No adaptive streaming!
```

```bash
# ✅ Good - Multiple resolutions
ffmpeg -i input.mp4 output_1080p.mp4
ffmpeg -i input.mp4 output_720p.mp4
ffmpeg -i input.mp4 output_480p.mp4
# Adaptive streaming support
```

### ❌ Don't: No Quality Control

```bash
# ❌ Bad - No quality control
ffmpeg -i input.mp4 -b:v 5M output.mp4
# Fixed bitrate, inconsistent quality
```

```bash
# ✅ Good - CRF for quality
ffmpeg -i input.mp4 -c:v libx264 -crf 23 output.mp4
# Consistent quality, variable bitrate
```

---

## Integration Points

- **Adaptive Bitrate** (`37-video-streaming/adaptive-bitrate/`) - ABR streaming
- **Live Streaming** (`37-video-streaming/live-streaming/`) - Live transcoding
- **CDN Delivery** (`37-video-streaming/cdn-delivery/`) - CDN distribution

---

## Further Reading

- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [AWS MediaConvert](https://aws.amazon.com/mediaconvert/)
- [Video Codec Guide](https://www.streamingmedia.com/Articles/Editorial/What-Is-What/What-Is-H.264-78221.aspx)

## Best Practices

1. **Codec Selection** - Choose codec based on requirements
2. **Quality** - Use CRF for quality control
3. **Hardware Acceleration** - Use GPU when available
4. **Multiple Resolutions** - Support adaptive streaming
5. **Progress Tracking** - Monitor transcoding progress
6. **Error Handling** - Handle transcoding failures
7. **Cost Optimization** - Optimize transcoding costs
8. **Queue Management** - Use queues for async processing
9. **Storage** - Clean up temporary files
10. **Testing** - Test output quality

## Resources

- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [AWS MediaConvert](https://aws.amazon.com/mediaconvert/)
- [Mux Video](https://mux.com/)
- [Cloudinary Video](https://cloudinary.com/video)
- [H.264 vs H.265](https://www.encoding.com/h265/)
