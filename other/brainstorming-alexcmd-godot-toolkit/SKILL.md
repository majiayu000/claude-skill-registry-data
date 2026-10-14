---
name: brainstorming
description: Design Godot features before touching code — use before implementing any new scene, system, or GDScript class.
---

# Godot Brainstorming

Use before implementing any new feature. Produce a written spec before writing code.

## Hard Gate

Do NOT write any GDScript, C++, or modify any `.tscn` until the spec is written and approved.

## Checklist

You MUST create a task for each of these items and complete them in order:

1. **Explore project context** — check existing scenes, scripts, docs, recent commits
2. **Ask clarifying questions** — one at a time: purpose, constraints, AgentBridge validation strategy
3. **Propose 2–3 approaches** — with trade-offs and your recommendation
4. **Present design** — get user approval
5. **Write spec** — save to `docs/specs/YYYY-MM-DD-<feature>.md` and commit
6. **Spec self-review** — check for placeholders, contradictions, ambiguity (fix inline)
7. **User reviews written spec** — ask user to review before proceeding
8. **Transition to implementation** — invoke `godot:writing-plans`

## Godot-Specific Design Questions (one at a time)

Ask these based on what the feature touches — skip ones that don't apply:

**Scope & placement**
- What does this feature do for the player or editor?
- Which existing scenes does it touch?
- Should this be a new scene, a node added to an existing scene, or an autoload?
- Does it need persistent state across scenes? (→ autoload or resource)

**Implementation layer**
- GDScript or GDExtension (C++)? Use GDExtension when: compute-intensive loops, GPU access via RenderingDevice, tight C++ library integration. Otherwise GDScript.
- Does it need a CompositorEffect or RenderingServer hook? (→ `godot:graphics` / `godot:shader`)
- Does it involve physics queries or collision layers? (→ `godot:physics`)
- Does it play, mix, or spatialize audio? (→ `godot:audio`)
- Does it drive animations or blend trees? (→ `godot:animation`)
- Does it add UI elements or a HUD? (→ `godot:ui`)
- Does it spawn particles or screen-space VFX? (→ `godot:vfx`)
- Does it use NPC navigation or AI decision-making? (→ `godot:ai`)
- Does it involve multiplayer replication or RPCs? (→ `godot:networking`)

**Signals & architecture**
- Which nodes need to communicate? Design signal flow before writing code. (→ `godot:signals`)
- Can this live in one script, or does it need a resource + controller split? (→ `godot:architect`)

**Validation**
- How will it be tested via AgentBridge (`--execute` / `--log` / `--play`)?

## Skill Routing During Design

When the feature clearly belongs to a domain, consult the relevant skill **during brainstorming** to inform the design — not just at implementation time:

| Feature involves… | Consult during brainstorming |
|---|---|
| Shaders, CompositorEffect, RenderingDevice | `godot:shader`, `godot:graphics` |
| Collision, joints, raycasts, physics bodies | `godot:physics` |
| AnimationPlayer, AnimationTree, IK | `godot:animation` |
| Signals, event buses, node communication | `godot:signals` |
| Autoloads, resource architecture, plugin layout | `godot:architect` |
| UI, Control nodes, themes | `godot:ui` |
| Particles, trails, screen VFX | `godot:vfx` |
| Audio buses, spatial audio, one-shots | `godot:audio` |
| NPC AI, navigation, behavior trees | `godot:ai` |
| Multiplayer, RPC, scene replication | `godot:networking` |
| Terrain, GridMap, occlusion, navigation mesh | `godot:environment` |
| Player controller, input, save/load | `godot:gameplay` |
| GDExtension, C++ class, plugin structure | `godot:architect` |

## Approaches

Always propose 2–3 options with:
- How it fits the existing scene hierarchy
- What new nodes or scripts are required
- GDScript vs GDExtension trade-off (if relevant)
- AgentBridge validation strategy (which `godot-exec.sh` commands confirm it works)

## Spec Format

Save to `docs/specs/YYYY-MM-DD-<feature>.md`:

```markdown
# <Feature> Design

**Goal:** <one sentence>
**Scenes:** <list of .tscn files involved>
**New scripts:** <list of .gd/.cpp files to create>
**Signals:** <signals to add or connect>
**Skills needed:** <godot:* skills the plan will use>
**AgentBridge validation:** <which godot-exec.sh commands verify it works>
```

## Spec Self-Review

After writing the spec, check with fresh eyes:

1. **Placeholder scan:** Any "TBD", "TODO", or vague requirements? Fix them.
2. **Consistency:** Do sections contradict each other?
3. **Ambiguity:** Could any requirement be read two ways? Pick one and make it explicit.
4. **Skill coverage:** Does every implementation concern map to a `godot:*` skill in the plan?

Fix inline — no need to re-review.

## User Review Gate

After self-review, ask the user with a clear call to action:

> "Spec written and committed to `<path>`. Please review it and let me know if you want any changes.
>
> **Reply 'looks good' to start writing the implementation plan, or tell me what to change.**"

**Wait for the user's response.** If they request changes, update the spec and re-run self-review. Only proceed once the user approves.

## After Approval

Invoke `godot:writing-plans` to produce the implementation plan.
