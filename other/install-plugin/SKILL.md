---
name: superpowers-sage:install-plugin
description: >
  Install WordPress plugins in Bedrock — lando composer require, Bedrock plugin
  management, composer.json for WP plugins, WP packagist, wpackagist-plugin,
  mu-plugins vs plugins, Bedrock plugin activation, composer.json repositories,
  lando wp plugin list, plugin compatibility, roots/wordpress-packagist
user-invocable: true
argument-hint: "[plugin slug|composer package|/absolute/or/relative/path/to/plugin.zip]"
---

# Install Plugin (Composer + Lando)

Install WordPress plugins through Composer only.

Announce at start: "I'm using the install-plugin skill to install this plugin with Composer inside Lando."

## Inputs

$ARGUMENTS

## Rules

- Never use `wp plugin install` for new plugin installation.
- Always run `composer` through Lando: `lando composer ...`.
- Install at project root `composer.json` (WordPress/plugin level), not theme `composer.json`.
- If plugin activation is requested, use `lando wp plugin activate <slug>` after Composer install.

## Procedure

### 1) Validate context

1. Confirm this is a Lando WordPress project (`.lando.yml` and root `composer.json` exist).
2. Read `skills/sage-lando/references/wordpress-composer.md`.
3. Ensure `wp-packages.org` repository exists:

```bash
lando composer config repositories.wp-packages composer https://repo.wp-packages.org
```

### 2) Route by argument type

#### Case A: Local zip (`*.zip`)

1. Resolve path from `$ARGUMENTS`.
2. If zip is outside project root, copy to `./packages/<filename>.zip`.
3. Derive slug from filename:
   - `plugin-name.zip` -> package `local/plugin-name`, type `wordpress-plugin`
   - `mu-plugin-name.zip` -> package `local/plugin-name`, type `wordpress-muplugin`
4. Add/update a `type: package` repository entry in root `composer.json` pointing to `./packages/<filename>.zip`.
5. Install with Composer:

```bash
lando composer require local/plugin-name
```

#### Case B: Package name already provided (`vendor/name`)

1. If argument already matches `vendor/name`, install directly:

```bash
lando composer require vendor/name
```

2. If it starts with `wp-plugin/`, no extra conversion is needed.

#### Case C: Plugin slug or human name

1. Normalize to a slug candidate (lowercase, dashes).
2. Try package `wp-plugin/<slug>`.
3. If uncertain or missing, search on `https://wp-packages.org/` and map to the exact slug.
4. Install:

```bash
lando composer require wp-plugin/<slug>
```

### 3) Verify installation

```bash
# Composer package installed
lando composer show wp-plugin/<slug>

# WordPress sees plugin
lando wp plugin list
```

If user requested activation:

```bash
lando wp plugin activate <slug>
```

## Failure modes

### Package not found

- Cause: wrong slug or package namespace.
- Fix: search `wp-packages.org` and retry with exact package.

### Composer ran in wrong context

- Cause: command executed in theme folder.
- Fix: run from project root where WordPress `composer.json` lives.

### Zip package installs but plugin not recognized

- Cause: wrong package type (`wordpress-plugin` vs `wordpress-muplugin`) or invalid zip structure.
- Fix: correct repository metadata and ensure zip contains valid plugin root files.

## Completion

Report:

1. Which package was required
2. Whether repository config was added/updated
3. Whether plugin was activated
4. Any manual follow-up needed
