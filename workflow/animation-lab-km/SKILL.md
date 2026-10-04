---
name: animation-lab_KM
description: >-
  Make polished motion-design and animation prototypes with Claude Code and the local media/creative skill stack. Use this when the user asks for animation directions, ASCII/bit animation, kinetic typography, cinematic title cards, audio-reactive orb/waveform visuals, liquid holograms, blueprint/lab-note motion, retro terminal animation, or design explorations that should be rendered as MP4/GIF/contact sheets rather than just described.
metadata:
  hermes:
    command_priority: 90
    tags: [animation, motion-design, ascii-video, kinetic-typography, claude-code, media-creative]
---
# Animation Lab

Use this skill as the front door for Kosta's animation/motion-design workflow. It is intentionally broader than `ascii-video`: ASCII/data can be one accent layer, but the output should be readable, designed, and cinematic.

## Load these skills first

For most jobs, load:

- `creative__ascii-video` — production pipeline for MP4/GIF/image-sequence generation
- `creative__claude-design` — design taste, layout, typography, anti-slop rules
- `agentic__claude-code-subagent-lane` — how to launch Claude Code correctly from another agent
- `creative__touchdesigner-hermes-ops` if the prompt mentions TouchDesigner/twozero/port 40404

If using Claude Code, point it explicitly at the installed Claude skills:

```text
/Users/Kosta/.claude/skills/creative__ascii-video/SKILL.md
/Users/Kosta/.claude/skills/creative__claude-design/SKILL.md
/Users/Kosta/.claude/skills/creative__touchdesigner-hermes-ops/SKILL.md
```

## Preferred slash invocation

This skill is meant to be invoked as:

```text
/animation_lab <brief>
```

Hermes internally resolves underscores and hyphens interchangeably, so `/animation-lab <brief>` also works in text surfaces that allow hyphens. Telegram's command menu displays underscores because Telegram bot commands cannot contain hyphens.

## Taste rules

Do not default to dense hacker wallpaper. Avoid full-frame Matrix rain unless explicitly requested. Treat ASCII/data as an accent layer, not the whole visual language.

Default strongest direction:

```text
cinematic clean + audio-reactive orb + kinetic captions
```

That means: dark premium background, large readable type, one central responsive form, subtle data particles, sparse captions, and restrained glow.

Good directions to explore:

1. Clean cinematic title card — huge readable type, dark glass, subtle particle/data motion.
2. Swiss tech editorial — grid typography, thin rules, off-white/navy, restrained data blocks.
3. Audio-reactive orb/waveform — one breathing central form with readable labels/captions.
4. Liquid hologram — translucent blobs, refractive gradients, chromatic edges.
5. Blueprint/lab notebook — cyan lines, annotations, scanning reveals, equations/data fragments.
6. Retro terminal but readable — sparse scanlines, large labels, chunky CRT bloom.
7. Kinetic typography — words slide, snap, underline, type-on, explode/reassemble.
8. 3D particle sculpture — orb/DNA/network in a clean product-style frame.

## Claude Code production pattern

For multi-variant animation work, use Claude Code as the design/production lane. Always pass the prompt through stdin, not `"$(cat prompt.md)"`:

```bash
cat > /tmp/animation-lab-prompt.md <<'PROMPT'
<full brief here>
PROMPT

mkdir -p /tmp/animation-lab
cd /tmp/animation-lab
claude --print --input-format text --output-format json \
  --permission-mode acceptEdits \
  < /tmp/animation-lab-prompt.md
```

If running from Hermes, start that command with `terminal(background=true, notify_on_complete=true)`, then use `process.wait`/`process.log` and verify outputs yourself.

## Output standard

For explorations:

- Make separate MP4s, 4-6 seconds each.
- Make one contact sheet PNG with labeled stills.
- Prefer `/tmp/claude-ascii-directions/out/` or `/tmp/animation-lab/out/` unless the user gives a project path.
- Verify each MP4 with `ffprobe`.
- Return the best pick, why, and attach the strongest clips.

For final pieces:

- Combine the best directions into a single coherent film.
- Use actual script/audio timings if available.
- Re-encode for the target surface: landscape, square, or portrait.

## Verification

Before saying it is done, run:

```bash
find <outdir> -maxdepth 1 -type f | sort
for f in <outdir>/*.mp4; do ffprobe -v error -show_entries format=duration,size -of csv=p=0 "$f"; done
file <outdir>/contact_sheet.png
```

Report any limitation plainly, especially if TouchDesigner/twozero is not live because the GUI session is owned by another macOS user.
