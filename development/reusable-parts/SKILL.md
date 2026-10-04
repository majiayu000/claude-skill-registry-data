---
name: reusable-parts
description: Review code for functions that fuse logic instead of composing independent parts. Test whether convenience functions are thin orchestration (good) or god functions with trapped logic (bad).
user_invocable: true
argument-hint: "[agents=N] [model=sonnet|opus|haiku]"
trigger: Use when reviewing code for reusability, when a function does too many things, or when you want to verify that a convenience/orchestration function is truly just a calling sequence over independent parts.
---

# Reusable Parts

## Principle

The UNIX philosophy says: make simple functions that do one thing, then compose them into complex behavior. Convenience functions that orchestrate simple parts are fine — they're just shell scripts piping tools together. God functions that *fuse* logic are not — they trap decisions inside and make the parts unusable independently.

**The test:** Can you use the parts without the whole? If yes, the convenience function is just orchestration. If no, it's a god function.

## How to apply

**Step 1: Identify the target code.** Use the code the user points you to, or the recently changed code from git diff.

**Step 2: Parse arguments.** The user may pass optional arguments:
- `agents=N` — number of reviewer agents to spawn (default: 3)
- `model=sonnet|opus|haiku` — Claude model for the agents (default: inherit from parent)

For example: `/reusable-parts agents=5 model=haiku` spawns 5 agents using Haiku.

**Step 3: Spawn N independent reviewer agents in parallel** using the Agent tool (subagent_type: general-purpose, model: as specified). Give each agent:
- The full source of the code to review (paste it directly into the prompt, do not ask the agent to read files)
- The five tests below
- Instructions to return a structured report: one section per function reviewed, verdict (PASS / FAIL / WARN), and specific line citations for any violations

The three agents should work independently — do not share intermediate results between them before they report back.

**Step 4: Aggregate.** Once all N agents have returned, synthesize their findings:
- Violations all/most agree on → confirmed, high confidence
- Violations a majority flags → likely, note the dissent
- Violations only one flags → possible, lower confidence, include but mark as minority view
- Functions all pass → clean, note briefly

Present the aggregated report to the user, grouped by function. For each confirmed or likely violation, cite the specific lines and explain *why* they fail the test. Then propose a refactor: extract the trapped logic into independent primitives and reduce the orchestrator to a thin calling sequence.

---

## The five tests (give these verbatim to each agent)

For each function that calls multiple other functions or contains multiple logical steps, evaluate:

1. **Is it just a calling sequence?** The function should read like a recipe: call A, pass result to B, pass result to C. The orchestrator makes no decisions of its own beyond sequencing.

2. **Does logic live in the leaves?** Branching, retries, configuration interpretation, error recovery — these belong in the primitive functions, not in the orchestrator. If the orchestrator contains `if/elif` chains, `for` loops that build data structures, or `try/except` with recovery logic, the logic has leaked upward.

3. **Can the parts be used independently?** The ultimate proof. Can you call each primitive in a different context — a dry run, a single-shot redo, a test — without the orchestrator? If a primitive depends on state set up by the orchestrator, it's coupled.

4. **Do steps communicate through shared mutable state?** If step B's behavior depends on side effects from step A via a shared `state` dict or mutated object, the steps are fused even if they look like separate functions.

5. **Count the inputs.** Draw a circle around a block of inline code and count the arrows coming in from the surrounding scope. If the block only touches two or three variables out of the ten available in the function, it's telling you it doesn't belong to this scope. It's a self-contained computation sitting inside a larger function. Those few arrows are a function signature waiting to happen. This is especially common with inline math — a matrix inversion and decomposition that only needs two matrices, sitting inside a function that also has a robot handle, a camera, a config, and a list of images. The math doesn't know about any of that. It shouldn't have to.

## Case studies

### BAD: Logic trapped inside the orchestrator

```python
def collect_dataset(robot, cameras, config, dataset):
    # generates positions inline — can't reuse this logic
    positions = []
    for i in range(config.num_samples):
        pos = [random.uniform(*config.bounds[axis]) for axis in 'xyz']
        if config.avoid_collisions:
            while robot.would_collide(pos):
                pos = [random.uniform(*config.bounds[axis]) for axis in 'xyz']
        positions.append(pos)

    for pos in positions:
        # movement logic with retries baked in
        for attempt in range(3):
            try:
                robot.move(pos, velocity=0.3 if attempt == 0 else 0.1)
                break
            except MotionError:
                if attempt == 2:
                    continue

        # capture with inline calibration decisions
        images = []
        for cam in cameras:
            if cam.type == 'zed':
                img = cam.grab(resolution='2k', depth=True)
            elif cam.type == 'realsense':
                img = cam.grab(resolution='1080p', depth=True, laser_power=150)
            else:
                img = cam.grab()
            images.append(img)

        dataset.append({'pos': pos, 'images': images})
```

**Why this fails:**

- **Position generation is inline.** The collision-aware sampling logic is trapped inside the loop. You can't reuse it to visualize planned positions, test a different sampling strategy, or generate positions without a robot present.
- **Retry logic is baked into the orchestrator.** The velocity-backoff retry strategy is a movement policy decision, but it lives in the dataset collection function. You can't reuse this retry logic for a different task, and you can't move the robot without retries if you wanted to.
- **Camera dispatch is inline.** The `if cam.type == 'zed'` branching means adding a new camera type requires editing the dataset collection function. Capture configuration is a camera concern, not a dataset concern.
- **Nothing is independently callable.** You can't generate positions without collecting a dataset. You can't capture images without the full loop. Every piece of logic is fused into one monolith.

### BAD: Steps coupled through shared mutable state

```python
def collect_dataset(robot, cameras, config):
    state = {'retries': 0, 'skipped': [], 'dataset': [], 'last_pos': None}

    for i in range(config.num_samples):
        pos = generate_next_pos(state, config)  # reads state['last_pos']
        state['last_pos'] = pos

        success = try_move(robot, pos, state)    # mutates state['retries']
        if not success:
            state['skipped'].append(i)           # steps communicate through state
            continue

        images = capture(cameras, state)          # behavior depends on state['retries']
        state['dataset'].append({'pos': pos, 'images': images})

    return state
```

**Why this fails:**

- **The functions look independent but aren't.** They're separated into `generate_next_pos`, `try_move`, and `capture`, which gives the illusion of modularity. But they all read and write a shared `state` dict, so they're coupled through a side channel.
- **Behavior depends on hidden context.** `capture(cameras, state)` changes behavior based on `state['retries']` — a value set by `try_move`. This means you can't call `capture` independently without first setting up the state that `try_move` would have produced.
- **`generate_next_pos` depends on prior iteration.** It reads `state['last_pos']`, so you can't generate all positions up front or test the generation in isolation.
- **The state dict is a god object in disguise.** Instead of fusing logic into one function, the logic is fused through shared mutable state. The coupling is just harder to see.

### GOOD: Thin orchestration over independent parts

```python
# Simple primitives — each is self-contained
def generate_positions(bounds, n, collision_check=None) -> list[Pose]: ...
def move_robot(robot, pose) -> bool: ...
def capture_images(cameras) -> list[Image]: ...
def store_sample(dataset, images, pose): ...

# Convenience function — just a calling sequence
def collect_dataset(robot, cameras, config, dataset):
    for pose in generate_positions(config.bounds, config.num_samples):
        if move_robot(robot, pose):
            images = capture_images(cameras)
            store_sample(dataset, images, pose)
```

**Why this succeeds:**

- **The orchestrator contains no logic of its own.** It's a four-line loop that calls primitives in sequence. No branching, no retries, no configuration interpretation. It reads like a recipe.
- **Each primitive is self-contained.** `generate_positions` takes bounds and a count — it doesn't need a robot or a dataset. `capture_images` takes cameras — it doesn't need to know what position the robot is at. No function depends on side effects from another.
- **The retry/collision/calibration logic lives in the leaves.** `move_robot` handles its own retry policy internally. `generate_positions` handles collision avoidance via the optional `collision_check` callback. Each camera knows how to configure itself inside `capture_images`. The orchestrator doesn't need to know about any of this.

### GOOD: Proof — same parts, different compositions

```python
# Visualize planned positions without moving the robot
def dry_run(config):
    poses = generate_positions(config.bounds, config.num_samples)
    plot_poses(poses)

# Re-take images at a single known position
def recapture_at(robot, cameras, dataset, pose_index):
    pose = dataset[pose_index]['pose']
    move_robot(robot, pose)
    images = capture_images(cameras)
    store_sample(dataset, images, pose)
```

**Why this succeeds:**

- **This composition was never planned by the original author.** `dry_run` and `recapture_at` use the same primitives in arrangements the `collect_dataset` function never anticipated. This is only possible because the parts are truly independent.
- **Each new composition is also a thin calling sequence.** No new logic is introduced. The functions are just wired together differently.
- **This is the UNIX payoff.** Independent tools composed via simple scripts. The value isn't in any one function — it's in the fact that you can rearrange them freely.

### Real case study: split a god-export at its seam, share the pose decomposition

A dry-run debug export started as one function that baked debug cameras + grasp-frame axes
into a live USD stage **and** wrote a `.usdz` + `.npz`:

```python
# BAD — decoration fused with persistence; you can't get the decorated scene without writing files
def export_debug_bundle(runtime, scene, grasp_points, world_poses, render_dir):
    # ... bake cameras + axis gizmos into the stage ...
    usdz = export_subtree_usdz(stage, "/World", render_dir / "debug", "scene")
    np.savez(render_dir / "debug" / "dryrun.npz", world_poses=world_poses, ...)
    return usdz
```

Apply **test 3 (can the parts be used independently?)**: no — to obtain a decorated scene
you are forced to write a USDZ and an npz to a specific directory. The natural seam is the
moment the last gizmo is added: before it is *decorate the scene*, after it is *persist it*.

```python
# GOOD — mechanism returns the decorated scene; a thin policy persists it
def decorate_debug_scene(scene, grasp_points, world_poses) -> dict: ...   # no I/O
def export_debug_bundle(info, render_dir): ...                            # export + savez

# orchestrator is a calling sequence:
export_debug_bundle(decorate_debug_scene(scene, grasp_points, world_poses), render_dir)
```

Now `decorate_debug_scene` is reusable in arrangements the export author never planned —
render the scene in-process, open it in a viewer, or bake more onto it before exporting —
exactly the "same parts, different compositions" payoff above.

The same review also caught a hidden version of the problem via **test 5 (count the inputs)**.
`move_prims` was the only place an SE3 became a prim pose; its decomposition
(`p[:3,3]`, `R.from_matrix(p[:3,:3]).as_euler('xyz')`) only touched the pose matrix out of all
the Replicator state in scope — a self-contained computation wearing the function as a costume.
The dry run needed that identical math but *without* a Replicator graph. Extracting it paid off
immediately:

```python
def se3_to_pos_euler(pose):                 # the one decomposition, reused by both callers
    return (pose[:3, 3].tolist(),
            R.from_matrix(pose[:3, :3]).as_euler('xyz', degrees=True).tolist())

def set_prim_pose(prim_path, pose):         # static applier, prim-path addressed (dry run)
    t, e = se3_to_pos_euler(pose)
    set_transform(stage.GetPrimAtPath(prim_path), translation=t, rotation=e)

# move_prims (live capture) now consumes the same primitive instead of a private copy:
positions, rotations = zip(*(se3_to_pos_euler(p) for p in poses))
rep.modify.pose(position=rep.distribution.sequence(list(positions)),
                rotation=rep.distribution.sequence(list(rotations)))
```

One extracted primitive, two compositions (a batched Replicator graph and a static
per-prim setter) — and because both reuse the *same* decomposition, the dry-run cameras
can't drift from where the real capture would place them.
