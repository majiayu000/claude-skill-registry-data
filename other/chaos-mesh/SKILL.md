---
name: chaos-mesh
description: "Configures Chaos Mesh for Kubernetes-native chaos engineering - picks fault types (PodChaos, NetworkChaos, StressChaos, IOChaos, TimeChaos, DNSChaos, KernelChaos, HTTPChaos), targets via label selectors, controls blast radius via namespace whitelists + selector filters, schedules via CronJobs, observes via dashboard. Distinct from Litmus by architecture (Chaos Mesh has its own dashboard + workflow orchestration; Litmus uses ChaosCenter UI). Use when the target system runs on Kubernetes and fault experiments should be declared as CRDs in the cluster alongside the workloads they target."
---

# chaos-mesh

## Overview

Per [chaos-mesh-home][cm]:

[cm]: https://chaos-mesh.org/
[cm-helm]: https://chaos-mesh.org/docs/production-installation-using-helm/

> "**Chaos Mesh** is a platform that 'brings various types of fault
> simulation to Kubernetes and has an enormous capability to
> orchestrate fault scenarios.'"

Per [chaos-mesh-home][cm], Chaos Mesh leverages "Kubernetes
CustomResourceDefinitions (CRDs) for seamless integration with
the Kubernetes ecosystem."

## When to use

- The platform is Kubernetes.
- The team wants CRD-native chaos with a built-in dashboard.
- Workflow orchestration matters (sequence + parallel
  experiments).
- Physical machine support needed (Chaosd extension).

If LitmusChaos is already deployed, evaluate stack-fit before
adding Chaos Mesh - both serve similar use cases with different
ergonomics.

## Step 1 - Install

Install with Helm, per [Chaos Mesh Helm install][cm-helm] (pin the chart
`--version` you have validated; the docs recommend the `chaos-mesh`
namespace):

```bash
helm repo add chaos-mesh https://charts.chaos-mesh.org
helm install chaos-mesh chaos-mesh/chaos-mesh -n chaos-mesh --create-namespace --version 2.6.3
```

Avoid piping the mirror's `install.sh` into a shell: it runs unreviewed
remote code with your cluster credentials.

Per [chaos-mesh-home][cm], "no special dependencies required - 
Chaos Mesh deploys directly on Kubernetes clusters, including
minikube and kind."

## Step 2 - Fault types

Per [chaos-mesh-home][cm]:

| CRD              | Effect                                                        |
|------------------|---------------------------------------------------------------|
| `PodChaos`        | Pod kill, container kill, pod failure                         |
| `NetworkChaos`    | Latency, packet loss, partition, bandwidth, corruption        |
| `StressChaos`     | CPU stress, memory stress                                      |
| `IOChaos`         | Disk read/write delay, errors                                  |
| `TimeChaos`       | Clock skew                                                     |
| `DNSChaos`        | DNS lookup failures                                            |
| `KernelChaos`     | Kernel-level fault injection                                   |
| `HTTPChaos`       | HTTP request fault injection                                   |
| `JVMChaos`        | JVM-level (exception, GC pause, method delay)                  |

Plus `Schedule` for cron-style + `Workflow` for orchestration.

## Step 3 - Author a NetworkChaos

```yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: NetworkChaos
metadata:
  name: checkout-network-latency
  namespace: app
spec:
  action: delay
  mode: one                    # or 'all', 'fixed', 'fixed-percent', 'random-max-percent'
  selector:
    namespaces:
      - app
    labelSelectors:
      app: checkout
  delay:
    latency: '500ms'
    correlation: '50'
    jitter: '50ms'
  duration: '5m'
```

Per [chaos-mesh-home][cm], Chaos Mesh provides "selector-based
filtering using labels, annotations, and namespace whitelists to
control 'blast radius' and target specific resources."

## Step 4 - Author a PodChaos

```yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: checkout-pod-kill
  namespace: app
spec:
  action: pod-kill
  mode: fixed-percent
  value: '50'
  selector:
    namespaces:
      - app
    labelSelectors:
      app: checkout
  duration: '60s'
```

`mode: fixed-percent` + `value: '50'` kills 50% of matching pods.

## Step 5 - Workflow orchestration

Per [chaos-mesh-home][cm]: "Workflow Orchestration: Users can
combine serial and parallel experiments to simulate complex,
realistic failure scenarios matching actual system architecture."

```yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: Workflow
metadata:
  name: checkout-resilience-test
  namespace: app
spec:
  entry: combined-chaos
  templates:
    - name: combined-chaos
      templateType: Serial
      deadline: 30m
      children:
        - network-latency-step
        - then-pod-kill-step
        - then-stress-step
    - name: network-latency-step
      templateType: NetworkChaos
      networkChaos:
        action: delay
        mode: all
        selector: { ... }
        delay: { latency: 200ms }
        duration: 5m
    - name: then-pod-kill-step
      templateType: PodChaos
      podChaos:
        action: pod-kill
        mode: one
        selector: { ... }
    - name: then-stress-step
      templateType: StressChaos
      stressChaos:
        mode: all
        selector: { ... }
        stressors:
          cpu: { workers: 4, load: 80 }
        duration: 3m
```

## Step 6 - Dashboard

Per [chaos-mesh-home][cm], Chaos Mesh ships a dashboard with RBAC.

```bash
kubectl port-forward -n chaos-mesh svc/chaos-dashboard 2333:2333
# Open http://localhost:2333
```

The dashboard provides authoring (visual experiment construction),
running, observability, and replay.

## Step 7 - Run + verdict

```bash
kubectl apply -f checkout-network-latency.yaml

# Watch state
kubectl get networkchaos checkout-network-latency -w

# Status / events
kubectl describe networkchaos checkout-network-latency
```

The chaos resource lifecycle is `Created → Running → Stopped`.
Pair with external monitoring (Datadog / Prometheus / Grafana) to
verify the steady-state hypothesis held.

## Step 8 - Physical machine support

Per [chaos-mesh-home][cm]: "Physical Machine Support: Chaosd
(experimental) extends chaos testing to non-Kubernetes
environments through `PhysicalMachineChaos` resources."

For VM / bare-metal targets:

```yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: PhysicalMachineChaos
metadata:
  name: vm-cpu-stress
spec:
  action: stress-cpu
  address:
    - 'http://10.0.0.5:31767'
  duration: 5m
  stress-cpu:
    load: 80
    workers: 4
```

The Chaosd agent runs on the target VM; the K8s CRD remotely
triggers it.

## Step 9 - CI integration

```yaml
- name: Trigger chaos experiment
  run: |
    kubectl apply -f experiments/checkout-network-latency.yaml
    sleep 320  # 5min duration + buffer
    kubectl delete -f experiments/checkout-network-latency.yaml
- name: Check steady-state from Datadog
  run: ./scripts/datadog-verdict.sh
```

## Anti-patterns

| Anti-pattern                                                          | Why it fails                                                              | Fix |
|-----------------------------------------------------------------------|---------------------------------------------------------------------------|-----|
| `mode: all` without scope                                              | All matching pods affected; blast radius too wide.                       | Start with `mode: one` or `fixed-percent: 25`. |
| No `duration`                                                           | Chaos persists until manual cleanup; risky.                              | Always set `duration` (Step 3 example). |
| Targeting `chaos-mesh` namespace                                        | Crashes the chaos infrastructure itself.                                 | Whitelist `app` namespace; deny-list `chaos-mesh`. |
| Disable RBAC on dashboard                                               | Anyone with cluster access can trigger chaos.                           | Per [chaos-mesh-home][cm]: RBAC is on by default - keep it on. |
| Skipping observability integration                                      | Chaos runs but verdict invisible.                                        | Wire dashboard + external monitoring. |

## Limitations

- **Kubernetes only (mostly).** Chaosd is experimental; non-K8s
  is second-class.
- **Per-tool incompatibility.** Chaos Mesh CRDs aren't Litmus
  ChaosEngines.
- **JVM / language-specific chaos.** Available but requires agent
  installation in the target.
- **Resource overhead.** Chaos controller + dashboard pods cost
  cluster resources.

## References

- [cm][cm] - Chaos Mesh overview: K8s-native, fault types,
  selector-based blast-radius control, workflow orchestration,
  dashboard with RBAC, Chaosd for physical machines.
- [cm-helm][cm-helm] - Helm install: `helm repo add chaos-mesh`,
  recommended `chaos-mesh` namespace, `--version` pinning.
- LitmusChaos (references/litmus.md in `chaos-experiment-author`) - sibling K8s
  alternative.
- Gremlin (references/gremlin.md in `chaos-experiment-author`) - multi-platform
  commercial alternative.
- `chaos-experiment-author` - methodology this tool implements.
