---
name: cloudflare-sveltekit-workers-d1
description: Expert guidance for deploying TypeScript SvelteKit apps to Cloudflare Workers (edge) with D1. Use when configuring @sveltejs/adapter-cloudflare, Wrangler config, Workers Assets, D1 bindings/migrations, or when writing precise step-by-step deployment instructions for SvelteKit on Cloudflare Workers/Pages with D1.
---

# Cloudflare SvelteKit Workers D1

## Overview

Provide a clear, current workflow to connect a SvelteKit TypeScript app to Cloudflare Workers and D1, including adapter setup, Wrangler configuration, D1 bindings/migrations, local testing, and deployment instructions.

## Workflow Decision Tree

- **Existing SvelteKit app** -> Use the Manual Setup workflow in `references/manual-workers-d1.md`.
- **Brand new project** -> Use the Cloudflare framework CLI flow in `references/manual-workers-d1.md` (C3 option).
- **User wants fastest/auto config** -> Use `references/wrangler-autoconfig.md` (experimental) and still verify the generated config.

## Core Workflow (Manual Setup)

1. Verify the latest Cloudflare + SvelteKit docs with `web.run` (adapter-cloudflare, Workers framework guide, D1 commands).
2. Add the Cloudflare adapter and update `svelte.config.js`.
3. Create or update `wrangler.toml` for Workers Assets and D1 bindings.
4. Create the D1 database and copy its binding block into `wrangler.toml`.
5. Add TypeScript platform typings and use `platform.env.DB` in server endpoints.
6. Create/apply migrations locally and remotely.
7. Build, test with Wrangler, then deploy.

Use the exact steps and snippets in `references/manual-workers-d1.md`.

## D1 Integration Checklist

- Ensure the binding name is a valid JS identifier and matches `platform.env.<BINDING>` in code.
- Ensure `wrangler.toml` includes `[[d1_databases]]` with `database_name` + `database_id`.
- Create and apply migrations with both `--local` and `--remote` as needed.
- Update TypeScript declarations in `src/app.d.ts`.

## Local Dev and Testing Guidance

- Prefer SvelteKit dev server for general UI work.
- For Cloudflare-specific behavior, build and run `wrangler dev .svelte-kit/cloudflare`.
- Use adapter `platformProxy` options if local bindings need tweaks.

## Writing Deployment Instructions

- Be explicit about files, commands, and where to paste blocks.
- Always include the `wrangler.toml` skeleton and D1 binding block.
- Include verification steps (local dev and a deploy check).
- If there is any uncertainty in versions or commands, re-check docs via `web.run`.

## Resources

- `references/manual-workers-d1.md` - canonical manual setup workflow + snippets
- `references/wrangler-autoconfig.md` - experimental Wrangler auto-setup path
