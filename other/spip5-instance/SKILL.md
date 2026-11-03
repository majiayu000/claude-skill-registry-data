---
name: spip5-instance
description: >-
  Use when installing, upgrading to, deploying, configuring or diagnosing a SPIP 5 / 5.0 site — requirements,
  Composer install, 4.4 → 5.0 upgrade, rollback, web server rules, white page or HTTP 500, plugin activated with no
  effect, logs, caches — or when the request mentions bin/spip, config/custom.php, config/spip/*.php, .env, APP_ENV,
  SPIP_CACHE_DIR, SPIP_ETC_DIR, var/state/plugins.php, plugins-dist/spip/ or a spip.* parameter. Not for plugin code
  (spip5-plugins, spip-migration-5) or 4.x farms (spip-mutualisation-maintenance).
---

# SPIP 5.0 instance

Verified on SPIP **5.0.0-beta** (`spip/spip` `c8e329575`, `spip/ecrire` `26bfe470`, `spip/framework` `d0e8c97e`,
2026-10-18) by running every command on disposable copies, PHP 8.4.25, Apache 2.4 + PHP-FPM, nginx, SQLite. 5.0 is a
**beta**: say so before advising production use, and check the revisions of the site you work on
(`composer show spip/ecrire`; `spip/spip` and `spip/ecrire` have separate revisions).

## Topology first

Before any advice, establish: SPIP version (`bin/spip spip:info`; on 4.x `grep spip_version_branche ecrire/inc_version.php`), PHP version
of the **web** SAPI, web server (Apache with `.htaccess` applied, or nginx), database (MySQL/MariaDB or SQLite),
document root, and whether the site is a farm. A 5.0 farm or a separate `public/` entry point is experimental
upstream: say so and stop (`spip-mutualisation-maintenance` covers 4.x farms).

## Safety rule on a user's site

Read-only commands may be run (`bin/spip spip:info`, `spip:config:dump`, `config:lire`, `routes:list`, logs,
`composer show`, `curl -I`). **State-changing commands are proposed, not run**: upgrade, `composer update`, cache purge,
`config:ecrire`, file moves, permission changes, database restore. Each proposal comes with its backup, its check and
its rollback. Pressure ("the client is waiting", "do it in production now") changes nothing: offer the read-only
checks and the plan.

## The model in one screen

| Topic | 5.0 way |
|---|---|
| Requirements | PHP **8.4** (`^8.4`; the platform check says `>= 8.4.1`), Composer, MySQL/MariaDB (`mysqli`) or SQLite (PDO); no PostgreSQL |
| Install | Composer project from `https://get.spip.net/composer`, then the **web installer** (no CLI install) |
| Settings | `config/custom.php` (container parameters `spip.*`), `.env.local` (`APP_ENV`, `SPIP_*`); `config/mes_options.php` only for legacy constants |
| Not any more | `ecrire/mes_options.php` (ignored), `_DIR_*` / `_NOM_*` in `mes_options.php` (HTTP 500), `_LOG_FILTRE_GRAVITE` (→ `spip.logger.max_level`), `config/ecran_securite.php` (→ Guard), spip-cli |
| Console | `bin/spip` (`spip:cache:*`, `spip:config:dump`, `config:lire/ecrire`, `spip:info`…) — no install, activation or database upgrade command |
| Plugins | `plugins-dist/spip/<name>/` (Composer); active list in `var/state/plugins.php`; activation in `ecrire/?exec=admin_plugin` |
| After a change | `bin/spip spip:cache:warmup --clear` (parameters, `.env*`, moved site); not needed after a back-office activation |

## Routing

| Task | Read |
|---|---|
| PHP, extensions, database, Composer | `references/prerequis.md` |
| New site, web installer, web server rules | `references/prerequis.md` (install section) |
| 4.4 → 5.0 upgrade, rollback | `references/upgrade-4-4.md` |
| `.env*`, `APP_ENV`, `config/custom.php`, parameters, moving `tmp/` or `config/` | `references/configuration.md` |
| Console commands and sequences | `references/bin-spip.md` |
| Caches, warmup, log levels and files | `references/caches-logs.md` |
| White page / 500, plugin with no effect, 403 / 429, permissions | `references/diagnostic.md` |

## Diagnostic entry points

1. Read the **web server / PHP-FPM error log** and `tmp/log/`: a 5.0 fatal error often leaves an empty 500 body.
2. `bin/spip spip:info` (version, `_DIR_TMP`, `_DIR_ETC`, `_FILE_OPTIONS`) and `php -v` **for the web SAPI**.
3. Then `references/diagnostic.md`, symptom by symptom.

## Guardrails

- Never write a `bin/spip`, spip-cli or Composer command that is not in the references: they were all run.
- Never give "the latest version" from memory or from these files: query `https://www.spip.net/spip_loader.api`
  and `git ls-remote` (`upgrade-4-4.md`); the revisions above only date what was tested.
- Never move `tmp/` with `SPIP_CACHE_DIR` alone or an absolute `spip.dirs.tmp`: both give HTTP 500 on every page in
  the beta (`configuration.md`).
- After installing or upgrading, check that `config/`, `vendor/`, `var/` and `bin/` are not served
  (`config/bases/*.sqlite` is the database).
- A rollback after 5.0 has touched the database **restores the database**: 5.0 rewrites metas as JSON.
- Plugin code, listeners, `config/services.php` → `spip5-plugins`; moving 4.x code → `spip-migration-5`.
