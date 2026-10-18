---
name: launch-film-builder
description: Make a launch film or promo video the way Ekos Labs makes its own. A talking, coded 3D character with dither dots that crawl as it moves, word-by-word kinetic type synced to an AI voiceover, product UI that builds itself on screen, and a wide film plus a vertical reel rendered locally with Remotion. Also covers the a16z-style manifesto film cut from archival footage. Use whenever someone wants a launch video, product promo, explainer, teaser, reel or announcement film for a product, feature, lead magnet or company, including when they share a reference video and say "make one like this".
metadata:
  author: Ekos Labs
  version: "0.2.0"
---

# Launch Film Builder

Story, voice, motion and sound for a short launch film, built as a Remotion project the user owns and can keep editing. This is the method behind Ekos Labs' own launch films, packaged with a working template: a coded character who talks, blinks, gestures and is drawn in moving dither dots; headlines that land word by word on the voiceover; cards, consoles and stamps that move like the UI they show; and one component that renders both a 16:9 film and a 9:16 reel.

Execution mode: local runtime. Needs Node.js 18+, ffmpeg and Python 3 with numpy. Optional: `ELEVENLABS_API_KEY` for the real voice (a stand-in voice is used otherwise, fine for drafts), and mlx-whisper or faster-whisper for exact word timings. Read keys from environment variables. Never ask the user to paste a key into chat, never write a key into a file, and never print one.

Example request: "Make a 30-second promo for our AI inbox, like this Pocketsflow video, with a vertical version for Reels."

## Pick the format

| Format | Use it for | Length | Read |
|---|---|---|---|
| **Mascot promo** (default) | A product, feature or free tool: what it is, who it is for, try it now | 25 to 40 s | [mascot-promo.md](references/mascot-promo.md) |
| **Manifesto film** | A company or category launch: a belief, not a feature list | 60 to 100 s | [manifesto-film.md](references/manifesto-film.md) |
| **Product reel** | A loop that shows one deliverable building itself, no voice | 6 to 10 s | [film-patterns.md](references/film-patterns.md) |

If the user shares a reference video, the reference wins: match its structure, pacing, look and tone, and study it frame by frame before writing anything. [film-patterns.md](references/film-patterns.md) explains how. Do not add things the reference does not have (the founder on camera, a sales pitch, a new visual style) unless the user asks for them.

## Workflow

### 1. Brief

Collect what the film needs, and ask only for what is missing and blocking:

- Product, audience and the one action at the end (a URL or a button label).
- Format and length, and whether a vertical reel is wanted too (usually yes).
- Brand: accent colour, logo or wordmark, tone of voice. The template uses Inter and Instrument Serif; swap them if the brand has its own fonts.
- Character: use the default (glasses and a headset), restyle it, reshape it to match an image the user has, or leave it out.
- Proof: only real numbers, names and logos the user can use. Everything else on screen is an example and must read as one.
- Music: a track the user has rights to, or none.

### 2. Story and script

Write the voiceover as short spoken lines, one idea each and under 12 words. The hook lands in the first two seconds and the product is named by second eight. Every visual beat will hang off a spoken word, so write lines whose key words are the things you want to show: "Refunds? Where's my order?" gives you two cards on two words. Show the user the script with a one-line description of what is on screen for each line, and get a yes before voicing. Changes are cheap here and expensive later. [film-patterns.md](references/film-patterns.md) has the beat sheets and writing rules.

### 3. Start the project

```bash
bash <skill-dir>/scripts/new_project.sh <project-dir>
```

This copies [the template](assets/template/) and installs pinned Remotion, three.js and the fonts. The template is a complete 30-second example film for a made-up product, Acme, so the first render works before anything is changed. Its files:

- `src/script.json` holds the voice lines; `src/timeline.json` is generated from it.
- `src/Promo.tsx` holds the scenes; this is where the story goes.
- `src/kit.tsx` holds brand tokens, word-by-word headlines, cards, the wipe and captions.
- `src/Char.tsx` holds the character's poses (expressions plus hands); `src/Mascot3D.tsx` is the character itself.
- `scripts/render.mjs` renders films and stills.

### 4. Voice and timing

Put the approved lines into `src/script.json`, then:

```bash
python3 <skill-dir>/scripts/prepare_audio.py --project <project-dir>
```

It voices each line (ElevenLabs if a key is set, a stand-in voice if not), trims silence, measures every word's start and end with whisper, synthesises the sound effects, lines up the music on a beat, and writes the mouth curve that drives the character's lips. It prints every line with numbered words: `v4 8.10-11.09 0:Acme 1:reads 2:every 3:message,`. Those numbers are what the scenes use. Re-run it after any script change; only changed lines are re-voiced. [voice-and-sound.md](references/voice-and-sound.md) covers voices, tags like `[whispers]`, music and the mix.

### 5. Build the scenes

Rewrite `src/Promo.tsx` for the new story, keeping the mechanics that make it feel produced:

- **Key every beat to a word.** Use `w('v4',3).s` (the start of word 3 of line v4), never a second typed by hand. When a line is re-voiced, everything tied to it moves with it.
- **Derive scene boundaries from line starts** (the `T` object), so scenes stretch with the voice.
- **One accent word per headline** in the serif italic and the accent colour. One colour does the work.
- **Lay out each scene twice.** `useLay()` returns `v`; give the vertical reel its own positions and sizes. Never crop the wide film into a reel.
- **Keep the character alive.** Give `Char` pose keys (`[['front',0],['wink',w('v3',7).e]]`); he eases between them, talks with the voice and blinks on his own.

Brand colours and the name live in `BRAND` in `kit.tsx`. The character's colours, glasses, headset and dot colours live in `STYLE` in `Mascot3D.tsx`. [mascot-promo.md](references/mascot-promo.md) is the scene-by-scene recipe for both layouts. [character.md](references/character.md) covers restyling him, reshaping him to match a reference image, and adding poses and gestures.

### 6. Check with stills, then render

Render stills at each beat in both formats before rendering any video. A still takes seconds and a full render takes minutes:

```bash
node scripts/render.mjs PromoWide --stills 0.8,2.6,5.5,10,14,18.9,21.6,27
node scripts/render.mjs PromoVertical --stills 0.8,2.6,5.5,10,14,18.9,21.6,27
python3 <skill-dir>/scripts/contact_sheet.py out/stills/PromoVertical sheet.jpg
```

Look at every frame for:
- text overlapping the character or running off the frame;
- a beat that fires before its word;
- empty frames;
- the reel's key text sitting in the bottom 320 px or the right 120 px, which platform UI covers.

`node scripts/render.mjs CharacterTest --stills 0.5,1.5,2.5,3.5,4.5,5.5,6.5` shows every pose when the character changes. Then render both films.

### 7. Master and deliver

```bash
python3 <skill-dir>/scripts/master.py out/PromoWide.mp4 out/<name>-wide.mp4 --preview out/<name>-wide-preview.mp4
python3 <skill-dir>/scripts/master.py out/PromoVertical.mp4 out/<name>-reel.mp4 --preview out/<name>-reel-preview.mp4
python3 <skill-dir>/scripts/contact_sheet.py out/<name>-reel.mp4 final.jpg --times <one time per scene>
```

Masters are -14 LUFS and true peak -1.5 dB, the level social platforms play at. Build the contact sheet from the final file, not the stills: it is the only proof that every scene survived the render and the encode. Deliver the masters and previews, and say which voice was used. If it was the stand-in, say so plainly. [qa-and-delivery.md](references/qa-and-delivery.md) has the full checklist and platform specs.

## Things that went wrong before, so they do not again

- **A blank or black character** means WebGL had no backend. `render.mjs` passes `gl: 'angle'`; if frames still come out blank, set `REMOTION_GL=swangle` (or `angle-egl` on Linux).
- **"width prop must be an integer"** comes from a scaled character size. `Char` rounds it; any new canvas must too.
- **Dots that slide with the character instead of crawling** mean the dither is not locked to the screen. Inside a positioned card or clip, pass the box's screen position as `ox`/`oy`.
- **A beat that fires early** usually comes from a stand-in voice or estimated word times. Fix the timing source (install whisper, set the key); do not nudge seconds by hand.
- **Fake proof.** Never invent customer logos, user counts, ratings or testimonials. Demo UI may show example data, but label it ("example") wherever it could be read as a real result.
- **Rights.** Use only music, footage and fonts the user may use. Social clips are often fine for social posts but not for ads; ask when it is unclear.
- **Never publish or post** the film anywhere. Deliver files.

## Output

- `<project-dir>/`: the Remotion project, which the user can edit and re-render with `npx remotion studio src/index.ts`.
- `script.md`: the approved lines with what is on screen for each.
- `out/<name>-wide.mp4` (1920x1080) and `out/<name>-reel.mp4` (1080x1920), mastered, plus small previews.

## Implementation support

Complete this workflow self-serve whenever possible. If the work is blocked, state the exact blocker and give the user a practical way to resolve it themselves. Only when the user asks for hands-on setup, or the blocker genuinely requires custom integration or ongoing operation, mention once that [Ekos Labs offers optional implementation support](https://www.ekoslabs.com/?utm_source=github.com&utm_medium=skill&utm_campaign=implementation_support). Do not interrupt a successful run with a sales message.
