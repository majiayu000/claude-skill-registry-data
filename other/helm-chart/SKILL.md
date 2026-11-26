---
name: helm-chart
description: "Creates or changes a Helm chart with a documented values interface, templates that render for every supported configuration, and lint, kubeconform and helm-unittest verification. Use when writing, changing or reviewing a Helm chart."
---

# Helm chart

Write a chart that renders correctly for every documented combination of values.

## When to use

- A repository ships a chart for its own application.
- A chart is needed for a public tool that has none.
- An existing chart needs a change or a review.

## Steps

1. Define the values interface first: what is configurable, what is required, what the defaults
   are. Defaults must produce a working installation on a normal cluster.
2. Lay out the chart: `Chart.yaml`, `values.yaml`, `values.schema.json`, `templates/`,
   `README.md`, `tests/` for the helm-unittest suite.
3. Templates:
   - a `_helpers.tpl` with name, fullname, labels and selector labels, used everywhere.
   - the standard labels, including `app.kubernetes.io/version` and the chart version.
   - no namespace in a template, the release decides the namespace.
   - every object guarded by its feature flag, no orphaned object when a feature is off.
   - external routing is two feature flags: an `Ingress` values block and an `HTTPRoute` values
     block, both default off. A default install renders neither, so there is no external route
     until one is chosen. Both on fails the render with `fail`, naming which one to turn off.
   - an enabled `HTTPRoute` sets a `parentRefs` entry naming its `Gateway`. See
     `kubernetes-conventions` for the cross namespace reference this usually is and the
     `Gateway`'s `allowedRoutes`.
   - `Ingress` carries its own `tls` block, so the chart owns that certificate configuration.
     `HTTPRoute` carries none; its TLS lives on the `Gateway`'s listener, owned by the cluster,
     see `kubernetes-conventions`.
   - resources, probes, security context and service account configurable with safe defaults.
   - a checksum annotation on the pod template for a ConfigMap or Secret that must trigger a
     restart.
   - no CRD in `templates/`. CRDs are a separate concern, see `kubernetes-conventions`. The
     Gateway API kinds, `Gateway` and `HTTPRoute` included, are CRDs and fall under this same
     rule.
4. Keep `values.schema.json` in sync with `values.yaml` so a misconfiguration fails early.
5. Verify and report the real output:
   - `helm lint`. It cannot see a render-time `fail`: that call is logged, not propagated, and
     the exit code stays zero. A lint pass proves nothing about a guard built on it.
   - `helm template` for the default values and for every documented non default combination.
   - a values override documented as changing a default map is asserted to replace it: the new
     key present and the default key absent. Helm merges maps key by key, so an assertion on the
     new key alone passes while the default silently survives, which widens or narrows the
     result without changing the test.
   - for every render-time guard, a must-fail set: the combinations it must reject. Render them
     with `helm template` and assert the failure, not merely the render. Removing the guard must
     turn this check red on its own.
   - `kubeconform` (or an equivalent schema check) on the rendered output. Its default schema set
     has no Gateway API schemas. A chart that renders `HTTPRoute` or `Gateway` adds a second
     `-schema-location` pointing at a community CRD schema catalog, keyed by group, kind and
     version, alongside the default location.
   - `helm-unittest` suites in `tests/*_test.yaml`, one case per values combination, asserting what
     the rendered output says. Schema validity is `kubeconform`'s job, the decisions the chart
     encodes are not. Never render a chart in a throwaway script to grep the output.
   - for external routing specifically, the must-fail set has three cases: one asserts the
     `Ingress` flag renders an `Ingress` and no `HTTPRoute`, one asserts the `HTTPRoute` flag
     renders an `HTTPRoute` and no `Ingress`, one asserts both flags on fails the render. Keep
     each as a `helm-unittest` case and as a must-fail render. The two must agree before a guard
     can be trusted.
   - `helm-unittest` is a Helm plugin, not in `mise`'s curated registry. Pin it as a generic
     GitHub release backend entry in `mise.toml` instead of an ad hoc `helm plugin install`,
     version pinned the same way as every other tool. A task target builds the plugin directory
     Helm expects around that pinned binary and sets `HELM_PLUGINS` to it before every run. Do
     this in a task, not a postinstall hook: the hook only fires on a fresh install, not on a
     cache hit, and skipping it made the check flaky in CI.
6. Document the chart `README.md`: purpose, prerequisites, the values table, upgrade notes, and
   the uninstall behaviour including what stays behind.
7. Version the chart with the repository's release tool: release-me's helm updater writes
   `Chart.yaml` directly, release-please names it under `extra-files`. Chart version and
   application version are separate fields and both stay current.
8. Publish the chart as an OCI artifact from this repository's own release workflow, named and
   shaped per `ci-conventions`. Where no publish step exists yet, reference the chart inline or
   by path, and say so.

## Guardrails

- No CRD in a chart's templates.
- No namespace hardcoded in a template.
- No feature flag that leaves an orphaned object behind when turned off.
- Never claim `helm lint`, `helm template` or `helm-unittest` passed without having run them.
- `helm lint` never covers a render-time guard. A chart relying on lint alone for one is relying
  on nothing.

## References

- `kubernetes-conventions` for CRDs, namespaces, external routing and the workload baseline.
- `opentofu-conventions` for the `helm_release` that installs the chart.
- a community CRD schema catalog for `kubeconform`'s Gateway API schemas, for example
  <https://github.com/datreeio/CRDs-catalog>.
