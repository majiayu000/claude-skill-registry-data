---
name: sentinel-router
description: Use when a user asks to test, review, improve, package, or learn from a browser game using Sentinel-style workflows. Routes requests to browser-game playtesting, UI/UX review, game design review, safe learning governance, public skill packaging, or approval-gated runtime patch planning without loading every workflow at once.
---

# Sentinel Router

Choose the smallest safe Sentinel workflow for the request.

## Classify

- `playtest`: browser game smoke test, screenshot, console, mobile, performance, or route evidence.
- `ui_review`: overlap, readability, first-player clarity, confusing screen, hidden action, mobile layout.
- `game_design`: core loop, roguelike systems, reward loop, enemies, progression, character variety, build choice.
- `learning`: repeated mistake, lesson, rubric update, stale reference, improvement loop.
- `public_package`: preparing skills for public sharing.
- `runtime_patch`: changing game files or behavior.

## Route

| Signal | Use |
| --- | --- |
| screenshot, console, mobile, smoke test | `browser-game-playtest-sentinel` |
| text overlap, UX, first action, confusing UI | `game-ui-review` |
| enemy, reward, roguelike, progression, content idea | `game-design-review` |
| learn, repeated issue, rubric, stale lesson | `safe-learning-governance` |
| skill pack, distribute, public release | `public-skill-packaging` |
| implement/fix game code | require exact scope, approval, verification, rollback |

## Output

Return:

- chosen workflow;
- why;
- evidence needed;
- safe next action;
- blocked actions;
- verification target.

## Stop Rules

Stop before deployment, publishing, credentials, paid services, save migration, broad memory rewrite, external-code adoption, or runtime patching without explicit user approval.
