---
name: spip-lang
description: Use for SPIP translation/i18n work — creating, editing, or auditing language files
  (lang/prefix_XX.php, lang/paquet-prefix_XX.php), naming keys, adding translations,
  using _T() / <:module:key:>, or debugging missing/untranslated strings. Written for SPIP 4.x;
  on a SPIP 5.0 project the _T() options change (see the SPIP 5.0 section).
---

# SPIP language files

SPIP stores translatable strings in PHP files under `lang/`. Each plugin declares its
language module in `paquet.xml`; the reference language is defined by `<traduire reference="…">` (typically `fr`).

## SPIP 5.0

This skill describes SPIP 4.x. Check the version first and name the marker you relied on. A site is 5.0 if **any**
of: `ecrire/src/SpipVersion.php` declares `VERSION = '5.…'`, `bin/spip` exists, `vendor/spip/framework/` exists,
plugins live in `plugins-dist/spip/`. A plugin targets 5.0 if its `paquet.xml` `compatibilite` starts at 5.0 or
its `composer.json` requires `spip/framework`.

- The 3rd argument of `_T()` and `_L()` is typed `array` in 5.0: the old string form `_T($k, $args, 'css_class')`
  throws a `TypeError`. Write `['class' => 'css_class']` (already valid in 4.4) or drop it, in every file you touch,
  even on lines you were not asked to change.
- One call in another language: `_T($k, ['spip_lang' => 'en'])` is deprecated → `_T($k, [], ['lang' => 'en'])`.
  4.4's `_T()` silently **ignores** the `lang` option: code for 4.4 **and** 5.0 uses `lang_select('en')` …
  `lang_select()` (both versions) or keeps `spip_lang`.
- Unchanged: language files, `<traduire>`, `lang_select()`. In squelettes, `<:module:key:>` is case-sensitive: keep
  the lowercase keys this skill requires.

Details: `spip-migration-5` (`references/catalogue.md`).

---

## Quick routing

| Goal | Read |
|---|---|
| Create or edit a `lang/prefix_fr.php` file | `references/format.md` |
| Add a new translation file (`lang/prefix_XX.php`) | `references/format.md` |
| Name keys consistently (prefixes, plural forms, placeholders) | `references/conventions.md` |
| Use `_T()` in PHP or `<:module:key:>` in a squelette | `references/usage.md` |
| Apply filters on a translated string (`\|label_nettoyer`, `\|attribut_html`) | `references/usage.md` |
| Singular / plural in a squelette (`singulier_ou_pluriel`) | `references/usage.md` |
| Debug missing or untranslated output (silent fallback to raw key, `var_mode=traduction`) | `references/usage.md` + `references/conventions.md` |
| Declare the module in `paquet.xml` | `../spip-plugins/references/i18n.md` |
| Send translated output in a different language (`lang_select`) | `references/usage.md` |

---

## File overview

```
monplugin/
└── lang/
    ├── monplugin_fr.php          ← main strings (reference)
    ├── monplugin_en.php          ← translation (same keys)
    └── paquet-monplugin_fr.php   ← plugin manager metadata
```

`paquet.xml` declaration:
```xml
<traduire module="monplugin" reference="fr" />
```

---

## Minimal file skeleton

```php
<?php
// This is a SPIP language file  --  Ceci est un fichier langue de SPIP
return [
    // A
    'aucun_objet'          => 'Aucun objet trouvé',

    // B
    'bouton_ajouter'       => 'Ajouter',

    // E
    'erreur_champ_vide'    => 'Le champ @champ@ est obligatoire',

    // I
    'info_1_objet'         => 'Un objet',
    'info_nb_objets'       => '@nb@ objets',

    // T
    'titre_objets'         => 'Mes objets',
];
```

Key rules:
- Keep alphabetical section comments (`// A`, `// B`…)
- Lowercase `snake_case`
- Variable placeholders must use `@nom@`
- Save files as UTF-8 (without BOM)

---

## paquet-module

```php
// lang/paquet-monplugin_fr.php
return [
    'monplugin_description' => 'Description affichée dans le gestionnaire de plugins',
    'monplugin_slogan'      => 'Accroche courte',
];
```

These two keys are **mandatory**. Module in `_T()` calls: `paquet-monplugin:` (not `monplugin:`).

---

## Scope boundary

For plugin architecture, pipelines, or full `paquet.xml` structure, route to `spip-plugins`.
For language files and translation usage, stay in this skill.

---

## Source of truth

- SPIP core lang files: `ecrire/lang/` and `plugins-dist/*/lang/`
- Detailed conventions: `references/conventions.md`
- PHP and squelette usage: `references/usage.md`
- File format details: `references/format.md`
