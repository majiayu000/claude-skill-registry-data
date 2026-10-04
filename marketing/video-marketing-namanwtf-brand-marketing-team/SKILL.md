---
name: video-marketing
description: Automated video script writing, editing optimization, and platform-specific formatting
author: "@namanwtf"
version: 3.0.0
requires: brand-context, copywriting, social-content
category: video
---

# 🎬 Video Marketing Agent

**Purpose:** Create viral video content for TikTok, Reels, YouTube Shorts, and long-form—optimized for each platform's algorithm.

---

## When to Use

```bash
# Create TikTok/Reel script
@video-marketing script --platform tiktok --topic "unboxing"

# Optimize video for engagement
@video-marketing optimize /videos/draft.mp4

# Generate thumbnail
@video-marketing thumbnail "Product X Review"

# Platform reformatting
@video-marketing reformat youtube --to tiktok

# Script from blog post
@video-marketing convert /blog/post-url
```

---

## Capabilities

### 1. Script Generation
- Hook-first openings (first 3 seconds critical)
- Platform-optimized pacing
- Call-to-action placement
- Caption/subtitle generation
- Trending audio suggestions

### 2. Video Optimization
- Aspect ratio conversion (9:16, 16:9, 1:1)
- Attention heatmap analysis
- Optimal video length per platform
- Pacing recommendations
- B-roll suggestions

### 3. Thumbnail & Title
- Click-worthy thumbnail design
- High-CTR title generation
- A/B testing variations
- Brand consistency
- Platform-specific best practices

### 4. Multi-Platform Repurposing
- Long-form YouTube → Shorts
- Podcast clips → Reels
- Webinar segments → TikToks
- Live stream highlights
- Auto-resize and reformat

---

## Usage Examples

### TikTok Script
```
User: @video-marketing script --platform tiktok --topic "battery test"

Agent: 🎬 TIKTOK SCRIPT: "48-Hour Battery Challenge"

HOOK (0-3 sec):
[Show phone at 100% battery]
"I'm going to use this phone for 48 hours WITHOUT charging"

BODY (3-25 sec):
[Hour 12: Gaming session]
"Hour 12: 3 hours of gaming... still at 78%"

[Hour 24: All-day use]
"Hour 24: Full day of photos, videos, calls... 45% left"

[Hour 36: More gaming]
"Hour 36: Another gaming session... 23%"

[Hour 48: The reveal]
"Hour 48: STILL GOING at 8%!"

CTA (25-30 sec):
"Product X. Two days, one charge. Link in bio"
[Text overlay: "Long Battery Life"]

Technical Specs:
• Duration: 30 seconds
• Format: 9:16 vertical
• Captions: Required (burn-in)
• Audio: Trending music + voiceover
• Text overlays: 3-5 key points
```

### YouTube Optimization
```
User: @video-marketing optimize /videos/product-x-review-draft.mp4

Agent: 🎥 YOUTUBE OPTIMIZATION REPORT

Current Issues:
❌ Title too generic: "Product X Review"
❌ Thumbnail text unreadable at small size
❌ Hook at 45 seconds (should be 0-15)
❌ No chapters for skip navigation
❌ Missing end screen cards

Optimizations:
✅ New Title: "I Used This Product for 7 Days Straight... (Product X Review)"
✅ Thumbnail: Large "7000mAh" text, surprised face, arrow pointing to phone
✅ New Hook (0-15 sec): "This phone lasted 3 days without charging. I'm not kidding."
✅ Chapters added:
   • 0:00 Intro
   • 1:30 Unboxing
   • 3:45 Battery Test
   • 8:20 Camera
   • 12:10 Gaming
   • 15:30 Final Verdict
✅ End screen: Subscribe + 2 related videos

Expected CTR improvement: +45%
```

### Multi-Platform Repurpose
```
User: @video-marketing reformat /videos/youtube-review.mp4 --platforms all

Agent: 🔄 MULTI-PLATFORM PACKAGE

Original: 15-min YouTube review

OUTPUTS CREATED:

📱 TikTok (9:16, 60 sec):
• Hook: "This $200 phone beat my iPhone"
• Battery highlight clip
• Gaming performance clip
• Quick camera test
• CTA with link

📸 Instagram Reel (9:16, 90 sec):
• Same as TikTok + unboxing moment
• Story-style transitions
• Trending audio sync

📺 YouTube Short (9:16, 60 sec):
• Battery test only
• "Part 1 of 5" series hook
• Link to full video

🐦 Twitter/X (16:9, 45 sec):
• Gaming comparison clip
• Thread starter

💼 LinkedIn (16:9, 90 sec):
• Business/productivity angle
• ROI focus

All optimized for platform algorithms ✓
All have custom thumbnails ✓
All have platform-specific captions ✓
```

---

## Configuration

```yaml
video-marketing:
  platforms:
    tiktok:
      duration: [15, 60]
      aspect: "9:16"
      captions: true
      hooks: ["controversy", "surprise", "transformation"]
      
    youtube:
      duration: [480, 1800]
      aspect: "16:9"
      chapters: true
      cards: 3
      
    instagram:
      reels: {duration: [15, 90], aspect: "9:16"}
      feed: {duration: [3, 60], aspect: ["1:1", "4:5"]}
      
  brand-elements:
    intro-duration: 3
    outro-duration: 5
    logo-placement: "bottom-right"
    color-grade: "vibrant"
```

---

*Part of the Brand Marketing Team framework.*
*Author: @namanwtf | Version 3.0.0 | MIT License*
