---
name: lando-wp
description: Use when the question is about Lando itself in a WordPress project - which commands the recipe provides (lando wp, composer, db-import, db-export, logs) versus project tooling, start vs restart vs rebuild vs destroy vs poweroff, editing .lando.yml or .lando.local.yml (env_file, tooling), Xdebug, *.lndo.site DNS, untrusted certificates on WSL2, ports already allocated, unknown tooling commands. For running tests use testing-wp; for the Vite dev server use tailwind-vite-assets; for project detection use roots-triage.
license: MIT
compatibility: Filesystem agent with bash; Lando 3.21+ (3.26.x observed) with the @lando/wordpress recipe; Docker Desktop with WSL integration or Docker Engine. Lando 4 and services declared with api 4 are out of scope.
---

# Lando for WordPress projects

Every project command goes through Lando. This skill says which commands always exist, which must be read from the project, and what each lifecycle command does to containers and data.

## When to use

- Running WP-CLI, Acorn, Composer, Node, tests, linters, cache flushes, database import/export or log reads in a project with a `.lando.yml`.
- Choosing between `start`, `restart`, `rebuild`, `destroy`, `poweroff` after a change.
- Editing the Landofile chain (`.lando.base.yml`, `.lando.dist.yml`, `.lando.upstream.yml`, `.lando.yml`, `.lando.local.yml`).
- Site not loading, red URLs, certificate warnings, port clashes, Xdebug not stopping, tooling "not found".
- Not for: production or staging hosts, CI pipelines that do not use Lando, Lando 4 / `api: 4` experiments.

## Inputs required

Placeholders below are filled by the session context from the triage JSON. If a placeholder is still literal, read the field yourself:

| Placeholder | Triage field | Example |
|---|---|---|
| `{{name}}` | `runtime.lando.name` | `acme` |
| `{{webroot}}` | `runtime.lando.webroot` (default `.`) | `.`, `web`, `public` |
| `{{web_service}}` | `runtime.lando.webService` | `appserver` or `appserver_nginx` |
| `{{core_path}}` | `site.wpCli.path` | `wp`, `public/wp` |
| `{{php}}` | `runtime.lando.php` | `8.4` |
| `{{db_cli}}` | from `runtime.lando.database` | `mysql`, `mariadb`, `psql` |
| `{{redis_service}}` | the `services` entry of type `redis:*` | `redis`, `cache` |
| `{{tooling.<name>}}` | `runtime.lando.tooling` / `runners` | `{{runner.cache}}` = `lando cache-clear` |
| `{{runner.node}}` | `runtime.runners.node` | `lando yarn`, `lando npm`, none |

Also needed:

- Host facts: `lando version --all`, `docker context ls`, repo path inside the WSL filesystem (not `/mnt/c`).
- The user's consent before destructive steps: `lando destroy` (loses the database), `lando db-import` (wipes the database first unless `--no-wipe`), `lando poweroff` (stops every Lando app), `docker system prune`.

## Procedure

1. **Read the Landofile chain** in load order: `.lando.base.yml`, `.lando.dist.yml`, `.lando.upstream.yml`, then `.lando.yml`, then `.lando.local.yml` (last wins). If `recipe` is not `wordpress`, only the core commands are guaranteed (`lando ssh`, `lando exec`); there is no `lando wp`. Details: [references/landofile.md](references/landofile.md).
2. **Separate built-ins from project tooling.** The `wordpress` recipe always provides `lando wp`, `lando composer`, `lando php`, `lando db-import`, `lando db-export` and the database CLI (`lando mysql`, `lando mariadb` for MariaDB 10.4+, `lando psql`). It does **not** provide `yarn`, `npm`, `node`, `redis-cli`, `pull`, `push` or a dedicated `acorn` command: if they exist, the project defined them under `tooling:`. Read every tooling name; never assume one. Details: [references/wordpress-recipe.md](references/wordpress-recipe.md).
3. **Check state.** `lando list --app {{name}}`; if nothing runs, `lando start` (first run builds images, downloads WP-CLI and Composer, runs build steps and `pre-start` events; it can take minutes and needs network). Then `lando info --format json` for URLs, services and database credentials.
4. **Run commands from the project root**, so `wp-cli.yml` applies:
   - WP-CLI: `lando wp <cmd>`; add `--path=/app/{{core_path}}` only when there is no `wp-cli.yml`.
   - Acorn: `{{runner.acorn}}` when the project defines it, else `lando wp acorn <cmd>`.
   - PHP packages: `lando composer <cmd>`. Node: `{{runner.node}} <cmd>`, on the service the tooling names.
   - Tests, linters, cache: `{{runner.test}}`, `{{runner.lint}}`, `{{runner.cache}}`; without a cache tool, `lando wp cache flush` and `lando wp acorn optimize:clear`.
   - Anything without a route: `lando ssh -s appserver -c "<cmd>"` (deprecated, removed in Lando 4) or `lando exec appserver -- <cmd>`. Packages installed as root this way vanish on the next rebuild; persist them with `build_as_root`.
   - If `excludes:` lists `vendor` or `node_modules`, the host copy is not the container copy: never run host `composer` or `npm` for that project.

   The Composer and Node project that owns Acorn is not always the repo root. Pass the container path (`/app/...`):

   | | `sage-theme` | `acorn-mu-plugin` | `radicle-app` |
   |---|---|---|---|
   | Acorn's `composer.json` | theme folder: `lando composer --working-dir=/app/<theme path>`; the root one (Bedrock) holds WordPress and plugins | plugin folder: `lando composer --working-dir=/app/<plugin path>`; root `lando composer` only installs WordPress and plugins | project root: `lando composer` |
   | `package.json` / Vite | theme folder (tooling `dir:` or `cd` in the tooling `cmd`) | plugin folder (tooling `dir:` or `cd` in the tooling `cmd`) | project root, often on a separate Node service |
   | `lando wp acorn` answers | only while the theme is active | always | always |
5. **Apply configuration changes with the right lifecycle command** ([references/cli-semantics.md](references/cli-semantics.md)):

   | Change | Command |
   |---|---|
   | `.lando.yml`, `.lando.local.yml`, `env_file` contents, build steps, PHP version or extensions, `xdebug`, `webroot`, `via` | `lando rebuild -y` (database kept; `-s <service>` for a subset) |
   | Wedged processes, no config change | `lando restart` (does not re-run build steps) |
   | Database credentials, type or major version; empty database wanted | `lando destroy -y && lando start` (data lost; export first) |
   | Tooling command "not found" after editing `tooling:` | `lando --clear`, then `lando` |
   | Global `~/.lando/config.yml` | `lando poweroff`, then `lando start` |

   Team settings go in `.lando.yml`; personal ones in `.lando.local.yml` (gitignored). `env_file` is a **top-level** key: nested under `config:` it is silently ignored.
6. **Database work.** Import with `lando db-import <file>` (the file must be inside the project directory; `.sql`, `.sql.gz`, `.zip`; wipes first unless `--no-wipe`; fires `pre-db-import`/`post-db-import`). Export with `lando db-export [file]` or `--stdout`. GUI clients: `lando info --service database --format json` gives `external_connection` (`127.0.0.1:<port>`, port changes on restart unless pinned with `services.database.portforward: <port>`); credentials `wordpress`/`wordpress`/`wordpress`, or passwordless `root`. Inside the app, the host is `database`, never `localhost`.
7. **Diagnose.** `lando logs -s appserver -s {{web_service}} -f` (stdout/stderr only); `lando ssh -c "tail -f /app/{{webroot}}/wp-content/debug.log"` when `WP_DEBUG_LOG` is on; `lando info --deep`; `~/.lando/logs/{{name}}-error.log`; rerun with `-vvvv`. Symptom table: [references/failure-modes.md](references/failure-modes.md). WSL2 specifics (CA trust, filesystem, Docker integration): [references/wsl2.md](references/wsl2.md).
8. **Finish.** `lando stop` frees this app; `lando poweroff` frees ports 80/443 for everything (ask first: it stops other projects too).

## Verification

- `lando info --service {{web_service}} --format json` lists `https://{{name}}.lndo.site`; `curl -kI https://{{name}}.lndo.site` answers 200 or a redirect.
- `lando wp core is-installed && lando wp option get siteurl` matches the `.lndo.site` URL; `lando wp acorn --version` answers on Acorn projects.
- `lando php -v` shows `{{php}}`; `lando composer --version`; `{{runner.node}} --version` when Node tooling exists.
- `lando {{db_cli}} -e 'select 1'` succeeds.
- After a rebuild: `lando php -m | grep -i <ext>` for added extensions; `lando ssh -c "env | grep LANDO_WEBROOT"` prints `/app/{{webroot}}`.
- `lando redis-cli ping` returns `PONG`, only when that tooling exists and its `service` is `{{redis_service}}`.
- `lando` with no arguments lists every project tooling name; if one is missing, `lando --clear`.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| URLs red in `lando start`, browser cannot resolve `*.lndo.site` | No internet, or router DNS-rebinding protection (the wildcard resolves to 127.0.0.1 through public DNS) | `nslookup {{name}}.lndo.site`; add `127.0.0.1 {{name}}.lndo.site` to hosts; use the `localhost:<port>` URL from `lando info` |
| Certificate not trusted in the Windows browser | The Lando CA lives in the WSL distro, not in the Windows store | `certutil -addstore -f "ROOT" \\wsl.localhost\<distro>\home\<user>\.lando\certs\LandoCA.crt` from Windows; see `references/wsl2.md` |
| `lando <tool>`: unknown command after editing `tooling:` | Tooling routes are cached | `lando --clear`, then `lando` |
| Tooling fails with "No such service" | Tooling `service:` names a service that does not exist | Fix the tooling entry, or run `lando ssh -s <real-service> -c <cmd>` |
| Env var missing inside the container | `env_file` nested under `config:`, or an injected file edited without rebuild | Move `env_file` to the top level and `lando rebuild -y` |
| `wp` or `composer` not found, build step fails each start | Download from GitHub blocked (proxy, corporate network); failing build steps re-run every start | Proxy variables in an env file, or install a pinned binary in `build_as_root`; `lando rebuild -y` |
| "This does not seem to be a WordPress installation" | Ran from a subfolder without `wp-cli.yml` in scope | Run from the root, or `lando wp --path=/app/{{core_path}} ...` |
| Port 5173/5174 "already allocated" | Another app publishes the same host port | Stop that app or change `services.<svc>.ports` |
| Everything slow | Repo on `/mnt/c` or slow Docker file sharing | Move the repo into the WSL home; `excludes: [vendor, node_modules]` + rebuild |

The full 20-row table lives in `references/failure-modes.md`.

## Escalation

- Lando itself misbehaves: rerun with `--debug -vvvv`, collect `~/.lando/logs/lando-error.log`, `~/.lando/logs/{{name}}-error.log`, `lando version --all`, `docker version`, then open an issue on `lando/lando` or the plugin repository (`lando/wordpress`, `lando/php`).
- Landofile defects found by triage (misplaced `env_file`, tooling pointing at a missing service, unpinned database version, keys the recipe ignores): report them to the project maintainers; do not edit `.lando.yml` on your own initiative.
- Hosting, CI or production parity questions are outside this skill.
- Lando 4 / `api: 4`: out of scope; Lando 3.26.x is the supported line and the next major is unreleased.

<!-- verified: the reference acorn-mu-plugin project's .lando.yml build steps — root `composer install`, then `--working-dir=/app/wp-content/mu-plugins/<plugin>`, then `cd` into the plugin for `yarn install && yarn build` (acorn-mu-plugin); roots/sage clone — composer.json and package.json at the theme root (sage-theme); radicle-app facts checked against a licensed local Radicle project; not reproduced here -->
<!-- sources: report 08 §1.5, §1.8, §2.2–§2.10, §3.3, §5 — https://docs.lando.dev/cli/ · https://docs.lando.dev/landofile/ · https://docs.lando.dev/landofile/tooling.html · https://docs.lando.dev/config/env.html · https://docs.lando.dev/config/security.html · https://docs.lando.dev/help/dns-rebind.html · https://docs.lando.dev/plugins/wordpress/tooling.html · https://docs.lando.dev/plugins/wordpress/config.html · https://docs.lando.dev/guides/db-import.html · https://docs.lando.dev/config/performance.html -->
