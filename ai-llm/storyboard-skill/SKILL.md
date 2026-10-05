---
name: storyboard-skill
description: Build and manage AI image storyboard workflows with compact project files, scene/shot tracking, character and visual bibles, continuity checks, structured image prompts, fix prompts, and thread-safe context minimization. Use when Codex is asked to create, organize, review, or generate prompts for storyboard scenes, shot lists, ChatGPT Image/Image 2 workflows, image-to-image revisions, visual continuity, or production trackers.
---

# Storyboard Skill

## Core Rule

Optimize for low context use. Keep story, character, style, scene, shot, prompt, and review information in files. Load only the files needed for the current task, usually 1-3 files.

Never ask the user to paste an entire bible or long thread when a compact project file can be created or updated instead.

## Workflow

1. Identify the task type:
   - **Setup**: Create a project structure, bibles, shot list, or tracker.
   - **Prompting**: Convert a scene or shot into image prompts.
   - **Fixing**: Create targeted image-to-image or regeneration prompts.
   - **Review**: Check continuity, scene coverage, or prompt consistency.
   - **Packaging**: Prepare storyboard notes for a deck, document, or handoff.

2. Use the smallest useful context:
   - For character details, read `bible/character_bible.md`.
   - For visual rules, read `bible/visual_style_bible.md`.
   - For continuity rules, read `bible/continuity_rules.md`.
   - For a specific scene, read only that `scenes/scene_##.yaml` or `shots/scene_##_shots.yaml`.
   - For prompt formatting details, read `references/prompt-patterns.md`.
   - For platform safety, NSFW, likeness, or restricted-content checks, read `references/prompt-safety-checklist.md`.
   - For project layout details, read `references/project-structure.md`.
   - For examples of expected output shape, read only the relevant file in `examples/`.

3. Produce structured outputs with clear section labels. Prefer YAML, Markdown tables, or compact prompt blocks over long prose.

4. Keep generated prompts self-contained enough for an image model, but avoid repeating the full project bible. Include only the character/style/continuity details that affect the current shot.

5. When the user is creating a reusable project, update project files instead of keeping all decisions only in chat.

## Recommended Project Layout

When setting up a storyboard project, create or update this structure:

```text
storyboard-project/
  bible/
    character_bible.md
    visual_style_bible.md
    continuity_rules.md
  scenes/
    scene_01.yaml
  shots/
    scene_01_shots.yaml
  prompts/
    scene_01_shot_001.md
  reviews/
    continuity_review.md
```

Use concise identifiers such as `char_a_v3`, `style_neon_noir_01`, `loc_rooftop_02`, and `scene_01_shot_003`.

## Prompt Output Contract

For each image prompt, output:

```text
[SHOT ID]
[PURPOSE]
[CHARACTER]
[CAMERA]
[LIGHTING]
[EMOTION]
[COMPOSITION]
[ENVIRONMENT]
[CONTINUITY]
[NEGATIVE CONSTRAINTS]
[IMAGE PROMPT]
[FIX NOTES] optional
```

Keep `[IMAGE PROMPT]` ready to paste into the image tool. Keep the other sections as production notes.

## Continuity Checklist

Before finalizing a prompt or fix, check:

- Character identity, wardrobe, age, hair, props, and facial features.
- Scene location, time of day, weather, lighting logic, and set dressing.
- Camera lens, angle, framing, and emotional distance.
- Shot-to-shot action continuity.
- Style consistency: medium, rendering, color palette, texture, grain, aspect ratio.
- Forbidden changes listed in continuity rules.

## Fix Prompt Pattern

For image-to-image or regeneration fixes, preserve what works first, then specify only the change:

```text
Preserve: [identity, pose, composition, lighting, style, approved elements]
Change: [specific defect or requested adjustment]
Do not change: [continuity-critical items]
Output: [target frame description]
```

Avoid broad rewrites when the user asks for a localized fix.

## Resource Files

- Read `references/project-structure.md` when creating or repairing the project file layout.
- Read `references/prompt-patterns.md` when generating prompts, fix prompts, or review rubrics.
- Read `references/prompt-safety-checklist.md` when reviewing storyboard frames or image prompts for NSFW, restricted content, real-person likeness, minors, violence, copyrighted characters, or platform compliance risks.

## Example Files

- Read `examples/short-drama-scene.md` when the user needs a scene split into multiple storyboard prompts.
- Read `examples/image-prompt-review.md` when the user asks for continuity, prompt-quality, or safety review.
- Read `examples/fix-prompt.md` when the user asks to preserve an approved image while changing one specific detail.
