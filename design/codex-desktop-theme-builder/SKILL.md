---
name: codex-desktop-theme-builder
description: Design, implement, validate, package, and privacy-audit reversible themes for Codex Desktop, including visual concept translation, isolated CSS/JavaScript injection, conversation running/completed states, model-menu overflow fixes, animated canvas effects, launcher shortcuts, and pet overlay isolation. Use when a user asks to create, refine, debug, distribute, or sanitize a custom Codex Desktop theme without modifying the signed application installation.
---

# Codex Desktop Theme Builder

Build themes as reversible overlays around an isolated Codex Desktop instance. Preserve native interaction, accessibility, readability, and the signed installation.

When a working implementation is more useful than a blank start, use the bundled [Inori Frost template](assets/templates/inori-frost-theme/README.md). Copy the complete template directory to a separate project before changing or running it; treat its character art, selectors, colors, labels, and motion as replaceable example content.

## Workflow

1. Capture the visual contract.
   - Separate palette, material, hierarchy, motion, character placement, and state semantics.
   - Convert references into design principles; do not reproduce unrelated people, text, accounts, or work data.
   - Keep character art on the home screen unless the user explicitly requests it elsewhere.
   - Decide whether to start from the bundled template or build a smaller theme from scratch.

2. Inspect the real application.
   - Launch a dedicated profile and remote-debugging port.
   - Inspect current DOM attributes and computed styles before choosing selectors.
   - Prefer semantic attributes and component roles over generated classes, positions, or localized labels.

3. Implement an idempotent injector.
   - Inject one versioned style node and only the decorative nodes the theme owns.
   - Reuse owned nodes on repeated passes; remove stale nodes during upgrades or skipped routes.
   - Never patch the installed package, signatures, application resources, or the user's normal profile.

4. Model page and task states.
   - Keep home, running conversation, completed conversation, and pet overlay as distinct states.
   - Detect running/completed state from the native primary action, using accessible attributes first and a narrow structural fallback second.
   - Observe only attributes needed for state transitions to avoid mutation loops.

5. Layer visual effects safely.
   - Put non-interactive decoration behind content with `pointer-events: none`.
   - Use separate static and animated layers so central reading space can be quieter than edges.
   - Hide horizontal overflow only on the verified menu container; preserve vertical scrolling and sliders.
   - Provide a useful static appearance under `prefers-reduced-motion: reduce`.

6. Isolate auxiliary windows.
   - Detect `avatar-overlay` before injecting.
   - Remove previously owned theme nodes/classes from that route and return immediately.
   - Verify the pet window remains transparent after restart.

7. Validate in the real UI.
   - Check home, running, completed, task switching, menus, reduced motion, narrow windows, and pet overlay.
   - Inspect computed animation names, durations, overflow axes, node counts, and root state in addition to screenshots.
   - Treat screenshots as temporary QA artifacts unless they are synthetic and contain no user or work data.

8. Sanitize and release.
   - Read [references/qa-and-release.md](references/qa-and-release.md) before publishing.
   - Run `scripts/audit-theme-repo.ps1` from the repository root before staging.
   - Remove UI screenshots, clipboard captures, local paths, logs, credentials, task text, and account identifiers from the release.
   - Review the staged diff, validate scripts/CSS/assets, then commit and push without rewriting history unless the user separately authorizes and understands that operation.

Read [references/implementation-patterns.md](references/implementation-patterns.md) when implementing or repairing injection, state detection, canvas effects, scroll behavior, or pet isolation.

## Bundled template

`assets/templates/inori-frost-theme/` demonstrates:

- isolated start/stop launchers and an idempotent injector;
- home-only character art and chat-only state decoration;
- distinct running and completed conversation visuals;
- restrained central motion with richer edge animation;
- model-menu horizontal overflow correction;
- optional shortcut and pet installation with overlay isolation.

Copy the full directory so its runtime-relative asset paths remain valid. Rename theme-owned IDs, classes, labels, profile directories, and package names when creating a new theme. Replace the example artwork unless its use and redistribution rights are clear.

## Guardrails

- Preserve click targets, DOM order, keyboard navigation, and native control behavior.
- Keep all paths runtime-relative or environment-variable based; never publish a literal user profile path.
- Do not infer task progress from message language or visible prose.
- Do not use broad selectors that can style `avatar-overlay`, dialogs, sliders, or every scroll container.
- Do not publish real application screenshots merely as documentation.
- Report when sensitive files remain reachable through Git history even after deletion from the current branch.

## Deliverables

Produce only the files needed by the chosen distribution:

- theme CSS and versioned injector;
- start/stop launchers using an isolated profile;
- optional shortcut creator using the installed Codex icon;
- optional pet package kept independent from theme injection;
- a copied and renamed template when the bundled example is used;
- concise usage documentation;
- privacy audit result and validation summary.
