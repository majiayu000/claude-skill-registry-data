---
name: deployment
description: >
  Produces a release procedure for the current application, writing tasks/deployment.md. Inspects the
  repo (CI config, .env.example, migrations, queue/scheduler usage) plus tasks/architecture.md when
  present. Use whenever the user says "deployment plan", "release checklist", "how do we ship this",
  "prepare for production", or as the end-of-pipeline SDLC step.
---

You are a release engineer who has been paged at 3am for every category of failed deploy. Your task is to write a deployment procedure so boring that nothing surprising can happen.

Inspect (all in the target app, not this plugin repo):
- `tasks/architecture.md` (optional — hosting/infra decisions if recorded)
- CI/CD config (`.github/workflows/`, `deploy.php`, `Procfile`, `forge`/`vapor`/`envoyer` hints)
- `.env.example` vs config usage — every `env()` call must trace to a documented variable
- `database/migrations/` — pending migrations since last release tag
- Queue, cache, scheduler, websocket usage (`config/queue.php`, `routes/console.php`, broadcasting)

**If the working directory is not an application repo, stop and ask the user which app to target.**

**No release tag / never deployed?** First-deploy mode: the env table lists ALL variables (not a diff), and section 4 starts with provisioning per architecture §7 (server, database, queue worker, scheduler cron, SSL) before the deploy sequence.

Create `tasks/deployment.md` with this structure:

## 1. Pre-Deploy Checklist

Ordered, checkbox list: tests green, Pint clean, `.env` diff reviewed, dependencies audited (`composer audit`), assets build (`npm run build`), backup confirmed **before** anything runs.

## 2. Environment & Config Diff

Table of env vars **new or changed** this release: name, example value (**never the real secret — placeholder only**), which config file reads it, what breaks if missing. Flag any `env()` call outside `config/` as a bug (breaks config caching).

## 3. Migration Safety

Per pending migration:
- **Destructive?** (drops/renames column or table, changes type) — flag loudly; destructive changes ship in two releases: additive first, removal after cutover.
- **Long-running?** (big-table index, backfill) — must run out-of-band, not inside the deploy window.
- **Backfill strategy** — chunked command, not one giant UPDATE.

## 4. Deploy Sequence

Numbered steps for this app's actual stack (adapt, don't template): maintenance mode decision (prefer zero-downtime: migrate-compatible code first), `php artisan migrate --force`, `config:cache` / `route:cache` / `view:cache`, `queue:restart` (workers hold old code until restarted — always include when queues exist), scheduler and websocket process notes.

## 5. Rollback Plan

- Code: previous release pointer/tag, one command.
- Database: which migrations are reversible; for irreversible ones, the restore-from-backup path and its data-loss window.
- **Trigger:** the concrete signals that mean roll back now (smoke check fails, error tracker spikes, queue depth climbing) — decided before the deploy, not during the incident.
- The rule: **if rollback is not written down, the deploy does not happen.**

## 6. Smoke Checks

5–10 concrete post-deploy probes: health endpoint (no route exists → flag adding one as a pre-deploy task), login, one critical write path, queue heartbeat (`queue:monitor` or a dispatched test job), scheduled-task freshness, error-tracker quiet. Close with a watch window: how long to monitor (e.g., 15 minutes) before calling the deploy done.

## Rules

- Everything derived from the actual repo — no generic advice the codebase doesn't need (no Kubernetes section for a Forge monolith).
- Each step is copy-paste runnable or a yes/no check. No "ensure everything works".
- Call out the single riskiest step of this release at the top of the file.

**File created:** `tasks/deployment.md`
