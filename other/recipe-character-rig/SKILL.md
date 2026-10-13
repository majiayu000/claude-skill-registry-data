---
name: recipe-character-rig
description: "Import, rig, skin, pose and animate a character — and attach a weapon or prop to its hand — using the rig/anim ops plus numeric readback, instead of rediscovering the pipeline by trial and error."
---

# Character rig (recipe stub)

This is a **pointer**, not the recipe. The workflow lives in the engine and always matches the
build you are connected to, so load it from the running editor before you act:

    ngine.recipes {name: "authoring/character-rig"}

Follow the numbered steps it returns, and read its warnings first. Do not work from this stub
alone.

## Use it when

- importing a character, FPS arms, or any rigged mesh
- putting a weapon, tool or prop in a character's hand
- posing a skeleton, curling fingers, or building a grip
- authoring an animation clip, an idle, or a recoil
- asked why a limb snapped back to its bind pose
- an attached prop is the wrong size, angle, or in the wrong place

## Ops it names

`asset.import`, `scene.rig_query`, `scene.bind_skin`, `scene.attach_to_bone`, `scene.set_joint_rotation`, `scene.set_joint_rotations`, `scene.create_ik_chain`, `scene.set_ik_target`, `scene.bake_ik_chain`, `scene.remove_ik_chain`, `scene.save_pose`, `scene.apply_pose`, `scene.create_clip`, `scene.set_clip_channel`, `scene.screenshot_clip`, `scene.screenshot_views`, `scene.set_view`, `scene.bounds`, `scene.sample_motion`, `scene.inspect`, `scene.query`, `mesh.describe_shape`, `ui.overlays`, `ui.open_panel`, `scene.select_joint`, `rig.weights`, `rig.check_fit`, `rig.check_deform`, `rig.check_intersect`, `rig.check_limits`, `rig.balance`, `rig.stack`, `rig.bind`, `rig.smooth_weights`, `rig.mirror_weights`, `rig.clean_weights`, `rig.paint_weights`, `rig.set_skinning`, `rig.set_joint_limit`, `rig.set_twist_constraint`, `rig.auto_twist`, `rig.plate`, `rig.select_verts`, `rig.region_weights`, `rig.capture_corrective`, `rig.sculpt_corrective`, `rig.auto_corrective`, `rig.toggle_corrective`, `rig.bend_sheet`, `rig.frame_joint`, `rig.check_symmetry`, `rig.set_mirror`, `rig.add_joint`, `rig.rename_joint`, `rig.reparent_joint`, `rig.remove_joint`, `rig.transfer_weights`, `rig.set_aim_constraint`, `rig.set_parent_constraint`, `rig.set_spring_bone`, `rig.deform_report`, `anim.state`, `anim.retarget`, `rig.roles`, `rig.set_role`, `rig.profiles`, `rig.set_profile`, `anim.rebake_clips`, `anim.measure_foot_slide`, `anim.describe_curve`, `anim.synthesize_clip`, `anim.set_foot_ik`, `anim.graph_create`, `anim.add_state`, `anim.add_transition`, `anim.to_text`, `anim.validate`, `scene.set_anim_clip`, `scene.set_anim_layer`, `scene.insert_key`, `scene.move_keys`, `scene.delete_keys`, `game.play`, `game.stop`, `rig.auto_rig`

Check each op's arguments with `ngine.describe` before the first call: the recipe is the
order and the discipline, the live schema is the spelling.

Start the session with `editor.context`. If `ngine.recipes` cannot be reached the editor is not
running or not connected: run `/apeiron:status`.
