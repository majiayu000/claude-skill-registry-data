---
name: spip-plugins
description: Use when developing a SPIP plugin (paquet.xml present, _pipelines.php,
  spip_* table references in PHP) or when the user asks about plugin architecture,
  pipelines, hooks, or the SPIP PHP/SQL API. Written for SPIP 4.1–4.4; on a SPIP 5.0 project
  settings storage and the plugin model change (see the SPIP 5.0 section). Not for
  template/squelettes work — use the spip-squelettes skill for that.
---

# SPIP plugin development

## SPIP 5.0

This skill describes SPIP 4.x. Check the version first and name the marker you relied on. A site is 5.0 if **any**
of: `ecrire/src/SpipVersion.php` declares `VERSION = '5.…'`, `bin/spip` exists, `vendor/spip/framework/` exists,
plugins live in `plugins-dist/spip/`. A plugin targets 5.0 if its `paquet.xml` `compatibilite` reaches 5.x or
its `composer.json` requires `spip/framework`.

- Never read settings from `$GLOBALS['meta']` in code that runs on 5.0: it is a raw mirror of the SQL string, and
  arrays are stored as JSON once rewritten (one save of a `configurer_` form is enough).
  `unserialize($GLOBALS['meta']['acme'])` then returns `false` and the feature silently disappears. Read with
  `lire_config('acme/cle')` (4.4 and 5.0, not deprecated). Fix every such read in the files you touch, including an
  existing helper you reuse.
- Unchanged in 5.0: `<pipeline>` and `<genie>` in `paquet.xml`, `prefixe_pipeline()` functions, `affichage_final`,
  `$GLOBALS['html']`. Plugin for 4.4 **and** 5.0: keep this model only. The 5.0-only model (listeners,
  `config/services.php`, `#[AsCronTask]`) is in `spip5-plugins`; never register one pipeline both ways.
- `compatibilite` must accept the site's exact version: on `5.0.0-beta`, `[5.0.0;5.*]` refuses the plugin. Write
  `[5.0.0-dev;5.*]` (5.0 only) or `[4.4.0;5.*]`.

Details: `spip-migration-5` (`references/config-metas.md`, `references/double-compat.md`,
`references/plugin-modele-5.md`).

## SPIP-specific terms (always kept in original form)

| Term | Meaning |
|---|---|
| **boucle** | `<BOUCLE_xxx(TABLE){critères}>...</BOUCLE_xxx>` — template loop |
| **squelette** | Template file (`.html` with SPIP syntax) |
| **rubrique** | Hierarchical content section (SPIP's primary tree node) |
| **paquet.xml** | Plugin manifest — declares metadata, dependencies, pipelines, menus |
| **pipeline** | Extension hook — a named chain of functions called in sequence |
| **balise** | `#TAG` — template marker compiled to PHP |
| **critère** | `{criteria}` inside a boucle — constrains the SQL query |
| **filtre** | `\|function` — post-processor applied to a value in a squelette |
| **formulaire CVT** | Charger/Vérifier/Traiter — SPIP's form pattern (load/validate/process) |
| **objet éditorial** | First-class content type with CRUD, i18n, revisions (article, rubrique…) |
| **genie** | SPIP scheduled task (cron), declared via `<genie>` in paquet.xml |
| **action** | Secured script entry point (`?action=nom&arg=...&hash=...`) |
| **exec** | Private-space page handler (`?exec=nom`) |
| **inc** | Helper function file, lazy-loaded via `charger_fonction('nom', 'inc')` |
| **prefix** | Short plugin identifier — prefixes all PHP filenames and function names |

---

## Quick-start: minimal plugin skeleton

A SPIP plugin needs at minimum these files:

```
monplugin/
├── paquet.xml
├── monplugin_pipelines.php   ← pipeline handlers
└── lang/
    └── monplugin_fr.php      ← reference language strings
```

**paquet.xml** (no schema, no DB):
```xml
<paquet
  prefix="monplugin"
  version="1.0.0"
  compatibilite="[4.2.0;4.*]"
  etat="dev"
  categorie="divers">

  <nom>Mon Plugin</nom>
  <auteur>Prénom Nom</auteur>
  <licence>GNU/GPL</licence>

  <pipeline nom="mon_pipeline" inclure="monplugin_pipelines.php" />

  <traduire module="monplugin" reference="fr" />
</paquet>
```

**paquet.xml** (with a database table):
```xml
<paquet prefix="monplugin" version="1.0.0" schema="1.0.0" ...>

  <nom>Mon Plugin</nom>

  <!-- declare pipeline handlers for table declarations -->
  <pipeline nom="declarer_tables_objets_sql" inclure="base/monplugin.php" />
  <pipeline nom="declarer_tables_interfaces"  inclure="base/monplugin.php" />
</paquet>
```

The `schema=` attribute alone activates installation/upgrade support. SPIP looks for
`{prefix}_administrations.php` at the plugin root **by naming convention** — it must
exist and contain `{prefix}_upgrade()` and `{prefix}_vider_tables()`. There is **no**
`<install>` tag in the `paquet.xml` DTD (it was removed when `plugin.xml` was deprecated).

**monplugin_pipelines.php**:
```php
<?php
if (!defined('_ECRIRE_INC_VERSION')) { return; }

function monplugin_mon_pipeline($flux) {
    // modify $flux['data'], return $flux
    return $flux;
}
```

---

## Decision tree — I want to…

| Goal | Read |
|---|---|
| Create a plugin manifest (`paquet.xml`) | `references/paquet-xml.md` |
| Understand the directory layout and file loading order | `references/arborescence.md` |
| Hook into SPIP events (content published, user logged in, etc.) | `references/pipelines.md` |
| Add a contact/subscription/edit form | `../spip-formulaires/references/cvt-formulaires.md` |
| Write a secured action script (`action/`) | `references/actions.md` |
| Check or grant permissions in PHP or squelettes | `references/autorisations.md` |
| Read or write database rows | `references/sql-api.md` |
| Create a new database table (not an objet éditorial) | `references/declarer-table.md` |
| Create a new objet éditorial (with statut, edition form, search) | `references/declarer-objet.md` |
| Create public object URLs / custom `#URL_*` tags | `references/urls-objets.md` |
| Define a custom `#BALISE`, `\|filtre`, or `{critère}` | `references/balises-filtres-criteres.md` |
| Add translated strings to a plugin | `references/i18n.md` |
| Write install/upgrade/uninstall logic (`_administrations.php`) | `references/cycle-de-vie.md` |
| Build or customise private-space templates (liste, infos, contenu, editer) | `references/prive-objets.md` |
| Understand what `?exec=mon_objets` / `?exec=mon_objet` provides out-of-the-box | `references/exec-generique.md` |
| Apply SPIP coding standards (SCS1) | `references/coding-standards.md` |
| Configure composer.json, ecs.php or rector.php | `references/coding-standards.md` |
| Control page cache duration, disable caching, or trigger invalidation | `references/cache.md` |
| Write PHPUnit tests for my plugin (filtres, autorisations, squelettes) | invoke the **spip-testing** skill |
| Support content in multiple languages (`lang`, `id_trad`, translation groups) | `references/multilinguisme.md` |
| Run work asynchronously (background jobs, scheduled tasks) | `references/queue-jobs.md` |
| Add chunked file upload (bigup) to a formulaire CVT | `references/upload-bigup.md` |
| Create a plugin configuration page and read/write settings | `references/config.md` |

---

## Workflow index

### Starting a new plugin

1. `references/paquet-xml.md` → write the manifest
2. `references/arborescence.md` → choose the right file for each function
3. `references/pipelines.md` → pick which pipeline(s) to plug into
4. `references/coding-standards.md` → configure composer.json, ecs.php or rector.php (optional but recommended)

### Adding a database table

1. `references/declarer-table.md` → declare schema via `declarer_tables_principales` or
   `declarer_tables_objets_sql`
2. `references/cycle-de-vie.md` → write `_administrations.php` with `maj_tables()`
3. `references/sql-api.md` → read/write the table at runtime

### Building a form

1. `../spip-formulaires/references/cvt-formulaires.md` → implement `charger`, `verifier`, `traiter`
2. `references/sql-api.md` → write data in `traiter()`
3. `references/pipelines.md` → `formulaire_charger` / `formulaire_verifier` / `formulaire_traiter`
   if you need to hook into other plugins' forms

### Creating an objet éditorial

1. `references/declarer-objet.md` → full `declarer_tables_objets_sql` descriptor
2. `references/declarer-table.md` → add `declarer_tables_interfaces` for compiler config
3. `references/cycle-de-vie.md` → install/uninstall the table
4. `../spip-formulaires/references/cvt-formulaires.md` → use `formulaires_editer_objet_charger/verifier/traiter()`
5. `references/pipelines.md` → `pre_edition`, `post_edition` to react to changes

### Creating public URLs for a custom object

1. `references/urls-objets.md` → `#URL_<TYPE>`, `declarer_url_objets`, routing expectations
2. `references/declarer-objet.md` → descriptor keys `type`, `page`, `titre`
3. `references/declarer-table.md` → `declarer_tables_interfaces` (`table_titre`) for meaningful URLs

### Extending squelettes

1. `references/balises-filtres-criteres.md` → add `#BALISE`, `|filtre`, or `{critère}`
2. `references/declarer-table.md` → `declarer_tables_interfaces` for `table_des_traitements`

### Adding secured actions

1. `references/actions.md` → write `action_nom_dist()`, use `securiser_action`, check `autoriser`
2. `references/autorisations.md` → define custom `autoriser_` functions

### Restricting access

1. `references/autorisations.md` → `autoriser()` API, lookup chain, writing `autoriser_X_Y_dist()`

### Building the private-space UI for an objet éditorial

1. `references/exec-generique.md` → what `?exec=mon_objets` / `?exec=mon_objet` provides for free
2. `references/prive-objets.md` → create `liste/`, `infos/`, `contenu/` fragments as needed

### Adding file upload to a form

1. `references/upload-bigup.md` → enable bigup via `_bigup_rechercher_fichiers` in `charger()`
2. `../spip-formulaires/references/cvt-formulaires.md` → `verifier()` and `traiter()` with `$_FILES`

### Running background work

1. `references/queue-jobs.md` → `queue_add_job()`, `spip_jobs`, priority, deduplication
2. `references/paquet-xml.md` → `<genie>` for periodic tasks

### Testing a plugin

→ invoke the **spip-testing** skill

### Supporting multiple languages in an objet

1. `references/multilinguisme.md` → `lang`, `id_trad`, `action_referencer_traduction_dist()`
2. `references/declarer-objet.md` → `titre` accessor must include `lang`

---

## Source of truth

All examples in this skill are extracted from the **SPIP 4.4.15** sources:
- SPIP core: `ecrire/`
- plugins-dist (the 20 reference plugins shipped with SPIP): `plugins-dist/`
- coding standards reference: `references/coding-standards.md`

Paths inside the references are given relative to the SPIP root,
e.g. `plugins-dist/forum/paquet.xml`.

When in doubt, read the source.
