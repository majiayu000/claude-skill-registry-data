---
name: motion-video
description: Use when asked for a launch video, product video, explainer, product tour, showreel, social cut, motion ad, product demo, screencast, app preview, animated infographic, product reveal, sizzle reel, kinetic typography, Swiss-style or morphing animation, or any motion graphics video, or when building, rendering or fixing a film in a Motiontale workspace.
---

# Motion video

ENGINE is `../../engine/` from this file (film.py, voice.py, kit.py, motion.js, render.py). WORKSPACE is the folder with `kit/AUDIO.md` and a Python venv with engine/requirements.txt installed; films live at `WORKSPACE/<slug>/`. `PY` is that venv's python. Every command below is run from WORKSPACE. No WORKSPACE yet (no `kit/AUDIO.md` here or above)? Offer to set one up in the folder the user names, and once they agree run `bash ../../script/setup` (the plugin's `script/setup`, two folders above this file) from that folder: it installs the locked engine and its browser into `.venv`, downloads the sound library, copies `.env.example` to `.env`, and ends with `doctor`.

## Hard rules: break none, ask instead
1. Real UI only. Every product pixel is a screenshot or crop of the real page. Never redraw UI. Need a state the pages don't have? Edit the real page and screenshot it.
2. No invented numbers, names, prices, quotes or logos. Only the pages or the intake. A protagonist is a role, not a made-up person.
3. Every frame is a pure function of time: index.html uses motion.js and `studio(draw)`. No CSS animations, transitions, timers, requestAnimationFrame, Math.random, or state kept between frames.
4. Every time lives in timeline.js, in beats. Picture and sound read it.
5. Music and effects are real recordings from kit/audio. Never synthesize them. Voice is a human take unless the intake picked TTS; a TTS voice is named as AI on the post.
6. kit/ and other films are read-only. Write only inside `<slug>/`.
7. No crossfades, glows, particles, 3D, gradients on UI, or the banned defaults in CLAUDE.template.md.
8. Every number on screen has a facts.md row (fact with source, or example shown labelled "Example").
9. No video is shown as finished (the brief's stills and animatic are previews) until `film.py check` passes and the scored critique in checks.md has every score at 8 or more, or 3 rounds are done.

## Brief first
Run the motion-brief skill: it interviews once, writes `BRIEF.md`, `facts.md` and `shotlist.md`, and stops for approval after the shotlist and after the stills. Films over about 90 s, or needing several agents, or expected to run over an hour: hand the whole production to the motion-director skill instead of the pipeline below.

## Pipeline
1. **Film.** `PY ENGINE/film.py new <slug>` (`--size 1080x1920` or `1080x1080` for a vertical or square first cut): it copies the template, the fonts and CLAUDE.template.md as `<slug>/CLAUDE.md`. Paste the style card under `# Look` and set the voice line.
2. **Capture.** Run the motion-capture skill: real pages and elements by selector at 2x into `shots/`, `crops.js`, `provenance.json`, and `facts.suggested.md` to complete `facts.md`. Sound: read kit/AUDIO.md. `PY ENGINE/kit.py` rebuilds the whole kit from its fixed lists (downloads, then measures BPM, downbeat, drop and peaks); a new sound means adding it to those lists and rebuilding, never editing kit/ by hand.
3. **Look.** From each reference take one frame a second (`ffmpeg -i ref.mp4 -vf fps=1 ref_%03d.png`) and copy its grammar (pacing, type scale, entries, camera), never its words, colours or layouts.
4. **Voice** (narrated styles). Write `<slug>/script.md`, then `PY ENGINE/voice.py cut <slug>` (add `--tts` only if the brief chose it) and `PY ENGINE/voice.py place <slug>`. See scenes/voiceover-sync.md.
5. **Scenes.** A film one builder makes (up to about 90 s): write each scene from `scenes/<scene>.md` straight into `<slug>/index.html`, one timeline, so a fix lands once. Longer, or several agents: one clip per technique in `<slug>/clips/<scene>/` (`film.py new` it), each by its own agent (Claude: motion-scene-builder; Codex: motion_scene_builder) in parallel; with 3+ agents first write `<slug>/ANIMATION_GUIDE.md` (helpers, spring presets, type sizes, colour use). Animatic first: `PY ENGINE/film.py render <clip> --animatic`, the contact sheet and the scored critique (checks.md), fix pacing, then polish.
6. **Film.** With clips, join them on one timeline in `<slug>/index.html`: reuse each clip's draw code, every handoff through a shared shape, payoff on the music drop (`music.payoffCue`; film.py starts the track so its drop lands there, or write `music.bars`). Trim by whole beats, never stretch time. Add `asserts` to timeline.js for the moments that must happen (checks.md, asserts).
7. **Render.** `python3 ENGINE/lint.py <slug>` shows no blocking line (motion-review explains each; every number on screen needs a facts.md row). Then `PY ENGINE/film.py mix <slug> && PY ENGINE/film.py check <slug> contact layout determinism`, fix the three worst problems, then `PY ENGINE/film.py render <slug>` (blur samples double with motion, up to 64; `--shutter 180` for a crisper look). `--from F --to F` renders just those frames to `part_F-T.mp4` to preview a fix; ship only a full render. Sound-only notes: `film.py mix` then `film.py mux`, no re-render.
8. **Check.** `PY ENGINE/film.py check <slug>` and the scored critique in checks.md, or hand the film to the critic agent (Claude: motion-critic; Codex: motion_critic).
9. **Formats.** Same timeline, reframed by FMT/pick() in the page: `SIZE=1080x1080` or `SIZE=1080x1920` before render and check. Never crop.
10. **Deliver.** `PY ENGINE/film.py export <slug>` (captions from the voice lines, or from timeline.js `"captions": [{"at": cue, "text"}]` when there's no voice, which the page draws from too; chapters only when YouTube will use them: 3 or more, each 10 s or more; poster, GIF) and `PY ENGINE/film.py replay <slug>` (proves the recipe rebuilds every frame). Frame one states the pain or opens on the payoff; the film works muted; TTS is named as AI.
11. **Report.** Fixed (with the check that now passes), still change (worst first), listen for (beats a human must hear).

## Effort
Medium for notes and re-renders. xhigh for a new film. max only when the first 3 seconds carry a launch.

## Notes from the user
A note is a problem plus the result wanted. Read the clip's "what I'd still change" list first. Fix in the clip, re-render the clip, then the film.

## Known limits
You can't hear: a human listens to every mix. Checks catch only what they measure: when a note repeats, add a check. Moves over about 120 px a frame step even at 64 samples: slow them. Real data rarely lines up: seed it. Runs are slow: parallel clips, `--workers`, animatic before full renders.

## Extending
New style or scene technique: use the motion-extend skill. Brief: motion-brief. Real UI: motion-capture. Long or multi-agent runs: motion-director. Source review of one film: motion-review. The whole workspace (stale renders, unchecked films, drift, licences, clutter): motion-audit. Styles are discovered from styles/*.md, so nothing here needs editing.

