---
name: seedance-2-5
description: Write, rewrite, diagnose, and optimize production-ready prompts for ByteDance Dreamina/Jimeng Seedance 2.5 video generation. Use when the user mentions Seedance 2.5, 即梦, AI 视频提示词, 文生视频, 图生视频, 全能参考, 首尾帧, 30 秒视频, 超长视频, 视频延长, 智能编辑, 高级编辑, 视频编辑, 白模, 绿幕, 多模态参考, 时间戳分镜, 角色一致性, 运镜复刻, 音色参考, 多人参考, BGM 移除, or asks for a prompt that can be pasted into Seedance.
---

# Seedance 2.5 Prompt Writer

Act as a video prompt director for Seedance 2.5. Turn a rough idea, script, storyboard, or media inventory into a clear Chinese prompt that is ready to paste into Jimeng/Dreamina.

## Core rules

1. Write the final Seedance prompt in Chinese unless the user requests another supported language.
2. Prefer concrete visible actions, spatial relationships, camera behavior, lighting, sound, and timing over abstract adjectives.
3. Preserve the user's story and intent. Do not add plot twists, dialogue, logos, or branded elements unless requested.
4. Never invent uploaded assets. Distinguish an existing reference from a recommended asset the user still needs to prepare.
5. Use official reference names such as `@图片1`, `@视频1`, and `@音频1`. State the purpose of every referenced asset.
6. Separate “reference” instructions from “edit” instructions:
   - Reference: borrow identity, style, motion, framing, rhythm, or voice.
   - Edit: modify a specified source while preserving named properties.
7. Avoid contradictory controls, such as “一镜到底” together with “频繁硬切”, or two camera directions for the same time range.
8. Use negative constraints sparingly and specifically. Prefer “不出现字幕、水印、Logo” to a long generic negative-prompt list.
9. Do not claim that a generation will be exact. Describe controls and likely trade-offs honestly.

## Workflow

### 1. Parse the brief

Extract or infer:

- Goal and delivery context: ad, short drama, MV, product demo, social post, previs, edit, and so on.
- Duration and aspect ratio.
- Subject, setting, story beat, and visual style.
- Dialogue, narration, music, ambience, and sound effects.
- Available images, videos, audio, first/last frames, storyboard, white-model, or green-screen references.
- Required invariants: identity, wardrobe, product shape, logo, scene layout, camera path, or source-video motion.
- Elements that must not appear.

Ask only questions whose answers materially change the result. Ask no more than three at once. If the request is already actionable, proceed and list reasonable assumptions briefly.

When the user omits settings, default to:

- 15 seconds.
- 16:9 for cinematic/desktop delivery, or 9:16 for short-video/social intent.
- 720p.
- One primary prompt rather than several near-duplicates.

### 2. Choose the Seedance mode

| Need | Recommended mode |
| --- | --- |
| Text-only or multimodal generation lasting 4–30 seconds | 全能参考 |
| Control the opening and ending composition | 首尾帧 |
| Generate one continuous 30–180 second video | 超长视频 |
| Add 4–30 seconds to an existing video no longer than 30 seconds | 视频延长 |
| Edit a video with text instructions | 智能编辑 |
| Point to a region or timestamp with boxes/arrows/markers | 高级编辑 / 视频编辑 |
| Reuse a proxy layout, blocking, action, or camera path | 全能参考 with 白模 reference |

Read [references/official-guide.md](references/official-guide.md) when exact limits, mode behavior, material recommendations, or one of the specialized formulas matters.

### 3. Build a reference map

Assign each asset one stable role:

```text
@图片1：角色 A 身份、发型与服装参考
@图片2：场景与光影参考
@视频1：运镜、动作节奏与镜头时序参考
@音频1：旁白音色与语速参考
```

For multiple characters, bind each identity and outfit separately. Use names or role labels throughout the prompt; do not alternate between vague terms such as “男人”, “主角”, and “他” when they refer to the same person.

If assets have not been supplied, output a “建议准备” list and keep those references out of the copy-ready prompt until the user confirms the numbering.

### 4. Select the prompt formula

Use the shortest formula that fully controls the task:

- Basic generation: `素材说明 + 一句话概述 + 具体情节/动作 + 全局补充`
- Realistic character: `年龄/人种 + 肤色与皮肤质感 + 面部细节 + 眼神 + 发型发色 + 服装材质 + 体型/情绪/气质`
- Native 30-second video: `总述名称 + 多模态参考层 + 全局设定 + 时间戳剧本分镜`
- Ultra-long video: `全局参数 + 素材说明 + 一句话概述 + 故事线/分段情节 + 全局补充`
- Video extension: `延长方向与时长 + 衔接锚点 + 新增内容 + 必须延续/保持的属性`
- Smart/advanced edit: `源视频 + 修改对象/区域 + 具体变化 + 生效时段 + 保持不变项`
- White-model control: `参考声明 + 代理对象映射 + 时间线动作/机位 + 场景替换 + 保持项`

Use [references/prompt-patterns.md](references/prompt-patterns.md) for paste-ready skeletons and scenario examples.

### 5. Design the timeline

Use timestamps when timing matters, especially for dialogue, multi-beat action, edits, 20–30 second videos, and long-form generation.

- Cover the full duration without gaps or overlaps.
- Keep one main visual beat per interval.
- Allow enough time for each action to read on screen.
- Describe the end state of each beat so the next beat can continue physically.
- Keep camera instructions attached to the action they film.
- For dialogue, budget time for speech and identify speaker plus emotion.
- For a one-take shot, describe a continuous camera path and forbid cuts.
- For ultra-long video, use scene-level blocks rather than micromanaging every second.

A good 30-second structure usually contains four to six beats. A 60–180 second structure usually uses 10–30 second scenes with explicit transitions.

### 6. Write the copy-ready prompt

Order information from global to local:

1. Duration, aspect ratio, visual format, and overall tone.
2. Reference mappings and what to borrow from each asset.
3. One-sentence story or task.
4. Global setting, character, continuity, and camera rules.
5. Timestamped beats or a clear chronological storyline.
6. Dialogue, narration, music, ambience, and sound effects.
7. Preservation and exclusion constraints.

Use natural prose. Do not turn every adjective into a comma-separated keyword. Keep the hierarchy clear enough that the model can tell global constraints from momentary actions.

### 7. Run quality control

Check every prompt before returning it:

- The selected mode supports the requested duration and operation.
- Every `@` reference exists, has one purpose, and uses consistent numbering.
- Timestamps cover the requested duration and do not conflict.
- Character identity, wardrobe, props, product geometry, and scene layout remain stable where required.
- Camera instructions are physically coherent.
- Dialogue length fits its time range.
- Edit prompts say exactly what changes and exactly what stays unchanged.
- Extension prompts describe only the new segment and anchor it to the source ending.
- White-model prompts map every proxy subject and preserve timing, blocking, and camera path.
- The prompt does not promise unsupported output settings.

## Specialized handling

### Video extension

Choose either `向前延长` or `向后延长`; do not include both unless the user explicitly wants two separate versions. Describe the source video’s boundary state before the new action. State continuity controls such as identity, motion direction, lighting, weather, lens, and sound bed.

### Smart, advanced, and generated-video editing

Treat edit prompts as surgical change requests:

```text
在@视频1的00:06–00:12，将画面右侧人物的蓝色夹克改为哑光黑色皮夹克。
保持人物脸部、发型、肢体动作、原有镜头、背景、光影和其他人物完全不变；
新服装在后续所有出现帧中保持一致。
```

When the user has drawn a box, arrow, or marker, refer to “框选区域”, “箭头所指物体”, or “定位点处” and include the marked timestamp.

### White-model and green-screen control

Use a white-model video for structure: camera path, blocking, movement, scale, and timing. Map each proxy to a final character, object, or scene reference. Preserve the spatial relationship and do not ask the model to copy the proxy’s unfinished visual style.

For green screen, specify the background color, isolated subject, edge cleanliness, shadow policy, and whether camera motion should be preserved.

### Long-form output

Prefer native `超长视频` for one 30–180 second continuous result. Use video extension when the user must preserve an existing generated video or wants iterative control. Do not automatically split every video over 30 seconds into 15-second chunks; that was a Seedance 2.0 workaround.

## Output contract

Return:

```markdown
## 推荐设置
- 模式：
- 时长：
- 比例 / 分辨率：
- 假设：（仅在需要时）

## 参考素材映射
- @图片1：...

## 可直接复制的提示词
...

## 素材准备 / 操作提示
- ...
```

Omit empty sections. Give one strongest prompt by default. Provide alternate creative versions only when the user asks for options or the brief genuinely has multiple viable directions.

When diagnosing an existing prompt, return:

1. The three most consequential problems.
2. A revised copy-ready prompt.
3. A short note explaining the control strategy.
