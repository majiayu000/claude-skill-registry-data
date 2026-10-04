---
name: ai-short-drama-director-kit
description: "Use this skill when the user wants an AI short-drama director tool library, wants Codex to choose among director/cinematography/commercial/story skills, or asks for screenplay, shot design, visual style, hooks, comedy, action, emotional polish, or multi-skill creative direction. It routes selectively across the installed skills: zhou-xingchi-director, peter-pau-cinematography, johnnie-to-staging, wong-kar-wai-emotion, tsui-hark-fantasy-action, ning-hao-black-comedy, wong-jing-commercial-hooks, zhang-yimou-visual-ritual, and ang-lee-emotional-realism."
---

# AI Short Drama Director Kit

## Role

Use this as the top-level routing skill for AI短剧导演工作. It should not load every director method by default. Select only the layers needed for the user's task, then read the corresponding skill files.

## Installed Creative Layers

- **Comedy / 小人物 / 桥段**: `zhou-xingchi-director`
- **Cinematography / 光影 / 构图**: `peter-pau-cinematography`
- **Spatial staging / 群像 / 黑色压力**: `johnnie-to-staging`
- **Mood / 时间 / 记忆 / 暧昧**: `wong-kar-wai-emotion`
- **Fantasy action / 武侠 / 奇观**: `tsui-hark-fantasy-action`
- **Grounded black comedy / 多线因果**: `ning-hao-black-comedy`
- **Commercial hooks / 爽点 / 追更**: `wong-jing-commercial-hooks`
- **Symbolic visuals / 色彩 / 仪式**: `zhang-yimou-visual-ritual`
- **Emotional realism / 克制 / 潜台词**: `ang-lee-emotional-realism`

## Selection Rules

1. For a first draft short drama, start with `wong-jing-commercial-hooks` for retention, then add one story tone layer and one visual layer.
2. For comedy, pair `zhou-xingchi-director` with either `ning-hao-black-comedy` (grounded) or `wong-jing-commercial-hooks` (commercial).
3. For image generation or visual frames, start with `peter-pau-cinematography`; add `zhang-yimou-visual-ritual` for symbolic color/ceremony or `wong-kar-wai-emotion` for mood.
4. For scenes where people stand and talk, use `johnnie-to-staging` before adding dialogue.
5. For action or AI spectacle, use `tsui-hark-fantasy-action`, then stabilize emotion with `ang-lee-emotional-realism`.
6. For "make it less AI," use three passes: human pressure, visible business, and production constraints.

## Workflow

1. Diagnose the task: story, scene, visual, image prompt, episode structure, character, action, comedy, or polish.
2. Pick at most 3 skills for the first pass.
3. Read only those skills and their relevant references.
4. Produce a layered output: hook/story, scene mechanics, visual plan, performance notes, production prompt.
5. Name which layers were used so the user can steer taste.

## Library Reference

Read `references/layers.md` for a compact matrix of which skill to use by creative problem.
Read `references/manifest.md` when you need the full installed library inventory, paths, and layer map.
Use `cinema-director-master-library` when the user asks for broader director references beyond the existing focused skills, especially for a 50-director master roster across fantasy, magic, Chinese/eastern, western, romance, fighting, period, friendship, freedom, rhythm, and narrative.
