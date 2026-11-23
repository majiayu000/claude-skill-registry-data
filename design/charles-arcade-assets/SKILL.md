---
name: charles-arcade-assets
description: "Make retro pixel-art, video-game style motion design timed to a voiceover, on any topic - a flat pixel mascot (or a cast made for the topic) acting out every line, pixel scenes, rebuilt app UI and the real pages, logos, covers and photos the words name, with counters, charts, stamps and hand-drawn marks landing on the word - rendered to video with HyperFrames from generated art (fal) and code. Use whenever Charles asks for \"arcade\", game-style, pixel, retro, opusjake-style or \"fun\" motion graphics or animations, for parts of a video he is editing (often from charles-claude-editing, which picks the layout and asks for an asset at that size: a 2:1 card above his face, a tall card, a split panel, an overlay or a new screen), or for a whole voiceover or reel."
---

# Goal

Every idea in the voiceover becomes a playful, literal moment: the mascot doing it in a cute 16-bit game, the
product UI doing exactly what is said, or the real thing (the page, the logo, the book, the person), landing on
the word. Something new is on screen about every second and something moves inside it every few frames. It
should look like a polished indie game and a clean product demo, never like AI slop: crisp pixels, one
consistent look and cast, real things shown as they are, exact text, deliberate motion.

`T` below is this skill's folder (`skills/charles-arcade-assets`); run commands from the repo root unless noted. Write
commands out in full: zsh does not split a variable such as `F="python3 x.py"` into a command and its arguments.

# What you are making

| Ask | Output |
|---|---|
| **Asset** (from charles-claude-editing or "animate this part"): a time range of a video and a size | one file at exactly that size and the part's length, no audio: `.mp4`, or a transparent `.webm` when it goes over footage as an overlay. Plus `sfx.json` (see Making an asset for charles-claude-editing) |
| **Asset set**: several time ranges at one size (every card moment of a video) | one file at that size covering the whole span; see Making an asset for charles-claude-editing |
| **Reel**: a whole voiceover or audio track | one 1080x1920 `.mp4` with the audio, full-screen visuals for every second |
| **Several sizes** for one video (a card, a tall card and a full screen) | one file per size, each an asset or asset set as above, made as one set (`new_project.py --set`) so every size shares one cast and look |

Captions and music are not yours: charles-claude-editing adds them. Never burn the voiceover's words in as captions; short
labels, titles, UI text and HUD text are part of the visuals.

**Sizes.** Make the asset at the size you are asked for. Where it goes on screen is charles-claude-editing's call, not yours;
make the best asset for that frame. Common sizes:
- a 2:1 card above Charles' face, like @opusjake's: render 1280x630 (charles-claude-editing shows it about 900x442 and adds
  the rounded corners, the shadow and the cream band, so fill the frame edge to edge and keep key content
  40 px clear of the corners)
- a tall card that covers his face: 1280x1550
- 1080x1920 for a new full screen; 1080x960 and 1080x768 for split panels; an overlay's own size

charles-claude-editing puts its captions on top of your asset: a pill at about y 1380-1465 on a full 1080x1920 screen, under
a tall card, and on the seam (the asset's top or bottom edge) in a split. Keep y 1360-1480 of a full screen free
of anything the viewer must see: no labels, faces or key props under it.
Blueprints come in four layouts: wide (laid out at 1280x630), tall card (1280x1550), short (1080x960) and tall
(1080x1920);
`mount.py` copies the one that fits the project's shape and says when a scene needs re-laying out. Keep text
inside the area you are given (a full 1080x1920 screen keeps it between y 250 and y 1450, x 80-1000; other
sizes at least 40-60 px from every edge). Art and backgrounds fill the whole frame. Text size is about what the
phone shows; `reference/build.md` has the rule.

# Setup (once per machine)

- `node` 22+, `ffmpeg`, `python3`, Google Chrome (for page captures). HyperFrames runs through
  `npx --yes hyperframes@0.8.217` (written `hf`).
- The repo venv for sprite tools: `python3 -m venv .venv && .venv/bin/pip install pillow numpy`.
- `FAL_KEY` in the repo's `.env` (`tools/fal.py` finds it).
- The sprite library (the `claude` and `gpt` characters and `props/`) isn't part of the public skill. Charles' lives
  in claude-editing at `assets/arcade-cast/`; `tools/new_project.py` finds it there, or wherever `ARCADE_CAST`
  points. Below, `cast/` means that library.

# Workflow

Work inside the video's `videos/<video>/graphics/<name>/` folder. Source and notes are tracked; footage,
captures, and renders stay local. Read `reference/metaphors.md` before planning, `reference/art.md` before
generating, `reference/build.md` before writing scenes, and the kit reference for what you use:
`reference/critter.md` (the mascot, its roles and props), `reference/cast.md` (generated characters as actors,
the tier list, the loot bar, book and author reveals), `reference/motion.md` (camera, transitions, physical
gags), `reference/ui-claude.md` and `reference/ui-web.md` (rebuilt apps), `reference/annotate.md` (marker marks,
stamps, counters, charts). Historical `work/kit-*` demos mentioned in the references are not bundled here;
start from the included `blueprints/` and `template/` files.

1. **Project.** `python3 $T/tools/new_project.py videos/<video>/graphics/<name> --audio <voice file>` for a reel. For an asset, see
   Making an asset for charles-claude-editing: no `--audio`, and `--size` at the size asked for.
2. **Words.** In the project (for a set of sizes, in the set's folder): `hf transcribe assets/voice.m4a -d . --json`.
   From the repo root, run `.venv/bin/python $T/tools/onsets.py videos/<video>/graphics/<name>/transcript.json
   videos/<video>/graphics/<name>/assets/voice.m4a`. Then run `python3 $T/tools/words.py transcript.json`. Proofread names against
   the context (Whisper writes "Chat GBT" for ChatGPT, turns product names and comment keywords into common words
   that sound alike) and fix them in `transcript.json`. Put every name and keyword the video shows in
   `assets/names.js` (`NAMES`, used with `data-name`) and the running example's numbers in the same file
   (`FACTS`, used with `data-fact`). When a name stays ambiguous and Charles is not around, take the reading that
   fits the topic and name it in the handover; fixing it is then a one-line change. onsets.py moves the first word
   after each pause to where its sound begins (recognisers start those 0.2-0.4 s off) and keeps the original as
   `transcript.raw.json`. Words inside a phrase drift too, by 0.1-0.25 s: early into the word before ("the
   paywall"), late onto their own second syllable at a phrase end ("aha moment"). Run the same command with
   `--check --strip review/words.png`: it lists every word more than 0.1 s from where its sound starts, with that
   time, moves nothing, and draws each one (red: the transcript's start, green: where the sound starts). Move the
   ones the strip confirms with `--move paywall,aha`, or your own time read off the strip (`--move moment=29.22`);
   look before moving a "less sure" one. A hit must land on its word: once the beat sheet names its key words, run
   `--check --words <them> --strip review/keys.png` and settle every one ("not paired" means judge it on the
   strip). `python3 $T/tools/words.py transcript.json --strip review/w.png --from 27.3 --to 29.6` draws any
   stretch. On fast conversational speech most flags are "less sure": check only the hit words there.
   `hf transcribe` uses Parakeet once it is installed (`hf models list`), else Whisper small.en. Parakeet's timing
   is best after onsets.py, but it writes numbers wrong ("ten out of ten" came out "10 out of 1."), so proofread
   numbers too.
3. **Cast and worlds.** Decide who acts and where (`reference/metaphors.md`, "Cast for the topic"). For Claude
   and AI-tool videos the mascot is the code-drawn Claude critter (`critter.js`), in a different role per idea
   with props from the library (`cast/props`); ChatGPT is the `gpt` sprite. For any other topic, keep a host
   (the pal, the critter's neutral cousin drawn in code, or Charles as a pixel character from a photo) and add
   one to three characters for the topic's ideas (the enemy, the reward, the rival) with `tools/cast.py new`. Pick the two to four worlds the
   video keeps returning to.
4. **Real things.** List every real product, site, app, book, person and number the voiceover names, and fetch
   them with `tools/source.py`: page captures, App Store icons and screenshots (references for rebuilt screens),
   logos, book covers at full size, photos of people with their credit. Real people
   and brands are always real images (photos keep their credit line on screen), never generated.
5. **Beat sheet.** Write `beats.md`: one row per beat with start-end (from word times), the words, the visual
   (what literally happens on screen, and who causes it), the world, the blueprint or "custom", the assets it
   needs, and the key moment's time. Rules in `reference/metaphors.md`; in short:
   - frame 0 is the hook: the first line as a visual joke, already on screen and already moving, usually the
     mascot causing it; its key change lands on the first stressed word (within ~0.7 s), not a second later;
   - shots of 0.4-1.6 s, median 0.8-1.0 s; one idea each; contiguous, covering every second; most shots get a
     new scene (a new plate, a cut-in on a detail, a re-frame), not just new text. Plan at clause level: every
     noun, number, app and person the voice names is an event, two to four events per shot, each landing on its
     word (a line types, a counter ticks, a stamp lands, the mascot acts). A rebuilt app the voice walks through
     (paste, type, send) can run 3-4 s if something changes every ~0.3 s;
   - the mascot causes things in about two thirds of the beats: it pulls, presses, throws, stamps, carries,
     rides, and the scene reacts. It is never just standing next to the content;
   - one running example (a question, a trade, a price, an app being cloned) carried through every beat that can
     show it, with the same exact numbers from `FACTS`;
   - mix pixel scenes, rebuilt UI and real pages; never the same blueprint twice in a row;
   - every number said becomes a counter, the biggest thing in its frame (with its source under it when it is a
     fact); every app step becomes the UI doing it; every real name shows the real thing; when the voice says
     what a tool does, a beat shows that tool doing it, after any metaphor for it; the CTA ("follow and comment
     X") is the `cta-follow` card;
   - a tool or skill launch follows the segment format in `reference/metaphors.md`.
   If Charles is around and did not say to just do it, show him the beat sheet before generating art.
6. **Art.** Generate every scene plate, character, prop and missing pose (`reference/art.md` has the exact
   prompt blocks and commands; check `cast/props` first). Plates with screens get flat green screens so live UI
   can play inside them. Run the independent `fal.py` calls in parallel. Open every image, reject and regenerate
   the failures, key the sprites, and check them on the review sheet. Generated video only for one or two hero
   moments.
7. **Scenes.** Fill `beats.json` (`{"duration": <audio length>, "beats": [{"id": "b01", "start": 0, "dur": 1.0,
   "blueprint": "hook-gag"}, ...]}`), run `python3 $T/tools/mount.py videos/<video>/graphics/<name>`, then edit each
   `compositions/<id>.html`: copy, images, layout, and the `T` times (word time minus beat start). Custom
   scenes follow the skeleton in `reference/build.md`. Use the kit's helpers rather than raw tweens. A beat's
   first frame is its finished world, locked: no settle, no drift, never popping or fading in from an empty
   stage (`AR.settle` at 0 just makes it visible). The camera moves only when the story moves it: cut-ins on the
   same plate to escalate (1.0, 1.25, 2.0x), a push onto what fills or matters, a pull-back to reveal the whole
   app, a shake on a hit.
8. **Check.** In the project: `hf check --json`. Fix every error and every runtime warning ("GSAP target not
   found" means a broken selector). Fix layout warnings (overlaps, key text too small). These are fine:
   `duplicate_media_discovery_risk` (a reused image), `film_silent` (an asset without audio), `dead_stretch`,
   `subcomposition_blanks` and `first_frame_empty` on the hold beats of an asset set, reading-time
   warnings for text the voice is saying, that types on screen or that carries over from the beat before,
   small-text warnings (`text_below_floor`) on secondary UI text (build.md, Text size), and contrast warnings on placeholder text in
   a rebuilt app (it is grey in the real app too) or on things dimmed on purpose (the others in a spotlight). Name
   fonts only through the kit's classes and variables: a `font-family` naming a pixel font in a scene's own style
   fails the lint. Blueprints carry example names: `grep -rn "Charles Liu\|scout-skill\|Good afternoon"
   compositions/` and replace any left over with this video's names (from `names.js`).
9. **Review.** `hf snapshot --at <each beat's key moment + 0.15> --no-end -o review/` and look at the contact
   sheet, then at single frames where anything is doubtful. Then `hf snapshot --review -o review/cuts/` and
   check that every cut lands on a complete frame. Go through the checklist below, fix, repeat. Do not render
   before the stills pass. After the render, run `.venv/bin/python $T/tools/qa.py out/<name>.mp4` (with
   `--ranges 2.0-3.0,5.3-7.0` for an asset set) and fix every flash, blink and edge it reports; a sparse or
   still span stays only if it is meant (the last beat, a page being read). Then hunt what it cannot see with
   12 fps strips (`ffmpeg -ss <t-0.3> -t 0.8 -i out/<name>.mp4 -vf "fps=12,scale=420:-2,tile=5x2" ...`) around
   every cut and every key word: a sprite clipped by a floor or a card edge, parts of a sprite coming apart or
   see-through, ghost rows while a list scrolls, text clipped at a container's edge, a piece of the next scene
   showing at an edge, a change that appears less than 0.3 s before a cut (it reads as a flicker: move it or
   the cut), a flip or stamp that lands before its word.
10. **Render.** `hf render -o out/<name>.mp4`, or `--format webm` for a transparent overlay, in the background
    (a 22 s reel renders in about 15 s). Then make a 4 fps contact sheet of the render (`ffmpeg -i
    out/<name>.mp4 -vf "fps=4,scale=270:-2,tile=8x4" ...`) for motion and variety, and check sync on exact
    frames (`ffmpeg -ss <word time> -i out/<name>.mp4 -frames:v 1 ...`): the sheet's samples drift by a frame.
11. **Hand over.** The file path(s), the beat sheet in two lines per beat, the fal cost total from the
    `costs.jsonl` files, the credit lines of any photos, and anything you were unsure about.

# Review checklist

For every beat:
- **Literal:** a muted viewer would understand what is being said from this frame alone.
- **On the word:** the key change lands within ±0.1 s of its word; nothing waits for a word already gone. Text
  that types starts on its word and is complete by the word's end; a stamp lands on its word, not after it.
- **Alive:** something moves at least every 0.4 s; no hold over 1 s except the last beat or a page being read,
  and no still of more than about 0.5 s waiting for a reveal. Nothing glides in a straight line for more than
  0.5 s: it hops, steps or snaps. The last beat ends on motion (the plane flies off, the stamp lands).
- **Actor:** where the mascot is on screen, it causes the change, and the scene reacts to it.
- **Real:** a product, site, book or person the voiceover names shows the real thing.
- **Cut:** its first frame already shows its finished world, locked; nothing builds up from an empty stage and
  nothing drifts; every camera move has a reason.
- **Exact text:** spelled right, matches the voiceover's numbers and names, the key text big enough on the phone
  (build.md), inside the frame's text zone, nothing overlapping or cut off. A number the video shows twice shows
  the same value both times (take it from `FACTS`); a grid of labels stays readable on a phone (fewer, bigger
  tiles beat many tiny ones). A real page, table or document the voice points at is cropped and zoomed to the
  rows that matter, never a whole page shrunk into the card with most of the frame blank. What the beat is about
  fills the frame: no wide shot of tiny actors, no app window whose text is under the size rule as the subject,
  and no full screen or tall card that is mostly empty (a lone small mascot on a blank card).
- **Composed:** nothing pokes out of the thing it sits on (a card wider than the phone behind it, a label wider
  than its tombstone), no empty card waiting for its content, no stray element from another beat. No prop or
  character covers the key text (a hat falling across the repo name). An idle pane is dimmed lightly, never
  covered by a flat grey slab.
- **Clean art:** no garbled letters, extra limbs, off-model characters, floors under props, holes, or blur;
  every character and prop fully opaque (fade a whole scene if anything, never a sprite on its own).
- **Variety:** neither the framing nor the blueprint repeats in the next beat; at least six different
  blueprints or custom scenes in a 30 s piece.
- **Cast:** the same characters, the same scale, reacting to what happens, and never vanishing between two
  moments of one scene. The Claude critter stays coral in every role: Claude sessions and jobs differ by props
  and costume, never by colour (recolour only for another company's agent), and no costume hides the critter.

For the whole piece: frame 0 works as a thumbnail and a hook; the last beat holds at least 1 s; pixel scenes,
UI and real things alternate; one running example ties it together; it feels like one game, not a collage.

# Making an asset for charles-claude-editing

charles-claude-editing gives you the video, the part's time range (or several ranges), the asset's size, the area its text has
to stay inside, and sometimes what to show. It has already chosen the layout (a card, a split panel, an overlay,
a new screen).

1. Make the project at that size, without `--audio`, with the part's length: `python3 $T/tools/new_project.py
   videos/<video>/graphics/<name> --size <W>x<H> --duration <end - start>`. When the video needs assets at more than one size (a card,
   a tall card and a full screen), make them one set: `python3 $T/tools/new_project.py videos/<video>/graphics/<name> --set
   card:1280x630,tall:1280x1550,full:1080x1920 --duration <span> --start <start>`. Each size is its own project
   (`videos/<video>/graphics/<name>/card`, ...) with its own `beats.json` and scenes on the same clock, and all of them share
   `videos/<video>/graphics/<name>/assets`: names.js, the cast, art, logos and real things, plus `video.css` and `video.js` for this
   video's own styles and helpers. Fetch and generate into that shared folder once, so one cast and one look run
   through every size; it prints each size's mount and render commands. Generate plates in each frame's shape
   (`reference/art.md`). For an asset set, cover the whole span from the first range's start to the last range's
   end, and put one plain hold beat in each gap: only the ranges are shown. A set that starts at 0 runs on the
   reel's own clock: transcribe the whole voiceover and keep every beat in reel seconds. Pad every range with its
   own frames: hold the range's first frame for 0.1 s before it starts and its last frame for 0.1 s after it ends,
   so a frame of rounding at charles-claude-editing's cut shows the right picture and never flashes a neighbouring beat.
2. Cut the part's audio into it and transcribe that (for a set of sizes, once, in the set's folder): `ffmpeg -ss
   <start> -to <end> -i <video> -vn -c:a aac videos/<video>/graphics/<name>/part.m4a`, then `hf transcribe part.m4a -d . --json` there,
   then `.venv/bin/python $T/tools/onsets.py videos/<video>/graphics/<name>/transcript.json videos/<video>/graphics/<name>/part.m4a` and its `--check`
   (Workflow step 2). Its times start at 0.
3. Plan beats for the ranges only. Keep the cast and style identical across every asset of the same video. The
   render matches the part to the frame (HyperFrames rounds up to whole frames).
4. Render `out/part_<start>_<W>x<H>.mp4` (`part_012.4_1280x630.mp4`); for a set of sizes, run the render line it
   printed for each size (they land in `videos/<video>/graphics/<name>/out/`). For an overlay, delete the `.stage` and `.bg-art` layers
   and render `--format webm`, so only the moving pieces remain.
5. Write `out/part_<start>_<W>x<H>.sfx.json`: the moments that earn a sound, in part time:
   `[{"t": 1.02, "kind": "hit"}]` with kinds hit, pop, whoosh, type, coin, blip, success, fail. Mark the
   strongest two to four per 10 s; charles-claude-editing picks which to use. For an asset set, also list the ranges it covers.
