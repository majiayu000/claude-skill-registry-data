---
name: video-moves
description: >-
  Camera and editing grammar for any code-built video (HyperFrames) - ads, launch films, UI
  walkthroughs, illustrated scenes. 24 moves (pan, tilt, dolly, zoom, tracking, orbit, crane,
  dolly zoom, rack focus, handheld, FPV, dutch angle, slow motion, speed ramp, time-lapse, freeze
  frame, jump cut, match cut, whip pan, dissolve, wipe, smash cut, J-cut, L-cut): when to use
  each, how to stage it on the film's own material, numbers, traps, sound, and working code
  (camera-kit.js rigs, story time for picture and sound, synthesised move sounds). An executor
  under video-studio, whose laws still apply. Use when a film needs more than hard cuts, a move is
  named, or video-studio picks a hook, a transition or a signature moment. Triggers: "camera
  move", "make a transition", "push in", "dolly zoom", "match cut", "speed ramp", "slow motion",
  "freeze frame", "whip pan", "how to cut this".
---

# video-moves

The grammar of the camera and the cut for any HyperFrames film: an ad, a launch film for a
product or a side project, a walkthrough, an illustrated or abstract scene. Nothing here is
tied to one brand or one piece of material: moves are described in roles (subject, near
props, background, shot A / shot B), the code takes any DOM content, and the styles use
neutral `--mv-*` colour tokens that each film sets from its own material (the colours of
what is being edited - not a brand).

It came from the "24 camera and editing moves" guide (see THIRD_PARTY_NOTICES.md), ported from
Three.js to DOM rigs and tested move by move on a 77 s test reel that staged all 24 on one
recorded video call. Each new film stages the moves on its own material.

**Input: the film's `brief.md`** (`../video-studio/references/brief.md`). It owns copy, claims,
tone, material, moments and private data; this skill owns the implementation. If the brief
cannot be met, say so to video-studio - never change it silently.

video-studio orchestrates the film (format, laws, order of work); video-sound, video-build and
video-check do sound, building and gates. This skill owns the moves: which one, how to stage
it so it reads, the code, and its sound. video-studio's house laws apply to every film, and
your brand laws to your brand's films. When a rule here and a law disagree, the law wins.

**Setup.** What video-build needs (HyperFrames CLI, Node 22+, FFmpeg). For the move sounds:
the sound library's Python venv, installed by `../video-sound/scripts/library.py install`.

## 1. Pick the move by meaning

Every move needs a finished "the camera moves because...". No reason = no move.

| The film needs | Take |
|---|---|
| a hook in the first second | smash cut, crash zoom, dolly zoom |
| the subject close, the key element | dolly in (we come closer), zoom (a sharp accent) |
| scale: one of many, the whole picture | crane up, tilt, pull-out to a grid |
| speed, a process running | tracking, FPV, whip pan |
| the peak of the action, the promise | speed ramp into slow motion, freeze frame on the peak |
| time has passed | time-lapse, jump cut, dissolve |
| two scenes are one idea | match cut, J-cut, L-cut |
| a problem, confusion | dutch angle, handheld |
| the finale | orbit, crane, dissolve into the end card |
| cause here, effect there | whip pan across one world |

Rhythm: main cuts are hard. Effect transitions (whip, dissolve, wipe) go in 2-3 key places
only. One move per shot. A move starts 0.1-0.3 s after its cut and an important frame holds
at least 1 s after the move lands.

Full catalogue - what each move tells the viewer, how to stage it, its numbers, what must be
visible for it to read, its traps and its sound: `references/moves.md`. Read the entries for
the moves you pick, not the whole file.

## 2. Build it

`references/rigs.md` is the build manual. Its section 0 is a complete two-scene film (a pan and
a dolly in) that builds and renders with the files below as they are - start there. The shape:

1. **One pure render function.** A single linear driver tween on the paused GSAP timeline
   calls `render(t)`; each scene is a HyperFrames clip with an `IMPL[id](root, scene)`
   whose `frame(u)` writes every transform from local time `u` alone. Nothing reads the
   clock, `Math.random` or the layout per frame.
2. **Rigs from `scripts/camera-kit.js`** (inline it into the composition):
   `lens2d` (pan, tilt, zoom, roll, shake, whip - no parallax) and `pose3d` on a CSS 3D
   world under a static-perspective stage (dolly, orbit, crane, tracking, FPV; dolly zoom
   animates the perspective, which is the focal length).
3. **Story time** for slow motion, speed ramp and freeze: one rate curve per scene
   (`piecewiseRate` → `makeStoryTime`), written to `scenes.json` so the picture and
   `scripts/move_audio.py` read the same curve. Words, the voice, a scope - everything in
   the world - live in story time; the camera and the cut live in real time.
4. **Styles and scaffold** to copy into a project: `assets/moves.css` (rigs, label,
   readout pill, voice scope, edit strip, focus brackets, freeze border, scene dip; colours
   are `--mv-*` tokens - set them per film from the film's own palette) and `assets/scaffold.js`
   (scene loop, `show()`, label timing, 3+3-frame dip, driver tween; its example `IMPL`
   entries are placeholders you replace with the film's scenes).
5. **The code for each rig** - 2D lens, CSS 3D world, story time, A/B transitions, overlays -
   is in `references/rigs.md` sections 2-6, with the numbers from `moves.md`.

## 3. Give it sound

`references/sound.md`: the sound of each move (whoosh with a rising band for the whip,
tone 110 → 520 Hz for the dolly zoom, tape stop for the ramp, silence and a 1760 Hz ring
for the freeze, the hit on the cut frame for the smash), story-time varispeed of a real
recording, J/L-cuts measured from the recording's first word, and the loudness traps.
Synths and helpers: `scripts/move_audio.py`, run with the library venv:

```bash
"${VIDEO_LIBRARY:-$HOME/.local/share/marketing-agent-kit/video-library}/tools/.venv/bin/python" \
  ${CLAUDE_SKILL_DIR}/scripts/move_audio.py --demo /tmp/move-sounds   # every synth, for listening
```

A film's own audio script imports it (`import move_audio as ma`); mix with video-sound's
`scripts/mix.py`.

## 4. Check that the move reads

Before the full render, stills at the start, middle and landing of every move, and
either side of every cut (video-check `scripts/stills.py`). For each move ask the
question from its entry in `moves.md` - "does the foreground pass by (dolly) or get
cropped (zoom)?", "does something visibly slow down?" - a move that needs explaining
does not work. Then video-check's gates and independent review as usual.

## 5. Generated shots (Atlas)

A model is told the move in words: `references/prompts.md` has the English camera terms
and one prompt line per move. One move per generated shot; cuts inside one generation are
unreliable - generate two shots and cut them in HyperFrames.

## 6. When something new is learned

A move used in a real film and approved by the user: note it in its `moves.md` entry
("Proven in: <film>") and, if it changes how films are made, in `../video-studio/references/laws.md`. A move
rejected: write why in its entry and as a rule against it in `laws.md`. Code fixes go into
`scripts/` and `assets/`; re-run the section 0 example in `rigs.md` so it keeps rendering.
Note what changed in the film's own notes; for changes to the skill itself, open a PR
(CONTRIBUTING.md).

## Adapt it

- Set the `--mv-*` tokens per film from that film's own material, after `moves.css`; the
  defaults are neutral placeholders.
- Keep a project of your own that uses the moves on your material (start from `rigs.md`
  section 0) as your house example.
- Add "Proven in: <film>" or a rejection note to `moves.md` as your films use the moves.
- Swap the Kenney sounds in `move_audio.py` (`KENNEY` map) for sounds from your own library.
- Add prompt lines that worked on your video model to `references/prompts.md`, with the date.
