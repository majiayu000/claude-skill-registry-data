---
name: electron-playwright-validator
description: >-
  This skill should be used when a user asks to launch, inspect, automate, test,
  validate, or debug an Electron desktop UI through Playwright/CDP, including
  blank renderers, runtime import failures, accessibility snapshots, layout
  defects, click-through flows, or post-change checks. Not for native macOS or
  mobile apps, browser-only pages, or unit-level IPC tests. The target project
  must provide Electron and Playwright.
---

# Electron Playwright Validator

Use the bundled `e-cli` as the interface. It keeps one Electron process alive
and connects subsequent commands through CDP, avoiding repeated startup cost.

## Resolve the bundled tool

The executable is `scripts/e-cli` relative to this skill directory. Resolve that
path from the host's skill context. In a full plugin install the equivalent path
is:

```bash
E_CLI="${CLAUDE_PLUGIN_ROOT}/skills/electron-playwright-validator/scripts/e-cli"
```

Verify `"$E_CLI" --help`, then run from the project root. The tool resolves
Electron and Playwright from the project's dependencies; do not install global
copies or silently change the project's toolchain.

Direct skill installs can resolve `scripts/e-cli` from the skill directory. Use
`node "$E_CLI"` when a distribution loses executable mode.

## Drive one observable transaction at a time

1. Launch the app.
2. Read an accessibility snapshot.
3. Resolve one target from current state.
4. Act.
5. Wait for a product postcondition, then snapshot again.
6. Capture pixels only when they can reveal a rendering or layout defect.
7. Close the session when validation finishes.

Treat launch, interaction, and product success as separate claims. A successful
click does not prove the view changed correctly.

## Prefer semantic state

Use role and accessible-name selectors before text, test IDs, or CSS. The
snapshot is both the discovery surface and the primary behavioral assertion.
Load `references/accessibility-selectors.md` only when selector construction is
non-obvious.

Electron rendering is asynchronous. Wait for the resulting element or state
instead of relying on an arbitrary sleep. Snapshot again after navigation,
modal changes, or asynchronous content. Read
`references/electron-gotchas.md` for lazy rendering, terminal surfaces, and
timing failures.

For multi-window apps, run `e-cli pages` and select the intended renderer rather
than assuming the first window is the product surface.

## Bound visual context

Save screenshots to disk. When the host retains and resends image inputs, use a
bounded isolated visual task and return only its compact text finding to the
driver. A small before/after pair may share one visual task when comparison is
the decision. If isolation is unavailable, inspect the smallest necessary image
or crop and avoid accumulating screenshots in a long-running context.

Use pixels for blank surfaces, broken styles, clipping, overlap, contrast, and
layout. Do not take a screenshot merely because the command exists.

## Diagnose runtime failures

A typecheck can pass while the packaged renderer fails at runtime. On a blank
or error screen, inspect:

- launch stderr and renderer console output;
- the root element and document title;
- preload bridge availability;
- dynamic import and packaging errors;
- the fresh accessibility snapshot and screenshot.

Use `e-cli logs` for captured process/renderer diagnostics. `e-cli eval` runs
arbitrary JavaScript with renderer and preload privileges; prefer read-only
expressions and do not call mutating bridge methods unless the user requested
that effect. The full contract lives in `references/e-cli-reference.md`; prefer
live `"$E_CLI" --help` when they differ.

## Choose the durable test boundary

Use `e-cli` for interactive exploration, reproducing runtime failures, and
checking a specific rendered state. Use the project's existing Playwright E2E
suite for deterministic regression and CI. Convert a discovered regression
into a durable test when the behavior is important enough to prevent from
returning.

Always close the session, including after failure, and surface cleanup errors
rather than leaving a process that blocks the next run.

Keep `.e-cli-state.json`, `.e-cli-launch.lock`, and screenshot artifacts out of
version control.
