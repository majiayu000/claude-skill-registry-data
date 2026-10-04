---
name: compose-from-simple-parts
description: Review code for monolithic functions that inline multiple operations, and refactor them into composed simple parts. Use when a function does too many things at once, when operations are tangled together, or when you want to make complex behavior readable and testable by decomposing it.
argument-hint: [file-or-function to analyze]
---

# Compose Complex Behavior from Simple Parts

From the Unix tradition: build complex behavior by composing small, focused pieces that each do one thing well.

## The Core Idea

A function that inlines multiple distinct operations is hard to read, hard to test, and hard to reuse. When you decompose it into named parts that compose, each part becomes independently understandable, testable, and reusable — and the top-level function reads like a description of what it does rather than how it does it.

This is not about reducing line count or creating abstractions for their own sake. It's about **giving names to the operations you're performing**, so the reader doesn't have to reverse-engineer intent from implementation.

## The Diagnostic

Read the function and list, in plain English, the distinct operations it performs. If the list has more than one entry and the operations are interleaved or sequenced without names, the function is doing too much inline.

**Ask:** "If I described what this function does to a colleague, would I use words that don't appear anywhere in the code?"

If yes, those missing words are the names of functions that should exist.

## Case Study: Generating SE3 Poses on a Grid

### The Problem

Generate a batch of SE3 (4×4 homogeneous transformation) matrices representing poses on a 3D grid, each with the same orientation.

### Monolithic Version

```python
def robot2base(xrange, yrange, zrange, Nx, Ny, Nz, anglez, angley, anglex):
    box_frame_poses = np.stack(
        np.meshgrid(
            np.linspace(*xrange, num=Nx),
            np.linspace(*yrange, num=Ny),
            np.linspace(*zrange, num=Nz),
            indexing='xy'
        ), axis=-1
    ).reshape(-1, 3)
    se3 = np.stack(
        [np.eye(4) for _ in range(len(box_frame_poses))]
    )
    se3[:, :3, -1] = box_frame_poses
    rotation = R.from_euler('ZYX', (anglez, angley, anglex)).as_matrix()
    se3[:, :3, :3] = rotation
    return se3
```

Read this and list the operations:
1. **Generate grid offsets** — create a meshgrid of positions and flatten it
2. **Build identity SE3 matrices** — allocate a batch of 4×4 identity matrices
3. **Set translations** — place the grid offsets into the translation column
4. **Compute rotation** — convert Euler angles to a rotation matrix
5. **Set rotations** — place the rotation into every SE3 matrix

Five operations, none named. The reader must mentally parse numpy broadcasting and indexing to understand what each block does. The operations are also fused: you can't generate offsets without also building SE3 matrices, and you can't apply a rotation to an arbitrary SE3 matrix — the rotation logic is wired to this specific construction sequence.

### Composed Version

```python
def add_rotation(se3_matrix, z, y, x):
    rotation = R.from_euler('ZYX', (z, y, x)).as_matrix()
    mat = se3_matrix.copy()
    mat[:3, :3] = rotation
    return mat

def offset_to_4x4(offset):
    se3 = np.eye(4)
    se3[:3, -1] = offset
    return se3

def generate_offsets(xrange, yrange, zrange, Nx, Ny, Nz):
    xx, yy, zz = np.meshgrid(
        np.linspace(*xrange, num=Nx),
        np.linspace(*yrange, num=Ny),
        np.linspace(*zrange, num=Nz),
        indexing='xy'
    )
    return np.stack((xx, yy, zz), axis=-1).reshape(-1, 3)

def robot2base(xrange, yrange, zrange, Nx, Ny, Nz, anglez, angley, anglex):
    offsets = generate_offsets(xrange, yrange, zrange, Nx, Ny, Nz)
    return np.array([
        add_rotation(offset_to_4x4(offset), anglez, angley, anglex)
        for offset in offsets
    ])
```

Now:
- `generate_offsets` does one thing: produce a flat array of 3D positions from axis ranges. You can test it, reuse it, and read it without any SE3 context.
- `add_rotation` does one thing: set the rotation of an SE3 matrix. It takes any SE3 matrix — not just ones from this particular grid construction. It copies instead of mutating, so the caller controls side effects.
- `offset_to_4x4` does one thing: convert a 3D offset to a 4×4 identity matrix with that translation. Small, testable, reusable.
- `robot2base` reads like its description: generate offsets, convert each to SE3, apply rotation. The "what" is visible; the "how" lives in the parts.

### What Changed and Why

| Monolithic | Composed | Why it matters |
|---|---|---|
| Grid generation and SE3 construction are interleaved | `generate_offsets` is independent of SE3 | Reusable for any grid task, testable in isolation |
| Rotation applied by broadcasting into a pre-allocated batch | `add_rotation` operates on a single matrix | Works on any SE3 matrix, not just batch-constructed ones |
| Identity matrix allocation is manual (`np.stack([np.eye(4)...])`) | `offset_to_4x4` names the operation | Reader sees intent ("offset to 4×4") not mechanism (`np.eye` + slice assignment) |
| Top-level function is a sequence of numpy operations | Top-level function is a composition of named operations | Reads like a description of the algorithm |

## Red Flags — When to Decompose

### 1. You're explaining the code in chunks

If you find yourself mentally grouping lines and thinking "this part does X, this part does Y" — those groups are unnamed functions.

### 2. Local variables serve as section headers

When a variable like `box_frame_poses` exists mainly to label the output of a chunk before the next chunk consumes it, that chunk is a function waiting to be extracted.

### 3. You can't test an operation without running the whole function

If "generate grid offsets" is only possible by calling `robot2base` and inspecting intermediate state, the operation isn't separable. Extraction makes it testable.

### 4. Operations work on different levels of abstraction

In the monolithic version, `np.meshgrid` (coordinate generation) and `se3[:, :3, :3] = rotation` (matrix surgery) operate at different conceptual levels but sit side by side. Functions should operate at one level of abstraction.

### 5. You're duplicating a sequence of operations

If the same meshgrid-and-reshape pattern appears in another function, the monolithic version forces you to duplicate it. Named parts compose and reuse.

## When NOT to Decompose

Not every multi-step function needs extraction. Keep it inline when:

- **The operations are genuinely inseparable** — they share intermediate state that has no independent meaning.
- **The function is already short** (under ~10 lines) and reads clearly.
- **The extracted function would be called exactly once** and its name would just restate what the single line of code says. `x = compute_sum(a, b)` is worse than `x = a + b`.
- **The parts have no independent use or testability** — if you can't imagine a caller wanting just the offset generation without the SE3 construction, extraction adds indirection without value.

Apply the vocabulary levels test: does the extracted function earn its existence by bridging an abstraction gap, encoding an invariant, or enabling reuse? If it just moves code sideways, leave it inline.

## The Fix Process

1. **Read the function and narrate it** — describe each block of operations in plain English.
2. **Name each operation** — your narration gives you the function names.
3. **Identify inputs and outputs for each** — what does this operation need, and what does it produce?
4. **Extract bottom-up** — start with the leaves (operations that depend on nothing else in the function) and work upward.
5. **Verify each part is independently meaningful** — can you describe it without referencing the parent function?
6. **Compose at the top level** — the original function becomes a sequence of named calls that reads like its own documentation.

Present the decomposed code, showing what each part does and how they compose.