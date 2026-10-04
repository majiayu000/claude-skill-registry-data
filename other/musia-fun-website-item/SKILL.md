---
name: musia-fun-website-item
description: Use when preparing, auditing, fixing, documenting, or publishing a Fun Lazying Art website media item for Musia, including ASR/STT-corrected lyrics, multilingual lyric JSON, per-vocal lyric sets, timing and word highlighting, pinyin/furigana/Jyutping ruby, 16:9 covers, manifests, website validation, and player recording.
---

# Musia Fun Website Item

Use this skill after a song, localization, MV, short film, or vocal render has been selected for `fun.lazying.art`. This skill is about truthful website publication, not about accepting raw generation quality.

## Default Repo

```text
/home/lachlan/ProjectsLFS/Musia
```

## Runtime Rule

Use the unified `musia` conda environment for Musia Python tools. Prefer the
repo CLI wrapper because it automatically routes through
`conda run -n musia python ...`:

```bash
node bin/musia.js fun-validate
node bin/musia.js fun-audit --media-id <media-id>
node bin/musia.js fun-record --media-id <media-id>
```

Only bypass this with `MUSIA_PYTHON` or `MUSIA_NO_CONDA=1` when the user
explicitly asks or a tool cannot run inside the shared environment.

## Core Rule

The website must match the real audio. Planned lyrics, prompts, and translations are references; ASR/STT, listening, and phrase timing are evidence. If a vocal repeats, skips, garbles, or changes a line, the published lyric set must reflect that vocal or the vocal should stay experimental.

Do not encode instrumental or pure-music spans as song-level lyrics. Public
lyric JSON, manifest timeline lyrics, music-publish lyric files, and subtitles
must contain sung lyric lines only. Do not add `role: "instrumental"` rows or
`♪` / `♪♪♪` rows to lyric tracks. The player may infer intro, break, outro, and
idle sections from timing gaps and show musical-note status in the player UI,
but those note markers are presentation state, not lyric data.

For generated multilingual songs, treat each playable vocal as its own evidence
source. A Chinese, English, Japanese, Cantonese, or mixed render may diverge
from the prompt and from the other language renders, even when they came from
the same master package. Do not copy another vocal's lyric text, timing, or
translations into a public lyric set unless ASR/listening proves that exact
audio actually sings the same structure.

The prompt lyric is only a reference until the selected audio confirms it. If a
vocal is unclear, garbled, skips words, repeats a line, or sings different text:

- correct the active lyric track to the audible line;
- mark that vocal experimental and keep it out of public/recorded outputs; or
- regenerate before publication.

Do not prettify translations into lyrics the audio did not sing.
For compact mixed-language ACE songs such as `Best Am I`, the planned native
lyric may be only an intention document. The active vocal can be English plus
Mandarin pinyin and Japanese romaji. Publish that active mixed layer truthfully,
then provide native EN/JA/ZH companion tracks for meaning. If the selected audio
only sings a compact subset, do not force the longer draft bridge/final chorus
into website lyrics, subtitles, or music-platform lyric files.

For every selected Musia song that is not explicitly private or experimental,
website preparation is part of the definition of done. Always prepare the data
for `fun.lazying.art` after song creation:

```text
selected audio -> ../MusiaSongs/audio/*.mp3
../MusiaSongs/audio.json
website/data/songs/<media-id>/manifest.json
website/data/songs/<media-id>/lyrics/<vocal-set>/<lang>.json
website/assets/covers/<media-id>-16x9.png
website/data/catalog.json
```

Apply the public version naming rule before publishing:

- standard selected ACE/ACE-Step version: pure song name, no suffix;
- older ACE/ACE-Step candidate: `ACE Legacy`;
- DiffRhythm variants: visible `DR` suffix, such as `DR Short` or
  `DR Full Lyrics`;
- lower-quality localization, SVC, or model-transfer routes: visible method
  suffix, such as `SoulX Localization`;
- only the standard selected ACE version should carry
  `manifest.playback.defaultMode: "single"` when the user wants default
  looping. Other variants should omit the playback hint unless intentionally
  requested.

For the current Fun catalog naming pass, rerun:

```bash
PYTHONNOUSERSITE=1 conda run -n musia python scripts/apply_fun_version_naming.py
```

Then validate both repos before final response.

When the song will also be published through LazyEdit/Shipinhao Music, the
music package must reuse the corrected website lyric JSON for the selected
vocal. Pass that exact active-language file as `--lyrics-json`; never hand off
the original prompt lyric, draft lyric, or another vocal's lyric set as the
music-platform lyric source.

This is a hard blocker. Before any Shipinhao Music, YouTube Music, or pure
music handoff, open the exact `website/data/songs/<media-id>/lyrics/<vocal>/<lang>.json`
file that will be passed as `--lyrics-json`, compare its line count/order
against the ASR-reviewed active vocal and the planned/reference lyric, and
confirm no planned lines are missing because of a stale website generator,
merged ASR segment, or earlier manual omission. If any line is missing or
timing is stale, fix the website JSON first and rebuild the music package from
that corrected JSON.

For video/music platform metadata, write for listeners, not for engineers.
Describe the song itself: title, artist, mood, story, language mix, genre, and
emotional hook. Do not leak conversation notes, generation pipeline details,
recording style names, implementation caveats, or "how this video was made"
unless the user explicitly asks for a technical demo post.

Do not let ASR override a good intended lyric just because the recognizer chose
a nearby word. If the input/reference lyric is phonetically close, fits the
sentence better, and the phrase structure has not changed, preserve the input
lyric. Use ASR to catch real omissions, repeats, order changes, and garbling,
not to downgrade plausible words such as `When` into `In` when listening and
context support `When`.

## Musia Atlas Learning Pages

When the user asks for a Chordify/Chord AI-like learning page, guitar-practice
view, song detail page, music-theory training page, or `musia.js`, prepare it as
**Musia Atlas** rather than inventing a separate player. Atlas uses the same
corrected website lyrics and media clock, then adds learning data:

```text
website/data/songs/<media-id>/study.json
website/musia.js
https://fun.lazying.art/?mode=atlas&media=<media-id>
https://fun.lazying.art/atlas/<media-id>/
```

Atlas data must be honest about confidence:

- lyrics: corrected website JSON for the active vocal;
- chords: timed manifest chord map, marked analysis-grade unless human audited;
- beats: local beat-analysis grid when available, otherwise BPM-estimated;
- capo/transpose/simplify: display-only transforms; the audio remains unchanged.

After correcting a song for the website or preparing it for Shipinhao Music,
rebuild Atlas before recording/publishing:

```bash
node bin/musia.js atlas-build --media-id <media-id>
node bin/musia.js fun-validate
```

For a catalog-wide refresh:

```bash
node bin/musia.js atlas-build --all
```

Do not use Atlas to teach false certainty. If chord timing, harmony, beats,
melody, or rhythm are approximate, label them as analysis or estimate. For
practice pages, make the UI beginner-readable: current phrase, current chord,
beat count, tempo, chord fingering, and simple steps before dense theory.

Atlas rhythm coach rule: strum and fingerpicking patterns are optional practice
guides, not verified original arrangements unless a musician or reliable
symbolic source confirms them. Default beginner behavior should divide the
active chord span into simple playable parts such as `D U D U`, with slower
playback-rate controls for practice. Keep the pattern labels clear enough for a
learner who cannot sing yet and does not know music theory.

Atlas layout default: use a compact four-column top on desktop. Column 1 is the
player, column 2 is chords plus guitar fingering, and columns 3-4 are the
current two lyric rows shown side by side. Keep a sticky mini player available
while scrolling the study section. Practice speed should support a broad range
such as `25%` to `200%`, with pitch preservation where the browser supports it.

Atlas current phrase must render the same ruby-aware lyric tokens as the main
player. Chinese uses `token.pinyin`; Japanese kanji uses `token.reading`. Do not
invent ruby in the client if the corrected lyric JSON lacks it; enrich the lyric
JSON first.

Atlas **Number notes** are allowed only as labeled learning data. This is the
English UI label for 简谱-style numbered notation. When `melody_f0.csv` exists,
the Atlas builder may convert token-level median F0 to note names and
key-relative numbered scale degrees, but mark it `analysis` unless a human
audits the lead sheet. The note lane should show all current-phrase notes,
highlight the active sung note, and auto-scroll with playback.

Catalog curation: use `hidden: true` plus `hiddenReason` for low-quality,
terrible, superseded, or suffix/demo versions. The normal player and playback
queue should hide them; `?showall` or `?showAll` should reveal the full catalog
for review/debug. Prefer hiding over deleting so old direct links still work.

## Unlisted Preview Protocol

Use **Preview** for `试听`. Use **Unlisted Preview** when a song is published as
a complete website item for human listening but must not appear in the normal
library, search peek, or autoplay queue. Unlisted means discoverability is
reduced; it is not private, and anyone with the direct URL can open it.

Do not use `hidden` or `Legacy` for a healthy candidate that is awaiting a
selection decision. Mark the catalog item explicitly:

```json
{
  "visibility": "unlisted",
  "releaseStage": "preview",
  "category": "preview",
  "previewLabel": "Listening Preview"
}
```

Also set `manifest.publication.visibility: "unlisted"`,
`manifest.publication.stage: "preview"`, and
`manifest.publication.listed: false`. A Preview must still meet normal
publication quality:

- selected normalized audio is hosted in `MusiaSongs`;
- each independently generated candidate has its own `asset`, `lyricSet`, ASR
  correction evidence, word timing, chords, and beats;
- all companion translations align to that candidate's actual sung structure;
- pinyin/furigana/Jyutping, cover, title, artist, and provenance are complete;
- strict media audit and full website validation pass.

The default catalog, search peek, and playback queue must exclude Preview
items. A direct hash remains usable, and `?preview=1` exposes the Preview
library for listening:

```text
https://fun.lazying.art/?preview=1#<media-id>
```

When several candidates belong to one listening decision, prefer one media item
with clearly labeled switchable assets such as `Music First` and `Lyrics
First`. Do not merge their lyric or musical analysis merely because duration or
prompt is similar. After the user selects a master, either promote the selected
asset into a normal listed item or create the final listed item from it; rerun
the lyric audit instead of silently reusing draft Preview data.

## Workflow

1. Run or collect analysis for every public vocal:

```bash
PYTHONNOUSERSITE=1 conda run -n musia python scripts/run_pipeline.py AUDIO \
  --run-name <media-id>-<vocal>-analysis \
  --max-duration 180 \
  --asr-model small \
  --language LANG
```

For final public lyric correction, prefer a `large-v3` correction pass when it
is feasible, especially for Chinese, Japanese, Cantonese, classical poetry, or
any song that will be recorded/published. Use `small`/`medium` only as quick
screening or cross-checks. If `large-v3` cannot run, document the fallback in
the production note and treat uncertain lyrics as experimental.

2. Correct lyrics using at least two sources:

- ASR/STT from that same selected vocal or stem, not only the master render or
  planned lyric;
- input/reference lyric, second ASR, or manual listening;
- phrase timing, separated vocal, and repeated listening when they disagree.

Use this evidence policy:

```text
actual audible structure > close intended lyric > ASR guess > translation draft
```

For close word-level conflicts, prefer the input/reference lyric when it is
sound-close and grammatically/musically stronger. Override it only when ASR plus
listening show a real structural change: missing line, repeated line, changed
line order, different phrase length, or a clearly different word.
For classical poems and other source-sensitive texts, matching word/syllable
count is strong evidence to preserve the source. If the source phrase and the
heard/ASR phrase have the same length and close sound, keep the source unless
manual listening proves the audio is clearly different.

Run a missing-planned-phrase audit before publication. Compare the planned or
reference lyric line-by-line against the corrected active-vocal track and ask:

- Which planned phrases are not represented in any published line?
- Did ASR swallow a short phrase into a long merged segment, especially repeated
  CJK phrases such as `一点，一点`?
- Did ASR miss a soft final syllable or tail at the ending, such as `不知`?
- Is there a timing gap between ASR segments where a soft or garbled planned
  phrase may still be audible, such as `梦也缱绻`?
- Does listening support adding the planned phrase even though ASR omitted it?

For mixed-language vocals, this audit must be word-by-word against the planned
mixed lyric, not only against the ASR segment list. ASR can silently collapse an
English or Japanese phrase into a gap between two recognized lines. Before any
recording or publication, print a side-by-side table of `planned/reference line
-> corrected active line/timing -> EN/JA/ZH companion lines` and account for
every planned line as one of: `kept`, `sound-close corrected`, `split`,
`merged`, `omitted-not-audible`, or `translation-only`. If a planned line falls
inside a timing gap and is even plausibly audible, add it as its own timed line
or explicitly document why it is not present.
When a gap follows a hook or chorus, run a no-VAD or looser-VAD ASR pass on the
separated vocal stem before treating the gap as instrumental. Snow We Share
needed this to recover a soft English continuation, an `Ah` vocal tail, and the
final Chinese pinyin tail. Add sung material with real timing when it is audible;
do not add `♪` or instrumental placeholder rows to the song-level lyric JSON.
For sound-close title or pinyin/romaji hooks, preserve the intended hook when it
is contextually stronger than ASR: `Best am I` over `Best of my`, `Wo shi tian
xia di yi deng` over `Washi tian shadi den`, and `Dare ni mo mienai namida`
over approximate ASR romaji. Override the planned form only when the audio
clearly changes structure or meaning.

For soft endings and mixed-language tails, do not trust one ASR pass. If ASR
hallucinates or stops early but the separated vocal/VAD still has energy, use
focused listening, waveform/VAD boundaries, user-provided hearing corrections,
and nearby prompt text to decide the public lyric. Example rule from `共饮长江水
· Same River`: replace stale guesses such as `Wo xiang xin` or `Same, same
longing` when listening confirms `Ding bu fu xiang si yi` and `Same river,
same longing`. Patch the active JSON and all companion translations before any
recording, video publish, or music package.

If a phrase is sound-supported, add it to the active-language JSON and to every
translation track in the same lyric set, using either the merged line timing or
a new line inside the gap. Update the manifest timeline and the production note
under `references/`. If the website was already public, commit, push, and wait
for the Pages deploy; do not leave live lyrics stale. After deploy, fetch the
live `https://fun.lazying.art/data/songs/...` JSON and confirm the corrected
lines are actually served before reporting completion or publishing elsewhere.

Treat a missing-planned-phrase audit failure as a release blocker. Do not record,
publish, or hand off music-platform metadata while the website still omits a
source-supported lyric line.

Normalize model-facing language codes before ASR/model calls: use `zh` for
Mandarin when the website track is `zh-Hans` / `zh-Hant`, and use `yue` for
Cantonese when the website track is `yue-Hant` / `yue-Hans`. Keep the public
website JSON code as `zh-Hans`, `zh-Hant`, or `yue-Hant`.

3. Choose the JSON shape:

- shared `textTracks[]` only when all playable vocals truly share line IDs and timing;
- per-vocal `lyricSets[]` when vocals are independent, imperfect, translated, mixed-language, or have different timing.

4. Build lyric tracks:

```text
lyrics/en-vocal/en.json
lyrics/en-vocal/zh-Hans.json
lyrics/en-vocal/ja.json
lyrics/zh-vocal/en.json
lyrics/zh-vocal/zh-Hans.json
lyrics/zh-vocal/ja.json
lyrics/ja-vocal/en.json
lyrics/ja-vocal/zh-Hans.json
lyrics/ja-vocal/ja.json
lyrics/mixed-vocal/mul.json
lyrics/yue-vocal/yue-Hant.json
```

Inside one lyric set, every track shares the same `line.id` sequence. The active vocal-language track owns line timing and exact word highlighting. Other tracks translate that active vocal's actual sung lines and may rough-highlight tokens inside the same current line.

5. Add pronunciation metadata:

- Mandarin CJK tokens: `pinyin`, such as `{"text": "光", "pinyin": "guang1"}`;
- Japanese kanji tokens: `reading`, such as `{"text": "光", "reading": "ひかり"}`;
- Cantonese CJK tokens: Jyutping in `reading`, such as `{"text": "光", "reading": "gwong1"}`.

Do not duplicate ruby by also putting pronunciation into the visible native text unless the active sung source is intentionally phonetic.

6. Prepare cover/poster:

- use 16:9 by default;
- save to `website/assets/covers/<media-id>-16x9.png`;
- set `assets.cover`, `assets.poster`, and `share.image`;
- record the cover prompt/source in `manifest.provenance` or the song production note.
- for public song covers, use a visually selected AgInTi/image-generation image
  matched to the song mood; no text, logo, or watermark; do not rely on a
  procedural placeholder cover for public recording/publishing.
- unless the user asks for a different visual direction, default Musia song
  covers to a song-specific cinematic megastructure feeling: the song's own
  setting, symbols, and emotional world should appear with vast scale, elegant
  architecture or impossible landscape, strong depth, and a small human/warm
  focal element. The megastructure must serve the song theme, not become a
  generic sci-fi background.
- `Best Am I` is the reference cover success: a small figure in a luminous
  golden-and-glass megastructure at sunrise, no text, no logo, no watermark,
  clean vivid color, and emotional alignment with self-belief.
- create or select a fresh cover for this exact song. Derive the image prompt
  from the corrected lyrics, title, emotional arc, setting, and symbols of the
  current song only. Do not reuse an older song cover, and do not let old song
  details contaminate the prompt or resulting image. Before publishing, confirm
  the cover does not visibly belong to another song, character, place, or theme.

7. Validate and audit:

```bash
npm run website:validate
musia fun-audit --media-id <media-id>
node --check website/app.js
git diff --check
```

Use strict audit mode before public release when reasonable:

```bash
musia fun-audit --media-id <media-id> --strict
```

The audit checks visible lyric script. Treat a warning such as Japanese or
Chinese visible text having high Latin content as a blocker unless the active
vocal is intentionally mixed-language and documented as mixed-language. Do not
leave English hooks in `ja.json`, `zh-Hans.json`, or `yue-Hant.json` just
because they came from a planning lyric; translate them or mark the active track
as mixed-language when the audio truly sings them.

8. Preview and record:

```bash
python3 -m http.server 9174 --directory website
musia fun-record --media-id <media-id> --skip-intro
```

Default publication recording, unless the user asks otherwise:

- 4K portrait, upper player/cover/header and lower current lyrics plus guitar
  fingering;
- current two KTV-style lyric lines, not the full lyric sheet;
- multilingual translation lines when available, especially EN/JP/ZH;
- advanced mode enabled with guitar fingering below the current lyrics;
- start from a smooth musical lead-in just before the first vocal, not exactly
  on the first syllable;
- mux the source audio from the same start time as the browser capture.

Use the realtime recorder for this default style:

```bash
PYTHONNOUSERSITE=1 conda run -n musia python scripts/record_fun_player_realtime.py \
  --media-id <media-id> \
  --asset-id <asset-id> \
  --output recorded_videos/<media-id>/<media-id>-<lang>-lyrics-guitar-portrait-4k.mp4 \
  --width 2160 --height 3840 \
  --css-width 1080 --css-height 1920 \
  --device-scale-factor 2 \
  --fps 24 \
  --start <smooth-vocal-lead-in-seconds> \
  --duration <remaining-duration-from-start> \
  --multilingual-lyrics \
  --advanced \
  --no-guitar-focus \
  --lyrics-guitar \
  --publication-layout \
  --capture-clock \
  --crf 12 \
  --preset ultrafast
```

Use this realtime recorder for normal publication clips. The slower deterministic
frame recorder is a fallback for visual debugging or special frame-exact renders,
not the default when the user wants a normal 4K portrait song capture quickly.
For portrait Fun-player recordings, do not create a landscape master and then
bg-fill it into portrait. Capture the page directly as native portrait
(`--width 2160 --height 3840 --css-width 1080 --css-height 1920
--device-scale-factor 2`) and publish that portrait MP4. If LazyEdit processing
is used for logo/metadata, pass `--no-portrait-blur-fill`; bg-fill is only for
converting non-portrait source videos and must respect source aspect ratio.

For publication recordings, `--publication-layout --capture-clock` is required.
The dedicated publication layout fixes the vertical slots as:

```text
header/player -> current multilingual lyrics -> chord carousel -> guitar fingering
```

The capture clock drives the visible lyrics/chords from the muxed audio start
time instead of browser media playback, so the recording cannot drift, freeze,
or desynchronize when the browser audio is muted and the final audio is burned
with FFmpeg. Do not publish a portrait Fun recording until sample frames prove
the lyric area, chord row, and guitar fingering do not overlap at vocal lines
or instrumental gaps.

When a Fun player recording is created, always sync the final MP4 to the
Nutstore Musia share folder before reporting completion. The recorder now does
this by default; use `--no-sync` only for private or temporary captures:

```bash
mkdir -p "/home/lachlan/Nutstore Files/Projects/Musia"
cp -f RECORDED_VIDEO.mp4 "/home/lachlan/Nutstore Files/Projects/Musia/"
```

For multi-vocal recordings, render and sync one MP4 per public vocal/language,
and make sure `--asset-id` matches both the visible website player and the
muxed audio track.

Use these standard portrait publication styles for Fun player recordings:

- `lyrics-only`: full-width top player plus current multilingual lyrics. Use
  `--multilingual-lyrics --no-advanced --no-guitar-focus` with the realtime
  recorder.
- `fingering-only`: full-width top player plus chord carousel and large guitar
  fingering. Use `--advanced --guitar-focus`.
- `lyrics+fingering`: full-width top player plus current multilingual lyrics,
  then guitar fingering in the lower spare portrait space. Use
  `--multilingual-lyrics --advanced --no-guitar-focus --lyrics-guitar
  --publication-layout --capture-clock`.

Do not change lyric content to make room for fingering. Use empty portrait
space first; only reduce type size if the text actually overflows.

After recording, inspect the MP4 with `ffprobe` and extract a sample frame before
publishing. If a LazyEdit logo/subtitle processing step turns an approved 4K
Musia recording into a much smaller, blurrier, or low-bitrate output, publish the
inspected recording through a direct HQ AutoPublish package instead of accepting
the degraded re-encode. Use clean listener-facing metadata and keep internal
workflow notes out of platform descriptions.

## Quality Gate

Before calling an item public-demo quality:

- listen to every selected vocal;
- confirm every public vocal has an active-language lyric track corrected from
  its own ASR/STT/listening pass;
- confirm prompt-only lyrics were not used as public EN/JP/ZH/Cantonese lyrics
  unless the exact selected vocal was verified;
- confirm each vocal has its own lyric set unless ASR proves shared timing is correct;
- confirm the first highlighted line begins at the real vocal entrance;
- confirm active-vocal word highlighting does not jump into another language's future line;
- confirm translation highlighting stays within the current line ID;
- confirm the visible text language matches the track code, especially for
  Japanese/Chinese/Cantonese tracks;
- confirm close ASR substitutions were corrected against the intended lyric
  when pronunciation and context support the intended word;
- confirm the missing-planned-phrase audit was done, including merged ASR
  phrases and timing gaps between segments;
- confirm pinyin/furigana/Jyutping display once and cleanly;
- confirm the chord row has a current highlighted chord when chord data exists;
- confirm title, artist `Musia`, cover, social image, and localized titles are present;
- if publishing to LazyEdit/Shipinhao Music, confirm the package uses the same
  corrected active-vocal lyric JSON as the website;
- confirm every requested recording has a Nutstore copy under
  `/home/lachlan/Nutstore Files/Projects/Musia/`;
- document ASR correction decisions and caveats under `references/`.

## Detailed Reference

Read only when preparing or reviewing a real website item:

```text
references/fun-website-item-preparation.md
references/musia-website-json-format.md
references/musia-song-generation-and-website-runbook.md
```
