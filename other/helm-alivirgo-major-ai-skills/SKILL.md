---
name: helm
description: "Package Kubernetes applications as Helm charts, configure values and dependencies, and inspect release upgrades or rollbacks."
category: devops
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["helm", "charts", "kubernetes", "values", "templating", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Helm Chart Packaging AI Skill Guide

## Overview & Engine Architecture

Helm packages Kubernetes manifests as **charts**: templates plus a `values.yaml` configuration surface. Releases track what was installed; upgrades render a new revision and apply the diff. Agents write maintainable templates, keep secrets out of committed values, and always render locally before touching a cluster.

```
Chart.yaml + values.yaml + templates/
            |
            v
    helm template / lint
            |
            v
    helm upgrade --install  ->  Kubernetes API
            |
            v
      release history (rollback)
```

## When to use this skill

- Packaging repeated Kubernetes YAML into a chart
- Promoting the same chart across dev/stage/prod with value files
- Debugging failed hooks or bad template rendering
- Vendoring chart dependencies

## Operational directives

1. Run `helm lint` and `helm template` before every install/upgrade.
2. Treat `values.yaml` as public defaults; inject secrets via `--set-file`, sealed secrets, or external secret stores.
3. Pin dependency chart versions in `Chart.yaml` / `Chart.lock`.
4. Prefer `upgrade --install` with an explicit `--namespace` and `--create-namespace` when intentional.
5. Keep templates readable: named helpers in `_helpers.tpl`, no copy-paste label blocks.

## Chart layout

```text
mychart/
  Chart.yaml
  values.yaml
  values.schema.json   # optional but valuable
  templates/
    _helpers.tpl
    deployment.yaml
    service.yaml
    ingress.yaml
  charts/              # vendored deps
  Chart.lock
```

`Chart.yaml` sketch:

```yaml
apiVersion: v2
name: mychart
description: Example API chart
type: application
version: 0.3.0
appVersion: "1.4.2"
dependencies:
  - name: redis
    version: 19.0.0
    repository: https://charts.bitnami.com/bitnami
    condition: redis.enabled
```

## Command loop

```bash
helm create mychart
helm dependency update ./mychart
helm lint ./mychart
helm template mychart ./mychart -f values.prod.yaml > /tmp/render.yaml
helm upgrade --install mychart ./mychart -n apps --create-namespace -f values.prod.yaml
helm history mychart -n apps
helm rollback mychart 2 -n apps
```

## Common failure modes

| Problem | Cause | Fix |
| --- | --- | --- |
| YAML parse error after render | Bad indentation in template | `helm template` and read line |
| Hooks never complete | Job hook fails / wrong weight | `kubectl logs` on hook pods |
| Values ignored | Wrong `-f` file or nested key typo | `helm get values` |
| Subchart not present | Missing `dependency update` | `helm dependency build` |

## Best practices

- Provide a `values.schema.json` for required keys when teams are large.
- Document every non-obvious value in comments or a VALUES.md.
- Use `lookup` sparingly - it makes charts cluster-dependent and harder to test.
- Separate cluster-wide operators from app charts.

## Limitations

- CRDs and operator installs often need special ordering beyond a single chart.
- Helm is not a secret manager; do not encode production passwords in Git values.
- Library charts and OCI registries add auth steps specific to the org.

## Related skills

- `@kubernetes` - raw manifests and debugging
- `@argocd` - GitOps delivery of Helm releases
- `@docker` - images referenced by charts
