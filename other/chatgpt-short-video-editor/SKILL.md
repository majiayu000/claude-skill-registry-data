---
name: chatgpt-short-video-editor
description: "Edit a user-supplied video into a vertical Reel, Short, TikTok, video diary short, or an approved eight-step AI short-video workflow. Use when the user provides or points to media and asks to transcribe, cut, subtitle, preview, or export a vertical short. Do not use for environment-only setup or generic Premiere Pro or CapCut help."
---

# ChatGPT Short-video Editor

Create a safe, evidence-backed vertical short from user-provided media. This
Skill starts only when a source file or clear source location is available.

## Boundary and prerequisites

1. Inspect the source with `ffprobe`; never overwrite, move, rename, or delete
   it. Put every new artifact beside the source in `<source-directory>/edit/`.
2. Check that the installed `video-use` workflow, `FFmpeg`, `ffprobe`, and
   ElevenLabs Scribe v2 are available for the documented full-precision path.
   Do not install, clone, update, or repair anything silently. If a dependency
   is missing, hand off to `chatgpt-video-editing-setup` and state what must be
   verified first.
3. Before the first upload of a source file to ElevenLabs, name the file, say it
   is for ElevenLabs Scribe v2 transcription, mention possible quota or cost,
   and wait for explicit consent. Do not upload before that consent.
4. Read [the eight-step workflow](references/eight-step-workflow.md), then
   [the production rules](references/production-rules.md), before editing.

## Required sequence

Follow these eight steps exactly: 素材檢查、逐字轉寫、內容整理、剪輯決策、逐段粗剪、轉色／圖卡／字幕、混音與完整預覽、QA 與正式定稿.

After the first three steps, propose a 4–8 sentence, plain-language editing
strategy and wait for approval. Until approval, do not choose edit points or
add B-roll, animations, music, effects, CTA, or a publishing schedule. Treat
these as opt-in creative decisions, not defaults.

Use word-level verbatim timestamps, cached per unchanged source. Never cut
inside a word. Keep 30–200ms padding around cut edges, work per segment, and
use output-timeline subtitle timing. Subtitles are the last visual operation.

Render a complete 720p preview first. Inspect the rendered preview, not only
the source; make no more than three evidence-based self-fix passes. After the
preview is approved, render the 1080×1920 final and verify that final file
before delivery. Never say a transcript, preview, QA pass, or final is
complete without the corresponding verified output.

## Handoff and delivery

If the requested operation exceeds this workflow, explain the safe stopping
point. For environment gaps, use `chatgpt-video-editing-setup`; it must obtain
approval before mutations and does not begin creative work.

Keep and report the artifacts defined in [the output contract](references/output-contract.md).
Present only one formal final outwardly, with its evidence-backed QA report.
