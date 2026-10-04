---
name: vocabulary-levels
description: Diagnose mixed abstraction levels in functions and determine whether an abstraction earns its existence. Use when reviewing code for readability, deciding whether to extract helpers, or evaluating whether a wrapper function adds value.
argument-hint: [file-or-function to analyze]
---

# Vocabulary Levels and Earned Abstractions

## The Core Idea

A function tells a story. Every line in the body uses a vocabulary — the concepts and operations it names. When the vocabulary is consistent, the function reads as a narrative at one level of abstraction. When the vocabulary is mixed, the reader must mentally jump between levels to understand what the function does.

## Diagnosing Mixed Vocabulary

Read each line of a function and describe what it does in plain language. Write the descriptions as a list. When the descriptions shift granularity, you've found a vocabulary break.

### Case Study: `action_loop_once`

```python
def action_loop_once(robot):
    device = get_model_device(robot.next_direction_model)
    obs = get_obs(robot)
    stereo_sample = obs.stereo_sample().transform(v2.ToImage()).move_to(device)
    dir = next_direction(robot, stereo_sample)

    robot2world = ru.prim_local2world(robot)
    robot_origin = transform_utils.get_translation(robot2world)

    ArrowRegistry.get().set_arrow(
        robot.name,
        ArrowSpec(
            origin=robot_origin,
            direction=transform_utils.rotate(dir, robot2world)
        )
    )
    step = transform_utils.resize_norm(dir, robot.step_size)
    move(step, robot)
    return ObsAction(obs, Action(dir))
```

The function's name says "one iteration of a robot's action loop." At that level, the narrative should be: observe, decide direction, draw debug arrow, move.

Line-by-line vocabulary check:

- `get_model_device(...)` — device placement detail. **Lower level.**
- `get_obs(robot)` — "observe." **Right level.**
- `obs.stereo_sample().transform(v2.ToImage()).move_to(device)` — data pipeline mechanics: torchvision transforms, device transfer. **Lower level.**
- `next_direction(robot, stereo_sample)` — "decide direction." **Right level.**
- `ru.prim_local2world(robot)` — coordinate transform mechanics. **Lower level.**
- `transform_utils.get_translation(robot2world)` — matrix decomposition. **Lower level.**
- `transform_utils.rotate(dir, robot2world)` — vector rotation. **Lower level.**
- `ArrowRegistry.get().set_arrow(...)` — "draw debug arrow." **Right level** (once you ignore the arguments that required lower-level computation).
- `transform_utils.resize_norm(dir, robot.step_size)` — vector normalization and scaling. **Lower level.**
- `move(step, robot)` — "move." **Right level.**

The narrative reads: *device detail, observe, pipeline detail, decide, matrix math, matrix math, vector rotation, draw arrow, vector math, move.* The right-level words are buried in lower-level operations.

## When to Extract

The test: **if you deleted a group of lines and replaced them with a single function call, would the name be easy to write?**

- The `device` + `stereo_sample` lines → `prepare_model_input(robot)` — easy name, coherent concept. Worth extracting.
- The `robot2world` + `robot_origin` + `rotate` lines → `draw_direction_arrow(robot, dir)` — easy name, coherent concept. Worth extracting.
- The `resize_norm` line → harder to name independently. It's one line of movement preparation. Might just be part of `move`'s job, or might stay inline.

If the name would be forced or vague (`do_stuff`, `handle_things`), the lines aren't a coherent lower-level concept. The mixed vocabulary is accidental — clean up naming instead of extracting.

## When an Abstraction Earns Its Existence

Not every cluster of lower-level lines deserves a function. A function earns its existence when it does at least one of:

- **Composes** multiple operations into a single concept the caller thinks about as one thing
- **Encodes an invariant** the caller shouldn't need to know (e.g., "device must match model device")
- **Makes an error structurally impossible** (e.g., encapsulating a cleanup obligation in a context manager)
- **Bridges an abstraction level** — the caller's vocabulary and the implementation's vocabulary are genuinely different

A function does NOT earn its existence when:

- It's a 1:1 pass-through of an existing operation (`make_policy` wrapping `partial`)
- The caller's vocabulary and the implementation's vocabulary are the same
- The name would just restate what the single line of code already says

### The `partial` Test

```python
# Does NOT earn its existence
def make_direction_policy(cls, **kwargs):
    return partial(cls, **kwargs)
```

The caller thinks "partially apply this class with these arguments." The implementation does "partially apply this class with these arguments." Same vocabulary, same concepts, same level. The wrapper is a door between two rooms that are actually the same room.

Contrast with something that does earn it:

```python
# Earns its existence — bridges a vocabulary gap
def prepare_model_input(robot):
    device = get_model_device(robot.next_direction_model)
    obs = get_obs(robot)
    return obs.stereo_sample().transform(v2.ToImage()).move_to(device)
```

The caller thinks "get the model input." The implementation thinks about stereo samples, torchvision transforms, and device placement. Different vocabularies — the function bridges the gap.

## The Vocabulary Change Test

**Can you describe what the caller wants without using the callee's words?**

- `physics_step(world)`: caller wants "advance simulation" — no mention of `world.step` or `render=True`. **Vocabulary changes. Function earns its name.**
- `move(action, robot)`: caller wants "move the robot" — no mention of local2parent transforms or `set_transform`. **Vocabulary changes.**
- `next_direction(robot, sample)`: caller wants "get the next direction" — no mention of model inference or policy buffers. **Vocabulary changes.**
- `make_direction_policy(cls, **kwargs)`: caller wants "partially apply cls with kwargs" — that's exactly what `partial(cls, **kwargs)` says. **No change. Wrapper adds nothing.**

When you can describe the caller's intent using different, higher-level words than the implementation uses, a function boundary belongs there. When the caller's intent and the implementation are described with the same words at the same granularity, there's no abstraction gap to bridge.

## Alternatives to Extraction

Sometimes a well-named intermediate variable is enough to restore the narrative without adding a function:

```python
# Before: reader must parse the RHS to follow the story
robot2world = ru.prim_local2world(robot)
robot_origin = transform_utils.get_translation(robot2world)

# After: variable name tells the story, RHS is ignorable detail
arrow_origin = transform_utils.get_translation(ru.prim_local2world(robot))
```

The question is whether the reader of the outer function needs to see the intermediate as a separate concept. If `robot2world` is only used to derive the arrow, it's not part of the action loop's vocabulary — it's an intermediate of "get the arrow parameters." Collapsing it removes a concept the reader doesn't need at this level.

## The Diagnostic Process

1. **Read each line and write down what it does in plain language**
2. **Circle the descriptions that match the function's stated purpose** — these are at the right level
3. **The remaining descriptions are at a lower level** — group them by coherent concept
4. **For each group, try to name it** — if the name is easy and meaningful, it's a candidate for extraction
5. **Apply the earnings test** — does the extraction compose, encode an invariant, prevent errors, or bridge vocabulary? If none, consider naming variables instead
6. **Verify the result reads as a narrative** — after extraction or renaming, the function body should read as a sequence of concepts at one level
