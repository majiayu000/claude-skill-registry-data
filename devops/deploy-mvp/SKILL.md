---
name: deploy-mvp
description: Run the first production deployment of this project onto the Portainer + Infisical + GitHub Container Registry + GitHub Actions stack. Use when the user asks to "deploy the MVP", "deploy to production for the first time", "set up the deployment", "provision the database and secrets", "create the Portainer stack", "configure GitHub Actions deployment", or in Spanish "desplegar el MVP", "primer despliegue", "configurar el deploy", "crear el stack en Portainer", "cargar los secretos en Infisical". Covers provisioning the Postgres role/database, seeding Infisical, publishing the image to ghcr.io, creating the Portainer stack from the Git repository, wiring GitHub Actions variables and secrets, and verifying that subsequent pushes deploy automatically.
disable-model-invocation: true
---

# Deploy MVP

Take a project from "code on GitHub" to "running in production, redeploying on
every push to `main`" on this five-part stack:

| Concern | System |
| --- | --- |
| Data | PostgreSQL (existing server, one role + database per project) |
| Secrets | Infisical (one project per service, injected at container start) |
| Images | GitHub Container Registry (`ghcr.io`) |
| Orchestration | Portainer (standalone Docker Compose stack, deployed from the Git repo) |
| CI/CD | GitHub Actions (`.github/workflows/build_*.yml`) |

## How secrets actually flow

Get this wrong and nothing else matters. **Portainer never holds the app's
(tier-1) secrets.** The stack env carries the five bootstrap values the
container needs to authenticate to Infisical and, for the backend stack only,
the Directus admin block (`ADMIN_SECRET`, `ADMIN_PASSWORD`, `ADMIN_DB_*`) that
compose substitutes into the `directus-admin` service. The app container pulls
everything else from Infisical at boot.

```
GitHub Actions ──build──▶ ghcr.io/<org>/<project>-api-prod:sha-abc1234
      │
      └──deploy──▶ Portainer  ──git clone──▶ backend/docker-compose.prod.yml
                       │                              │
                       │  injects 5 bootstrap vars    │  compose substitution
                       │  (+ Directus block)          ▼
                       └──────────────────────▶  container starts
                                                      │
                                        docker/start-prod runs:
                                        infisical login --method=universal-auth
                                        infisical run --projectId --env -- /commands <api|worker>
                                                      │
                                                      ▼
                                     Infisical  ──~45 app secrets──▶ app process
```

Read `references/env-vars.md` before touching any of the three tiers. The
single most common failure is putting an application secret into the Portainer
stack env, where the app will never see it.

## Safety contract

This skill provisions real infrastructure. Hold to these rules:

1. **Never print a secret value.** Print names, lengths, and fingerprints
   (`sha256 | head -c 8`) — never the value. This includes generated passwords:
   write them straight into Infisical and report only that they were set.
2. **Confirm before every mutation** in a system the user did not explicitly
   ask you to change. Creating a database, creating an Infisical project, and
   creating a Portainer stack each require an explicit go-ahead.
3. **Never `DROP` anything** without the user typing the object name back.
4. **Idempotency first.** Every script here is safe to re-run. If a step
   already happened, detect it and report "already present" rather than
   erroring or duplicating.
5. **Stop at the first failure.** A half-provisioned deploy is worse than none.
   Report exactly which phase failed and what state the earlier phases left.
6. **Never commit credentials.** `.env.deploy` is gitignored; verify before
   writing to it.

## Locate the bundled files

Resolve the absolute directory containing this loaded `SKILL.md`. Use
`<skill-dir>/scripts/...` and `<skill-dir>/references/...` regardless of
whether this skill was loaded from `.claude` or `.agents`. Do not assume they live under the repository's top-level `scripts/`.

The Python scripts use only the standard library — no `pip install`, no `curl`.
Run `python3 <skill-dir>/scripts/<name>.py --help` (or `bash <skill-dir>/scripts/github_setup.sh --help`) to see options.
`infisical_seed.py` and `portainer_stack.py` use subcommands: their global
options (`--env-file`, `--endpoint-id`, `--insecure`) go **before** the
subcommand, or argparse rejects them.

**Operator machine prerequisites:** `python3`, `bash`, `openssl`, `psql` on
PATH (phase 1 shells out to it), `gh` authenticated with admin on the repository
(phases 3–5), `git`, and `docker` with Buildx only for a manual image push
(`references/ghcr.md` § Manual first push). `docker network create` runs on
the Docker host, not necessarily your machine.

## Inputs the operator must supply

Collect every input **before** starting; ask in one batch rather than one at a
time. The authoritative list, with a comment per key, is
`<skill-dir>/assets/env.deploy.template`:

```bash
cp "<skill-dir>/assets/env.deploy.template" .env.deploy
git check-ignore -v .env.deploy   # must print a matching .gitignore rule
```

The user fills `.env.deploy` at the repo root; read values from there — never
inline them in a shell command, where they land in history and logs. Three
local files take part, all matched by `.env.*` in `.gitignore`:

| File | Written by | Holds |
| --- | --- | --- |
| `.env.deploy` | operator | inputs from the template |
| `.env.deploy.generated` | phases 1–2 | generated DB credentials and secrets |
| `.env.deploy.ci` | phase 3 (merge) | what `github_setup.sh` and the stack env read |

---

## Phase 0 — Preflight

Never provision blind. Verify every system answers before mutating any of them.

```bash
python3 "<skill-dir>/scripts/preflight.py" --env-file .env.deploy
```

It checks, and reports a table of pass/fail:

- Postgres reachable, credentials valid, server version, whether the target
  role/database already exist.
- Infisical reachable, machine identity authenticates, which projects it can see.
- Portainer reachable, token valid, which environment (endpoint) IDs exist,
  whether a stack with the target name already exists.
- GitHub: `gh auth status`, repo exists, Actions enabled, whether the
  `Production` environment exists.
- Repo: `docker-compose.prod.yml` present for each service, workflows present.

**Do not proceed past a failure.** Fix it or ask the user.

Record the Portainer `endpointId` from this output as `PORTAINER_ENDPOINT_ID`;
phase 4 needs it.

---

## Phase 1 — Provision the database

One role and one database per project, plus a **separate** database for
Directus if the backend stack includes it (it does by default in this repo).

```bash
python3 "<skill-dir>/scripts/provision_db.py" \
  --env-file .env.deploy \
  --name "$PROJECT_SLUG" \
  --with-directus \
  --dry-run
```

Review the emitted SQL with the user, then re-run without `--dry-run`.

The script generates a strong DSN-safe password, creates the role and database
idempotently, and applies the PostgreSQL 15+ schema grants that the naive
`GRANT ALL PRIVILEGES ON DATABASE` does **not** cover — without them migrations
fail with `permission denied for schema public`. See
`references/postgres.md` for the full rationale and the manual SQL if you
prefer to run it by hand.

It writes the generated credentials to `.env.deploy.generated` (gitignored) for
phase 2 to consume, and prints only the key names.

**Verify** before moving on:

```bash
python3 "<skill-dir>/scripts/provision_db.py" --env-file .env.deploy --name "$PROJECT_SLUG" --verify
```

---

## Phase 2 — Seed Infisical

One Infisical project per service (`<project>-backend`, `<project>-frontend`)
so a compromised frontend identity cannot read backend secrets.

In the commands below, `$PROJECT_SLUG`, `$BACKEND_PROJECT_ID`,
`$FRONTEND_PROJECT_ID`, `$PORTAINER_ENDPOINT_ID` and the `*_DEPLOYMENT_SERVICE`
names stand for the **non-secret** values in `.env.deploy`; substitute them or
export just those. `plan`/`apply` require an explicit `--project-id` — there is
no fallback, so a frontend seed can never land in the backend project.

1. If `BACKEND_PROJECT_ID`/`FRONTEND_PROJECT_ID` are blank, create the projects
   (go-ahead required), record the ids in `.env.deploy`, and grant the machine
   identity access to both:

   ```bash
   python3 "<skill-dir>/scripts/infisical_seed.py" --env-file .env.deploy \
     create-project --name "${PROJECT_SLUG}-backend"
   ```

2. Plan the backend from the repo's own `.env.example`, so nothing the app
   reads is missed:

   ```bash
   python3 "<skill-dir>/scripts/infisical_seed.py" --env-file .env.deploy plan \
     --template backend/.env.example \
     --overrides .env.deploy.generated \
     --project-id "$BACKEND_PROJECT_ID" \
     --environment prod
   ```

   `plan` prints key, source (override / operator / derived / template /
   generated / **MISSING**) and status against Infisical. Never apply a plan
   containing `MISSING` values without walking the user through each one;
   those are the settings only a human can supply (OAuth client IDs, SMTP
   credentials, S3 keys, `REDIS_HOST`/`REDIS_PASSWORD` and
   `RABBITMQ_HOST`/`RABBITMQ_USER`/`RABBITMQ_PASSWORD` — the production compose
   files ship no Valkey or RabbitMQ, and the backend refuses to start in
   production without `REDIS_PASSWORD` and a non-default `RABBITMQ_PASSWORD`). Put the answers in `.env.deploy`
   under the template's application block and re-plan.

3. Apply once the plan is clean — same arguments, subcommand `apply`:

   ```bash
   python3 "<skill-dir>/scripts/infisical_seed.py" --env-file .env.deploy apply \
     --template backend/.env.example --overrides .env.deploy.generated \
     --project-id "$BACKEND_PROJECT_ID" --environment prod
   ```

   Generated values (including `ADMIN_API_KEY`) are persisted to
   `.env.deploy.generated` so a re-run does not rotate them.

4. The frontend's `BACKEND_API_KEY` must equal the backend's `ADMIN_API_KEY`.
   The script would otherwise generate an independent value, so copy it as an
   override first (nothing is printed), then plan and apply the frontend:

   ```bash
   grep -q '^BACKEND_API_KEY=.' .env.deploy.generated || \
     grep -E '^ADMIN_API_KEY=.' .env.deploy.generated \
       | sed 's/^ADMIN_API_KEY=/BACKEND_API_KEY=/' >> .env.deploy.generated

   python3 "<skill-dir>/scripts/infisical_seed.py" --env-file .env.deploy plan \
     --template frontend/.env.example --overrides .env.deploy.generated \
     --project-id "$FRONTEND_PROJECT_ID" --environment prod
   # then the same command with `apply`
   ```

5. The Directus `ADMIN_SECRET`/`ADMIN_PASSWORD` live in the backend stack env,
   not Infisical, and no script generates them. Write them without printing:

   ```bash
   for k in ADMIN_SECRET ADMIN_PASSWORD; do
     grep -q "^$k=." .env.deploy.generated || \
       printf '%s=%s\n' "$k" "$(openssl rand -hex 32)" >> .env.deploy.generated
   done
   ```

6. Enforce the cross-service invariants listed in `references/env-vars.md`
   (`ADMIN_API_KEY` == `BACKEND_API_KEY`, CORS origins, redirect URIs). `check`
   reads both project ids from the env file:

   ```bash
   python3 "<skill-dir>/scripts/infisical_seed.py" --env-file .env.deploy check --environment prod
   ```

API details, auth flow, and the CLI equivalents are in
`references/infisical.md`.

---

## Phase 3 — Configure the GitHub environments

Do this **before** the first image. `.github/workflows/build_backend.yml` and
`build_frontend.yml` have **no `workflow_dispatch`**: they run on
`workflow_run` after the `Code Quality` workflow completes successfully for a
**push** to `main` or `dev`. They name the image from
`vars.BACKEND_REPOSITORY_URI`/`vars.FRONTEND_REPOSITORY_URI` and read the
stack name, compose path and bootstrap values from the same environment, so a
push before this phase builds nothing useful. The environment is selected from
the triggering branch, so configure **both** `Production` and `Development`:

```yaml
environment: ${{ github.event.workflow_run.head_branch == 'main' && 'Production' || 'Development' }}
```

`github_setup.sh` reads **one** env file, and the first line for a key wins
even when empty. Merge the generated values in front of the operator inputs:

```bash
(umask 077; cat .env.deploy.generated .env.deploy > .env.deploy.ci)
```

Run for each environment you deploy to (go-ahead required):

```bash
bash "<skill-dir>/scripts/github_setup.sh" --env-file .env.deploy.ci --environment Production --dry-run
bash "<skill-dir>/scripts/github_setup.sh" --env-file .env.deploy.ci --environment Production

bash "<skill-dir>/scripts/github_setup.sh" --env-file .env.deploy.ci --environment Development --dry-run
bash "<skill-dir>/scripts/github_setup.sh" --env-file .env.deploy.ci --environment Development
```

It creates the environment if absent (`gh secret set --env` 404s otherwise),
then sets 16 variables and 8 secrets — the exact list is in
`references/env-vars.md` § Tier 3. Values are piped via stdin, never passed as
arguments where they would appear in the process table. Secret values are
never printed, only their length.

Then audit:

```bash
bash "<skill-dir>/scripts/github_setup.sh" --env-file .env.deploy.ci --environment Production --audit
```

The audit extracts every `${{ vars.X }}` and `${{ secrets.X }}` from the deploy
workflows and reports any that is not configured — plus anything configured
that no workflow reads.

> **Why the audit matters:** an unset `vars.*` expands to an **empty string**
> in Actions, not an error. The deploy step then targets a stack named `""`,
> matches nothing, and either creates a stray stack or reports success having
> changed nothing.

Two things need a judgement call with the user rather than silent dead
configuration: the `CF_ACCESS_*` pair (stored, but not passed to the Portainer
step unless you add a `headers:` input — `references/env-vars.md` § Two names
that need a decision), and the deploy step's missing `endpoint:` input (the
action then uses the **first** Portainer endpoint — wrong on multi-environment
Portainer; `references/portainer.md` § The community GitHub Action).

> **Note:** In this template repository the deploy steps are guarded by
> `if: ${{ github.repository != 'Llamitai/wise' }}`, so they no-op here and run
> only in projects generated from the template. If you are testing in the
> template itself, that guard is why nothing deploys.

---

## Phase 4 — Publish the first image and create the stacks

**Prerequisite:** `backend/docker-compose.prod.yml` attaches to an external
network named `shared-network`. It must already exist on the Docker host:

```bash
docker network create shared-network   # run on the Docker host, once
```

`frontend/docker-compose.prod.yml` joins no shared network; see
`references/env-vars.md` § Frontend project for what that means for
`BACKEND_API_HOST`.

Each `*_REPOSITORY_URI` must equal the `image:` in the matching
`docker-compose.prod.yml` (without the tag), or CI pushes an image the stack
never pulls. Stacks are created from the **Git repository**, not an uploaded
compose file, so redeploys pull the current compose from the branch.

**Path A — CI (default; proves the pipeline).** Get an explicit go-ahead first:
the next push to `main` runs `Code Quality`, then both `Build & Deploy`
workflows build, push to GHCR and — in generated projects — **create or
update** the Portainer stacks named `*_DEPLOYMENT_SERVICE` with the env from
Phase 3. Push (an empty commit is enough, with the user's approval) and watch:

```bash
gh run list --workflow "Build & Deploy / Backend" --limit 1
gh run watch <run-id>
```

**Path B — review the stack before CI touches it.** Push a first image by hand
(`references/ghcr.md` § Manual first push), then build the stack env files from
`.env.deploy.ci` without printing them:

```bash
(
  umask 077
  get() { grep -E "^$1=.+" .env.deploy.ci | head -n1 | cut -d= -f2-; }
  boot="INFISICAL_API_URL INFISICAL_SECRET_ENV INFISICAL_MACHINE_CLIENT_ID INFISICAL_MACHINE_CLIENT_SECRET"
  admin="ADMIN_SECRET ADMIN_EMAIL ADMIN_PASSWORD ADMIN_DB_HOST ADMIN_DB_DATABASE ADMIN_DB_USER ADMIN_DB_PASSWORD ADMIN_PUBLIC_URL"
  { echo "PROJECT_ID=$(get BACKEND_PROJECT_ID)"; for k in $boot $admin; do echo "$k=$(get "$k")"; done; } > .env.deploy.stack.backend
  { echo "PROJECT_ID=$(get FRONTEND_PROJECT_ID)"; for k in $boot; do echo "$k=$(get "$k")"; done; } > .env.deploy.stack.frontend
)
```

Then create each stack under the **same name** CI will target, dry-run first:

```bash
python3 "<skill-dir>/scripts/portainer_stack.py" \
  --env-file .env.deploy --endpoint-id "$PORTAINER_ENDPOINT_ID" \
  create \
  --name "$BACKEND_DEPLOYMENT_SERVICE" \
  --repo "https://github.com/$GITHUB_REPOSITORY" \
  --ref refs/heads/main \
  --compose backend/docker-compose.prod.yml \
  --stack-env .env.deploy.stack.backend \
  --dry-run            # add --private-repo for a private repository
```

Review the dry-run payload (secrets redacted), then apply without `--dry-run`.
Repeat with `frontend/docker-compose.prod.yml` and `.env.deploy.stack.frontend`.
Stack env files hold only tier-2 bootstrap values plus the backend's Directus
block (`references/env-vars.md` § Tier 2); anything from
`backend/.env.example` there is the classic mistake — move it to Infisical.
Later CI deploys **replace** the stack env with their `env_data`, so GitHub
environments stay the durable source.

**After either path**, confirm:

- The package exists at `ghcr.io/<owner>/<project>-api-prod` and is **linked
  to the repository** (via the `org.opencontainers.image.source` label).
- The Portainer host can pull it. GHCR packages are **private by default**;
  either make the package public or add registry credentials on the Docker
  host. `references/ghcr.md` § Pulling a private image covers both. This is the most
  common silent failure: the stack deploys, then the container never starts
  because the host gets `denied`.
- The containers are healthy:

  ```bash
  python3 "<skill-dir>/scripts/portainer_stack.py" \
    --env-file .env.deploy --endpoint-id "$PORTAINER_ENDPOINT_ID" \
    status --name "$BACKEND_DEPLOYMENT_SERVICE"
  ```

If a container is restarting, get its logs through the same script
(`... logs --name "$BACKEND_DEPLOYMENT_SERVICE" --service api --tail 200`)
before changing anything. The usual causes are in § Gotchas.

---

## Phase 5 — Verify the loop closes

The deploy is not done until an ordinary push deploys itself.

1. With the user's explicit go-ahead (as in Path A), push a trivial change to
   `main`. `Code Quality` has no path filter, so
   every push to `main` runs it and, on success, **both** `Build & Deploy`
   workflows.
2. `gh run watch` — `Code Quality`, then build, push, and the Portainer deploy
   step of each service must all pass.
3. Confirm the running image tag advanced:

   ```bash
   python3 "<skill-dir>/scripts/portainer_stack.py" \
     --env-file .env.deploy --endpoint-id "$PORTAINER_ENDPOINT_ID" \
     status --name "$BACKEND_DEPLOYMENT_SERVICE"
   ```

   The reported image tag must equal the new commit's `sha-<short>`.
4. Hit the public URLs: `/api/py/health` (liveness) and `/api/py/health/ready`
   (database and Redis), the frontend root, and one
   authenticated round trip through the BFF (proves the
   `ADMIN_API_KEY`/`BACKEND_API_KEY` pair matches).

Only after step 4 report the deployment as complete.

---

## Rollback

Read [references/rollback.md](references/rollback.md) before rolling back. Rolling
back the **image** does not roll back **secrets** or **migrations**; say so
explicitly when the bad deploy changed either.

---

## Gotchas

Symptoms, their most likely cause and where to look.

| Symptom | Most likely cause | Where to look |
| --- | --- | --- |
| Container restart-loops immediately | Infisical login failed — wrong `PROJECT_ID`, `INFISICAL_SECRET_ENV`, or machine identity lacks project access | `references/infisical.md` § Troubleshooting |
| `denied` / `unauthorized` pulling image | GHCR package private, host not authenticated | `references/ghcr.md` § Pulling a private image |
| `permission denied for schema public` | PostgreSQL 15+ grants missing | `references/postgres.md` § The grant you actually need |
| Stack creates but no containers | `shared-network` missing on the host | Phase 4 prerequisite |
| Deploy step succeeds, nothing changes | Empty `vars.*DEPLOYMENT_SERVICE` — targeted a stack name that does not exist | Phase 3 audit |
| `Build & Deploy` never starts | `Code Quality` failed, or the run was not a `push` to `main`/`dev` (no `workflow_dispatch`) | Phase 3 |
| Backend exits: `Missing required production secret(s): REDIS_PASSWORD` | Valkey not seeded; prod compose ships no Valkey | `references/env-vars.md` § Backend project |
| API or worker exits at startup with an AMQP connection/authentication error | RabbitMQ unreachable from `shared-network` or `RABBITMQ_*` wrong; prod compose ships no broker | `references/env-vars.md` § Backend project |
| CI deployed to the wrong Portainer host | Deploy step has no `endpoint:` input — first endpoint wins | `references/portainer.md` § The community GitHub Action |
| Portainer call returns HTML, or 401/403 from CI only | Behind Cloudflare Access without service-token headers | `references/ghcr.md` § Cloudflare Access |
| Redeploy wiped the stack's variables | `env` omitted from `/git/redeploy` — the API applies zero values | `references/portainer.md` § The env-wipe trap |
| App boots but every BFF call 401s | `ADMIN_API_KEY` != `BACKEND_API_KEY` | `references/env-vars.md` § Cross-service invariants |
| Google login redirect mismatch | `GOOGLE_REDIRECT_URI` not registered in Google Cloud | `references/env-vars.md` |
| Infisical CLI errors on an API path | CLI version pinned in `backend/Dockerfile` (`INFISICAL_CLI_VERSION`) is mismatched with the self-hosted server | `references/infisical.md` § Troubleshooting |

## Reference index

| File | Contents |
| --- | --- |
| `references/env-vars.md` | The three variable tiers, full catalog, cross-service invariants |
| `references/postgres.md` | Provisioning SQL, PG15+ grants, idempotency, rollback |
| `references/infisical.md` | Machine identity auth, secret CRUD API, CLI, runtime injection |
| `references/portainer.md` | API auth, endpoints, git-stack create/redeploy, webhooks |
| `references/ghcr.md` | Build/push from Actions, SHA pinning, provenance/SBOM, manual first push, package visibility, private pulls, `gh` config |
| `references/rollback.md` | Rollback workflow, known-good tag and digest lookup, compose-ref and env gotchas |
| `assets/env.deploy.template` | Operator input template |
