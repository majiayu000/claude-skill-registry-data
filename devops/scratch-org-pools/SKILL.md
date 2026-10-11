---
name: scratch-org-pools
description: "Use this skill when configuring pre-created scratch org pools for parallel CI testing, reducing pipeline wait times by claiming pre-warmed orgs instead of provisioning on demand. Covers CumulusCI pool commands, Dev Hub allocation planning for pools, pool sizing strategies, and CI matrix integration. NOT for basic scratch org lifecycle (use scratch-org-management), scratch org definition files (use org-shape-and-scratch-definition), or test data seeding (use data-seeding-for-testing)."
category: devops
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Operational Excellence
  - Reliability
  - Scalability
tags:
  - scratch-org-pools
  - ci-cd
  - cumulusci
  - dev-hub
  - parallel-testing
  - devops
triggers:
  - "my CI pipeline is slow because every job creates a scratch org from scratch"
  - "how do I set up a pool of pre-created scratch orgs for parallel CI runs"
  - "CI jobs are failing because the Dev Hub daily scratch org creation limit is exhausted by concurrent pipelines"
  - "I want to pre-warm scratch orgs so developers can claim one instantly instead of waiting"
  - "how does CumulusCI scratch org pooling work and how do I size the pool"
inputs:
  - "Dev Hub edition and current allocation limits (daily creates, max active)"
  - "Number of parallel CI jobs expected per day"
  - "CumulusCI project configuration (cumulusci.yml) if already in use"
  - "Scratch org definition file path"
  - "CI platform (GitHub Actions, Jenkins, Bitbucket Pipelines, etc.)"
outputs:
  - "CumulusCI pool configuration commands and cron schedule"
  - "Pool sizing recommendation based on Dev Hub limits and CI concurrency"
  - "CI pipeline YAML integrating pooled org claims"
  - "Dev Hub allocation audit queries"
  - "Monitoring and replenishment strategy"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-06
---

# Scratch Org Pools

This skill activates when a team needs to reduce CI pipeline latency by pre-creating scratch orgs into a pool that parallel jobs can claim instantly, rather than provisioning a fresh org per job. The canonical pool manager is CumulusCI; the Salesforce CLI does not natively support pooling. This skill covers pool sizing, Dev Hub limit planning, CumulusCI pool commands, CI integration, and monitoring.

---

## Before Starting

Gather this context before working on anything in this domain:

- **What Dev Hub edition is in use and what are the current allocation limits?** Pool sizing is constrained by the daily creation limit and maximum active org limit. A Developer Edition Dev Hub (6/day, 3 active) cannot meaningfully support pooling.
- **How many parallel CI jobs run per day, and what is the peak concurrency?** This determines pool size. Each concurrent job consumes one pooled org; orgs are not shared between jobs.
- **Is CumulusCI already installed and configured?** CumulusCI is the only mainstream tool that provides scratch org pool management. If the project uses raw `sf` CLI only, CumulusCI must be added before pooling is possible.

---

## Core Concepts

### 1. Why Pools Exist

Scratch org provisioning takes 2-8 minutes depending on edition, features, and whether sample data is enabled. In a CI system running 10+ parallel jobs per pull request, this wait compounds into 20-80 minutes of idle pipeline time. A pool pre-creates orgs during off-peak hours so that when a CI job starts, it claims an already-provisioned org in seconds.

Each pooled org is a standard scratch org. There is no special "pooled" org type in Salesforce. The pool is a management abstraction maintained by CumulusCI in its keychain.

### 2. CumulusCI Pool Architecture

CumulusCI manages pools through a set of commands that interact with the Dev Hub:

- **`cci org pool create`** — Creates a batch of scratch orgs and stores them in the CumulusCI keychain. Each org is created from the project's scratch org definition file.
- **`cci org pool list`** — Shows all available pooled orgs with their expiration dates.
- **`cci org pool get`** — Claims one org from the pool for use. The org is removed from the pool and becomes a regular CumulusCI org.
- **`cci org pool prune`** — Removes expired or failed orgs from the pool.

Pooled orgs are **not initialized** until claimed. When a job runs `cci org pool get`, CumulusCI initializes the org (runs flows like `dev_org` or `ci_org`) on first use. This means the pool stores bare scratch orgs with no metadata deployed — initialization happens at claim time.

### 3. Dev Hub Limits and Pool Math

Every pooled org counts against the Dev Hub's active org limit and daily creation limit. Pool sizing must account for:

| Factor | Formula Component |
|---|---|
| Peak parallel jobs | Minimum pool size = peak concurrency |
| Org expiration | Orgs expire after `duration-days`; pool must be replenished before expiry |
| Daily creation limit | Total orgs created per day (pool replenishment + ad-hoc) must stay under the daily limit |
| Buffer | Add 20-30% buffer for failed creations and retries |

**Example:** A team runs 8 parallel CI jobs, each consuming one org. Orgs are created with 1-day duration. The pool needs at least 8 orgs. With 30% buffer, target 11 orgs per replenishment cycle. On an Enterprise Dev Hub (40 daily creates, 20 active), this is sustainable. On a Developer Dev Hub (6 daily, 3 active), it is impossible.

### 4. Pool Lifecycle

The pool lifecycle follows a create-claim-prune cycle:

1. **Replenish** — A scheduled job (cron, GitHub Actions schedule, or CI cron trigger) runs `cci org pool create` to fill the pool to the target size.
2. **Claim** — Each CI job runs `cci org pool get` to claim an org. If the pool is empty, the job falls back to creating a scratch org on demand.
3. **Use** — The job deploys metadata, runs tests, and collects results.
4. **Dispose** — After use, the org is deleted (not returned to the pool). Pooled orgs are single-use.
5. **Prune** — Periodically run `cci org pool prune` to remove expired or failed entries from the keychain.

---

## Common Patterns

### Pattern 1: Basic Pool Setup with CumulusCI

**When to use:** Team has CumulusCI configured, uses GitHub Actions or similar CI, and wants to reduce org provisioning wait time.

**How it works:**

```bash
# Step 1: Create a pool of 10 scratch orgs
cci org pool create dev 10

# Step 2: Verify pool contents
cci org pool list dev

# Step 3: In a CI job, claim one org from the pool
cci org pool get dev --org ci_pool_org

# Step 4: Run the CI flow against the claimed org
cci flow run ci_feature --org ci_pool_org

# Step 5: Delete the org after use
cci org scratch_delete ci_pool_org

# Step 6: Prune stale entries
cci org pool prune dev
```

**Why not create orgs on demand:** On-demand creation adds 2-8 minutes per job. With 10 parallel jobs, that is 20-80 minutes of pipeline time wasted on provisioning alone.

### Pattern 2: Scheduled Pool Replenishment in GitHub Actions

**When to use:** Pool must be automatically refilled on a schedule so CI jobs always have orgs available.

**How it works:**

```yaml
# .github/workflows/pool-replenish.yml
name: Replenish Scratch Org Pool
on:
  schedule:
    - cron: '0 4 * * *'  # Daily at 4 AM UTC
  workflow_dispatch: {}    # Allow manual trigger

jobs:
  replenish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install CumulusCI
        run: pip install cumulusci

      - name: Authenticate Dev Hub
        run: |
          echo "${{ secrets.SFDX_AUTH_URL }}" > auth.txt
          sf org login sfdx-url --sfdx-url-file auth.txt --alias DevHub --set-default-dev-hub

      - name: Prune expired orgs
        run: cci org pool prune dev

      - name: Replenish pool to target size
        run: cci org pool create dev 10

      - name: Report pool status
        run: cci org pool list dev
```

### Pattern 3: CI Job with Pool Fallback

**When to use:** CI jobs should use pooled orgs when available but fall back to on-demand creation if the pool is empty.

**How it works:**

```bash
#!/bin/bash
# claim-or-create.sh — used in CI pipeline steps

# Try to claim from pool
if cci org pool get dev --org ci_org 2>/dev/null; then
  echo "Claimed org from pool"
else
  echo "Pool empty — creating on demand"
  cci org scratch dev ci_org --days 1
fi

# Run CI flow
cci flow run ci_feature --org ci_org

# Always clean up
cci org scratch_delete ci_org
```

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Dev Hub is Developer Edition (6/day, 3 active) | Do not pool; use on-demand creation | Limits are too low for a meaningful pool |
| Enterprise Dev Hub, 5-10 parallel CI jobs | Pool of 12-15 orgs, replenish daily | Fits within 40/day limit with room for developer use |
| Unlimited Dev Hub, 20+ parallel jobs | Pool of 25-30 orgs, replenish twice daily | Higher limits allow larger pools; twice-daily replenishment keeps pool fresh |
| ISV with Partner Business Org | Pool of 30-50 orgs, replenish every 8 hours | PBOs have 200+ daily creates; larger pools are feasible |
| Team does not use CumulusCI | Evaluate adding CumulusCI or build custom pool script | No native sf CLI pool support exists; CumulusCI is the standard tool |
| Pool orgs expire before being claimed | Reduce `--duration-days` replenishment interval or increase frequency | Orgs created with 1-day duration must be claimed within 24 hours |

---

## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner setting up scratch org pools:

1. **Audit Dev Hub limits** — Query `SELECT COUNT() FROM ActiveScratchOrg` in the Dev Hub to determine current usage, and confirm the edition to know the daily creation and active org caps.
2. **Determine pool size** — Calculate peak CI concurrency, add 30% buffer, and verify the total fits within the Dev Hub's daily and active limits.
3. **Install and configure CumulusCI** — Ensure `cumulusci.yml` exists and the `dev` org config points to the correct scratch org definition file.
4. **Create the initial pool** — Run `cci org pool create dev <count>` and verify with `cci org pool list dev`.
5. **Set up scheduled replenishment** — Create a CI workflow (cron job) that runs pool prune and pool create on a regular schedule.
6. **Integrate pool claims into CI jobs** — Replace `sf org create scratch` in CI pipelines with `cci org pool get` and add a fallback for empty pools.
7. **Monitor and tune** — Track pool hit rate (claims vs. fallbacks) and adjust pool size and replenishment frequency based on actual usage.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] Dev Hub edition supports the planned pool size (daily and active limits verified)
- [ ] Pool size accounts for peak concurrency plus 30% buffer
- [ ] CumulusCI is installed and `cumulusci.yml` has correct org definitions
- [ ] Replenishment schedule runs during off-peak hours and before the next CI peak
- [ ] CI jobs include fallback logic for empty pools
- [ ] CI jobs delete orgs after use (pooled orgs are single-use)
- [ ] `cci org pool prune` runs before each replenishment to clear stale entries
- [ ] Team members know not to manually create orgs that consume pool allocation

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **Pooled orgs count against active limits even before being claimed** — Every org in the pool is a real active scratch org in the Dev Hub. A pool of 20 orgs uses 20 of the Dev Hub's active org slots, leaving fewer for developers and other pipelines.

2. **Daily creation limit is a rolling 24-hour window, not a midnight reset** — If the pool replenishment job creates 30 orgs at 4 AM, you cannot create another 30 at 4 PM on an Enterprise Dev Hub (40/day). Plan replenishment timing around the rolling window.

3. **Failed pool creations still count against the daily limit** — If the Dev Hub rejects a creation request (e.g., unsupported feature in the definition file), it still consumes one daily create. A misconfigured definition file can burn through the daily limit producing nothing.

4. **Pool orgs are not initialized until claimed** — CumulusCI stores bare scratch orgs in the pool. Metadata deployment and data loading happen at claim time. This means the "instant" claim still requires initialization time — the savings come from skipping the 2-8 minute provisioning step, not from having fully deployed orgs ready.

5. **There is no native `sf` CLI pool command** — The Salesforce CLI does not include any pool management functionality. Pool management requires CumulusCI or a custom script that tracks orgs externally. Do not advise practitioners to look for `sf org pool` commands.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| CumulusCI pool commands | Commands for creating, listing, claiming, and pruning the pool |
| Pool sizing worksheet | Calculation of pool size based on Dev Hub limits and CI concurrency |
| Replenishment workflow YAML | Scheduled CI workflow for automatic pool maintenance |
| CI pipeline integration | Modified CI job steps using `cci org pool get` with fallback |
| Dev Hub allocation audit | SOQL queries to monitor active org usage against limits |

---

## Related Skills

- `scratch-org-management` — Single-org lifecycle, definition files, allocation troubleshooting; use this when the problem is not about pooling but about individual org provisioning
- `org-shape-and-scratch-definition` — Definition file authoring and Org Shape configuration; the definition file feeds into pool creation
- `github-actions-for-salesforce` — Full GitHub Actions CI/CD setup; pools integrate into existing pipeline workflows
- `environment-strategy` — Broader environment planning across sandboxes, scratch orgs, and Dev Hubs; pools are one component of the strategy
