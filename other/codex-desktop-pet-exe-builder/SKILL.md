---
name: codex-desktop-pet-exe-builder
description: Build, upgrade, package, and validate standalone Windows desktop-pet applications from approved transparent sprite atlases. Use when Codex needs to assess desktop-pet feasibility; scaffold or modify a WPF pet player; implement animation states, transparent or click-through windows, tray controls, drag behavior, settings migration, single-instance handling, or per-user autostart; publish a self-contained single-file EXE; create an Inno Setup installer; or run real-window, install, uninstall, signing, and privacy QA for a Windows pet release.
---

# Codex Desktop Pet EXE Builder

Turn an approved animated-pet atlas into a Windows application through an explicit runtime contract, deterministic build pipeline, isolated system testing, and privacy-safe release. Keep art production separate from application engineering.

## Set the input boundary

Require an approved transparent atlas and a machine-readable animation map before writing the player. Record cell size, grid size, state names, used frames, frame durations, default state, resource hash, and redistribution rights.

Do not generate or repair character art in this Skill. If the atlas is incomplete, visually ambiguous, incorrectly keyed, or still awaiting approval, finish it with the appropriate pet-art workflow first.

If the user asks only for feasibility analysis, inspect the inputs and compare implementation routes without changing files or installing build dependencies.

## Read references as needed

- Read [references/runtime-architecture.md](references/runtime-architecture.md) before scaffolding the app, changing window behavior, or adding interactions.
- Read [references/build-and-packaging.md](references/build-and-packaging.md) before publishing a portable EXE, creating an installer, changing identifiers, or localizing setup.
- Read [references/qa-and-release.md](references/qa-and-release.md) before interaction testing, installation testing, upgrade work, signing decisions, or public release.

## Freeze the product contract

Before implementation, record:

- public product and pet display names;
- stable assembly name, application id, installer AppId, mutex name, settings location, autostart value name, and install directory;
- supported Windows versions, CPU architecture, .NET target, and publish RID;
- atlas geometry, state map, frame timing, and embedded resource name;
- default window scale, topmost, click-through, movement, and animation intervals;
- portable EXE, installer, upgrade, uninstall, localization, and code-signing scope.

Treat display names as presentation. Do not change stable internal identifiers during a rename unless the user explicitly wants a breaking migration.

## Use a gated implementation workflow

1. Validate the approved inputs.
   - Check file identity, dimensions, alpha, grid divisibility, row and frame bounds, and state timing.
   - Render representative cells without resampling and verify the first idle frame is useful as a static fallback and icon source.

2. Scaffold the Windows runtime.
   - Prefer WPF for a Windows-only lightweight pet unless requirements justify another framework.
   - Target a supported .NET LTS Windows Desktop runtime and pin the exact SDK used by the build.
   - Embed the atlas and icon; never depend on a developer-machine absolute path at runtime.

3. Implement the window and player.
   - Use a transparent, borderless, taskbar-hidden window with explicit DPI and multi-monitor behavior.
   - Slice the atlas deterministically and drive frames from the animation map.
   - Define one priority order for shutdown, manual drag, hover or click reactions, explicit menu state, scheduled movement, scheduled non-movement animation, pause, and idle.
   - Keep movement and cosmetic-animation schedules independent, with separately persisted intervals and deterministic short-interval test controls.
   - Prevent timers from overwriting a higher-priority interaction.

4. Add desktop integration.
   - Provide a tray menu for show or hide, pause, state selection, scale, topmost, click-through, autostart, reset, and exit as required.
   - Persist settings atomically, normalize every value, and migrate missing fields without overwriting existing choices.
   - Enforce one instance and support a deterministic shutdown path for testing.
   - Use current-user autostart when administrative installation is unnecessary.

5. Add deterministic self-test hooks.
   - Test atlas geometry, state and frame maps, embedded resources, defaults, settings round trips, runtime architecture, and version metadata without opening the UI.
   - Support isolated settings storage and controlled state or shutdown arguments for QA. Never point tests at a user's live settings.

6. Publish and package.
   - Restore and publish with the same explicit RID.
   - Produce a self-contained single-file portable EXE and fail immediately on every native command error.
   - Wait explicitly when invoking a GUI executable for self-test output.
   - Build a one-file installer that uses stable identifiers, a stable per-user install location, upgrade-safe metadata, optional shortcuts and autostart, and complete uninstall cleanup.

7. Run release QA.
   - Execute compile, self-test, real-window, interaction, independent-scheduler, single-instance, pause, install, autostart, upgrade, uninstall, and residue checks.
   - Capture only the application window or a tight surrounding region; never publish full-desktop screenshots by default.
   - Rebuild after every source fix and rerun every downstream test against the new binaries.

8. Audit the release.
   - Run `scripts/audit-windows-pet-release.ps1` on the final portable and installer EXEs.
   - Run repository privacy audits before staging and with history scanning before pushing.
   - Review the exact staged diff, every binary's purpose and rights, the public remote, and noreply commit metadata.

## Repair the smallest valid scope

- Resource or atlas-map failure: fix input registration or reject the input; do not silently reinterpret geometry.
- State arbitration failure: fix priority and cancellation rules, then rerun affected interactions and timer tests.
- Settings failure: repair normalization or migration and retest old and new schemas in isolated directories.
- Window automation failure: distinguish test timing or handle discovery from product behavior before changing the app.
- Installer failure: fix the installer or audit script without regenerating application art.
- Test-framework failure: prove actual system state independently, repair the test, then rerun the complete assertion set.

After the same root failure occurs twice, change the diagnostic method or design instead of repeating the same input sequence.

## Release boundaries

Keep source art, task transcripts, full-screen captures, test settings, local paths, build caches, signing secrets, certificates, passwords, logs, rejected binaries, and installer sandboxes outside the public release.

Report unsigned binaries honestly. Code signing is a separate credentialed release step; never extract, copy, invent, or publish signing material.

Deliver:

- source project and pinned build configuration;
- self-contained portable EXE;
- optional one-file installer;
- repeatable self-test and installer audit;
- tight application-only QA evidence;
- release summary with version, architecture, signing status, known limitations, and privacy result.

Do not include a README inside the Skill itself. Repository-level documentation may describe installation and invocation.
