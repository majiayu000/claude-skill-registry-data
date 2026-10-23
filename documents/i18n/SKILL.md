---
name: i18n
description: >-
  Add, change, or translate user-facing text in the Lyrion Dashboard, which
  ships bilingual FR/EN. Use this whenever a task introduces a new visible
  string (a label, tooltip, aria-label, empty state, stat name), changes
  wording, or touches the README or a `docs/` page — so every string lands in
  both languages and the EN/FR documentation pairs stay in sync. Covers
  `i18n.py`, how templates and JS consume translations, and the parity rule.
---

# Internationalization (FR/EN)

The whole UI is bilingual. There is one source of truth for UI strings — `i18n.py` — and two parallel READMEs. The cardinal rule: **a string never exists in only one language.** Adding an English label without its French counterpart (or vice-versa) is the bug this skill exists to prevent.

## How it works

`i18n.py` holds a `TRANSLATIONS` dict with a `fr` and an `en` sub-dict sharing the **same keys**. Language is chosen per request from the browser's `Accept-Language` header, defaulting to English:

```python
SUPPORTED = ("fr", "en")
DEFAULT_LANG = "en"

def pick_lang(accept_languages):
    return accept_languages.best_match(SUPPORTED) or DEFAULT_LANG
```

The route resolves the language and hands the **entire** chosen dict to the template as `t`, which is also serialized to JS so client-side strings share the same source:

```python
lang = pick_lang(request.accept_languages)
return render_template("nowplaying.html", lang=lang, t=TRANSLATIONS[lang], ...)
```

## Adding or changing a UI string

1. Add the key to **both** `fr` and `en` in `TRANSLATIONS`, under the matching comment section (`# Now playing`, `# Stats`, ...). Keep the two sub-dicts in the same order so a missing key is visible at a glance.
2. Use the key in the template via `t`, e.g. `{{ t.stats_title }}` or `aria-label="{{ t.choose_player }}"`. Many existing strings are tooltips / `aria-label`s — user-facing text in attributes counts too.
3. For client-side text, read it from the serialized `t` in `static/nowplaying.js` rather than hardcoding a literal — that's why the whole dict is exposed.
4. Never hardcode a display string in a template or JS. If it's visible to a user, it's a translation key.

**Keys are stable identifiers, not English text** — snake_case describing the role (`retry_lyrics`, `empty_state`), so the English wording can change without renaming the key.

## The parity test

`tests/test_i18n.py` turns the cardinal rule into a gate: `fr` and `en` must hold the same keys, no string may be blank, every `I18N.key` in `static/*.js` and every `t.key` in `templates/*.html` must be translated in both languages, and no key may survive with nothing reading it. Without it a missing key is silent — Jinja renders it as an empty string, and the JS hands `undefined` to a DOM property, so the tooltip reads the literal "undefined". The unused-key half is only exhaustive while access stays static: a computed `I18N[name]` would have to be taught to `referenced_keys()`.

## Documentation parity

Every documentation page exists twice, linked to its counterpart at the top:

- `README.md` (EN, primary) / `README.fr.md` (FR) — the landing page: features, demo gallery, install, security.
- `docs/configuration.md`, `docs/logs.md`, `docs/endpoints.md`, `docs/scripts.md` and their `.fr.md` counterparts — the detail the README links to.

Any change to one — a new feature bullet, a changed requirement, a restructured section — must be mirrored in the other in the same place. They should differ only in language, never in content or structure. When you edit one, edit the other in the same change.

`android/README.md` is deliberately English-only: it is contributor documentation (Gradle build, signing, CI, F-Droid packaging), and what a French user actually reads about the app is translated elsewhere — the READMEs, the UI, and the store listing under `fastlane/metadata/android/`. Every link to it from the FR README carries an "(en anglais)" flag — there are three, in the features list, the install section and the documentation list. Don't create a `.fr.md` for it; do keep that flag if the link moves.

## Checklist

- [ ] New UI string → key added to **both** `fr` and `en` in `i18n.py`.
- [ ] Keys are snake_case role names, present in both sub-dicts in the same order.
- [ ] Template/JS reads the string through `t`, nothing hardcoded.
- [ ] `python -m unittest tests.test_i18n` green — parity, every key the page reads translated, no orphan key.
- [ ] README or `docs/` page edited? Its counterpart in the other language got the same edit.
