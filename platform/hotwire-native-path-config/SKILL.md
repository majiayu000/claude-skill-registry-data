---
name: hotwire-native-path-config
description: Author and validate Hotwire Native path configuration (the JSON that drives native push/replace/modal/tab navigation on iOS + Android), and the Rails-side turbo_native_app? + request-variant setup. Use when a native screen opens with the wrong presentation (pushed instead of modal, doesn't switch tabs), when adding a new native route, when setting up native navigation for one Rails app across iOS + Android, or when web chrome (top nav) leaks into the native apps. Provides a starter config, a schema/footgun validator, and an iOS↔Android drift check.
---

# Hotwire Native path configuration

One Rails app, two native shells. A **path configuration** JSON maps URL patterns to
native navigation rules (push / replace / modal / tab roots / image viewer) on iOS
and Android; the Rails side detects native via `turbo_native_app?` and serves trimmed
markup via request variants. This skill helps you author both correctly and keep the
two platform configs in sync.

Full schema + the server setup: [`references/path-config-guide.md`](references/path-config-guide.md). Real-world note:
`piazza-web/wip/analysis/05-hotwire-native-variants.md`.

## When to use

- A native screen opens with the wrong presentation (pushed when it should be modal,
  or doesn't switch the bottom tab).
- Adding a new native route / screen.
- Setting up native navigation for a Rails app across iOS + Android.
- Web chrome (top navbar) shows up inside the native apps.

## The model (1-minute version)

```json
{ "settings": {}, "rules": [
  { "patterns": ["/.*"],            "properties": { "context": "default", "uri": "app://fragment/web" } },
  { "patterns": ["^/$", "/profile$"], "properties": { "presentation": "replace_root", "uri": "app://fragment/web/tab" } },
  { "patterns": ["/new$", "/edit$"], "properties": { "context": "modal", "uri": "app://fragment/web/modal" } }
] }
```

- Rules match **top-to-bottom, later wins** → catch-all FIRST, specifics BELOW.
- `context`: `default` | `modal`. `presentation`: `default|push|pop|replace|replace_root|clear_all|refresh|none`.
- **Android** rules need a `uri` (deep-link to a registered destination). **iOS** uses
  `view_controller` / `modal_style` instead.
- Modal in 1.x = `context: "modal"`. `presentation: "modal"` is a Strada-beta-ism.
- **Tab switching**: tab-root URLs use `replace`/`replace_root`; a server **redirect**
  to a tab URL then selects that native tab instead of pushing. Keep tab-root patterns
  in sync with the native tab bar's URLs.

## Server side (don't forget)

```ruby
# strip web chrome + serve mobile markup for the native apps
def set_request_variant
  request.variant = turbo_native_app? ? :mobile : (Browser.new(request.user_agent).device.mobile? ? :mobile : :desktop)
end
```
`turbo_native_app?` (turbo-rails) is true because Hotwire Native appends
`Turbo Native` / `Hotwire Native` to the WebView User-Agent. Guard web-only nav with
`unless turbo_native_app?`.

## Start a config

```bash
sed 's/__SCHEME__/yourapp/g' templates/path_configuration.json.tmpl > path_configuration.json
```
Bundle it (iOS `Piazza/path_configuration.json`, Android `assets/json/configuration.json`)
or serve it from Rails (e.g. `/configurations/ios.json`) so you can change native
navigation without an app-store release — keep the bundled file as the offline fallback.

## Validate

```bash
scripts/lint_path_config.sh path_configuration.json           # one file
scripts/lint_path_config.sh --compare ios.json android.json   # cross-platform drift
```

Validation: valid JSON; `rules` present; each rule has `patterns` + `properties`;
regex patterns **compile**; property keys/values are in the 1.x schema; flags the
`presentation: "modal"` beta-ism; flags unanchored short patterns (`/new` also matches
`/renew` → use `/new$`); checks the catch-all is first. `--compare` normalizes anchors
and reports paths handled on one platform but not the other (heuristic, names its
ceiling). Needs `ruby`.
