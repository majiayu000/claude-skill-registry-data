---
name: wp-astro-supabase-devops
description: Set up or fix Docker Compose, Nginx edge routing, healthchecks, and service wiring for WordPress headless (MariaDB), Astro, and Supabase self-hosted in C:\digitalbitsolutions\wordpress_headless. Use when asked to make docker compose up --build work, update edge routing, or adjust .env.example/README for this WP + Astro + Supabase stack.
---

# WP Astro Supabase DevOps

## Overview

Make the repo bootable with a single Nginx edge and a minimal Supabase stack alongside WordPress (MariaDB) and Astro. Focus on Docker Compose wiring, edge routing, and documentation so the acceptance checklist passes.

## Workflow

1. Inspect current `docker-compose.yml`, `docker/edge/*`, `.env.example`, and `README.md` for drift from the repo constraints.
2. Update `docker-compose.yml` to include edge, wp, mariadb, astro, and supabase services with required ports, networks, volumes, healthchecks, and depends_on.
3. Update `docker/edge/Dockerfile` and `docker/edge/nginx.conf` to route WordPress paths to PHP-FPM and everything else to Astro with HMR headers.
4. Update `.env.example` to document all required env vars and defaults for MariaDB, WordPress, and Supabase.
5. Update `README.md` with run, verify, and reset instructions plus Supabase URLs.
6. Validate with the acceptance checklist commands and adjust configs if any response is missing.

## Repo Constraints

- Use only these paths: `./docker/edge/*`, `./docker/wp/*`, `./wordpress/*`, `./frontend/*`, `./volumes/*`.
- Keep a single Nginx edge; do not add extra reverse proxies.
- Use MariaDB/MySQL for WordPress and Postgres for Supabase; do not mix them.
- Preserve the idempotent WordPress entrypoint behavior.
- Use Tailwind v4 via `@tailwindcss/vite` for Astro; do not add `@astrojs/tailwind`.

## Required Outputs

- Create or update: `docker-compose.yml`, `docker/edge/Dockerfile`, `docker/edge/nginx.conf`, `.env.example`, `README.md`.

## Edge Routing Rules

- Route WordPress to PHP-FPM for:
  - `= /wp-login.php`
  - `^~ /wp-admin`
  - `^~ /wp-json`
  - `^~ /graphql`
  - `^~ /wp-content`
  - `^~ /wp-includes`
- Proxy everything else to Astro.
- Include HMR headers for Astro dev (`Upgrade`/`Connection`) and preserve host headers.

## Compose Wiring

- Expose edge on `8080`, Astro on `4321` internally, and WP PHP-FPM on `9000` internally.
- Use a real healthcheck for MariaDB/MySQL; WordPress must depend on DB health.
- Edge must depend on WordPress and Astro being reachable.
- Add Supabase services (Postgres + Kong + Auth + REST + Realtime + Storage + Studio) and keep them off the edge.
- Store Supabase volumes under `./volumes/supabase_db` (or similar within `./volumes`).

## Ports And URLs

- Expose edge at `http://localhost:8080`.
- Expose Astro direct at `http://localhost:4321`.
- Keep WordPress admin at `/wp-admin`.
- Keep WPGraphQL at `/graphql`.
- Expose Supabase Kong at `http://localhost:54321`.
- Expose Supabase Studio at `http://localhost:54323`.

## Acceptance Checklist

- Verify `curl -I http://localhost:8080/` returns a response from Astro.
- Verify `curl -I http://localhost:8080/wp-admin/` returns a response.
- Verify `curl -I http://localhost:8080/wp-json` returns a response.
- Document Supabase Studio and API gateway URLs plus a reset procedure in `README.md`.
