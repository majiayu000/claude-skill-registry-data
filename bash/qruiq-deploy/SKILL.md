---
name: qruiq-deploy
description: |
  All-in-one orchestrator that takes an existing local Next.js project from "code on disk" to "live URL on TKE".
  Drives discovery (CLIs auto-detect domain/repo/secrets/cluster), validation, a single consolidated confirmation,
  then delegates to /qruiq-github-ci, /qruiq-tke-deployment, /qruiq-cdb-create-db, and verifies the live URL.
  Writes one end-to-end execution log capturing inputs, validations, steps, issues and resolutions.
  Use when asked to "deploy to TKE end-to-end", "ship this to production", "上线", "一键部署",
  "from local to live", "全流程部署", or any request to take a local project all the way to a live URL.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# qruiq-deploy

> Orchestrator: existing local project → live URL on TKE in one flow.
> Calls existing qruiq skills as building blocks. Does NOT replicate their logic.

## Operating principles

1. **CLI-first discovery, not interrogation.** Probe with `gh`, `tccli`, `kubectl`, `dig`, `flarectl` before asking the user. Only ask for what cannot be auto-detected.
2. **One consolidated confirmation, not 15 prompts.** Phase 1 collects everything; Phase 3 shows it all in one summary; user picks Proceed / Edit / Abort.
3. **Auto-resolve best practices, surface real blockers.** A missing `output: "standalone"` is fixed silently. A missing domain registration is escalated.
4. **Append events to an in-memory log as we go.** Phase 5 writes them to disk so the user (and future Claude) can see exactly what happened, what failed, and how it was resolved.
5. **Never duplicate sub-skill logic.** Invoke the sub-skill, capture stdout+stderr, classify outcome, move on. If a sub-skill needs improvement, fix the sub-skill — don't fork its behavior here.

## Prerequisites

**Verify before any action. Stop and tell the user how to fix if any fail.**

| Command | Required | Check | If missing |
|---|---|---|---|
| `gh` | yes | `command -v gh` | `brew install gh` |
| `gh` logged in | yes | `gh auth status` | `gh auth login` |
| `kubectl` | yes | `command -v kubectl && kubectl cluster-info` | `brew install kubectl` + configure `~/.kube/config` |
| `tccli` | yes | `command -v tccli` (auth probed below — never `tccli configure list`, leaks secrets) | `pip install tccli && tccli configure` |
| `git` | yes | `command -v git` | `brew install git` |
| `dig` | yes | `command -v dig` | macOS: `brew install bind` |
| `jq` | yes | `command -v jq` | `brew install jq` |
| `flarectl` | optional | `command -v flarectl && [ -n "$CF_API_TOKEN" ]` | If absent, DNS step falls back to manual instructions — do not block |
| `whois` | optional | `command -v whois` | only used when surfacing domain registration help |

## Phase 1 — Discovery (parallel CLI probes)

Run probes in parallel where possible. Capture each result into an in-memory state object (use shell variables; the script-style block below is the source of truth).

```bash
# --- project ---
APP_NAME=$(jq -r .name package.json 2>/dev/null || echo "")
HAS_K8S=$(test -d k8s && echo yes || echo no)
HAS_CI=$(test -f .github/workflows/deploy-tke.yml && echo yes || echo no)
HAS_DOCKERFILE=$(test -f Dockerfile && echo yes || echo no)
HAS_NEXT_STANDALONE=$(grep -q 'output:.*standalone' next.config.* 2>/dev/null && echo yes || echo no)
HAS_GITIGNORE_QRUIQ=$(grep -q '\.qruiq-dev\.conf' .gitignore 2>/dev/null && echo yes || echo no)
HAS_PRISMA=$(test -f prisma/schema.prisma && echo yes || echo no)
HAS_DATABASE_URL=$(grep -hq '^DATABASE_URL=' .env .env.dev .env.local 2>/dev/null && echo yes || echo no)
HAS_NEXTAUTH=$(grep -rlq 'next-auth\|@auth/' --include='*.ts' --include='*.tsx' . 2>/dev/null && echo yes || echo no)

# --- existing config ---
test -f .qruiq-dev.conf && source .qruiq-dev.conf  # populates DOMAIN, TCR_USERNAME, etc. if previously set

# --- github ---
GH_AUTHED=$(gh auth status >/dev/null 2>&1 && echo yes || echo no)
GH_USER=$(gh api user --jq .login 2>/dev/null || echo "")
GH_ORGS=$(gh api user/orgs --jq '.[].login' 2>/dev/null | tr '\n' ' ')
GIT_REMOTE=$(git remote get-url origin 2>/dev/null || echo "")

# --- cluster ---
KUBE_CTX=$(kubectl config current-context 2>/dev/null)
LB_IP=$(kubectl get svc -n ingress-nginx ingress-nginx-controller -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null)
EXPECTED_LB="43.173.190.227"

# --- tencent cloud (auth probe — never `tccli configure list`) ---
TCCLI_OK=$(tccli cvm DescribeRegions --output json 2>/dev/null | jq -e '.RegionSet | length > 0' >/dev/null 2>&1 && echo yes || echo no)

# --- cloudflare ---
CF_AUTO=$(command -v flarectl >/dev/null && [ -n "$CF_API_TOKEN" ] && echo yes || echo no)
```

Then derive:
- If `APP_NAME` empty → ask the user for it (rare; package.json should have one).
- If `GIT_REMOTE` empty and multiple orgs in `GH_ORGS` → ask which org to create the repo under.
- If `DOMAIN` empty after sourcing `.qruiq-dev.conf` → suggest `<APP_NAME>.qruiq.app` and confirm via `AskUserQuestion`.
- Compute `ZONE` (registrable apex) from `DOMAIN` via `awk -F. '{print $(NF-1)"."$NF}'`.
- `DOMAIN_NS=$(dig +short NS "$ZONE" | head -1)` — if it ends with `.cloudflare.com.` and `CF_AUTO=yes` → `DNS_AUTO=yes`.
- `DOMAIN_RESOLVED=$(dig +short "$DOMAIN" | tail -1)` — if equal to `EXPECTED_LB` → `DNS_AUTO=already-correct`.
- `REPO_EXISTS=$(gh repo view "$GITHUB_ORG/$APP_NAME" >/dev/null 2>&1 && echo yes || echo no)` once `GITHUB_ORG` is known.
- `ORG_SECRETS=$(gh secret list --org "$GITHUB_ORG" --json name --jq '.[].name' 2>/dev/null)` (may 403; that's fine — fall back to repo-level).

Ask **only the gaps** via `AskUserQuestion`. Typical gaps:
- `DOMAIN` (with the `<APP_NAME>.qruiq.app` suggestion as the recommended option)
- `GITHUB_ORG` (only if multiple orgs and no remote; offer the orgs as options)
- `ENV` (default `dev`; offer `prod` only if user explicitly asks)
- `TCR_USERNAME` / `TCR_PASSWORD` (only if missing both at org-level and in `.qruiq-dev.conf`)
- DB? (only if `HAS_PRISMA=yes` AND `HAS_DATABASE_URL=no`)

Persist what you collect by writing/updating `.qruiq-dev.conf` and `.env.dev` BEFORE the consolidated confirmation, so sub-skills don't re-ask later.

## Phase 2 — Validation

These are read-only and must all pass before moving to Phase 3. Capture each result for the log.

| Check | Pass condition | On fail |
|---|---|---|
| `gh auth status` exit 0 | yes | block; print `gh auth login` |
| `gh auth status` token has `repo` + `workflow` scopes | yes | block; print `gh auth refresh -s repo,workflow` |
| `kubectl cluster-info` exit 0 | yes | block; ask user to fix `~/.kube/config` |
| `KUBE_CTX` matches a TKE Singapore cluster | yes (warn if not `cls-rjk5qyka`) | warn only — capture in log |
| `LB_IP == EXPECTED_LB` | yes | warn — could be wrong context; ask user to confirm |
| `TCCLI_OK == yes` | yes | block; print `tccli configure` |
| If DB requested: `tccli cdb DescribeDBInstances` returns at least one instance | yes | block; tell user to provision a CDB instance first |
| If `DNS_AUTO=yes`: zone reachable via `flarectl zone info` | yes | downgrade `DNS_AUTO` to `manual` |

If `gh repo view "$GITHUB_ORG/$APP_NAME"` succeeds, mark `REPO=existing`; else `REPO=new`. If existing, also check `gh api repos/$GITHUB_ORG/$APP_NAME --jq .default_branch` matches the local current branch (`git branch --show-current`); if mismatch, surface in the summary so the user decides whether to push to `main` vs current.

## Phase 3 — Consolidated confirmation

Print one Markdown summary like the example below. Don't paginate — this is the user's last chance to course-correct. Then call `AskUserQuestion` with header `Confirm` and options:
1. `Proceed` (recommended)
2. `Edit a value` — re-enter Phase 1 prompts for any single field
3. `Abort` — write a partial log noting "user aborted before execution" and stop

```
=== qruiq-deploy plan ===
Project:       my-app                         (from package.json)
Env:           dev                             (namespace: my-app-dev, tag prefix: dev-tag/v*)
Domain:        my-app.qruiq.app                (zone qruiq.app on Cloudflare; DNS not pointed → flarectl will create A → 43.173.190.227)
GitHub repo:   qruiq-org/my-app                (NEW — will create)
Cluster:       cls-rjk5qyka (TKE Singapore)    (current context ✓; nginx LB 43.173.190.227 ✓)
TCR image:     sgccr.ccs.tencentyun.com/qruiq/my-app

GitHub secrets:
  ✓ TCR_USERNAME       org-level (inherited)
  ✓ TCR_PASSWORD       org-level (inherited)
  ✗ KUBE_CONFIG_DEV    will set at repo (from ~/.kube/config)
  ✗ KUBE_CONFIG_PROD   will set at repo (from ~/.kube/config)

Sub-skills to run, in order:
  1. /qruiq-github-ci         create repo, push, set secrets, add Dockerfile + workflow
  2. /qruiq-cdb-create-db     provision MySQL schema my_app + app account (Prisma detected)
  3. /qruiq-tke-deployment    write k8s/, init namespace, apply, verify pod
  4. (this skill)             push tag dev-tag/v0.1.0, watch CI, configure DNS, verify live URL

Auto-resolved best practices (no user action needed):
  • Patch next.config.mjs to add output: "standalone"
  • touch public/.gitkeep to keep Docker build happy
  • Append .qruiq-dev.conf and .env.dev to .gitignore

Manual actions you may need to do later:
  (none — TLS terminated at Cloudflare in Full mode for *.qruiq.app)

Estimated runtime: 6–8 minutes (dominated by Docker build).
Log will be written to: k8s/deployments/all-in-one-dev-<timestamp>.md
```

## Phase 4 — Execute

**Wrap each step in a try/log pattern.** Track an event list with fields `{step, status, summary, started_at, finished_at, stdout_tail, stderr_tail, resolution?}`. `status ∈ {OK, WARN, FAIL, FIXED}`. `FIXED` means the step initially failed but was auto-resolved and re-run.

**Order:**

### 4.1 Persist collected inputs

Write `.qruiq-dev.conf` (gitignored) so sub-skills find pre-filled values:

```
APP_NAME=<value>
TCR_NAMESPACE=qruiq
DOMAIN=<value>
TCR_USERNAME=<value>
TCR_PASSWORD=<value>
```

Ensure `.gitignore` contains `.qruiq-dev.conf` and `.env.dev` (append if missing). Stub `.env.dev` if it doesn't exist with the keys `DATABASE_URL`, `NEXTAUTH_SECRET`, `NEXTAUTH_URL` so sub-skills can extend it.

### 4.2 Auto-resolve known build-time issues

```bash
# Next.js standalone output
if ! grep -q 'output:.*standalone' next.config.* 2>/dev/null; then
  # patch existing config (don't blindly overwrite)
  CFG=$(ls next.config.* 2>/dev/null | head -1)
  [ -n "$CFG" ] && {
    # idempotent insert before module.exports / export default
    if [ "${CFG##*.}" = "mjs" ] || [ "${CFG##*.}" = "ts" ]; then
      sed -i '' 's/const nextConfig = {/const nextConfig = {\n  output: "standalone",/' "$CFG"
    fi
    EVENT_FIXED "next.config standalone output" "patched $CFG"
  }
fi

# public/ guard
[ ! -d public ] && mkdir -p public
[ -z "$(ls -A public 2>/dev/null)" ] && touch public/.gitkeep

# .gitignore
grep -q '\.qruiq-dev\.conf' .gitignore 2>/dev/null || echo '.qruiq-dev.conf' >> .gitignore
grep -q '\.env\.dev' .gitignore 2>/dev/null || echo '.env.dev' >> .gitignore
```

Each fix appended to the event list with `status=FIXED`.

### 4.3 Sub-skill: `/qruiq-github-ci`

Skip if `HAS_CI=yes`. Otherwise invoke. After completion, verify:
- `gh repo view "$GITHUB_ORG/$APP_NAME"` succeeds
- `gh secret list --repo "$GITHUB_ORG/$APP_NAME"` includes any non-org-level secrets
- `git remote get-url origin` matches the repo

If a sub-skill prompt blocks on a value we already collected, that's a bug — record under issues and continue.

### 4.4 Sub-skill: `/qruiq-cdb-create-db` (conditional)

Skip unless `DB_REQUESTED=yes`. After completion:
- Read the connection URI it produced
- Append `DATABASE_URL=<uri>` to `.env.dev` (overwrite existing line)
- Sub-skill emits the password to stdout once — capture into the log as `[REDACTED]` only

### 4.5 Sub-skill: `/qruiq-tke-deployment`

Skip if `HAS_K8S=yes` AND `kubectl get deployment -n "${APP_NAME}-${ENV}" "${APP_NAME}-web"` succeeds. Otherwise invoke. The sub-skill writes its own per-skill log to `k8s/deployments/<APP_NAME>-${ENV}-<ts>.md` — we do NOT duplicate that; instead we link to it from the all-in-one log.

After completion:
- `kubectl rollout status deployment/${APP_NAME}-web -n ${APP_NAME}-${ENV} --timeout=2m` (sub-skill already does this; we re-check for idempotency)
- Capture the pod name + image tag for the log

### 4.6 Trigger first deploy via tag

```bash
# pick next available tag — don't blow up if 0.1.0 already exists
EXISTING=$(git tag -l "dev-tag/v*" | sort -V | tail -1)
if [ -z "$EXISTING" ]; then
  TAG="dev-tag/v0.1.0"
else
  # bump patch version
  TAG=$(echo "$EXISTING" | awk -F. '{print $1"."$2"."$3+1}')
fi
git tag "$TAG"
git push origin "$TAG"
```

### 4.7 Watch the CI run

```bash
sleep 5  # give GH a moment to register the workflow
RUN_ID=$(gh run list --repo "$GITHUB_ORG/$APP_NAME" --workflow deploy-tke.yml --limit 1 --json databaseId --jq '.[0].databaseId')
gh run watch --repo "$GITHUB_ORG/$APP_NAME" --exit-status "$RUN_ID"
```

On non-zero exit, the workflow failed. Fetch failed-step logs:

```bash
gh run view --repo "$GITHUB_ORG/$APP_NAME" "$RUN_ID" --log-failed | tail -100
```

Diagnose common failures and auto-resolve where safe (each adds an `Issue → Resolution` entry):

| Failure signature in logs | Auto-resolution |
|---|---|
| `output: "standalone"` missing → `Cannot find /app/.next/standalone` | Patch next.config, bump tag, retry |
| `pull access denied` from TCR | Verify `TCR_USERNAME`/`TCR_PASSWORD` secrets; if missing, set and retry |
| `kubectl: error: You must be logged in` | Re-base64 kubeconfig and re-set `KUBE_CONFIG_DEV`; retry |
| `ImagePullBackOff` after deploy | Wait one more rollout cycle (`kubectl rollout restart`), then describe pod |
| `prisma migrate deploy` fails with "no migrations folder" | Switch workflow's prod branch to `prisma db push` for first-time, OR ask user — record under issues |

Anything outside this table → record `FAIL`, ask the user via `AskUserQuestion`: `Retry / Skip / Abort`.

### 4.8 Live verification

```bash
# external HTTPS first (only valid if DNS_AUTO != manual)
if [ "$DNS_AUTO" != "manual" ]; then
  for i in 1 2 3 4 5; do
    sleep 10
    if curl -fsS --max-time 10 "https://${DOMAIN}/api/health" >/dev/null 2>&1; then
      LIVE_HTTPS=ok; break
    fi
  done
fi

# fallback: through ingress with Host header (works even without DNS)
if [ "$LIVE_HTTPS" != "ok" ]; then
  curl -fsS --max-time 10 -H "Host: ${DOMAIN}" "http://${LB_IP}/api/health" >/dev/null 2>&1 \
    && LIVE_BY_HOST=ok || LIVE_BY_HOST=fail
fi

# in-cluster final fallback (always available; tells us pod is alive even if ingress is broken)
POD=$(kubectl get pod -n "${APP_NAME}-${ENV}" -l "app=${APP_NAME},component=web" -o jsonpath='{.items[0].metadata.name}')
kubectl exec -n "${APP_NAME}-${ENV}" "$POD" -- wget -q -O - http://localhost:3000/api/health \
  && LIVE_INCLUSTER=ok || LIVE_INCLUSTER=fail
```

If `LIVE_HTTPS=ok` → call it shipped. If only `LIVE_BY_HOST=ok` → DNS pending, record manual action. If only `LIVE_INCLUSTER=ok` → ingress problem, dig into nginx logs and record. If all three fail → emergency mode, dump pod logs and ask user how to proceed.

## Phase 5 — Execution log

Path: `k8s/deployments/all-in-one-${ENV}-$(date +%Y%m%d-%H%M).md`

Write the template below, filling from the in-memory event list. **Never include secret values** — only key names. Capture both successful and failed events; the log is the post-mortem record, so failures + their resolutions are the most important content.

```markdown
# All-in-one deploy: <APP_NAME>-<ENV> — <YYYY-MM-DD HH:MM TZ>

## Inputs (collected)
- App: <APP_NAME>
- Env: <ENV>
- Domain: <DOMAIN>
- Repo: <GITHUB_ORG>/<APP_NAME> (<created|existing>)
- Cluster: <KUBE_CTX>
- Ingress LB: <LB_IP>
- TCR image: sgccr.ccs.tencentyun.com/<TCR_NAMESPACE>/<APP_NAME>
- DB: <provisioned|skipped|already-set>
- DNS method: <flarectl|manual|already-correct>
- Auth detected in code: <next-auth|none>

## Pre-flight validations
- [✓|✗] gh auth status (scopes: <scopes>)
- [✓|✗] kubectl cluster-info (context: <ctx>)
- [✓|✗] ingress-nginx LB IP = <LB_IP> (expected 43.173.190.227)
- [✓|✗] tccli auth (cvm DescribeRegions OK)
- [✓|✗] Cloudflare zone <ZONE> reachable via flarectl

## Steps executed
1. [OK|FIXED|FAIL] Persist .qruiq-dev.conf + .env.dev — <summary>
2. [OK|FIXED|FAIL] Auto-resolve build-time fixes — <list of fixes applied>
3. [OK|SKIP|FAIL] qruiq-github-ci — <summary, e.g. "created repo, set 2 repo secrets, 2 inherited">
4. [OK|SKIP|FAIL] qruiq-cdb-create-db — <summary>
5. [OK|FAIL]      qruiq-tke-deployment — applied <N> resources, pod ready in <Ns>, link: k8s/deployments/<APP>-<ENV>-<ts>.md
6. [OK|FAIL]      Tag push <TAG> + workflow run #<id> (<duration>)
7. [OK|FAIL]      DNS — <method> — <result>
8. [OK|FAIL]      Live HTTPS — <status>

## Issues encountered + resolution
<!-- For each FAIL/FIXED event, one entry. Empty section if perfect run. -->
1. **Issue:** <verbatim signal — first relevant line of stderr / log>
   **Diagnosis:** <one sentence>
   **Resolution:** <what we did automatically OR what the user did>
   **Outcome:** <succeeded on retry #N | manual action queued | aborted>

## Final state
- Live URL: <https://...> → <HTTP status>
- Pods: <READY>/<DESIRED> Running in <namespace>
- Latest image: <tag>
- GitHub repo: <url>
- Latest workflow run: <url>

## Manual actions remaining
- <list — or "none">

## Operator
- Run by: <git config user.email>
- Skill: qruiq-deploy
- Sub-skill logs: k8s/deployments/<APP>-<ENV>-<ts>.md
```

After writing:

```bash
mkdir -p k8s/deployments
# (write the file)
git rev-parse --is-inside-work-tree >/dev/null 2>&1 && git add k8s/deployments/all-in-one-*.md
```

**Do NOT auto-commit.** The user reviews and commits along with their other changes.

## Final report (printed to chat)

After the log is written, print a tight summary to chat — same shape as `qruiq-tke-deployment` step 6c:

```
=== qruiq-deploy summary ===
App:           <APP_NAME>
Env:           <ENV>
Live URL:      https://<DOMAIN>/api/health  →  <HTTP 200 / pending DNS / failed>
Pods:          <READY>/<DESIRED> Running in <namespace>
Image tag:     <tag>
Repo:          https://github.com/<ORG>/<APP_NAME>
Workflow:      https://github.com/<ORG>/<APP_NAME>/actions/runs/<run_id>
DNS:           <method> — <result>
Log written:   k8s/deployments/all-in-one-<env>-<ts>.md (staged)

=== Issues fixed automatically ===
  • <list — suppress section if none>

=== Action items for you ===
  1. git commit -m "deploy: <APP> <ENV> <date>" k8s/deployments/all-in-one-<env>-<ts>.md && git push
  2. <other items if any — DNS pending, TLS upgrade, etc. Else suppress.>
```

## Idempotency

This skill is safe to re-run. Every phase checks state before acting:
- Existing `.github/workflows/deploy-tke.yml` → skip github-ci
- Existing `k8s/` with healthy deployment → skip tke-deployment
- Existing `DATABASE_URL` → skip cdb-create-db
- Existing `dev-tag/v0.1.x` tag → bump patch version
- Existing log file at the same minute → append `-2`, `-3` suffix

Re-running on a green deployment should result in: "no changes needed; live URL still 200" + a brief log noting the no-op.

## What this skill does NOT do

- **Domain registration.** If the user has no domain, suggest `/qruiq-domain-name` and stop.
- **TLS via cert-manager.** Default assumption is Cloudflare Full mode terminating TLS. If the user wants ingress-terminated TLS, that's a separate add-on.
- **Production deploys without a green dev deploy first.** If `ENV=prod` and no `<APP>-dev` namespace exists, refuse and tell the user to run `dev` first.
- **Multi-env in one invocation.** One run = one env. Run twice for dev + prod.
- **Tencent Cloud account / CDB instance / TKE cluster provisioning.** Those are out of scope; this skill assumes they exist.
- **Replicating sub-skill logic.** If a sub-skill's behavior is wrong, fix the sub-skill — not this orchestrator.

## Reference

| Resource | Value |
|---|---|
| Cluster ID | `cls-rjk5qyka` |
| nginx Ingress LB IP | `43.173.190.227` |
| TCR registry | `sgccr.ccs.tencentyun.com` |
| Default TCR namespace | `qruiq` |
| Default app domain pattern | `<APP_NAME>.qruiq.app` |
| Default dev tag | `dev-tag/v0.1.0` |
| Default prod tag | `v1.0.0` |
| Sub-skills used | `/qruiq-github-ci`, `/qruiq-tke-deployment`, `/qruiq-cdb-create-db`, `/qruiq-domain-name` |
