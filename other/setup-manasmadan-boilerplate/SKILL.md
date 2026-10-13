---
name: setup
description: Set up this repo on a new machine or repair a broken local environment. Use when the user asks to install, set up, bootstrap or "get it running", when `bun run doctor` reports problems, or when commands fail because of missing tools, .env variables or local services.
---

# Setup

1. Run `bun run doctor` and read every line.
2. Fix tool problems first; they need the user:
   - Node version mismatch → ask the user to run `nvm install && nvm use` (reads `.nvmrc`).
   - Docker not running → ask the user to start Docker Desktop.
   - `uv` missing → required, not only for `apps/ai`: codegen runs the AI service's
     exporter, and setup, `bun dev`, types and tests all run codegen. Ask the user to
     install it (`brew install uv`, or https://docs.astral.sh/uv/).
   - Bun older than `engines.bun` → ask the user to run `bun upgrade`.
3. Run `bun run setup`. It is idempotent: creates `.env` with generated secrets, installs
   dependencies, starts core services, applies migrations and generates code.
4. Run `bun run doctor` again and confirm "All good".

Never read or print `.env`. To set a value the user gives you, run
`bun run env:set KEY=value`. When the doctor says variables are missing from `.env`
(usually after a pull that added some), run `bun run setup`: it adds every missing one
from `.env.example` and generates the secrets, keeping existing values. Variables the
doctor reports in `.env` but not in `.env.example` are stale: tell the user to delete
those lines (you can't edit `.env`).

If a port is taken, find the holder with `lsof -nP -iTCP:<port> -sTCP:LISTEN`, then
either the user stops it, or set the matching `*_PORT` variable (see `.env.example`)
with `bun run env:set`, update the URL that uses it, and `bun run db:up`. When another
checkout of this repo holds it (its `bun dev` or e2e run), `bun run setup --stack <n>`
moves all of this checkout's ports and URLs instead.

`docs/troubleshooting.md` explains every doctor message.
