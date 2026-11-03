---
name: plugin-escal
description: Use when working on a SPIP site that uses the Escal squelette — installing or activating it, placing or configuring its noisettes (blocs latéraux, onglets « À la une »), reading or writing its escal/config settings, using its special pages (agenda, contact, recherche, annuaire, trombinoscope, forum de site, mots-clés, auteur, 404), choosing a layout, using its technical mots-clés, or restyling it without forking. Written for SPIP 4.x; Escal does not run on SPIP 5.0 (see the SPIP 5.0 section).
---

# Escal (squelette SPIP)

## Overview

Escal is a **jeu de squelettes** (full theme) for SPIP, prefix `escal`, category `squelette`.
Current release read here: **5.6.2** (`de508fb`, 2026-10-15), schema `1.0.17`, GNU/GPL, compatible `[4.1.0;4.*]`.
Author: Jean-Christophe Villeneuve. Docs: <https://contrib.spip.net/Escal-4077>.

**The one thing to understand:** Escal is a *composition engine driven by one meta*.
A single SPIP meta named `escal`, casier `escal/config`, decides both

1. **which block goes where** — every slot in every page is an `<INCLURE>` whose *fond name* is read from the meta, and
2. **what the site looks like** — six stylesheets are SPIP squelettes (`*.css.html`, `#CACHE{0}`) recompiled per request with `#CONFIG` values injected.

```spip
[(#CONFIG{escal/config/blocnav3}|=={rien}|non)
  <div class="cadre-couleur">
    <INCLURE {fond=inclusions/inc-#CONFIG{escal/config/blocnav3,edito}}{env}{ajax}>
  </div>
]
```

Nothing about the composition is hard-coded in the page squelettes. Changing a setting changes which file gets included.

## SPIP 5.0

This skill describes SPIP 4.x. Check the site's version first and name the marker you relied on. A site is 5.0 if
**any** of: `ecrire/src/SpipVersion.php` declares `VERSION = '5.…'`, `bin/spip` exists, `vendor/spip/framework/`
exists, plugins live in `plugins-dist/spip/`.

- Escal does not run on 5.0: its latest release (5.6.2, 2026-10-15) declares `compatibilite="[4.1.0;4.*]"`, which
  SPIP 5.0 refuses, so it is never activated (a site upgraded to 5.0 falls back to the default squelettes; the
  `escal` meta stays in base). Read the `paquet.xml` of the release at hand before any advice. Never force it
  (editing `compatibilite`, `_DEV_VERSION_SPIP_COMPAT`). The options: keep the site on 4.4, wait for a release whose
  `compatibilite` reaches 5.x, or choose another squelette.
- Going back to 4.4 means restoring the pre-migration backup, files **and** database. Never offer to reinstall 4.4
  over the migrated database: 5.0 rewrites array settings as JSON, which 4.4 (`unserialize`) does not decode, so the
  Escal settings would not come back. Without that backup, say there is no verified way back with the settings.
- The spip-cli recipes below do not apply to a 5.0 site: spip-cli is a 4.x tool, and 5.0's `bin/spip` has no
  download, activation or `php:eval` command. The commands useful here: `config:lire` / `config:ecrire` and
  `spip:cache:clear`.
  `bin/spip config:lire escal --json` shows the kept settings. Its JSON is pretty-printed (`"cle": null`): to test
  whether Escal was ever installed, read the one key `escal_base_version` and match `grep -Eq '": ?null'` (not
  `':null}'`). Never run that test on the whole `escal` meta, where any `null` setting would match.

Details: `spip-migration-5` (`references/audit-outils.md`: `bin/spip` commands); 4.4 → 5.0 upgrade and rollback of
the site: `spip5-instance` (`references/upgrade-4-4.md`).

## Vocabulary traps — verify before answering

These are the things agents reliably get wrong about Escal. Every row was an actual hallucination in baseline testing.

| Wrong (do not say) | Correct |
|---|---|
| `noisettes/noisette_*.html` | Noisettes live in **`inclusions/inc-*.html`**. There is no `noisettes/` directory. |
| `spip plugin:install escal` | spip-cli uses **`plugins:svp:telecharger`** then **`plugins:activer`**. There is no `plugin:install`. |
| Meta is `config_escal` | Meta is **`escal`**; settings sit in casier **`escal/config`**; read with `#CONFIG{escal/config/‹cle›}` or `lire_config('escal/config/‹cle›')`. |
| `bloc_gauche_2`, `bloc_droite_1` | Slot keys are **`blocnav‹n›`** (colonne navigation) and **`blocextra‹n›`** (colonne extra), with a page-family suffix: `blocnavart3`, `blocextrarub2`, `blocnavpages7`, `blocnavforumsite4`. |
| "`plugins:svp:telecharger` said it worked, so the plugin is there" | On **unpatched** spip-cli it prints successes while downloading nothing (MR !91). Always confirm with `plugins:lister --short`, never with the download command's own output. |
| Escal has a "paste your CSS here" field | It does not. Surcharge via **`squelettes/styles/perso.css`** and **`squelettes/persoconfig.css.html`**. |
| "fluide/mixte change the column order" | Column order is the **letters** (`PMP`, `MPP`, `PPM`, `MP`, `PM`). `fixe`/`fluide`/`mixte` are **width modes**, orthogonal to order. |
| "`blocnav` = colonne de gauche" | **Not always.** `navigation`/`extra` are *slots*, not sides — which side they land on depends on the layout, and RTL swaps them. See the placement table below. |
| "Drop `inc-monbloc.html` in `squelettes/`, then type `monbloc` in a slot" | **No.** Every `bloc*` slot is a `<select>` with a hard-coded option list (`formulaires/configurer_escal_choix_blocs.php`). The webmestre *picks* a block; nothing scans the filesystem. To ship your own content use `perso` / `article_libre1…5`, or override a listed noisette's file. |
| Tab value = noisette filename | The `onglet‹n›` values are their own vocabulary: `derniersarticles` → `inc-une_derniers.html`, `rubrique2` → `inc-rubrique_accueil2.html`. See references/noisettes.md. |

**When unsure of an exact key or filename, read the plugin source rather than guessing.** The authoritative list of block values is the `'data'` arrays in `formulaires/configurer_escal_choix_blocs.php`.

## Install with spip-cli

Verified against **spip-cli 2.0.1** on SPIP 4.4.14. Run `spip list` if a command name looks off.

### ⚠ `plugins:svp:telecharger` is broken in stock spip-cli

Upstream 2.0.1 **cannot download a plugin at all**, and hides it:

- the depot lookup compares `UPPER(pl.prefixe)` to `LOWER("PREFIXE")` — never equal, so every plugin
  reports *« Le plugin xxx n'est pas référencé »*;
- past that, the `autoriser_exception` is registered under the wrong key and `action/teleporter.php`
  refuses the download;
- and `one_action()` returns the action description *before* running it, so failures were printed as
  successes.

Fixed by [MR !91](https://git.spip.net/spip-contrib-outils/spip-cli/-/merge_requests/91). Check the
local copy before trusting a download:

```bash
grep -q 'UPPER(pl.prefixe) = UPPER' src/Command/PluginsSvpTelecharger.php \
  && echo "patché (MR!91)" || echo "NON patché — les téléchargements échoueront en silence"
```

On an unpatched CLI, install the plugins by hand into `plugins/` (or via the private area) and use
spip-cli only for `plugins:activer`.

### Recette

Run from the SPIP root (the directory holding `config/connect.php`).

```bash
# 0. SVP unpacks into plugins/auto/ — core:preparer does NOT create it.
#    Without it every download fails with
#    « Le répertoire de paquets plugins/auto/ n'est pas accessible en écriture ».
mkdir -p plugins/auto && chmod u+rwx plugins/auto

# 1. register the official depot (once)
spip plugins:svp:depoter https://plugins.spip.net/depots/principal.xml

# 2. download Escal and its hard dependencies
spip plugins:svp:telecharger saisies verifier yaml agenda fullcalendarcompat \
     svpstats nospam facteur tri_par_rubrique aide escal -y

# 3. activate, dependencies first
spip plugins:activer saisies verifier yaml agenda fullcalendarcompat \
     svpstats nospam facteur tri_par_rubrique aide escal -y

# 4. run the plugin upgrades, then check
spip plugins:maj:bdd                 # prints « Installation du plugin Escal … MAJ 1.0.17 »
spip plugins:lister --short          # every prefix above must appear
spip cache:vider
```

SVP unpacks one directory per version: `plugins/auto/escal/v5.6.2/`, not `plugins/auto/escal/`.
Step 2 also pulls **`calendriermini`** as a transitive dependency — expect 11 packages, not 10.

### ⚠ After a CLI install, the starter contents stay unpublished

`escal_upgrade()` creates a hidden rubrique plus three articles — *Édito*, *Accès direct*,
*Mentions légales* — already tagged, and asks for `statut = publie`. From the private area that
works. **From spip-cli it does not:** there is no authenticated author, `autoriser('publierdans', …)`
returns false, and the three articles are left in `prepa`. The Édito and Accès direct blocks then
render empty and the site looks broken. Publish them by giving the CLI a session:

```bash
spip php:eval 'include_spip("action/editer_objet"); include_spip("base/abstract_sql");
$GLOBALS["visiteur_session"] = sql_fetsel("*", "spip_auteurs", "statut=" . sql_quote("0minirezo"));
$GLOBALS["visiteur_session"]["webmestre"] = "oui";
foreach (sql_allfetsel("id_article", "spip_articles", "statut=" . sql_quote("prepa")) as $x) {
  objet_instituer("article", $x["id_article"], ["statut" => "publie"]);
}'
```

Note the `sql_quote()`: the whole PHP program travels inside shell single quotes, so any nested
`\"` is mangled before PHP sees it. Build SQL string literals with `sql_quote()` rather than
escaping quotes — that is the form that actually runs.

Same limitation for anything scripted through `php:eval` that crosses an `autoriser()` check — set
the session first. `config:ecrire` is unaffected: it writes `spip_meta` directly.

### Notes

`plugins:activer` and `plugins:svp:telecharger` take prefixes as positional arguments, or
`--from-list=a,b,c`; `-y` skips the prompts. Activating `escal` runs `escal_upgrade()`, which creates
the two mots-clés groups and the starter contents — never hand-write the `escal` meta to "install" it.

Optional plugins Escal detects if present: `palette`, `spip_400`, `orr` (typographic shortcuts),
`Shoutbox`, `reservation_evenement`, `reservations_multiples`. Enable the matching noisettes in the
*Plugins* config screen.

## Reading and writing settings from the CLI

`config:lire` and `config:ecrire` operate on `spip_meta`, so they reach Escal's casier directly —
handy for scripted setup and for inspecting a site you cannot log into.

```bash
spip config:lire escal --json                     # dump the whole configuration
spip config:lire escal/config/blocnav2            # one setting
spip config:lire escal_base_version --json        # {"escal_base_version":null} ⇒ not installed

spip config:ecrire escal/config/blocnav2:derniers_articles     # full path as the option
spip config:ecrire -p escal config/blocnav2:derniers_articles  # same thing, -p prepends "escal/"
spip config:ecrire escal/config/nomsite --valeur 'Mon site'    # value containing ":" or spaces
```

The argument is split on the **first** colon only. A value that itself contains a colon (a URL, a
time) must go through `--valeur`.

Use `--json` whenever you test for absence. Plain `config:lire` always prints the key label, so its
output is never an empty string and `[ -z "$(spip config:lire escal_base_version)" ]` silently
passes even when the plugin has never been installed. Compare against `:null}` instead.

Several settings at once — note the nesting, `-p escal` plus a `config` sub-object rebuilds
`escal/config/…`:

```bash
spip config:ecrire -p escal --json '{"config":{"blocnav1":"edito","blocnav2":"derniers_articles","layout":"PMPfluide"}}'
spip cache:vider
```

Always `cache:vider` afterwards: the generated stylesheets are `#CACHE{0}` but the pages that include
them are not.

## Placing a noisette

Configuration UI: **espace privé → Squelettes → Escal** (webmestre only). Page `?exec=configurer_escal&cfg=choix_blocs`.

The slot key encodes column + page family + rank:

| Page family | Colonne navigation | Colonne extra | Centre |
|---|---|---|---|
| Sommaire | `blocnav1…10` | `blocextra1…10` | `blocune1…3` |
| Article | `blocnavart1…6` | `blocextraart1…6` | — |
| Rubrique | `blocnavrub1…6` | `blocextrarub1…6` | — |
| Autres pages | `blocnavpages1…10` | `blocextrapages1…10` | — |
| Forum de site | `blocnavforumsite1…10` | — | — |

The value is a **noisette short name** (no `inc-` prefix, no `.html`), or `rien` for an empty slot.
Example — *Derniers articles* in second position of the navigation column on the home page:

```php
ecrire_config('escal/config/blocnav2', 'derniers_articles');
// → renders inclusions/inc-derniers_articles.html
```

**Each slot is a closed dropdown.** The screen renders a Saisies `selection` per slot; its options are
hard-coded in the `'data'` arrays of `formulaires/configurer_escal_choix_blocs.php`. The webmestre
chooses among them — there is no free-text field, and adding a file to `squelettes/inclusions/` adds
nothing to the list. Option counts per dropdown (`rien` included) differ by family *and* by column:
sommaire 29 nav / 27 extra, article 22 / 20, rubrique 20 / 18, autres pages 21 / 19, forum de site 16.
The only values that differ between the two columns are `choixmenuV1` / `choixmenuV2`, offered in
`blocnav*` only.

`ecrire_config()` bypasses the form, so a value outside the list is stored as-is: it renders
`inclusions/inc-‹valeur›.html` if that file exists, an empty slot otherwise — and the next save of the
config screen drops it back to a listed value. Do not sell that as the way to add a block.

**Full catalogue, per-family availability, and the central « À la une » tabs: `references/noisettes.md`.**

## Layouts

Order is spelled by the letters, read left to right: **P** = narrow column, **M** = `main#contenu`.

- Orders: `PMP`, `MPP`, `PPM`, `MP`, `PM`
- Width modes: *fixe* (suffix none), *fluide*, *mixte* (side columns fixed, centre elastic)
- Mixte exists only for the 3-column orders → **13** `layout*.css.html` files

The 13 valid values of `escal/config/layout`, verbatim:

`PMP` `MPP` `PPM` `MP` `PM` · `PMPfluide` `MPPfluide` `PPMfluide` `MPfluide` `PMfluide` · `PMPmixte` `MPPmixte` `PPMmixte`

Widths: `largeurlayoutbase` + `colonnelayoutbase` (fixe), `largeurmaxlayoutfluide` (fluide), `colonnelayoutmixte` (mixte).

**Where each column actually lands** — `navigation` is not a synonym for "left":

| Ordre | Gauche → droite | Colonne la plus à gauche | Colonne la plus à droite |
|---|---|---|---|
| `PMP` | nav · contenu · extra | `blocnav*` | `blocextra*` |
| `PPM` | nav · extra · contenu | `blocnav*` | `blocextra*` (2ᵉ en partant de la gauche) |
| `PM` | nav · extra · contenu | `blocnav*` | `blocextra*` (2ᵉ en partant de la gauche) |
| `MPP` | contenu · nav · extra | `blocnav*` (mais à droite du contenu) | `blocextra*` |
| `MP` | contenu · nav · extra | `blocnav*` (mais à droite du contenu) | `blocextra*` |

`blocnav*` always precedes `blocextra*` in reading order; what changes between layouts is where the
pair sits relative to the content. In `MPP` and `MP` there is **no** column left of the content — a
request for "the left column" there needs a layout change (`PMP`, `PPM` or `PM`) first.

In RTL (`#LANG_DIR` = `rtl`) the two `<section>` elements are emitted in the reverse order, mirroring the whole thing. So "put this block in the left column" is only answerable once you know the site's layout — check `escal/config/layout` first.

The layout stylesheet is loaded with `media="screen and (min-width: 641px)"` — below that, `styles/mobile.css` stacks everything. `#ENV{layout}` overrides `#CONFIG`, so `?layout=MPfluide` previews without saving.

## Mots-clés techniques

Installation creates two groups: **`affichage`** (44 mots) and **`Agenda_couleur`** (5 mots, hex code or CSS colour in the *descriptif*). Squelettes test them with `{titre_mot=…}`.

Three roles — full list in `references/configuration.md`:

- **Reroute the squelette**: `pleinepage` on an article → `article_pleinepage.html`; `forum` on a secteur → `forumSite-*.html`; `trombino`, `popup`.
- **Designate content**: `edito`, `acces-direct`, `actus`, `annonce`, `citations`, `mentions-legales` — the noisette fetches the article carrying the mot.
- **Exclude from a listing**: `invisible`, `pas-au-menu`, `pas-a-la-une`, `pas-au-plan`, `site-exclu`.

Two further groups, **`type_article`** and **`type_rubrique`**, are **not created by the installer** — the webmestre creates them. Attach such a mot to a *rubrique* and Escal includes `inclusions/inc-article_‹mot›.html` / `inc-rubrique_‹mot›.html` when that file exists, falling back to `inc-article.html` / `inc-rubrique_normal.html`. This is the supported way to give a section its own gabarit.

To create one: espace privé → **Mots-clés** → *Créer un nouveau groupe de mots*, name it exactly
`type_rubrique` (or `type_article`), tick *Rubriques* (resp. *Articles*) in its `tables_liees`,
add a mot, then attach that mot to the rubrique.

**How the filename is derived:** the squelette does `#SET{type, #TITRE}` and includes
`inclusions/inc-article_#GET{type}.html` — no filter is applied, so the mot's **titre is used
verbatim**, with no slugifying, no lowercasing and no accent stripping. A mot titled `Recettes` looks
for `inc-article_Recettes.html`. The one file Escal ships for this mechanism is
`inc-rubrique_trombino.html`, so it needs a mot titled exactly `trombino`, lowercase. Give your own
mots short ASCII titles with no spaces, and name the file with the identical string. If the file is
missing, Escal silently falls back to `inc-article.html` / `inc-rubrique_normal.html` — a wrong case
looks exactly like "the feature doesn't work".

Do not read `inc-article_forumSite.html` / `inc-rubrique_forumSite.html` as examples of this
mechanism: they are included directly by `forumSite-article.html` and `forumSite-rubrique.html`,
which are reached through the `forum` mot on the secteur.

## Restyling without forking

SPIP resolves `squelettes/` before plugins, and both hooks load *after* every generated stylesheet.

| Goal | File to create |
|---|---|
| Plain CSS overrides | `squelettes/styles/perso.css` |
| CSS that reads `#CONFIG` | `squelettes/persoconfig.css.html` (ship-empty file exists for this) |
| Colour one section | `squelettes/styles/secteur‹ID_SECTEUR›.css` |
| Replace a block | `squelettes/inclusions/inc-‹nom›.html` |
| Add your own content to a lateral slot | Nothing new to name: use the listed `perso` (articles tagged `special`) or `article_libre1`…`5`, and override `squelettes/inclusions/inc-perso.html` if the markup must change |
| Give a rubrique its own central gabarit | `squelettes/inclusions/inc-rubrique_‹mot›.html` + a mot of group `type_rubrique` |

Never edit files inside the plugin directory — upgrades overwrite them.

## Reference files

- `references/noisettes.md` — the 107 noisettes: catalogue, per-family availability, « À la une » tabs, per-noisette settings
- `references/pages-speciales.md` — agenda, mini-calendrier, auteur, forum d'article, recherche, 404, contact, annuaire, mots-clés, trombinoscope, forum de site: URL, activation, dependencies
- `references/configuration.md` — the 24 config screens, key-naming conventions, the 44 technical mots-clés, PHP surface (filtres, balises, pipelines)
- `references/documentation-amont.md` — map of the author's tutorial site to noisettes, pages and settings. **Beginner-oriented human docs, secondary to the code:** never quote an identifier or a default from it without confirming it in the source.
