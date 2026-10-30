---
name: twin-flames
description: Zuko's twin flames for pixel-exact UI parity. Two flames from the same forms must burn the same color. Use for visual-parity, matching two UI implementations, migrating a styling system or component library, or "make it look exactly the same". The baseline is the spec, and equivalence is proven by image diff, not by eye.
---

# Zuko's twin flames

Zuko and Azula learned the same forms from the same masters. One flame still burned orange and the other blue, and anyone who looked closely could tell them apart. Two UI implementations that should match are the same. Close enough by eye hides a different color. Only an image diff tells you the flames are twins.

You own pixel-exact equivalence. The baseline is the spec, and you do not touch it.

On Codex, read [avatar-mode/references/codex.md](../avatar-mode/references/codex.md) for tool equivalents.

## Steps

1. **Establish the baseline first, before any migration.** Build a visual regression harness that screenshots the current component across its states (sizes, themes, hover, focus, disabled, empty, loading, error), plus the target when you are matching two implementations. No baseline, no parity claim. This is a blocking prerequisite, not a follow-up.
2. **State the anti-shortcut rules and hold them.** No harness changes, no baseline edits, and no component restructuring to make a diff pass. If the baseline looks wrong, stop and ask the human. Do not edit it.
3. **Migrate shared primitives first** as a blocking phase (tokens, typography, spacing, the base button and input). Every component builds on them.
4. **Then migrate one component at a time.** When the top-level session runs this skill, dispatch components in parallel, one owner per component, each in its own git worktree, so no two writers share a file. Dispatch each as `team-avatar:appa` on Appa's model from the avatar-setup sheet, with an effort level that fits the job. When you are already a dispatched character, migrate them yourself, one after another.
5. **Verify each component against its baseline by image diff** on the matching surface, through the project's verification skill (generate one with `vital-signs`) or Claude Code's `run` skill. A nonzero diff is a fail. Investigate the pixel delta, fix the component, and repeat until the diff is zero. On Claude Code, `/loop` can drive that repeat per component.
6. **Hand to `yip-yip`** per component or per safe batch.

## Reply

The components migrated, the diff result for each, the baseline harness location, and what is left.
