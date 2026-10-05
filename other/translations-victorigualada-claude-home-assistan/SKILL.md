---
name: ha:translations
description: "Home Assistant translations — strings.json anatomy (config/options/entity/exceptions/services), icons.json, exception translations, common-key reuse via [%key:...], device-class defaults, the script.translations develop loop. Use when writing or editing strings.json/icons.json, adding exception/entity translations, or wiring translation keys."
effort: medium
paths:
  - "homeassistant/components/*/strings.json"
  - "homeassistant/components/*/icons.json"
  - "custom_components/*/strings.json"
  - "custom_components/*/icons.json"
---

# Home Assistant Translations Reference

Reference for translating everything a Home Assistant integration shows a user.
`strings.json` is the source of truth: config flow, options, entities, exceptions, and
service actions all resolve their English text from it, and every other language is
generated from it downstream (Lokalise). `icons.json` maps entity/state/action keys to
Material Design Icons. Get the keys right here and the frontend, the app, and 90+
languages follow for free.

## Iron Laws — Never Violate These

1. **TRANSLATE EVERYTHING USER-FACING (P9)** — Every string a user can see is a
   translation key in `strings.json`; nothing is hardcoded in Python or in an
   `html\`\`` template. 7/7 core maintainers, DOC-BACKED (ADR-0009, i18n docs,
   `entity-translations`/`exception-translations`/`icon-translations` Gold). hassfest
   validates that keys exist and resolve.
2. **REUSE COMMON KEYS VIA `[%key:...]` REFERENCES (P9)** — Identical strings share one
   key; never copy the same English text under two keys. "As the string is the same, it
   means the same for the user, so why don't we use the same key?" — joostlek,
   https://github.com/home-assistant/core/pull/160263#discussion_r2987673952
3. **NEW KEY, NEVER MUTATE (P9 / F9 / FI-4)** — When meaning or placeholders change, add
   a *new* key; do not edit an existing en string in place. Wording-only iteration
   reuses the key. "putting the sentence in multiple parts, which is not ideal for
   translators" — silamon,
   https://github.com/home-assistant/frontend/pull/29104#discussion_r2734954889
4. **NO DASHES IN KEYS; ENUM OPTIONS ARE snake_case (P9)** — Keys and option values use
   `snake_case`, never `kebab-case`. "Translation keys shouldn't be using dashes.
   Instead it should be `passive_defrost`." — frenck,
   https://github.com/home-assistant/core/pull/156238#discussion_r2510038957
5. **COMPOSE TRANSLATOR-SAFE — WHOLE SENTENCES WITH PLACEHOLDERS (F9)** — Never
   concatenate fragments or interpolate an English word into a template; use `{name}`
   placeholders and ICU select so a translator can reorder the whole sentence. Enforced
   by silamon, piitaya, MindFreeze, bramkragten, wendevlin.
6. **FRONTEND STRINGS GO THROUGH `hass.localize` (F1)** — In ha-frontend, every visible
   string is a `hass.localize("...")` call with a key in `src/translations/en.json`;
   no literal English text nodes in `html\`\`` templates. "Translation is missing in
   en.json" — wendevlin,
   https://github.com/home-assistant/frontend/pull/22594#discussion_r1822479687

## Strong Defaults — Flag, Don't Block

1. **Prefer device-class defaults — OMIT the key (PS8 / P9 mechanics)** — A sensor with a
   built-in `device_class` already has a translated name and unit; adding an entity
   translation for it *duplicates* the framework default and is a finding. "prefer
   built-in device classes over custom translations" (sensor docs, strong-defaults.md
   PS8). The right action for a device-class entity is usually to delete the translation
   key, not write one.
2. **`data_description` for every new config/options field (PS15)** — the small helper
   text under a field label. A `data` label alone tells the user *what* the field is;
   `data_description` tells them *what to put there*. "Use `add_suggested_values_to_schema`
   … so the user doesn't need to fill in everything again" — emontnemery,
   https://github.com/home-assistant/core/pull/125595#discussion_r2321110457
3. **Inject the integration name via placeholders, never hardcode it (PS15)** — titles and
   descriptions take `{name}` from `description_placeholders`; a translated string never
   contains a literal brand name that a translator would have to preserve.

## strings.json Anatomy

The top-level keys are the translated surfaces of an integration. Full section-by-section
breakdown with worked examples: `${CLAUDE_SKILL_DIR}/references/strings-anatomy.md`.

| Section | Holds | Resolves for |
|---|---|---|
| `config` | `step.<id>.{title,description,data,data_description}`, `error.*`, `abort.*`, `flow_title` | Config flow (see `/ha:config-flow`) |
| `options` | Same shape as `config`, under `step` | Options flow |
| `config_subentries` | Per-subentry-type `step`/`error`/`abort` trees | Config subentries |
| `entity` | `<platform>.<translation_key>.{name, state, state_attributes}` | Entity names + ENUM/state text |
| `exceptions` | `<key>.message` with `{placeholders}` | Raised `HomeAssistantError` subclasses (P3) |
| `services` | `<service>.{name, description, fields.<f>.{name, description}}` | Service action UI |
| `selector` | `<key>.options.<value>` | Shared selector option labels |
| `common` | Reusable fragments referenced via `[%key:...]` | Everything above |

### Common-key reuse

```json
{
  "config": {
    "step": {
      "reauth_confirm": {
        "description": "[%key:component::example::config::step::user::description%]"
      }
    },
    "error": {
      "cannot_connect": "[%key:common::config_flow::error::cannot_connect%]",
      "invalid_auth": "[%key:common::config_flow::error::invalid_auth%]"
    }
  }
}
```

`[%key:common::...%]` points at the shared strings in `homeassistant/components/`
(the platform-wide `common` catalog); `[%key:component::<domain>::...%]` points within the
same integration. hassfest resolves and validates every reference. If two of your own
strings are identical, promote one and reference it — do not duplicate (Law 2).

### Exception translations (P3)

Exceptions carry a `translation_domain` + `translation_key`; the human text lives under
`exceptions.<key>.message`, never in the Python `raise`:

```python
raise ServiceValidationError(
    translation_domain=DOMAIN,
    translation_key="invalid_temperature",
    translation_placeholders={"value": str(value)},
)
```

```json
{
  "exceptions": {
    "invalid_temperature": {
      "message": "The temperature {value} is outside the allowed range."
    }
  }
}
```

The message string obeys F9: a whole sentence with `{value}` placeholders, never
`"The temperature " + value + " is..."`. See `/ha:service-actions` for where these are
raised.

## icons.json

`icons.json` translates keys → MDI icons, mirroring the `entity` and `services` trees:

```json
{
  "entity": {
    "sensor": {
      "power_state": {
        "default": "mdi:power",
        "state": { "charging": "mdi:battery-charging" }
      }
    }
  },
  "services": {
    "reboot": { "service": "mdi:restart" }
  }
}
```

- `default` is the base icon; `state` overrides per state value (keys are the same
  snake_case ENUM options as in `strings.json`).
- A built-in `device_class` supplies its own icon — omit the key rather than restating
  the framework default (Strong Default 1).
- `icon-translations` is a Gold quality-scale rule; run hassfest to validate.

## The Translation Dev Loop

`strings.json` is the *source*; the frontend and tests read the *generated*
`translations/en.json`. After any edit you must regenerate:

```bash
ruff format .
python3 -m script.hassfest --domain <domain>      # validates strings.json + icons.json + [%key:%] refs
python3 -m script.translations develop            # generate translations/en.json locally
pytest tests/components/<domain>/                  # tests resolve the generated strings
```

`script.translations develop` is the loop that surfaces missing/broken keys before CI
does. Never hand-edit `translations/en.json` — it is generated; edit `strings.json` and
regenerate.

## User-Copy Quality (Socratic — never a hard rule, §D-2)

String *quality* is judgment, not a mechanical law (strong-defaults.md §D "would my mom
understand it?" → rejected to this skill). Coach with questions; do not block:

- "Read the field label and its `data_description` cold — would someone who has never
  seen this device know what to type?"
- "Does this error tell the user what to *do*, or only that something broke?"
- "Is there jargon here (endpoint, token, MAC, polling) that a non-technical user
  wouldn't recognize? What would you call it at the kitchen table?"
- "Could a translator render this in another language without knowing your device — or
  does it lean on an English idiom?"

These are prompts, not gates. The mechanical laws above (P9/F9) are what the judge
enforces; copy quality is what review conversation improves.

## Common Anti-patterns

| Wrong | Right |
|---|---|
| `raise HomeAssistantError("Cannot connect")` | `translation_domain` + `translation_key` + `exceptions.*.message` (P3) |
| Same English text under two keys | promote one, reference via `[%key:...]` (P9) |
| Editing an existing `en` string's value in a diff | add a new key (P9 / FI-4) |
| `"cool-mode"` / `"Passive-Defrost"` option value | `"cool_mode"` / `"passive_defrost"` (P9) |
| `f"Set up {DOMAIN}"` label in Python | translated `config.step.user.title` with `{name}` placeholder |
| Entity translation for a `device_class` sensor | omit the key — use the device-class default (PS8) |
| `localize("ui.x") + " " + name` in a Lit template | one key with a `{name}` placeholder (F9) |

## Framework-Development Note (audience: framework-development)

Working in the `home-assistant/frontend` repo itself, the Lokalise pipeline mechanics
apply (FI-4, framework-dev-laws.md): a meaning/param change means a **new** key —
Lokalise keeps serving the old one as *unverified* until translators update it; a
wording-only iteration reuses the key. Contributors only ever *remove* a retired key
from `en.json`; maintainers delete it in Lokalise. This note does not apply to
integration authoring (source: review-patterns-frontend-internals.md §FI-4).

## References

- `${CLAUDE_SKILL_DIR}/references/strings-anatomy.md` - Every strings.json section with worked examples, placeholders, and the config-flow wiring
