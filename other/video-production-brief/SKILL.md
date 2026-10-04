---
name: video-production-brief
description: >
  Generates video production plans including shot lists, scripts, B-roll
  suggestions, music mood, thumbnail concepts, and platform-specific specs
  for reels, YouTube, and video ads.
tags: [video, production, brief, creative, content]
---

# Video Production Brief

Generates comprehensive video production plans that a videographer, editor, or production team can execute. Covers everything from script to shot list to post-production specs. Complements `video-script` (which generates the spoken script) by wrapping it in full production planning.

## Prerequisites

- `agency.config.json` populated (agency info, services, case studies)
- Video concept or topic
- Optional: script output from `video-script`

## Phase 0: Intake

Read `agency.config.json`:
- `agency.name`, `agency.founder`, `agency.tagline` -- branding
- `services[]` -- for service explainer videos
- `case_studies[]` -- for case study video content

Accept parameters:
- `video_type` -- (required) one of: `reel`, `youtube`, `ad`, `testimonial`, `explainer`, `case-study`, `behind-the-scenes`
- `topic` -- (required) subject or concept
- `duration_target` -- (optional) target length in seconds. Default: auto based on type
- `script` -- (optional) pre-written script from `video-script`
- `platform` -- (required) one of: `instagram-reels`, `youtube`, `youtube-shorts`, `tiktok`, `linkedin`, `facebook`, `multi-platform`
- `talent` -- (optional) who appears on camera: `founder`, `team-member`, `voiceover-only`, `text-only`
- `budget_level` -- (optional) `low` (phone + natural light), `medium` (basic setup), `high` (full production). Default: `medium`

## Phase 1: Format Specs

### Platform-Specific Requirements
| Platform | Aspect | Max Duration | Resolution | File Format |
|----------|--------|-------------|------------|-------------|
| Instagram Reels | 9:16 | 90 seconds | 1080x1920 | MP4 (H.264) |
| YouTube | 16:9 | 15+ minutes | 1920x1080 (min) | MP4 (H.264) |
| YouTube Shorts | 9:16 | 60 seconds | 1080x1920 | MP4 |
| TikTok | 9:16 | 10 minutes | 1080x1920 | MP4 |
| LinkedIn | 16:9 or 1:1 | 10 minutes | 1920x1080 | MP4 |
| Facebook | 16:9, 1:1, 9:16 | 240 minutes | 1920x1080 | MP4 |

### Duration Guidelines by Type
| Video Type | Reel/Short | YouTube | Ad |
|-----------|------------|---------|-----|
| Explainer | 30-60s | 5-8 min | 15-30s |
| Case study | 45-90s | 3-5 min | 30-60s |
| Testimonial | 30-60s | 2-4 min | 15-30s |
| Behind-the-scenes | 15-60s | 5-10 min | N/A |
| Ad/promo | 15-30s | N/A | 15-60s |

## Phase 2: Script Structure

If no script provided, generate one. If script provided from `video-script`, validate against these structures:

### Reel/Short Script (15-90 seconds)
```
[0-3s] HOOK: [Attention-grabbing opening, visual or verbal]
[3-15s] PROBLEM: [State the pain point]
[15-40s] SOLUTION: [Show/explain the approach]
[40-60s] PROOF: [Result, stat, or demonstration]
[60-75s] CTA: [What to do next]
[75-90s] OUTRO: [Brand tag, follow prompt]
```

### YouTube Script (3-10 minutes)
```
[0-30s] HOOK: [Why should they keep watching?]
[30s-1m] INTRO: [Context, what they'll learn]
[1-7m] BODY: [3-5 key points, each with example]
[7-9m] SUMMARY: [Recap key takeaways]
[9-10m] CTA: [Subscribe, comment, link in description]
```

### Ad Script (15-60 seconds)
```
[0-3s] HOOK: [Stop the scroll]
[3-10s] PROBLEM: [Pain point, relatable scenario]
[10-20s] SOLUTION: [Introduce the offer]
[20-40s] PROOF: [Testimonial, stat, demo]
[40-50s] OFFER: [What they get, price/value]
[50-60s] CTA: [Clear action, urgency if applicable]
```

## Phase 3: Shot List

For each script segment, define shots:

```
SHOT LIST
---
Shot 1:
  Timestamp: [0:00 - 0:03]
  Script line: "[corresponding dialogue]"
  Shot type: [close-up / medium / wide / over-shoulder / screen-recording / B-roll]
  Subject: [who/what is in frame]
  Action: [what happens in this shot]
  Camera movement: [static / pan / tilt / tracking / zoom]
  Location: [office / desk / outdoors / screen / etc.]
  Props: [laptop, phone, product, whiteboard, etc.]
  Notes: [lighting, framing, mood]

Shot 2:
  ...
```

## Phase 4: B-Roll Suggestions

List B-roll footage needed to cover cuts, transitions, and visual variety:

```
B-ROLL LIST
---
1. [Description]: Hands typing on laptop with Shopify admin visible
   Duration: 3-5 seconds
   Use at: [timestamp range]
   Source: [shoot / stock footage / screen recording]

2. [Description]: Close-up of analytics dashboard showing growth
   Duration: 2-3 seconds
   Use at: [timestamp range]
   Source: [screen recording]

3. [Description]: Team working in office / co-working space
   Duration: 3-5 seconds
   Use at: [timestamp range]
   Source: [shoot / stock]
```

## Phase 5: Audio & Music

```
AUDIO SPECS
---
Music mood: [upbeat / inspiring / corporate-modern / lo-fi / cinematic]
Music tempo: [BPM range, e.g., 100-120 BPM]
Music suggestions: [genre, reference tracks if applicable]
Music source: [royalty-free library, e.g., Epidemic Sound, Artlist]
Voiceover: [yes/no, male/female, tone descriptor]
Sound effects: [whoosh transitions, notification sounds, keyboard clicks, etc.]
Audio levels:
  Dialogue: -6dB to -12dB
  Music (under dialogue): -18dB to -24dB
  Music (standalone): -6dB to -12dB
  SFX: -12dB to -18dB
```

## Phase 6: Thumbnail Concept

```
THUMBNAIL BRIEF
---
Concept: [1-2 sentence description]
Text overlay: "[3-5 word hook]"
Text style: [bold, high contrast, readable at 120x68px]
Face/subject: [expression, position]
Background: [color / blurred frame / graphic]
Branding: [small logo placement]
Dimensions: 1280x720 (YouTube) / 1080x1920 (Reel cover)
Click-worthiness check: Would this make YOU stop scrolling?
```

## Phase 7: Post-Production Notes

```
EDITING NOTES
---
Pacing: [fast cuts for reels, measured for YouTube, punchy for ads]
Transitions: [hard cuts / smooth / zoom / morph]
Text overlays: [key phrases, stats, captions]
Captions: Required (85% of social video watched without sound)
Caption style: [burned-in / platform auto / SRT file]
Color grading: [warm / cool / neutral / brand-matched]
Intro/outro: [branded template, duration]
End screen: [YouTube: subscribe + suggested video, 20 seconds]
Watermark: [agency logo, corner, subtle]
```

## Phase 8: Output

Return structured JSON:

```json
{
  "video_type": "reel",
  "platform": "instagram-reels",
  "duration_target": "60s",
  "aspect_ratio": "9:16",
  "resolution": "1080x1920",
  "script": {
    "hook": "Your Shopify store is losing 40% of mobile visitors at checkout",
    "sections": [
      {"timestamp": "0:00-0:03", "type": "hook", "dialogue": "...", "visual": "..."},
      {"timestamp": "0:03-0:15", "type": "problem", "dialogue": "...", "visual": "..."}
    ],
    "total_word_count": 145,
    "estimated_duration": "58s"
  },
  "shot_list": [
    {"shot": 1, "timestamp": "0:00-0:03", "type": "close-up", "subject": "founder face", "action": "..."}
  ],
  "b_roll": [
    {"description": "Shopify admin dashboard", "duration": "3s", "source": "screen-recording"}
  ],
  "audio": {
    "music_mood": "upbeat, modern",
    "voiceover": false,
    "captions_required": true
  },
  "thumbnail": {
    "concept": "Founder pointing at phone showing checkout page",
    "text_overlay": "Fix This NOW",
    "dimensions": "1080x1920"
  },
  "budget_level": "low",
  "equipment_needed": ["smartphone", "ring light", "lapel mic"],
  "estimated_shoot_time": "30 minutes",
  "estimated_edit_time": "2 hours",
  "generated_at": "2026-03-13T10:00:00Z"
}
```

## Example Usage

Trigger phrases:
- "Create a production brief for a reel about Shopify CRO tips"
- "Plan a YouTube video about our Kibi Sports case study"
- "Brief a 30-second ad for Plasho services"
- "Create a testimonial video plan for a client"
- "Plan a behind-the-scenes reel about our design process"
- "Generate a shot list for a product explainer video"
