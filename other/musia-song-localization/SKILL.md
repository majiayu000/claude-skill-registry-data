---
name: musia-song-localization
description: Use when working on Musia, AI song localization, song-to-Chinese or cross-language re-singing, extracting bass/drums/vocals/other stems, lyrics, beats, chords, phrase timing, singable lyric adaptation, YingMusic-Singer-Plus or SoulX-Singer synthesis preparation, creating same-music translated singing artifacts, or fixing Fun Lazying Art per-vocal lyric/timing JSON.
---

# Musia Song Localization

## Purpose

Use this skill for Musia-style music localization: keep the song arrangement, rhythm, beats, chords, and melody, while adapting lyrics into another language and preparing singing synthesis artifacts.

## Non-Negotiables

- Do not present speech TTS as the final result for a singing localization request.
- Preserve the original music path whenever possible: `bass`, `drums`, `other` form `instrumental`; `vocals` or `human_sound` provide melody/timbre reference.
- Treat the four Demucs stems as `bass`, `drums`, `vocals`, and `other`.
- For Chinese output, adapt for singability: phrase duration, syllable/character count, rhyme, natural Chinese, emotional meaning, and tone-melody comfort.
- Same melody is not worth a bad song. If strict same-score localization makes the vocal unclear, robotic, badly pronounced, or musically weak, keep the artifact as experimental and regenerate a higher-quality independent version instead.
- Do not overfill the melody with translated meaning. Use 留白, held notes,
rests, and simpler hooks when the phrase needs musical space. Some phrases can
be sparse and some can be fuller; fit the song rather than cramming words.
- If singing model weights are not installed, produce a complete localization package and clearly mark vocal synthesis as blocked, not completed.
- Avoid cloning or imitating a real singer unless the user owns or has consent for that voice.
- Do not reuse one vocal render's lyric timeline for another render unless listening/ASR confirms the renders truly match.
- Planned/reference lyrics are correction evidence, not blind truth. The published lyric timing must follow the actual audible vocal, but close ASR word substitutions should be corrected back to the intended lyric when pronunciation, grammar, and phrase structure support the intended word.
- Before publishing, run a missing-planned-phrase audit: compare the source or
  planned lyric against the corrected active-vocal JSON and inspect ASR timing
  gaps plus long merged ASR segments. ASR can swallow short repeated phrases or
  soft poetic CJK phrases. If listening supports the planned phrase, add it back
  with real timing, translations, and ruby/pinyin; if not, document it as
  skipped. If the user later catches a missed phrase, patch the website data and
  redeploy rather than leaving the public lyrics stale.
- After generation, every target vocal must be transcribed and listened to
  independently before public lyrics are written. Prompt lyrics are not enough:
  if the English, Japanese, Chinese, Cantonese, or mixed render sings something
  else, correct to the audible line, mark it experimental, or regenerate.

## Local Musia Repo Workflow

Default repo path:

```text
/home/lachlan/ProjectsLFS/Musia
```

Runtime rule: use the unified `musia` conda environment for Musia Python tools.
Prefer the repo CLI wrapper because it automatically routes through
`conda run -n musia python ...`; only bypass it with `MUSIA_PYTHON` or
`MUSIA_NO_CONDA=1` when explicitly needed.

Run local analysis:

```bash
PYTHONNOUSERSITE=1 conda run -n musia python scripts/run_pipeline.py INPUT_AUDIO \
  --run-name RUN_NAME \
  --max-duration 120 \
  --asr-model base.en \
  --language en \
  --demucs-device cuda
```

Expected artifacts:

```text
data/runs/RUN_NAME/stems/bass.wav
data/runs/RUN_NAME/stems/drums.wav
data/runs/RUN_NAME/stems/vocals.wav
data/runs/RUN_NAME/stems/other.wav
data/runs/RUN_NAME/stems/instrumental.wav
data/runs/RUN_NAME/stems/human_sound.wav
data/runs/RUN_NAME/analysis/lyrics.json
data/runs/RUN_NAME/analysis/beats.csv
data/runs/RUN_NAME/analysis/chords.csv
data/runs/RUN_NAME/manifest.json
```

## Chinese Localization Package

For high-quality Chinese localization, create a package before synthesis:

```bash
python /home/lachlan/.codex/skills/musia-song-localization/scripts/create_localization_pack.py \
  --run-dir /home/lachlan/ProjectsLFS/Musia/data/runs/RUN_NAME \
  --target-language zh-CN \
  --target-lines TARGET_LINES.txt \
  --output-dir /home/lachlan/ProjectsLFS/Musia/data/runs/RUN_NAME/localization/zh-CN
```

The package should include:

- `target_lyrics.txt`
- `target_lyrics.json`
- `target_text_yingmusic.txt`
- `yingmusic_request.jsonl`
- `synthesis_status.md`

## Singing Backend Priority

1. **YingMusic-Singer-Plus**: preferred for lyric manipulation and same-melody Chinese/English editing. Use `vocals.wav` as melody reference and `target_text_yingmusic.txt` as target text.
2. **SoulX-Singer**: preferred when MIDI/F0 conditioning and zero-shot singing are ready.
3. **Full-song models** such as ACE-Step/YuE: only for inspiration/new-song modes, not strict same-music localization.

If using YingMusic-Singer-Plus, prepare:

```text
ref_audio = stems/vocals.wav or a consented timbre reference
melody_audio = stems/vocals.wav
ref_text = source phrase text if reliable
target_text = phrase1|phrase2|phrase3...
output = localized_vocal_zh-CN.wav
then mix localized_vocal_zh-CN.wav + stems/instrumental.wav
```

## Local Quality Backend Setup

The Musia repo contains helper scripts for large optional backends. Keep weights, envs, and caches local and ignored by git:

```bash
bash scripts/download_quality_backends.sh all
bash scripts/install_quality_envs.sh all
```

Validated local helpers:

```bash
bash scripts/run_soulx_env.sh .conda/soulxsinger/bin/python -c "import soulxsinger; print('soulx ok')"
bash scripts/run_moss_music_env.sh .conda/moss-music/bin/python -c "import torchcodec; print('torchcodec ok')"
```

When quality is poor, prioritize a short 20-40 second chorus/verse render through SoulX-Singer or a professional synth workflow before attempting a full song. Accept a render only if the vocal is clearly sung, audible, natural in the target language, and aligned to the original phrase rhythm.

## LLM Prosody And Rhyme Check

Before finalizing EN/JP/ZH target lyrics, run a lyric-quality review with the
best available LLM path: OpenAI, DeepSeek, or a strong Codex/GPT-5.5 xhigh
reasoning pass. Ask for a compact score and specific rewrites for:

- phrase rhythm and breath points against the melody/timing;
- musical space / 留白: where to hold vowels, leave rests, or simplify instead of adding words;
- rhyme / 押韵, including slant rhyme where exact rhyme sounds forced;
- English stress and singable end words;
- Mandarin natural wording, character count, rhyme group, and tone-melody comfort;
- Japanese mora flow, vowel endings, particles, and rhyme-like vowel echoes;
- meaning preservation and emotional force.

Do not let the LLM make the lyric verbose. Prefer short, concrete, singable lines
that a vocal model can pronounce clearly.

## Master-Companion Handoff

For original multilingual songs where the current full-song and strict
localization pipelines should remain unchanged, use the opt-in route:

```bash
musia master-companion \
  --title "Song Title" \
  --master-language ja \
  --master-audio master.mp3 \
  --run-analysis \
  --target-languages en zh-Hans \
  --control-policy quality-first
```

It creates a phrase map, chord/beat evidence, melody/F0 guide, target-language
LyricFit packets, soft companion prompts, and strict SVS handoffs. Treat strict
same-melody output as experimental until listening and ASR prove the vocal is
natural and clear.

## Website Lyric Protocol

For `fun.lazying.art`, use the `musia-fun-website-item` publication workflow before calling a website item finished. Use per-vocal `lyricSets[]` when generated or localized vocals differ by language, phrase count, repeated lines, or timing:

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

Each playable audio asset must set `lyricSetId`. The active vocal language owns timing and exact current-word highlighting. Other languages in the same set translate that active vocal's real sung lines and may rough-highlight corresponding tokens inside the same current `line.id`. If the vocal misses, changes, or repeats a planned line, reflect that fact.

Correct every public lyric set from at least two evidence sources: ASR/STT from the actual vocal plus input/reference lyrics, second ASR, or manual listening. When ASR and input disagree only on a close word, keep the input lyric if it is sound-close and makes better sentence/musical sense. Override the input only for real audible structure changes such as skipped, repeated, reordered, garbled, or clearly different lines. Add pinyin for Mandarin, furigana readings for Japanese kanji, and Jyutping readings for Cantonese. Run:

This correction must include a missing-planned-phrase pass: every source lyric
phrase should be accounted for as `audible`, `merged into line <id>`,
`added in timing gap <start-end>`, or `not audible/skipped`. Update the active
lyric JSON, translation JSON, manifest timeline, references, and website deploy
when this pass changes the public item.

For generated companion vocals, do this per vocal, not per project. The
Japanese public lyric set must be corrected against the selected Japanese
audio, the English set against the selected English audio, and the Chinese set
against the selected Chinese audio. Do not publish prompt-only lyrics or a
master vocal transcript as if it described another language render.

When handing a localized song to LazyEdit/Shipinhao Music, pass the corrected
active-vocal website lyric JSON as the publisher lyric source. Do not pass the
source lyric, target draft, master-language transcript, or another vocal's JSON
unless it was corrected against the selected audio.

```bash
npm run website:validate
musia fun-audit --media-id <media-id>
```

For mixed-language vocals, use one active sung/phonetic track plus translation tracks:

```text
lyrics/mixed-vocal/mul.json
lyrics/mixed-vocal/en.json
lyrics/mixed-vocal/zh-Hans.json
lyrics/mixed-vocal/ja.json
```

If a local model fails to sing native CJK script reliably in a mixed render, use pinyin/romaji for the sung input and display native Chinese/Japanese in translation tracks with pinyin/furigana. Document the compromise instead of claiming native-script singing.

Shared `textTracks[]` are acceptable only for strict same-timeline media.

For public Fun player videos, keep the website frame clean: two-line KTV lyric carousel, visible current-chord highlighting, native-language labels, and no bottom full-lyrics section in capture mode. Use:

```bash
musia fun-record --media-id <media-id> --skip-intro
```

## References

- Read `references/workflow.md` for the detailed localization workflow, quality gates, and failure modes.
- In the Musia repo, read `references/musia-song-generation-and-website-runbook.md` for song-generation and website publishing rules.
- In the Musia repo, read `references/fun-website-item-preparation.md` for the detailed website-item quality gate.
- In the Musia repo, read `references/musia-website-json-format.md` before editing website lyric JSON.
