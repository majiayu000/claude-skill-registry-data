---
name: recipe-pose-by-text
description: "Pose any rig — humanoid or creature — by reading and writing numbers instead of guessing from screenshots — read in bend/side/twist, write the same terms, reach, grip, limit, diff, and only then look."
---

# Pose by text (recipe stub)

This is a **pointer**, not the recipe. The workflow lives in the engine and always matches the
build you are connected to, so load it from the running editor before you act:

    ngine.recipes {name: "authoring/pose-by-text"}

Follow the numbered steps it returns, and read its warnings first. Do not work from this stub
alone.

## Use it when

- posing a character or creature for a still, a key, or a shot
- a hand must hold a prop, touch something, or reach a point
- matching a reference pose, or checking how far a pose is from a saved one
- a pose looks wrong but you cannot tell which joint is off
- fingers, a tail, a spine or any chain has to curl or aim

## Ops it names

`rig.describe_pose`, `rig.pose`, `rig.reach`, `rig.pose_goals`, `scene.space_switch`, `rig.grip`, `rig.grip_report`, `rig.auto_limits`, `rig.check_limits`, `rig.set_joint_limit`, `rig.socket_set`, `control.derive`, `control.set`, `scene.save_pose`, `scene.apply_pose`, `scene.key_pose`, `scene.attach_to_bone`, `scene.screenshot`

Check each op's arguments with `ngine.describe` before the first call: the recipe is the
order and the discipline, the live schema is the spelling.

Start the session with `editor.context`. If `ngine.recipes` cannot be reached the editor is not
running or not connected: run `/apeiron:status`.
