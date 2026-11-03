---
name: spip5-plugins
description: >-
  Use when writing or extending a SPIP 5.0 plugin — listeners, scheduled tasks, injected services, Guard rules,
  private-space pages and menus — or when code mentions config/services.php, #[AsPipelineListener], #[AsCronTask],
  #[AsGuard], PipelineEvent, GuardRuleInterface, ConfigRepositoryInterface, spip.logger_registry. Not for moving
  4.x code (spip-migration-5), plugins that must still run on 4.4 (spip-migration-5 double-compat), or 4.x plugins
  (spip-plugins).
---

# SPIP 5.0 plugins

Verified on SPIP **5.0.0-beta** (`spip/spip` `c8e329575`, `ecrire` `2cd5843f`) by running every example on an
instance; additions of 2026-10-18 on `ecrire` `26bfe470`. SPIP 5 is still in development: when a symbol looks off,
check the source and `bin/spip`.

## The model in one screen

| Piece | 5.0 way |
|---|---|
| Manifest | `paquet.xml` (still required), `compatibilite="[5.0.0-dev;5.*]"`, **no** `<pipeline>`, `<genie>`, `<menu>` |
| Autoload | plugin `composer.json`: `"type": "spip-plugin"`, `autoload.psr-4` → `src/` |
| Services | `config/services.php`: `defaults()->autowire()->autoconfigure()` + `load('Acme\\', '../src/')` |
| Pipelines | `#[AsPipelineListener]` on a method typed with the event class (`Spip\Framework\Pipeline\Event\…`) |
| Tasks | `#[AsCronTask(name: …, periode: …)]`, `return 0` = success — **see the beta bug in `cron.md`** |
| Logs, config | inject with `#[Autowire(service: …)]` — plain `LoggerInterface` / `ConfigRepositoryInterface` **break the container** |
| Security | `GuardRuleInterface` + `#[AsGuard(priority: …)]` |
| Back office | `config/menus.php`, `prive/squelettes/contenu/<page>.html` |
| Rebuild | `bin/spip spip:cache:warmup --clear` after **any** new class, attribute or `services.php` change |

## Routing

| Task | Read |
|---|---|
| Create a plugin, files and activation | `references/squelette-plugin.md` |
| Hook a pipeline, which event class, which methods | `references/listeners-events.md` |
| Scheduled task | `references/cron.md` |
| Logger, config, request, directories, HTTP requests | `references/services.md` |
| Plugin settings (metas, own store) | `references/config-plugin.md` |
| Block or throttle requests | `references/guard.md` |
| Private page, menu, tabs, CSS/JS | `references/espace-prive.md` |
| Something is not called, console commands, `APP_ENV`, PHPStan / Rector | `references/outils.md` |

## Guardrails

- Exact FQCNs, never guessed: `SpipLeague\Bridge\Pipeline\Attribute\AsPipelineListener`,
  `SpipLeague\Bridge\Pipeline\Attribute\AsCronTask`, `SpipLeague\Component\Guard\Attribute\AsGuard`. Symfony's
  `#[AsEventListener]` is not a pipeline listener.
- Inside a class, inject (logger, config, inputs) — no `spip_log()`, `_request()`, `lire_config()`. The `Spip::`
  façade is for procedural code (filters, `genie_*`, `*_fonctions.php`), where `spip_log()` / `_request()` are
  deprecated but `lire_config()` is **not** (only its `/<store>/` prefix and `lire_config(,, false)` are).
- No `$GLOBALS['meta']`: it is a raw string mirror (`'[30]'` after an API write).
- One registration per pipeline: never a listener **and** a legacy function for the same behaviour.
- CLI is `bin/spip` (Symfony Console). spip-cli (`spip …`) is a 4.x tool.
- Site-wide settings go in the site's `config/custom.php`, plugin parameters in its `config/services.php`; never in
  `config/spip/*.php` or `options.php`.
- Code that must also run on 4.4 → `spip-migration-5` (`double-compat.md`), not this skill.
