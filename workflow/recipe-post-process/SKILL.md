---
name: recipe-post-process
description: "Drive the post chain — read the live pass order, settle WHICH volume wins before touching a knob, respect the ordering (exposure before bloom, tonemap before grade, TAA before both), and author a post-process material."
---

# Post process (recipe stub)

This is a **pointer**, not the recipe. The workflow lives in the engine and always matches the
build you are connected to, so load it from the running editor before you act:

    ngine.recipes {name: "authoring/post-process"}

Follow the numbered steps it returns, and read its warnings first. Do not work from this stub
alone.

## Use it when

- tuning bloom, exposure, tone mapping, vignette, sharpen or the colour grade
- an effect toggle or a preset 'did not apply'
- choosing an anti-aliasing rung, or motion blur / depth of field will not turn on
- authoring a post-process material (scanlines, ink, heat haze, posterize)
- a post-process volume changed things you never asked it to change
- deciding the order to tune the post chain in

## Ops it names

`render.graph`, `render.post_resolved`, `render.post_overrides`, `render.exposure`, `render.set_aa`, `render.set_grade`, `render.set_lens`, `render.set_ssr_mode`, `render.set_effect`, `render.ab_capture`, `render.histogram`, `render.region_stats`, `render.periodicity`, `render.edge_crawl`, `render.sharpness`, `render.explain_pixel`, `render.capture_pass`, `render.targets`, `post.stack`, `scene.spawn_post_process_volume`, `scene.set_component_field`, `material.set_graph_domain`, `material.author`

Check each op's arguments with `ngine.describe` before the first call: the recipe is the
order and the discipline, the live schema is the spelling.

Start the session with `editor.context`. If `ngine.recipes` cannot be reached the editor is not
running or not connected: run `/apeiron:status`.
