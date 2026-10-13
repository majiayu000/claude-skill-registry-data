---
name: recipe-cinematic-sequence
description: "Shoot a VIDEO of the scene — build a sequence, bind a clip to a character, frame the shot and render a frame-locked mp4 (with audio) or EXR/PNG sequence — instead of screenshotting frames by hand."
---

# Cinematic sequence (recipe stub)

This is a **pointer**, not the recipe. The workflow lives in the engine and always matches the
build you are connected to, so load it from the running editor before you act:

    ngine.recipes {name: "authoring/cinematic-sequence"}

Follow the numbered steps it returns, and read its warnings first. Do not work from this stub
alone.

## Use it when

- asked for a video, a movie, a clip, an mp4, or 'render the animation'
- shooting a cinematic, a cutscene, a trailer beat or a turntable
- a still frame is not enough because the thing being judged MOVES
- an animation looks right in single frames and you need to see it play
- choosing between scene.screenshot_clip, sequence.render and live playback

## Ops it names

`sequence.create`, `sequence.add_track`, `sequence.add_key`, `sequence.scrub`, `sequence.state`, `sequence.render`, `sequence.render_status`, `sequence.preview`, `sequence.frame`, `sequence.play`, `sequence.to_text`, `sequence.save`, `sequence.set_track`, `sequence.motion_trail`, `sequence.record`, `scene.create_clip`, `scene.set_clip_channel`, `scene.screenshot_clip`, `scene.screenshot`, `camera.set`, `lookdev.begin`, `lookdev.end`, `ui.overlays`, `env.set_time`, `image.sheet`

Check each op's arguments with `ngine.describe` before the first call: the recipe is the
order and the discipline, the live schema is the spelling.

Start the session with `editor.context`. If `ngine.recipes` cannot be reached the editor is not
running or not connected: run `/apeiron-web:status`.
