---
name: unity-localize-content
description: Implement Unity localized strings, assets and locale changes with stable table identities and owned asynchronous lifetimes.
engines: [UNITY]
---

# Unity Localize Content

## When to use

Localize an existing Unity game's text, fonts, images or audio, including changing locale during loading. This skill owns content resolution; the selected UI workflow owns layout and focus.

## Activation and inputs

Run `commands/resolve-engine.sh` and `commands/resolve-skill.sh unity-localize-content`; require effective `UNITY` compatibility before production edits or tool launches. Honor task override evidence and its output scope. A skill request does not select an engine.

Inspect the actual Editor, Localization and Addressables versions, configured locales, table collections, UI stack, fallback policy and target platforms. Use installed package documentation; do not add packages, locales or remote providers implicitly. Record observations and evidence under the resolved `.hephaera/.cache/` task directory.

## Workflow

1. Inventory existing content and bindings before changes. Preserve Canvas/screen hierarchy, unrelated listeners, shared table GUIDs and entry IDs. Add or repair the smallest owned binding; do not rebuild the scene to localize one label.
2. Define locale startup and persistence, required coverage and missing-key behavior. Await initialization before resolving content; handle unavailable settings, locale and tables as explicit errors or the project's declared fallback.
3. Use stable table/entry references. Separate translated text from gameplay keys; retain stable IDs through imports and CSV round trips. Review placeholders, Smart String arguments, plurals and escaped markup with translators.
4. Give each displayed binding an owner and request generation. A late result from an older locale, closed screen or replaced asset must not overwrite current content. Detach only owned callbacks and release only owned resource references on disable, cancellation or replacement.
5. Review text expansion, shaping, bidirectionality and font/fallback coverage through the chosen TMP/TextCore stack. Localize accessible labels, input prompts and media alternatives as well as visible captions.
6. Verify offline and target-player behavior, including cold loads and rapid locale changes. Do not use blocking localization calls on web targets or assume an Editor cache proves build inclusion.

Read [locale and resource ownership](references/locale-lifecycle.md) for async bindings, asset handles, import identity and test design.

## Output and verification

Deliver version-qualified bindings and tables, locale/fallback and handle-ownership decisions, coverage findings and a target layout matrix. Test missing keys, format errors, plural categories, A→B→A during loading, screen teardown, unrelated listener survival, font misses and remote/offline failures.

Record expected/observed results, environment and evidence; mark unavailable player/device checks blocked or not run. Successful string lookup cannot certify translation quality, font shaping or accessible presentation. Cloud translation, external exports and service activation require their own authorization.
