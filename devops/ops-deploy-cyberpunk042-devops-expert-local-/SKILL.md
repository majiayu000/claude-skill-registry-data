---
name: ops-deploy
description: Execute a deployment with pre-flight gates, the deploy itself, post-deploy smoke tests, and a recorded rollback contract. For AICP this means `docker compose up` of LocalAI + activating the right profile (`make profile-use PROFILE=<name>`) + verifying health (`aicp --check`); for sister fleet projects, it's their compose stack + their post-deploy probe. Distinct from `config-deploy` (prepares the config a deployment will USE) and `ops-rollback` (executes a recorded rollback). Loads when the operator says "deploy", "ship it", "push to prod/staging", "roll out X", "release the change".
argument-hint: [environment: dev|staging|prod]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: high
---

# ops-deploy

The deployment-execution skill. It runs the gates (tests + lint + branch + uncommitted check), executes the deploy command for the target environment, smoke-tests the result, and records the rollback contract (previous version + how to roll back). Distinct from `config-deploy` which prepares the config the deploy uses — this skill is the act of deploying.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: operator says "deploy", "ship it", "push to staging/prod", "roll out X", "release the new version", "restart with the new image".
- **Stage transition**: a feature is at `feature-test` → done and the operator wants the working build out. Or a config change is at `config-deploy` → ready and needs to be activated.
- **Recovery deploy**: re-deploying after a fix, after `ops-incident` resolved root cause, or after `ops-rollback` rolled back and a corrected version is ready.

Do NOT load when:

- The deploy already failed and the system is degraded — load `ops-incident` (active incident response).
- The current deploy needs to be reverted — load `ops-rollback`.
- Routine non-deploy maintenance (cert renewal, dep update, log rotation) — load `ops-maintenance`.
- Setting up the CI/CD pipeline that calls this skill — load `foundation-ci`.
- Choosing which profile/config the deploy should use — load `config-deploy` first, then this skill.

## Operations

This skill has 4 named operations. Execute strictly in order — each is a gate for the next.

### Operation 1: Pre-flight gates

**Trigger**: skill loaded; operator named the target environment (dev / staging / prod).

**Process**:

1. Identify the target environment and its compose file or deploy command:
   ```bash
   ls docker-compose.yaml docker-compose.<env>.yaml 2>/dev/null
   grep -E "^deploy-<env>:" Makefile 2>/dev/null
   ```
   Capture: which compose / Make target this deploy uses.
2. Branch + commit cleanliness:
   ```bash
   git status --porcelain   # MUST be empty for staging/prod
   git rev-parse --abbrev-ref HEAD   # confirm correct branch (main for prod typically)
   ```
3. Tests + lint (skip ONLY for emergency hotfix with explicit operator override):
   ```bash
   make test 2>&1 | tail -5    # or pytest -q
   make lint 2>&1 | tail -5    # or ruff check .
   ```
4. Confirm the target environment's profile is the intended one:
   ```bash
   .venv/bin/aicp --profile-show 2>/dev/null
   # for prod: should be `default` (audit-safe pinned K2.6) or operator's prod-named profile
   # for dev: usually `personal` or `dev`
   ```
5. For prod deploys: confirm operator has done `git pull --ff-only` against origin/main and there's no divergence.
6. Record the CURRENT (pre-deploy) version + commit SHA — this is the rollback target:
   ```bash
   git rev-parse --short HEAD > /tmp/predeploy-sha-<env>.txt
   docker compose ps --format "{{.Image}}" | sort -u > /tmp/predeploy-images-<env>.txt
   ```

**Quality bar (Operation 1 done when)**:

- [ ] Target compose file / Make target identified.
- [ ] `git status --porcelain` empty (or operator explicitly authorized dirty deploy with reason).
- [ ] On the correct branch for the target environment.
- [ ] Tests + lint passed in this run (not "they passed yesterday").
- [ ] Active profile matches target environment expectation.
- [ ] Rollback target (commit SHA + image tags) recorded to `/tmp/predeploy-*-<env>.txt`.

### Operation 2: Execute the deploy

**Trigger**: Operation 1 gates green.

**Process**:

1. Build artifact if needed:
   ```bash
   docker compose build 2>&1 | tail -20
   # or: make build-<env>
   ```
2. Pull latest images for unchanged services:
   ```bash
   docker compose pull 2>&1 | tail -10
   ```
3. Deploy — use the LEAST disruptive command that achieves the change:
   ```bash
   # Preferred: rolling restart only the changed services
   docker compose up -d --no-deps <service-name>
   # If services depend on each other or env vars changed:
   docker compose up -d
   # If full reload needed (compose file restructure, network reset):
   docker compose down && docker compose up -d
   ```
4. For AICP specifically: activate the target profile if a profile change is part of this deploy:
   ```bash
   make profile-use PROFILE=<env-profile>
   ```
5. Watch logs for the first 30 seconds — catch crash-on-boot:
   ```bash
   docker compose logs -f --tail 50 --since 30s &
   sleep 30; kill $!
   ```

**Quality bar (Operation 2 done when)**:

- [ ] Deploy command exited 0.
- [ ] No service in `Restarting` state (verified by `docker compose ps`).
- [ ] No FATAL or "Exited" entries in first-30s logs.
- [ ] If profile changed, `aicp --profile-show` confirms new profile active.
- [ ] Least-disruptive deploy mode chosen (didn't `down`+`up` if `up -d` was sufficient).

### Operation 3: Smoke test the running system

**Trigger**: Operation 2 deploy completed.

**Process**:

1. Container health snapshot:
   ```bash
   docker compose ps --format json | jq -r '.[] | "\(.Name): \(.State) (\(.Health // "no-healthcheck"))"'
   ```
   Every service must be `running (healthy)` or `running (no-healthcheck)`.
2. AICP-specific health probe:
   ```bash
   .venv/bin/aicp --check 2>&1 | head -20
   curl -sS -m 5 http://localhost:8090/readyz || echo "LocalAI not ready"
   ```
3. Golden-path inference probe (proves the deployment actually serves):
   ```bash
   .venv/bin/aicp --backend local --prompt "say ok" 2>&1 | tail -5
   ```
4. Metrics endpoint reachable (if monitoring is part of this deployment):
   ```bash
   curl -sS -m 5 http://localhost:9101/metrics | head -3
   curl -sS -m 5 http://localhost:8090/metrics | head -3
   ```
5. Sister-project smoke probes if this skill is invoked from openfleet/dspd/nnrt — use that project's documented health endpoint, not AICP's.

**Quality bar (Operation 3 done when)**:

- [ ] All services `running (healthy)`.
- [ ] `aicp --check` exits 0 with backend chain healthy.
- [ ] Golden-path inference returns a non-empty response within 30s.
- [ ] Metrics endpoints respond 200 (if monitoring stack is part of this deploy).
- [ ] If ANY probe fails, do NOT mark deploy successful — proceed to Operation 4 rollback path.

### Operation 4: Record outcome + rollback contract

**Trigger**: Operation 3 smoke complete (success OR failure).

**Process**:

1. **On success** — record the deployment:
   ```bash
   echo "$(date -u +%FT%TZ) deploy=<env> sha=$(git rev-parse --short HEAD) status=ok by=$(whoami)" \
     >> docs/DEPLOY-LOG.md
   ```
   Append the rollback contract: previous SHA from `/tmp/predeploy-sha-<env>.txt` + the exact rollback command (e.g., `git checkout <prev-sha> && make profile-use PROFILE=<prev> && docker compose up -d`).
2. **On smoke failure** — execute rollback IMMEDIATELY (don't debug live in prod):
   ```bash
   git checkout "$(cat /tmp/predeploy-sha-<env>.txt)"
   docker compose up -d
   ```
   Then load `ops-rollback` to formalize the rollback record + load `ops-incident` to investigate root cause.
3. Update fleet visibility surfaces:
   - If openfleet is wired: post deploy outcome to Mission Control board (or note in standing-orders).
   - If ntfy is configured: send a deploy-success ping (`config/alerts.yaml` has the topic).
4. For prod deploys: monitor metrics for the first 5 minutes — circuit-breaker errors, latency spike, OOM. If anomaly emerges, roll back even if smoke passed.

**Quality bar (Operation 4 done when)**:

- [ ] `docs/DEPLOY-LOG.md` (or equivalent) updated with timestamp, env, SHA, status, deployer.
- [ ] Rollback contract is RECORDED, not implied — exact command listed.
- [ ] On failure: rollback executed; no half-deployed state lingering.
- [ ] On success: 5-min post-deploy metric watch noted (or explicitly skipped for dev).
- [ ] Fleet visibility surface updated (or "no fleet visibility wired" stated).

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Smoke test passes because it's checking the OLD container

`docker compose up -d` is slow on a large image; the smoke probe runs while the OLD container is still serving on the port. Probe returns 200, deploy declared successful. Five minutes later, the new container finishes coming up — and it's broken. Operator already moved on.

**The rule**: between Operation 2 and Operation 3, verify the container's `Started` timestamp is AFTER the `docker compose up -d` invocation. Use `docker inspect <container> -f '{{.State.StartedAt}}'` and compare to a timestamp captured before the up command. If the container hasn't actually restarted, the deploy didn't take effect — don't smoke-test ghost.

### Gotcha 2: Tests "passed yesterday" — running deploy without re-running them

Operator says "deploy". Skill skips the test gate because tests passed in CI yesterday. But the operator made a local change that didn't get pushed through CI. Deploy ships broken code. The CI badge says green; the actual code on the branch isn't.

**The rule**: Operation 1 step 3 runs tests + lint IN THIS SESSION. The fact that CI passed earlier is not evidence about the current commit's state. The cost of `make test` is small; the cost of a broken deploy is large.

### Gotcha 3: Pre-deploy SHA captured AFTER the deploy starts

Operation 1 forgets to capture rollback target before any deploy mutation. Deploy fails mid-flight; skill tries to roll back but the "previous SHA" is the half-deployed state, not the last-known-good. Rollback rolls back to broken.

**The rule**: rollback target capture (Operation 1 step 6) MUST happen before any deploy mutation in Operation 2. The captured SHA + image tags are the rollback contract — they are taken when the system is known-good. If the file is missing when rollback is needed, that's a process bug, not a runtime decision.

### Gotcha 4: Rolling restart hides config errors

`docker compose up -d --no-deps <service>` only restarts the named service; dependent services keep their old env vars. A change to a shared env file (or to `.env`) won't propagate until the dependents also restart. Smoke against the restarted service passes; the bug only shows when a dependent service tries to use the new env var.

**The rule**: if THIS deploy changed env vars, `.env`, a shared config, or a network/volume, the deploy mode must be `up -d` (no `--no-deps`) — let compose decide which dependents need restart. Reserve `--no-deps` for code-only changes to a single service. Operation 2 step 3 must check: did this commit touch `.env*`, `docker-compose*.yaml`, or shared config? If yes, no `--no-deps`.

### Gotcha 5: Prod deploy with a dirty working tree

`git status` shows uncommitted changes. Operator says "just deploy, I'll commit after". Skill obliges. The deployed artifact is built from a working state that exists nowhere in git history. When something breaks, the rollback target SHA is the last commit — but the running state was AHEAD of it. Rollback regresses changes that were never recorded.

**The rule**: for staging/prod, `git status --porcelain` MUST be empty. No exceptions for "small" or "I'll commit later". For dev environments, dirty deploys are allowed but the deploy log must explicitly note `dirty=true` so post-incident archaeology shows what was actually running. Reject prod-dirty even on operator override unless they paste a written reason that goes into the deploy log.

## Reference exemplars

The Extension Standards reference exemplars for skills are the second brain's `model-builder` and `wiki-agent` skills — see `~/devops-solutions-research-wiki/skills/`. This skill follows their structure: trigger phrases, multiple named operations, per-operation Process + Quality bar, Gotchas with detection + rule + reasoning.

## Domain context

This skill operates in the **backend-ai-platform-python** domain. AICP deployments are dominantly Docker-compose-based (LocalAI on `:8090`, optional Prometheus `:9090` + Grafana `:3000`, AICP own metrics on `:9101`). There is no traditional Kubernetes cluster — the deploy surface is a single host with optional second-host LocalAI for cluster peering (Stage 4, deferred). Profile activation is a first-class part of an AICP deploy: `make profile-use PROFILE=<name>` is often what makes a deploy meaningful, not a code change. For sister fleet projects (openfleet, dspd, nnrt), the compose stack and probes are theirs — this skill applies the same gating discipline against their commands.

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| ops-rollback | Revert a bad deploy to last known good | This skill executes a forward deploy with a rollback contract; `ops-rollback` invokes that contract |
| ops-incident | Active incident response (deploy broke prod) | Incident response is reactive + restorative; this skill is forward action with gates |
| ops-maintenance | Routine maintenance (deps, certs, cleanup) | Maintenance preserves; this skill changes |
| config-deploy | Prepare the config a deployment will use | Sets up the profile/env; this skill activates and ships |
| foundation-ci | Build the pipeline that invokes this skill | CI authors the pipeline; this skill is what the pipeline runs |
| openclaw-setup | Bootstrap OpenClaw fresh | First-time install vs subsequent deploys; this skill is for already-installed systems |
