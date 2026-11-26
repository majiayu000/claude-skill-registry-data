---
name: kubernetes-conventions
description: "Kubernetes conventions for how a workload reaches the cluster, how namespaces and CRDs are organised, and the baseline every workload meets: resources, probes, non root, secrets, default deny network policy. Use when installing, changing or reviewing anything that runs in Kubernetes."
---

# Kubernetes conventions

How workloads reach the cluster and how they are organized.

## When to use

- Installing or changing a component in the cluster.
- Reviewing infrastructure code that touches Kubernetes.
- Deciding where a component belongs and what namespace it gets.

## Rules

### Installation

- A workload is a `helm_release` from OpenTofu: the upstream chart where one is usable, otherwise
  a chart of our own. Never a raw manifest applied by hand.
- A handful of core objects with exactly one purpose are typed Kubernetes provider resources
  instead of a chart: Namespace, ConfigMap, Secret, ServiceAccount, RBAC, StorageClass,
  RuntimeClass, PriorityClass. A chart for three objects with no values interface is a release to
  maintain for nothing.
- `kubernetes_manifest` is avoided. It needs a live cluster to produce a plan, which couples every
  plan to the API being reachable. State the reason explicitly on the rare resource that needs it.
- Chart versions are pinned and raised by Renovate. Values live in the calling code, not in
  defaults that drift silently.

### Namespaces

- One namespace per topic, named after the topic. Every component of a topic shares it, not one
  namespace per component.
- Every release of a topic goes into that topic namespace, CRD releases included.
- Namespaces come from one place only: a dedicated namespace resource. Never `create_namespace =
  true` on a `helm_release`, and turn off any chart option that would create one.

### CRDs

- CRDs are installed by a dedicated `install-crds` chart, one release per component, in the topic
  namespace. It applies the pinned bundle server side and waits for every CRD to be Established
  before the release is considered done.
- No chart ever owns a CRD. `skip_crds = true` (or the chart's equivalent) on every release whose
  chart ships CRDs. A chart that renders CRDs from its templates instead has them dropped from the
  rendered manifest before install and handed to their own `install-crds` release.
- A Helm owned CRD takes every custom resource of its kind with it on an uninstall or a rename.
  Verify by listing CRDs with their owning release; every one has to come back unowned.
- The exception is a CRD an operator creates itself at runtime, from a custom resource it
  reconciles and removes itself. That is the operator's own teardown, not a chart accident, and
  `install-crds` does not duplicate it.

### External routing

- A chart exposes a workload externally through an `Ingress` or a Gateway API `HTTPRoute`,
  never both for the same hostname. Picking one is a deliberate choice, not a migration path.
- `Gateway`, `HTTPRoute` and the rest of the Gateway API are CRDs. They follow the CRDs rule
  above: a dedicated `install-crds` release installs the bundle once per cluster, no chart that
  renders an `HTTPRoute` ships it.
- An `HTTPRoute` names its `Gateway` through `parentRefs`. The `Gateway` usually lives in a
  different, platform owned namespace than the `HTTPRoute`, so `parentRefs` is a cross
  namespace reference by design.
- The `Gateway`'s `allowedRoutes` decides which namespaces and kinds may attach to it. A
  chart's `HTTPRoute` only works where the cluster's `Gateway` allows it. The chart owns the
  `HTTPRoute` and its hostnames; the cluster owns the `Gateway` and that decision.
- TLS for an `Ingress` is a `tls` block on the `Ingress` itself, so the chart owns the
  certificate configuration. TLS for an `HTTPRoute` terminates on the `Gateway`'s listener, so
  the cluster owns it; an `HTTPRoute` carries no `tls` field of its own.

### Workloads

- Resource requests always, limits where the workload tolerates them. State the reasoning when a
  limit is left off.
- Liveness and readiness probes, plus a startup probe where startup is slow.
- Run as non root, read only root filesystem where the image supports it, capabilities dropped,
  no privilege escalation.
- Standard labels and annotations: name, instance, version, component, part-of, managed-by.
- A secret reaches a pod through the secret manager operator, never a plain `Secret` manifest with
  a value written into it.
- A `NetworkPolicy` default denies ingress and egress per namespace, with explicit allows for what
  the namespace actually needs.
- `kubeconform` (or the chart's equivalent schema check) runs in CI against every rendered
  manifest.

## Guardrails

- Never set `create_namespace = true`.
- Never let a chart own a CRD it ships, the Gateway API kinds included.
- Never put a secret's value directly into a `Secret` manifest.
- Never skip resource requests, probes or the non root defaults without stating why.

## Config

- `iac`: infrastructure tool for the `helm_release` and typed resources. Default: `opentofu`.

## References

- `opentofu-conventions` for the OpenTofu side of `helm_release` and the Kubernetes provider.
- `helm-chart` for authoring a chart of our own.
- `k8s-debug` for diagnosing a workload that is not behaving as installed.
