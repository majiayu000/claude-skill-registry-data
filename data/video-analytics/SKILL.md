---
name: Video Analytics
description: Tracking viewer behavior, engagement, and quality metrics for video content including player events, QoE metrics, watch time, and analytics dashboards.
---

# Video Analytics

> **Current Level:** Intermediate  
> **Domain:** Video Streaming / Analytics

---

## Overview

Video analytics tracks viewer behavior, engagement, and quality metrics. This guide covers player events, QoE metrics, and analytics dashboards for understanding video performance and viewer engagement.

## Video Metrics

### Core Metrics

```typescript
// types/analytics.ts
export interface VideoMetrics {
  // View metrics
  views: number;
  uniqueViews: number;
  impressions: number;
  
  // Engagement metrics
  watchTime: number; // Total seconds watched
  averageWatchTime: number;
  completionRate: number; // Percentage who finished
  engagementRate: number;
  
  // Quality metrics (QoE)
  averageBufferTime: number;
  averageStartTime: number;
  averageBitrate: number;
  errorRate: number;
  
  // Interaction metrics
  likes: number;
  shares: number;
  comments: number;
}
```

## Player Events Tracking

```typescript
// services/video-analytics.service.ts
export class VideoAnalyticsService {
  private sessionId: string;
  private startTime: number = 0;
  private lastPosition: number = 0;
  private watchedSegments: Set<number> = new Set();

  constructor(private videoId: string, private userId?: string) {
    this.sessionId = this.generateSessionId();
  }

  trackPlay(): void {
    this.startTime = Date.now();
    
    this.sendEvent({
      event: 'play',
      videoId: this.videoId,
      sessionId: this.sessionId,
      userId: this.userId,
      timestamp: Date.now()
    });
  }

  trackPause(position: number): void {
    const watchTime = (Date.now() - this.startTime) / 1000;
    
    this.sendEvent({
      event: 'pause',
      videoId: this.videoId,
      sessionId: this.sessionId,
      position,
      watchTime,
      timestamp: Date.now()
    });
  }

  trackProgress(position: number, duration: number): void {
    // Track 25%, 50%, 75%, 100% milestones
    const percentage = (position / duration) * 100;
    const milestones = [25, 50, 75, 100];

    milestones.forEach(milestone => {
      if (percentage >= milestone && !this.watchedSegments.has(milestone)) {
        this.watchedSegments.add(milestone);
        
        this.sendEvent({
          event: 'milestone',
          videoId: this.videoId,
          sessionId: this.sessionId,
          milestone,
          position,
          timestamp: Date.now()
        });
      }
    });

    this.lastPosition = position;
  }

  trackSeek(from: number, to: number): void {
    this.sendEvent({
      event: 'seek',
      videoId: this.videoId,
      sessionId: this.sessionId,
      from,
      to,
      timestamp: Date.now()
    });
  }

  trackQualityChange(oldQuality: string, newQuality: string): void {
    this.sendEvent({
      event: 'quality_change',
      videoId: this.videoId,
      sessionId: this.sessionId,
      oldQuality,
      newQuality,
      timestamp: Date.now()
    });
  }

  trackBuffering(duration: number): void {
    this.sendEvent({
      event: 'buffering',
      videoId: this.videoId,
      sessionId: this.sessionId,
      duration,
      position: this.lastPosition,
      timestamp: Date.now()
    });
  }

  trackError(error: string): void {
    this.sendEvent({
      event: 'error',
      videoId: this.videoId,
      sessionId: this.sessionId,
      error,
      position: this.lastPosition,
      timestamp: Date.now()
    });
  }

  trackEnd(): void {
    const totalWatchTime = (Date.now() - this.startTime) / 1000;
    
    this.sendEvent({
      event: 'end',
      videoId: this.videoId,
      sessionId: this.sessionId,
      watchTime: totalWatchTime,
      timestamp: Date.now()
    });
  }

  private async sendEvent(event: any): Promise<void> {
    await fetch('/api/analytics/video-event', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(event)
    });
  }

  private generateSessionId(): string {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
}

// Usage with Video.js
const analytics = new VideoAnalyticsService(videoId, userId);

player.on('play', () => analytics.trackPlay());
player.on('pause', () => analytics.trackPause(player.currentTime()));
player.on('timeupdate', () => {
  analytics.trackProgress(player.currentTime(), player.duration());
});
player.on('seeked', () => {
  analytics.trackSeek(previousTime, player.currentTime());
});
player.on('ended', () => analytics.trackEnd());
player.on('error', (e) => analytics.trackError(e.message));
```

## Quality of Experience (QoE) Metrics

```typescript
// services/qoe-tracker.service.ts
export class QoETrackerService {
  private metrics: QoEMetrics = {
    startupTime: 0,
    bufferingEvents: [],
    bitrateChanges: [],
    errors: []
  };

  trackStartupTime(time: number): void {
    this.metrics.startupTime = time;
  }

  trackBuffering(startTime: number, endTime: number): void {
    this.metrics.bufferingEvents.push({
      startTime,
      endTime,
      duration: endTime - startTime
    });
  }

  trackBitrateChange(timestamp: number, bitrate: number): void {
    this.metrics.bitrateChanges.push({
      timestamp,
      bitrate
    });
  }

  trackError(error: VideoError): void {
    this.metrics.errors.push(error);
  }

  calculateQoEScore(): number {
    let score = 100;

    // Penalize long startup time
    if (this.metrics.startupTime > 3000) {
      score -= 20;
    } else if (this.metrics.startupTime > 1000) {
      score -= 10;
    }

    // Penalize buffering
    const totalBuffering = this.metrics.bufferingEvents.reduce(
      (sum, event) => sum + event.duration,
      0
    );
    score -= Math.min(totalBuffering / 1000 * 5, 30);

    // Penalize frequent bitrate changes
    if (this.metrics.bitrateChanges.length > 10) {
      score -= 15;
    }

    // Penalize errors
    score -= this.metrics.errors.length * 10;

    return Math.max(score, 0);
  }

  getMetrics(): QoEMetrics {
    return this.metrics;
  }
}

interface QoEMetrics {
  startupTime: number;
  bufferingEvents: BufferingEvent[];
  bitrateChanges: BitrateChange[];
  errors: VideoError[];
}

interface BufferingEvent {
  startTime: number;
  endTime: number;
  duration: number;
}

interface BitrateChange {
  timestamp: number;
  bitrate: number;
}

interface VideoError {
  code: string;
  message: string;
  timestamp: number;
}
```

## Heatmaps

```typescript
// services/heatmap.service.ts
export class HeatmapService {
  async generateHeatmap(videoId: string): Promise<HeatmapData> {
    // Get all view events
    const events = await db.videoEvent.findMany({
      where: {
        videoId,
        event: { in: ['play', 'pause', 'seek'] }
      }
    });

    // Get video duration
    const video = await db.video.findUnique({ where: { id: videoId } });
    const duration = video?.duration || 0;

    // Create time buckets (1 second intervals)
    const buckets = new Array(Math.ceil(duration)).fill(0);

    // Count views for each second
    events.forEach(event => {
      if (event.position !== undefined) {
        const bucket = Math.floor(event.position);
        if (bucket < buckets.length) {
          buckets[bucket]++;
        }
      }
    });

    // Normalize to percentage
    const maxViews = Math.max(...buckets);
    const normalized = buckets.map(count => (count / maxViews) * 100);

    return {
      videoId,
      duration,
      data: normalized
    };
  }

  async getDropOffPoints(videoId: string): Promise<DropOffPoint[]> {
    const heatmap = await this.generateHeatmap(videoId);
    const dropOffs: DropOffPoint[] = [];

    // Find significant drops (>20% decrease)
    for (let i = 1; i < heatmap.data.length; i++) {
      const drop = heatmap.data[i - 1] - heatmap.data[i];
      if (drop > 20) {
        dropOffs.push({
          timestamp: i,
          dropPercentage: drop,
          viewsBefore: heatmap.data[i - 1],
          viewsAfter: heatmap.data[i]
        });
      }
    }

    return dropOffs.sort((a, b) => b.dropPercentage - a.dropPercentage);
  }
}

interface HeatmapData {
  videoId: string;
  duration: number;
  data: number[]; // Percentage of viewers at each second
}

interface DropOffPoint {
  timestamp: number;
  dropPercentage: number;
  viewsBefore: number;
  viewsAfter: number;
}
```

## A/B Testing

```typescript
// services/video-ab-test.service.ts
export class VideoABTestService {
  async assignVariant(userId: string, testId: string): Promise<string> {
    // Check if user already assigned
    const existing = await db.abTestAssignment.findUnique({
      where: {
        userId_testId: { userId, testId }
      }
    });

    if (existing) {
      return existing.variant;
    }

    // Assign variant (50/50 split)
    const variant = Math.random() < 0.5 ? 'A' : 'B';

    await db.abTestAssignment.create({
      data: {
        userId,
        testId,
        variant
      }
    });

    return variant;
  }

  async trackConversion(userId: string, testId: string, metric: string, value: number): Promise<void> {
    await db.abTestMetric.create({
      data: {
        userId,
        testId,
        metric,
        value
      }
    });
  }

  async getTestResults(testId: string): Promise<ABTestResults> {
    const assignments = await db.abTestAssignment.groupBy({
      by: ['variant'],
      where: { testId },
      _count: true
    });

    const metrics = await db.abTestMetric.groupBy({
      by: ['variant', 'metric'],
      where: { testId },
      _avg: { value: true }
    });

    return {
      testId,
      assignments: assignments.map(a => ({
        variant: a.variant,
        count: a._count
      })),
      metrics: metrics.map(m => ({
        variant: m.variant,
        metric: m.metric,
        average: m._avg.value || 0
      }))
    };
  }
}

interface ABTestResults {
  testId: string;
  assignments: { variant: string; count: number }[];
  metrics: { variant: string; metric: string; average: number }[];
}
```

## Analytics Dashboard

```typescript
// components/AnalyticsDashboard.tsx
export function AnalyticsDashboard({ videoId }: { videoId: string }) {
  const [metrics, setMetrics] = useState<VideoMetrics | null>(null);
  const [heatmap, setHeatmap] = useState<HeatmapData | null>(null);

  useEffect(() => {
    loadAnalytics();
  }, [videoId]);

  const loadAnalytics = async () => {
    const [metricsData, heatmapData] = await Promise.all([
      fetch(`/api/analytics/video/${videoId}/metrics`).then(r => r.json()),
      fetch(`/api/analytics/video/${videoId}/heatmap`).then(r => r.json())
    ]);

    setMetrics(metricsData);
    setHeatmap(heatmapData);
  };

  return (
    <div className="analytics-dashboard">
      <div className="metrics-grid">
        <MetricCard title="Views" value={metrics?.views || 0} />
        <MetricCard title="Watch Time" value={formatDuration(metrics?.watchTime || 0)} />
        <MetricCard title="Completion Rate" value={`${metrics?.completionRate || 0}%`} />
        <MetricCard title="Engagement" value={`${metrics?.engagementRate || 0}%`} />
      </div>

      {heatmap && (
        <div className="heatmap">
          <h3>Viewer Retention</h3>
          <HeatmapChart data={heatmap} />
        </div>
      )}

      <div className="qoe-metrics">
        <h3>Quality of Experience</h3>
        <QoEChart videoId={videoId} />
      </div>
    </div>
  );
}
```

---

## Quick Start

### Video Event Tracking

```typescript
// Track video events
function trackVideoEvent(
  videoId: string,
  event: 'play' | 'pause' | 'seek' | 'complete',
  timestamp: number
) {
  analytics.track('video_event', {
    videoId,
    event,
    timestamp,
    watchTime: calculateWatchTime(videoId)
  })
}

// Calculate watch time
function calculateWatchTime(videoId: string): number {
  const events = getVideoEvents(videoId)
  let watchTime = 0
  let lastPlayTime = 0
  
  events.forEach(event => {
    if (event.type === 'play') {
      lastPlayTime = event.timestamp
    } else if (event.type === 'pause') {
      watchTime += event.timestamp - lastPlayTime
    }
  })
  
  return watchTime
}
```

---

## Production Checklist

- [ ] **Event Tracking**: Track all video events
- [ ] **Watch Time**: Calculate accurate watch time
- [ ] **Engagement Metrics**: Track engagement (completion rate, etc.)
- [ ] **Quality Metrics**: Track video quality (buffering, bitrate)
- [ ] **Privacy**: Anonymize user data
- [ ] **Sampling**: Use sampling for high traffic
- [ ] **Real-time**: Real-time analytics
- [ ] **Aggregation**: Pre-aggregate metrics
- [ ] **Dashboards**: Analytics dashboards
- [ ] **Retention**: Data retention policies
- [ ] **Performance**: Don't impact playback
- [ ] **Testing**: Test analytics implementation

---

## Anti-patterns

### ❌ Don't: Track Too Much

```typescript
// ❌ Bad - Track every millisecond
setInterval(() => {
  trackEvent('heartbeat', { timestamp: Date.now() })
}, 1)  // Too much data!
```

```typescript
// ✅ Good - Track key events
video.addEventListener('play', () => trackEvent('play'))
video.addEventListener('pause', () => trackEvent('pause'))
video.addEventListener('ended', () => trackEvent('complete'))
```

### ❌ Don't: No Privacy

```typescript
// ❌ Bad - Track personal data
trackEvent('video_view', {
  userId: user.id,
  email: user.email,  // Privacy issue!
  videoId: video.id
})
```

```typescript
// ✅ Good - Anonymize
trackEvent('video_view', {
  userId: hashUserId(user.id),  // Anonymized
  videoId: video.id
})
```

---

## Integration Points

- **Live Streaming** (`37-video-streaming/live-streaming/`) - Live analytics
- **Adaptive Bitrate** (`37-video-streaming/adaptive-bitrate/`) - Quality metrics
- **Analytics** (`23-business-analytics/`) - General analytics

---

## Further Reading

- [Video Analytics Best Practices](https://www.wistia.com/learn/analytics)
- [Video Metrics Guide](https://www.brightcove.com/en/resources/video-analytics/)

## Resources

- [Google Analytics for Video](https://support.google.com/analytics/answer/1136960)
- [Mux Data](https://mux.com/data)
- [Video.js Analytics](https://videojs.com/plugins/)
- [YouTube Analytics](https://support.google.com/youtube/topic/9257891)
