---
name: spip-squelettes
description: Use for any SPIP template question — BOUCLE loops, balises, critères,
  filtres, INCLURE, pagination, image filters, recursive trees, AJAX reloads. Covers
  public squelettes and plugin squelettes (espace privé, modèles). Trigger even when
  the user doesn't say "squelette". Not for PHP hooks/pipelines → use spip-plugins.
  Written for SPIP 4.x; on a SPIP 5.0 project some syntaxes are removed (see the SPIP 5.0 section).
---

# SPIP — Squelettes Reference

SPIP generates pages from **squelettes** — `.html` files mixing HTML with BOUCLE loops and `#BALISE` tags. All template work lives in `squelettes/`. No PHP needed.

## SPIP 5.0

This skill describes SPIP 4.x. Check the version first and name the marker you relied on. A site is 5.0 if **any**
of: `ecrire/src/SpipVersion.php` declares `VERSION = '5.…'`, `bin/spip` exists, `vendor/spip/framework/` exists,
plugins live in `plugins-dist/spip/`. A plugin targets 5.0 if its `paquet.xml` `compatibilite` starts at 5.0 or
its `composer.json` requires `spip/framework`. On a 5.0 project, fix these in every squelette you touch, not only in
the code you add:

- **Removed in 5.0**: `<INCLURE{…}></INCLURE>` → `<INCLURE{…} />`, and `.html` only (no `<INCLURE(x.php)>`, no
  `fond=x.php`); logo pseudo-filters `[(#LOGO_X|right)]` (`left`, `center`, `top`, `bottom`) → `[(#LOGO_X{right})]`,
  `|#URL_X` → `{#URL_X}`, `|fichier` → `#LOGO_X**`. The new forms already work in 4.4: use them on both.
- `{fusion}` / `{fusion_supprimer}` / `{collecte}` → `{groupby}` / `{groupby_supprimer}` / `{collate}` (deprecated
  in 5.0). The new names do not exist in 4.4: a squelette for 4.4 **and** 5.0 keeps the old ones.
- Also removed: `(POUR)` → `(DATA){source tableau, …}`, `|foreach` → a `DATA` loop, `#EMBED_DOCUMENT` →
  `#MODELE{emb, …}`, `#LARGEUR_ECRAN` → `#LAYOUT_PRIVE{…}`, `#CONST{_DIR_RESTREINT_ABS}` →
  `#PARAM{spip.routes.back_office}`.
- Brackets are now allowed in optional parts: in CSS, `a[href] { … url(#CHEMIN_IMAGE{x.svg}) }` can be read as one →
  `url("#CHEMIN_IMAGE{x.svg}")`.
- Language items are case-sensitive: `<:Acme:Titre:>` ≠ `<:acme:titre:>`.

Details: `spip-migration-5` (`references/squelettes.md`).

---

## SPIP-specific terms (always kept in original form)

| Term | Meaning |
|---|---|
| **source of data** | iterable data provider (e.g., SQL query result, array, csv file) |
| **boucle** | `<BOUCLE_xxx(TABLE){critères}>...</BOUCLE_xxx>` — data extractor and content generator (includes pre/post sections and zero-result alternative) |
| **squelette** | Template file (`.html` with SPIP syntax) |
| **paquet.xml** | Code manifest — declares metadata, dependencies |
| **balise** | `#TAG` — template marker compiled to PHP |
| **critère** | `{criteria}` inside a boucle — constrains the SQL query |
| **filtre** | `\|function` — post-processor applied to a value in a squelette |
| **formulaire CVT** | Charger/Vérifier/Traiter — SPIP's form pattern (load/validate/process) |
| **objet éditorial** | First-class content type with CRUD, i18n, revisions (article, rubrique…) |

## Complete BOUCLE Syntax

```html
<BB_name>
<!-- optional header section: always displayed -->
<B_name>
<!-- optional pre-section: output once before body, only if ≥1 result -->
<BOUCLE_name(TABLE){critère1}{critère2}>
  <!-- Content repeated for each result row -->
</BOUCLE_name>
<!-- optional post-section: output once after body, only if ≥1 result -->
</B_name>
<!-- optional zero-result alternative: output when loop returns nothing -->
<//B_name>
<!-- optional footer section: always displayed -->
</BB_name>
```

**Example — 10 articles, newest first, paginated:**

```html
<B_arts>
<ul>
<BOUCLE_arts(ARTICLES){id_rubrique}{par date}{inverse}{pagination 10}>
  <li><a href="#URL_ARTICLE">#TITRE</a> — [(#DATE|affdate_court)]</li>
</BOUCLE_arts>
</ul>
</B_arts>
<p>No article.</p>
<//B_arts>
```

**Nested loop — context inheritance:**

```html
<BOUCLE_rubs(RUBRIQUES){racine}{par titre}>
  <h2>#TITRE</h2>
  <!-- {id_rubrique} refers to the current row of the outer loop -->
  <BOUCLE_arts(ARTICLES){id_rubrique}{par date}{inverse}{limit 5}>
    <a href="#URL_ARTICLE">#TITRE</a>
  </BOUCLE_arts>
</BOUCLE_rubs>
```

## #BALISE Syntax

| Form | Meaning |
|------|---------|
| `#TITRE` | Outputs value; empty string if absent |
| `[(#TITRE)]` | Outputs nothing if empty (suppresses wrapper too) |
| `[before(#TITRE)after]` | Wraps value with before/after only if not empty |
| `[(#TITRE\|filtre1\|filtre2)]` | Chains filters; optional wrapper |

## Key Critères

| Critère | Effect |
|---------|--------|
| `{id_rubrique}` | Items in current rubrique (inherited from outer loop or URL) |
| `{id_rubrique=3}` | Items in rubrique #3 |
| `{par date}{inverse}` | Newest first |
| `{par titre}` | Alphabetical |
| `{limit 5}` | Max 5 results |
| `{pagination 10}` | 10 per page; add `[(#PAGINATION)]` for links |
| `{statut=publie}` | Published items only |
| `{doublons}` | Skip items already stored in an earlier doublon on this page |
| `{branche}` | Current rubrique and all its sub-rubriques |
| `{lang}` | Current language only |

## Key Balises

| Balise | Description |
|--------|-------------|
| `#TITRE` | Title |
| `#TEXTE` | Body (shortcodes processed) |
| `#URL_ARTICLE` / `#URL_RUBRIQUE` | Permalink |
| `#DATE` | Publication date |
| `#LOGO_ARTICLE` | Article logo `<img>` tag (empty if none) |
| `#LOGO_ARTICLE_RUBRIQUE` | Article logo with automatic rubrique fallback |
| `#ENV{key}` | URL param or INCLURE argument |
| `#PAGINATION` | Page nav links (requires `{pagination N}`) |
| `#CACHE{3600}` | Cache this page for N seconds |
| `#FILTRE{f1\|f2}` | Apply filters to the full rendered squelette |

## Load on Demand

- All native loop types, recursive loops → `references/boucles.md`
- Full critères + balises catalog → `references/balises.md` and `references/criteres.md`
- Filter signatures with examples → `references/filtres.md`
- INCLURE composition, file resolution, AJAX partial reload → `references/inclure-ajax.md`
- #ENV, #SET/#GET, #SESSION_SET/#SESSION → `references/variables.md`
- Modèles (`#MODELE`, raccourcis éditoriaux, `modeles/`) → `references/modeles.md`
- Native formulaires, #CACHE, 404, page variants → `references/avance.md`
- Copy-paste complete patterns → `references/exemples.md`

Not for plugin PHP development → use the `spip-plugins` skill.
Not for PHPUnit tests on squelettes or `#BALISE` → use the `spip-testing` skill.
