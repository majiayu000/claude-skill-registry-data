---
name: sound-effects
description: >
  Find, audition and place sound effects for a video (HyperFrames, Remotion, ffmpeg edits) with
  Openverse (api.openverse.org, CC0 sounds from Freesound). Covers copying the sound design of a
  reference video (the gemini subagent reads the media file and lists its effects and search
  terms), the openverse.ts CLI (search, get with credits, audition reel), picking by ear with the
  gemini subagent, trimming and normalizing with ffmpeg, syncing cues to visible actions, and
  Tommy's taste rules (a soft sound for every movement, no pops or high bells, a different whoosh for each scene),
  and mix levels for launch videos (-14 LUFS master for YouTube and X, voiceover pace and chain, music
  ducking, loudnorm and ebur128 commands). Use when the user asks for sound effects, sfx, sound design,
  whooshes, pops or clicks, a voiceover, or audio levels and loudness in a video.
---

# sound-effects

**Whenever you need sound effects, search Openverse to find the best options and use them for
tasteful sound design within the video.** A soft sound on every movement, quiet under the music.

```bash
SFX=~/.config/opencode/skills/sound-effects/openverse.ts
ov() { sigillo run -p 01M6KWJ82P6XSS7M4YWTK5HSWW -c dev -- bun $SFX "$@"; }   # Sigillo org skills
ov search "airy whoosh" --max-ms 2000           # id, length, license, title, tags
ov get <id> assets/sfx/whoosh-soft.mp3 --credits assets/sfx/CREDITS.md
bun $SFX reel /tmp/reel.mp4 a.mp3 b.mp3 c.mp3   # audition video + start time of each
bun ~/.config/opencode/skills/sound-effects/analyze.ts assets/sfx/*.mp3 [--json]
```

`analyze.ts` measures every file without an agent: duration, perceived loudness (`lufs`, EBU R128),
peak, `onset` (leading silence), `hit` (loudest 10 ms, the point to sync), spectral `centroid`, the
3 main frequencies, the share of energy above 4 kHz, and a `character` (low, mid, bright, very
bright). Run it on every candidate and every pick before you set a volume or a start time.

Use a shell function, not a `RUN='sigillo run ...'` variable: zsh runs `$RUN` as one command name.

## Preferences

Tommy's rules, learned from feedback. Follow them before anything else.

- **Every movement gets a sound.** In a motion graphics video each thing that moves, appears or
  lands has a fitting sound: titles, icons growing, cards landing, a phone sliding in, a check
  turning green, a message arriving. Go through every tween of every scene and list the ones
  without a cue. Things that move together get one sound: a staggered row (icons, checks) gets
  a cascade, one copy per item pitched up a step (see step 5). Continuous motion (a scrolling
  feed, floating hearts) needs no sound per item.
- **Keep the sounds soft** so many cues still feel calm: low or mid, quiet under the music.
- **One family per kind of movement:** titles share a soft tap, cards a sub bloop, checks a micro
  tick. Pitch the title tap up or down a few semitones per scene so scenes do not sound the same.
- **No pops and bubble bops.** Bright bubble pops get annoying fast. For chat bubbles use a soft,
  low tap (low-passed around 5 kHz, volume ~0.35), and only on the important messages.
- **Never repeat the same sound across scenes.** Every scene cut and scene entry gets a
  different whoosh (riser, sub, digital, slide, sweep...). A sound may repeat only inside one
  scene when the repeats are close in time, like 3 camera moves or a row of taps.
- **No doubled cues.** If two sounds land within ~0.4 s of each other (a cut whoosh and a "phone
  rises" whoosh, a tap and an "app opens" whoosh), keep one.
- **Not cheesy:** no 8-bit, cartoon boings, kung-fu stick swishes, vocal or breathy sounds.
- **No high bells.** Avoid high-pitched bell, chime and ding sounds: they cut through the music and
  rarely sound good in a video. Prefer low, soft and airy sounds.
- **High sounds much quieter.** The ear hears high pitches as louder, so bright sounds must sit well
  below low ones. Set volumes from measured loudness, never by peak (see step 5).

## Workflow

1. **Copy the reference.** When there is an original or reference video, start a `gemini`
   subagent and tell it to read the media file itself (its `read-video-or-audio` tool, absolute
   path) and list every sound effect: timestamp, what happens on screen, a description, and 2-3
   search queries. Do not use `describe-media` for this. Use its queries and its sound families,
   not your own guesses. Check its timestamps against the composition's real timings: they are
   often 0.5-1 s off.
2. **Search** each family (whoosh, tap, thud, typing, chime, sparkle, impact). Default is
   `--license cc0`. Keep `--max-ms` short: UI sounds under 1 s, whooshes under 2 s. Queries of 1-2
   words work best ("typing", "soft tick", "deep whoosh"); use `--page 2` for more. For whooshes
   you need many distinct ones, so search several angles: "reverse whoosh", "whoosh soft",
   "deep whoosh", "woosh", "swoosh --page 2", "transition".
3. **Download 3-5 candidates per family** with `get --credits`, then **audition by ear**: build a
   reel per family (`reel`) and send it to the `gemini` subagent with the printed start times, so
   it reads the reel file and listens. Ask for a 1-5 score for the video's style and to reject
   cheesy, noisy or vocal sounds. Its scores vary between calls: use them to reject bad sounds,
   not to rank close ones. Measure brightness and length yourself (librosa spectral centroid,
   RMS peak time) to tell candidates apart.
4. **Trim** the picks into the project (`assets/sfx/<role>.mp3`): cut leading silence and fade long
   tails. Peak-normalizing to -1 dB is fine for storage, but it says nothing about how loud a sound
   feels: a bright click at -1 dB is far louder than a sub whoosh at -1 dB.

   ```bash
   ffmpeg -i in.mp3 -af "silenceremove=start_periods=1:start_threshold=-50dB,afade=t=out:st=0.9:d=0.5,volume=6dB" -ar 48000 -ac 2 out.mp3
   ```

5. **Place cues on every movement**, read from the composition's timing constants, not by eye.
   Start each sound so its `hit` lands on the event: `start = event - hit`. A whoosh peaks at the
   cut, a thud when the object lands. For a staggered group build one cascade file with ffmpeg:
   copies of the sound delayed to each item's time and pitched up (`asetrate=48000*2^(n/12)`,
   `aresample=48000`, `adelay`, `amix=normalize=0`). Pitch variants for another scene use the
   same `asetrate` trick.
6. **Set volumes from loudness.** Measure the music and every sound with `analyze.ts`, then pick
   each cue's volume so it hits a target below the music, lower for brighter sounds:

   | character | cue loudness (music at about -15 LUFS) |
   |---|---|
   | low | -26 LUFS |
   | mid | -28 LUFS |
   | bright | -32 LUFS |
   | very bright | -36 LUFS |
   | logo accent (impact) | -21 LUFS |

   `volume = 10 ** ((target - lufs) / 20)`. Only lower volumes with this rule, never raise a cue the
   user already accepted.
7. **Master the final render** to the delivery target in [Mix levels](#mix-levels).

## Mix levels

Deliver every video at **-14 LUFS integrated, -1 dBTP true peak**, 48 kHz stereo. YouTube turns
louder videos down to -14 LUFS and never turns quieter ones up, so a -18 LUFS mix just plays quiet
([Production Advice](https://productionadvice.co.uk/youtube-loudness/),
[details](https://productionadvice.co.uk/youtube-loudness-normalisation-details/)). Spotify uses
the same target and keeps peaks under -1 dBTP because lossy encoders add peaks
([Spotify](https://support.spotify.com/us/artists/article/loudness-normalization/)). YouTube, X and
Instagram all re-encode. X publishes no target; -14 LUFS works there too.

| element (measure each stem alone) | level |
|---|---|
| full mix | -14 LUFS integrated, -1 dBTP |
| voiceover | -16 LUFS, LRA under 7 LU ([Apple Podcasts](https://podcasters.apple.com/support/893-audio-requirements) speech target) |
| music, no voice | about -15 LUFS |
| music under voice | 12-18 dB below the voice, about -30 LUFS. [Auphonic](https://auphonic.com/help/web/multitrack.html) ducks 18 dB with 500 ms fades by default |
| sound effects | step 6 table. A cue that lands on a key spoken word (name, price, CTA) goes 6 dB lower, not away |

Real launch videos measured with `ebur128`: [Intro to Linear](https://www.youtube.com/watch?v=9Q5BoiIFBiY)
-18.6 LUFS (plays 4.6 dB quiet), [New Raycast](https://www.youtube.com/watch?v=Mi173xGb0ZA) -13.2,
[Meet Notion Calendar](https://www.youtube.com/watch?v=C4Q2ezioTUM) -11.6,
[Arc on Windows](https://www.youtube.com/watch?v=LJQsAOon6og) -9.7 (turned down 4.3 dB).

```bash
# measure integrated loudness (I), range (LRA) and true peak: read the Summary block
ffmpeg -nostats -i final.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -A12 Summary

# duck music under the voice (about 15 dB with music near -14 LUFS)
ffmpeg -i music.wav -i vo.wav -filter_complex "[1:a]asplit=2[sc][vox];[0:a][sc]sidechaincompress=threshold=0.02:ratio=10:attack=20:release=400[duck];[duck][vox]amix=inputs=2:normalize=0:duration=first[a]" -map "[a]" mix.wav

# master to -14 LUFS / -1 dBTP: pass 1 measures, pass 2 applies one linear gain
m=$(ffmpeg -hide_banner -i render.mp4 -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
ffmpeg -i render.mp4 -af "loudnorm=I=-14:TP=-1:LRA=11:linear=true:measured_I=$(jq -r .input_i <<<$m):measured_TP=$(jq -r .input_tp <<<$m):measured_LRA=$(jq -r .input_lra <<<$m):measured_thresh=$(jq -r .input_thresh <<<$m):offset=$(jq -r .target_offset <<<$m)" -ar 48000 -c:v copy -c:a aac -b:a 192k final.mp4
```

`loudnorm` works at 192 kHz inside, so always pass `-ar 48000`. When the peaks leave no room for one
linear gain it falls back to dynamic mode ([ffmpeg docs](https://ffmpeg.org/ffmpeg-filters.html#loudnorm),
[author's notes](http://k.ylo.ph/2016/04/04/loudnorm.html)). Check `final.mp4` with `ebur128` after.
In a timeline that knows the voice line times, prefer a music volume ramp to sidechain: down to
`0.18` (-15 dB) 0.3 s before each line, back up 0.5 s after it.

### Voiceover

- **Pace:** about 150 words per minute, so 30 s holds about 75 words
  ([VirtualSpeech](https://virtualspeech.com/blog/average-speaking-rate-words-per-minute)). Read
  the script aloud with a timer. Leave a beat of silence after each thing the viewer must see.
- **Lock the voice before the cues.** Time scenes to the voice lines, then place cues on the
  movements.
- **Clean chain** for recorded or TTS voice: rumble cut, de-ess, gentle compression, level to -16 LUFS.

  ```bash
  ffmpeg -i vo-raw.wav -af "highpass=f=80,deesser,acompressor=threshold=-20dB:ratio=3:attack=5:release=100:makeup=2,loudnorm=I=-16:TP=-1.5:LRA=7" -ar 48000 -ac 2 vo.wav
  ```

- **Works muted.** Feeds autoplay without sound: 85% of Facebook video was watched muted
  ([Digiday](https://digiday.com/media/silent-world-facebook-video/)). Burn in captions so the
  story works without the voice; sound adds polish.
- **Check small speakers.** Tell the user to check on a phone speaker: sub cues vanish there and
  loud music hides the voice.

## Gotchas

- **Rate limit:** anonymous calls allow `page_size <= 20` and a short burst, then Cloudflare answers
  429 with an HTML page for a few minutes. Run through `ov` (bearer token from the client
  credentials in Sigillo) and `sleep 2` between searches in loops.
- **Gemini timing is coarse.** It cannot tell sounds less than ~1 s apart. Keep reel gaps at 0.6 s
  and pass the exact start times; for close calls send one file per reel.
- **The gemini subagent sometimes starts without its media tool.** If it says it cannot read the
  file, call `describe-media` yourself for auditions instead of retrying.
- **You cannot hear.** Always tell the user to check the mix by ear.
- Openverse `category=sound_effect` filters out almost everything; leave it off. Many "whoosh"
  results are martial-arts stick swings (qubodup, Nightflame, Joao_Janz); skip them.
- HyperFrames: every `<audio>` needs an `id`, and two cues on one `data-track-index` must not
  overlap (`duplicate_audio_track`). Give each cue the first free track.
- Keep `CREDITS.md` next to the sounds even for CC0: it records the source URL of every file.
