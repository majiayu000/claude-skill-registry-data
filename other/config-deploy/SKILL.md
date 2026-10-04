---
name: config-deploy
description: Configure deployment-specific settings — pick the right AICP profile (`make profile-use PROFILE=<name>`), tune Docker compose envs (`CONTEXT_SIZE`, `LLAMACPP_PARALLEL`), set per-environment overrides (dev / staging / prod). Distinct from ops-deploy (executes the deployment with checks) — this skill prepares the configuration deployment will use. Loads when the operator says "configure for production" / "set deploy profile" / "tune docker for fleet" / "what config does X env need".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: medium
---

# config-deploy

Prepares the configuration that a deployment will use. AICP's deploy-time
config has 4 layers: the active **profile** (one of 9, picked via
`make profile-use`), **Docker compose envs** (`CONTEXT_SIZE`,
`LLAMACPP_PARALLEL`, etc., set via the profile or `.env`), **per-environment
overrides** (dev/staging/prod variations), and the **identity profile**
(per CLAUDE.md `## Identity Profile` — phase, scale).

This skill PICKS and TUNES the configuration. Different from `ops-deploy`
which EXECUTES the deployment (pre-flight, deploy, smoke test, rollback).
Different from `config-secrets` which manages secret values.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: operator says "configure for production", "set deploy profile", "tune docker for fleet", "what config does X env need", "switch to dual-gpu config", "prep for cluster deploy"
- **Pre-deployment**: about to ship to a target environment; pick + tune the profile first
- **Hardware change**: VRAM upgrade (8GB → 19GB) — reconfigure for the new capacity (dual-gpu profile becomes runnable)
- **Workload change**: AICP starts serving fleet (`fleet-light` profile) vs solo dev (`default`) — reconfigure per workload
- **Fleet integration**: AICP about to be exposed to fleet agents — reconfigure with `reliable` profile (circuit breaker + warmup + DLQ)
- **Cost optimization cycle**: tune profile parameters to push more requests local (reduces Claude tokens)

Do NOT load when:

- The deployment itself is being executed (load `ops-deploy` for the deploy run)
- Secrets need to be managed (load `config-secrets`)
- Feature flags need toggling (load `config-feature-flags`)
- General config is being set up greenfield (load `foundation-config`)
- Something broke in production (load `ops-incident` first)

## Operations

This skill has 4 named operations.

### Operation 1: Identify target environment + workload

**Trigger**: skill loaded; deployment context emerging.

**Process**:

1. Frame the target concretely:
   - **WHERE** runs AICP? Local dev machine / staging server / production fleet node / dual-GPU host
   - **WHO** consumes AICP? Solo dev / fleet agents / external MCP clients
   - **WHAT** workload? Interactive (low latency, low concurrency) / batch (higher latency OK, higher throughput) / heartbeat (minimal — fleet keep-alive only)
   - **HARDWARE** available? CPU only / single GPU 8GB / dual GPU 19GB / different
2. Map (target, workload, hardware) → AICP profile candidate per the 9 profiles documented in CLAUDE.md:

   | Workload | Hardware | Profile candidate |
   |----------|----------|-------------------|
   | Interactive solo dev | 8GB GPU | `default` or `fast` |
   | Heartbeat duty (fleet node) | 8GB GPU | `fleet-light` |
   | Architecture review (deep RAG) | 8GB GPU | `thorough` |
   | Code review batch | 8GB GPU | `code-review` |
   | Production fleet (reliability) | 8GB GPU | `reliable` |
   | Air-gapped / no cloud allowed | any | `offline` |
   | MoE inference (dual GPU) | 19GB+ | `dual-gpu` |
   | Deterministic eval | any | `benchmark` |
   | General balanced | 8GB GPU | `default` |

3. If no profile maps cleanly to the target, the answer is NOT "make a custom config" — the answer is either pick the closest profile + override specific fields OR (if persistent need) author a NEW profile in `config/profiles/<name>.yaml`. Picking a profile is the high-leverage decision; ad-hoc overrides drift.
4. Document the choice + rationale in `wiki/decisions/00_inbox/deploy-config-<env>-<date>.md` (type=decision — picking a profile is a decision).

**Quality bar (Operation 1 done when)**:

- [ ] Target framed concretely (where + who + what + hardware)
- [ ] Profile candidate selected from the 9 (or new-profile-needed flagged)
- [ ] Choice + rationale recorded in the decision page

### Operation 2: Apply the profile + verify resolution

**Trigger**: Operation 1 profile chosen.

**Process**:

1. Inspect the profile's resolved config (don't guess what it does — verify):

   ```bash
   make profile-show PROFILE=<chosen-profile>
   ```

   Note: backend chain, router thresholds, RAG depth, budget, cache settings, timeouts, circuit_breaker config, warmup config, DLQ config, Docker envs (CONTEXT_SIZE, LLAMACPP_PARALLEL, THREADS, MAX_ACTIVE_BACKENDS).

2. Compare against the target's needs from Operation 1. Any mismatch?
   - Profile's CONTEXT_SIZE smaller than the workload needs → override required (or pick a different profile)
   - Profile's failover chain includes claude but the env is offline → wrong profile (use `offline`)
   - Profile's circuit_breaker threshold too lax for production (default has threshold=5; reliable has threshold=2) → switch profiles
3. Apply the profile:

   ```bash
   make profile-use PROFILE=<chosen-profile>
   ```

   This writes `.env` + restarts Docker compose. Verify:

   ```bash
   cat .env | grep -E 'AICP_PROFILE|CONTEXT_SIZE|LLAMACPP_PARALLEL'
   docker compose ps  # confirm restart picked up new envs
   ```

4. For per-environment overrides that don't fit a profile (e.g., production needs `ntfy` URL set to a specific topic; profile shouldn't bake in that operational value):
   - User-level overrides go in `~/.aicp/config.yaml` (per-user, not committed)
   - Project-level overrides go in `<project>/.aicp/config.yaml`
   - One-off CLI: `aicp --config <path>`

5. Verify the resolved config matches expectations:

   ```bash
   aicp --check  # confirms required env vars + profile
   make profile-validate  # confirms profile YAML schemas
   ```

**Quality bar (Operation 2 done when)**:

- [ ] Profile's resolved config inspected (not assumed)
- [ ] Any mismatches with target needs resolved (re-pick OR override)
- [ ] Profile applied via `make profile-use`
- [ ] `.env` reflects the new profile
- [ ] Docker compose restarted; `docker compose ps` confirms healthy
- [ ] `aicp --check` + `make profile-validate` pass

### Operation 3: Smoke-test the deploy config

**Trigger**: Operation 2 config applied.

**Process**:

1. Run a representative request that exercises the config:
   - For interactive profiles: a quick chat completion with low latency expectation
   - For batch/thorough profiles: a longer reasoning task
   - For dual-gpu: a request that loads the 30B MoE model
   - For offline: a request that should NOT escalate to cloud (verify it stays local even on quality drop)

2. Check observability is reading the new config (if `monitoring-up`):

   ```bash
   curl -s localhost:9101/metrics | grep -E 'profile|circuit|backend' | head -10
   ```

3. Check the circuit breaker state per backend (especially after profile change — breakers reset):

   ```bash
   aicp --route "test" 2>&1 | tail -5
   ```

4. For production-target configs, run the reliability subset:
   - Trigger a failover (point a backend at a wrong URL temporarily) — verify the chain falls through
   - Trigger a DLQ retry — verify failed task lands in `~/.aicp/dlq/`
   - Restore the backend; verify recovery

5. If any smoke test fails: STOP. Don't deploy. Diagnose the config issue (Operation 1 or 2 mistake) before proceeding.

**Quality bar (Operation 3 done when)**:

- [ ] Representative request succeeds
- [ ] Observability reflects new config
- [ ] Circuit breaker state confirmed per backend
- [ ] For production: failover + DLQ tested end-to-end
- [ ] Any smoke test failure halts deploy (no proceeding with broken config)

### Operation 4: Document + commit + hand off to ops-deploy

**Trigger**: Operation 3 smoke-test passed.

**Process**:

1. Update the decision page from Operation 1 with the verified outcome:
   - Profile applied (with `make profile-show` snapshot)
   - Override files used (if any)
   - Smoke-test results (which requests + which thresholds confirmed)
2. Update `docs/runbooks/deploy.md` (create if missing) with the env-specific deploy config:
   - Target environment
   - Profile + any overrides
   - Smoke-test commands operator should run before traffic
3. Commit:
   - Profile choice → none (already committed in `config/profiles/`); if user picked a CUSTOM new profile, commit that YAML
   - Override files (if checked into the repo) → conventional commit
   - Decision page → `docs(deploy): config decision for <env>`
4. Hand off to `ops-deploy` skill for the actual deployment execution. ops-deploy will run pre-flight checks (test pass + lint pass + correct branch + uncommitted changes), then deploy, then smoke test, then offer rollback. This skill ENDS at "config ready"; ops-deploy STARTS at "deploy now."

**Quality bar (Operation 4 done when)**:

- [ ] Decision page captures the chosen config + verification
- [ ] Runbook updated with env-specific config
- [ ] Conventional commit applied
- [ ] Operator informed: "config ready; ops-deploy can take it from here"

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Picking a profile by name without inspecting it (cargo cult)

The temptation: "fleet-light sounds right for fleet" — apply it. But you didn't read what `fleet-light` actually contains. Maybe its primary model is `gemma4-e2b` (53 tok/s, 2.9GB) which is great for heartbeats but useless if your fleet workload includes complex reviews.

**Detection**: did Operation 2 step 1 actually run `make profile-show PROFILE=<name>` and READ the resolved settings?

**The rule**: profiles have descriptive names but the names are HEURISTICS, not guarantees. Always inspect the resolved config and verify it matches your workload needs.

### Gotcha 2: Hand-tuning Docker envs without updating the profile (drift)

The temptation: profile has `CONTEXT_SIZE=16384` but you need 32768 for one big request. Edit `.env` directly. Now `.env` and the profile's `.env` snippet disagree. Next `make profile-use` overwrites your edit.

**Detection**: `git diff .env` shows manual edits NOT explained by the active profile.

**The rule**: profiles are the source of truth. If you need `CONTEXT_SIZE=32768`, either pick a profile that has it OR author a new profile OR use a per-user `.aicp/config.yaml` override that takes precedence over `.env`. Never hand-edit `.env` for persistent settings.

### Gotcha 3: Deploying without smoke test (false confidence)

The temptation: profile applied, `aicp --check` passes, ship it. NO — `aicp --check` validates config presence, not config CORRECTNESS in this environment. A profile that runs cleanly on dev hardware may fail on production hardware (e.g., dual-gpu profile on a single-GPU host).

**Detection**: did Operation 3 actually run a representative request, or did you skip to Operation 4?

**The rule**: smoke-test before deploy. Even one passing request is more signal than `aicp --check` alone.

### Gotcha 4: Skipping the failover test for production configs (silent reliability gap)

The temptation: production deploy works for happy path; assume failover works because it's configured. NO — circuit breaker / DLQ / failover chain are EXACTLY the things that don't get exercised under happy path. They only matter under failure. You must inject a failure to verify they work.

**Detection**: did Operation 3 step 4 (failover + DLQ test) run for production-target configs?

**The rule**: production configs have a separate failover smoke test. Inject a failure (point a backend at the wrong URL, kill a container, set an invalid token), verify the failover chain catches it, restore, verify recovery.

### Gotcha 5: Picking `default` for everything (no-decision-as-decision)

The temptation: when uncertain, pick `default`. But `default` is a balanced profile — by definition, it's not optimal for any specific workload. Production fleet should be `reliable`. Heartbeat should be `fleet-light`. Air-gapped should be `offline`. Picking `default` everywhere defeats the profile system.

**Detection**: did you pick `default` because it matched your workload, or because you didn't want to think about it?

**The rule**: every deploy config picks a profile that maps to a real workload reason. `default` is the right choice ONLY for a balanced general-use deployment with no specific workload pattern. For everything else, justify the choice.

## Reference exemplars

Per Extension Standards, reference exemplars are the second brain's `model-builder` and `wiki-agent` skills. For the OUTPUT artifacts:

- **Real profiles**: see [config/profiles/](../../../config/profiles/) for the 9 profiles this skill picks among
- **Real profile system**: see [aicp/core/profiles.py](../../../aicp/core/profiles.py) for loader + validator + diff engine + `extends:` inheritance
- **Sibling decision exemplar**: [4-tier router with profiles](../../../wiki/decisions/01_drafts/4-tier-router-with-profiles-over-hardcoded-routing.md) for the architecture this skill operates within
- **Pattern exemplar**: [profile-as-coordination-bundle](../../../wiki/patterns/01_drafts/profile-as-coordination-bundle.md) for why profile-driven config matters

## Domain context

This skill operates in **backend-ai-platform-python** — see [wiki/config/domain-profiles/backend-ai-platform-python.yaml](../../../wiki/config/domain-profiles/backend-ai-platform-python.yaml). AICP-specific concerns: profile system is the coordination bundle (per the pattern doc), `make profile-use` is the atomic switch, Docker compose restart is required for env-var changes to take effect.

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| ops-deploy | execute the deployment | Reads this skill's prepared config + runs pre-flight + deploys + smoke-tests + offers rollback |
| config-secrets | secret values for deployment | Different config dimension (secrets vs operational settings) |
| config-env | general env var management | Includes deploy envs but broader |
| config-feature-flags | feature toggles | Different layer (behavior toggles vs operational settings) |
| infra-monitoring | dashboard + alert config | Different infrastructure (observability vs runtime config) |
| ops-rollback | revert a bad deploy | Reactive; this skill is proactive (pick config that doesn't need rollback) |
| foundation-config | greenfield config setup | Greenfield; this skill picks among existing profiles |
