---
name: cloud-docker-registry
description: >
  Find and loot exposed container registries — image pull/push, secrets baked in layers, and
  registry misconfig. Load on exposed Docker registry (port 5000, /v2/), a registry URL, harbor/ECR/
  GCR/ACR references, or "container registry". Signals: /v2/_catalog, registry:2, unauth pull/push.
domain: cloud
type: technique
stability: learning
modes: [bugbounty, pentest]
severity: high
owasp: [A05:2021-Security-Misconfiguration]
cwe: [CWE-522, CWE-306]
mitre: [T1525, T1552.001]
tools: [docker, crane, curl, trufflehog]
schema_version: 1
---

# Exposed container registry

## When it applies
A Docker/OCI registry is reachable — a self-hosted registry (`:5000`, `/v2/`), or a cloud one
(ECR/GCR/ACR/Harbor) with weak auth. Images are goldmines: source, configs, and baked-in secrets.

## Why it works
Registries are often deployed without auth ("internal only") or with over-broad pull access. Image
layers preserve everything added at build time — `.env` files, cloud keys, private source,
tokens — even if a later layer deletes them, earlier layers keep them.

## Method
1. **Detect & enumerate**: `curl -s https://registry:5000/v2/_catalog` (repo list) and
   `.../v2/<repo>/tags/list`. `registry:2` banner / an unauth `/v2/` = exposed.
2. **Pull images**: `docker pull registry:5000/<repo>:<tag>` or `crane pull` (no docker daemon).
   Anonymous pull of private images is the finding.
3. **Mine layers for secrets**: `crane export`/`docker save` then scan with `trufflehog filesystem`
   / grep for keys, `.env`, kubeconfig, cloud creds (→ validate with `code-review-secrets-detection`).
4. **Push (critical)**: if anonymous/weak push works, you can poison images (supply-chain) — prove
   with a harmless tag, don't tamper real images.
5. **Cloud registries**: test misconfigured ECR/GCR/ACR policies; leaked registry creds → pull private images.

## Gotchas
- Scan *all* layers/history, not just the final image — secrets hide in intermediate layers.
- Anonymous **push** is critical (supply-chain); anonymous **pull** of private images is high — rate accordingly.
- Only pull what proves the issue; images can be large and contain real data — handle carefully.

## Verify success
Anonymous/unauthorized pull of a private image, a live secret extracted from its layers, or a
successful (harmless) push proving write access.

## References
Docker registry API docs; crane/trufflehog; "hacking Docker registries" write-ups.
