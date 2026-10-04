---
name: rage-compile
description: Attacks the error list in one relentless pass — fix, rebuild, repeat, no commentary — until it builds clean; invoke via /rage-compile when you have a wall of build/type/lint errors and just want them gone.
---

# Rage Compile

Errors are not feelings to discuss. They are a list to delete. This mode locks onto the build output and grinds — fix, rebuild, fix, rebuild — without narrating its emotions, until the thing compiles green.

## When to use
- You have a wall of build, type, or lint errors and want them eliminated.
- You don't need explanation per error — you need a clean build.

## Behavior
1. Run the build/type/lint and capture the full error list before touching anything.
2. Group errors by root cause — one bad type or import often spawns dozens of downstream errors.
3. Fix from the root outward: address the upstream cause first, then rebuild to see what actually remains.
4. Loop tightly: edit, rebuild, re-read errors, repeat — minimal commentary between cycles.
5. Don't paper over errors with `any`, `@ts-ignore`, or suppressions unless genuinely unavoidable, and flag any you use.
6. Keep fixes correct, not just silencing — a passing build that broke behavior is a failure.
7. Stop only when the build is fully clean, then report what was wrong.

## Output
A clean build, plus a terse after-action summary of the root causes fixed and any suppressions used that deserve a second look.
