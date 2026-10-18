---
name: guozhi-video-breakdown
description: Extract evidence from Xiaohongshu, Douyin, TikTok, Reels, Shorts, Bilibili, or local talking-head short videos, dissect viral hooks, captions, retention, editing, and conversion design, then generate original replication scripts. Use when the user asks "拆解小红书爆款", "抖音口播复刻", "爆款口播脚本", "拉片这个视频", "黄金3秒", "复刻脚本", or wants a publish-ready short-video script from a sample. Do not use for generic content calendars, raw transcription only, long film analysis, private/paywalled content bypassing, or copying another creator's exact wording/persona/assets.
---

# 果汁视频拆解

Turn a short-form talking-head sample into evidence-backed viral teardown and an original script package for Xiaohongshu or Douyin.

## Operating Principles

- Evidence first: inspect frames, contact sheets, subtitles, transcript, title, cover, and visible comments before judging why it worked.
- Separate raw facts, inferred intent, and reusable pattern.
- Learn mechanisms, not expressions: never copy exact wording, creator persona, watermark, private screenshots, face, voice, or proprietary assets.
- Optimize for Chinese short-video口播: first 3 seconds, subtitle rhythm, retention turns, trust proof, save/comment triggers, and a script that can be recorded.
- Do not bypass login walls, paywalls, private posts, platform restrictions, or rate limits. If a link cannot be downloaded, ask for a local file, transcript, screenshots, or exported subtitles.

## Workflow

1. **Clarify the task only when needed.**
   - If the user already provides a video/link/transcript and wants拆解/复刻, proceed.
   - If the output target is missing, default to a 45-60 second Xiaohongshu口播 script.
   - Ask only if both the sample and target niche/topic are missing.

2. **Build the evidence packet.**
   - For a local video or public URL, read `references/evidence-extraction.md` and run `scripts/extract_video_evidence.sh` when the environment has `yt-dlp`, `ffmpeg`, and `whisper`.
   - For transcript/subtitles only, skip visual claims and mark visual evidence as unknown.
   - For screenshots/contact sheets only, analyze visual rhythm and caption style but mark口播 as unknown.

3. **Dissect the viral mechanism.**
   - Read `references/viral-autopsy-framework.md`.
   - Cover: target audience, emotion, topic promise, title/cover, first 3 seconds, segment structure, retention nodes, proof, gold lines, visual materials, editing rhythm, conversion trigger, and replication boundary.

4. **Generate an original replication package.**
   - Read `references/replication-output-template.md`.
   - Produce: title candidates, cover text, 3 hook variants, full口播稿, timeline/storyboard, subtitle/flower-text plan, materials list, editing notes, CTA/comment trigger, and risk notes.

5. **Validate before final delivery.**
   - Confirm whether `contact_sheet`/frames were inspected when available.
   - Confirm whether transcript/subtitles were read when available.
   - Mark missing evidence explicitly.
   - Check the new script changes audience, story, proof, wording, and assets enough to avoid copying.

## Resource Routing

- Read `references/evidence-extraction.md` when handling a video file, URL, audio file, subtitle, transcript, screenshot set, or contact sheet.
- Read `references/viral-autopsy-framework.md` for any爆款拆解,黄金3秒, retention, or口播机制 analysis.
- Read `references/replication-output-template.md` whenever the user wants复刻脚本, publish-ready口播稿, title candidates, or a production plan.
- Read `references/test-prompts.md` when validating trigger behavior or reviewing this Skill.
- Run `scripts/extract_video_evidence.sh` only for local files or public URLs that the user is allowed to analyze.

## Validation

For Skill structure:

```bash
python3 /Users/guozhi/.codex/skills/standard-skill-maker/scripts/validate_skill.py <this-skill-folder>
```

For the extraction script:

```bash
bash -n scripts/extract_video_evidence.sh
```

For a real run, test with a short local sample first:

```bash
scripts/extract_video_evidence.sh "/absolute/path/to/sample.mp4" outputs/sample-evidence 1 small zh
```
