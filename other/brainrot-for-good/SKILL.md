---
name: brainrot-for-good
category: video
description: "Produce high-retention, dopamine-aware video content using brainrot editing techniques — fast cuts, word-by-word captions, sound design, visual velocity, pattern interrupts — all in service of genuinely valuable content. The Fireship model: brainrot pacing meets real substance. Built on Remotion with Imagen/Veo for assets. Use when: (1) creating edutainment content that competes with brainrot for attention, (2) making technical content accessible to younger audiences, (3) producing TikTok/Reels/Shorts that teach while entertaining, (4) applying engagement psychology ethically, (5) adding brainrot energy to a launch video or product demo. Triggers on: 'brainrot', 'edutainment', 'fast-paced video', 'tiktok style', 'shorts style', 'dopamine video', 'high retention', 'fireship style', 'brainrot for good'."
---

# Brainrot for Good — High-Retention Video with Substance

Use the attention-capture techniques of brainrot content — fast cuts, word-by-word captions, sound design, pattern interrupts — to deliver content that actually matters. The pacing of brainrot, the substance of a textbook.

## The Ethical Framework

**This skill exists for one reason**: attention is the scarcest resource, and the techniques that capture it most effectively are currently used for empty content. We reclaim them for value.

### The Ethical Test (apply to every piece)

1. **Value-first**: Does every engagement technique serve content that delivers genuine insight?
2. **Substance survives**: If you removed all effects and read the script as plain text, would it still be worth reading?
3. **Active recall**: Does the content prompt action (try this, build this, think about this)?
4. **No exploitation**: Are you capturing attention to deliver value, or just capturing attention?
5. **Transparency**: The audience knows this is engineered for engagement — don't pretend otherwise.

**If the script has nothing to teach, no technique will save it. Fix the script first.**

## Compounding Skills

| Skill | Role |
|-------|------|
| `/launch-video` | Liquid Glass aesthetic, GlassPanel, ParticleField, spring animations |
| `/remotion-best-practices` | Composition structure, `<Sequence>`, rendering |
| `/content-creation` | Storytelling frameworks, AI assets (Imagen, Veo, TTS) |
| `/google-veo` | Cinematic B-roll generation |
| `/subtitle-generation` | Word-by-word caption generation |
| `/blog-post` | Distribution pipeline |
| `/creative-review` | Style adherence scoring |

## The 8 Retention Triggers

Based on dopamine-economy research. Use all 8 in every video:

| # | Trigger | Technique | Ethical Use |
|---|---------|-----------|-------------|
| 1 | **Pattern Interrupt** | Visual/audio jolt every 2-4s that resets attention | Emphasize key information, not random noise |
| 2 | **Information Gap** | Tease the answer before revealing it | Build genuine curiosity about real concepts |
| 3 | **Visual Velocity** | Scene change every 2-4 seconds | Match cuts to content beats, not arbitrary |
| 4 | **Micro-Narrative** | Setup → conflict → resolution in 15-60s | Teach through story, not just facts |
| 5 | **Sensory Layering** | Synced VO + visuals + text + SFX | Each layer reinforces the SAME message |
| 6 | **Social Proof** | "Most developers don't know this" | Only use when the claim is actually true |
| 7 | **Thesis-Antithesis** | Present belief → challenge → resolve with insight | Create genuine cognitive engagement |
| 8 | **Exit Prevention** | Cliffhanger or CTA in final 3 seconds | Point to something worth their time |

## Pacing Specs

| Metric | Brainrot Standard | Brainrot-for-Good Target | Fireship Reference |
|--------|-------------------|--------------------------|-------------------|
| Cuts per minute | 20-30 | 10-15 | 10-15 |
| Words per minute | 180-220 | 200-250 | 200-250 |
| Scene hold time | 1-2s | 2-4s | 2-4s |
| Total duration | 15-60s | 30-120s | 100s (strict) |
| Pattern interrupts | Every 1-2s | Every 3-5s | Every 4-6s |
| Hook window | 1.3s | 3s | 3s |

**Key difference**: Pure brainrot overstimulates. Brainrot-for-good operates at the cognitive load *sweet spot* — enough stimulation to hold attention, not so much it overwhelms comprehension.

## Caption System (Word-by-Word)

The highest-engagement caption format. Each word appears as it's spoken, with the current word highlighted.

### Remotion Implementation

Placement follows content-engine's 9:16 layout contract
(`content-engine/references/vertical-layout.md`). On a 1080x1920 canvas the caption box
is the caption band: x 220-860, y 1288-1463, centred on 72% of the height and ending
short of the like/comment/share rail (x 872). The old bottom-anchored placement put the
words in the band the Reel UI covers with the username and caption (from y 1686 down).
Keep each group on one line within the band's 640 px, counting the active word's
1.2x scale. At 72 px extra-bold Montserrat that is about 10 uppercase characters, so
shrink the font or split the group. Run the gate with `--expect-captions`: it fails
captions moved wholly out of the band, but not captions only partly out of it, or
captions elsewhere while other text (your end-card CTA) sits in the band. Check those
on the guide sheet.

```tsx
// 1080x1920 caption band from content-engine/layout/vertical-9x16.json
const CAPTION_BAND = { left: 220, top: 1288, width: 640, height: 175 };

const WordByWordCaption: React.FC<{
  words: string[];
  currentWordIndex: number;
}> = ({ words, currentWordIndex }) => (
  <div style={{
    position: 'absolute',
    ...CAPTION_BAND,
    display: 'flex',
    flexWrap: 'wrap',
    alignItems: 'center',
    alignContent: 'center',
    justifyContent: 'center',
    gap: 8,
    lineHeight: 1.1, // two lines of 72px fit the 175px band; keep groups to one
  }}>
    {words.map((word, i) => {
      const isActive = i === currentWordIndex;
      const isPast = i < currentWordIndex;
      return (
        <span key={i} style={{
          fontFamily: 'Montserrat, sans-serif',
          fontWeight: 800,
          fontSize: 72,
          textTransform: 'uppercase',
          color: isActive ? '#FFDD00' : isPast ? '#FFFFFF' : 'rgba(255,255,255,0.3)',
          transform: isActive ? 'scale(1.2)' : 'scale(1)',
          // Stroke, not just a shadow: footage behind brainrot captions is busy.
          WebkitTextStroke: '6px #000',
          paintOrder: 'stroke fill',
          textShadow: isActive
            ? '0 0 20px rgba(255,221,0,0.5), 2px 2px 0 #000'
            : '2px 2px 0 #000',
          transition: 'all 0.1s ease',
        }}>
          {word}
        </span>
      );
    })}
  </div>
);
```

### Caption Style Presets

| Style | Font | Active Color | Use Case |
|-------|------|-------------|----------|
| **Hormozi** | Montserrat Bold, uppercase | Yellow (#FFDD00) | Business/productivity |
| **Fireship** | Inter Bold | White with glow | Technical/dev |
| **Clean** | SF Pro, sentence case | Blue (#3B82F6) | Professional/launch |
| **Chaotic** | Comic Sans Bold, random rotation | Rainbow cycling | Meme-aware edutainment |

## Sound Design

### Sound Effect Library (Ethical Use)

| Sound | When to Use | Effect | Source |
|-------|-------------|--------|--------|
| **Impact/boom** | Key stat or revelation | Emphasizes importance | Vine Boom style |
| **Whoosh** | Transition between scenes | Smooth flow | Standard SFX |
| **Cash register** | Cost savings, revenue numbers | Monetary emphasis | Standard SFX |
| **Notification ping** | New concept introduced | Signals attention | UI sounds |
| **Typing clicks** | Code or terminal scenes | Authenticity | Keyboard ASMR |
| **Bass drop** | Plot twist or contrarian reveal | Dramatic emphasis | Music production |

**Rule**: Sound effects emphasize key information. Never use them as empty stimulation. Every sound must correspond to a content beat.

### Background Music

- Lofi beats (90-110 BPM) for tutorials
- Electronic/synthwave (120-140 BPM) for product demos
- No vocals — compete with narration
- Volume: -18dB below narration

## Scene Types (Brainrot Variants of /launch-video)

### 1. Rapid-Fire Intro (replaces Title Card)
**Duration**: 3 seconds
**Content**: 3 fast cuts — problem image → solution image → result stat
**Audio**: Three ascending impact sounds
**Caption**: "STOP. SCROLLING." → topic in 5 words

### 2. Terminal Speed Run (replaces Prompt Scene)
**Duration**: 4-6 seconds
**Content**: Terminal with FAST typewriter (3-4 chars/frame), code flying by
**Audio**: Rapid keyboard ASMR, subtle bass build
**Caption**: Word-by-word narration of what's happening

### 3. Pipeline Blitz (replaces Pipeline Scene)
**Duration**: 4-5 seconds
**Content**: All 9 nodes SLAM in simultaneously with stagger of 3 frames each
**Audio**: Machine-gun impact sounds, ascending pitch
**Caption**: "NINE. PHASES." (Hormozi style, big text)

### 4. File Explosion (replaces Product Demo)
**Duration**: 3-4 seconds
**Content**: Files spray outward from center like an explosion, then snap into a grid
**Audio**: Whoosh → snap into place sound
**Caption**: "18 files. One command."

### 5. Checkmark Cascade (replaces Platform Success)
**Duration**: 3 seconds
**Content**: Platform cards slam in from edges, checkmarks EXPLODE with particle burst
**Audio**: Four rapid success chimes, ascending
**Caption**: "X. LinkedIn. Instagram. Blog. DONE."

### 6. CTA Slam (replaces CTA Card)
**Duration**: 3 seconds
**Content**: Command text SLAMS onto screen with bounce animation
**Audio**: Final impact + brief silence
**Caption**: Word-by-word "install it right now"

## Composition Structure

```
Total: 20-30 seconds (brainrot-optimized)

[0-3s]   Rapid-Fire Intro — 3 fast cuts with impacts
[3-7s]   Terminal Speed Run — fast typewriter in glass panel
[7-11s]  Pipeline Blitz — 9 nodes slam in rapid sequence
[11-15s] File Explosion — outputs spray and snap to grid
[15-18s] Checkmark Cascade — platforms verified with particle bursts
[18-21s] CTA Slam — install command with bounce

Background: ParticleField (doubled particle count, faster drift)
Captions: Word-by-word throughout, Hormozi style
Music: Synthwave 130BPM, -18dB
SFX: Impact on every scene transition
```

## Production Pipeline

```
1. SCRIPT → Write narration first (200-250 WPM, every word must teach)
   → Apply ethical test: does substance survive without effects?
2. STORYBOARD → Map each sentence to a scene with visual + SFX
3. ASSETS → Imagen 4.0 for key frames, Veo 3.1 for 2-3s B-roll bursts
4. COMPOSE → Remotion composition with:
   → WordByWordCaption component synced to narration timing
   → SFX timed to content beats (not arbitrary)
   → Visual velocity: scene change every 2-4 seconds
   → ParticleField with 80+ particles (doubled from launch-video)
5. RENDER → npx remotion render BrainrotComposition --output video.mp4
6. REVIEW → /creative-review with brainrot-specific checklist
7. DISTRIBUTE → /blog-post publish pipeline
```

## Quality Checklist (Brainrot-for-Good Specific)

### Must Pass
- [ ] Script has genuine substance (ethical test: plain text is still worth reading)
- [ ] Hook captures in first 3 seconds (pattern interrupt, not just text)
- [ ] Word-by-word captions present and synced
- [ ] 9:16 layout gate meets the pass criteria in content-engine SKILL.md "Vertical Layout Gate": `python3 ~/.claude/skills/content-engine/scripts/check_vertical_layout.py video video.mp4 --expect-captions`
- [ ] Sound effect on every scene transition
- [ ] No static shot longer than 4 seconds
- [ ] Total duration 20-60 seconds
- [ ] CTA in final 3 seconds

### Should Pass
- [ ] At least 1 thesis-antithesis moment (challenge a belief)
- [ ] At least 1 concrete number or stat
- [ ] Background music present, below -18dB
- [ ] Pacing at 10-15 cuts per minute
- [ ] Active recall prompt ("try this" or "think about this")

### Must NOT
- [ ] No engagement technique without corresponding content value
- [ ] No sensory stimulation that competes with comprehension
- [ ] No misleading social proof ("99% don't know this" — if untrue)
- [ ] No infinite-scroll optimization (video must have a clear endpoint)
- [ ] No empty split-screen gameplay (if split-screen, both halves must serve the message)
