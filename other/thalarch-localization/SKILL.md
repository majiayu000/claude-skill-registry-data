---
name: thalarch-localization
description: >
  Localization and i18n quality workflow for multi-locale applications. Use when adding or changing
  user-facing strings, locale resources, plurals, formatting, RTL behavior, or when a UI redesign
  must remain complete and natural across all languages supported by the project.
---

# Thalarch Localization

Localization completeness is a product contract, not a side effect of the default locale compiling.

## 1. Discover the real locale surface

Inspect the repository rather than assuming a language list.

Identify:

- default locale resources;
- all translated locale/resource sets;
- plural/select resources;
- locale-specific assets/layout behavior where present;
- existing translation conventions and terminology;
- generated/localization tooling if the project uses one.

Do not add a new parallel i18n system when the project already has one.

## 2. Key parity

For changed user-facing strings, check:

- missing keys;
- extra/stale keys when relevant;
- duplicate keys;
- raw/unresolved key display risk;
- fallback to the default language that would create mixed-language screens.

A successful default-locale build does not prove translated resource parity.

## 3. Placeholder and formatting safety

Preserve the semantic contract of:

- positional placeholders such as `%1$s`, `%2$d`;
- number/date/time formatting;
- plural quantities;
- escaped apostrophes/quotes where the resource format requires them;
- markup/spans;
- newline intent;
- parameter order differences across languages.

Never "fix" a translation by deleting a placeholder needed by call-site logic.

## 4. Natural terminology

Translate for the product/domain, not word-by-word.

For established technical/product terms, determine whether the target locale normally:

- translates them;
- transliterates them;
- keeps the standard English/product spelling.

Terms such as `Equalizer`, `ReplayGain`, `Crossfade`, `Preamp`, codec names, protocol names, or brand
names may legitimately remain unchanged in some locales. Avoid awkward literal translations that a
native user would not recognize.

Do not invent premium/marketing wording absent from the source product intent.

## 5. Layout expansion

Review changed UI for:

- longer translations;
- wrapping;
- ellipsis/truncation;
- button width;
- chips/tabs/segmented controls;
- slider labels/units;
- dialog height;
- small-screen overflow;
- font scaling.

Short English source strings are not a safe layout bound.

## 6. RTL

For supported RTL locales, inspect:

- mirrored navigation/directional icons;
- start/end vs left/right alignment;
- padding/margins;
- row ordering when directionally meaningful;
- mixed LTR technical tokens inside RTL text;
- number/unit readability.

Prefer platform-aware start/end semantics and AutoMirrored icon variants where appropriate.

## 7. Translation review strategy

When authoritative human translations are unavailable:

- preserve existing project terminology;
- keep phrasing concise and idiomatic;
- avoid adding semantic claims not present in the source;
- flag uncertain high-impact wording rather than fabricating domain meaning.

Machine-generated text may be a draft, not proof of native-quality localization.

## 8. Automated checks

When practical, add or run checks for:

- key parity;
- placeholder signature parity;
- malformed resource syntax;
- duplicate identifiers;
- unresolved localization keys;
- locale resource compilation.

Keep checks aligned with the project's real resource format rather than installing a new framework
for a small change.

## 9. Rendered verification

For a UI change, combine with `thalarch-compose-ui` or the relevant platform UI skill.

Render representative locales, especially:

- one language with longer labels;
- one RTL locale when supported;
- the default locale.

Source-resource parity does not prove clipping, wrapping, or visual hierarchy.

## 10. Completion report

State:

- locales discovered;
- keys changed;
- parity/placeholder checks run;
- representative rendered locales tested;
- any translations/layouts still `UNVERIFIED`.
