---
name: clarila-stylex
description: Set up, author, migrate, audit, and debug StyleX in JavaScript or TypeScript applications using current official Meta/StyleX guidance. Use for StyleX compiler configuration, static styles, variables, themes, typed style props, linting, CSS extraction, or migrations to StyleX. Do not use for general visual design that does not involve StyleX.
license: Private skill; bundled StyleX references are MIT licensed, see references/stylex-license.txt.
metadata:
  compatibility: Requires Go 1.27.3 and network access for live official-source refresh. Verified cached references support offline use.
---

# StyleX

Use the official Meta/StyleX documentation as the technical authority. Project instructions and public component contracts still own product-specific restrictions; do not present local design-system policy as a StyleX requirement.

## Refresh official guidance

At the start of every invocation, run the synchronizer with the installed Go toolchain. Resolve `STYLEX_SKILL_DIR` to this skill's directory.

```bash
sh "$STYLEX_SKILL_DIR/scripts/sync-official-sources.sh" --json
```

This resolves `facebook/stylex` `main` to one immutable commit, downloads and validates the complete guides/license bundle, then publishes it under the user's external cache. The installed skill and bundled fallback remain unchanged. Use the returned `reference_dir`, `source_commit` and `manifest_sha256` as the exact reference identity; read guides from that directory. A file lock serializes refreshes, complete bundles have immutable commit paths, and an atomic selection points readers at one verified bundle. `--cache-dir` selects another external cache. `--check` or `--offline` verifies existing guidance without network or writes. If live refresh is unavailable, complete manifest/hash verification permits cached use; disclose that upstream was not freshly checked. An invalid selected bundle fails. Stop before StyleX claims when the helper exits unsuccessfully.

Then read only the references needed for the request:

- Setup, compiler, bundler, PostCSS, CSS layers, TypeScript, ESLint, or missing styles: `stylex-installation.md` in the returned reference directory (bundled fallback: [installation](references/stylex-installation.md)).
- Component authoring, composition, selectors, responsive styles, variables, themes, or typed style props: `stylex-authoring.md` in that same directory (bundled fallback: [authoring](references/stylex-authoring.md)).
- Audit or migration of an existing codebase: read both.

For an API or option not covered there, use the current official docs at `https://stylexjs.com/docs/llms-full.txt` or the installed package source. Community posts and skills may identify questions, but may not establish correctness.

## Inspect before editing

Read repository instructions and trace the real style pipeline:

1. Record the installed versions of `@stylexjs/stylex`, compiler integration, framework, and build tool. Keep StyleX packages on matching versions.
2. Find the CSS entrypoint, compiler configuration, extraction configuration, source include patterns, aliases, and module-resolution settings.
3. Inspect representative variable files, component styles, style-prop boundaries, and the active ESLint configuration.
4. Search for legacy styling only within the user-approved scope. Do not remove a coexistence path until its consumers are gone.

## Apply the official model

- StyleX is a compile-time system. A successful production transform and extracted CSS are required proof; runtime calls or TypeScript alone are insufficient.
- Keep ordinary `stylex.create()` definitions at module scope and colocated with the component unless a genuinely shared recipe already owns them.
- Keep raw style objects statically analyzable. Use literals, supported compile-time expressions, StyleX variables/constants, and sparse dynamic style functions only where runtime values are truly required.
- Apply styles with `stylex.props()` on React DOM host elements. For custom components, expose a typed style prop and apply it at the owned host element.
- Compose base, variant, state, and caller styles in intended precedence order. Account for the configured `styleResolution`; do not repeat the inaccurate claim that every shorthand/longhand conflict is simple last-wins.
- Prefer longhands or single-value shorthands. Put pseudo-classes and at-rules inside property values, include `default`, and use `null` when no default rule should be emitted.
- Avoid unnecessary `::before` and `::after`; prefer semantic elements when they improve accessibility and reduce CSS.
- Use dynamic style functions sparingly; prefer static conditional composition for finite variants.
- Put `defineVars()` and `defineConsts()` in `*.stylex.ts` or `*.stylex.js` files as named exports with no unrelated exports. Use constants for static values and variables only when runtime or subtree overrides are needed.
- Use `createTheme()` for variable overrides on a DOM subtree. Preserve package and compiler alias resolution for imported StyleX variable files.
- Enable the official recommended ESLint rules. Add optional rules such as extension enforcement or sorting only when they fit the repository's conventions; label them optional rather than official requirements.
- With the PostCSS integration, include every source package that authors StyleX, parse the repository's JS/TS syntax, import a CSS entry containing `@stylex;`, disable runtime injection for production, and make CSS-layer ordering explicit when other named layers coexist.

## Audit and change

Classify each checked area as one of:

- `PASS` — current code follows the applicable official guidance.
- `PROJECT POLICY` — a stricter local choice that remains valid StyleX.
- `FAIL` — a concrete incompatibility or missing proof; fix it at the responsible layer when the request authorizes changes.
- `UNRESOLVED` — insufficient evidence or an upstream limitation; do not guess.

Prefer existing repository patterns and the smallest evidence-backed correction. Preserve unrelated dirty work. Do not add a wrapper, dependency, token barrel, or abstraction merely because an example uses one.

## Verify

Run the smallest relevant check first. If it fails, fix the responsible layer and rerun that check. Once focused checks pass, run the repository's normal formatting, StyleX-aware lint, type, and test gates, followed by an uncached production build. Do not report completion while a required gate is failing.

Inspect the build output or emitted CSS sufficiently to prove that StyleX transformed application and shared-package sources. For visual behavior changes, use the project's rendered or visual-regression proof when available.

For a missing-CSS or monorepo failure, trace a representative rule from each affected source package through the compiler transform into the same production CSS artifact. Then check that the application's CSS entry loads that artifact. Record which include/alias boundary omitted the rule. Generated class names establish only the transform step. Cite the actual loaded manifest's commit-specific installation source, and check applicability to the installed package/compiler version; a newer upstream guide does not change the installed API.

## Report

For substantive execution, follow the current owner's [pinned poteto-mode workflow](../clarila/references/pstack.md) and actual applicable procedures. A delegated StyleX stage stays with its existing coordinator and source. The official-source refresh, project policy, compiler applicability and required build/runtime proof above retain their meaning.

State the result using `PASS`, `PROJECT POLICY`, `FAIL`, or `UNRESOLVED`, then include the supporting evidence, material changes, exact checks run, remaining visual/runtime boundary, and delivery state.

Report exact PASS/FAIL results, what the build proves, any unchecked runtime/visual boundary, and the precise delivery state. Never equate a local green build with a commit, push, merge, deployment, or release.
