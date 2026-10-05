---
name: audio-processing
description: Use when processing audio for Xiaohongshu content, editing voiceovers, improving sound quality, creating podcasts, or producing audio-based posts
---

# Audio Processing (音频处理)

## Overview

Audio processing encompasses recording, editing, enhancing, and optimizing audio content for Xiaohongshu posts, ensuring professional sound quality that significantly enhances content professionalism, viewer retention, and overall production value. Poor audio is the #1 reason viewers abandon content within seconds - even with stunning visuals, bad audio makes content unwatchable. This skill covers the complete audio production workflow: from recording setup through editing, noise reduction, mixing, and final optimization for Xiaohongshu's platform specifications.

**Key insight**: Viewers will forgive mediocre video quality, but they will not tolerate poor audio. Investing in audio processing yields 50%+ improvements in viewer retention and 3-5x increases in engagement rates. Professional audio transforms amateur content into credible, trustworthy content.

## When to Use

**Use when**:
- Recording voiceovers for Xiaohongshu videos, tutorials, or storytelling content
- Editing podcast-style audio content or interview recordings
- Improving audio quality in existing recordings (noise reduction, volume leveling)
- Creating background music tracks or adding sound effects to videos
- Producing audio-first content formats (podcasts, audio diaries, voice notes)
- Fixing common audio issues: background noise, echo, distortion, low volume
- Optimizing audio for Xiaohongshu's platform specifications and compression
- Creating consistent audio quality across content series
- Adding professional polish with music beds, transitions, and sound design

**Do NOT use when**:
- Using licensed music without proper permissions (copyright violation)
- Content requires pure ambient sound (over-processing disrupts authenticity)
- Audio is already professional quality (over-processing can degrade quality)
- Quick, casual content where production speed matters more than polish
- Live streaming (different audio setup requirements)

## Core Pattern

**Before** (poor audio quality):
❌ "Background noise, room echo, distractions"
❌ "Inconsistent volume, too quiet then too loud"
❌ "Viewer adjusts volume constantly, gives up"
❌ "Content seems amateur, low credibility"
❌ "Viewers scroll away within 3 seconds"

**After** (professional audio):
✅ "Clean, clear voice recording"
✅ "Consistent volume levels throughout"
✅ "Pleasant listening experience, no adjustments needed"
✅ "Content feels professional, trustworthy"
✅ "Viewers watch complete content, high engagement"

**6 Essential Audio Processing Elements**:

| Element | Purpose | Quality Impact | Priority |
|---------|---------|----------------|----------|
| **Clean Recording** | Prevent issues at source | Critical | #1 - cannot fix in post |
| **Noise Reduction** | Remove background distractions | High | #2 - most common issue |
| **Volume Normalization** | Consistent listening levels | High | #3 - prevents frustration |
| **EQ & Clarity** | Enhance voice intelligibility | Medium-High | #4 - professional polish |
| **Music & Effects** | Add emotional depth | Medium | #5 - enhance, don't distract |
| **Platform Optimization** | Meet technical specs | Medium | #6 - avoid compression artifacts |

## Quick Reference

**Audio Processing Software Comparison**:

| Tool | Best For | Skill Level | Cost | Platform | Key Features |
|------|----------|------------|------|----------|--------------|
| **Audacity** | Basic editing, noise reduction | Beginner | Free | Win/Mac/Linux | Noise gate, normalize, EQ |
| **Adobe Audition** | Professional production | Intermediate-Advanced | Paid (Subscription) | Win/Mac | Multitrack, advanced repair, batch processing |
| **GarageBand** | Mac users, simple editing | Beginner | Free (Mac) | macOS | Built-in effects, music loops, easy interface |
| **Descript** | Text-based editing, podcasts | Beginner-Intermediate | Paid (Freemium) | Web/Mac/Win | Edit audio like text, overdub, filler removal |
| **Logic Pro** | Music production, advanced editing | Advanced | Paid (One-time) | macOS | Professional DAW, massive library |
| **Reaper** | Power users, customization | Advanced | Paid (Free trial) | Win/Mac/Linux | Lightweight, extensible, affordable |

**Xiaohongshu Audio Specifications**:
- **Format**: AAC, MP3, or M4A
- **Sample Rate**: 44.1kHz or 48kHz
- **Bitrate**: 128-320 kbps (192 kbps recommended for balance)
- **Channels**: Stereo or Mono (Mono for voice-only is fine)
- **Loudness Target**: -16 LUFS (YouTube/Broadcast standard)

**Quick Audio Fixes** (by symptom):

| Symptom | Likely Cause | Quick Fix |
|---------|--------------|-----------|
| **Background hiss/hum** | Room noise, equipment hiss | Noise reduction filter |
| **Room echo/reverb** | Recording in untreated room | Move closer to mic, use de-reverb plugin |
| **Volume too low** | Recording level too low | Gain/normalize to -3dB peak |
| **Distorted/clipping** | Recording level too high | Reduce gain, use clip restoration |
| **Muffled sound** | Poor mic quality or wrong EQ | High-pass filter + EQ boost |
| **Inconsistent levels** | Multiple clips or variable distance | Compression + normalization |

## Implementation

### Step 1: Recording Setup and Environment

**Prevention is better than correction** - capturing clean audio at source saves hours of editing and yields better results than any post-processing.

**Microphone Selection**:

| Mic Type | Best For | Pros | Cons | Price Range |
|----------|----------|------|------|-------------|
| **USB Mic** | Beginners, simplicity | Plug-and-play, easy | Limited quality, no upgrades | ¥200-800 |
| **Dynamic XLR** | Voice recording, noisy rooms | Rejects room noise, durable | Quiet, need preamp | ¥500-2000 |
| **Condenser XLR** | Studio recording, vocals | Detailed, professional | Sensitive to room noise | ¥800-5000 |
| **Lavalier (Lapel)** | Video, talking head | Hands-free, close to mouth | Visible in shot, can rub on clothes | ¥100-500 |
| **Shotgun** | Interviews, outdoor | Directional, outdoor use | Expensive, need operator | ¥1000-8000 |

**Environment Setup**:
- **Quietest room available**: Close windows, turn off fans/AC, avoid high-traffic times
- **Reduce reflections**: Hang blankets, use acoustic foam, record in closet full of clothes
- **Distance to mic**: 6-12 inches (15-30cm) for optimal balance of proximity effect and room noise
- **Pop filter**: Essential for plosive sounds (P, B sounds) - cheap foam or metal mesh
- **Shock mount**: Isolates mic from desk vibrations and handling noise

**Recording Levels**:
- **Target**: -12dB to -6dB average, peaks around -3dB
- **Too low**: -24dB or below → brings up noise floor when boosted later
- **Too hot**: Peaking at 0dB → distortion/clipping, cannot be fixed
- **Test record**: Always do 10-second test, check levels before full recording

**Recording Checklist**:
- [ ] Room is quiet (no traffic, appliances, people)
- [ ] Mic positioned 6-12 inches from mouth
- [ ] Pop filter attached
- [ ] Recording level peaks around -6dB
- [ ] Headphones monitoring live audio
- [ ] Test recording sounds clear, no issues

### Step 2: Basic Audio Editing

**Importing and Organizing**:
- **Multi-track setup**: Keep voice on track 1, music on track 2, effects on track 3
- **Label tracks**: "Voiceover", "Background Music", "Sound Effects" for clarity
- **Save project file**: Always save editable project format (.aup3, .sesx, etc.) before exporting

**Trimming and Arranging**:
- **Remove mistakes**: Cut out coughs, false starts, long pauses
- **Tighten pacing**: Reduce pauses between sections to 0.5-1 second for better flow
- **Crossfade edits**: Use 5-10ms crossfades on all cuts to avoid clicks/pops
- **Arrange content**: Drag clips to reorder, build narrative flow

**Basic Editing Techniques**:

| Technique | How | Why |
|-----------|-----|-----|
| **Cut/Copy/Paste** | Select region, edit menu | Remove mistakes, reorder content |
| **Split** | Cut at cursor point | Separate sections for independent editing |
| **Trim** | Remove selected region | Quickly cut ends or mistakes |
| **Fade In/Out** | Apply fade to clip start/end | Smooth transitions, avoid abrupt starts/ends |
| **Crossfade** | Overlap clips with transition | Seamless joins between audio segments |

**Edit Best Practices**:
- **Always backup original**: Keep raw recording untouched, work on copy
- **Non-destructive editing**: Use software that preserves original (Audacity, Adobe Audition)
- **Undo is your friend**: Ctrl+Z / Cmd+Z liberally while learning
- **Save versions**: Save project after major edits (v1, v2, v3) so you can backtrack

### Step 3: Noise Reduction and Cleanup

**Identify Noise Types**:

| Noise | Character | Removal Method | Difficulty |
|-------|-----------|----------------|------------|
| **Hiss** | Steady high-frequency noise | Noise reduction plugin | Easy |
| **Hum** | Low-frequency electrical buzz (50/60Hz) | High-pass filter or notch filter | Easy |
| **Room reverb** | Echoey, cavernous sound | De-reverb plugin or reduce room noise | Medium |
| **Clicks/pops** | Sharp sudden sounds | Click removal plugin | Medium |
| **Wind noise** | Low-frequency rumble | High-pass filter + wind reduction | Medium-Hard |
| **Static/crackle** | Continuous crackling | Noise reduction + de-crackle | Hard |

**Noise Reduction Workflow** (using Audacity as example):

**Step 1: Capture Noise Profile**
1. Find a section of pure noise (no voice) - usually 0.5-2 seconds at start/end
2. Select only the noise section
3. Effect → Noise Reduction → Get Noise Profile
4. Software analyzes the noise character

**Step 2: Apply Noise Reduction**
1. Select entire audio track (Ctrl+A / Cmd+A)
2. Effect → Noise Reduction
3. Adjust settings:
   - **Noise reduction (dB)**: Start with 12dB, adjust to taste
   - **Sensitivity**: 3-6 (higher = more aggressive, may artifact)
   - **Frequency smoothing**: 3-6 bands
4. Preview, adjust, then apply

**Step 3: Fine-Tune**
- **Too aggressive**: Audio sounds underwater, robotic
- **Too light**: Still hear noise
- **Artifact check**: Listen for "watery" artifacts on "S" and "F" sounds
- **Apply multiple light passes** better than one heavy pass

**Alternative Noise Reduction Methods**:
- **High-pass filter**: Removes low-frequency rumble below 80-100Hz
- **Low-pass filter**: Removes high-frequency hiss above 12-15kHz
- **Notch filter**: Removes specific frequency (like 60Hz electrical hum)
- **Gate**: Silences audio below threshold (good for background noise between words)

### Step 4: Volume Normalization and Compression

**Consistent volume is critical** - viewers should never have to adjust their volume.

**Leveling Techniques** (in order of application):

**1. Normalization** (simple, fixes overall level):
- **Purpose**: Bring entire track to target peak level
- **Settings**: Normalize to -3dB peak (leaves headroom, prevents clipping)
- **When**: First step after noise reduction
- **How**: Select all, Effect → Normalize → Target peak level

**2. Compression** (evens out dynamics):
- **Purpose**: Reduce difference between loudest and softest parts
- **Key settings**:
  - **Ratio**: 2:1 to 4:1 for voice (2:1 = subtle, 4:1 = more aggressive)
  - **Threshold**: -20dB to -12dB (lower = more compression)
  - **Attack**: 5-10ms (fast enough to catch peaks)
  - **Release**: 100-300ms (natural release)
- **Result**: Whisper-quiet parts become audible, loud parts tamed

**3. Limiting** (prevents clipping):
- **Purpose**: Hard ceiling at -0.1dB or -1dB, ensures no digital distortion
- **Settings**: Threshold -1dB, ceiling -0.1dB
- **When**: Final step before export
- **Result**: No peaks exceed target, consistent loudness

**Compression Quick Settings by Use Case**:

| Use Case | Ratio | Threshold | Attack | Release |
|----------|-------|-----------|--------|---------|
| **Spoken word (tutorial)** | 2:1 | -18dB | 10ms | 200ms |
| **Narration (documentary)** | 3:1 | -15dB | 5ms | 150ms |
| **Podcast (conversation)** | 2.5:1 | -16dB | 8ms | 250ms |
| **Emotional/intimate** | 1.5:1 | -20dB | 15ms | 300ms |
| **Energetic/promo** | 4:1 | -12dB | 3ms | 100ms |

### Step 5: EQ and Audio Enhancement

**Equalization (EQ) shapes tone** - making voice sound clear, professional, and pleasant.

**Voice EQ Basics**:

| Frequency | Effect on Voice | When to Adjust |
|-----------|----------------|----------------|
| **Below 80Hz** | Low rumble, room noise | **Cut** completely for voice (high-pass filter) |
| **80-200Hz** | Warmth, body | Boost slightly for thin voices, cut for muddy |
| **200-500Hz** | Fullness, presence | Leave mostly flat |
| **500Hz-2kHz** | Intelligibility, clarity | Boost slightly (+1-3dB) if voice is dull |
| **2kHz-6kHz** | Definition, clarity | Boost (+2-4dB) to make voice "pop" |
| **6kHz-12kHz** | Air, brilliance, sibilance | Cut S-heavy voices at 7kHz, boost for "air" |
| **Above 12kHz** | Ultra-highs, hiss | Cut if hissy, leave if clear |

**Simple Voice EQ Recipe** (works for 80% of recordings):
1. **High-pass filter**: Remove everything below 80Hz
2. **Cut mud**: -2dB at 250Hz if voice sounds boomy
3. **Boost clarity**: +2dB at 3kHz for intelligibility
4. **Tame harshness**: -3dB at 7kHz if S-sounds are harsh
5. **Add air**: +2dB at 10kHz if voice needs openness

**De-Essing** (taming harsh S and T sounds):
- **Problem**: Sibilance causes harsh, ear-piercing S sounds
- **Solution**: De-esser plugin targets 5-8kHz frequencies only
- **Settings**: Threshold -20dB, frequency 7kHz, range -6dB
- **Alternative**: Manual EQ cut at 7kHz by -2 to -4dB

### Step 6: Adding Music and Sound Effects

**Music enhances emotion** but should never compete with voice.

**Music Selection Principles**:
- **Match mood**: Upbeat music for energetic content, calm for tutorials
- **Instrumental preferred**: Lyrics distract from spoken content
- **Right tempo**: 60-90 BPM for narration, 120+ for energetic
- **Legal sources**: Royalty-free from YouTube Audio Library, Epidemic Sound, Artlist

**Leveling Voice vs. Music**:

| Content Type | Voice Level | Music Level | Ratio |
|--------------|-------------|-------------|-------|
| **Tutorial/education** | -6dB to -3dB | -20dB to -18dB | 12-15dB difference |
| **Narration/story** | -6dB to -3dB | -16dB to -14dB | 10-12dB difference |
| **Emotional/intimate** | -8dB to -6dB | -22dB to -20dB | 14-16dB difference |
| **High-energy promo** | -3dB to 0dB | -12dB to -10dB | 10-12dB difference |

**Music Mixing Workflow**:
1. **Import music** to separate track (never mix with voice on same track)
2. **Fade music in**: 2-3 second fade at beginning
3. **Duck music**: Lower music volume by 4-6dB when voice is present
4. **Auto-duck** (if available): Software automatically lowers music during voice
5. **Fade music out**: 2-3 second fade at end
6. **Check on phone**: Test on mobile device (most viewers use mobile)

**Sound Effects (SFX)**:
- **Transition sounds**: Whooshes, clicks, swipes between sections
- **Emphasis**: Ding, pop, or sparkle for key points
- **Ambience**: Subtle room tone, nature sounds for atmosphere
- **Rule**: Less is more - 1-3 sounds per minute max

### Step 7: Export and Platform Optimization

**Export Settings for Xiaohongshu**:

| Setting | Recommended | Why |
|---------|-------------|-----|
| **Format** | AAC (.m4a) or MP3 | Best compression quality |
| **Sample Rate** | 44.1kHz or 48kHz | Match source rate |
| **Bitrate** | 192 kbps (stereo) or 128 kbps (mono) | Balance quality and file size |
| **Channels** | Stereo or Mono | Mono fine for voice-only |
| **Loudness** | -16 LUFS | Streaming platform standard |

**Export Quality Comparison**:

| Bitrate | File Size (1 min) | Quality | Use Case |
|---------|-------------------|---------|----------|
| **128 kbps** | ~1 MB | Good | Voice-only,节省流量 |
| **192 kbps** | ~1.5 MB | Very Good | **Recommended** for most content |
| **256 kbps** | ~2 MB | Excellent | Music-heavy or audiophile content |
| **320 kbps** | ~2.5 MB | Best | Overkill for social media |

**Final Checklist Before Export**:
- [ ] Noise reduction applied, no hiss or hum
- [ ] Volume normalized, consistent levels throughout
- [ ] Voice EQ applied, clear and pleasant
- [ ] Music balanced, doesn't compete with voice
- [ ] No clipping or distortion
- [ ] Fades at beginning and end
- [ ] Test listen on headphones, speakers, and phone
- [ ] Export at correct bitrate and format

**Quality Control Testing**:
1. **Headphones**: Check for details, hiss, harshness
2. **Speakers**: Check overall balance, bass response
3. **Phone speakers**: Most viewers listen here - critical test
4. **Car test**: Play in car (noisy environment) - intelligible?

## Common Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|----------------|-----|
| **Recording in noisy room** | Noise reduction can't fix everything, artifacts result | Record in quietest space, treat room with blankets |
| **Mic too far from mouth** | Room echo increases, voice-to-noise ratio decreases | Move 6-12 inches from mic, use pop filter |
| **Recording level too low** | Boosting in post amplifies noise floor | Aim for -12dB to -6dB average |
| **Recording level too hot** | Distortion/clipping is permanent and unfixable | Leave headroom, peak around -6dB |
| **Over-applying noise reduction** | Audio sounds robotic, underwater artifacts | Use light passes (6-12dB), not heavy (20dB+) |
| **No compression on voice** | Inconsistent volume, whisper-quiet then too-loud | Apply 2:1 to 4:1 compression |
| **Music too loud** | Distracts from voice, makes content hard to follow | Duck music 12-15dB below voice |
| **Too much high-frequency EQ** | Harsh, ear-fatiguing, sibilance amplified | Cut 7kHz region, boost 3kHz instead |
| **Exporting at wrong bitrate** | Either poor quality (too low) or huge files (too high) | Use 192 kbps for optimal balance |
| **Never testing on phone** | Sounds different on viewers' most common device | Always final QC on mobile device |

## Real-World Impact

**Case Study 1: Tutorial Creator's Retention Transformation**

**Creator**: Xiaohongshu tech tutorial creator
**Problem**: 40% viewer drop-off within 30 seconds, despite valuable content
**Issue**: Poor audio quality - room echo, inconsistent volume, background noise
**Solution Implemented**:
- Purchased USB microphone (¥300) and pop filter
- Treated recording space with blankets on walls
- Applied noise reduction, compression, and EQ in Audacity
- Normalized all content to -16 LUFS

**Results** (60 days):
- Average view duration: 45 seconds → 2:45 minutes (6x retention)
- 30-second drop-off: 40% → 15% (62.5% improvement)
- Engagement rate: 2% → 7% (3.5x increase)
- Comment feedback: "Finally can hear clearly!" "Audio quality is pro"

**Case Study 2: Podcaster's Audio Upgrade**

**Creator**: Storytelling podcast on Xiaohongshu
**Problem**: Listeners complained about "can't hear in car," "too quiet then too loud"
**Solution**:
- Implemented compression (3:1 ratio, -15dB threshold)
- Added limiter to prevent peaks
- Normalized to -16 LUFS loudness target
- Applied high-pass filter below 80Hz
- Subtle voice EQ boost at 3kHz

**Results**:
- Listener complaints: 0 (down from multiple per episode)
- Apple Podcasts rating: 4.2 → 4.8 stars
- Average completion rate: 45% → 72% (listeners finish episodes)
- Subscription growth: +200% (word-of-mouth from quality improvement)

**Case Study 3: Brand's Audio Consistency**

**Brand**: Beauty brand with multiple content creators
**Problem**: Inconsistent audio quality across 20+ creators, damaged brand credibility
**Solution**:
- Created audio processing template (preset in Adobe Audition)
- Standardized recording guidelines document
- Provided creators with cheap USB mic + pop filter kit
- Centralized post-processing: all audio edited by one person using template

**Results** (3 months):
- Audio consistency: 100% across all content
- Viewer retention: +35% (measured by average watch time)
- Brand perception: "Professional, trustworthy" in user surveys
- Reduced editing time: 4 hours per video → 45 minutes (template efficiency)

---

## Related Skills

**REQUIRED**:
- **short-video-production**: Complete video creation including audio integration
- **vlog-creation**: Vlog-specific audio challenges and solutions
- **podcast-production**: Long-form audio content creation techniques

**RECOMMENDED**:
- **music-licensing**: Legal music sourcing and copyright compliance
- **content-equipment**: Microphone and recording gear selection guides
- **post-production**: Comprehensive video/audio post-production workflow
- **accessibility**: Adding subtitles and transcripts for accessibility

**NEXT STEPS**:
1. Audit your current audio: What are your top 3 audio quality issues?
2. Upgrade recording setup: Start with mic + pop filter + quiet room
3. Learn basic editing: Download Audacity (free) and practice on test recordings
4. Create processing preset: Save your EQ, compression, and normalization settings
5. Test on mobile: Always final quality check on phone before publishing

---

**Professional audio is not about expensive gear - it's about clean recording and thoughtful processing. A ¥300 microphone with good technique beats a ¥5000 mic used poorly. Your viewers will forgive imperfect visuals, but they will abandon content with painful audio. Invest in audio processing first, visuals second.**
