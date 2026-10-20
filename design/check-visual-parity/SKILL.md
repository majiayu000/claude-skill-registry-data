---
name: check-visual-parity
description: >-
  Load this skill when a UI change must not change how it looks, or only where intended (a
  migration, CSS refactor, or library upgrade): Playwright baselines, then explain every diff.
  Trigger on "make sure it looks the same", "pixel parity", "visual regression check".
disable-model-invocation: false
user-invocable: true
compatibility: >-
  Requires Playwright with its browsers installed (`bunx playwright install`), the git CLI for a
  worktree of the old version, and both versions able to run locally. Screenshots differ across
  operating systems and font sets, so both runs must happen on the same machine or image.
license: Apache-2.0
---

# Check visual parity

Prove that two versions of a UI render the same, by screenshot diff, everywhere outside the areas
meant to change. The task is done when every captured screen either matches the old version or
has a diff with a written reason, and no diff is left unexplained.

## Procedure

1. **List what to capture.** Each route the change touches, at two viewports (360 and 1280 wide),
   in each theme the app has, in the states that render differently: empty, loaded, error, and the
   focus and hover states of the components the change touched. Write the list down: it is the
   coverage the result claims, and a screen not on it is not proven.
2. **Make rendering deterministic.** Serve fixed data (MSW handlers or a seeded database), freeze
   the clock with `page.clock.setFixedTime(...)`, wait for `document.fonts.ready`, and mask what
   still varies (avatars, relative times, ads) with the `mask` option. Keep Playwright's default
   `animations: "disabled"`. A screen that differs between two runs of the same version cannot
   prove anything about two versions.
3. **Write one spec over the list**, one `expect(page).toHaveScreenshot("<route>-<viewport>-<state>.png")`
   per entry, under the project's existing Playwright setup.
   `ceh-web-frontend:write-vitest-playwright-tests` holds the runner conventions.
4. **Capture the baseline from the old version.** Check it out in a worktree
   (`git worktree add ../parity-base <old-commit>`), copy the spec in, start that version, and run
   `bunx playwright test <spec> --update-snapshots`. Run it twice: if the second run is not
   identical, go back to step 2.
5. **Compare the new version.** Copy the baseline snapshots into the working tree, start the new
   version, and run `bunx playwright test <spec>`. Playwright writes the expected, actual, and
   diff image of each failure under `test-results/`.
6. **Explain every diff.** Open each diff image. An intended change gets one line in the report
   naming the change that caused it, then its snapshot alone is updated with
   `--update-snapshots --grep "<test name>"`. An unintended one is a bug, fixed in the new version
   and compared again.
7. **Remove the worktree** with `git worktree remove ../parity-base`.

## Rules

- **Tolerance is set per screenshot, with a reason.** Start at Playwright's default of zero
  differing pixels. Raise `maxDiffPixels` on one screenshot only, for a cause you can name, such as
  sub-pixel font anti-aliasing. A global threshold hides real regressions in every other screen.
- **Both versions run on the same machine or image, back to back.** A baseline from a laptop
  against a run in CI compares two font renderers, not two versions.
- **Commit the baseline snapshots with the spec**, so the reviewer sees exactly what the new
  version was held to.

## Output

```markdown
**Compared:** <old commit> → <new commit>, on <machine or image>

| Screen                             | Result                                    |
| ---------------------------------- | ----------------------------------------- |
| <route> <viewport> <theme> <state> | match / intended: <reason> / fixed: <bug> |

**Not captured:** <screens left off the list, and why>
```

## Stop conditions

- The old version will not start → report it. A baseline taken from anything else (a design
  file, a screenshot from memory) proves nothing about the code.
- Two runs of the same version still differ after step 2 → report which regions vary and stop,
  since every comparison after that is noise.
