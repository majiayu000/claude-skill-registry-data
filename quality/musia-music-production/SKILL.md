---
name: musia-music-production
description: Use when generating, correcting, reviewing, documenting, publishing, or handing off original music in Musia, including idea-to-song, lyrics-to-song, melody/chord-controlled songs, ACE-Step/YuE/SoulX route selection, vocal quality checks, song review reports, Fun Lazying Art website publishing, per-vocal lyric sets, and LALACHAN song-first video handoffs.
---

# Musia Music Production

Use this skill for original song creation and review. For strict same-song localization, also use `musia-song-localization`.

## Default Repo

```text
/home/lachlan/ProjectsLFS/Musia
```

## Runtime Rule

Use the unified `musia` conda environment for Musia Python tools. Prefer the
repo CLI wrapper because it automatically routes through
`conda run -n musia python ...`:

```bash
node bin/musia.js doctor --json
node bin/musia.js song review --project-dir data/creative_projects/<song-id>
node bin/musia.js fun-validate
```

Only bypass this with `MUSIA_PYTHON` or `MUSIA_NO_CONDA=1` when the user
explicitly asks or a tool cannot run inside the shared environment.

## Core Rule

Do not accept a generated song just because a WAV exists. A usable song needs:

- audible sung vocal;
- healthy levels;
- coherent tempo/chord analysis;
- saved lyrics and prompt;
- review report;
- human listening pass when the result matters.

Quality comes before same-melody control. If a same-score/same-F0 route makes
the vocal, pronunciation, phrasing, or arrangement worse, label that render
experimental and leave it out of the public/final path. Regenerate with the
best full-song model instead, even if EN/JP/ZH end up as independent high-quality
versions rather than one perfectly shared melody.

For beautiful song generation, use ACE/ACE-Step as the default and final route.
The user explicitly prefers ACE output quality and asked to always use ACE.
Treat DiffRhythm clean LRC as an alignment experiment only, not a beautiful-song
route. The `蜀道难 · 原文重组 DR Draft` and `行路难 · 原文重组 DR Draft` checks
showed that DiffRhythm can align lyrics reasonably, but melody and singing
quality may be terrible or only so-so. Keep such outputs visibly `DR
Draft`/experimental, do not record or publish them as final-quality songs, and
return to an ACE-Step candidate sweep when beauty, melody, and vocal feel matter.

For new Mandarin or mixed Mandarin generation, prefer real Chinese characters
as the model-facing sung lyric. Do not use pinyin as the primary sung lyric just
because it is easier to tokenize; it often makes Mandarin sound foreign. Keep
pinyin for website ruby, external pronunciation guides, correction notes, or
explicit phonetic fallback experiments only. If a pinyin-based render is kept
public, label it with a meaningful version suffix instead of treating it as the
standard clean-language version.

Before inventing a new generation route, inspect the closest successful Musia
project and reuse its proven structure. For example, `越人歌` worked because it
used a focused Chinese ancient-song route, source-line selection/repetition,
compact positive prompting, and public restoration of source-close ASR errors.
`共饮长江水` worked because it used sparse English-led mixed phonetic lyrics
with pinyin/romaji as private sound control, then corrected public lyrics from
the actual audio. The old `共白头 · Snow We Share · 雪中回声` worked because its
hook lyric was sparse and pinyin/romaji-led. If a remake needs higher source
truth, first try the focused `越人歌` route; if the user wants a mixed-language
vocal, try the `共饮长江水` sparse phonetic route. Do not keep iterating dense
new prompt shapes after ASR shows drift.
`Best Am I · 我是天下第一等` is the compact mixed-anthem reference: dense mixed
lyrics failed, compact XL Turbo seed sweep worked, XL SFT hallucinated generic
video-outro text, and the public lyric was corrected to the actual compact sung
structure. For motivational/cute/pop mixed EN/ZH/JP songs, start with a native
public lyric for intent, rewrite it into a compact ACE-facing performance lyric
with one language phrase per line, use English as the lead scaffold plus short
Mandarin pinyin/Japanese romaji hooks, repeat the title hook, and select by
ASR/listening rather than draft coverage. See
`/home/lachlan/ProjectsLFS/Musia/references/best-am-i-mixed-language-route-lessons-2026-07-12.md`.
For the Snow We Share route specifically, keep the old public sparse hook as
the baseline when the user praises it; later native/no-pinyin remakes are not
automatically better. See the LazySkills reference note named
`musia-snow-we-share-route-and-publish-recovery-2026-07-10.md` and the Musia
repo reference
`/home/lachlan/ProjectsLFS/Musia/references/musia-successful-song-routes-2026-07-10.md`
before choosing a new route.

Pinyin can be used as a private pronunciation-control lyric when the user
accepts it or when a previous pinyin route clearly worked, but the public text
must be corrected from the actual audio and restored to the original Chinese
only when the sound, phrase count, and context are close. Include the original
Chinese source lines in the caption/notes so the model has semantic grounding;
do not rely on pinyin alone.

Planned lyrics are intent, not blind truth. After generation, use listening and ASR/STT evidence to decide what the render actually sang. If the rendered vocal repeats, skips, reorders, or clearly changes a phrase, document the mismatch and publish lyrics/timing that match the audio. If ASR only substitutes a nearby word and the planned lyric is phonetically close, grammatically stronger, and supported by manual listening, keep the planned lyric; do not let ASR downgrade `When` to `In` or similar close words just because the recognizer guessed that token.

Instrumental and pure-music spans are not lyrics. Do not write intro, break,
outro, or silent-gap placeholders such as `♪`, `♪♪♪`, or
`role: "instrumental"` into website lyric JSON, manifest timeline lyrics,
subtitle tracks, or music-publish lyric files. Store only sung lines. Let the
Fun player infer non-lyric spans from timing gaps and show musical-note status
as UI state only.

If the user wants the public lyric to feel closer to the actual performance,
allow a sound-close poetic compromise only when the rendered phrase has clearly
changed structure, word count, or sound. When the input/source lyric has the same
phrase length, is phonetically close, and is more beautiful or grammatically
stronger, preserve the source and treat ASR's nearby modern word as a guess.
Document every compromise in the production note. Example from `越人歌`: after
user review, `心爱君兮` was restored to source `心悦君兮`, `追不着` was restored
to `君不知`, and `牵愁中流` was restored to `搴舟中流`; the `望之` phrases
remain because those lines changed structure more clearly.

Before calling the lyric correction complete, run a missing-planned-phrase audit:
compare the planned/reference lyric against the corrected active-vocal lines and
look for prompt phrases that ASR omitted, merged into a long segment, or placed
inside a timing gap. Short repeated or soft CJK phrases can be swallowed by ASR
even when audible. Always check the ending manually for soft final syllables or
tails that ASR may miss. If listening supports the intended phrase or tail, add
it back with real timing and translations; if it is not audible, document that
it was skipped.
For soft mixed-language hooks, run a second no-VAD or loose-VAD ASR pass on the
separated vocal when a suspicious gap follows a chorus or hook. Snow We Share
recovered `Let our hearts be less alone`, a long `Ah` tail, and the final
`Ta zhao ruo shi tong lin xue / Ye suan gong bai tou` only after this extra
check. Do not mark that span instrumental until no-VAD, waveform energy, and
manual listening all agree it has no sung content.
For mixed-language songs, do a word-by-word coverage table before accepting the
song for website, recording, LazyEdit, or Shipinhao Music. Compare each planned
line against the corrected active vocal and mark it as kept, sound-close
corrected, split, merged, omitted-not-audible, or translation-only. Pay special
attention to ASR gaps between adjacent recognized lines; a missing English line
such as `Moonlight will not return to me` can live entirely inside a gap between
`Moon` and a Japanese line. Do not record or publish until every planned line is
accounted for and companion EN/JA/ZH tracks translate the actual active line.
For endings, treat ASR silence or hallucination as suspicious when VAD/waveform
still shows vocal energy. Use manual listening and user correction to recover
soft tail lyrics; then patch website JSON, manifest, translations, and the
production note before recording or packaging. The `共饮长江水 · Same River`
tail is the canonical example: `Ding bu fu xiang si yi` -> `Same river, same
longing` -> `Give me all`.
When the user later identifies a missed phrase, patch the website lyric JSON,
manifest timeline, and references immediately, then push/deploy if the item is
already public.

Never package Shipinhao Music, YouTube Music, or another pure-music release from
draft lyrics. The music-publish lyric source must be the corrected website
active-vocal JSON after the missing-planned-phrase audit. Open that JSON, verify
line count/order/timing against ASR and the intended lyric, and only then pass it
as `--lyrics-json`.

For multilingual companion renders, run that correction independently for each
selected audio. A Japanese render needs Japanese ASR/listening evidence; an
English render needs English ASR/listening evidence; a Chinese render needs
Chinese ASR/listening evidence. Do not assume a companion vocal matches its
prompt just because the lyric file was used during generation. If the vocal
diverges, publish the actual sung lyric, mark the render experimental, or
regenerate it before website/recording use.

Avoid real singer imitation or voice cloning unless the user owns or has explicit consent.

## Beautiful Song Standard

Before generating, write a compact producer brief with:

- emotional arc;
- short singable lyric lines;
- duration, language, key/BPM when known;
- arrangement and vocal direction;
- negative instructions such as no clipped endings, no buried vocal, and no real-singer imitation.

When the user says quality matters or has time to wait, use the best practical
local route before accepting a faster route:

- inspect installed model checkpoints before generation;
- use `acestep-v15-xl-turbo` as the proven Musia production baseline and sweep
  6-10 seeds when the result matters;
- include `acestep-v15-xl-sft` as an A/B challenger when VRAM allows, but never
  promote it merely because it uses more steps;
- if a newer XL/XXL/XXXL or higher-quality model is available in the upstream
  project or community and can be installed legally, download/test it before
  final publication when the user asks for best quality;
- keep the older model output only if listening and ASR prove it is better for
  the specific song;
- document the exact model, checkpoint, seeds, duration, and fallback reason in
  the project note.

Do not assume `acestep-v15-xl-sft` is better for every song. The failed `Star
Bucks` SFT attempts produced noise/gibberish or unrelated outro chatter, while
the earlier successful Musia songs (`越人歌`, `云海之恋`, `Take Care of Yourself`,
`Aya Chan Hikari Ame`) mostly came from ACE XL Turbo with compact positive
prompts and seed sweeps. If SFT returns empty ASR, generic outro text, buried
vocals, or user-reported gibberish, immediately switch to a Turbo candidate
sweep instead of trying to publish or record it.
For mixed EN/ZH/JP songs, pinyin/romaji can be a useful active-vocal
sound-control layer when it helps ACE sing beautifully, but it is not the public
meaning layer. Publish the corrected active mixed vocal plus native companion
translations. If the render only sings a compact subset of the prompt, publish
that subset honestly and omit unsung draft lines.

For frontier-quality work, use a license-aware candidate gate rather than a
single model name:

1. Generate multiple ACE candidates from one frozen lyric/producer brief.
2. Run `scripts/audio_health_report.py`; reject silence, clipping, non-finite
   audio, broken dynamics, and hard cuts before expensive review.
3. Use APEX + MERT only to rank which candidates deserve listening; its
   coherence, musicality, memorability, clarity, and naturalness scores do not
   verify lyrics.
4. Run at least two lyric evidence routes, such as separated-vocal
   faster-whisper plus MOSS-Music or HeartTranscriptor, then audit gaps,
   repeats, weak endings, and source-close ASR substitutions manually.
5. Select by human listening with melody/emotion weighted above raw lyric
   coverage, while still rejecting materially wrong or missing lyrics.

Do not reject a high-music candidate from mixed-track ASR alone. Dense
instrumentation can make ASR return generic speech, miss whole sections, or
hallucinate an outro even when the isolated vocal is intelligible. For every
serious finalist, separate the vocal first and rerun a large ASR model plus an
independent music-understanding transcription. Keep a `music-first` finalist
and a `lyric-first` finalist when the evidence disagrees, loudness-match their
listening copies, and require a full human listen before choosing one. The
`洛水照影` experiment is the canonical example: the stronger music candidate
had lower automated lyric overlap, while the alternate recovered more of the
planned lyric.

Prefer a compact positive producer caption for ACE. Long negative instructions
can leak into the generated vocal or encourage generic outro speech. Put
forbidden behavior in the external quality gate instead of making the model
sing a list of prohibitions.

LeVo 2 / SongGeneration-v2 may be used as a private same-brief research
challenger only. Its current upstream license excludes commercial and production
use, so never send its outputs to Fun, LazyEdit, Shipinhao, or another public
release. Qwen-Music and the 2026 FullDiT full-song route are paper-only until
official runnable weights exist. SegTune currently provides training/inference
code but no ready official checkpoint; do not claim it is installed merely
because its repository can be cloned. Read
`/home/lachlan/ProjectsLFS/Musia/references/luoshenfu-frontier-model-research-2026-07-29.md`
before changing Musia's production default.

Prefer fewer stronger lines over dense poetry. For Chinese/Japanese, reduce pronunciation risk by using natural, short phrases and correcting after ASR/listening.

### Classical Source-Text Default

When the user names or supplies a classical poem, ci, yuefu, fu, or other
premodern text and asks for a song without explicitly requesting a rewrite,
default to an **original-source-text song**:

- for a short work, try to use the complete original text;
- for a long work, select the most musical and emotionally central original
  passages rather than forcing the whole text linearly;
- ordering, sectioning, repetition, held syllables, and musical space are
  allowed, but every Chinese sung lyric line must come from the source;
- do not add modern Chinese paraphrase, connective lines, or newly written
  hooks merely because the user asks for a beautiful or resonant song;
- show and save the selected source-text lyric layout before generation;
- keep public lyrics in the verified source wording. Private homophone,
  pinyin, or easier-character substitutions may guide the model, but restore
  the source wording wherever listening confirms a sound-close performance;
- when EN/JA companion lyrics are requested, the Chinese layer remains source
  text while EN/JA may be culturally singable adaptations.

An adapted modern-lyric version is a separate route, not the implicit default.
Use it only when the user explicitly asks for adaptation, or offer it as a
clearly labeled alternate after repeated source-text attempts fail pronunciation
or musical quality. Never silently replace the poem with a rewrite.

For classical Chinese poems, especially Li Bai/Tang poetry, run a
pronunciation-prep gate before ACE/YuE generation:

- verify the source text and likely poem variant from at least one external
  source or local reference;
- search/check a poem-specific pinyin or annotated reading source when
  available;
- run pypinyin as a baseline, then manually audit polyphonic and rare
  characters such as `行`, `将`, `了`, names, place names, and classical words;
- write a pinyin guide and list risky pronunciations in the project notes;
- when exact classical diction causes garbling, first try a shorter selected
  source excerpt, better repetition/spacing, private phonetic controls, and
  additional seeds. Move to a modern adaptation only as a separately labeled
  route under the source-text default above;
- add ACE-facing caption guidance for the risky words, and after generation
  compare ASR/listening against the pinyin guide before publishing.

For very short classical poems, do not assume a single exact pass is enough.
If ACE produces no ASR recovery, weak vocal text, or subtitle/credit leakage:

- repeat only original poem lines into a verse/chorus/hook form rather than
  adding modern words;
- emphasize the most important couplet or hook by repeating it;
- keep captions positive and compact, avoiding long forbidden-word lists that
  the model may sing;
- use private phonetic substitutions for rare characters, then restore the
  public original text only where sound-close;
- select by actual hook recovery and listening, not by model size alone.

For long classical poems where the user wants original text but a beautiful
song, do not force the full poem linearly. Choose the most 朗朗上口,
emotionally central, and 音韵-compatible original lines; preserve those selected
lines exactly; reorganize them into verse/pre-chorus/chorus/bridge form; repeat
the strongest couplet as a hook when it improves melody, memory, rhyme, and
audience resonance. This is still an original-text route if every sung line is
from the source. The creative work is selection, ordering, repetition, and
musical pacing, not modern paraphrase.

For future original-poem experiments, create a recursive refinement package
instead of hand-building the project from scratch:

```bash
PYTHONNOUSERSITE=1 conda run -n musia python scripts/prepare_ace_poem_refinement_pack.py \
  --title "Poem Title" \
  --poem-file poem.txt \
  --hook "main emotional couplet" \
  --substitution "rare=common-sound-control"
```

Use the generated `REFINEMENT_PLAN.md`, `source/pronunciation-guide.md`,
repeated-hook lyrics, SFT/Turbo configs, and `commands.sh`. The successful
`越人歌 · 原诗版` route came from this philosophy: source truth -> pronunciation
truth -> private model-facing simplification -> multiple lyric layouts -> model
sweep -> ASR/listening rejection -> hook-focused regeneration -> truthful
website correction.

For the full reusable ACE poem-song method, use the repo reference:

```text
/home/lachlan/ProjectsLFS/Musia/references/ace-poem-song-beauty-and-lyric-alignment-method-2026-07-01.md
/home/lachlan/ProjectsLFS/Musia/references/yue-ren-ge-recursive-refinement-playbook-2026-07-01.md
```

The rewritten `侠客行` workflow remains a useful optional adaptation route, but
it does not override the source-text default. A beautiful song can come from
selection, reordering, repetition, phrasing, and arrangement without modern
paraphrase. Do not force every line of a long poem into ACE; use a strong
original excerpt first. Label an adapted route explicitly, preserve the poem's
spirit and iconic images, and keep it separate from the source-text version.

Do not cram words into the song just to preserve every detail. Use musical
space: 留白, held vowels, rests, repeated hooks, and breath-friendly pauses.
Some lines should be sparse and some can be fuller; the goal is a proper fit
to the melody and emotion, not the fewest words and not the most words.

Do not overcorrect into lyrics that are too sparse. For ACE-style 80-95 second
short songs, prior successful Musia renders usually use a complete verse /
pre-chorus / chorus / bridge-or-outro shape with many short lines: roughly
30-45 CJK lines, average 4-7 CJK characters per line, and about 150-280 total
CJK lyric characters. Use this as a density target, then simplify only when
ASR/listening shows the model is skipping or garbling lines.

For English ACE songs, use a lower lyric-density target than Chinese/Japanese.
Successful 65-80 second English renders often use one short verse, one chorus,
and one outro, roughly 18-28 short lines. If ASR recovers the first verse but
drops the chorus or later sections, shorten the lyric first; do not add more
prompt constraints. A good fallback pattern is: XL Turbo, 8 internal steps,
70-78 seconds, 4-8 seeds, clear positive caption, upfront natural English vocal,
and candidate selection by listening plus large-v3 ASR.

Before generating or accepting EN/JP/ZH lyrics, do an LLM lyric-quality pass
when an API/model is available. Use OpenAI, DeepSeek, or a strong Codex/GPT-5.5
reasoning pass to check:

- rhythm fit: short singable phrases, line length, phrase stress, and likely breath points;
- musical space / 留白: whether a line should hold notes, leave rests, or repeat a simple hook instead of adding more words;
- rhyme / 押韵: English end rhyme or slant rhyme, Chinese rhyme groups, Japanese vowel/mora echoes;
- language-specific fit: English stress, Chinese tone comfort and natural wording, Japanese mora flow and particles;
- emotional clarity: the lyric should say something concrete and singable, not just be poetic filler.

Revise lyrics before generation if the LLM flags awkward rhythm, weak rhyme, overlong lines, or unnatural CJK wording.

## Fast Workflow

Create a song package:

```bash
musia song init \
  --title "Song Title" \
  --idea "short concept" \
  --vocal-language ja \
  --lyrics-file lyrics.txt \
  --genre "cinematic J-pop" \
  --style "piano, warm strings, gentle drums" \
  --voice-notes "clear upfront young female vocal, no real singer imitation"
```

Generate:

```bash
data/creative_projects/<song-id>/commands.sh generate
```

Review:

```bash
data/creative_projects/<song-id>/commands.sh review
```

If the review shows quiet vocals, wrong language, clipped endings, or poor lyric recovery, do not publish as final. Run a correction pass or label it as experimental.

Correct:

```bash
musia song correct \
  --project-dir data/creative_projects/<song-id> \
  --issues "vocal unclear or endings clipped" \
  --caption-extra "clearer vocal, fewer words per line" \
  --lyrics-file corrected-lyrics.txt
```

Handoff to LALACHAN:

```bash
musia song handoff \
  --project-dir data/creative_projects/<song-id> \
  --audio data/creative_projects/<song-id>/final/selected.mp3 \
  --cover data/creative_projects/<song-id>/assets/cover-16x9.png
```

## Master-Companion Pipeline

Use this as a third opt-in route when the existing full-song and strict
localization pipelines should stay unchanged, but multilingual versions need
more consistency:

```bash
musia master-companion \
  --title "Song Title" \
  --master-language ja \
  --master-audio master.mp3 \
  --run-analysis \
  --target-languages en zh-Hans \
  --control-policy quality-first
```

This route chooses or generates one high-quality master render, extracts beats,
chords, phrase timing, and melody/F0, then creates target-language lyric
adaptation packets, soft full-song companion prompts, and strict SVS handoffs.

Default policy: quality first; change lyrics for rhyme/rhythm/naturalness before
changing melody; allow small melody changes when strict matching hurts the song;
publish strict same-melody outputs only after listening and ASR checks.

## Reusable Script

Primary script:

```text
scripts/musia_song_workbench.py
```

It supports:

```text
init
review
correct
handoff
find-audio
```

Generated song folders are intentionally ignored by git:

```text
data/creative_projects/<song-id>/
```

## MiniMax Music 3 Option

For explicit MiniMax requests or a frontier-model comparison, use Musia's
`scripts/install_minimax_music3.sh` and `scripts/run_minimax_music3.sh`.
The verified local runtime is a virtualenv overlay at `.conda/minimax-music3`,
not a named conda environment; keep the shared MOSS base intact.
Read `references/minimax-music3-setup-and-ayachan-2026-09-13.md` in the Musia repo
for pinned versions, resumable hash-checked downloads, commands and actual trials.

Keep native lyrics separate from the structured Global Metadata / Vocal Details /
Arrangement caption. Section tags must stand alone or trailing lyric text is
discarded. Duration is an upper bound, not a guarantee. Preserve native 44.1 kHz
stereo and check true peaks, not only sample peaks. Audit the entire rendered
vocal: ASR can both omit real lines and invent zero-duration duplicate endings.
Do not turn an ASR duplicate into a public repeat without supporting evidence.
Mandarin was tested here; other languages need their own audition. Compare
against the retained ACE baseline and review the downloaded model's release
terms before public/commercial use. Installation is not proof of superior music.

## Model Routing

- Idea/lyrics to full song: ACE-Step 1.5 first.
- Best-quality full song: ACE multi-seed production sweep, objective health
  gate, APEX shortlist, multi-route lyric audit, then human listening.
- Frontier local A/B: HeartMuLa as a license-compatible challenger; LeVo 2 only
  as private research under its current non-production license.
- Music QA: MOSS-Music and HeartTranscriptor for independent lyric evidence;
  APEX for aesthetic ranking only; FFmpeg/signal measurements remain
  authoritative for clipping, loudness, silence, and hard-cut checks.
- Vocal-only controlled short hook: SoulX if language metadata is supported.
- Strict source-song localization: Demucs/analysis plus YingMusic/SoulX prep, not full-song generation.
- Same melody is optional when it hurts quality. Prefer high-quality independent ACE/YuE language renders over low-quality same-score vocals.
- If Japanese/Chinese lyric accuracy is poor: shorten lines, reduce kanji ambiguity, increase vocal clarity in caption, try new seed/model, or use a specialized vocal workflow.
- For mixed EN/ZH/JP full-song demos on local open models, prefer one active `mul` sung/phonetic lyric track. If native CJK script collapses or garbles, use pinyin/romaji in the sung input and display native Chinese/Japanese as translations with pinyin/furigana. Document this as a phonetic render, not native-script singing.

## Website Publishing Rule

For any selected Musia song that is not explicitly private or experimental,
prepare the Fun website item before calling the song finished. The default
post-song closeout is:

1. Copy or transcode selected audio to `../MusiaSongs/audio/`.
2. Regenerate `../MusiaSongs/audio.json` and commit/push that repo when publishing.
3. Create or update `website/data/songs/<media-id>/manifest.json`.
4. Create per-vocal lyric JSON with ruby/pinyin/furigana and timing.
5. Add or update the song entry in `website/data/catalog.json`.
6. Add a 16:9 cover at `website/assets/covers/<media-id>-16x9.png`.
   The cover must be newly generated or newly selected for this exact song.
   Base the cover prompt on the corrected lyrics, story, mood, symbols, and
   final title of the current song. By default, make Musia song covers feel
   like song-themed cinematic megastructures: vast scale, elegant impossible
   architecture or landscape, deep atmosphere, and one small warm human-scale
   focal point tied to the lyric. Do not reuse an older song cover, and do
   not let old song names, characters, scenes, metadata, or prompt fragments
   pollute the new cover. If adapting a prior visual style, rewrite the prompt
   from a clean current-song brief and verify the resulting image does not look
   like a stale cover from another song.
7. Run `npm run website:validate`, `musia fun-audit --media-id <media-id>`, `node --check website/app.js`, and `git diff --check`.

If the song will be packaged for LazyEdit/Shipinhao Music or YouTube Music,
the package must use the corrected active-vocal website lyric JSON as its
lyrics source. Do not hand off the original prompt lyric, planned translation,
or master-language transcript to the publisher. The music platform lyrics
should match the corrected `fun.lazying.art` lyric set for that exact audio.

For `fun.lazying.art`, use the `musia-fun-website-item` publication workflow before calling a website item finished. Use shared `textTracks[]` only when all playable vocals truly sing the same line structure. If English, Chinese, and Japanese renders are independent or imperfect, create per-vocal `lyricSets[]`:

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
```

The active vocal owns timing and exact word highlighting. Other languages in the same set are translations of that vocal's actual sung lines and may rough-highlight corresponding tokens inside the same current `line.id`.

Correct every public lyric set from at least two evidence sources: ASR/STT from the actual vocal plus input/reference lyrics, second ASR, or manual listening. For close word conflicts, preserve the input/reference lyric when pronunciation, grammar, and phrase structure support it; use ASR to detect real structural differences, not as an unquestioned transcript. Add pinyin for Mandarin, furigana readings for Japanese kanji, and Jyutping readings for Cantonese. Run the publication audit:

Also check missing planned phrases before publishing: scan any ASR timing gap
and any unusually long merged ASR segment against the source lyric. Add
sound-supported phrases to the active JSON and matching translation tracks; do
not leave the public site or LazyEdit/Shipinhao handoff using the older
incomplete lyric set.

For companion-language songs, this evidence rule applies to each playable
asset separately. Never reuse the master-language transcript, prompt lyric, or
another vocal's timing as the public lyric source for EN/JP/ZH/Cantonese unless
the selected audio's own ASR/listening pass confirms it.

```bash
musia fun-audit --media-id <media-id>
```

For EN/JP/ZH companion renders, double-check every visible translation track
before publishing. `ja.json` should not silently contain English hooks, and
`zh-Hans.json` / `zh-Hant.json` should not silently contain English hooks,
unless the active vocal truly sang a mixed-language line and the manifest says
so. Use `musia fun-audit --media-id <media-id> --strict` to catch wrong-script
visible text.

The Fun player should keep public song playback clean: native-language dropdown labels, a two-line KTV lyric carousel, visible current-chord highlighting, and capture mode for videos. To record a share clip with the original audio muxed directly, run:

```bash
musia fun-record --media-id <media-id> --skip-intro
```

For a mixed-language vocal, use:

```text
lyrics/mixed-vocal/mul.json
lyrics/mixed-vocal/en.json
lyrics/mixed-vocal/zh-Hans.json
lyrics/mixed-vocal/ja.json
```

## References

Read only as needed:

```text
references/musia-song-generation-and-website-runbook.md
references/fun-website-item-preparation.md
references/musia-song-workbench.md
references/lalachan-song-first-video-workflow.md
references/musia-full-capability-guide.md
references/musia-creative-studio.md
references/musia-website-json-format.md
```
