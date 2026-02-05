---
name: sound-effect-sourcing
description: Sound effect sourcing from Adobe Audition, Freesound, ElevenLabs text-to-sound-effects, and audio library management for professional productions. Use when adding sound effects, building audio libraries, or creating immersive soundscapes.
---

# Sound Effect Sourcing

## Adobe Audition Sound Library (12,000+ Free Effects)

### Access

- **No Subscription Required**: Available to everyone
- **Quality**: Broadcast-quality, fully uncompressed
- **Access**: Via Adobe Audition or Premiere Pro
- **License**: Royalty-free

### Categories

```
Available sound effects:
├─ Ambience (nature, city, crowds)
├─ Animals (birds, dogs, wildlife)
├─ Crashes (glass, metal, impacts)
├─ Drones (atmospheric, industrial)
├─ Fires & Explosions
├─ Foley (movement, cloth, objects)
├─ Footsteps (surfaces, paces)
├─ Impacts (punches, hits, falls)
├─ Interfaces (buttons, beeps, UI)
├─ Machines (engines, tools, tech)
├─ Nature (weather, water, wind)
├─ Transportation (cars, trains, planes)
└─ Voices (crowd reactions, shouts)
```

### Download

```
Adobe Audition → Effects → Sound Effects
Browse by category
Preview in application
Download individual or bulk
```

## Freesound (Community Library)

### Overview

- **Size**: Vast library of user-contributed sounds
- **License**: Mostly Creative Commons
- **Quality**: Variable (check ratings)
- **Attribution**: Check each sound's license

### License Types

```
CC0 (Public Domain):
- No attribution required
- Use freely

CC BY (Attribution):
- Credit required
- "Sound by [author] from Freesound.org"

CC BY-NC (Attribution-NonCommercial):
- Credit required
- Non-commercial use only
```

### Search Best Practices

```
# Use specific terms
"wooden door creak slow" (better)
vs "door sound" (too broad)

# Filter by:
- License type (CC0 for easiest use)
- Duration
- Sample rate
- File type (WAV preferred)

# Check:
- Preview before download
- Read description
- Verify license
```

## ElevenLabs Text-to-Sound-Effects

### API Generation

```javascript
await mcp__elevenlabs__text_to_sound_effects({
  text: "Heavy wooden door creaking open slowly",
  duration_seconds: 3,
  loop: false,
  output_format: "mp3_44100_128"
})
```

### Effective Prompts

```
# Be specific and descriptive
GOOD: "Footsteps on gravel path, slow pace, approaching from distance"
BAD: "walking sound"

GOOD: "Old typewriter keys clacking rhythmically with carriage return"
BAD: "typing"

GOOD: "Thunder crash followed by rain gradually increasing"
BAD: "storm"

GOOD: "Coffee machine brewing with steam hissing and dripping"
BAD: "coffee sound"
```

### Duration Guidelines

```
Short SFX: 0.5-2 seconds (impacts, clicks)
Medium SFX: 2-5 seconds (actions, movements)
Loop-able: 3-5 seconds (ambience, backgrounds)

Maximum: 5 seconds
```

## Sound Library Organization

### File Naming Convention

```
[Category]_[Description]_[Variation].wav

Examples:
SFX_DoorCreak_Wood_Slow_01.wav
AMB_CoffeeShop_Busy_Morning_02.wav
FOLEY_Footsteps_Gravel_Walk_Fast_03.wav
IMPACT_Glass_Break_Small_01.wav
```

### Directory Structure

```
sound-library/
├─ ambience/
│   ├─ indoor/
│   ├─ outdoor/
│   └─ nature/
├─ foley/
│   ├─ footsteps/
│   ├─ movement/
│   └─ objects/
├─ impacts/
├─ interfaces/
└─ voices/
```

## Layering Sounds

```
Base Layer:    "Rain on window, medium"
Mid Layer:     "Distant thunder rumbles"
Detail Layer:  "Occasional wind gust"

Result: Rich, immersive rainy atmosphere
```

## Resources

- Adobe Audition: audition.adobe.com/sounds
- Freesound: freesound.org
- ElevenLabs SFX: elevenlabs.io/sound-effects
- BBC Sound Effects: bbcsfx.acropolis.org.uk
