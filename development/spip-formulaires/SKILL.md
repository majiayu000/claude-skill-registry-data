---
name: spip-formulaires
description: Use when creating, reviewing, or debugging SPIP CVT forms — canonical HTML
  wrappers, field/global errors, `charger`/`verifier`/`traiter`/`identifier`, or when
  deciding whether Saisies or Verifier are appropriate. Written for SPIP 4.x; on a SPIP 5.0 project
  the request API changes (see the SPIP 5.0 section).
---

# SPIP CVT forms

A **formulaire CVT** is a SPIP form built around the PHP contract
`charger` / `verifier` / `traiter`, with an optional `identifier`.

## SPIP 5.0

This skill describes SPIP 4.x. Check the version first and name the marker you relied on. A site is 5.0 if **any**
of: `ecrire/src/SpipVersion.php` declares `VERSION = '5.…'`, `bin/spip` exists, `vendor/spip/framework/` exists,
plugins live in `plugins-dist/spip/`. A plugin targets 5.0 if its `paquet.xml` `compatibilite` starts at 5.0 or
its `composer.json` requires `spip/framework`.

- Code for 5.0 only, in `charger` / `verifier` / `traiter` as everywhere: `_request('x')` → `Spip::input('x')`,
  `set_request('x', $v)` → `Spip::setInput('x', $v)`. Both old functions are deprecated in 5.0, including in the
  examples of this skill's references. `Spip` is a global alias of `Spip\Framework\Spip`: no `use` needed.
  One difference: on a site whose charset is not UTF-8, `_request()` converts UTF-8 values of an AJAX request to the
  site charset (`importer_charset()`), `Spip::input()` does not. Migrating such a site: convert where needed.
- `spip_sanitize_from_request($env, '*')` (whole environment) is removed → `spip_sanitize_env_from_request($env)`,
  which also exists in 4.4. The single-value form `spip_sanitize_from_request($value, 'key')` stays.
- `autosave_clean_value()` is deprecated → `Spip\Pipeline\Listener\CvtAutoSaveListener::cleanValue()`.
- Plugin for 4.4 **and** 5.0 (`compatibilite` from 4.x to `5.*`): keep `_request()` / `set_request()`, the only API
  in both.

Details: `spip-migration-5` (`references/catalogue.md`, `references/double-compat.md`).

## Quick routing

| Goal | Read |
|---|---|
| Build or review a standard SPIP form template | `references/form-structure.md` |
| Render global messages and field-level errors correctly | `references/form-structure.md` |
| Implement `charger()`, `verifier()`, `traiter()`, or `identifier()` | `references/cvt-formulaires.md` |
| Check `charger()` return values (`array`, `false`, `string`) and result keys | `references/cvt-formulaires.md` |
| Decide whether Saisies is worth introducing | `references/form-structure.md` + `references/plugin-saisies.md` |
| Use the recommended Saisies method | `references/plugin-saisies.md` |
| Pick a Saisies field type, or look up its options | `spip-saisies` |
| Write a custom field type, or hook a `saisies_*` pipeline | `spip-saisies` |
| Add reusable validation or normalisation rules | `references/plugin-verifier.md` |
| Review an existing form mixing template and PHP issues | `references/form-structure.md` + `references/cvt-formulaires.md` |

## Guardrails

- Start with the plain SPIP structure and the base CVT contract before adding plugin
  dependencies.
- Canonical HTML uses `formulaire_spip`, `.editer-groupe`, `.editer`,
  `reponse_formulaire`, `.erreur_message`, and `.boutons`.
- Global banners use `#ENV*{message_ok}` / `#ENV*{message_erreur}` with
  `role="status"` / `role="alert"`.
- Field errors use `#ENV*{erreurs/champ}` (single `*`, never `**`) and the conditional
  class `[ (#ENV*{erreurs/champ}|oui)erreur]`; field values use plain `#ENV{champ}`.
- `#ACTION_FORMULAIRE` is called without argument; the `<form>` is wrapped in
  `[(#ENV{editable}|oui) … ]`.
- `charger()` may return an `array`, `false`, or a `string`; `verifier()` returns an
  errors array; `traiter()` returns a result array.
- Use Saisies when the form is field-driven enough to justify the dependency. Preferred
  method: declare fields in `formulaires_<nom>_saisies()` and leave the HTML file empty.
- Treat `#GENERER_SAISIES` as the rare custom-markup exception, not the default.
- Use Verifier for reusable format/range/normalisation rules, not for tiny obvious checks
  that plain CVT handles clearly.

## Minimal template pattern

```html
<div class="formulaire_spip formulaire_editer formulaire_editer_x formulaire_editer_x-#ENV{id_x,nouveau}">
  [<div class="reponse_formulaire reponse_formulaire_ok" role="status">(#ENV*{message_ok})</div>]
  [<div class="reponse_formulaire reponse_formulaire_erreur" role="alert">(#ENV*{message_erreur})</div>]
  [(#ENV{editable}|oui)
  <form method='post' action='#ENV{action}'><div>
    #ACTION_FORMULAIRE
    <div class="editer-groupe">
      <div class="editer editer_titre obligatoire[ (#ENV*{erreurs/titre}|oui)erreur]">
        <label for="titre"><:info_titre:></label>
        [<span class='erreur_message'>(#ENV*{erreurs/titre})</span>]
        <input type='text' class='text' name='titre' id='titre' value="[(#ENV{titre})]">
      </div>
    </div>
    <!--extra-->
    <p class='boutons'><input type='submit' class='btn submit' value='<:bouton_enregistrer:>'></p>
  </div></form>
  ]
</div>
```

## Scope boundary

For broader plugin architecture, SQL API, pipelines, or `paquet.xml` work, use
`spip-plugins`. For the Saisies plugin beyond its use in a CVT form — field types and their
options, writing a custom type, `saisies_*` pipelines, the `inc/saisies*` API — use
`spip-saisies`.
