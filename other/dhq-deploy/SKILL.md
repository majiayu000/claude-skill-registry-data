---
name: dhq-deploy
description: Deploy code with the DeployHQ CLI (dhq), and diagnose pushes that don't deploy (auto-deploy, webhook). Use for "deploy to production", "trigger a deployment", "ship via DeployHQ", "push didn't deploy", "dhq 404". Not for DB/asset pushes (server-deploy).
---

# DeployHQ CLI Deployment

## Prerequisites

- `dhq` CLI installed and authenticated (`dhq auth status` / `dhq doctor`)
- Know the **project permalink** — the short slug visible in the DeployHQ URL, e.g. `my-project`. This is NOT the UUID.

## Critical: permalink vs UUID

`dhq deploy` and most commands require the **project permalink** (a short slug), not the UUID. Using a UUID returns a 404 from the DeployHQ API. Always confirm with `dhq projects list` if unsure.

## Find project and server identifiers

```bash
# List all projects — shows permalink in the first column
dhq projects list

# List servers for a project
dhq servers list -p <permalink>
```

## Deploy

### Simplest case (single project, single server, latest commit)

```bash
dhq deploy --wait
```

`--wait` streams the deployment log until it completes or fails. It cannot be combined with `--dry-run`. Confirm the final status with `dhq deployments show` (below) rather than relying on the exit code.

### Explicit: specific project, server, and revision

```bash
dhq deploy -p <permalink> -s <server-identifier> -r <git-sha> --wait
```

### Preview without deploying

```bash
dhq deploy -p <permalink> --dry-run
```

## Watch an existing deployment

If a deployment was triggered without `--wait`:

```bash
dhq deployments watch <deployment-id> -p <permalink>
```

## Common flags

| Flag | Short | Meaning |
|------|-------|---------|
| `--project` | `-p` | Project permalink |
| `--server` | `-s` | Server or group identifier |
| `--revision` | `-r` | End revision (default: latest) |
| `--start-revision` | | Start revision (default: the server's last deployed commit) |
| `--branch` | `-b` | Branch to deploy |
| `--wait` | `-w` | Stream log and block until done |
| `--dry-run` | | Preview only, no deployment created |
| `--full` | | Deploy entire branch from first commit |
| `--timeout` | | Seconds before `--wait` gives up (0 = none) |

## Check result and duration

To inspect status and duration, or retrieve the deployment ID for further commands:

```bash
# Most recent deployments with status and duration
dhq deployments list -p <permalink>

# Full details for a specific deployment
dhq deployments show <deployment-id> -p <permalink>

# Machine-readable (status, duration_seconds, etc.)
dhq deployments show <deployment-id> -p <permalink> --json
```

## Auto Deploy on push

DeployHQ's own **Auto Deploy** is a per-server toggle, independent of the CLI's manual
`dhq deploy` — it does not require `dhq` to be running anywhere. Verify or enable it directly:

```bash
# Show each server's auto-deploy status + preferred branch, and the account's deploy webhook URL
dhq auto-deploys list -p <permalink>

# Enable (or --disable) auto-deploy for a specific server
dhq auto-deploys enable -p <permalink> --server <server-identifier>
```

`dhq auto-deploys list` returns each deployable with `auto_deploy: true|false` and its
`preferred_branch` — auto-deploy only fires for a push to *that* server's configured branch,
not any push to the repo. The same response also includes the account's `webhook_url`
(`https://<account>.deployhq.com/deploy/<permalink>/<token>`) — **this is the actual trigger**:
DeployHQ deploys when that webhook receives a push notification, not by polling the repo itself.
If the project's repository was added to DeployHQ via its native GitHub/GitLab/Bitbucket
integration, the webhook is normally auto-registered; if the repo uses a different connection
method (e.g. manual git URL, SSH-only), confirm the webhook is actually configured on the git
host's side (repo Settings → Webhooks) and points at that same URL.

If push-triggered deploys aren't achievable this way for a given host/CI setup, trigger `dhq
deploy` explicitly from a CI step instead, e.g. a GitHub Actions step on push to `master`:

```yaml
- name: Deploy via DeployHQ
  run: dhq deploy -p <permalink> -s <server-identifier> --wait
  env:
    DEPLOYHQ_ACCOUNT: <subdomain>
    DEPLOYHQ_EMAIL: ${{ secrets.DEPLOYHQ_EMAIL }}
    DEPLOYHQ_API_KEY: ${{ secrets.DEPLOYHQ_API_KEY }}
```

## Post-deploy

DeployHQ runs any SSH commands configured on the server (e.g. `composer install`, `sake dev/build`, OPcache flush) automatically after the file transfer. No manual post-deploy steps are needed unless something is not in the server's SSH command list.

Before deploying, check for unpushed commits (`git log origin/<branch>..<branch> --oneline` must be empty; DeployHQ deploys from the git remote). For the `composer install` stale-vendor, de-tracked-file deletion and Ploi database-host caveats, see [`server-deploy`](../server-deploy/SKILL.md#deployhq--ploi-caveats).

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `404 Not Found` on deploy | You used the project UUID instead of the permalink. Run `dhq projects list` and use the slug. |
| No servers found | Run `dhq servers list -p <permalink>` to confirm identifiers. |
| Deploy queued but not running | Check for a running deployment: `dhq deployments list -p <permalink>`. DeployHQ queues if one is already in progress. |
| Pushed to a branch, no deployment appeared at all | Distinct from the row above — no deploy was ever queued. Run `dhq auto-deploys list -p <permalink>` to confirm the target server has `auto_deploy: true` for the branch pushed to (a mismatched `preferred_branch` silently means no trigger). If auto-deploy is correctly enabled, the repo's webhook to DeployHQ's `webhook_url` may not be configured or firing — check the git host's webhook delivery log (repo Settings → Webhooks) for a failed or missing delivery. |
| Auth failure | Run `dhq auth status`, then `dhq doctor` to verify credentials and connectivity. |
