---
name: storyboard
description: Build a complete storyboard package from a script, narration, topic, approved world-design run, or existing material. Confirms production scope in one line, then delivers storyboard images, five prompt types, an asset index, and a combined visual-prompt XLSX. Use this whenever the user mentions 做分镜、生成分镜、拆镜头、把剧本拆成镜头、关键帧、图生视频提示词、智能多帧、全能参考、即梦分镜、分镜表, asks to control production volume or token cost, or invokes $storyboard — including when they describe the task without using the word 分镜.
---

# Storyboard

The single public entry from source material to a production-ready storyboard package.

## Route

1. Infer the source from the conversation, attached files, and current project. If an unfinished `storyboard_runs/` directory matches this source, resume it instead of starting over.
2. Read `../research-grounded-storyboard-pipeline/references/production-configuration.md` and `.../quality-floor.md`.
3. Parse the full source. Establish duration and per-scene durations. Extract the narration into segments and run `validate_script_capacity.py` — if the script holds more words than its running time allows, say so and wait for the user to cut text or extend the film before going further. Resolve the evidence mode: `strict_evidence`, `hybrid_evidence`, or `fiction_consistency`.
4. Estimate `compact` / `standard` / `detailed` when a comparison helps the decision.
5. Treat explicit user values and stable project values as confirmed. Present one compact approval line for the remaining open choices, including the expected image count.
6. Record confirmed values in `planning/production_config.json`.
7. Follow `../research-grounded-storyboard-pipeline/SKILL.md`.
8. Follow `../research-grounded-world-design/SKILL.md` when recurring entities need stable visual assets, or when an approved world-design run exists.
9. When the input is only a topic or loose concept, develop it into a script first, then continue from step 3.

## Delivery Boundary

Keep the configuration card, estimates, gates, manifests, and QA inside the run. The public reply opens with the approved storyboard gallery, then concise shot cards, five prompt routes, and downloadable files. One approval line before, one status line after.

## Defaults

- `standard` depth, all five prompt routes, `approval_sample` images. Move to `all_selected` only after the user accepts the full count.
- Full storyboard field set at every depth; one beat, one primary action, one camera intent per shot.
- `standard` 2–3s grain, 1.5–4s working range; override reasons attached to outliers.
- Camera recorded as enumerated `shot_size` / `camera_angle` / `camera_movement` plus a unique per-shot note; on-screen text declares `generation` or `post`, and anything that moves is `post`.
- One project `style_token`; image prompts carry what is unique to the frame plus that token, nothing else.
- Bible sections declared per project — `style` and `continuity` always, everything else only if the project contains it.
- Real entities bind to evidence IDs and visual fact cards; invented entities bind to world asset IDs.
- Every shot gets an anchor keyframe; cadence, action-turn, and handoff frames follow the confirmed interval.
- Transitions and group handoffs stay inside a scene.
- One complete image per selected keyframe, registered immediately.
- Workbook opens on `关键帧图文`; `制作配置` and `QA` last as internal control sheets.
- Reuse the project's existing aspect ratio, style, duration, and reference directories when clear.
- Ask one concise question only when two source projects or creative directions are equally plausible.

Invoke with `$storyboard 用这个剧本做分镜。` or any natural phrasing carrying the same intent.
