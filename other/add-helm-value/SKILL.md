---
name: add-helm-value
description: Add or change a setting in the Helm charts (deploy/charts/stack or data), or add a cluster add-on (an operator or tool in deploy/platform/addons). Use when a deployment needs a new knob, a per-environment value, or a new in-cluster component.
argument-hint: <value path or add-on name>
---

# Add a Helm value or a platform add-on

Nothing here touches a real cluster: Argo CD applies what's on `master`.
`.claude/rules/infra.md` has the rules; deploy/README.md the layout.

## A value in a chart

1. **Schema first.** `deploy/charts/<stack|data>/values.schema.json` has
   `additionalProperties: false`: add the property with its type, bounds and a
   description, or `helm template` fails.
2. **Default** in the chart's `values.yaml`, with a comment on what it does. Per
   environment: `deploy/environments/<env>/<stack|data>.yaml`. A secret never goes in
   values: it's a SOPS Secret (the add-env-var skill).
3. **Template.** Use it in `templates/`; helpers are in `templates/_helpers.tpl`.
4. **Test.** A helm-unittest case in `deploy/charts/<chart>/tests/` for the rendered
   result, including the default and an override.
5. A new environment also goes in `RELEASE_VALUES` in `scripts/charts.ts`.

## A platform add-on

1. A file in `deploy/platform/addons/<addon>.yaml`: `addon`, `namespace`, and either
   `repoURL` + `chart` + `version` (pinned exactly; the `platform` ApplicationSet in
   `deploy/argocd/appsets/platform.yaml` reads the fields), or `path` for a chart in this
   repo, or `secretsPath` for SOPS manifests. `wave` orders it against the others
   (operators before what uses their resources).
2. Our values for it in `deploy/platform/values/<addon>.yaml`, with memory limits.
3. Renovate follows the chart through the add-on managers in `renovate.json5`; a file
   pattern they don't match needs a custom manager.
4. Everything in-cluster and self-hosted: a managed service is an exception the user
   decides (`.claude/rules/infra.md`).

## Done when

- `bun run charts:check` passes (lint, unit tests, every environment rendered and
  validated with kubeconform, add-ons at their pinned versions); it takes minutes, so in
  the background.
- `bun run k8s:up` and `bun run k8s:smoke` pass locally if the change affects how the
  stack runs (the user starts and stops the local cluster).
- The `security-reviewer` agent reports nothing for anything that opens a port, a route
  or a permission.
