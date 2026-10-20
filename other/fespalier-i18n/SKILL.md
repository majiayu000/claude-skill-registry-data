---
name: fespalier-i18n
description: "Translated texts in a fespalier app with fespalier_tolgee (since 0.10.0) — the language from the URL ($lang enum segments and route.dart paths spellings) through TranslationScope.routerConfig on MaterialApp.router, context.tr and TrText with ICU plurals and selects, bundled ARB or Tolgee JSON assets that show on the first frame and offline, Tolgee Content Delivery over the air with an ETag cache in dataCacheStorage and the fallback chain, a language menu with relocate, the first URL from preferredLocale, debug-only in-context editing with no API key in a build, and fakeTranslations in tests. Load before adding translations, localizing an app, wiring Tolgee, a language switcher or right-to-left text, or when a page shows raw keys, the wrong language, No TranslationScope found or No MaterialLocalizations found."
---

# fespalier-i18n

> **Verified against fespalier `589cf391` (2026-10-08), release v0.13.0.**
> These skills ship in the fespalier repository, and CI checks them against its code
> on every change. Version-sensitive claims say the release they became true in; if
> your app pins another fespalier, trust that release's code over this page. See
> [Versions](https://github.com/fespalier/fespalier/blob/main/skills/README.md#versions).

**Since 0.10.0.** `package:fespalier_tolgee` gives an app translated texts that show at once, keep working offline and
can be updated without a release: the texts bundled in the app are the floor, [Tolgee](https://tolgee.io)'s Content
Delivery (or a `TranslationSource` you write) brings fresh ones, and **the language comes from the URL**. It adds no
file kind, no `fespalier:` key and no `fsp` command, and `app.g.dart` is the same bytes. It is **not** the `tolgee`
SDK: that one imports `dart:io` (no web), keeps the locale in a static singleton, can put the network before `runApp`,
and runs in-context editing on the production key. A release that predates 0.10.0 has no such package.

## Install

```yaml
# pubspec.yaml: the same url and the same ref as fespalier, or pub refuses to resolve
dependencies:
  fespalier:
    git:
      url: https://github.com/fespalier/fespalier
      path: packages/fespalier
      ref: <the tag of your fespalier>
  fespalier_tolgee:
    git:
      url: https://github.com/fespalier/fespalier
      path: packages/fespalier_tolgee
      ref: <the same tag>
  flutter_localizations:
    sdk: flutter
flutter:
  assets:
    - assets/i18n/
```

(A fragment: pub resolves the pair only at a release tag that contains the package, 0.10.0 or later. Write `ref: v…`
with a real tag in an app, but never in these pages, where `cli/tests/versions.rs` would read it as fespalier's own
version. The package's own
[install block](https://github.com/fespalier/fespalier/blob/main/packages/fespalier_tolgee/README.md#install) is the
one release-please keeps current.) For a cache that survives restarts add `fespalier_storage` and use its
`PrefsDataStorage` as `dataCacheStorage` (see [`fespalier-data`](../fespalier-data/SKILL.md) (its `storage-backends.md` page)).

## The shape of it

One enum for the languages, a setup in `startup()`, an app that gives `MaterialApp.router` the **scope's router
config**, and pages that ask for the language by its enum.

```dart
// lib/lang.dart
enum Lang { en, fr, de }
```

```dart
// lib/app/startup.dart
import 'package:fespalier/startup.dart';
import 'package:fespalier_tolgee/fespalier_tolgee.dart';
import 'package:my_app/lang.dart';

const _cdn = String.fromEnvironment('TOLGEE_CDN_URL'); // public, not a secret

Future<List<Override>> startup() async => [
  translationsConfig.overrideWithValue(
    Translations(
      // Local assets only: assets/i18n/en.arb, fr.arb, de.arb. A missing file throws, and splash.dart offers the retry.
      bundled: await BundledTranslations.load(locales: Lang.values.map((l) => l.name)),
      baseLocale: 'en',
      remote: _cdn.isEmpty ? null : TolgeeCdn(Uri.parse(_cdn)),
    ),
  ),
];
```

```dart
// lib/app/app.dart
import 'package:fespalier/fespalier.dart';
import 'package:fespalier_tolgee/fespalier_tolgee.dart';
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

class App extends ConsumerWidget {
  const App({super.key, required this.router});

  final GoRouter router;

  @override
  Widget build(BuildContext context, WidgetRef ref) => MaterialApp.router(
    routerConfig: TranslationScope.routerConfig(router, localeOf: localeSegment()),
    supportedLocales: ref.watch(translationsConfig).supportedLocales.map(localeFromTag),
    localizationsDelegates: GlobalMaterialLocalizations.delegates,
  );
}
```

```dart
// lib/app/$lang/products/page.dart
// -> /en/products, /fr/products, /de/products
import 'package:fespalier_tolgee/fespalier_tolgee.dart';
import 'package:flutter/material.dart';
import 'package:my_app/lang.dart';

class ProductsPage extends StatelessWidget {
  const ProductsPage({super.key, required this.lang});

  final Lang lang; // asking for it is what types the segment as the enum: /xx/products is not found

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const TrText('products.title')),
    body: Center(child: Text(context.tr('product.stock', {'count': 3}))), // {count, plural, ...}
  );
}
```

```yaml
# pubspec.yaml dependencies
  flutter_localizations:
    sdk: flutter
```

The catalog behind it, one file per language (a fragment, not built):

```json
// assets/i18n/fr.arb
{
  "@@locale": "fr",
  "products.title": "Produits",
  "product.stock": "{count, plural, =0 {Épuisé} one {# en stock} other {# en stock}}"
}
```

## Golden rules

- **Give `MaterialApp.router` `routerConfig: TranslationScope.routerConfig(router, localeOf: ...)`, never the
  router itself.** The config wraps go_router's root Navigator in the scope, so the first frame is already in the
  route's language and a dialog on the root navigator is under it too.
- **`localizationsDelegates: GlobalMaterialLocalizations.delegates` is required** (and `flutter_localizations` in the
  pubspec). Without it a route in a language the app has no `MaterialLocalizations` for makes an `AppBar` or a
  `BackButton` throw `No MaterialLocalizations found.`
- **The locale comes from the route.** A `data.dart` takes `required Lang lang`; there is no global locale and no
  `setLocale`. A language menu navigates (`relocate`, below).
- **Bundled texts are the floor.** Every locale you list is read from `assets/i18n/` before the first frame; a missing
  asset makes `startup()` throw (so `splash.dart` offers the retry), and **the base locale must be bundled**.
- **Never an API key in a build.** `TolgeeCdn` has no parameter for one. The only key is the in-context editor's,
  passed with `--dart-define-from-file=tolgee.local.json` (gitignored) to a **debug** run; release builds pass only
  `TOLGEE_CDN_URL`.
- **A test passes its own `app:`.** `pumpRouter`'s default app is a bare `MaterialApp.router` with no scope, and
  `context.tr` there throws. [`references/testing.md`](references/testing.md).

## Traps

- **No `translationsConfig` override means every key renders as itself, silently** (`Translations.none`). Raw keys on
  screen: the override is missing (a test does not run `startup()`), or the key is a typo; `Translator.originOf(key)`
  says which link answered, or `TranslationOrigin.missing`.
- **The enum segment only takes effect if some file asks for `required Lang lang`.** Otherwise `$lang` is a `String`
  and `/xx/products` matches. A tag like `pt-BR` cannot be an enum name: use a `String` segment, which the scope
  resolves against what you bundled (`pt-BR` to `pt`).
- **Spellings alone do not give the canonical path a locale.** With `const paths = {'fr': 'produits'}` and no `$lang`
  folder, `/products` says nothing: the locale is then the previous one, or the device's (`preferredLocale`).
- **ICU apostrophes are quotes.** `l'{app}` renders `l{app}`; write `l''{app}`. Files written for `gen-l10n` may need
  an apostrophe before `{` or `}` doubled.
- **Numbers are not locale-formatted** (`1000`, not `1 000`). `selectordinal` is **not supported**: the message is shown
  as written and reported once in debug. Plural categories come from `intl` (French 0 is `one`; 1.5 is `other`); a
  `select` given an enum matches on its `name`.
- **A CDN failure is silent.** The app keeps the cache, then the bundled text, and nothing is printed. Tolgee publishes
  after up to 15 minutes; a locale is fetched **once per container**; `refreshOnResume` is off by default and
  `refreshOnReconnect` acts only after a **failed** fetch. The web needs CORS headers on the CDN.
- **Hive storage gives the cache one frame later**; `PrefsDataStorage` gives it on the first frame.
- **`adapters: [fespalier_tolgee]` does not compile**: the package has no `fespalier_adapter.dart` (the setup is app
  code, which `startup()` already is). `Target of URI doesn't exist` names the file.
- `localeSpelling` and `relocate` need `AppManifest` (from `app.g.dart`, or the library `output_manifest` names).

## What it does not do

Typed keys (gen-l10n's job: an app may keep gen-l10n beside this, its getters are just not updated over the air), the
`tolgee` SDK's widgets, a polling refresh, `fespalier_adapter.dart`, and telemetry (none in v1; a later span would never
carry keys, texts or the CDN URL). It starts no timer and adds no listener of its own.

## References

| Need                                                                                        | Page                                                                                                    |
| ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `$lang` versus `paths`, `localeSegment`, `localeSpelling`, the language menu, the first URL | [`references/locales-and-the-url.md`](references/locales-and-the-url.md)                                |
| ARB and Tolgee JSON, the ICU subset, `tolgee pull`, gen-l10n beside it or migrating from it | [`references/messages-and-catalogs.md`](references/messages-and-catalogs.md)                            |
| `TolgeeCdn`, ETags, the fallback chain, the cache key, a `TranslationSource` of your own    | [`references/over-the-air-and-cache.md`](references/over-the-air-and-cache.md)                          |
| The debug-only panel, `tolgee.local.json`, key scope, `RecordingEditor`                     | [`references/in-context-editing.md`](references/in-context-editing.md)                                  |
| `fakeTranslations`, `FakeTranslations`, a restart, `fsp test` and `setup.dart`              | [`references/testing.md`](references/testing.md)                                                        |
| An error message, or a symptom                                                              | [`fespalier-troubleshooting`](../fespalier-troubleshooting/SKILL.md) (its `diagnostics-tolgee.md` page) |
| The route side: `route.dart` `paths`, `locationFor`, `locale:`                              | [`fespalier-routing`](../fespalier-routing/SKILL.md) (its `route-dart.md` page)                         |

## Example

`examples/i18n` (in the fespalier repository) is this skill as a runnable app: `lib/app/startup.dart` (bundled ARB assets), `app.dart` (the scope's `routerConfig`), `$lang/layout.dart` (a language switch with `relocate`), `products/` (an ICU plural and a `paths` spelling) and `test/i18n_test.dart` (`pumpRouter(app:)`, `FakeTranslations`, `fakeTranslations`), with no network and no key.

## Where the code is

`packages/fespalier_tolgee/lib/src/`: `scope.dart` (`TranslationScope`, `context.tr`, `TrText`), `providers.dart`
(`translationsConfig`, `translator`, `preferredLocale`, the fetcher and the cache), `translator.dart` (the chain,
`originOf`), `icu.dart`, `locale.dart` (`localeSegment`, `localeSpelling`, `relocate`), `tolgee_cdn.dart`,
`bundled.dart`, `in_context/`; `lib/testing.dart`; `test/no_timers_test.dart` and `test/no_secrets_test.dart` grep
`lib/` for timers and for key code. The guide is
[`docs/i18n-tolgee.md`](https://github.com/fespalier/fespalier/blob/main/docs/i18n-tolgee.md).
