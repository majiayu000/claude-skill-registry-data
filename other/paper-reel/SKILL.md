---
name: "paper-reel"
description: "Make a faceless 9:16 explainer reel in the cut-paper 'Claude mascot' style (flat textured paper shapes, a terracotta box mascot with a hat per scene, a screwed header sign, a typing terminal bar, counter cards, rubber stamps, word-by-word paper caption chips, hard cuts on every voice line, a soft lo-fi bed) — fully free and local: Kokoro voice, whisper.cpp word timing, canvas + Playwright + ffmpeg. Use when the user asks for a reel/short/TikTok in this paper or Claude-mascot style, a 'skill checkpoint'/tool-spotlight reel, or a faceless explainer with a comment-keyword CTA."
argument-hint: "[topic or tool] [CTA keyword]"
---

# paper-reel

You make 18–25s vertical reels drawn entirely in code. The voice is the clock: every spoken line is one scene, and props, stamps and counters land on the words that name them. No paid APIs, no API keys.

Everything runs through `bin/reel` in this skill folder (call it `REEL=<this skill dir>/bin/reel`). The pieces live in the user's project, e.g. `<project>/pieces/<name>/`.

## 0. Setup check
`$REEL doctor` checks node, ffmpeg, Playwright and Chromium, whisper-cli and its model, Kokoro (Python and model), and the fonts. Run it first. It prints the exact install command for anything missing; tell the user that command and stop until it's fixed.

## 1. Script (approve with the user before drawing)
6–8 lines, 18–25s total, about 3.5 words/s. The proven arc:
1. **Hook:** what it is plus the payoff in one line ("This free Claude skill turns any topic into a Khan Academy style video.")
2. **How it works,** 2–3 lines, one concrete step each.
3. **The catch:** one honest limitation (it builds trust).
4. **"And get this."** The kicker: free, open source, a big number.
5. **CTA:** "For the <thing>, comment <WORD>." One keyword, all caps in the script.

Rules:
- Every factual claim (stars, prices, features) must be checked from a primary source first: the repo API, the README, the vendor page.
- Write numbers the way they're said ("over a hundred stars").
- Avoid words Kokoro mangles; read the align output to catch them. "Mac" came out as "map", so the script said "laptop". "Claude" is heard as "clawed", which is the correct pronunciation.
- A line id can't be `voice`.

Put it in `voice/script.json`: `{ "lead": 0.15, "tail": 0.6, "lines": [{ "id": "hook", "text": "...", "after": 0.12 }, ...] }`.

## 2. Voice + timing
`$REEL new <project>/pieces/<name>` copies the starter. `--from khan-skill` copies the full worked example instead. Edit the script, then run `$REEL voice <piece> [--voice am_michael] [--speed 1.32]`:
- Kokoro writes one take per line. `voice.mjs` joins them into `voice/voice.wav`, and `align.mjs` writes every word's time into `voice.json` using whisper.cpp.
- Check the `align: N/M words heard` line and the heard text. Fix any mispronounced words by rewording, then rerun just those lines with `--only id1,id2`.
- Good Kokoro voices: `am_michael` (default, energetic male), `am_fenrir`, `af_heart` (female). Speed 1.25–1.35 hits about 3.5 words/s.
- `--say` uses the macOS voice instead. It only works from a normal Terminal, not inside sandboxed agents.

## 3. Scenes
Edit `src/scenes.js`: one `SCENES.<line id> = () => { ... }` per line, in that order. To cut again inside a line on a word, add `SPLITS.push([lineId, word, n, sceneKey])` plus `SCENES[sceneKey]`. Sound cues go in `SFX_CUES()`. Read [references/style.md](references/style.md) for the layout grid and the look's rules. The kit API is at the end of this file.

What every scene needs (the style's fingerprint):
1. **A full-bleed world** with its own wall colour and one visual metaphor for the line: a classroom, a security desk, a carnival, a studio, a corkboard, a dusk road, a checkout. Never a prop floating on blank paper.
2. **The sign:** `prSign('HEADLINE')`. 2–5 words, caps, a different headline per scene. The kicker defaults to `SKILL SPOTLIGHT`; pass `{ kicker }` to brand a series.
3. **One hero prop that acts on a spoken word:** cue it with `VW(line, word).t0` (write-on, `countUp` counter, `prStamp` slam, `prCheck`/`prCross` pop, a typing `prTerm`).
4. **The mascot** `clawd(CLAWD_X, CLAWD_Y, { hat, mood, hold, view })`, bottom right and cropped by the frame edge. Give it a different hat per scene: `guard`, `mortar`, `boater`, `ranger`, `cap`, `phones`, `beret`. Its mood changes on the payoff word (`happy`, `wow`, `flat`). Use `view: 'side', walk: true` when it walks or points.
5. **3+ details of background life:** a clock, bunting, books, a lamp, notes, stars, a moon, acoustic foam, lane marks moving.
6. **`prChips()` last.** The captions are automatic, one paper scrap per spoken word. Keep the bottom-left band (y 1450–1600, x < 930) free of other text.

## 4. Check, then export
- `$REEL still <piece> 2.6,6,10,14 look.png --scale 0.4`. Look at the frames, and check them against [references/style.md](references/style.md).
- `$REEL check <piece>` must say `text: PASS` and `deterministic: true`. Fix any overlaps it reports by moving props, not captions.
- `$REEL export <piece> <out.mp4>` renders a 1080x1920 30fps video at about -14 LUFS in about 30 seconds and deletes the frame cache.
- Tell the user what you can't verify: you can't hear the mix, so ask them to listen.

## 5. Deliver
Give the MP4 path, a contact strip, the checks' numbers, the weakest shot, and a post caption in this pattern:

```
<hook sentence>. Follow so the DM lands 📩👇
READ BELOW: <3–4 numbered plain facts from the source>
The catch: <limitation>.
For the link, comment "<WORD>".
```

Never post it anywhere without the user's explicit go-ahead.

## Kit API (styles/paper-reel/kit.js)
- **Shapes:** `pp(path, fill, { key, shadow, sb, sy, tex, rim, shade })`. Paths: `pR(x,y,w,h,r)`, `pE(cx,cy,rx,ry)`, `pG(points)`, `pA(cx,cy,r,a0,a1)`. Transforms: `withT(x,y,rot,scale,fn)`. Colours are in `PR.*`.
- **Text:** `txt(str,x,y,size,color,{ weight, font, align, frac })`, `txtW`, `fitSize`. Fonts: `F_HEAD`, `F_CHIP`, `F_CHALK`, `F_MONO`.
- **World:** `prWall(colour,{ streak, panel, gap })`, `prFloor(y, colour, { studs, trim })`, `prBunting(y)`, `prClock(x,y,r,h,m)`, `prCorkboard`, `prNote`, `prStar`, `prBoard(x,y,w,h)`.
- **Story props:** `prSign`, `prTerm(str, frac)`, `prCounter(label, value, x, y, { s, rot, big })`, `countUp(t0,d,a,b)`, `prStamp(str,x,y,colour,t0,{ rot, size })`, `prCheck`/`prCross(x,y,t)`, `prChecklist(x,y,w,title,items,t0,dt)`, `prRepoCard(x,y,repo,sub,stars,ta,tb)`, `prCommentBox(x,y,WORD,t)`, `prReceipt(x,y,rows,total)`, `prFolder(x,y,s,fill,{ label })`, `prBurst(x,y,t0)`, `chalk(str,x,y,size,frac)`, `chalkLine(points, frac)`, `sparkIcon`.
- **Mascot:** `clawd(x,y,{ s, hat, mood, look, view, walk, hold: propStick(angle) | propPencil(angle), hand: { x, y }, flip })`. Set `CLAWD_SCALE` once per piece.
- **Time:** `TT` (now), `E0` (scene start), `ev(t,d)` 0→1, `popS(t)` back-eased pop, `springMove(t0,a,b,SPRING.playful)`, `VL(id)`, `VW(id, word, n)`, `seg`, `EZ.*`.
- **Determinism:** seeded `RNG(...)` only; never `Math.random()` or the clock. `$REEL check` verifies it.

## Gotchas
- **Kokoro inside sandboxed agents:** phonemizer copies `libespeak-ng.dylib` to a temp folder that macOS refuses to load. `tools/kokoro_lines.py` symlinks the original signed library instead; keep that patch.
- **faster-whisper** can hang in sandboxes. The timing uses whisper.cpp (`tools/align.mjs`, model at `~/.cache/whisper/ggml-base.en.bin`, override with `WHISPER_MODEL`).
- **Old copies of the style:** `build.mjs` uses a `styles/paper-reel/` folder beside or above the piece before this skill's copy. Delete or refresh any old copy in the project.
- **Name clashes:** `kit/core.js` and `kit/morph.js` already define many short top-level names (`smooth`, `grain`, `ink`, `burst`, `push`, `layer`, `W`, `H`, `F`, `B`…), so prefix your own scene helpers. A clash shows up as a `syntax error` at build.
- **Reviewing frames:** the animate `review.mjs` sheets need ffmpeg's `drawtext`, which the Homebrew build lacks. Use `still` and `check` instead.

Renderer and tools are vendored from the MIT-licensed `animate` skill (cth9191/animate); see NOTICE.md.
