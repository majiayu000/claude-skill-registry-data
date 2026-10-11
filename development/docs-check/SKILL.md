---
name: docs-check
description: Verify documentation keeps up with a code change in dynamic-neural-field-composer - Doxygen on public API, the matching wiki page, and stale references elsewhere. Use before opening a PR, or when asked whether docs need updating.
---

# Docs check

Three passes over `git diff origin/main...HEAD`. Report findings; do not silently rewrite
prose that is merely different from how you would put it.

## Pass 1 - Doxygen

Scope: new or changed public entities under `dynamic-neural-field-composer/include/`.

Each needs:
- `@brief` - one line, what it does
- one `@param` per parameter, names matching the signature exactly
- `@return` unless the return type is `void`

Flag three failure modes:
- **Missing** - new public function/class/struct with no block.
- **Stale** - a parameter was renamed, added or removed and the block still describes the
  old signature. This is the most common and the easiest to miss.
- **Wrong** - the description contradicts what the code now does.

Private helpers in `src/` do not need Doxygen.

## Pass 2 - Wiki

`dynamic-neural-field-composer/wiki/` has 15 pages. Map the change to its page:

| Changed | Page |
|---|---|
| Element behaviour, new element type | `Elements.md`, `Element Reference.md` |
| Element parameters, tuning defaults | `Element Reference.md`, `Parameter Tuning Guide.md` |
| GUI, windows, node editor | `Application and UI.md` |
| Simulation loop, timing, recorder | `Simulation.md` |
| Plots, heatmaps, visualization | `Visualization.md` |
| Build, dependencies, setup | `Getting Started.md`, `Troubleshooting.md` |
| Public API shape, architecture | `Architecture.md`, `How to Add New Elements.md` |
| New example executable | `Examples.md`, `How to Create and Run Your Own Example Executable.md` |
| Test infrastructure | `Testing.md` |

Rule of thumb: **if a user could notice the change without reading the source, a wiki page
owes them an explanation.** Pure internal refactors do not.

## Pass 3 - Stale references

Grep the repo for references the change invalidated:

```bash
grep -rn "<old_symbol>" README.md CONTRIBUTING.md CHANGELOG.md dynamic-neural-field-composer/wiki/ .claude/
```

Look for renamed or removed symbols, moved file paths, changed build commands or flags,
and example snippets that no longer compile. Check `README.md` and `CONTRIBUTING.md`
specifically when the build process or directory layout moved.

## Output

For each pass: either "clean" or a concrete list of file + line + what is wrong. If nothing
in the diff touches public API or user-visible behaviour, say so and stop - a refactor with
no API change legitimately needs no doc update.
