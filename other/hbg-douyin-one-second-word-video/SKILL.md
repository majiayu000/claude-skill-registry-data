---
name: douyin-one-second-word-video
description: >-
  Create and revise 9:16 Chinese Douyin “一秒钟记一个单词” mnemonic videos for one English word
  using deterministic HyperFrames HTML/CSS/SVG/GSAP and Edge TTS. Use when a user supplies an
  English word and wants the approved chalkboard structure: headword and IPA from frame zero,
  Chinese phonetic mnemonic revealed only when spoken, phonetic chunks assembling into the word,
  a natural annotated example, “所以”, four spoken repetitions, and a final meaning plus IPA. Also
  use to batch or standardize this exact vocabulary-video format. Do not use Qwen or image/video
  generation models.
---

# Douyin One-Second Word Video

Create one complete vertical vocabulary video per English word. Preserve the approved structure; vary only the word-specific mnemonic, SVG example, copy, and speech-aligned timing.

## Required companions

Read and apply `hyperframes`, `hyperframes-core`, `hyperframes-cli`, `hbg-douyin-code-explainer-video`, GSAP, and `code-video-visual-qa`. Use code-only HTML/CSS/SVG/GSAP.

## Non-negotiable format

- Render 1080×1920 at 24 fps.
- Use Edge TTS `zh-CN-XiaoxiaoNeural` at `+20%` unless the user overrides it.
- Generate one continuous semantic narration turn. Never use Qwen.
- Do not use image-generation or video-generation models.
- Do not add BGM unless requested.
- Create a new project or revision path; never overwrite an approved MP4.
- Read [references/proven-structure.md](references/proven-structure.md) before writing the storyboard or composition.

## Workflow

1. Generate at least two candidate sound-chunk splits. Prefer two or three chunks that map to Chinese units and can form a short causal story, even when the English word is technically one syllable. Call them sound chunks, not syllables. Use a single whole-word mnemonic only when every plausible split makes the pronunciation unrecognizable or cannot produce a natural mini-story; record the rejected candidates in `BRIEF.md`.
2. Choose short Chinese sound mnemonics that combine into a meaningful action, image, or mini-event. Prefer a memorable natural phrase over a forced transliteration; admit approximation through the visual mapping instead of adding explanatory clutter.
3. Write a conversational semantic bridge. Use a concrete action or object that naturally produces the English meaning. Reject sentences that merely concatenate the mnemonic and definition.
4. Write `BRIEF.md`, `SCRIPT.md`, and `STORYBOARD.md` before the composition.
5. Generate Edge TTS with [scripts/generate_edge_tts.py](scripts/generate_edge_tts.py). Use the emitted word boundaries as the timing source.
6. Build the static hero frames first, then add seek-safe GSAP motion.
7. Run HyperFrames `check`, inspect source snapshots, render a new high-quality MP4, then inspect the same timestamps from the encoded MP4.
8. Run [scripts/final_media_qa.sh](scripts/final_media_qa.sh) on the final revision.

## Copy contract

Use this narration arc, adapting punctuation for natural Edge TTS delivery:

```text
一秒钟记一个单词，今天要记的是 <word>，<meaning>。
<Chinese mnemonic units, spoken in Chinese only>。
窍门：<mnemonic>！你看，<natural concrete example that ends in the meaning>！
所以，<word>！<word>！<word>！<word>！<meaning>。
```

Keep the example short enough to fit in at most four large lines. Put the pronunciation hint directly beside the Chinese mnemonic and put `(<word>)` beside the result meaning. Ensure parentheses remain visible during scale emphasis by giving annotation spans explicit horizontal margin.

## Completion gate

Deliver only after all of these pass:

- Frame zero contains only the word, IPA, and meaning—never the mnemonic.
- The mnemonic uses at least two sound chunks whenever a defensible split exists. If a rare one-chunk fallback is used, record in `BRIEF.md` why the attempted splits failed pronunciation or story naturalness.
- English chunks are visible before mnemonic speech, while Chinese mnemonic units appear one by one on their Chinese TTS boundaries.
- The narration never reads English split chunks.
- Assembly reuses the same live chunk elements, closes every gap, and holds the complete word clearly before the next beat.
- The example reads naturally and its annotations are unobscured.
- The final frame retains four word echoes, the meaning, and the IPA.
- Final MP4 is H.264/yuv420p, 1080×1920, 24 fps, AAC stereo 48 kHz, faststart, with no black frames or unexplained long silence.
- Full-resolution frames were inspected from the encoded MP4, not only from source snapshots.
