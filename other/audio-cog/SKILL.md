---
name: audio-cog
description: AI audio generation powered by CellCog. Text-to-speech, voice synthesis, voiceovers, podcast audio, narration, music generation, background music, sound design. Professional audio creation with AI.
metadata:
  openclaw:
    emoji: "🎵"
author: CellCog
dependencies: [cellcog]
---

# Audio Cog - AI Audio Generation Powered by CellCog

Create professional audio with AI - from voiceovers and narration to background music and sound design.

---

## Prerequisites

This skill requires the `cellcog` skill for SDK setup and API calls.

```bash
clawhub install cellcog
```

**Read the cellcog skill first** for SDK setup. This skill shows you what's possible.

**Quick pattern (v1.0+):**
```python
# Fire-and-forget - returns immediately
result = client.create_chat(
    prompt="[your audio request]",
    notify_session_key="agent:main:main",
    task_label="audio-task",
    chat_mode="agent"  # Agent mode is optimal for all audio tasks
)
# Daemon notifies you when complete - do NOT poll
```

---

## What Audio You Can Create

### Text-to-Speech / Voiceover

Convert text to natural-sounding speech:

- **Narration**: "Generate a professional male voiceover for this product video script"
- **Audiobook Style**: "Create an engaging narration of this short story with emotional delivery"
- **Podcast Intros**: "Generate a warm, friendly podcast intro: 'Welcome to The Daily Tech...'"
- **E-Learning**: "Create clear, instructional voiceover for this training module"
- **IVR/Phone Systems**: "Generate professional phone menu prompts"

---

## Available Voices

CellCog provides 8 high-quality voices with distinct characteristics:

| Voice | Gender | Best For | Characteristics |
|-------|--------|----------|-----------------|
| **cedar** | Male | Product videos, announcements | Warm, resonant, authoritative, trustworthy |
| **marin** | Female | Professional content, tutorials | Bright, articulate, emotionally agile |
| **ballad** | Male | Storytelling, flowing narratives | Smooth, melodic, musical quality |
| **coral** | Female | Energetic content, ads | Vibrant, lively, dynamic, spirited |
| **echo** | Male | Thoughtful content, documentaries | Calm, measured, deliberate |
| **sage** | Female | Educational, knowledge content | Wise, contemplative, reflective |
| **shimmer** | Female | Gentle content, wellness | Soft, gentle, soothing, approachable |
| **verse** | Male | Creative, artistic content | Poetic, rhythmic, expressive |

### Voice Recommendations by Use Case

**For product videos and announcements:**
> Use **cedar** (male) or **marin** (female) - both project confidence and professionalism.

**For storytelling and audiobooks:**
> Use **ballad** (male) or **sage** (female) - designed for engaging, flowing narratives.

**For high-energy content:**
> Use **coral** (female) - vibrant and dynamic, perfect for ads and exciting announcements.

**For calm, educational content:**
> Use **echo** (male) or **shimmer** (female) - measured pacing ideal for learning.

### Voice Style Customization

Beyond selecting a voice, you can fine-tune delivery with style instructions:

- **Accent & dialect**: American, British, Australian, Indian, etc.
- **Emotional range**: Excited, serious, warm, mysterious, dramatic
- **Pacing**: Slow and deliberate, conversational, fast and energetic
- **Special effects**: Whispering, character impressions

**Example with style instructions:**
> "Generate voiceover using cedar voice with a warm, conversational tone. Speak at medium pace with slight enthusiasm when mentioning features. American accent."

---

## Music Generation

Create original background music and soundtracks:

- **Background Music**: "Create calm lo-fi background music for a study video, 2 minutes"
- **Podcast Music**: "Generate an upbeat intro jingle for a tech podcast, 15 seconds"
- **Video Soundtracks**: "Create cinematic orchestral music for a product launch video"
- **Ambient/Mood**: "Generate peaceful ambient sounds for a meditation app"
- **Genre-Specific**: "Create energetic electronic music for a fitness video"

### Music Specifications

| Parameter | Options |
|-----------|---------|
| **Duration** | 15 seconds to 5+ minutes |
| **Genre** | Electronic, rock, classical, jazz, ambient, lo-fi, cinematic, pop, hip-hop |
| **Tempo** | 60 BPM (slow) to 180+ BPM (fast) |
| **Mood** | Upbeat, calm, dramatic, mysterious, inspiring, melancholic |
| **Instruments** | Piano, guitar, synth, strings, drums, brass, etc. |

### Music Licensing

**All AI-generated music from CellCog is royalty-free and fully yours to use commercially.**

You have complete rights to use the generated music for:
- YouTube videos (including monetized content)
- Commercial projects and advertisements
- Podcasts and streaming
- Apps and games
- Any other commercial or personal use

No attribution required. No licensing fees. The music is generated uniquely for you.

---

## Audio Output Formats

| Format | Best For |
|--------|----------|
| **MP3** | Standard audio delivery, voiceovers, music |
| Combined with video | Background music for video-cog outputs |

---

## Chat Mode for Audio

**Use `chat_mode="agent"`** for all audio generation tasks.

Audio generation—whether voiceovers, music, or sound design—executes efficiently in agent mode. CellCog's audio capabilities don't require multi-angle deliberation; they require precise execution, which agent mode excels at.

There's no scenario where agent team mode provides meaningfully better audio output. Save agent team for research and complex creative work that benefits from multiple reasoning passes.

---

## Example Audio Prompts

**Professional voiceover with specific voice:**
> "Generate a professional voiceover using the **marin** voice for this script:
> 
> 'Introducing TaskFlow - the project management tool that actually works. With intelligent automation, seamless collaboration, and powerful analytics, TaskFlow helps teams do their best work.'
> 
> Style: Confident and friendly, medium pace. Suitable for a product launch video."

**Podcast intro with voice selection:**
> "Create a podcast intro voiceover using **cedar** voice:
> 
> 'Welcome to Future Forward, the podcast where we explore the technologies shaping tomorrow. I'm your host, and today we're diving into...'
> 
> Style: Warm and engaging, conversational tone. Also generate a 10-second upbeat intro music bed to go underneath."

**Background music:**
> "Generate 2 minutes of calm, lo-fi hip-hop style background music. Should be chill and unobtrusive, good for studying or working. Include soft piano, mellow beats, and gentle vinyl crackle. 75 BPM."

**Audiobook narration:**
> "Create an audiobook-style narration using **ballad** voice for this passage:
> 
> [passage text]
> 
> Style: Warm storytelling quality, measured pace with appropriate pauses for drama."

**Cinematic music:**
> "Generate 90 seconds of cinematic orchestral music for a tech company's 'About Us' video. Start soft and inspiring, build to a confident crescendo, then resolve to a hopeful ending."

---

## Multi-Language Support

CellCog can generate speech in 50+ languages:

- English (multiple accents)
- Spanish, French, German, Italian, Portuguese
- Chinese (Mandarin, Cantonese)
- Japanese, Korean
- Hindi, Arabic
- Russian, Polish, Dutch
- And many more

Specify the language in your prompt:
> "Generate this text in Japanese with a native female speaker using shimmer voice: 'いらっしゃいませ...'"

---

## Tips for Better Audio

1. **Choose the right voice**: Match the voice to your content type. Cedar/marin for professional, ballad/sage for storytelling, coral for energy.

2. **Provide the complete script**: Don't say "something about our product" - write out exactly what should be said.

3. **Include style instructions**: "Confident but warm", "slow and deliberate", "with slight excitement" helps shape delivery.

4. **For music**: Specify duration, tempo (BPM if you know it), mood, and genre.

5. **Pronunciation guidance**: For names or technical terms, add hints: "CellCog (pronounced SELL-kog)"

6. **Emotional beats**: For longer voiceovers, indicate tone shifts: "[excited] And now for the big reveal... [serious] But there's a catch."
