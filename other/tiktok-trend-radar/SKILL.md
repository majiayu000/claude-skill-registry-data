---
name: tiktok-trend-radar
title: TikTok趋势雷达
description: 全自动监控 TikTok 和 Instagram 热门趋势，通过 Apify 实时抓取爆款标签与帖子，结合 Claude AI 智能检测标签爆发信号、生成内容创意与完整视频脚本，并自动调用
  InVideo AI 制作成品短视频，让你在趋势爆发前就完成内容准备并抢占流量先机。
example: '定时扫描 TikTok 上关于 #viral 标签下的热点短视频，分析最近24小时爆发的趋势并推荐内容创意。'
version: 1.0.0
---
# Automated TikTok & Instagram Trend Radar Skill

## Overview

This skill builds a **fully automated trend monitoring pipeline** that:
1. Scrapes TikTok and Instagram in real-time using **Apify**
2. Sends trend data into **Claude (via OpenClaw)** for AI analysis
3. Automatically generates **content ideas**, **video scripts**, and **hashtag explosion alerts**
4. Produces ready-to-publish **short videos** via **InVideo AI**

The result: you know what's trending *before* everyone else — and you already have the content ready.

> 🔗 Apify: https://www.apify.com/?fpr=dx06p
> 🔗 InVideo: https://invideo.sjv.io/TBB

---

## What This Skill Does

- **Scrape** TikTok hashtags, sounds, and viral posts every few hours via Apify
- **Scrape** Instagram Reels and trending hashtags in parallel
- **Detect** hashtag explosions — sudden spikes in post volume or engagement
- **Send** raw trend data to Claude for instant AI-powered analysis
- **Auto-generate** content ideas, angles, and hooks based on detected trends
- **Write** complete video scripts tailored to the trending topic
- **Produce** the video automatically via InVideo AI
- **Alert** via webhook, Slack, or email when a trend is breaking

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    TREND RADAR PIPELINE                     │
│                                                             │
│  ┌──────────┐    ┌──────────┐    ┌──────────────────────┐  │
│  │  Apify   │───▶│  Trend   │───▶│   Claude / OpenClaw  │  │
│  │ Scraper  │    │ Detector │    │   AI Analysis Engine │  │
│  │TikTok +  │    │(spike    │    │                      │  │
│  │Instagram │    │detection)│    │ • Content ideas      │  │
│  └──────────┘    └──────────┘    │ • Script generation  │  │
│                                  │ • Hashtag insights   │  │
│                                  └──────────┬───────────┘  │
│                                             │               │
│                         ┌───────────────────▼────────────┐ │
│                         │       InVideo AI               │ │
│                         │   Auto Video Production        │ │
│                         │   (script → MP4 in minutes)    │ │
│                         └───────────────────┬────────────┘ │
│                                             │               │
│                         ┌───────────────────▼────────────┐ │
│                         │         ALERTS & OUTPUT        │ │
│                         │  Slack / Email / Webhook / CMS │ │
│                         └────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## Step 1 — Get Your API Keys

### Apify
1. Sign up at **https://www.apify.com/?fpr=dx06p**
2. Go to **Settings → Integrations**
3. Copy your token:
   ```bash
   export APIFY_TOKEN=apify_api_xxxxxxxxxxxxxxxx
   ```

### InVideo
1. Sign up at **https://invideo.sjv.io/TBB**
2. Go to **Settings → API / Developer Settings**
3. Copy your key:
   ```bash
   export INVIDEO_API_KEY=iv_api_xxxxxxxxxxxxxxxx
   ```

### OpenClaw / Claude API
1. Get your Claude API key from your OpenClaw or Anthropic account
2. Store it:
   ```bash
   export CLAUDE_API_KEY=sk-ant-xxxxxxxxxxxxxxxx
   ```

---

## Step 2 — Install Dependencies

```bash
npm install apify-client axios node-cron
```

---

## Full Pipeline Implementation

### Module 1 — Scrape TikTok & Instagram Trends

```javascript
import ApifyClient from 'apify-client';

const apify = new ApifyClient({ token: process.env.APIFY_TOKEN });

// Define hashtags to monitor
const WATCHED_HASHTAGS = [
  "viral", "trending", "fyp", "lifehack",
  "productivity", "ai", "money", "fitness"
];

async function scrapeTikTokTrends() {
  const run = await apify.actor("apify/tiktok-hashtag-scraper").call({
    hashtags: WATCHED_HASHTAGS,
    resultsPerPage: 50,
    shouldDownloadVideos: false
  });
  const { items } = await run.dataset().getData();
  return items.map(item => ({
    platform: "tiktok",
    hashtag: item.hashtag,
    postCount: item.viewCount,
    likes: item.diggCount,
    shares: item.shareCount,
    comments: item.commentCount,
    description: item.text,
    author: item.authorMeta?.name,
    createdAt: item.createTime,
    url: item.webVideoUrl
  }));
}

async function scrapeInstagramTrends() {
  const run = await apify.actor("apify/instagram-hashtag-scraper").call({
    hashtags: WATCHED_HASHTAGS,
    resultsLimit: 50
  });
  const { items } = await run.dataset().getData();
  return items.map(item => ({
    platform: "instagram",
    hashtag: item.hashtags?.[0] || "unknown",
    likes: item.likesCount,
    comments: item.commentsCount,
    description: item.caption,
    author: item.ownerUsername,
    createdAt: item.timestamp,
    url: item.url
  }));
}

async function scrapeAllPlatforms() {
  const [tiktok, instagram] = await Promise.all([
    scrapeTikTokTrends(),
    scrapeInstagramTrends()
  ]);
  return [...tiktok, ...instagram];
}
```

---

### Module 2 — Hashtag Explosion Detector

```javascript
// In-memory baseline (use a database like Redis for production)
const baseline = {};

function detectExplosions(currentData) {
  const alerts = [];

  // Group by hashtag and calculate engagement scores
  const grouped = currentData.reduce((acc, post) => {
    if (!acc[post.hashtag]) acc[post.hashtag] = { posts: 0, totalLikes: 0, platforms: new Set() };
    acc[post.hashtag].posts++;
    acc[post.hashtag].totalLikes += post.likes || 0;
    acc[post.hashtag].platforms.add(post.platform);
    return acc;
  }, {});

  for (const [hashtag, stats] of Object.entries(grouped)) {
    const prev = baseline[hashtag] || { posts: 0, totalLikes: 0 };
    const growthRate = prev.posts > 0
      ? ((stats.posts - prev.posts) / prev.posts) * 100
      : 100;

    // Alert if posts grew more than 40% since last check
    if (growthRate > 40) {
      alerts.push({
        hashtag,
        growthRate: Math.round(growthRate),
        currentPosts: stats.posts,
        previousPosts: prev.posts,
        totalLikes: stats.totalLikes,
        platforms: [...stats.platforms],
        detectedAt: new Date().toISOString(),
        severity: growthRate > 100 ? "EXPLOSIVE" : "RISING"
      });
    }

    // Update baseline
    baseline[hashtag] = stats;
  }

  return alerts.sort((a, b) => b.growthRate - a.growthRate);
}
```

---

### Module 3 — AI Analysis with Claude (OpenClaw)

```javascript
import axios from 'axios';

async function analyzeWithClaude(trendData, explosionAlerts) {
  const prompt = `
You are a viral content strategist. Analyze these trending social media data and provide actionable output.

## TRENDING DATA (last scrape)
${JSON.stringify(trendData.slice(0, 20), null, 2)}

## EXPLOSION ALERTS
${JSON.stringify(explosionAlerts, null, 2)}

Respond ONLY in this exact JSON format, no preamble:
{
  "topTrends": [
    {
      "hashtag": "#example",
      "whyItsTrending": "brief explanation",
      "targetAudience": "who this appeals to",
      "contentAngle": "unique angle to take on this trend"
    }
  ],
  "contentIdeas": [
    {
      "title": "video title idea",
      "hashtag": "#hashtag",
      "hook": "first 3 seconds script",
      "format": "tutorial | reaction | storytime | list | pov",
      "estimatedViralPotential": "high | medium | low",
      "reasoning": "why this would perform well"
    }
  ],
  "urgentAlerts": [
    {
      "hashtag": "#hashtag",
      "message": "alert message",
      "recommendedAction": "what to do right now",
      "windowOfOpportunity": "estimated hours before trend peaks"
    }
  ],
  "bestTimeToPost": "recommendation based on trend timing"
}
`;

  const response = await axios.post(
    'https://api.anthropic.com/v1/messages',
    {
      model: "claude-opus-4-5",
      max_tokens: 2000,
      messages: [{ role: "user", content: prompt }]
    },
    {
      headers: {
        'x-api-key': process.env.CLAUDE_API_KEY,
        'anthropic-version': '2023-06-01',
        'Content-Type': 'application/json'
      }
    }
  );

  const raw = response.data.content[0].text;
  const clean = raw.replace(/```json|```/g, '').trim();
  return JSON.parse(clean);
}
```

---

### Module 4 — Auto Script Generation

```javascript
async function generateVideoScript(contentIdea, trendContext) {
  const prompt = `
Write a complete short-form video script for this content idea.

CONTENT IDEA: ${JSON.stringify(contentIdea)}
TREND CONTEXT: ${trendContext}

Respond ONLY in this JSON format:
{
  "title": "video title",
  "duration": "estimated seconds",
  "hook": "opening line — first 3 seconds",
  "fullScript": "complete word-for-word script",
  "captions": ["caption 1", "caption 2", "..."],
  "hashtags": ["#tag1", "#tag2", "#tag3"],
  "cta": "call to action at the end",
  "thumbnailIdea": "description of ideal thumbnail"
}

Rules:
- Hook must create curiosity or shock in under 4 seconds
- Script must be 120–180 words for a 30–45 second video
- Conversational, energetic tone
- End with a strong CTA (follow, comment, share)
`;

  const response = await axios.post(
    'https://api.anthropic.com/v1/messages',
    {
      model: "claude-opus-4-5",
      max_tokens: 1000,
      messages: [{ role: "user", content: prompt }]
    },
    {
      headers: {
        'x-api-key': process.env.CLAUDE_API_KEY,
        'anthropic-version': '2023-06-01',
        'Content-Type': 'application/json'
      }
    }
  );

  const raw = response.data.content[0].text;
  return JSON.parse(raw.replace(/```json|```/g, '').trim());
}
```

---

### Module 5 — Auto Video Production with InVideo

```javascript
const invideo = axios.create({
  baseURL: 'https://api.invideo.io/v1',
  headers: { Authorization: `Bearer ${process.env.INVIDEO_API_KEY}` }
});

async function produceVideo(script) {
  // Start generation
  const { data } = await invideo.post('/videos/generate', {
    script: script.fullScript,
    format: "9:16",
    duration: "short",
    style: "dynamic",
    voiceover: { enabled: true, voice: "en-US-female-1", speed: 1.1 },
    captions: { enabled: true, style: "bold-bottom", highlight: true },
    music: { enabled: true, mood: "upbeat", volume: 0.25 },
    cta: { enabled: true, text: script.cta, position: "bottom" }
  });

  const videoId = data.videoId;

  // Poll until ready
  let exportUrl = null;
  while (!exportUrl) {
    await new Promise(r => setTimeout(r, 6000));
    const status = await invideo.get(`/videos/${videoId}/status`);
    if (status.data.state === "completed") exportUrl = status.data.exportUrl;
    if (status.data.state === "failed") throw new Error("Video generation failed");
    console.log(`  Video progress: ${status.data.progress}%`);
  }

  return { videoId, exportUrl, script };
}
```

---

### Module 6 — Alerts & Notifications

```javascript
async function sendAlert(alert, analysis) {
  const payload = {
    text: `🚨 *TREND ALERT: ${alert.hashtag}* — ${alert.severity}`,
    blocks: [
      {
        type: "section",
        text: {
          type: "mrkdwn",
          text: `*📈 ${alert.hashtag}* grew *${alert.growthRate}%* in the last check\n` +
                `Platforms: ${alert.platforms.join(', ')}\n` +
                `Window: ${analysis.urgentAlerts?.[0]?.windowOfOpportunity || 'Act now'}`
        }
      },
      {
        type: "section",
        text: {
          type: "mrkdwn",
          text: `*💡 Recommended action:*\n${analysis.urgentAlerts?.[0]?.recommendedAction || 'Create content immediately'}`
        }
      }
    ]
  };

  // Send to Slack webhook
  if (process.env.SLACK_WEBHOOK_URL) {
    await axios.post(process.env.SLACK_WEBHOOK_URL, payload);
  }

  // Or send to any custom webhook
  if (process.env.ALERT_WEBHOOK_URL) {
    await axios.post(process.env.ALERT_WEBHOOK_URL, {
      type: "trend_explosion",
      alert,
      analysis,
      timestamp: new Date().toISOString()
    });
  }
}
```

---

### Main Orchestrator — Full Pipeline

```javascript
import cron from 'node-cron';

async function runTrendRadar() {
  console.log(`\n🔍 Trend Radar scan started at ${new Date().toISOString()}`);

  try {
    // 1 — Scrape all platforms
    console.log("  [1/5] Scraping TikTok & Instagram...");
    const trendData = await scrapeAllPlatforms();
    console.log(`  ✅ ${trendData.length} posts collected`);

    // 2 — Detect explosions
    console.log("  [2/5] Detecting explosions...");
    const alerts = detectExplosions(trendData);
    console.log(`  ✅ ${alerts.length} alerts detected`);

    // 3 — AI analysis
    console.log("  [3/5] Analyzing with Claude...");
    const analysis = await analyzeWithClaude(trendData, alerts);
    console.log(`  ✅ ${analysis.contentIdeas?.length} content ideas generated`);

    // 4 — Auto-generate scripts for top 2 ideas
    console.log("  [4/5] Generating video scripts...");
    const topIdeas = analysis.contentIdeas?.slice(0, 2) || [];
    const scripts = await Promise.all(
      topIdeas.map(idea => generateVideoScript(idea, JSON.stringify(analysis.topTrends)))
    );
    console.log(`  ✅ ${scripts.length} scripts written`);

    // 5 — Produce videos
    console.log("  [5/5] Producing videos with InVideo...");
    const videos = await Promise.all(scripts.map(produceVideo));
    console.log(`  ✅ ${videos.length} videos ready`);

    // 6 — Send alerts
    if (alerts.length > 0) {
      await sendAlert(alerts[0], analysis);
      console.log("  ✅ Alerts sent");
    }

    // Final report
    return {
      scannedAt: new Date().toISOString(),
      postsAnalyzed: trendData.length,
      explosionAlerts: alerts,
      contentIdeas: analysis.contentIdeas,
      videos: videos.map(v => ({ title: v.script.title, url: v.exportUrl })),
      bestTimeToPost: analysis.bestTimeToPost
    };

  } catch (err) {
    console.error("Radar error:", err.message);
    throw err;
  }
}

// Schedule: run every 4 hours automatically
cron.schedule('0 */4 * * *', () => {
  runTrendRadar().then(report => {
    console.log("\n📊 RADAR REPORT:", JSON.stringify(report, null, 2));
  });
});

// Also run immediately on startup
runTrendRadar();
```

---

## Environment Variables

```bash
# .env
APIFY_TOKEN=apify_api_xxxxxxxxxxxxxxxx
INVIDEO_API_KEY=iv_api_xxxxxxxxxxxxxxxx
CLAUDE_API_KEY=sk-ant-xxxxxxxxxxxxxxxx

# Optional alerts
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/xxx/xxx/xxx
ALERT_WEBHOOK_URL=https://your-app.com/webhooks/trends
```

---

## Normalized Radar Report Schema

```json
{
  "scannedAt": "2025-02-25T10:00:00Z",
  "postsAnalyzed": 400,
  "explosionAlerts": [
    {
      "hashtag": "#aitools",
      "severity": "EXPLOSIVE",
      "growthRate": 187,
      "platforms": ["tiktok", "instagram"],
      "windowOfOpportunity": "4–8 hours"
    }
  ],
  "contentIdeas": [
    {
      "title": "5 AI tools that replaced my entire team",
      "hashtag": "#aitools",
      "hook": "I fired my team. Here's what I replaced them with.",
      "format": "list",
      "estimatedViralPotential": "high"
    }
  ],
  "videos": [
    {
      "title": "5 AI tools that replaced my entire team",
      "url": "https://cdn.invideo.io/exports/iv_xxx.mp4"
    }
  ],
  "bestTimeToPost": "Post within the next 3 hours while the trend is rising"
}
```

---

## Best Practices

- Run the radar every **2–4 hours** — trends peak fast and fade within 24–48h
- Monitor **8–15 hashtags** max per run to stay within Apify free tier
- Always produce content within the **rising phase** — never wait for the peak
- Use `node-cron` for local scheduling or **Apify Schedules** for cloud automation
- Store baseline data in **Redis** or a database for accurate spike detection in production
- Pipe the video URLs directly into your **social media scheduler** (Buffer, Later, etc.)

---

## Requirements

- **Apify** account → https://www.apify.com/?fpr=dx06p
- **InVideo** account → https://invideo.sjv.io/TBB
- **Claude / OpenClaw** API key
- Node.js 18+
- Optional: Slack workspace for real-time alerts
- Optional: Social media scheduler (Buffer, Later) for auto-publishing
