---
name: kubescape-operator
description: Install, tune and troubleshoot the Kubescape operator for continuous in-cluster security — posture scans on every change, vulnerabilities filtered to packages that actually load (relevancy), eBPF runtime threat detection against learned container profiles, NetworkPolicies generated from observed traffic, SecurityException resources with an expiry, and Prometheus metrics and alerts. Flux or Argo CD install with a capability matrix, preflight for kernel and overlap with Falco or Trivy Operator, upgrade and rollback. Interactive when run without arguments. Use when asked to "install kubescape in the cluster", "continuous kubernetes security scanning", "which CVEs actually run", "runtime alerts for containers", "generate network policies from traffic", "kubescape operator not working", or "node-agent crashloop". One-off scans, CIS audits and the PR gate → /platform-skills:kubescape. Falco rules → /platform-skills:runtime-security. Trivy Operator → /platform-skills:trivy.
argument-hint: "[install|vulns|runtime|netpol|exceptions|metrics|debug] [namespace or workload]"
title: "Kubescape Operator Command"
sidebar_label: "kubescape-operator"
custom_edit_url: null
---

Run Kubescape inside the cluster: posture that updates itself, CVEs ranked by whether they load, alerts on behaviour a container never showed, and NetworkPolicies drafted from real traffic.

Read `references/kubescape-operator.md` before responding. It holds the preflight, the capability matrix and install profiles, the scanner image override, result commands, runtime and NetworkPolicy details, exceptions, metrics and troubleshooting. The working files are in `examples/kubescape-operator`.

The GitOps engine for this organisation is `${user_config.gitops_engine}`. If that reads as a literal placeholder or is empty, it is not configured: detect Flux (`kubectl get crd helmreleases.helm.toolkit.fluxcd.io`) or Argo CD (`kubectl get crd applications.argoproj.io`), or ask.

## Ownership boundary (enforced at the menu)

| Question | Authoritative command |
|---|---|
| "Scan continuously, keep results in the cluster" | **this command** |
| "Which CVEs are in code that actually runs?" | **this command** (`vulns`) |
| "Alert on unexpected container behaviour" | **this command** (`runtime`), or `/platform-skills:runtime-security` where Falco runs |
| "Draft NetworkPolicies from traffic" | **this command** (`netpol`) |
| "Score the cluster now / CIS audit / PR gate" | `/platform-skills:kubescape` |
| "CVE reports with Trivy Operator" | `/platform-skills:trivy k8s` |
| "Dashboards and alert routing" | `/platform-skills:observability` |

---

## Mode dispatch

Parse the first word of `$ARGUMENTS` as the mode. When `$ARGUMENTS` is empty, or is a question in plain words, run the interactive wizard.

| Mode | What it does |
|---|---|
| `install` | Preflight, pick a profile, write the Flux (or Argo CD) manifests, install, verify, upgrade or roll back |
| `vulns` | Read and rank vulnerability results; on-demand scan; private registries |
| `runtime` | Enable detection, check learning progress, bind rules, route alerts, test an alert |
| `netpol` | Turn a generated policy into a reviewed NetworkPolicy in Git |
| `exceptions` | Accept a risk in the cluster: `SecurityException` with reason, author, expiry |
| `metrics` | Exporter, ServiceMonitor, alert rules |
| `debug` | Diagnose an operator that installs but misbehaves |
| _(empty)_ | Interactive wizard |

---

## Step 0 — detect before asking (silent)

```bash
kubectl config current-context
kubectl version -o json | jq -r .serverVersion.gitVersion            # >= 1.28
kubectl get nodes -o jsonpath='{range .items[*]}{.status.nodeInfo.kernelVersion}{"  "}{.spec.providerID}{"\n"}{end}' | sort -u
kubectl -n kubescape get helmrelease,deploy,ds 2>/dev/null           # already installed? which profile?
kubectl get crd | grep -E 'helm.toolkit.fluxcd.io|argoproj.io|monitoring.coreos.com|kyverno'
kubectl get ds -A | grep -iE 'falco|tetragon'                       # another eBPF agent
kubectl get deploy -A | grep -i trivy-operator                      # another CVE operator
```

Then, only if a node-agent profile is in play, run the kernel preflight from the reference on one node per node image (`CONFIG_FANOTIFY_ACCESS_PERMISSIONS`, `CONFIG_DEBUG_INFO_BTF`). Tell the user what you found in one short block before the first question, for example:

```
Cluster: prod-eu-west-1 (EKS, Kubernetes 1.33, 3 node images)
Flux: yes · Prometheus Operator: yes · Falco: yes (daemonset falco) · Trivy Operator: no
Kernel: fanotify permissions ✔ on all node images
Kubescape: not installed
```

## Interactive wizard

Ask with the `AskUserQuestion` tool when it is available (one question per call, recommended option first); otherwise print the numbered menu and wait.

### Layer 1 — What do you want?

```
What do you want Kubescape to do in this cluster?
  1. "Install it" / "change what it does"                  → install
  2. "Show me which vulnerabilities actually matter"       → vulns
  3. "Alert me when a container does something odd"       → runtime
  4. "Write NetworkPolicies from real traffic"             → netpol
  5. "We accept this risk in the cluster"                  → exceptions
  6. "Get it into Prometheus / Grafana"                    → metrics
  7. "It's installed but something is wrong"               → debug

  Just a score or a CIS audit right now → /platform-skills:kubescape cluster
```

Not installed and the user picked 2–6 → say it needs `install` first and offer it.

### Layer 2 — Install profile (install only)

Offer the profiles from the reference, pre-selected from Step 0:

```
Which profile?
  a. Full — posture, relevancy-ranked CVEs, runtime alerts, NetworkPolicies    [recommended: supported kernel, no Falco]
  b. Full without runtime alerts — keep Falco for alerting                     [recommended: Falco detected]
  c. Posture + CVEs, no node-agent — any kernel, no privileged DaemonSet       [required: kernel lacks fanotify permissions]
  d. Posture only — Trivy Operator keeps CVEs                                  [recommended: Trivy Operator detected]
```

State why the recommended one fits, in one line. Never offer a node-agent profile on nodes that failed the kernel preflight: the install would fail and Flux would uninstall the release.

### Layer 3 — Only the settings that can hurt

- **Overlap** (detected Falco or Trivy Operator): "Turn off Kubescape's <runtime alerts | CVE scanning> so each signal has one owner? [Y]".
- **Learning period** (`runtime`): "Profiles learn for 24h before anomaly rules fire. Keep 24h? [Y]" Shorter means more false alerts.
- **Cluster name** (`install`): "Name this cluster in reports? [<context name>]". The chart default `cluster` makes clusters indistinguishable.
- **Alert destination** (`runtime`): logs only (default), Alertmanager or syslog. HTTP only with a Kubescape backend configured (`server` plus credentials); chart 1.40.4 ignores the HTTP URL otherwise.

## Status card (every mode ends with this)

```
Kubescape operator — prod-eu-west-1                      chart 1.40.4 · scanner v4.0.16
Posture      ✔ 214 workloads scanned · 3 critical · 41 high      last scan 12m ago
CVEs         ✔ relevancy on · 2 critical in loaded packages (of 31 total)
Runtime      ✔ 38/41 profiles completed · 0 alerts in 24h
NetPol       ✔ 41 generated · 0 applied from Git yet
Exceptions   2 active · next expiry 2026-12-31 (payments-api C-0237)

Next: /platform-skills:kubescape-operator netpol payments
```

Build it from `kubectl get workloadconfigurationscansummaries -A`, `vulnerabilitymanifestsummaries -A`, `containerprofiles -A` annotations, `generatednetworkpolicies -A`, `se -A`/`cse`. Show only lines for enabled capabilities; one next command.

---

## Mode: install

1. Step 0 and the profile (Layer 2).
2. Copy `examples/kubescape-operator/flux/` into the user's GitOps path; apply the profile's capability changes; set `clusterName`; keep `version` exact and `kubescape.image.tag` at v4.0.16 (or later) — the bundled v4.0.13 scanner produces no results; keep `global.enableClusterWideSecretAccess: false` (the chart default `true` lets the scanner and operator read every Secret in the cluster) and ask for explicit approval before turning it on.
3. Argo CD: same values in an `Application` (`helm.valuesObject`, `ServerSideApply=true`).
4. Commit, reconcile, then verify: HelmRelease Ready, pods, APIService `Available`, `kubescape operator scan configurations` followed by summaries appearing.
5. Restart workloads once if runtime capabilities are on, so profiles reach `complete`.
6. Print the status card, the blast radius (privileged DaemonSet per node, fail-open admission webhook, kubevuln memory) and the rollback (`flux suspend`, `git revert`).

Upgrade: bump `version` in a PR; read the release notes; compare the new bundled scanner tag with the override.

## Mode: vulns

1. `kubectl get vulnerabilitymanifestsummaries -A` → rank by `critical.relevant` then `high.relevant` (with relevancy) or by `all` (without, and say so).
2. Top five workloads: image, critical/high, fixable count. Image CI gate → `/platform-skills:trivy`.
3. On demand: `kubescape operator scan vulnerabilities --include-namespaces <ns>`.
4. Private registry pulls failing → `imageScanning.privateRegistries.credentials` from a managed secret.

## Mode: runtime

1. Preflight passed? Falco on the same nodes? (Layer 3 overlap.)
2. `capabilities.runtimeDetection: enable`, `alertCRD.installDefault: true`; one node pool first.
3. Learning: list `containerprofiles` with `kubescape.io/status` and `kubescape.io/completion`; explain `ready` = still learning, `completed` = active.
4. Bindings: keep `all-rules-all-pods`. A binding cannot reach a namespace in `excludeNamespaces` (node-agent never traces it). To narrow a noisy namespace (CI runners) to signature rules, use the opt-in `examples/kubescape-operator/ci-runners/` in two steps: first its binding (after the operator is Ready; Flux `dependsOn`), then switch the operator's Kustomization to `ci-runners/release/`, which adds the post-renderer that removes the namespace from the default binding. Never the other way round, and never in the base install.
5. Alerts: logs, Alertmanager or syslog exporter values (HTTP needs backend submission; see the reference).
6. Prove it: after `completed`, `kubectl exec` into a test pod and show the R2000/R0001 alert in `kubectl -n kubescape logs ds/node-agent`.

## Mode: netpol

1. `kubectl -n <ns> get generatednetworkpolicies`; pick the workload (`<kind>-<name>`).
2. Extract `.spec`. Use `policyRef` (`dns`, `server`) to identify each destination, then write in-cluster peers as `podSelector`/`namespaceSelector` and external ones as a reviewed `ipBlock` CIDR — NetworkPolicy has no hostname peers (FQDN rules need a CNI-specific policy such as Cilium `toFQDNs`). The policy selects only this workload, so it isolates only these pods. Add a namespace-wide default-deny later, once every workload in the namespace has a reviewed allow policy and its traffic is validated; earlier, it cuts traffic for pods that have none yet.
3. Ask how long the workload has run; under one full traffic cycle (daily jobs, weekly reports) → wait.
4. Commit for the GitOps reconciler; one namespace at a time; rollback = revert. Never `kubectl apply` the generated object to production.
5. Hardening the rest of the namespace → `/platform-skills:kubernetes`.

## Mode: exceptions

1. Control ID, kind, name, namespace (from the last summary or the user); reason; author; expiry (default 90 days).
2. Write a `SecurityException` from `examples/kubescape-operator/security-exception.yaml` (`ClusterSecurityException` with `namespaceSelector` for many namespaces); `action: ignore`, or `alert_only` to keep it visible.
3. Confirm `capabilities.riskAcceptance: enable`; apply through Git; show the control at `passed (w/exceptions)` after the automatic rescan.
4. Remind: a file exception in CI wins over this for the same control and resource.

## Mode: metrics

1. `capabilities.prometheusExporter: enable`; ServiceMonitor with the Prometheus Operator, otherwise `configurations.prometheusAnnotations: enable`.
2. Apply `examples/kubescape-operator/prometheusrule.yaml`; fix the `release` label to the user's Prometheus ruleSelector.
3. Without relevancy, explain why `relevant` series are 0 and the fallback alert exists.
4. Dashboards → `/platform-skills:observability`.

## Mode: debug

Classify, then follow the matching troubleshooting entry in the reference:

| Symptom | First command | Usual cause |
|---|---|---|
| node-agent CrashLoopBackOff | `kubectl -n kubescape logs ds/node-agent --previous \| grep -i fanotify` | runc path (`global.overrideRuntimePath`) or kernel without fanotify permissions |
| Installed, no results | `kubectl -n kubescape logs deploy/kubescape \| grep 'scanning failed'` | bundled scanner v4.0.13 (`framework 'C-0042' not found`) |
| HelmRelease gone / InstallFailed | `kubectl -n kubescape get hr kubescape -o jsonpath='{.status.conditions}'` | node-agent not Ready → Flux uninstall remediation |
| APIService unavailable | `kubectl get apiservice v1beta1.spdx.softwarecomposition.kubescape.io` | storage starting or out of memory |
| Profiles stay `partial` | `kubectl get containerprofiles -n <ns>` annotations | pods older than node-agent → restart |
| No metrics | port-forward the exporter, `curl /metrics` | ServiceMonitor selection, or scans failing |

Use the systematic order: evidence first, one hypothesis, smallest test, then the fix with verification and rollback.

---

## Agent behavior

### Never do these
- Enable a node-agent capability on nodes that failed the kernel preflight.
- Enable `remediation` or `autoUpgrading`.
- Turn on `global.enableClusterWideSecretAccess` without explicit security approval.
- Install with the chart's bundled scanner (v4.0.13) and call it done.
- Apply a generated NetworkPolicy directly to production.
- Use `kubectl get applicationprofiles` or `networkneighborhoods` (removed); use `containerprofiles`.
- Run Kubescape runtime detection and Falco on the same nodes without saying so.

### Always do these
- Show the Step 0 findings before the first question.
- State blast radius and rollback for install and upgrade.
- End with the status card and one next command.

## Cross-references

- `references/kubescape-operator.md` — full operator reference
- `/platform-skills:kubescape` — CLI, CIS audits, PR gate, VAP
- `/platform-skills:runtime-security` · `/platform-skills:trivy` · `/platform-skills:fluxcd` · `/platform-skills:observability`
