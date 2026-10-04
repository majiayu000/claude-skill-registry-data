---
name: video-streaming
description: Video streaming expertise from Netflix - the world's largest streaming service. Master video encoding, adaptive bitrate streaming, CDN optimization, and global delivery. Use when building video platforms, optimizing streaming quality, or scaling video delivery. Learn from 260M+ subscribers, 99.999% uptime.
expert_level: 10/10
source_company: Netflix
specialist: netflix-backend-architect
related:
  - aws-expert
  - microservices
  - performance-optimization
---

# Video Streaming - Netflix Expertise

**Expert**: Marcus Johnson (Netflix, 14 years)
**Level**: 10/10 - Netflix Principal Engineer

## Overview

Video streaming at Netflix scale - 260M+ subscribers, petabytes of video served daily, 99.999% uptime. The playbook that powers the world's largest streaming service.

Netflix didn't just build a streaming service - they revolutionized how video is delivered globally.

## When to Use What

**Video Encoding:**
- H.264 (AVC) - Universal compatibility - H.265 (HEVC) - 50% better compression
- AV1 - Next-gen, 30% better than HEVC

**Streaming Protocols:**
- HLS - Apple devices, iOS/Safari - DASH - Android, web browsers
- CMAF - Unified format for both

**CDN Strategy:**
- Multi-CDN - AWS CloudFront, Akamai, Fastly - Open Connect - Netflix's own CDN

**Quality Metrics:**
- VMAF - Video quality scoring 
## Core Workflow

1. **Ingest** - Upload source video (high quality)
2. **Encode** - Multi-bitrate ladder (4K → 240p)
3. **Package** - HLS/DASH manifests
4. **Distribute** - Upload to CDN/S3
5. **Stream** - Adaptive bitrate playback
6. **Monitor** - Quality metrics, rebuffer rate

## Netflix's Encoding Pipeline

**Per-Title Encoding:**
- Analyze each title's complexity
- Optimize bitrate ladder per video
- Save bandwidth without quality loss

**Example**: Simple animation needs less bitrate than action movie.

## Adaptive Bitrate Streaming (ABR)

Client automatically switches quality based on network:

```
Network fast → 4K (16 Mbps)
Network medium → 1080p (5 Mbps)
Network slow → 480p (1 Mbps)
```

## Netflix's Global Scale

- **260M+ subscribers** worldwide
- **Billions of hours** streamed monthly
- **15,000+ video titles** (each in 10+ bitrates)
- **Petabytes** served daily
- **99.999% uptime** (5 minutes/year downtime)

## CDN Strategy

Netflix uses:
1. **Open Connect** - Own CDN, 95% of traffic
2. **AWS CloudFront** - Backup/overflow
3. **Edge caching** - Videos cached near users

## Best Practices

1. **Per-title encoding** - Optimize bitrate per video
2. **VMAF quality scoring** - Measure perceptual quality
3. **Multi-CDN** - Redundancy and performance
4. **Adaptive bitrate** - Smooth playback on varying networks
5. **Edge caching** - Reduce latency globally

## Related Skills

- **[aws-expert](../aws-expert/SKILL.md)** - S3, CloudFront CDN
- **[microservices](../microservices/SKILL.md)** - Netflix architecture
- **[performance-optimization](../performance-optimization/SKILL.md)** - Video player optimization

---

**Last Updated**: 2026-02-03
**Expert**: Marcus Johnson (Netflix, 14 years) - Streams to 260M+ users
