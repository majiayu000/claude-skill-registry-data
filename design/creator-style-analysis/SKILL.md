---
name: creator-style-analysis
description: Systematically analyze any YouTube creator's visual and content style, extract parameters, and replicate them in your own videos using Remotion and FFmpeg.
purpose: Learn from proven patterns to position Chris as an AI authority by understanding what makes successful creators' content resonate with their audiences.
---

# Creator Style Analysis

## When to use this skill

- User wants to analyze a creator's visual style (typography, colors, motion, rotation)
- User asks "how does [creator] edit their videos?"
- User wants to replicate a specific creator's aesthetic
- User needs to understand content patterns (hooks, retention, pacing)
- User is designing graphics/overlays and needs proven parameters
- User wants to understand WHY certain visual choices work psychologically

## Prerequisites

- 3-5 sample videos from target creator (for pattern analysis)
- Whisper installed (`pip install faster-whisper`) for transcription
- FFmpeg for technical analysis (cuts per minute, color grading)
- Remotion project for implementation (`remotion-editor/`)
- Basic understanding of psychology behind design choices

## Workflow

- [ ] Watch 3-5 videos from target creator
- [ ] Extract visual parameters (rotation, colors, fonts, motion timing)
- [ ] Transcribe first 30 seconds (hook analysis)
- [ ] Count cuts per minute (pacing analysis)
- [ ] Identify signature moves (recurring elements)
- [ ] Document parameters in JSON format
- [ ] Map to Remotion components
- [ ] Test implementation and iterate

## The Creator Analysis Framework

### Visual Style Dimensions

| Dimension | What to Extract | Example Values |
|-----------|----------------|----------------|
| **Typography** | Font family, size, weight, letter spacing, transform | Inter 72px, weight 800, uppercase, -0.03em spacing |
| **Color** | Base text, highlight colors, backgrounds | White base, yellow #FFFF00 highlight, pink #FF9999 accent |
| **Rotation** | Static angle, animated rotation, tilt direction | -3° static (energetic), 0° (authoritative), +2° (playful) |
| **Motion** | Entry style, exit style, easing curves, duration | Pop-in with spring overshoot, 6 frames, cubic-bezier(0.34, 1.56, 0.64, 1) |
| **Timing** | Duration on screen, stagger between elements | 2.2s hold, 4 frame stagger per word |
| **Spatial Layout** | Position (x/y %), max width, alignment | Center 50%, y=55%, max width 90% |

### Content Style Dimensions

| Dimension | What to Extract | Purpose |
|-----------|----------------|---------|
| **Pacing** | Cuts per minute, speech rate, silence duration | High energy (8+ CPM), calm educational (3-5 CPM) |
| **Hook Structure** | First 5-30 seconds formula | Question + promise + proof + curiosity gap |
| **Retention Tactics** | Setup-payoff cycles, visual variety, music sync | Every 8-12 seconds, change stimulus |
| **Storytelling Structure** | Core/casual/new framework, chapter announcements | Appeal to all audience segments simultaneously |

### Technical Dimensions

| Dimension | How to Measure | Tools |
|-----------|---------------|-------|
| **Audio Quality** | Loudness (LUFS), EQ profile, compression ratio | FFmpeg loudnorm filter, Adobe Audition |
| **Cuts Per Minute** | Frame-by-frame scene detection | FFmpeg scene filter, manual counting |
| **B-Roll Usage** | % of video with overlays vs talking head | Manual analysis |
| **Color Grading** | LUT analysis, color temperature, contrast | FFmpeg histogram, color analysis |

---

## Case Study 1: Iman Gadzhi (PRIMARY REFERENCE)

> **Signature Style**: High-energy business authority with aggressive text animations, -3° tilted kinetic typography, and word-level highlighting synced to speech emphasis.

### Visual Signature

**The -3° Rotation** (Iman's trademark):

```json
{
  "rotation_degrees": -3,
  "angle_static": true,
  "psychology": "Dynamic and energetic without being chaotic",
  "use_case": "Emphasis phrases, keywords, urgent calls-to-action"
}
```

**Why -3° works:**
- **0°**: Professional, authoritative, stable (news anchors, educational)
- **-3°**: Energetic, dynamic, action-oriented (business, motivation)
- **-5° or more**: Chaotic, overwhelming, loses readability
- **Positive angles (+2° to +4°)**: Playful, casual, friendly

**Color Psychology**:

| Color | Hex | Psychological Effect | When to Use |
|-------|-----|---------------------|-------------|
| Yellow | #FFFF00 | Optimism, urgency, attention | Action words, benefits, key metrics |
| Pink | #FF9999 | Warmth, approachability, emotion | Personal stories, relatable moments |
| White | #FFFFFF | Clarity, authority, professionalism | Base text, headlines, facts |

### Technical Parameters (Iman's Style)

**Headline Phrases** (first 30 seconds):

```json
{
  "component_type": "text_highlight_caption",
  "spatial": {
    "anchor": "center",
    "x_percent": 50,
    "y_percent": 50,
    "max_width_percent": 80,
    "rotation_degrees": 0
  },
  "transform": {
    "entry_style": "fade_in_scale_up",
    "scale": { "from": 1.0, "to": 1.05 },
    "opacity": { "from": 0, "to": 1 },
    "easing": "ease_out"
  },
  "timing": {
    "entry_duration_frames": 10,
    "hold_duration_seconds": 2.5,
    "exit_behavior": "hard_cut"
  },
  "color": {
    "base_text": "white",
    "highlight": "none"
  }
}
```

**Emphasis Phrases** (the signature kinetic text):

```json
{
  "component_type": "kinetic_text_phrase",
  "spatial": {
    "anchor": "center",
    "x_percent": 50,
    "y_percent": 55,
    "max_width_percent": 90,
    "rotation_degrees": -3,
    "position_drift": true
  },
  "transform": {
    "entry_style": "pop_in",
    "scale": { "from": 0.9, "to": 1.0 },
    "opacity": { "from": 0, "to": 1 },
    "easing": "ease_out_back"
  },
  "timing": {
    "entry_duration_frames": 6,
    "hold_duration_seconds": 2.0,
    "exit_behavior": "hard_cut"
  },
  "color": {
    "base_text": "white",
    "highlight": "accent",
    "color_change_strategy": "per_word",
    "intonation_alignment": true
  },
  "typography": {
    "font_family": "Inter",
    "font_size": 72,
    "font_weight": 800,
    "text_transform": "uppercase",
    "letter_spacing": "-0.03em"
  }
}
```

### Remotion Implementation

Iman's style is implemented in:
- `remotion-editor/src/components/iman-graphics/KineticTextPhrase.tsx`
- `remotion-editor/src/components/iman-graphics/TextHighlightCaption.tsx`

**Key Implementation Details**:

```tsx
// The -3° rotation with Y-drift for organic feel
<div style={{
  transform: `scale(${entryScale}) rotate(-3deg) translateY(${yDrift}px)`,
  opacity: opacity
}}>
  {/* Kinetic text content */}
</div>

// Per-word highlighting with stagger
const staggerDelay = index * WORD_STAGGER_FRAMES; // 4 frames
const wordScale = isHighlighted ? 1.1 : 1.0; // 10% pop on emphasis
const wordColor = isHighlighted ? YELLOW : WHITE;
```

**Intonation Alignment Rule**:
> Visual scale pop (1.1x) occurs exactly on the vowel stress of the emphasized word.

Example:
- "TRANSFORM your business" → "TRANSFORM" pops at frame 12
- "Make MORE money" → "MORE" pops at frame 24

### When to Use Iman's Style

| Content Type | Use Iman Style? | Reason |
|-------------|----------------|--------|
| Business coaching | YES | Authority + energy matches business growth mindset |
| Technical tutorials | PARTIAL | Use 0° rotation, keep color highlights for key concepts |
| Personal vlogs | NO | Too aggressive, use softer styles |
| Sales/marketing content | YES | Urgency and action-orientation drives conversions |
| Educational explainers | PARTIAL | Use headline style (0°), avoid kinetic emphasis |

---

## Case Study 2: Other Creator Patterns

### Jack Roberts / Harut: Validation Framework

**Core Strategy**: Outlier analysis on small channels

**Content Dimensions**:
```
1. Find small channels with recent outlier videos (last 2 months)
2. Copy their title and search it
3. Ask: "What can I do better than this?"
4. Validate the idea BEFORE executing
5. Document thesis of why the video is doing well
```

**Time-to-Value Score**: How quickly does the viewer get actionable value?

**Visual Style**: Clean, minimal overlays. Focus on clarity over flash.

### Paddy Galloway: Frontloading Strategy

**Hook Formula**:
```
First 5 seconds: Answer "Why am I watching this?"
↓
Promise the outcome
↓
Show proof (authority/results)
↓
Deliver value immediately
```

**Core/Casual/New Framework**: Make videos that appeal to three audience segments simultaneously:
- **Core**: Deep insights for existing subscribers
- **Casual**: Interesting enough for occasional viewers
- **New**: Accessible for first-time viewers

**Visual Style**: Professional broadcast quality, lower thirds, clean typography (0° rotation).

### Alex Hormozi: Title Obsession

**Content Strategy from `.tmp/extracted/youtube/chunk_001.md` (line 46-48)**:
> "An hour just on titles, big idea and concept, the packaging and the first 20 secs. Not on the video as much."

**The 5 Ps Checklist**:
1. **Proof**: "Why should I listen to you?" (show credentials/results)
2. **Promise**: The transformation you're offering
3. **Plan**: The roadmap to get there (3 steps, 5 rules, etc.)
4. **Pain**: The opposite of promise ("so you don't waste hours doing XYZ")
5. **Picture**: Vivid imagery of the outcome

**Unanswered Question Principle**: Thumbnail + title create curiosity gap that can ONLY be closed by watching.

**Visual Style**: Minimal text overlays, focus on packaging (thumbnail/title) over in-video graphics.

### Aprilynne Alter: Hook Psychology

**From `.tmp/extracted/aprilynne/hooks/chunk_001.md` (lines 8-28)**:

**4-Step Intro Formula**:
1. **Match the thumbnail** (first 5 seconds confirm T&T wasn't clickbait)
2. **Create unanswered question** ("Will he get the world record?")
3. **Promise a formula** ("3 simple steps")
4. **Show don't tell** (visual proof, not just claims)

**Thumbnail Psychology** (lines 82-98):
```
Curiosity = Desire + Deprivation
↓
Brain craves closure
↓
Unfinished story + Question without answer = Click
↓
"What led to this moment? What happens next?"
```

**Scroll Stoppers** (lines 116-135):
- **Faces**: Larger face = bigger effect
- **Recognizable interfaces**: Discord, iMessage, PayPal
- **Large round numbers**: Especially with money attached
- **Danger/Movement**: Signals threat detection
- **Emotion**: Emotional reactions trigger empathy
- **Bright colors**: Yellow, pink, red
- **Aesthetics**: Visually pleasing = dopamine reward

**Visual Style**: Heavy motion graphics, fast cuts, music synced to visual changes.

### Retention Strategy (Setup → Payoff Cycles)

**From `.tmp/extracted/aprilynne/retention/chunk_001.md` (lines 10-14)**:

> "Each payoff comes with a setup that provides the purpose, context and tone of upcoming section. Primes the audience to care what is coming next."

**Pattern**: Setup (curiosity + intrigue) → Payoff (answer + new question)

**Example**:
```
Setup: "There are 3 mistakes killing your channel..." (curiosity)
↓
Payoff: "The first one is..." (answer)
↓
Setup: "But the second mistake is even worse..." (new curiosity)
```

**Timing**: Every 8-12 seconds, change one of:
- A-roll to B-roll
- Quiet to music
- Static to motion graphic
- Close-up to wide shot

---

## How to Extract Style Parameters (Step-by-Step)

### Step 1: Visual Pattern Recognition

Watch 3-5 videos from the creator. For each, note:

```
Video: [Title]
Runtime: [Duration]

TEXT OVERLAYS:
- Font: [Family, size, weight]
- Colors: [Base, highlight 1, highlight 2]
- Rotation: [Degrees, static or animated]
- Position: [Screen area, % from edges]
- Duration: [Seconds on screen]

MOTION:
- Entry: [Fade in, pop in, slide in, etc.]
- Exit: [Hard cut, fade out, slide out]
- Easing: [Linear, ease-out, spring bounce]
- Timing: [Duration in frames]

SIGNATURE MOVES:
- [Recurring element 1]
- [Recurring element 2]
- [Recurring element 3]
```

### Step 2: Hook Structure Analysis

Transcribe the first 30 seconds:

```bash
# Use Whisper to transcribe
python -c "
from faster_whisper import WhisperModel
model = WhisperModel('base')
segments, _ = model.transcribe('video.mp4', language='en')
for i, seg in enumerate(segments):
    if seg.start < 30:  # First 30 seconds only
        print(f'[{seg.start:.1f}s] {seg.text}')
"
```

Analyze the hook:
```
[0.0s] "Three mistakes are killing your channel..."  ← Creates curiosity
[3.2s] "And I'm going to show you exactly how to fix them..."  ← Promise
[6.1s] "Because I grew my channel to 500K using these..."  ← Proof
[8.9s] "Let's start with the first one..."  ← Forward momentum
```

### Step 3: Pacing Analysis (Cuts Per Minute)

```bash
# Count scene changes with FFmpeg
ffmpeg -i video.mp4 -vf "select='gt(scene,0.3)',showinfo" -f null - 2>&1 | \
  grep "Parsed_showinfo" | wc -l

# Calculate CPM
# cuts / (duration_seconds / 60) = cuts per minute
```

**Benchmarks**:
- High energy (MrBeast, Iman): 8-12 CPM
- Standard talking head: 4-6 CPM
- Educational/calm: 2-4 CPM

### Step 4: Identify Signature Moves

Look for patterns that appear in EVERY video:

**Iman Gadzhi**: -3° tilted kinetic text + yellow highlights on emphasis words
**Ali Abdaal**: Smooth camera movements + pastel color overlays
**MrBeast**: High-contrast thumbnails + fast-paced editing + money references

### Step 5: Document in JSON Format

Create a style profile:

```json
{
  "creator_name": "Creator Name",
  "analysis_date": "2026-02-16",
  "sample_videos": ["video1_id", "video2_id", "video3_id"],

  "visual_signature": {
    "typography": {
      "font_family": "Inter",
      "font_size": 72,
      "font_weight": 800,
      "text_transform": "uppercase",
      "letter_spacing": "-0.03em"
    },
    "colors": {
      "base_text": "#FFFFFF",
      "highlight_1": "#FFFF00",
      "highlight_2": "#FF9999"
    },
    "rotation": {
      "angle_degrees": -3,
      "static": true,
      "reasoning": "Dynamic energy without chaos"
    },
    "motion": {
      "entry_style": "pop_in",
      "entry_duration_frames": 6,
      "exit_style": "hard_cut",
      "easing": "cubic-bezier(0.34, 1.56, 0.64, 1)"
    }
  },

  "content_signature": {
    "hook_formula": "Question + Promise + Proof",
    "avg_cuts_per_minute": 8,
    "retention_tactic": "Setup-payoff cycles every 10s",
    "storytelling_structure": "Core/casual/new framework"
  },

  "technical_specs": {
    "audio_lufs": -16,
    "speech_rate_wpm": 160,
    "b_roll_percentage": 35
  }
}
```

### Step 6: Map to Remotion Components

For each visual element, identify the corresponding Remotion component:

| Creator Style Element | Remotion Component | Props to Set |
|----------------------|-------------------|--------------|
| Tilted kinetic text | `<KineticTextPhrase />` | `rotationDegrees={-3}`, `highlightColor` |
| Headline overlay | `<TextHighlightCaption />` | `yPercent={60}`, `rotationDegrees={0}` |
| Background graphic | `<BackgroundTakeover />` | `backgroundType`, `foregroundElements` |
| Lower third | `<LowerThird />` | `name`, `title`, `position` |

---

## When to Use Which Style

### Content Type → Style Mapping

| Content Goal | Recommended Style | Key Elements | Avoid |
|-------------|------------------|--------------|-------|
| **Authority Building** (AI coaching, business strategy) | Iman Gadzhi | -3° rotation, yellow highlights, kinetic text | Playful colors, slow pacing |
| **Educational Tutorials** (how-to, step-by-step) | Paddy Galloway | 0° rotation, clean lower thirds, chapter markers | Aggressive motion, tilted text |
| **Personal Branding** (vlogs, storytelling) | Aprilynne Alter | Heavy B-roll, fast cuts, music sync | Corporate colors, static overlays |
| **Sales/Marketing** (VSLs, lead gen) | Hormozi + Iman | Minimal overlays, focus on packaging, -3° for CTAs | Over-designed graphics that distract |
| **Viral Shorts** (TikTok, YouTube Shorts) | MrBeast | High contrast, large text, 10+ CPM | Subtle effects, small text, slow pacing |

### Business Goal → Creator Reference

**For Heroes Ark (Chris positioning as AI authority)**:

```
Primary: Iman Gadzhi style (70%)
- Authority + energy matches AI business positioning
- -3° rotation for emphasis on ROI/results
- Yellow highlights on key metrics ($10K/month, 5x ROI, etc.)
- White base text for professional credibility

Secondary: Hormozi packaging (20%)
- Obsess over first 20 seconds
- Title/thumbnail create unanswered question
- Show proof early (client results, case studies)

Tertiary: Paddy Galloway structure (10%)
- Core/casual/new framework
- Appeal to agency owners (core), consultants (casual), skeptics (new)
- Frontload the "why" (time savings, revenue increase)
```

---

## Implementation Guide

### Adapting Iman's -3° Rotation

**When to use -3°**:
- Emphasis phrases ("TRANSFORM your business")
- Action-oriented CTAs ("Book a call NOW")
- Key metrics ("$50K in 30 days")
- Urgency statements ("Limited spots available")

**When to use 0°** (professional authority):
- Headlines and chapter titles
- Complex technical explanations
- Credibility statements (case studies, testimonials)
- Legal disclaimers or important caveats

**When to use other angles**:
- `+2° to +4°`: Playful, casual content (personal vlogs, behind-the-scenes)
- `-5° or more`: Avoid (loses readability, feels chaotic)

### Color Psychology Application

**Yellow (#FFFF00)** - Optimism, attention, urgency:
```tsx
// Use for action words and benefits
<KineticTextPhrase
  words={["GROW", "YOUR", "BUSINESS"]}
  highlightWordIndex={0}  // "GROW" in yellow
  highlightColor="#FFFF00"
  rotationDegrees={-3}
/>
```

**Pink (#FF9999)** - Warmth, emotion, relatability:
```tsx
// Use for personal stories and emotional hooks
<TextHighlightCaption
  text="I was broke and desperate..."
  highlightColor="#FF9999"
  rotationDegrees={0}
/>
```

**White (#FFFFFF)** - Clarity, authority, professionalism:
```tsx
// Use for facts, statistics, explanations
<TextHighlightCaption
  text="AI automation reduces costs by 73%"
  baseColor="#FFFFFF"
  rotationDegrees={0}
/>
```

### Remotion Component Templates

**Template 1: Iman-Style Emphasis** (for key moments):

```tsx
import { KineticTextPhrase } from './components/iman-graphics';

<Sequence from={90} durationInFrames={66}>
  <KineticTextPhrase
    words={["TRANSFORM", "YOUR", "BUSINESS"]}
    highlightWordIndex={0}
    rotationDegrees={-3}
    highlightColor="#FFFF00"
    intonationAligned={true}
  />
</Sequence>
```

**Template 2: Professional Headline** (for chapters):

```tsx
import { TextHighlightCaption } from './components/iman-graphics';

<Sequence from={0} durationInFrames={75}>
  <TextHighlightCaption
    text="The 3 Rules of AI Automation"
    yPercent={50}
    rotationDegrees={0}
    fontWeight={700}
    highlightBehavior="all_at_once"
  />
</Sequence>
```

**Template 3: Speech-Synced Reveal** (for dynamic captions):

```tsx
import { TextHighlightCaption } from './components/iman-graphics';

<Sequence from={30} durationInFrames={180}>
  <TextHighlightCaption
    text="This is how you automate your entire workflow"
    words={[
      { word: "This", startFrame: 0, endFrame: 8, isHighlighted: false },
      { word: "is", startFrame: 8, endFrame: 12, isHighlighted: false },
      { word: "how", startFrame: 12, endFrame: 20, isHighlighted: false },
      { word: "you", startFrame: 20, endFrame: 28, isHighlighted: false },
      { word: "automate", startFrame: 28, endFrame: 50, isHighlighted: true },
      // ... continue for each word
    ]}
    yPercent={65}
    rotationDegrees={-3}
    highlightBehavior="speech_synced"
    highlightColor="#FFFF00"
  />
</Sequence>
```

---

## Troubleshooting

### Issue: Text is hard to read

**Causes**:
- Rotation angle too extreme (> 5°)
- Font size too small (< 48px at 1080p)
- Insufficient contrast with background
- Letter spacing too tight

**Solutions**:
```tsx
// Add text shadow for readability
import { TEXT_SHADOW_STRONG } from './components/iman-graphics/colors';

style={{
  textShadow: TEXT_SHADOW_STRONG,  // "0 2px 8px rgba(0,0,0,0.8)"
}}

// Or add background box
style={{
  backgroundColor: "rgba(0,0,0,0.7)",
  padding: "0.5em 1em",
  borderRadius: "0.2em",
}}
```

### Issue: Motion feels too aggressive or slow

**Diagnosis**:
```bash
# Check entry duration
entry_duration_frames = 6  # Too fast if < 4, too slow if > 12

# Check easing curve
easing = "ease_out_back"  # Creates overshoot bounce
easing = "ease_out"       # Smoother, more professional
```

**Solutions**:
- **Too aggressive**: Increase `entry_duration_frames` to 10-12, use `ease_out` instead of `ease_out_back`
- **Too slow**: Decrease to 4-6 frames, use `ease_out_back` for pop

### Issue: Style doesn't match creator reference

**Debugging checklist**:
1. Compare rotation angle (use browser dev tools to inspect)
2. Verify color hex codes (use eyedropper tool)
3. Measure duration on screen (count frames in reference video)
4. Check easing curve (does it bounce or smooth?)
5. Verify font family, size, weight (screenshot and compare)

### Issue: Intonation alignment is off

**Problem**: Visual emphasis doesn't match speech emphasis.

**Solution**:
```tsx
// Manually set word timing based on Whisper transcription
const words = [
  { word: "TRANSFORM", startFrame: 12, endFrame: 28, isHighlighted: true },
  { word: "your", startFrame: 28, endFrame: 36, isHighlighted: false },
  { word: "business", startFrame: 36, endFrame: 52, isHighlighted: false },
];

// Set highlightWordIndex to the emphasized word
<KineticTextPhrase
  words={words}
  highlightWordIndex={0}  // "TRANSFORM"
  intonationAligned={true}
/>
```

---

## Mission Connection

**How Creator Style Analysis Serves Heroes Ark's Mission**:

1. **Authority Positioning**: By studying creators who successfully position themselves as authorities (Iman, Hormozi), we learn visual and content patterns that signal expertise and credibility.

2. **Inbound Lead Generation**: Analyzing viral hooks and retention tactics (Aprilynne, MrBeast) helps create videos that get views and warm up cold audiences before outreach.

3. **Proof for Florian's Coaching**: Systematizing the analysis process demonstrates mastery of content production, which becomes a case study for Florian's AI coaching business.

4. **Efficient Iteration**: Understanding WHY certain styles work (psychology of -3° rotation, color choices, etc.) allows rapid testing without guesswork.

**The Ultimate Goal**: Chris's videos should establish AI authority, generate qualified leads, and demonstrate systemized processes — all of which are optimized by learning from proven creator patterns.

---

## Resources

### Primary References

- **Iman Gadzhi Style Profile**: `directives/iman_gadzhi_style_profile.md`
- **Remotion Implementation**: `remotion-editor/src/components/iman-graphics/`
  - `KineticTextPhrase.tsx` (lines 1-178)
  - `TextHighlightCaption.tsx` (lines 1-189)
- **YouTube Research Notes**: `.tmp/extracted/youtube/chunk_001.md`
  - Jack Roberts/Harut: lines 10-25
  - Paddy Galloway: lines 28-40
  - Hormozi: lines 46-60
- **Aprilynne Alter - Hooks**: `.tmp/extracted/aprilynne/hooks/chunk_001.md`
  - Hook formula: lines 8-28
  - Thumbnail psychology: lines 82-156
- **Aprilynne Alter - Retention**: `.tmp/extracted/aprilynne/retention/chunk_001.md`
  - Setup-payoff cycles: lines 10-31

### Related Skills

- `editing-talking-head-videos` - Base editing workflow (silence removal, audio enhancement)
- `transcribing-youtube-videos` - Extract transcripts for content analysis
- `scraping-youtube-channel-videos` - Gather sample videos for analysis

### External Resources

- Remotion docs: https://www.remotion.dev/docs/
- FFmpeg filters: https://ffmpeg.org/ffmpeg-filters.html
- Color psychology: https://www.verywellmind.com/color-psychology-2795824
- Typography psychology: https://www.toptal.com/designers/typography/psychology-of-fonts

### Tools for Analysis

```bash
# Transcribe first 30 seconds
python -c "from faster_whisper import WhisperModel; ..."

# Count cuts per minute
ffmpeg -i video.mp4 -vf "select='gt(scene,0.3)',showinfo" -f null -

# Extract color palette
ffmpeg -i video.mp4 -vf "palettegen=stats_mode=single" palette.png

# Measure audio loudness
ffmpeg -i video.mp4 -af "loudnorm=print_format=json" -f null -
```

---

## Quick Reference: Creator Style Cheat Sheet

| Creator | Rotation | Highlight Color | Pacing (CPM) | Best For |
|---------|----------|----------------|--------------|----------|
| **Iman Gadzhi** | -3° | Yellow #FFFF00 | 8-10 | Business coaching, authority content |
| **Hormozi** | 0° | Minimal overlays | 4-6 | Sales, marketing, packaging-first |
| **Paddy Galloway** | 0° | White/pastels | 5-7 | Educational, strategic analysis |
| **Aprilynne Alter** | Variable | Bright colors | 10-12 | Personal branding, storytelling |
| **MrBeast** | 0° | High contrast | 12+ | Viral content, shorts, entertainment |

**For Heroes Ark (Chris)**: Iman-style -3° rotation + yellow highlights + 8 CPM + Hormozi packaging principles.
