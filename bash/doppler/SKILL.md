---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: doppler
description: >
  Doppler CLI workflows for secrets management in this workspace. Covers
  creating projects non-interactively (agent-friendly), renaming the
  default envs to development/preview/production, uploading secrets,
  type-safe env access in TypeScript apps, CI integration via GitHub
  Actions, and syncing secrets to Cloudflare Workers (wrangler) and
  Fly.io (flyctl). Use this skill whenever a task involves `doppler run`,
  `DOPPLER_TOKEN`, creating or renaming Doppler projects/configs, adding
  `.env` secrets to Doppler, syncing Doppler secrets to a deployment
  target, or wiring Doppler into a new service or CI workflow.
---

# doppler

Doppler is the secret store this workspace uses across every package. All
`package.json` scripts that need env vars are wrapped in `doppler run -c
<config> --`, and deploys pull secrets out of Doppler into the deployment
target (Cloudflare Workers, Fly, GitHub Actions) instead of committing
`.env` files.

## Shell env var ordering

When a command needs both shell env vars and Doppler secrets, put the shell env vars **before** `doppler run`, never after.

```bash
# GOOD
CLOUDFLARE_ENV=preview doppler run -c preview -- vite dev
CLOUDFLARE_ENV=preview doppler run -c preview -- vite build

# BAD
doppler run -c preview -- CLOUDFLARE_ENV=preview vite dev
doppler run -c preview -- CLOUDFLARE_ENV=preview vite build
```

Why:

- tooling like Wrangler and `@cloudflare/vite-plugin` reads some env vars from the outer process setup
- this keeps scripts consistent and easy to scan
- it avoids subtle scope confusion about which process sees which env var

**Always run `doppler --help` and `doppler <command> --help` first.** The
help output is the source of truth. Do not pipe it through `head`/`tail` —
read it in full.

## Naming convention used in this workspace

All Doppler projects in this workspace use these **env slugs**:

- `development` — local dev, default for `doppler run` with no `-c`
- `preview` — staging / preview worker / preview database
- `production` — live site, workers, and Fly apps

The default slugs Doppler ships with (`dev`, `stg`, `prd`) are **always
renamed** to the above before using a new project. Scripts everywhere in
this repo rely on `-c preview` and `-c production` existing — never leave
a new project on the defaults.

Example from `plugin-mcp/package.json`:

```json
"dev": "doppler run -c preview -- vite",
"build": "doppler run -c production -- pnpm vite build",
```

Example from `db/package.json`:

```json
"diff:prod":    "doppler run -c production --command '...'",
"diff:preview": "doppler run -c preview --command '...'",
"diff:dev":     "doppler run -c dev --command '...'"
```

Note the `db` package still uses the legacy `dev` slug — new projects
should standardize on `development` instead.

## Authentication for agents (no `doppler login`)

`doppler login` is interactive (opens a browser). To run Doppler from an
agent or non-interactive script, skip login entirely:

```bash
# Option A: env var (nothing written to disk, preferred in CI)
export DOPPLER_TOKEN="dp.pt.xxxxx"   # personal token from dashboard

# Option B: persist in ~/.doppler, scoped to a directory
doppler configure set token="dp.pt.xxxxx" --scope=/

# Option C: inline per-command
doppler projects list --token "dp.pt.xxxxx"
```

Token types:
- **Personal token** (`dp.pt.*`) — full workplace access. Generate from
  Dashboard → Settings → API → Personal Tokens. Use for local agents.
- **Service account token** — scoped, better for CI/production.
- **Service token** (`dp.st.*`) — read-only for one config, safest for
  deploys.

**Orgs/workplaces cannot be created from the CLI.** You must sign up via
the dashboard once. After that, everything is CLI-able.

## Create a new project + rename envs (bootstrap script)

Use this exact script when bootstrapping a new package or service. It
creates the project, renames the three default envs to our convention,
and renames the matching child configs (otherwise `doppler run -c
development` breaks — see gotcha below).

```bash
#!/usr/bin/env bash
set -euo pipefail

PROJECT=$1   # e.g. "website"

# 1. Create project
doppler projects create "$PROJECT" --description "$PROJECT service"

# 2. Rename envs: dev → development, stg → preview, prd → production
doppler environments rename dev -p "$PROJECT" --name Development --slug development --yes
doppler environments rename stg -p "$PROJECT" --name Preview     --slug preview     --yes
doppler environments rename prd -p "$PROJECT" --name Production  --slug production  --yes

# 3. Rename the root config inside each env (env rename does NOT rename configs)
doppler configs update dev -p "$PROJECT" --name development
doppler configs update stg -p "$PROJECT" --name preview
doppler configs update prd -p "$PROJECT" --name production

# 4. Bind the current directory to this project + development config
doppler setup --no-interactive -p "$PROJECT" -c development
```

**Gotcha: env rename ≠ config rename.** Each environment contains one
root config that starts with the same slug. Renaming the env leaves the
child config stuck on the old name, which breaks `doppler run -c
development`. Always follow `environments rename` with `configs update`.

## Add secrets

```bash
# Individual keys
doppler secrets set API_KEY="abc" DATABASE_URL="postgres://..." -p website -c development

# From an .env / JSON / YAML file
doppler secrets upload .env -p website -c development

# Copy secrets between envs (pipe download into upload)
doppler secrets upload -p website -c preview \
  <(doppler secrets download -p website -c development --no-file --format json)
```

**`doppler secrets set` silently overwrites existing keys.** If you want
to preserve values, check first with `doppler secrets get KEY -p ... -c
... --plain` before setting.

## See env vars available

```bash
# Pretty list of all secrets in a config (values masked by default)
doppler secrets -p website -c development

# One secret, raw value
doppler secrets get DATABASE_URL -p website -c development --plain

# Export as .env to stdout
doppler secrets download -p website -c development --no-file --format env

# JSON
doppler secrets download -p website -c development --no-file --format json
```

For the currently bound project/config (set via `doppler setup`) just run
`doppler secrets` with no flags.

## Type-safe env in a TypeScript app

This workspace uses a hand-maintained `env.ts` object rather than a
validator library. The pattern is:

1. Read each var off `process.env` into a single `env` object.
2. At module load, throw if any server-side var is missing.
3. Import `env` everywhere instead of touching `process.env` directly.

Example (`website/src/lib/env.ts`):

```ts
export const env = {
    PUBLIC_URL: process.env.PUBLIC_URL,
    DATABASE_URL: process.env.DATABASE_URL,
    STRIPE_SECRET_KEY: process.env.STRIPE_SECRET_KEY,
    GITHUB_APP_PRIVATE_KEY: process.env.GITHUB_APP_PRIVATE_KEY,
    // ...every var the app uses
}

// Fail fast on missing vars. Only enforce PUBLIC_* in the browser.
for (const k in env) {
    if (
        env[k] == null &&
        (typeof window === 'undefined' || k.includes('PUBLIC'))
    ) {
        throw new Error(`Missing env var ${k}`)
    }
}
```

Rules for adding a new env var:
1. Add it to Doppler first (`doppler secrets set NEW_VAR=... -p <proj>
   -c development`). Repeat for `preview` and `production`.
2. Add it to `env.ts`.
3. Import from `env.ts`, never read `process.env.NEW_VAR` directly in
   app code.
4. `PUBLIC_*` vars are safe to expose to the browser. Anything else must
   only be read server-side.

To discover what the app expects vs what Doppler has:

```bash
# Vars the app reads
rg "process\.env\." src/lib/env.ts

# Vars Doppler provides
doppler secrets -p website -c development
```

## CI: GitHub Actions + Doppler

Every CI job that needs secrets follows this pattern (from
`.github/workflows/ci.yml`):

```yaml
jobs:
  ci:
    runs-on: ubuntu-latest
    env:
      DOPPLER_TOKEN: ${{ secrets.DOPPLER_TOKEN }}
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with: { node-version: 22 }
      - uses: pnpm/action-setup@master
      - uses: dopplerhq/cli-action@master   # installs the `doppler` binary
      - uses: superfly/flyctl-actions/setup-flyctl@master
      - run: pnpm install --frozen-lockfile=false
      - run: pnpm test   # scripts already call `doppler run -c ...`
```

Two things to wire up:

1. **Generate a service account token** in the Doppler dashboard
   (Settings → Service Accounts). Prefer this over a personal token in
   CI so it survives if a team member leaves.

2. **Add it to GitHub repo secrets** as `DOPPLER_TOKEN`:
   ```bash
   gh secret set DOPPLER_TOKEN --body "dp.sa.xxxxx" --repo owner/repo
   ```
   Or paste it in GitHub → Settings → Secrets and variables → Actions.

3. **Expose it at job level** via `env: DOPPLER_TOKEN: ${{
   secrets.DOPPLER_TOKEN }}` so every step (including `doppler run`
   inside package scripts) picks it up automatically.

The `dopplerhq/cli-action` step just installs the binary. It does not
log in — authentication happens via the `DOPPLER_TOKEN` env var. If you
forget the env var, `doppler run` in CI will fail with "no token found".

For workflows that scope the token tighter, pass it directly instead of
relying on job-level env:

```yaml
- run: doppler run -p website -c production -- pnpm deploy
  env:
    DOPPLER_TOKEN: ${{ secrets.DOPPLER_TOKEN_PROD }}
```

## Upload secrets to Cloudflare Workers

Cloudflare Workers store their own copy of secrets via `wrangler secret
put`. We sync from Doppler → Wrangler using the `--mount` flag so
wrangler sees a temporary `.env` file on disk, then `wrangler secret
bulk` uploads everything at once.

For local development, prefer `doppler run` directly instead of `.env` files:

```bash
doppler run -c development -- wrangler dev
CLOUDFLARE_ENV=preview doppler run -c preview -- vite dev
```

Use `.env` only as a temporary mounted file for `wrangler secret bulk`, not as the main local-development source of truth.

This is the exact pattern used in `plugin-mcp/package.json`:

```json
"secrets:preview": "doppler run -c preview --mount .env.preview --mount-format env -- wrangler secret bulk --env preview .env.preview",
"secrets:prod":    "doppler run -c production --mount .env.prod    --mount-format env -- wrangler secret bulk .env.prod"
```

Breakdown:
- **`doppler run -c <config>`** — pulls secrets from the Doppler config.
- **`--mount .env.preview`** — writes them to a temp file at
  `.env.preview` that only exists for the duration of the command.
  Nothing is written permanently to disk.
- **`--mount-format env`** — serialize as dotenv format (vs `json` /
  `yaml`).
- **`wrangler secret bulk <file>`** — wrangler reads the file and PUTs
  every key to the worker's secret store in one API call.
- **`--env preview`** — wrangler env name matches the Doppler config
  name, so `wrangler.toml`'s `[env.preview]` block gets the secrets. The
  production script omits `--env` to target the top-level worker.

Run this once per deploy target whenever secrets change:

```bash
pnpm secrets:preview   # sync Doppler preview → worker preview env
pnpm secrets:prod      # sync Doppler production → worker prod
```

Do **not** try to use `doppler run -- wrangler secret put KEY` one var
at a time — wrangler prompts for each value interactively and the
script hangs. Always use `wrangler secret bulk` with `--mount`.

## Upload secrets to Fly.io

Fly stores secrets via `flyctl secrets set` or `flyctl secrets import`.
The import form reads a dotenv-style stream on stdin, which pairs
perfectly with `doppler secrets download`:

```bash
# Sync Doppler production → Fly app secrets
doppler secrets download -p website -c production --no-file --format env \
  | flyctl secrets import --app my-fly-app
```

Or wrap it in a `package.json` script:

```json
"secrets:fly":         "doppler secrets download -p website -c production --no-file --format env | flyctl secrets import --app my-fly-app",
"secrets:fly:preview": "doppler secrets download -p website -c preview    --no-file --format env | flyctl secrets import --app my-fly-app-preview"
```

Gotchas:
- **`flyctl secrets import` triggers a restart/deploy** of the Fly
  machines once all keys are staged. Expect ~30s downtime for
  single-machine apps.
- **`--no-file`** makes `doppler secrets download` write to stdout
  instead of creating a local file. Without it you get `doppler.env`
  sitting on disk which must be gitignored.
- **Only keys that changed cause a restart**. If all values are
  identical to what Fly already has, Fly skips the restart.
- For CI use `--stage` to stage without restarting, then `flyctl deploy`
  separately: `flyctl secrets import --stage --app my-fly-app`.

## Quick reference

| Task | Command |
|---|---|
| Create project | `doppler projects create NAME` |
| Rename env | `doppler environments rename OLDSLUG -p PROJ --name NEW --slug NEW --yes` |
| Rename root config | `doppler configs update OLDNAME -p PROJ --name NEW` |
| Set one secret | `doppler secrets set KEY=VAL -p PROJ -c CONFIG` |
| Upload from file | `doppler secrets upload FILE -p PROJ -c CONFIG` |
| List secrets | `doppler secrets -p PROJ -c CONFIG` |
| Get one value | `doppler secrets get KEY -p PROJ -c CONFIG --plain` |
| Export env | `doppler secrets download -p PROJ -c CONFIG --no-file --format env` |
| Bind dir to project | `doppler setup --no-interactive -p PROJ -c CONFIG` |
| Run with secrets | `doppler run -c CONFIG -- COMMAND` |
| Debug config source | `doppler configure debug` |

## Docs

- CLI guide: https://docs.doppler.com/docs/cli
- Importing secrets: https://docs.doppler.com/docs/importing-secrets
- Service tokens: https://docs.doppler.com/docs/service-tokens
- GitHub Actions integration: https://docs.doppler.com/docs/github-actions
- Cloudflare Workers integration: https://docs.doppler.com/docs/cloudflare-workers
- Fly.io integration: https://docs.doppler.com/docs/fly
- CLI source: https://github.com/DopplerHQ/cli
