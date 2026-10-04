---
name: clean-lecture-notes
description: "Clean lecture transcripts, meeting transcripts, class recordings, ASR output, Feishu/Lark docx transcripts, local Markdown/text transcripts, and courseware into review-ready study notes. Use when the user asks for transcript cleanup, lecture notes, course notes, classroom recording cleanup, study-note generation, Mermaid mindmaps, Feishu/Lark writeback, or 中文任务 such as 清洗录音转文字、清洗逐字稿、整理上课录音、整理课堂笔记、把录音和课件做成笔记、生成复习版笔记、写回飞书。"
---

# Clean Lecture Notes

## Overview

Use this skill to turn noisy lecture transcripts, meeting transcripts, class recordings, Feishu/Lark docs, local ASR output, and optional courseware into reliable cleaned transcripts and review-ready study notes.

Default to preserving the original transcript. Unless the user explicitly asks to overwrite a source document, create new cleaned transcript and study-note artifacts.

## Workflow

1. Identify the source:
   - Local transcript file: read it directly.
   - Local audio or video: use the user's available transcription or meeting-minutes tooling first, then continue from the transcript.
   - Feishu/Lark Minutes URL: if Feishu/Lark tools are available, fetch the transcript before cleaning.
   - Feishu/Lark docx transcript URL: if `lark-doc` is available, fetch the source doc before cleaning.
   - Courseware URL or file: extract its title, module order, core diagrams, and assignments; use it as the study-note spine.
2. For transcript cleanup only, read `references/transcript-cleaning.md` and produce a cleaned transcript.
3. For study notes, read both `references/transcript-cleaning.md` and `references/study-note-workflow.md`.
4. For Feishu/Lark output, read `references/feishu-output.md`; treat Feishu/Lark as optional integration, not a hard dependency.
5. Before final delivery, read `references/quality-checklist.md`.
6. When local note artifacts exist, run `scripts/check_note_artifacts.py`; for final study notes, include `--final-note`.

## Output Contract

- Cleaned transcript: remove filler words, repeated fragments, ASR noise, broken punctuation, and fragmented paragraphs while preserving meaning, examples, names, numbers, assignments, caveats, and event order when relevant.
- Study notes: include a Mermaid mindmap or knowledge map, time-boxed review path, core conclusions, active recall questions, conceptual modules, practice/project migration items, interview-ready wording when useful, and sources.
- Emphasis: bold the first occurrence of core concepts, key methods, important metrics, and high-value sentences; do not bold entire paragraphs.
- Perspective: final study notes must use a learner review and transfer perspective. Do not write them as class minutes, a meeting recap, or "the teacher said..." narration.
- Pending information: cleaned transcripts may keep speaker labels and pending checks; final study notes must not include a standalone `待确认` section. Put unresolved factual uncertainty in the source and quality audit section.
- Feishu/Lark output: default to creating new docs, verify outlines after writing, and ensure the top `思维导图` section is a Mermaid flowchart or equivalent visual whiteboard rather than a plain text tree.

## Optional Integrations

- Use Feishu/Lark tools only when they are available in the current Codex environment or the user explicitly asks for Feishu/Lark writeback.
- When Feishu/Lark tooling is unavailable, produce local Markdown artifacts and clearly state that remote writeback was skipped.
- For visual study-note overviews, prefer Mermaid `flowchart TD` or `flowchart LR`.

## Safety Rules

- Never write secrets, API keys, access tokens, `.env` values, private Feishu/Lark links, or credentials into notes, logs, examples, or commits.
- Do not overwrite or delete source transcripts unless the user explicitly asks for it.
- Mark uncertain ASR corrections briefly instead of turning guesses into facts.
- Do not add analytics, telemetry, or unrelated network calls.

## Final Response

Report:

- the local output paths or Feishu/Lark document URLs created,
- whether the source transcript remained unchanged,
- which validation commands were run,
- any unresolved terminology or source-quality caveats.
