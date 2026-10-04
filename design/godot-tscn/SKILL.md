---
name: godot-tscn
description: Use when a Godot task requires reading, editing, generating, diff-reviewing, or validating `.tscn` scene files directly and the agent must preserve scene-file structure, resource ordering, node paths, connections, and editor-compatible conventions instead of treating the file as generic text.
---

# Godot TSCN

Use this skill when a Godot 4.x task involves **direct work on a `.tscn` text scene file** rather than only scene architecture or C# code.

This skill is for scene-file-aware implementation and review. Its job is not to give a generic scene-design lecture, and it is not primarily a runtime-debugging skill. Its job is to help an agent read or modify `.tscn` safely: keep the file descriptor and section order sane, preserve `ExtResource` / `SubResource` integrity, avoid breaking root and parent rules, respect `NodePath` and connection semantics, and define the smallest validation needed after the change.

Prefer this skill when the main risk is that a technically small text edit can quietly turn into a scene-load failure, broken node wiring, or editor rewrite churn.

## Purpose

This skill is used to:

- classify the requested scene-file task before editing
- map the current `.tscn` structure and live reference surfaces
- preserve resource IDs, node paths, parent paths, and connections
- flag serializer and editor behaviors that can make diffs misleading
- produce a structured scene-edit brief another agent can follow confidently

## Use this skill when

Invoke this skill for tasks such as:

- editing a `.tscn` file directly instead of going through the Godot editor
- reviewing or resolving a manual merge conflict inside scene text
- generating or repairing a small scene snippet, node block, or connection block
- checking whether a node move, rename, or resource rewiring is safe in text form
- explaining how a scene file represents nodes, resources, `NodePath`s, or connections
- diagnosing whether a hand-edited scene file is likely to break on load

### Trigger examples

- "Help me edit this `.tscn` safely"
- "What does this scene file block mean?"
- "Can I rename this node directly in scene text?"
- "This merge conflict is inside `[sub_resource]` and `[node]` blocks—what must stay consistent?"
- "Why did this hand-edited scene rewrite so much when saved in Godot?"

## Do not use this skill when

Do not use this skill when:

- the main ask is scene or system architecture review rather than file-level scene editing
- the task is primarily C# or GDScript implementation with no direct `.tscn` editing risk
- the problem is a runtime failure whose first unclear layer is broader than the scene text itself
- the file of interest is mainly a `.tres` resource file rather than a scene file
- the user wants UI/UX review or upgrade planning rather than scene-text guidance

## Pattern

- Primary pattern: **Tool Wrapper**
- Secondary pattern: **Generator**

Why this fit is better than the alternatives:

- the skill packages reusable Godot scene-text rules and parser-aware cautions
- it still needs to produce a repeatable structured artifact instead of loose advice
- a full Pipeline would add ceremony without enough value, because the ordered checks can live directly in this file

## TSCN surfaces that must be considered

Every result must explicitly consider these surfaces, even if some are unaffected:

1. **file descriptor and section order**
2. **external and internal resource integrity**
3. **root node and parent-path correctness**
4. **node properties and `NodePath` references**
5. **connections, editable entries, or inherited-scene metadata**
6. **save-time normalization and default-value omission**

If a surface is not relevant to the current task, say so briefly instead of silently skipping it.

## Inputs

Collect or infer these inputs when available:

- target `.tscn` file path or snippet
- task summary and intended scene change
- whether the file is being hand-edited, merged, generated, or repaired
- nodes, resources, or connections expected to change
- whether the scene uses inheritance, instancing, or imported assets
- any current parser, scene-load, or diff symptoms
- Godot version if known, especially when older 4.x files may still appear

If inputs are incomplete, do not block on perfect detail. Infer the smallest safe assumptions and call out the assumptions that would change the file shape.

## Workflow

Follow this sequence every time.

### 1. Classify the edit shape

State what kind of `.tscn` task this is.

Common categories:

- read-only explanation
- local property tweak
- node add / remove / move / rename
- resource wiring or ID-preservation change
- connection repair
- merge-conflict cleanup
- generated scene block or templated snippet

Do not jump into line edits before you know whether the risky part is structure, references, or serializer behavior.

### 2. Read the scene structure before editing

Map the current scene layout first.

At minimum, identify:

- the file descriptor such as `[gd_scene format=3 ...]`
- whether deprecated header fields like `load_steps` are present and should simply be tolerated
- the current order of `[ext_resource]`, `[sub_resource]`, `[node]`, `[connection]`, and any `[editable]` entries
- the scene root, which must be unique and must not declare a `parent`
- inherited or instanced markers such as `instance`, `instance_placeholder`, `owner`, `groups`, `index`, and `unique_id`

Do not start editing until you know which IDs, paths, and blocks are actually live.

### 3. Trace the reference surfaces that must survive the edit

List the references that the edit can break.

Check for:

- `ExtResource("id")` and the matching `[ext_resource ... id="..."]`
- `SubResource("id")` and the matching `[sub_resource ... id="..."]`
- `parent`, `owner`, `instance`, and other path-bearing node-header fields
- `NodePath(...)` values inside node properties or animation data
- `[connection ...]` fields such as `from`, `to`, `signal`, `method`, `binds`, and `flags`

If a node, resource, or property is being renamed, moved, or removed, name every dependent surface before recommending the edit.

### 4. Apply safe edit rules

When shaping the edit, preserve these rules:

- keep the file descriptor first
- keep the major scene sections in valid order
- keep exactly one scene root
- do not add `parent` to the root node
- for a direct child of the root, use `parent="."`
- for deeper nodes, use parent paths that omit the root node's name
- do not assume `unique_id` exists in every scene; older 4.x files may omit it
- do not depend on deprecated `load_steps`; ignore it if present
- ensure a `SubResource("id")` reference points to a sub-resource already declared in the file
- remember that external-resource IDs and internal-resource IDs are different reference surfaces
- separate semantic correctness from formatting preservation, because the editor may normalize comments, whitespace, and default-value storage on save

If the edit would fight likely editor normalization, prefer semantic correctness and call out the expected diff churn.

### 5. Produce the scene-edit brief

Return the result using `assets/scene-edit-brief.md`.

The brief should:

- summarize the target scene and requested change
- state the current structure that matters to the edit
- outline the smallest safe edit sequence
- list the reference surfaces that must remain consistent
- call out likely rewrite or load-risk behaviors
- define the validation path after the edit

### 6. Define validation and reload checks

After the edit guidance, define the smallest meaningful verification path.

At minimum, consider:

- whether the scene should reopen in the editor without parse/load errors
- whether the scene tree and inspector should show the expected nodes and resources
- one runtime smoke path that exercises the changed node, resource, or connection
- one nearby regression guard such as an animation path, signal connection, instanced child path, or inherited override

If the edit touches instancing or inheritance, include at least one instance-resolution or inherited-scene check.

## Output contract

Return the result using `assets/scene-edit-brief.md` in this section order:

- `Task summary`
- `Scene structure read`
- `Safe edit plan`
- `Reference surfaces to preserve`
- `Risks and invariants`
- `Validation steps`
- `Assumptions`

Output rules:

- separate observed scene facts from proposed edits
- mention exact IDs, paths, nodes, or connections when available
- explicitly call out when the editor may rewrite formatting or drop default-valued properties
- keep the edit plan minimal and file-aware instead of drifting into generic architecture advice
- prefer preservation of reference integrity over cosmetic diff cleanliness

## TSCN heuristics

- `.tscn` stores one text-based scene tree and is generally more VCS-friendly than binary scene formats.
- The descriptor is usually `[gd_scene format=3 ...]` in Godot 4.x.
- Scenes saved before Godot 4.6 may still contain deprecated `load_steps` in the header.
- The scene root must be unique and must not have a `parent` field.
- `NodePath` values are relative to the current node, and they can also target properties such as `NodePath("Box:scale")`.
- A direct child of the root uses `parent="."`, not the root node name.
- External resources may use `res://` paths or relative paths; UID and path are related but not interchangeable.
- `unique_id` is useful when present, but it is not guaranteed in older scene files.
- Connections require stable `from`, `to`, `signal`, and `method` semantics.
- Comments, whitespace, and properties equal to defaults may disappear when the editor saves the scene.

## Companion files

- `references/tscn-format-notes.md` — distilled official TSCN structure, resource, node, `NodePath`, parser, and save-time caveats
- `assets/scene-edit-brief.md` — reusable template for file-aware scene edit guidance

## Validation

A good result should satisfy all of the following:

- the scene-edit task is classified correctly
- the scene structure and live reference surfaces are identified before edits are suggested
- root and parent-path rules are respected
- resource ID and `NodePath` integrity are treated as first-class constraints
- likely editor normalization is called out when relevant
- validation covers editor load plus one meaningful runtime or wiring check
- the result stays focused on scene-file guidance rather than broader architecture advice

## Common pitfalls

- treating a `.tscn` file like generic INI or JSON text
- renaming a node without checking `NodePath`s, connections, or animation tracks
- assuming the root node should have `parent="."`
- assuming `unique_id` exists in every Godot 4 scene
- adding sub-resource references before the target sub-resource is declared
- fighting editor formatting normalization instead of preserving semantics
- mistaking scene-text guidance for broader architecture review

## Completion rule

This skill is complete when the agent has:

- classified the `.tscn` task
- mapped the scene structure that matters to the edit
- identified the reference surfaces that must remain valid
- produced a concrete scene-edit brief
- defined the validation and reload checks for the changed behavior
