---
name: talos-ops
description: "Operates a Talos cluster whose machine configuration, bootstrap and upgrades run as OpenTofu resources, one node at a time, with a health and etcd quorum gate between nodes. Use when upgrading Talos or Kubernetes, reconfiguring a node, bootstrapping a cluster, or diagnosing a node with talosctl."
---

# Talos operations

Change nodes one at a time through the provider and never lose etcd quorum.

## When to use

- Changing machine configuration, or upgrading Talos or Kubernetes.
- Bootstrapping etcd once a cluster's nodes already have Talos installed.
- A node is unhealthy and needs `talosctl` diagnostics or emergency intervention.

## Steps

### Ownership

- OpenTofu, through the talos provider: machine configuration, the image factory schematic and
  installer image, the resource that applies configuration and drives the Talos and the
  Kubernetes upgrade, and the one time etcd bootstrap.
- `talosctl`, read only: health, logs, `dmesg`, service and certificate state. Reach for it in
  an emergency only, a node the provider cannot reach or recovery from an etcd snapshot, and
  state the reason first.
- The operator's own talosctl config: retrieved with `talosctl` against the running cluster, or
  written by a resource through a write-only attribute. Never printed, never from an output.
- The kubeconfig an upgrade task needs: produced by an `ephemeral` resource and handed to the
  provider through a write-only attribute, so it never lands in state. See
  `opentofu-conventions` for the write-only pattern.

1. Establish the baseline: `talosctl health`, etcd member health, node list with versions, and
   a verified etcd backup before any control plane change.
2. Read the upstream release notes for the target version. Note deprecations and ordering.
3. Plan the order: workers first, control planes last, one node at a time. State the plan
   before the first node.
4. A machine configuration change is a diff in the OpenTofu code, never an ad hoc `talosctl
   patch` or `talosctl edit`. Every apply follows `tofu-plan`: a saved plan file, read in full,
   confirmed for that node before it runs.
5. Apply one node at a time: a targeted apply against that node's resource. Never a plain apply
   that lets every node's resource change together.
6. Per node: confirm health and quorum are green, apply, wait for the node to report Ready and
   for etcd to be healthy again, check kubelet and any pending CSR, confirm workloads
   rescheduled. Only then move to the next node, control planes last.
7. An upgrade that reboots a node drains it first and uncordons it after, through the
   `drain_on_upgrade` flag on the task that wraps the upgrade. Do not cordon or drain by hand
   around a provider driven upgrade.
8. Stop on the first anomaly. Do not continue a rolling operation on a degraded cluster, and do
   not parallelize nodes to save time.
9. Afterwards: report versions, cluster health, etcd health, and anything that needed manual
   intervention. State the rollback plan if the operation is not complete.

## Guardrails

- Never run `talosctl reset`.
- Never change more than one node's configuration at a time.
- Never patch a node's config ad hoc. Change the OpenTofu code and apply it.
- Never skip the etcd backup check before a control plane change.
- Never hand write a talosconfig or a kubeconfig, and never read either through an output or
  `tofu output`. Use the write-only pattern instead.
- Never continue a rolling operation past an anomaly to finish faster.

## References

- `kubernetes-conventions` for what runs on top of the cluster.
- `opentofu-conventions` for the write-only pattern.
- `tofu-plan` for the plan and apply workflow each node's apply follows.
