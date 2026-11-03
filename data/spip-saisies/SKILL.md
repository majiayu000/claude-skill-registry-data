---
name: spip-saisies
description: Use when working with the SPIP Saisies plugin — declaring fields in
  `formulaires_<nom>_saisies()`, writing a custom field type in `saisies/` or
  `saisies-vues/`, using `#SAISIE` / `#GENERER_SAISIES` / `#VOIR_SAISIES`, hooking a
  `saisies_*` pipeline, or manipulating a field array with the `inc/saisies*` PHP API.
---

# SPIP Saisies plugin

**Saisies** describes form fields as a PHP array and generates the markup, the error handling,
the conditional display and the multi-step logic from that description. Written against
**Saisies 6.3.4**; `UPGRADE_5.0.md` and `UPGRADE_6.0.md` in the plugin sources list the
breaking changes from earlier majors.

## Quick routing

| Goal                                                                           | Read                           |
|--------------------------------------------------------------------------------|--------------------------------|
| Find which field type to use, and its options                                  | `references/saisie-types.md`   |
| Look up options shared by every type (`obligatoire`, `afficher_si`, `class`…)  | `references/saisie-types.md`   |
| Write a new field type (`saisies/mon_type.html` + `.yaml` + `.php`)            | `references/custom-saisies.md` |
| Make a type configurable in the form builder, or inherit from an existing type | `references/custom-saisies.md` |
| Add a read-only view of a field                                                | `references/custom-saisies.md` |
| Hook into Saisies from another plugin                                          | `references/pipelines.md`      |
| Add, remove, move or rewrite fields in an existing field array                 | `references/api-php.md`        |
| Read a posted value, including files                                           | `references/api-php.md`        |
| Declare the fields of a CVT form and its `verifier` contract                   | `spip-formulaires`             |

## The one command that beats guessing

The plugin **generates its own exhaustive reference** from the type definitions it ships:
private area → *Development* → *Documentation des saisies* (`ecrire/?exec=saisies_doc`). Every
type, every option, every default, always in sync with the installed version. Read
`saisies/<type>.yaml` in the plugin sources for the same data as a file.

Never invent an option name — check one of those two.

## Guardrails

- A field is `['saisie' => 'type', 'options' => ['nom' => …], 'verifier' => …]`. `options.nom`
  is mandatory on every real field.
- Field types live in `saisies/<type>.html`. The `.yaml` sibling is what makes a type appear in
  the form builder — without it the type still works when declared in PHP.
- `saisies_lister_disponibles()` and the whole builder need the **yaml** plugin (`<utilise>`,
  not `<necessite>`): guard the code that calls it.
- `verifier()` runs **before** the declarative verifications, so it sees raw values; put
  cross-field checks that need normalised values in
  `formulaires_<nom>_verifier_post_saisies()`, which runs after them.
- Never rebuild a field array by hand when `saisies_inserer()`, `saisies_modifier()` or
  `saisies_supprimer()` does it: they walk nested fieldsets, which manual array code forgets.
- Read posted values with `saisies_request()`, not `_request()`, when the form has steps or
  nested names.

## Scope boundary

For the CVT contract itself (`charger` / `verifier` / `traiter`, template wrappers, error
markup), use `spip-formulaires`. For plugin architecture, `paquet.xml` and the SQL API, use
`spip-plugins`.
