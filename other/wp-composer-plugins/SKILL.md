---
name: wp-composer-plugins
description: Use when adding, removing, updating or patching WordPress plugins, mu-plugins or themes through Composer - "install plugin", wpackagist versus wp-packages.org, installer-paths, a premium or private plugin zip as a Composer package, Composer patches, DISALLOW_FILE_MODS. For Acorn packages use the matching acorn-* skill; for Lando command wiring use lando-wp.
---

# WordPress plugins and themes through Composer

Plugins, mu-plugins and themes are Composer dependencies. Never install them with `{{runner.wp}} plugin install`, the admin upload screen or a hand-copied folder: the change would be lost on the next deploy and would not appear in `composer.lock`.

Runner placeholders (`{{runner.composer}}`, `{{runner.wp}}`, `{{runner.cache}}`) come from the session context. On Lando they default to `lando composer`, `lando wp` and the project's cache-clear tool; the `lando-wp` skill explains the wiring.

## When to use

- Installing, removing or updating a plugin, mu-plugin or theme.
- Choosing between wp-packages.org, WPackagist, a private repository or a local zip.
- Deciding which `composer.json` receives a dependency.
- A plugin installed in the wrong folder, an mu-plugin that does not load, or an update screen that offers to install things.
- Applying a fix to a third-party plugin without forking it.

Do not use for PHP libraries that only the Acorn application needs (for example a service provider package): those still go through Composer, but follow the matching acorn-* skill.

## Inputs required

1. The active profile and its Composer layout (session context). Read the root `composer.json` first: `repositories`, `extra.installer-paths`, `extra.wordpress-install-dir`.
2. What the user asked for: a wordpress.org slug, a `vendor/name` package, a zip path, or a Git URL.
3. Whether the plugin is premium or private (it cannot come from wp-packages.org).
4. Which Composer repository the project already uses (see "Repository" below). Do not mix two registries for the same kind of package.

### Which composer.json

| Profile | Site-level `composer.json` (WordPress plugins, themes, core) | Acorn application `composer.json` (PHP libraries for the app) |
|---|---|---|
| `sage-theme` | project root (Bedrock or plain Composer WordPress) | theme folder (`vendor/` inside the theme) |
| `acorn-mu-plugin` | project root | the mu-plugin folder (own `vendor/`, own lock) |
| `radicle-app` | project root, which is also the Acorn application | same file; Acorn providers go in `extra.acorn.providers` |

A WordPress plugin (`wp-plugin/*`, `wordpress-plugin` type) always belongs to the site-level file, the one that holds `installer-paths`. Run Composer against the right folder with `--working-dir` when the target is the nested Acorn application, for example `{{runner.composer}} --working-dir=<acorn base path> require vendor/package`.

### Installer paths per profile

Composer places a package by its `type` through `extra.installer-paths`. Read the project's own map before installing; the folders differ by layout.

| Layout (profile usually seen with it) | plugins | mu-plugins | themes | core |
|---|---|---|---|---|
| Bedrock (`sage-theme`) | `web/app/plugins/{$name}/` | `web/app/mu-plugins/{$name}/` | `web/app/themes/{$name}/` | `web/wp` |
| Composer WordPress at the repo root (`acorn-mu-plugin` seen in a project using `wp-content/`) | `wp-content/plugins/{$name}/` | `wp-content/mu-plugins/{$name}/` | `wp-content/themes/{$name}/` | `wp` (or similar) |
| Radicle layout (`radicle-app`) | `public/content/plugins/{$name}/` | `public/content/mu-plugins/{$name}/` | `public/content/themes/{$name}/` | `public/wp` |

Rules that hold in every layout:

- The mapping key is a path template, the value is a list of `type:wordpress-plugin`, `type:wordpress-muplugin`, `type:wordpress-theme` (or a package name). Packages without a matching entry land in `vendor/`, which is the usual cause of "installed but WordPress does not see it".
- To force a normal plugin into the mu-plugins folder, add its package name to the mu-plugin entry's list (see [references/installer-paths.md](references/installer-paths.md)).
- WordPress loads only `*.php` files placed directly in the mu-plugins folder; folders are ignored. A Composer-installed mu-plugin lives in a subfolder, so the project needs a loader (Bedrock ships `roots/bedrock-autoloader`; Radicle tracks a boot file in that folder). If a new mu-plugin does nothing, check the loader before anything else.
- Installed plugin and mu-plugin folders are normally git-ignored; Composer recreates them. Do not commit them unless the project decided to.

### Repository

| Registry | Config | Package names | Notes |
|---|---|---|---|
| wp-packages.org (preferred for new work) | `{{runner.composer}} config repositories.wp-packages composer https://repo.wp-packages.org` | `wp-plugin/<slug>`, `wp-theme/<slug>` | Free, no authentication, wordpress.org directory only. Run by Roots, refreshes in minutes. |
| WPackagist (legacy, still common) | `repositories` entry pointing to `https://wpackagist.org` | `wpackagist-plugin/<slug>`, `wpackagist-theme/<slug>` | Same content, slower refresh. Keep it if the project uses it; migrating is a rename of the package prefix plus a repository swap (Roots publishes a migration script). |
| Vendor repository (premium) | the vendor's own `type: composer` URL with credentials in `auth.json` or `COMPOSER_AUTH` | vendor's name | ACF Pro is the common case. Credentials never go into `composer.json` or the repo. |
| Private artifact | `type: package` or `type: vcs` | your own `vendor/name` | See below. |

wp-packages.org does not host premium plugins. A plugin that is not on wordpress.org cannot be installed with `wp-plugin/<slug>`; do not guess a slug, check the directory first.

## Procedure

1. **Confirm the layout.** Read `composer.json` (`repositories`, `installer-paths`, `config.allow-plugins`). Confirm `composer/installers` or the project's installer is allowed. If the repository for wordpress.org plugins is missing, add it with the `config` command above rather than editing JSON by hand.
2. **Classify the source.**
   - wordpress.org slug: `{{runner.composer}} require wp-plugin/<slug>` (or `wpackagist-plugin/<slug>` on a WPackagist project). If unsure about the slug, look it up on wp-packages.org.
   - `vendor/name` already given: `{{runner.composer}} require vendor/name`.
   - Premium or private: use the private-package path below.
   - Untagged plugin on wordpress.org: `dev-trunk` is possible but pins to an SVN revision; ask first.
3. **Pin sensibly.** Let Composer write a caret constraint for stable plugins. For plugins that break on minor releases, ask the user whether to pin an exact version.
4. **Install.** Run the require command from the correct `--working-dir`. Read the output: the line `Installing wp-plugin/<slug> (x.y.z)` followed by the target path tells you the installer path was applied.
5. **Activate if asked.** Plugins: `{{runner.wp}} plugin activate <slug>`. Mu-plugins need no activation. Activation changes the database; do it only when the user asked.
6. **Clear caches.** `{{runner.cache}}` after changing anything that registers hooks, blocks or providers (the Acorn caches and the object cache can still describe the old state).
7. **Remove.** `{{runner.wp}} plugin deactivate <slug>` if active, then `{{runner.composer}} remove <package>`. Report data the plugin leaves behind (options, tables) but do not delete it unasked.
8. **Update.** Re-require the package (`{{runner.composer}} require wp-plugin/<slug>`) or run `{{runner.composer}} update vendor/name --with-dependencies`; core with `{{runner.composer}} require roots/wordpress -W` on a Roots layout. Update one package at a time so the diff of `composer.lock` is reviewable.
9. **Report.** Package and version, repository added or reused, target folder, activation state, the lock file change.

### Private or commercial plugins

Preferred order, simplest first:

1. **Private Git repository** with a `composer.json` of type `wordpress-plugin`, one tag per release, added as a `vcs` repository. This is the method documented by Roots.
2. **Artifact registry or generic package registry URL** declared as a `type: package` repository with `dist.url`, `dist.type: zip` and `dist.shasum`. Works well in CI because the URL is stable and the checksum is verified.
3. **Local zip** in a `packages/` folder with `dist.url` pointing at it. Fine for a quick start; the path is resolved relative to where Composer runs and the zip must be committed or provided to CI.
4. Satis, SatisPress or Private Packagist when the team has many private packages.

For every `type: package` entry the `version` is mandatory and must be bumped by hand on each new zip. Use `type: wordpress-muplugin` for mu-plugins. Never put licence keys or tokens in the entry; use `auth.json` (git-ignored) or `COMPOSER_AUTH`. Full examples: [references/private-packages.md](references/private-packages.md).

### Patching a plugin

Do not edit installed plugin files; they are overwritten on the next install. Use `cweagans/composer-patches`, keep the `.patch` in a tracked `patches/` folder, and record why in the patch description. The configuration shape depends on the major version in `composer.lock` (1.x maps a description to a path; 2.x uses a list of `description` + `url`). Details in [references/patching.md](references/patching.md).

### Production safety

Set `DISALLOW_FILE_MODS` to true in non-local environments (Bedrock does this in its application config). WordPress then refuses plugin and theme installation and updates from the admin, which keeps the Composer lock as the single source of truth. Locally you can leave it off, but still install through Composer.

## Verification

- `{{runner.composer}} show <package>` prints the installed version and path.
- The package folder exists at the path the installer map promises (`ls` the plugins or mu-plugins folder).
- `{{runner.wp}} plugin list` shows the plugin (status `inactive` is normal until activated). `{{runner.wp}} plugin list --status=must-use` lists only top-level mu-plugin files such as the loader; an mu-plugin loaded by an autoloader from a subfolder is verified by its behaviour (a hook it registers, a log line), not by that list.
- `{{runner.composer}} validate` passes and `git status` shows only `composer.json`, `composer.lock` and, if relevant, `patches/` or `packages/`.
- After activation, load a page and check the log (see roots-debugging) for fatals.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `Could not find a matching version of package wp-plugin/<slug>` | Repository missing, wrong prefix for the registry, or the plugin is not on wordpress.org | Check `repositories`; use the prefix of the registry the project uses; premium plugins need a vendor or private source |
| Package installed under `vendor/` instead of the plugins folder | No `installer-paths` entry for the type, or `composer/installers` not allowed | Add the entry and allow the installer in `config.allow-plugins`, then reinstall the package |
| mu-plugin installed but nothing runs | WordPress ignores subfolders of the mu-plugins folder | Add or fix the loader (autoloader package or a tracked boot file) |
| Plugin vanished after deploy | Installed by `{{runner.wp}} plugin install` or the admin upload | Require it through Composer and commit the lock |
| `The "./packages/x.zip" file could not be downloaded` | Relative path resolved from another directory, or the zip is not in CI | Run Composer from the root, commit the zip, or move to a registry URL with `shasum` |
| `shasum` mismatch | New zip uploaded under the same URL | Recompute the checksum and bump the package `version` |
| Patch fails to apply after an update | Plugin source changed | Rebuild the patch against the new version, or drop it if upstream fixed the issue |
| Admin shows "Install" or "Update" buttons in production | `DISALLOW_FILE_MODS` not set | Define it for the production environment |
| `Your requirements could not be resolved` between two plugins that bundle the same library | Conflicting PSR or helper packages | Prefer the maintained plugin; as a last resort patch the bundled copy |

## Escalation

- A plugin that is premium, abandoned or needs credentials you do not have: ask the user for the source and the licence process.
- Changing `installer-paths`, the registry or `allow-plugins` affects every deploy: show the diff and wait for approval.
- Anything that needs file changes on a running environment (not through the pipeline) belongs to the deploy owner.

<!-- verified: wp/wp-includes/load.php:974-997 — wp_get_mu_plugins only lists top-level *.php files of WPMU_PLUGIN_DIR;
wp/wp-includes/load.php:1829-1838 — wp_is_file_mod_allowed is false when DISALLOW_FILE_MODS is true;
refs/roots-bedrock/composer.json:26-31 — Bedrock ships the wp-packages repository https://repo.wp-packages.org;
refs/roots-bedrock/composer.json:37 — roots/bedrock-autoloader is a Bedrock dependency;
refs/roots-bedrock/composer.json:61-72 — installer-paths web/app/{mu-plugins,plugins,themes} and wordpress-install-dir web/wp;
refs/roots-bedrock/config/application.php:151 — DISALLOW_FILE_MODS defined true;
refs/roots-docs/bedrock/composer.md — wp-plugin and wp-theme namespaces, forcing a plugin into mu-plugins via installer-paths;
refs/roots-docs/bedrock/private-or-commercial-wordpress-plugins-as-composer-dependencies.md — private Git repo as vcs repository, tag per release;
refs/roots-docs/bedrock/patching-wordpress-plugins-with-composer.md — cweagans/composer-patches, extra.patches with description+url;
the reference acorn-mu-plugin project's composer.json — ACF Pro as wpengine/advanced-custom-fields-pro; installer-paths wp-content/*, type:package zips with dist.shasum, ACF Pro vendor repository, extra.patches 1.x shape;
its composer.lock — cweagans/composer-patches 1.7.3 in use;
radicle-app facts checked against a licensed local Radicle project; not reproduced here;
report 01 §3.8 — wp-packages.org: no auth, no premium, dev-trunk for untagged, migration script;
the reference acorn-mu-plugin project (lando wp plugin list --status=must-use) — lists only top-level files (bedrock-autoloader etc.), not the autoloaded subfolder mu-plugin -->
