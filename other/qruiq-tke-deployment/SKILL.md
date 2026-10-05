---
name: qruiq-tke-deployment
description: |
  Add TKE Kubernetes deployment config: Namespace, ConfigMap, Secret, Deployment, Service, Ingress.
  Uses nginx ingress controller on Tencent TKE (Singapore cluster).
  Use when asked to "add K8s config", "deploy to TKE", "add deployment", or "setup Kubernetes".
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# qruiq-tke-deployment

> Per-project Namespace isolation on Tencent TKE with nginx ingress. Based on production config from `ufcenter.xyz`.

## Prerequisites

**Check before proceeding. Stop and prompt user if any fail:**

### 1. Detect user shell

```bash
echo $SHELL
```

### 2. Verify dependencies

| Command | Required | Check | If missing |
|---|---|---|---|
| `kubectl` | yes | `command -v kubectl` | `brew install kubectl` |
| Cluster connected | yes | `kubectl cluster-info` | Configure `~/.kube/config` |
| Correct context | yes | `kubectl config current-context` | Show context, confirm with user |
| `git` | yes | `command -v git` (needed in step 6 to stage the deploy log) | `brew install git` |
| `dig` | yes | `command -v dig` (used in step 5 to check DNS state) | macOS: `brew install bind` |
| `flarectl` + Cloudflare creds | optional | `command -v flarectl && ([ -n "$CF_API_TOKEN" ] \|\| ( [ -n "$CF_API_KEY" ] && [ -n "$CF_API_EMAIL" ] ))` | If missing, step 5 falls back to manual DNS instructions — don't block on this |

**Cloudflare auth — two modes (flarectl supports both):**
- **Scoped API Token** — `CF_API_TOKEN=<token>`. Get from `https://dash.cloudflare.com/profile/api-tokens`, template "Edit zone DNS", scoped to the target zone(s).
- **Global API Key** — `CF_API_KEY=<key>` + `CF_API_EMAIL=<account email>`. Older mode, account-wide (more powerful, less safe).

If a user pastes a Cloudflare key that fails as `CF_API_TOKEN` with `Invalid access token (9109)`, retry as Global API Key with their account email — many "global keys" are pasted into the wrong slot.

Parameter loading/auto-detect happens in **Step 0** below (driven by `.qruiq-dev.conf`), not here.

## Parameters

All parameters are persisted in `.qruiq-dev.conf` at the project root. Step 0 loads it (or creates it). Subsequent steps `source` it.

| Key | Required | Auto-detect method | Example |
|---|---|---|---|
| `APP_NAME` | Yes | `package.json` name field | `my-app` |
| `TCR_NAMESPACE` | Yes | default `qruiq` | `qruiq` |
| `DOMAIN` | Yes | `k8s/ingress.yaml` host field, else suggest `<APP_NAME>.qruiq.app` | `my-app.qruiq.app`, `invoory.com` |
| `TCR_USERNAME` | Yes | **try existing namespace first** (see Step 0), else ask | `100012345678` |
| `TCR_PASSWORD` | Yes | **try existing namespace first** (see Step 0), else ask (sensitive) | `xxxxxx` |

**DOMAIN doesn't have to be a `qruiq.app` subdomain** — any zone with NS on Cloudflare works (e.g. `invoory.com`, `esgdone.com`). What matters is that the zone resolves through Cloudflare so the proxy can route to the nginx ingress LB. Domains parked on registrar-provided NS (afternic, GoDaddy default) won't work until NS is changed to Cloudflare.

`.env.dev` is a **separate** file (consumed by the app at runtime and by `kubectl create secret --from-env-file`). It must contain at least: `DATABASE_URL`, `NEXTAUTH_SECRET`, `NEXTAUTH_URL`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`.

Both `.qruiq-dev.conf` and `.env.dev` contain credentials — **must be gitignored**.

## Steps

**Execute all steps directly. Do not list as TODOs.** Pause only when:
- step 0 is missing required keys (ask user to fill, then continue), or
- step 3 finds `.env.dev` missing (ask user to create it, then continue).

### 0. Load or initialize `.qruiq-dev.conf`

```bash
test -f .qruiq-dev.conf && echo "EXISTS" || echo "MISSING"
```

**If EXISTS:** `source .qruiq-dev.conf`, then verify every required key (table above) is set and non-empty. For any missing/empty key, ask the user (use `AskUserQuestion`) and append/update the file.

**If MISSING:** Auto-detect what you can, then write the file with placeholders for the rest.

**TCR creds — try to auto-extract from an existing namespace first** (skip the user prompt). Every TKE namespace this skill creates has a `tcr-secret`; same creds are reused across all qruiq projects. Decode whichever exists:

```bash
SRC_NS=$(kubectl get secret tcr-secret -A -o jsonpath='{.items[0].metadata.namespace}' 2>/dev/null)
if [ -n "$SRC_NS" ]; then
  AUTH=$(kubectl get secret tcr-secret -n "$SRC_NS" -o jsonpath='{.data.\.dockerconfigjson}' | base64 -d)
  TCR_USERNAME=$(echo "$AUTH" | jq -r '.auths["sgccr.ccs.tencentyun.com"].username')
  TCR_PASSWORD=$(echo "$AUTH" | jq -r '.auths["sgccr.ccs.tencentyun.com"].password')
fi
```

Only ask the user if no `tcr-secret` exists anywhere yet (first project on the cluster).

Write `.qruiq-dev.conf`:

```
# qruiq dev deployment config — gitignored, contains credentials
APP_NAME=<from package.json>
TCR_NAMESPACE=qruiq
DOMAIN=<APP_NAME>.qruiq.app          # or any Cloudflare-NS domain
# Tencent Container Registry creds — get from https://console.cloud.tencent.com/tcr
TCR_USERNAME=<auto-extracted, or empty>
TCR_PASSWORD='<auto-extracted, or empty>'   # quote — passwords often contain shell-special chars
```

For any keys still empty after auto-detect, ask the user via `AskUserQuestion`, then write them back. Also ensure `.qruiq-dev.conf` and `.env.dev` are in `.gitignore` — append if missing.

Finally, `source .qruiq-dev.conf` so subsequent steps see the values as env vars.

### 1. Copy K8s config files

```bash
mkdir -p k8s/scripts
cp ~/.qruiq/skills/skills/qruiq-tke-deployment/template/k8s/*.yaml k8s/
cp ~/.qruiq/skills/skills/qruiq-tke-deployment/template/k8s/scripts/init-namespace.sh k8s/scripts/
chmod +x k8s/scripts/init-namespace.sh
```

### 2. Replace placeholders

Values come from `.qruiq-dev.conf` (sourced in step 0).

```bash
sed -i '' "s/__APP_NAME__/$APP_NAME/g" k8s/*.yaml
sed -i '' "s/__TCR_NAMESPACE__/$TCR_NAMESPACE/g" k8s/*.yaml
sed -i '' "s/__IMAGE_NAME__/$APP_NAME/g" k8s/*.yaml
sed -i '' "s/__DOMAIN__/$DOMAIN/g" k8s/*.yaml
```

### 3. **[PAUSE]** Verify `.env.dev` exists, then initialize Namespace

Check `.env.dev` is present and contains the keys listed in Parameters. If missing, stop and ask the user to create it before continuing.

Then run (TCR creds already sourced from `.qruiq-dev.conf`):

```bash
./k8s/scripts/init-namespace.sh "$APP_NAME" dev
```

**Wait for the script to finish before continuing.**

### 4. Verify deployment

Execute all verification — do not leave for user to check.

**4a. Wait for pods**
```bash
kubectl rollout status deployment/${APP_NAME}-web -n ${APP_NAME}-dev --timeout=5m
```

On failure, diagnose:
```bash
kubectl get pods -n ${APP_NAME}-dev
kubectl describe pod -n ${APP_NAME}-dev -l app=${APP_NAME},component=web
kubectl logs -n ${APP_NAME}-dev -l app=${APP_NAME},component=web --tail=50
```

**4b. Health check (in-cluster)**
```bash
POD=$(kubectl get pod -n ${APP_NAME}-dev -l app=${APP_NAME},component=web -o jsonpath='{.items[0].metadata.name}')
kubectl exec -n ${APP_NAME}-dev $POD -- wget -q -O - http://localhost:3000/api/health
```

**4c. External access**

If `DOMAIN` resolves publicly:
```bash
curl -sf https://${DOMAIN}/api/health
```

Otherwise (DNS not yet pointed), test via LB IP + Host header:
```bash
LB_IP=$(kubectl get svc -n ingress-nginx ingress-nginx-controller -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
curl -sf -H "Host: ${DOMAIN}" http://$LB_IP/api/health
```

### 5. Pick TLS strategy, then configure DNS

Set `DNS_METHOD`, `DNS_RESULT`, and `TLS_MODE` for use in the operation log (step 6).

**5a. Ask the user once which TLS path they want** (via `AskUserQuestion`). Default = Flexible — fastest, zero origin config:

| Choice | What happens | Best for |
|---|---|---|
| **Cloudflare Flexible** (default) | DNS proxy=ON. Cloudflare gives `https://` at the edge with its cert; talks `http` to origin (the nginx ingress on port 80). No origin TLS config needed. | First-time bring-up, dev/staging |
| **Cloudflare Full (Strict)** | DNS proxy=ON. Origin needs a real cert — install cert-manager + add `tls:` block to `k8s/ingress.yaml`. Adds ~10min. | Production-ish |
| **No proxy, HTTP only** | DNS proxy=OFF. User accesses `http://<domain>` only, no TLS. | Internal/test |

Set `TLS_MODE` and `PROXY_FLAG` accordingly (`true` for Flexible/Full, `false` for HTTP only).

**5b. Skip DNS write if already pointed correctly**

```bash
RESOLVED=$(dig +short "$DOMAIN" | tail -1)
# Cloudflare-proxied domains resolve to 104.* / 172.* anycast IPs, not 43.173.190.227 directly.
case "$RESOLVED" in
  43.173.190.227) DNS_METHOD="already-correct"; DNS_RESULT="skipped (direct A)" ;;
  104.*|172.*)    DNS_METHOD="already-correct"; DNS_RESULT="skipped (Cloudflare-proxied)" ;;
esac
```

**5c. If not resolved, try `flarectl`** (works with either auth mode — see Prerequisites)

```bash
HAS_FLARECTL_AUTH=false
if command -v flarectl >/dev/null; then
  if [ -n "$CF_API_TOKEN" ] || ([ -n "$CF_API_KEY" ] && [ -n "$CF_API_EMAIL" ]); then
    HAS_FLARECTL_AUTH=true
  fi
fi
```

If true, derive the zone (`invoory.com` → zone `invoory.com`; `my-app.qruiq.app` → zone `qruiq.app`) and create the A record. **Use the Cloudflare API directly to set SSL mode**, since flarectl doesn't expose it:

```bash
# Pick the zone: if DOMAIN equals zone, the apex; else extract last two labels.
ZONE=$(echo "$DOMAIN" | awk -F. '{print $(NF-1)"."$NF}')

flarectl dns create-or-update \
  --zone "$ZONE" \
  --name "$DOMAIN" \
  --type A \
  --content 43.173.190.227 \
  --proxy="$PROXY_FLAG"

# If user picked Flexible, set the zone's SSL mode (flarectl doesn't expose this)
if [ "$TLS_MODE" = "flexible" ]; then
  ZONE_ID=$(flarectl zone info --zone "$ZONE" --json 2>/dev/null | jq -r '.[0].id')
  if [ -n "$CF_API_TOKEN" ]; then
    AUTH_HEADERS=(-H "Authorization: Bearer $CF_API_TOKEN")
  else
    AUTH_HEADERS=(-H "X-Auth-Email: $CF_API_EMAIL" -H "X-Auth-Key: $CF_API_KEY")
  fi
  curl -s -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/ssl" \
    "${AUTH_HEADERS[@]}" -H "Content-Type: application/json" \
    -d '{"value":"flexible"}' >/dev/null
fi
```

Then set `DNS_METHOD="flarectl"` and `DNS_RESULT="A $DOMAIN → 43.173.190.227 (zone $ZONE, proxy=$PROXY_FLAG, ssl=$TLS_MODE)"`. Re-run the `dig` check above to confirm.

**5d. Otherwise — record manual action needed**

If `flarectl` is missing OR no Cloudflare creds, do NOT attempt the API by hand. Set:
- `DNS_METHOD="manual"`
- `DNS_RESULT="pending: user must add A record $DOMAIN → 43.173.190.227 in Cloudflare (proxy=$PROXY_FLAG); set SSL/TLS mode to '$TLS_MODE'"`

Tell the user how to enable automation next time:
```
To automate DNS in future runs, set ONE of these in your shell rc:
  # Scoped token (preferred, get from https://dash.cloudflare.com/profile/api-tokens):
  export CF_API_TOKEN=<token with Zone:DNS:Edit + Zone:Zone Settings:Edit on the zone>
  # OR Global API Key (account-wide):
  export CF_API_KEY=<global key>
  export CF_API_EMAIL=<your account email>
flarectl: brew install cloudflare/cloudflare/flarectl   # or: go install github.com/cloudflare/cloudflare-go/v4/cmd/flarectl@latest
```

### 6. Write operation log + git add + final report

**6a. Write the log to a tracked path**

Path: `k8s/deployments/<APP_NAME>-dev-$(date +%Y%m%d-%H%M).md`

Content template — fill from variables already in scope. **Never include secret values** (only key names from `.env.dev`):

```markdown
# Deployment: <APP_NAME>-dev — <YYYY-MM-DD HH:MM TZ>

## Configuration
- App: <APP_NAME>
- Namespace: <APP_NAME>-dev
- Image: sgccr.ccs.tencentyun.com/<TCR_NAMESPACE>/<APP_NAME>:<tag observed in deployment.yaml>
- Domain: <DOMAIN>
- Cluster: cls-rjk5qyka (TKE Singapore)
- Ingress: nginx (LB IP 43.173.190.227)

## Resources applied
- Namespace: <APP_NAME>-dev
- Secret: tcr-secret (docker-registry, server sgccr.ccs.tencentyun.com)
- Secret: <APP_NAME>-secrets (keys: <space-separated key names from .env.dev — NOT values>)
- ConfigMap, Deployment, Service, Ingress

## Verification
- Pod rollout: <success / failure reason>
- In-cluster /api/health: <HTTP status>
- External /api/health: <HTTP status / pending>

## DNS
- Method: <DNS_METHOD>
- Result: <DNS_RESULT>

## Operator
- Run by: <git config user.email, or "unknown">
- Skill: qruiq-tke-deployment

## Manual actions still required
- <list anything pending: TLS, CI/CD, DNS if manual, etc. — or "none">
```

**6b. Stage the log for commit (do not commit)**

```bash
mkdir -p k8s/deployments
# (write the file in 6a)
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git add k8s/deployments/<filename>.md
  STAGED="staged"
else
  STAGED="not-a-git-repo (file written, no git add performed)"
fi
```

Do NOT auto-commit — let the user review and commit alongside their other changes. If not a git repo, surface that fact in the final report so the user knows to `git init` (or move the file into the project's repo) to get it into GitHub.

**6c. Print the final report**

Tailor each line to the actual state observed (don't repeat items already satisfied):

```
=== Deployment summary ===
App:           <APP_NAME>
Namespace:     <APP_NAME>-dev
Image:         sgccr.ccs.tencentyun.com/<TCR_NAMESPACE>/<APP_NAME>:<tag>
Domain:        <DOMAIN>
Pod status:    <Running / failure reason>
Health check:  <in-cluster: pass/fail>  <external: pass/fail/skipped>
DNS:           <DNS_METHOD> — <DNS_RESULT>
Log written:   k8s/deployments/<filename>.md (<STAGED>)

=== Next steps ===
1. Commit the deployment log:
     git commit -m "deploy: <APP_NAME>-dev <date>" k8s/deployments/<filename>.md
     git push

2. TLS — if you need HTTPS, add a cert-manager Issuer + tls block to k8s/ingress.yaml,
   or terminate at Cloudflare with "Full" mode.

3. CI/CD — image must be built & pushed to TCR before the deployment can pull.
   If not set up yet, run /qruiq-github-ci to add a GitHub Actions pipeline that
   builds & pushes on tag push (dev-tag/v* → dev, v* → prod).

4. Updating the running image after a new build:
     kubectl set image deployment/<APP_NAME>-web web=<new-image>:<tag> -n <APP_NAME>-dev

5. Tail logs:
     kubectl logs -f deployment/<APP_NAME>-web -n <APP_NAME>-dev

6. Rotating creds — `.qruiq-dev.conf` and `.env.dev` hold secrets. To rotate:
   edit the file, then re-run `./k8s/scripts/init-namespace.sh <APP_NAME> dev`
   (it re-applies secrets via kubectl apply).
```

Suppress items 2–3 if already verified working in step 4c / step 5. Always show 1, 4–6.

## Placeholder conventions

Template files use `__UPPERCASE__` placeholders:

| Placeholder | Description |
|---|---|
| `__APP_NAME__` | App name, also used as namespace prefix |
| `__TCR_NAMESPACE__` | TCR image namespace (default: `qruiq`) |
| `__IMAGE_NAME__` | Docker image name |
| `__DOMAIN__` | External domain |
| `__INGRESS_IP__` | TKE Ingress LB IP |

## Namespace convention

```
<project-name>-dev    # Dev/test environment (also currently used for prod)
<project-name>-prod   # Production (reserved — not used in practice yet)
```

**Current reality:** All live projects run in `-dev` namespaces, including production traffic
(e.g. `qruiq-dev` hosts `ufcenter-web` serving `qruiq.app` / `www.qruiq.app`, and
`the-fist-web-app-web` serving `the-fist-web-app.qruiq.app`). Don't assume `-dev`
means "safe to break" — verify what's actually deployed before touching a namespace.

## Resource manifest (deploy order)

1. **Namespace** — `k8s/namespace.yaml`
2. **TCR Secret** — `kubectl create secret docker-registry tcr-secret ...`
3. **ConfigMap** — `k8s/configmap.yaml`
4. **App Secret** — `kubectl create secret generic <app>-secrets --from-env-file=.env.dev`
5. **Deployment** — `k8s/deployment.yaml` (health probes on `/api/health:3000`)
6. **Service** — `k8s/service.yaml` (ClusterIP, port 80 → 3000)
7. **Ingress** — `k8s/ingress.yaml` (nginx ingress class)

## Cluster reference

| Item | Value |
|---|---|
| Cluster ID | `cls-rjk5qyka` |
| nginx Ingress LB IP | `43.173.190.227` — **use this for DNS** |
| Other CLB IP | `150.109.21.157` — **not nginx ingress, do not use** |
| TCR (Singapore) | `sgccr.ccs.tencentyun.com` |
| TCR Namespace | `qruiq` |
| Domain for new projects | `*.qruiq.app` (NS on Cloudflare) |

## Migrations on Next.js standalone images (Prisma)

This is a recurring trap when the project uses `next.config.js` `output: "standalone"` (the qruiq Dockerfile template does). The standalone tracer **does not include `prisma/schema.prisma`** in the runtime image, so a Job that runs `npx prisma db push` from that image fails with `Could not find Prisma Schema`.

Two known-good options:

**Option A (preferred) — bake the schema into the image.** Add to the `runner` stage of the Dockerfile (alongside `COPY .next/standalone`):

```dockerfile
COPY --from=builder --chown=nextjs:nodejs /app/prisma ./prisma
```

Then `kubectl exec` or a Job using the same image can run `npx prisma db push` directly. Also pin the version (see below).

**Option B — mount the schema via ConfigMap** (no image rebuild needed):

```bash
kubectl create configmap prisma-schema \
  --from-file=schema.prisma=prisma/schema.prisma \
  -n <APP_NAME>-dev --dry-run=client -o yaml | kubectl apply -f -

JOB=prisma-push-$(date +%s); cat <<EOF | kubectl apply -f -
apiVersion: batch/v1
kind: Job
metadata:
  name: $JOB
  namespace: <APP_NAME>-dev
spec:
  backoffLimit: 1
  ttlSecondsAfterFinished: 300
  template:
    spec:
      restartPolicy: Never
      imagePullSecrets: [{ name: tcr-secret }]
      containers:
        - name: migrate
          image: sgccr.ccs.tencentyun.com/qruiq/<APP_NAME>:<tag-already-in-TCR>
          workingDir: /tmp   # nextjs user can't write /app
          command: ["sh","-c","mkdir -p /tmp/prisma && cp /schema/schema.prisma /tmp/prisma/schema.prisma && cd /tmp && npx -y prisma@<MAJOR>.<MINOR>.<PATCH> db push --accept-data-loss --schema=/tmp/prisma/schema.prisma"]
          envFrom: [{ secretRef: { name: <APP_NAME>-secrets } }]
          volumeMounts: [{ name: schema, mountPath: /schema }]
      volumes:
        - name: schema
          configMap: { name: prisma-schema }
EOF
```

**Always pin the prisma CLI version** to match the project's `prisma` dep — `npx prisma` resolves to the latest on npm, and Prisma 7 removed `datasource.url` from schema files (causes `P1012` validation error). Read the pin from `package.json`:

```bash
PRISMA_VER=$(jq -r '.dependencies.prisma // .devDependencies.prisma' package.json | tr -d '^~')
```

Then `npx -y prisma@$PRISMA_VER db push ...`.

`workingDir: /tmp` matters: the runner stage runs as user `nextjs` (uid 1001) which cannot create directories under `/app`.

## Notes

- Only domains with NS on Cloudflare can route to nginx ingress. `qruiq.app` works; `ufcenter.xyz` (NS on afternic) does not.
- `kubectl get ingress` ADDRESS field is **always** misleading on this cluster — every ingress shows `150.109.21.157`, but actual traffic goes through nginx ingress at `43.173.190.227`. Always check `ingress-nginx-controller` Service EXTERNAL-IP and point DNS there.
- TKE CBS storage only supports `ReadWriteOnce`. For multi-pod shared storage, use CFS (NFS).
- Standard TCR pull secret name in this cluster is `tcr-secret` (the `init-namespace.sh` script creates it). Older `soxgrow` namespace uses `repo` — don't copy that pattern for new projects.

## Common operations

```bash
kubectl get pods -n <namespace>
kubectl logs -f deployment/<project>-web -n <namespace>
kubectl rollout restart deployment/<project>-web -n <namespace>
kubectl set image deployment/<project>-web web=<image>:<version> -n <namespace>
```
