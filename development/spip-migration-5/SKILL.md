---
name: spip-migration-5
description: >-
  Use when moving SPIP 4.x plugin or squelette code to SPIP 5.0, keeping a plugin compatible with both 4.4 and 5.0,
  auditing code for SPIP 5 deprecations, or when code or errors mention SPIP 5, #[AsPipelineListener], #[AsCronTask],
  Spip::, config/services.php, bin/spip, or a deprecation "since 5.0". Not for plain SPIP 4.x development — use spip-plugins.
---

# SPIP 4.x → 5.0 migration

SPIP 5.0 runs SPIP inside a **compiled Symfony container**: plugins contribute services, typed pipeline
**events** and **attributes**; historical constants and helpers are removed or deprecated; config values
are stored differently. It is **not** Symfony full-stack: no `bin/console`, no `#[AsEventListener]`, no
`debug:event-dispatcher`.

**Verified against SPIP 5.0.0-beta** (`spip/spip` `c8e329575`, 2026-09-22, `ecrire` `2cd5843f`; additions of
2026-10-18 on `ecrire` `26bfe470`) and SPIP 4.4.23. SPIP 5.0 is still
moving: when a name in this skill looks off, check the source (paths in *Source of truth*) and `bin/spip list`.

**Requires the `spip5-plugins` skill** for the 5.0 target code (listeners, tasks, injection, Guard, menus): this
skill only maps 4.x constructs to it. If `spip5-plugins` is not available, say so instead of guessing the 5.0 code.

## Terms (keep as is)

| Term | Meaning |
|---|---|
| **pipeline (historique)** | `prefixe_nom()` function declared by `<pipeline>` in `paquet.xml` — still works in 5.0 |
| **listener** | service method with `#[AsPipelineListener]`, receives an **event** |
| **event** | typed object carrying pipeline data (`Spip\Framework\Pipeline\Event\*`) or generic `PipelineEvent` |
| **façade `Spip`** | `Spip\Framework\Spip` (global alias `Spip`) — 5.0 entry point for config, logs, inputs, paths |
| **`bin/spip`** | SPIP 5 console (`spip-league/console`). **spip-cli (`spip …`) is the 4.x tool** |

## Highest-risk changes

| 4.x | 5.0 | Why it bites |
|---|---|---|
| `function acme_affichage_final($html)` | listener `#[AsPipelineListener] onAffichageFinal(AffichageFinalEvent $e)` + `config/services.php` | without `services.php` + PSR-4 the class is never registered |
| `param()`, `service()`, `spip_logger()`, `spip_log()`, `_request()` | `Spip::param()`, `Spip::service()`, `Spip::logger()`, `Spip::input()` | old helpers are deprecated in 5.0 |
| `_IS_CLI`, `_ESPACE_PRIVE`, `_DIR_RESTREINT_ABS`, `_ROOT_RACINE` | `Spip::platform()->isCli()`, `Spip::isBackOffice()`, `generer_url_ecrire('acme')` for a `?exec=` URL, `Spip::directories()->getProjectDir()` | **removed**: fatal "undefined constant" |
| `app()->getRootDir()`, `app()->getCoreDir()`, `app()->relative()` | `Spip::directories()->getProjectDir()` / `getCoreDir()` / `relative()` | deprecated Kernel methods |
| genie `return 1;` (success) | `#[AsCronTask]` service, **`return 0;`** = success | in 5.0 `> 0` = **failure**, re-planned immediately; on 5.0.0-beta the queue does not run these services yet |
| `$GLOBALS['meta']['x']` read / `unserialize()` | `Spip::config('x')` | writes now store JSON (`150` → `"[150]"`); the mirror is the raw SQL string |
| `$GLOBALS['spip_pipeline']` in `options.php` | `<pipeline>` or listener | **silently ignored** by the compiled container |
| `{fusion}`, `[(#LOGO_ARTICLE\|left)]`, `</INCLURE>`, `(POUR)` | `{groupby}`, `[(#LOGO_ARTICLE{left})]`, `<INCLURE{…} />`, `(DATA){source tableau, …}` | removed or deprecated syntax |

## Routing

| Goal | Read |
|---|---|
| Look up one symbol (constant, function, critère, balise) and its replacement | `references/catalogue.md` |
| Rewrite pipelines, cron tasks, menus, assets, services for 5.0 | `references/plugin-modele-5.md` (mapping), then the **`spip5-plugins`** skill for the target code |
| Fix a squelette for 5.0 | `references/squelettes.md` |
| Config / metas behave differently after the upgrade | `references/config-metas.md` |
| Keep one plugin working on **4.4 and 5.0** | `references/double-compat.md` |
| Audit a plugin (grep, PHPStan, Rector), verify listeners, CLI commands | `references/audit-outils.md` |

## Guardrails

- Never use Symfony full-stack names: `#[AsEventListener]`, `bin/console`, `debug:*`, `EventSubscriberInterface`.
- Never invent an event class or method: the list is `bin/spip spip:pipeline:events` and `vendor/spip/framework/src/Pipeline/Event/`.
- Code targeting 4.4 **and** 5.0 must not call `Spip::` unguarded (absent in 4.4) — see `references/double-compat.md`.
- `lire_config()` / `ecrire_config()` are **not** deprecated; only the `/<store>/` prefix and `lire_config(,, false)` are.
- After adding or changing a listener, task or `services.php`: `bin/spip spip:cache:warmup --clear`, then `bin/spip spip:pipeline:listeners`.
- Requirements: PHP **8.4**, Symfony 8.1, upgrade the site from SPIP ≥ 3.2 (ideally 4.4 first).

## Source of truth

- `vendor/spip/framework/src/Spip.php` — façade; `vendor/spip/framework/src/Pipeline/Event/` — core events
- `vendor/spip-league/pipeline-bridge/src/` — `AsPipelineListener`, `AsCronTask`, `PipelineEvent`
- `vendor/spip-league/kernel/src/` — `Kernel`, `Directory/SpipDirectories`, `Platform`
- `ecrire/CHANGELOG.md`, `UPGRADE_5.0.md`; markers `trigger_deprecation('spip', '5.0'` and `#[\Deprecated(… since: '5.0')]`
- Documentation: dev.spip.net (`spip/docs`, `docs/fr/5.0/`) — where it disagrees with the source, the source wins
