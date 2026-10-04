---
name: story-film-suite
description: Self-contained Story-Film Skills bundle for story, book, screenplay, image, audio, video, film, postproduction, and release work. Use this entry point when Story-Film Skills was installed with npx skills.
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Story-Film Skills Suite

This is the self-contained installation entry point.

If the harness also exposes the normal `story-film` skill, use `story-film` and stop here. That means Story-Film is being consumed as a normal Git/package installation rather than through this self-contained npx bundle. Do not inspect or scan `bundle/` in that case.

1. Read `bundle/skills/story-film/SKILL.md` as the main router.
2. When that router names another Story-Film skill, read it from `bundle/skills/<skill-name>/SKILL.md`.
3. Run shared tools from `bundle/scripts/`.
4. Read shared contracts from `bundle/references/`.
5. Use `bundle/docs/README.md` for the user manual.
6. Bundled ComfyUI workflows are under `bundle/comfyui_workflows/<task>/<model>/`.
7. Do not assume that any files exist outside this skill directory.
8. The paths above are authoritative. Do not use Bash, `find`, `ls`, or directory scans to rediscover this bundle's router, playbooks, scripts, references, or workflows.
9. Before any live ComfyUI installation, server, model, node, or workflow discovery, read `bundle/skills/comfyui/SKILL.md` and `bundle/skills/comfyui-discover/SKILL.md`. In Pi, use `story_comfy`; never scan guessed ComfyUI or model paths. Story-Film does not search ComfyUI core/custom template catalogs.

For Pi's optional interactive Todo extension, install `bundle/extensions/story-film-progress/index.ts` into the Pi extensions directory, or use the Git clone installer instead.
