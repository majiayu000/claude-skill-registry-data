---
name: deploy-evidence
description: TrueAlpha Deploy Evidence & Issue Closure Guard. Automates AGENTS.md Rule 6 ("Closed means verified on staging with real data") verification before any product issue can be closed.
---

# TrueAlpha Deploy Evidence & Closure Guard

> **Core Axiom (AGENTS.md Rule 6)**:
> *"A product issue closes only when staging runs its capability on real captured data. The issue holds the evidence: the deployed call site plus real-data output (SQL rows or an HTTP response)."*

## 1. When to Activate This Skill
- Before marking any TrueAlpha product issue as `Closed`.
- When verifying whether a PR actually closed an issue or merely merged code into `main`.
- When auditing staging or production deployment evidence.

## 2. The Verification Protocol (Step-by-Step)

### Step 1: Release Workflow, Health & Image Digest Check
Verify that the target release tag (`vX.Y.Z`) and commit SHA are promoted and served on the target environment:
```bash
# 1. Verify remote release deploy and surface walk workflows succeeded for vX.Y.Z
gh run list --workflow deploy-release.yml --limit 5
gh run list --workflow walk-release.yml --limit 5

# 2. If running directly on the VPS host via SSH, verify container image digests:
docker inspect -f '{{.Config.Image}}' truealpha-dagster-webserver-staging
docker inspect -f '{{.Config.Image}}' truealpha-dagster-daemon-staging
docker inspect -f '{{.Config.Image}}' truealpha-web-staging
docker inspect -f '{{.Config.Image}}' truealpha-llm-staging
```

### Step 2: Dagster & Runtime Liveness Proof
Confirm live service health (`git_sha` and `governed_pointers` in `/api/health`) and daemon heartbeat (on VPS host: `docker exec truealpha-dagster-daemon-staging dagster-daemon liveness-check`).

### Step 3: Deployed Execution Proof (Reachable Path)
Verify that the capability was invoked via a deployed path. A deployed path is reachable from the Dagster composition root (`dagster_defs.py`) or a deployed service/App entrypoint:
- **For DataHub/Ingestion**: The Dagster job ticked under daemon or sensor, writing to `mart.served_head`.
- **For Web/API**: An HTTP 200 response with typed data from the live service domain (`truealpha.club` or staging subdomain).
- **For Factors**: Factor outputs materialized into `mart` tables and readable via `mart_readonly`.

### Step 4: Real-Data Row Assertion
Never use `*_fixture` outputs as completion evidence!
Query the actual database:
```sql
-- Assert real data rows exist in the target mart table
SELECT run_id, count(*), min(valid_time), max(valid_time)
FROM mart.topt_capture_status
WHERE complete = true
GROUP BY run_id
ORDER BY max(valid_time) DESC
LIMIT 5;
```

## 3. Red Lines (Instant Rejection)
- ❌ Code merged into `main` without deployed proof: **DO NOT CLOSE ISSUE**.
- ❌ Green tests using fixture data or mocked responses: **DO NOT CLOSE ISSUE**.
- ❌ Output says `unavailable`, `unsourced`, or returns a sentinel placeholder / hardcoded confidence stamp (`0.85`, `0.92`, `1.00`) without an explicit scope demotion note (a real computed value with a `low_confidence` continuous score is valid and counts as produced): **DO NOT CLOSE ISSUE**.
- ❌ Standing checks supply parameters that deployed callers omit (#284): **REJECT EVIDENCE**.
