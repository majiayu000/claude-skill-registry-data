---
name: wp-headless-backend
description: Build and bootstrap WordPress headless (PHP-FPM) with an idempotent wp-cli entrypoint and WPGraphQL enabled, using MariaDB/MySQL from docker-compose. Use when asked to implement or fix docker/wp/Dockerfile and docker/wp/entrypoint.sh for WordPress in this repo.
---

# WP Headless Backend

## Overview

Make WordPress self-install and configure on container start with WPGraphQL enabled, while staying safe to restart. Focus on PHP-FPM image setup and an idempotent wp-cli entrypoint.

## Workflow

1. Inspect `docker/wp/Dockerfile` and `docker/wp/entrypoint.sh` for PHP-FPM base, extensions, wp-cli, and bootstrap flow.
2. Ensure Dockerfile installs required PHP extensions and minimal tools, sets `WORKDIR /var/www/html`, and includes wp-cli.
3. Implement entrypoint bootstrap steps with retries for DB readiness and idempotent install guards.
4. Enable permalinks, install and activate WPGraphQL, and avoid destructive actions on reboot.
5. Finish by exec'ing PHP-FPM in foreground.

## Repo Assumptions

- DB service is `db_wp` (MariaDB/MySQL), not Postgres.
- WordPress files are mounted from `./wordpress` into `/var/www/html`.
- Edge calls PHP-FPM at `wp:9000`.

## Required Outputs

- Create or update: `docker/wp/Dockerfile` and `docker/wp/entrypoint.sh`.
- Optionally add a minimal theme at `wordpress/wp-content/themes/headless/`.

## Dockerfile Requirements

- Use PHP 8.3 FPM base.
- Install extensions: `mysqli`, `pdo_mysql`, `gd`, `intl`, `zip`, `opcache`.
- Install wp-cli (official binary).
- Include minimal utilities: `curl`, `unzip`, `bash`/`sh`.
- Set `WORKDIR /var/www/html`.

## Entrypoint Behavior

- Wait for DB with retry/backoff and clear errors.
- If WordPress is not installed:
  - Download core if missing.
  - Create wp-config using env DB vars.
  - Run `wp core install` using env `WP_URL`, `WP_TITLE`, `WP_ADMIN_*`.
  - Set permalinks to `/%postname%/`.
- Install and activate `wp-graphql` plugin.
- If WordPress is already installed, avoid destructive actions.
- Always exec PHP-FPM in foreground at the end.

## Acceptance Checklist

- Rebooting containers does not reinstall WordPress.
- `http://localhost:8080/graphql` responds.
- WPGraphQL plugin is active.
