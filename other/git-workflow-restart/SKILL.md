---
name: git-workflow-restart
kind: pattern
rule: deploy-flow
description: Pattern of rule deploy-flow. Load for a manual production restart — after editing .env.prod, when investigating a rollout, when starting a container on the server. Ready-made commands with the image tag by sha and what to check the result against. Migrations — pattern git-workflow-migration.
---
<!-- rt-kit v0.34.0 · patterns/git-workflow-restart.md · 5d54f9ea612d · правится надстройкой, не здесь -->

# A manual production restart

Pattern of the rule `deploy-flow`. What must be true meanwhile — the law
`docs/constitution/delivery.md`.

## When to use

- `.env.prod` was edited, and the container must be brought up again.
- It is being analysed what exactly is rolled out now.
- A container is brought up on the server by hand, past the rollout by merge.

## The command must carry the sha

`.github/workflows/deploy.yml` rolls out images by the commit sha. Without the variable
`docker compose` substitutes the default `latest`, and `latest` in the registry lags behind the
main branch — production silently rolls back to the old image and keeps answering:

```bash
IMAGE_TAG='<sha>' docker compose -f docker-compose.prod.yml --env-file .env.prod pull migrate api ssr web
IMAGE_TAG='<sha>' docker compose -f docker-compose.prod.yml --env-file .env.prod up -d --no-build --remove-orphans
```

## The sha is taken before the restart

From the rolled-out container or from the last merge into the main branch:

```bash
docker inspect <контейнер> --format '{{.Config.Image}}'
```

## The check goes by the log, not by the response code

A substituted image is visible only by the missing lines of the new code: the `startup` digest
with `integrations` disappears from the logs, while `API is running` stays in place. After the
restart — the same `inspect` and the presence of the expected lines in the log.

## Rollback: the same call with the previous sha

A rollback is not a separate mechanism but the same startup by sha, only taken one step back. The
previous sha is taken from the registry, where the cleanup keeps the last three — there is no
rollback deeper:

```bash
docker image ls '<реестр>/<образ>' --format '{{.Tag}}\t{{.CreatedAt}}' | sort -k2 -r | head -3
IMAGE_TAG='<прежний sha>' docker compose -f docker-compose.prod.yml --env-file .env.prod up -d --no-build
```

A rollback returns the previous image, but not the previous storage schema: a migration that
left with the new version stays applied, and the previous image works with the changed schema.
That is why a schema edit is split into compatible and incompatible — the migration pattern.

A rolled-back production does not converge with the main branch at once: main carries an edit
that production no longer has. By a work queue line this is not visible at all, and it is named
to the owner in words, together with the sha rolled back to.

## Common misses

- The conclusion "production is alive, so it rolled out" — the response code does not show a
  substituted image.
- Environment variables, secrets and name records are set **before** the merge: the merge rolls
  out at once, and a branch that depends on a new variable lands on production before the
  variable is created.
- Entering the server over ssh in the automatic mode is cut by a rule — the normal mode is
  needed.
