---
name: helm-pro
description: Helm guidance — chart structure, templating, values management, releases, hooks, and chart best practices.
category: development
---

## Overview

Helm is the package manager for Kubernetes: charts bundle manifests with templating, values files customize per environment, and releases track what's deployed with rollback support. For third-party software (databases, ingress controllers, monitoring), Helm charts are the standard distribution format; for your own apps, charts are one packaging option among several.

Helm's templating is powerful and easy to abuse — charts drift into unmaintainable Go-template spaghetti without discipline. This skill covers chart structure, values management across environments, safe release practices, and when to prefer Kustomize or plain manifests instead.

## When to use

- Packaging an application as a Helm chart.
- Managing environment differences with values files.
- Deploying third-party charts (choosing versions, values).
- Debugging templating errors and failed releases.
- Using Helm hooks, tests, and OCI registries.
- Choosing between Helm, Kustomize, and plain manifests.
- Operating Helm releases in production (rollbacks, upgrades).

## Core concepts

- **Charts.** A chart is a directory: `Chart.yaml` (metadata), `values.yaml` (defaults), `templates/` (manifests), optional `charts/` (subcharts). Charts version independently of the app (`version` vs `appVersion`).
- **Values.** `values.yaml` defaults overridden by `-f` files and `--set` flags — later sources win. Per-environment values files (`values-prod.yaml`) are the standard environment mechanism. `--set` for one-offs, files for anything persistent.
- **Templating.** Go templates with Helm's functions (`{{ .Values.replicaCount }}`, `{{ include "chart.name" . }}`). Keep templates readable: named templates (`_helpers.tpl`) for repeated snippets, minimal logic in templates, validation via `required` and `fail`.
- **Release management.** `helm install/upgrade --install` with `--atomic` (rollback on failure) and `--wait`; release history enables `helm rollback`. Releases are namespaced; names should be stable per environment.
- **Hooks.** `pre-install`, `post-upgrade`, `pre-delete` etc. for jobs that run outside the normal lifecycle (DB migrations, backups). Hooks have their own deletion policies — misconfigured hooks linger or never run.
- **Tests.** `helm test` runs test pods defined in `templates/tests/` — smoke tests executed post-install. Cheap verification that the release actually works.
- **Dependencies.** `Chart.yaml` dependencies on other charts (databases, etc.) with version constraints; `helm dependency update` vendors them. Pin versions — floating dependencies break installs.
- **OCI registries.** Charts stored as OCI artifacts (`helm push oci://...`) — chart distribution through the same registry as images, with the same auth and immutability semantics.
- **Lint and template.** `helm lint` catches chart errors; `helm template` renders locally for inspection and diffing. Run both in CI before any install.
- **Values schema.** `values.schema.json` validates values files — catches typos and type errors before they become failed releases. Write schemas for charts others consume.
- **Secrets.** Values files are plaintext — don't put secrets in them. Reference external secret stores, use `--set` from CI secrets sparingly, or template from mounted secrets.
- **Chart sources.** Artifact Hub for discovery; prefer official/verified charts; pin chart versions in dependencies and deployments — `latest` charts are undebuggable.
- **Helm vs Kustomize.** Helm: parameterization and packaging (great for distributing software). Kustomize: overlays without templates (great for your own apps' environment diffs). Many teams use Helm for third-party + Kustomize for first-party.
- **Release naming.** Consistent naming (`<app>-<env>`) so releases are greppable; avoid generating names with timestamps — releases should be stable identities.
- **Dry run and diff.** `helm upgrade --dry-run` and the diff plugin show what will change before it changes — the plan/apply equivalent. Review diffs like code.

## Practical workflow

1. **Structure the chart.** Standard layout; `values.yaml` with documented defaults; `_helpers.tpl` for naming/labels; one template file per resource kind.
   ```
   shop-api/
     Chart.yaml  values.yaml  values-prod.yaml
     values.schema.json
     templates/{deployment,service,ingress,hpa,tests}/  _helpers.tpl
   ```
2. **Write clean templates.** Named helpers for labels/selectors; `required` for mandatory values with clear error messages; keep conditionals shallow.
   ```yaml
   # templates/deployment.yaml (excerpt)
   replicas: {{ .Values.replicaCount }}
   image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
   ```
3. **Manage values per environment.** Base `values.yaml` + `values-prod.yaml` overrides; schema validation; secrets from external stores, never in values files.
4. **Lint, template, diff in CI.** `helm lint`, `helm template` rendering checks, diff against the live release — the review gate before upgrade.
5. **Deploy safely.** `helm upgrade --install --atomic --wait --timeout 10m -f values-prod.yaml`; hooks for migrations with proper delete policies; `helm test` smoke tests after.
   ```bash
   helm upgrade --install shop-api ./shop-api \
     -f values.yaml -f values-prod.yaml \
     --namespace shop-prod --atomic --wait --timeout 10m
   ```
6. **Handle third-party charts.** Pin chart versions; values files for your overrides (never edit the chart); track upstream changes before upgrading.
7. **Use hooks deliberately.** Migration jobs as pre-upgrade hooks with `before-hook-creation` delete policy; verify hook completion in the release pipeline.
8. **Publish and version.** OCI registry for chart storage; semantic versioning for chart changes; changelog per release; deprecate values keys with warnings before removing.

## Common pitfalls

- **Template spaghetti** — deeply nested conditionals and string building; keep logic minimal, validate inputs.
- **Secrets in values files** — plaintext credentials in git; external secret management.
- **Unpinned chart versions** — floating dependencies breaking installs; pin everything.
- **No values schema** — typos becoming failed releases; `values.schema.json` for shared charts.
- **Skipping diff review** — upgrading blind; diff before every upgrade.
- **Non-atomic upgrades** — half-applied releases on failure; `--atomic` for rollback.
- **Hook misconfiguration** — hooks that never run or never clean up; set hook weights and delete policies.
- **Editing third-party charts** — forked charts drifting from upstream; override via values, contribute fixes upstream.
- **`--set` for complex config** — escaping hell; values files for anything non-trivial.
- **Release name instability** — generated names breaking tooling; stable names per environment.
- **Ignoring `helm test`** — no post-install verification; add smoke tests.
- **Chart version vs appVersion confusion** — bumping the wrong one; chart version for chart changes, appVersion for the app.
- **Storing charts in git without registry** — no immutability story; OCI registries for distribution.
