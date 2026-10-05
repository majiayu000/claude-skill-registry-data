---
name: video-editor
description: Use when professional video post-production using FFmpeg — color grading,
  audio design, kinetic typography, transitions, motion effects, captions, brand overlays,
  and platform-optimized export for promotional and marketing videos. Use when editing
  videos, adding captions, color grading, or creating promo content.
domain: content
author: oyi77
license: Apache-2.0
subdomain: content-creation
tags:
- content-creation
- video-production
- ffmpeg
- post-production
- color-grading
- promotional-video
- captions
- audio-design
version: 1.0.0
category: content
---

# Video Editor — Professional Post-Production

Companion skills: [remotion](../remotion/SKILL.md) · [video-gen](../video-gen/SKILL.md) · [faceless-youtube](../faceless-youtube/SKILL.md)

## When to Use

**Trigger phrases:**
- "edit this video" · "add captions" · "color grade" · "make a promo video"
- "merge clips" · "add music" · "watermark" · "optimize for instagram"
- "speed ramp" · "slow motion" · "lower third" · "add transitions"

**Use cases:**
- Post-production editing of AI-generated or recorded footage
- Adding captions/subtitles with brand styling
- Color grading and visual correction
- Audio mixing, ducking, and loudness normalization
- Creating promotional videos from raw clips
- Platform-specific export (YouTube, TikTok, Instagram, LinkedIn)
- Batch processing multiple videos
- Thumbnail extraction and creation

**When NOT to use:**
- When creating video from scratch with React (use [remotion](../remotion/SKILL.md))
- When generating video from AI models (use [video-gen](../video-gen/SKILL.md))
- When the task requires real-time editing (use a NLE like DaVinci Resolve)

---

## Overview

FFmpeg is the industry-standard tool for video post-production. This skill covers professional-grade filter graphs for promotional videos: color grading, audio design, kinetic text, transitions, motion effects, and multi-platform export.

## Process

1. **Ingest** — Analyze source footage (duration, resolution, codec, audio levels)
2. **Assembly** — Trim, arrange, and concatenate clips
3. **Color grade** — Apply LUTs, curves, contrast, and color harmony
4. **Audio design** — Mix music, voiceover, SFX; apply ducking and normalization
5. **Add text** — Captions, lower thirds, title cards, CTAs
6. **Add brand** — Logo overlay, watermark, consistent color scheme
7. **Transitions** — Crossfade, wipe, or zoom between scenes
8. **Motion effects** — Speed ramps, slow-mo, Ken Burns, motion blur
9. **Export** — Master file + platform-specific optimized versions
10. **Thumbnail** — Extract best frame, add text overlay

---

## Promo Video Structure

Professional promotional videos follow a proven narrative arc:

```
┌─────────────────────────────────────────────────────────────────┐
│  HOOK (0-3s)          │ Grab attention immediately              │
│  Bold text / motion   │ "Stop scrolling" moment                 │
├───────────────────────┼─────────────────────────────────────────┤
│  PROBLEM (3-8s)       │ State the pain point                    │
│  Text + B-roll        │ "You're wasting hours on..."            │
├───────────────────────┼─────────────────────────────────────────┤
│  SOLUTION (8-20s)     │ Show your product/service               │
│  Screen recording /   │ "Here's how X fixes this"               │
│  product demo         │                                         │
├───────────────────────┼─────────────────────────────────────────┤
│  PROOF (20-30s)       │ Social proof, metrics, testimonials     │
│  Stats / quotes       │ "10K+ users" / "4.9★ rating"           │
├───────────────────────┼─────────────────────────────────────────┤
│  CTA (30-45s)         │ Clear call to action                    │
│  Bold text + logo     │ "Try free today" + URL                  │
└─────────────────────────────────────────────────────────────────┘
```

### Timing Guide

| Section | Duration | Frame Count (30fps) |
|---|---|---|
| Hook | 2-3s | 60-90 |
| Problem | 3-5s | 90-150 |
| Solution | 10-15s | 300-450 |
| Proof | 5-8s | 150-240 |
| CTA | 3-5s | 90-150 |
| **Total** | **25-40s** | **750-1200** |

---

## Professional FFmpeg Filter Graphs

### 1. Color Grading

#### Apply LUT (Look-Up Table)

```bash
# Apply a .cube LUT file for cinematic color grading
ffmpeg -i input.mp4 -vf "lut3d=file='cinematic.cube'" -c:a copy graded.mp4

# Apply LUT with reduced intensity (50% blend)
ffmpeg -i input.mp4 -vf "
  [0:v]split[orig][lut];
  [lut]lut3d=file='cinematic.cube'[graded];
  [orig][graded]blend=all_expr='A*(1-0.5)+B*0.5'
" -c:a copy graded-subtle.mp4
```

#### Manual Color Correction

```bash
# Lift shadows, boost highlights, add warmth
ffmpeg -i input.mp4 -vf "
  curves=lighter=0/0 0.25/0.22 0.5/0.52 0.75/0.78 1/1:
         green=0/0 0.5/0.48 1/1:
         blue=0/0 0.5/0.47 1/1,
  eq=brightness=0.03:contrast=1.1:saturation=1.15
" -c:a copy color-corrected.mp4
```

#### Cinematic Teal & Orange

```bash
ffmpeg -i input.mp4 -vf "
  curves=
    r='0/0.05 0.3/0.25 0.5/0.55 0.7/0.75 1/0.9':
    g='0/0.03 0.3/0.2 0.5/0.48 0.7/0.7 1/0.85':
    b='0/0.1 0.3/0.3 0.5/0.45 0.7/0.6 1/0.7',
  eq=saturation=1.3:contrast=1.15,
  unsharp=5:5:0.8
" -c:a copy teal-orange.mp4
```

#### High-Contrast Promo Look

```bash
ffmpeg -i input.mp4 -vf "
  eq=contrast=1.3:brightness=0.02:saturation=1.2,
  curves=master='0/0 0.15/0.05 0.5/0.55 0.85/0.95 1/1',
  unsharp=5:5:1.0
" -c:a copy high-contrast-promo.mp4
```

### 2. Audio Design

#### Background Music + Voiceover Mixing

```bash
# Mix voiceover (primary) with background music (ducked)
ffmpeg -i voiceover.mp4 -i music.mp3 -filter_complex "
  [0:a]volume=1.0[vo];
  [1:a]volume=0.15[music];
  [vo][music]amix=inputs=2:duration=shortest:dropout_transition=3
" -c:v copy -c:a aac -b:a 192k mixed.mp4
```

#### Audio Ducking (Auto-Lower Music During Speech)

```bash
# Sidechain compress: music ducks when voice is present
ffmpeg -i voiceover.mp4 -i music.mp3 -filter_complex "
  [1:a][0:a]sidechaincompress=threshold=0.02:ratio=10:attack=200:release=1000[ducked];
  [0:a]volume=1.0[vo];
  [vo][ducked]amix=inputs=2:duration=shortest
" -c:v copy -c:a aac ducked-mix.mp4
```

#### Loudness Normalization (EBU R128)

```bash
# Normalize to broadcast standard (-14 LUFS for streaming)
ffmpeg -i input.mp4 -af "loudnorm=I=-14:TP=-1.5:LRA=11" -c:v copy normalized.mp4

# Two-pass for accurate normalization
ffmpeg -i input.mp4 -af "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json" -f null - 2>&1 | tail -12
# Then apply measured values in second pass:
ffmpeg -i input.mp4 -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=-20:measured_TP=-3:measured_LRA=8" -c:v copy normalized.mp4
```

#### Fade In/Out

```bash
# Audio fade in (0.5s) and fade out (1s) at end
ffmpeg -i input.mp4 -af "afade=t=in:st=0:d=0.5,afade=t=out:st=29:d=1" -c:v copy audio-faded.mp4
```

### 3. Text & Captions

#### Animated Title Card

```bash
# Title that fades in, holds, fades out (frames 0-90 = 3s at 30fps)
ffmpeg -i input.mp4 -vf "
  drawtext=text='YOUR BRAND':
    fontfile=fonts/Bold.ttf:
    fontsize=120:
    fontcolor=white:
    borderw=3:
    bordercolor=black@0.3:
    x=(w-text_w)/2:
    y=(h-text_h)/2:
    enable='between(t,0,3)':
    alpha='if(lt(t,0.5),t*2,if(gt(t,2.5),(3-t)*2,1))'
" -c:a copy title-card.mp4
```

#### Lower Third (Name + Title)

```bash
# Animated lower third with background bar
ffmpeg -i input.mp4 -vf "
  drawbox=x=0:y=ih-160:w=iw:h=160:color=black@0.7:t=fill:
    enable='between(t,2,8)',
  drawtext=text='John Smith':
    fontfile=fonts/Bold.ttf:fontsize=48:fontcolor=white:
    x=60:y=ih-130:
    enable='between(t,2,8)':
    alpha='if(lt(t,2.5),(t-2)*2,if(gt(t,7.5),(8-t)*2,1))',
  drawtext=text='CEO, Company':
    fontfile=fonts/Regular.ttf:fontsize=32:fontcolor=white@0.8:
    x=60:y=ih-80:
    enable='between(t,2,8)':
    alpha='if(lt(t,2.5),(t-2)*2,if(gt(t,7.5),(8-t)*2,1))'
" -c:a copy lower-third.mp4
```

#### Styled Subtitles (Brand Colors)

```bash
# Burn subtitles with custom styling
ffmpeg -i input.mp4 -vf "
  subtitles=captions.srt:
    force_style='
      FontName=Inter,
      FontSize=28,
      PrimaryColour=&H00FFFFFF,
      OutlineColour=&H00000000,
      BackColour=&H80000000,
      Bold=1,
      Outline=2,
      Shadow=1,
      MarginV=60,
      Alignment=2
    '
" -c:a copy captioned.mp4
```

#### Word-by-Word Highlight Captions (ASS Format)

```bash
# Generate ASS file with word-by-word highlighting
cat > captions.ass << 'EOF'
[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Inter,48,&H00FFFFFF,&H0000FFFF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,3,1,2,40,40,60,1
Style: Highlight,Inter,48,&H0000FFFF,&H0000FFFF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,3,1,2,40,40,60,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:01.00,0:00:03.00,Default,,0,0,0,,{\k50}This {\k30}is {\k40}your {\k50}brand
EOF

ffmpeg -i input.mp4 -vf "ass=captions.ass" -c:a copy word-highlight.mp4
```

### 4. Transitions

#### Crossfade Between Clips

```bash
# 1-second crossfade between two clips
ffmpeg -i clip1.mp4 -i clip2.mp4 -filter_complex "
  [0:v]fade=t=out:st=4:d=1[v0];
  [1:v]fade=t=in:st=0:d=1[v1];
  [v0][v1]concat=n=2:v=1:a=0[outv];
  [0:a]afade=t=out:st=4:d=1[a0];
  [1:a]afade=t=in:st=0:d=1[a1];
  [a0][a1]concat=n=2:v=0:a=1[outa]
" -map "[outv]" -map "[outa]" crossfade.mp4
```

#### Wipe Transition

```bash
# Horizontal wipe (left to right) between clips
ffmpeg -i clip1.mp4 -i clip2.mp4 -filter_complex "
  [0:v][1:v]xfade=transition=wipeleft:duration=1:offset=4
" -c:a copy wipe-transition.mp4
```

#### Available xfade Transitions

| Transition | Name | Effect |
|---|---|---|
| `fade` | `fade` | Crossfade |
| `wipeleft` | `wipeleft` | Horizontal wipe L→R |
| `wiperight` | `wiperight` | Horizontal wipe R→L |
| `wipeup` | `wipeup` | Vertical wipe bottom→top |
| `wipedown` | `wipedown` | Vertical wipe top→bottom |
| `slideleft` | `slideleft` | Slide L→R |
| `slideright` | `slideright` | Slide R→L |
| `circleopen` | `circleopen` | Circle open reveal |
| `circleclose` | `circleclose` | Circle close |
| `dissolve` | `dissolve` | Dissolve |
| `pixelize` | `pixelize` | Pixelize transition |
| `diagtl` | `diagtl` | Diagonal from top-left |

### 5. Motion Effects

#### Speed Ramp (Slow-Mo → Normal)

```bash
# Slow-mo section (2x slower from 5s to 8s), normal elsewhere
ffmpeg -i input.mp4 -filter_complex "
  [0:v]setpts='if(between(T,5,8),PTS*2,PTS)'[v];
  [0:a]atempo='if(between(T,5,8),0.5,1.0)'[a]
" -map "[v]" -map "[a]" speed-ramp.mp4
```

#### Ken Burns (Slow Zoom on Still Image)

```bash
# 10-second Ken Burns zoom-in on a product image
ffmpeg -loop 1 -i product.jpg -t 10 -vf "
  zoompan=z='min(zoom+0.001,1.5)':
    x='iw/2-(iw/zoom/2)':
    y='ih/2-(ih/zoom/2)':
    d=300:
    s=1920x1080:fps=30
" -c:v libx264 -pix_fmt yuv420p ken-burns.mp4
```

#### Motion Blur (For Fast Movements)

```bash
ffmpeg -i input.mp4 -vf "
  tmix=frames=4:weights='1 1 1 1'
" -c:a copy motion-blur.mp4
```

### 6. Brand Elements

#### Logo Overlay (Corner)

```bash
# Logo in bottom-right corner, 10% opacity watermarked
ffmpeg -i input.mp4 -i logo.png -filter_complex "
  [1:v]scale=150:-1,format=rgba,colorchannelmixer=aa=0.3[logo];
  [0:v][logo]overlay=W-w-30:H-h-30
" -c:a copy watermarked.mp4
```

#### Animated Logo Intro (Logo + Fade)

```bash
# Logo appears centered, fades in over 0.5s, holds 2s, fades out
ffmpeg -i input.mp4 -i logo.png -filter_complex "
  [1:v]scale=300:-1,format=rgba[logo];
  [0:v][logo]overlay=(W-w)/2:(H-h)/2:
    enable='between(t,0,3)':
    format=auto
" -c:a copy logo-intro.mp4
```

### 7. Multi-Clip Assembly

#### Full Promo Assembly Pipeline

```bash
# Step 1: Prepare individual clips (trim, color grade, normalize audio)
ffmpeg -i raw_hook.mp4 -t 3 -vf "eq=contrast=1.2:saturation=1.1" -af "loudnorm=I=-14" -c:v libx264 -crf 18 hook.mp4
ffmpeg -i raw_problem.mp4 -ss 2 -t 5 -vf "eq=contrast=1.2:saturation=1.1" -af "loudnorm=I=-14" -c:v libx264 -crf 18 problem.mp4
ffmpeg -i raw_solution.mp4 -ss 0 -t 12 -vf "eq=contrast=1.2:saturation=1.1" -af "loudnorm=I=-14" -c:v libx264 -crf 18 solution.mp4
ffmpeg -i raw_proof.mp4 -ss 5 -t 8 -vf "eq=contrast=1.2:saturation=1.1" -af "loudnorm=I=-14" -c:v libx264 -crf 18 proof.mp4
ffmpeg -i raw_cta.mp4 -t 4 -vf "eq=contrast=1.2:saturation=1.1" -af "loudnorm=I=-14" -c:v libx264 -crf 18 cta.mp4

# Step 2: Create concat list with crossfades
cat > clips.txt << EOF
file 'hook.mp4'
file 'problem.mp4'
file 'solution.mp4'
file 'proof.mp4'
file 'cta.mp4'
EOF

# Step 3: Concatenate with xfade transitions
ffmpeg -i hook.mp4 -i problem.mp4 -i solution.mp4 -i proof.mp4 -i cta.mp4 -filter_complex "
  [0:v][1:v]xfade=transition=fade:duration=0.5:offset=2.5[v01];
  [v01][2:v]xfade=transition=wipeleft:duration=0.5:offset=7[v012];
  [v012][3:v]xfade=transition=fade:duration=0.5:offset=18.5[v0123];
  [v0123][4:v]xfade=transition=fade:duration=0.5:offset=26[vout];
  [0:a][1:a]acrossfade=d=0.5[a01];
  [a01][2:a]acrossfade=d=0.5[a012];
  [a012][3:a]acrossfade=d=0.5[a0123];
  [a0123][4:a]acrossfade=d=0.5[aout]
" -map "[vout]" -map "[aout]" -c:v libx264 -crf 18 -c:a aac -b:a 192k promo-assembled.mp4

# Step 4: Add music bed with ducking
ffmpeg -i promo-assembled.mp4 -i bg-music.mp3 -filter_complex "
  [0:a]volume=1.0[vo];
  [1:a]volume=0.12,afade=t=out:st=30:d=3[music];
  [music][vo]sidechaincompress=threshold=0.02:ratio=12:attack=150:release=800[ducked];
  [vo][ducked]amix=inputs=2:duration=shortest:dropout_transition=2,
  loudnorm=I=-14:TP=-1.5:LRA=11
" -c:v copy -c:a aac -b:a 192k promo-with-music.mp4

# Step 5: Add logo watermark
ffmpeg -i promo-with-music.mp4 -i logo.png -filter_complex "
  [1:v]scale=120:-1,format=rgba,colorchannelmixer=aa=0.25[logo];
  [0:v][logo]overlay=W-w-25:H-h-25
" -c:a copy promo-final-master.mp4
```

---

## Batch Processing

### Export for All Platforms

```bash
#!/bin/bash
# export-all.sh — Export master video for all platforms
MASTER="promo-final-master.mp4"
OUTDIR="exports"
mkdir -p "$OUTDIR"

# YouTube (16:9, 1080p)
ffmpeg -i "$MASTER" -vf "scale=1920:1080" -c:v libx264 -preset slow -crf 18 -c:a aac -b:a 192k "$OUTDIR/youtube.mp4"

# Instagram Reels (9:16, 1080x1920)
ffmpeg -i "$MASTER" -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:white" -c:v libx264 -preset slow -crf 22 -c:a aac -b:a 128k -t 90 "$OUTDIR/instagram-reels.mp4"

# TikTok (9:16, 1080x1920)
ffmpeg -i "$MASTER" -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:v libx264 -preset slow -crf 22 -c:a aac -b:a 128k -t 600 "$OUTDIR/tiktok.mp4"

# Instagram Feed (1:1, 1080x1080)
ffmpeg -i "$MASTER" -vf "scale=1080:1080:force_original_aspect_ratio=decrease,pad=1080:1080:(ow-iw)/2:(oh-ih)/2:white" -c:v libx264 -preset slow -crf 22 -c:a aac -b:a 128k -t 60 "$OUTDIR/instagram-feed.mp4"

# LinkedIn (16:9, 1080p)
ffmpeg -i "$MASTER" -vf "scale=1920:1080" -c:v libx264 -preset slow -crf 20 -c:a aac -b:a 192k -t 600 "$OUTDIR/linkedin.mp4"

# X / Twitter (16:9, 720p)
ffmpeg -i "$MASTER" -vf "scale=1280:720" -c:v libx264 -preset slow -crf 22 -c:a aac -b:a 128k -t 140 "$OUTDIR/twitter.mp4"

# Thumbnail
ffmpeg -i "$MASTER" -ss 00:00:03 -vframes 1 -q:v 2 "$OUTDIR/thumbnail.jpg"

echo "✅ Exported to $OUTDIR/"
ls -lh "$OUTDIR/"
```

### Platform Specifications

| Platform | Resolution | Aspect | Max Length | Codec | CRF | Audio |
|---|---|---|---|---|---|---|
| YouTube | 1920×1080 | 16:9 | Unlimited | H.264 | 18 | AAC 192k |
| Instagram Reels | 1080×1920 | 9:16 | 90s | H.264 | 22 | AAC 128k |
| Instagram Feed | 1080×1080 | 1:1 | 60s | H.264 | 22 | AAC 128k |
| TikTok | 1080×1920 | 9:16 | 10min | H.264 | 22 | AAC 128k |
| LinkedIn | 1920×1080 | 16:9 | 10min | H.264 | 20 | AAC 192k |
| X / Twitter | 1280×720 | 16:9 | 2:20 | H.264 | 22 | AAC 128k |
| Facebook | 1280×720 | 16:9 | 240min | H.264 | 22 | AAC 128k |

---

## Color Grading Presets

### Cinematic (Teal & Orange)

```bash
-vf "curves=r='0/0.05 0.3/0.25 0.5/0.55 0.7/0.75 1/0.9':g='0/0.03 0.3/0.2 0.5/0.48 0.7/0.7 1/0.85':b='0/0.1 0.3/0.3 0.5/0.45 0.7/0.6 1/0.7',eq=saturation=1.3:contrast=1.15"
```

### Clean Corporate (Bright, High Contrast)

```bash
-vf "eq=brightness=0.03:contrast=1.2:saturation=1.1,curves=master='0/0 0.15/0.08 0.5/0.55 0.85/0.95 1/1'"
```

### Moody Dark (Low Key)

```bash
-vf "eq=brightness=-0.05:contrast=1.3:saturation=0.9,curves=master='0/0 0.2/0.1 0.5/0.4 0.8/0.75 1/0.9'"
```

### Vibrant Social Media (Punchy Colors)

```bash
-vf "eq=brightness=0.02:contrast=1.25:saturation=1.4,unsharp=5:5:0.8"
```

### Desaturated Premium (Muted, Elegant)

```bash
-vf "eq=saturation=0.7:contrast=1.15,curves=master='0/0.02 0.3/0.28 0.5/0.52 0.7/0.73 1/0.95'"
```

---

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Just concat the clips" | Raw concatenation has jarring cuts. Use xfade transitions for professional flow. |
| "Skip color grading" | Ungraded footage looks amateur. Even subtle correction (contrast +5%, saturation +10%) transforms quality. |
| "Audio doesn't matter" | Audio is 50% of perceived quality. Normalize loudness, mix music properly, add SFX. |
| "Burn-in captions are fine" | Unstyled captions look auto-generated. Use brand colors, proper fonts, and word-by-word highlighting. |
| "One export for all platforms" | Each platform has different specs. A 16:9 video letterboxed on 9:16 looks terrible. Export per platform. |
| "Skip the thumbnail" | Thumbnail is the #1 click driver. Extract the best frame, add bold text overlay. |
| "CRF 23 is good enough" | For promotional content, use CRF 18. Quality is visible, especially on large screens. |
| "Audio ducking is optional" | Without ducking, music drowns voiceover. Professional promos always duck music during speech. |

## Verification

- [ ] Audio normalized to -14 LUFS (streaming standard)
- [ ] Music ducked during voiceover/speech
- [ ] Color grading applied consistently across all clips
- [ ] Transitions between scenes are smooth (xfade, not hard cuts)
- [ ] Captions styled with brand colors and fonts
- [ ] Logo/watermark placed consistently
- [ ] CTA is bold, readable, and appears long enough to read
- [ ] Exported for each target platform with correct specs
- [ ] Thumbnail extracted and styled
- [ ] Final video watched from start to finish before delivery
