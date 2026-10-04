---
name: darkmatter-gitops-conventions
description: Safe-change playbook for the darkmatter/gitops repo — validation before commit (kubeconform with CI-identical flags, yq for YAML manifests, jq for SOPS JSON, git diff --check), sha-pinned images, KSOPS/SOPS secret editing rules, rollback via revert, and how ArgoCD reconciles. Use for ANY change to darkmatter/gitops (manifests, Helm values, apps/*.yaml, secrets), when asked to bump an image tag, wire a secret, or roll back a deploy. Also use when tempted to kubectl apply/edit/patch anything — the answer is no.
---

# Darkmatter gitops conventions

`darkmatter/gitops` is the single source of truth for the k3s cluster: ArgoCD
app-of-apps, Helm values, KSOPS secrets, network policies, cloudflared routes.
A change is real only when it's committed here — everything else is drift.

## The prime rule

Never mutate the cluster imperatively. No `kubectl apply/edit/patch`, no
`helm upgrade`, no imperative restarts. If a live object disagrees with the
repo, the repo wins and the object is the bug.

- **Reload a deployment**: bump its pod-template config-rev annotation in the
  manifest and commit — not `kubectl rollout restart`.
- **Force ArgoCD to reconcile now**: set the
  `arc.darkmatter.io/reconcile-at: "<current UTC timestamp>"` annotation in
  the manifest.
- **Roll back**: `git revert` the offending commit and push. ArgoCD converges.
  Never "fix forward" live.

## Validate before every commit

Run all three; CI runs them and a red main is worse than a slow commit:

```bash
kubeconform -strict -ignore-missing-schemas -summary <changed manifests>
yq eval '.' <changed file> > /dev/null        # syntax parse
git diff --check                              # whitespace damage
```

For ArgoCD `apps/*.yaml` whose Helm values live in a block scalar, validate
the embedded YAML too:

```bash
yq eval '.spec.sources[0].helm.values | from_yaml' apps/<app>.yaml > /dev/null
```

Assertion scripts must not paper over failures: no `|| true`; use `set +e`
plus explicit `PIPESTATUS[0]` capture when a pipeline's exit code matters.

## Images

Pin by full-commit tag (`sha-<40-hex>`) or digest — never `latest`, never a
branch tag. Bumping an image = a one-line diff that names the commit it ships
in the message. ArgoCD picks it up on sync (~3 min); a changed sandbox/pod
spec hash churns dependent warm pools automatically.

## Secrets (KSOPS/SOPS)

- Secrets live encrypted in-repo as JSON (`*.sops.json`), rendered by KSOPS.
  See [ADR-0011](../../docs/adr/0011-sops-files-as-json.md). Do not add new
  `*.sops.yaml` / `.env.sops`. Convert existing YAML SOPS files when touched.
  Kubernetes Secret JSON is valid for the API.
- Editing: decrypt to a `0600` temp file, edit, re-encrypt, then verify
  structurally (`jq empty` on the decrypted form) and by diffing key NAMES
  only — never print values. Clean up the temp file. Plain non-secret
  manifests stay YAML; keep using `yq` for those.
- Reference secrets by name everywhere else; an inline secret value in any
  manifest or log is an incident.
- Agent/runtime secrets follow the hardened flow (Centaur vault + console
  PUTs), not git — this repo carries infra secrets only.

## ArgoCD expectations

- Sync cadence ~3 min; check the app in ArgoCD rather than re-pushing.
- Stale sync retries: remove the `/operation` field from the Application and
  hard-refresh.
- Critical resources that must survive pruning carry `IgnoreExtraneous` /
  `Prune=false` annotations — respect existing ones when editing nearby.

## Tasks

Track follow-ups in beads (`bd create`), not TODO comments. Reproducibility
is the bar: the cluster must be rebuildable from this repo alone.
