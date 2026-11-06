---
name: game-build-verification
description: Verify and debug a generated game before shipping — pre-build checklists, build/test/visual order, error diagnosis workflow, and forbidden operations.
---

# Game Build Verification

## When to use

- Before considering a generated or modified game done.
- When a game fails to build, crashes at runtime, or misbehaves visually.

## When NOT to use

- A single obvious typo you can fix directly.
- Environment/setup failures (missing runtime, wrong package manager).

## Pre-build checklist (cheap static checks — run before compiling)

- **Animation chain**: every frame key in the animation definitions exists in the asset manifest; every animation key used by characters exists in the animation definitions; every referenced image exists on disk. Games with static portraits declare an empty animation list.
- **Config chain**: every config field accessed in code exists in the configuration; required sections for the game type are present.
- **Scene chain**: every transition target is registered; the level order's first entry is the real first scene; the title screen's game title was updated from the placeholder.
- **Type discipline**: interface/type imports use the type-only form; overridden methods exist in the base class; override visibility is never narrowed; no invented type names.
- **Tilemap names**: layer names in code match the map data exactly (case-sensitive).
- **Restart hygiene**: scenes reused via transitions reset mutable state; event listeners don't leak across restarts; per-round UI is destroyed before recreation.
- **No leftovers**: no template placeholder names or TODO markers remain.

## Execution order

Build → test → visual. Fix everything at each stage before moving on. Build catches type errors fastest (no runtime needed); tests catch logic errors; the dev server is for visual/console issues only.

- The dev server NEVER runs in the foreground — it blocks control forever. Run it in the background, wait a few seconds, read the URL from output, and verify with browser tools.

## Diagnosis workflow

1. Read the COMPLETE error message — not just the first line.
2. Note the file and line number and go there first.
3. Classify the error: type/compile, runtime, asset, or registration.
4. Apply the targeted fix; re-run the same stage to verify before moving on.

### Error pattern → cause → fix

| Pattern | Cause | Fix |
|---|---|---|
| Cannot find module | Wrong relative import depth | Count directory levels; verify the file exists |
| Property does not exist on type | Missing member or typo | Check the class definition; add or correct |
| Cannot read property of undefined | Object used before creation | Create before use — check creation order |
| Texture not found | Asset key mismatch | Compare with the manifest keys exactly |
| Animation not found | Missing animation definition | Add the entry; verify frame keys exist |
| Scene not found | Scene not registered | Register it; match keys exactly |
| Maximum call stack exceeded | Infinite recursion | Find the cycle; add a base case |
| Hit-area callback error | Interactivity set on a container | Set interactive on the inner shape and listen there |
| Runtime crash reading "duration" | Animation references a missing image | Verify every frame key exists in the manifest and on disk |
| Safe-access crash on config | Field absent for this game type | Read config defensively with defaults |

## Isolation technique

When one feature fails, write a focused debug test that boots just that scene, advances a few frames, logs before/after state, and asserts the expected change. Strategic logging beats guessing.

## Forbidden operations

| Never do | Why | Do instead |
|---|---|---|
| Reinstall dependencies | Dependencies are pre-installed; errors are code errors | Read the error, fix the code |
| Run security audit fixes | Unrelated to game logic | Focus on the actual error |
| Update package versions | Version drift breaks things | Use existing versions |
| Delete the dependencies folder | Nuclear, minutes to recover | Never needed for code bugs |
| Random code changes | Guessing wastes time | Read the error carefully |
| Blanket try/catch | Hides bugs | Fix the root cause |
| Comment out broken code | Ships incomplete features | Fix or remove properly |

## Anti-patterns in reasoning

- Skipping the error message — it carries the diagnosis.
- Copying code from the internet without understanding the template's patterns.
- Checking unlikely causes first — import errors are the most common; start there.
- Debugging without reading the template code that defines expected behavior.
