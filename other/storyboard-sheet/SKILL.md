---
name: storyboard-sheet
description: >
  Runtime-neutral conversion of novels, scripts, outlines, or episode beats into
  short-drama storyboard sheets, shot lists, image prompts, and video-generation
  plans. Supports episode-level review sheets and shot-by-shot planning.
metadata:
  author: renoise
  version: 0.4.1
  category: video-production
  tags: [storyboard, short-drama, adaptation, image-generation, video-generation, portable]
---

# Storyboard Sheet / Short Drama Board

Turn source text into usable visual planning for short drama and AI video generation. Do not paste raw novel/script text into image prompts; first adapt it into visual beats.

Use only capabilities exposed by the current host. Planning works without generation capability. If the user asks to generate outputs, query live capabilities and hand the complete plan to the active host execution workflow. If generation is unavailable, return the complete plan and prompts in the conversation; never guess commands or require host filesystem access.

```text
source → adaptation bible → episode beats → shot list/sheet plan → references → prompts → optional generation → QA → targeted rerun
```

## 1. First Ask: What Output?

If unclear, ask once:

```text
你要哪种输出？
A. 每集一张 storyboard sheet，用于预览/审稿
B. 每个 shot 单独一张图，用于后续视频生成
C. 两者都要：先 sheet 审稿，再拆 shot 图和视频 prompt
```

Default for short-drama/video work: B or C, not only a sheet.

### A. Storyboard Sheet / 审稿预览

```text
one episode = one image containing multiple panels
```

Good for pitch, visual overview, client review, and director preview. It is not ideal as direct video-model input.

Default:

```text
panels: 6
layout: 2×3
ratio: 16:9 unless user wants vertical short drama
text: only tiny P1-P6 labels
```

### B. Shot-by-shot / 视频生成

```text
one shot = one image prompt + one video prompt
```

Good for video generation, first-frame workflows, and precise continuity.

Default for short drama:

```text
ratio: 9:16
shots per 60-90s episode: 8-12
style: vertical mobile drama, close-up heavy, emotion readable
```

## 2. Short Drama Adaptation

Build an adaptation bible in the conversation:

```text
- title / genre
- main characters and relationships
- protagonist desire
- core conflict engine
- must-keep plot points
- secrets / reveals / reversals
- recurring locations
- visual motifs
- continuity constraints: age, wardrobe, injuries, props, money, rules
```

Each episode should usually follow:

```text
opening hook → setup → conflict → escalation → reversal/reveal → cliffhanger
```

Rules:

- Internal thought → visible action, prop, expression, or dialogue.
- Long exposition → conflict scene or reaction beat.
- One beat must be visually clear in one shot/panel.
- Keep the first three seconds strong.
- End with a hook, reversal, danger, or emotional question.
- Prefer faces, reactions, hands, phones, doors, documents, money, wounds, and reveals over abstract narration.

## 3. Character and Scene References

A character appearing more than once needs one approved visual anchor; do not rely on text description alone. Use a user-authorized image or create a reference through the host's generation flow, show it for approval, and reuse the same resulting material through a role advertised by the selected model.

Character reference prompt:

```text
角色设定图，干净背景，现实主义竖屏短剧风格。
[角色名]，[年龄]，[身份]，[体型]，[发型]，[五官/气质]。
固定服装：[服装]。
包含正面全身、半身近景、侧面小头像，必须像同一个人。
不要水印，不要多余文字，不要夸张动漫风。
```

For recurring locations, create a scene reference only when needed. Too many references can confuse layout and identity.

Before optional generation, read `../model-routing/SKILL.md`, then:

1. Query live image-model capabilities.
2. Preserve a user-selected model; otherwise choose the best available specialist for the shot/sheet task and use the advertised default only as fallback.
3. Apply that model's prompting profile and use only advertised ratio, resolution, duration, material roles, and limits.
4. Hand the complete prompt, references, and parameters to the active host execution workflow.
5. Record any task identifier returned by the host before waiting or polling.

## 4. Output Templates

### Episode Sheet Plan

```json
{
  "episode": 1,
  "title": "...",
  "hook": "...",
  "panels": [
    {"panel": "P1", "beat": "opening hook", "visual": "..."},
    {"panel": "P2", "beat": "setup", "visual": "..."},
    {"panel": "P3", "beat": "conflict", "visual": "..."},
    {"panel": "P4", "beat": "escalation", "visual": "..."},
    {"panel": "P5", "beat": "reveal/reversal", "visual": "..."},
    {"panel": "P6", "beat": "cliffhanger", "visual": "..."}
  ]
}
```

Sheet prompt:

```text
一张完整的电影分镜 storyboard sheet，严格 2行3列，共6个清晰 panel，黑色细边框。
现实主义短剧风格，角色与参考图一致，服装/年龄/发型不变。
不要水印，不要长文字，只允许很小的 P1-P6 编号。

第[N]集《[标题]》：
P1 ...
P2 ...
P3 ...
P4 ...
P5 ...
P6 ...
```

### Shot List for Video Generation

```json
{
  "episode": 1,
  "title": "...",
  "shots": [
    {
      "shot": "EP01_SH01",
      "duration": "4s",
      "framing": "tight close-up / medium / over-shoulder / insert",
      "visual": "what we see",
      "action": "one clear action only",
      "emotion": "specific readable emotion",
      "camera": "simple camera move or static",
      "image_prompt": "first-frame image prompt",
      "video_prompt": "motion prompt for video model"
    }
  ]
}
```

Video-friendly rules:

- One shot = one action.
- Avoid time jumps inside one shot.
- Avoid complex crowd/blocking unless necessary.
- Use simple camera language: static, slow push-in, handheld slight shake, over-shoulder.
- Keep text/UI minimal; exact generated text often fails.
- Generate first frames individually, not from a multi-panel sheet.

## 5. QA

Story QA:

```text
[ ] hook is strong enough
[ ] episode order is correct
[ ] no false plot events
[ ] reveal/cliffhanger matches adaptation
[ ] internal monologue became visible action
```

Visual QA:

```text
[ ] correct characters, age, wardrobe
[ ] consistent face/hair/body
[ ] correct location/time/props
[ ] layout correct if sheet
[ ] shot is usable as first frame if video workflow
[ ] no harmful/confusing generated text
```

Give a direct result:

```text
Keep: EP01, EP02
Rerun: EP03_SH04 - character age drifted; EP04 sheet - layout became poster
```

Rerun only failed sheets/shots unless the whole visual system is wrong. Preserve approved references and add the specific failed constraint to the revised prompt.

## 6. User-Facing Summary

Keep the explanation short:

```text
我会先把原文改成短剧节奏：开场钩子、冲突升级、反转和集尾悬念。
如果是审稿，我做每集一张 storyboard sheet；如果要生成视频，我会拆成逐 shot 的首帧图 prompt 和视频 prompt，并用角色 reference 保持一致。
```
