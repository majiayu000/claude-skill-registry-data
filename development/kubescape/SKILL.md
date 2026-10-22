---
name: kubescape
description: Check Kubernetes manifests, Helm charts, Kustomize overlays and live clusters against NSA-CISA, MITRE ATT&CK, CIS (EKS, AKS, GKE, vanilla) and SOC2 with the Kubescape CLI. Covers framework choice, score and severity gates, PR gates that fail only on new findings (--baseline), exceptions that actually suppress, controls configuration, auto-fix, Kubescape's CEL admission policy library, and one-off image scans. Interactive when run without arguments. Use when asked to "scan my manifests", "how secure is my cluster", "run a CIS benchmark", "NSA hardening check", "add a Kubernetes security gate to CI", "accept this finding", "fix what Kubescape found", or "run kubescape". Continuous in-cluster scanning, runtime alerts, NetworkPolicies from traffic → /platform-skills:kubescape-operator. Image CVE gates → /platform-skills:trivy. Admission with Kyverno → /platform-skills:kyverno. Terraform → /platform-skills:checkov.
argument-hint: "[scan|cluster|ci|exceptions|fix|vap|image] [path, chart, framework or control]"
title: "Kubescape Command"
sidebar_label: "kubescape"
custom_edit_url: null
---

Find out how a Kubernetes change or cluster measures up against a security framework, in plain language, and stop new problems at the pull request.

Read `references/kubescape.md` before responding. It holds the verified install, the framework table, gate exit codes, the baseline recipe, how the two exception actions really behave, fix limits, the VAP rollout, and troubleshooting. The working files are in `examples/kubescape`.

The primary cloud for this organisation is `${user_config.primary_cloud}`. If that reads as a literal placeholder or is empty, it is not configured: detect the provider from the cluster, or ask.

## Ownership boundary (enforced at the menu)

| Question | Authoritative command |
|---|---|
| "Does this manifest / chart / cluster meet NSA, MITRE, CIS or SOC2?" | **this command** |
| "Block insecure Kubernetes changes in PRs" | **this command** (`ci`) |
| "Scan continuously, see which CVEs actually load, alert on runtime behaviour, generate NetworkPolicies" | `/platform-skills:kubescape-operator` |
| "Is this image safe to ship?" (CI gate) | `/platform-skills:trivy` |
| "Will this pass admission?" (cluster runs Kyverno) | `/platform-skills:kyverno` |
| "Is my Terraform misconfigured?" | `/platform-skills:checkov` |
| "Is this production-ready overall?" | `/platform-skills:preflight` |

---

## Mode dispatch

Parse the first word of `$ARGUMENTS` as the mode. When `$ARGUMENTS` is empty, or is a question in plain words, run the interactive wizard.

| Mode | What it does |
|---|---|
| `scan` | Score manifests, a Helm chart, a Kustomize overlay or a git URL against a framework |
| `cluster` | Score the live cluster in the current kube context (or several contexts) |
| `ci` | Add a GitHub Actions gate that fails a PR only on findings it introduces |
| `exceptions` | Accept a risk properly: an exceptions entry that suppresses, with a review date |
| `fix` | Preview and apply Kubescape's automatic fixes, then hand-fix the rest |
| `vap` | Enforce a control at admission with Kubescape's CEL policy library (Warn → Deny) |
| `image` | One-off image CVE check (CI image gates live in `/platform-skills:trivy`) |
| _(empty)_ | Interactive wizard |

---

## Step 0 — detect before asking (silent)

Run these quietly and use the answers to skip questions. Never ask what the repository or cluster already tells you.

```bash
command -v kubescape && kubescape version                     # installed? version?
kubectl config current-context 2>/dev/null                     # is there a cluster?
kubectl version -o json 2>/dev/null | jq -r .serverVersion.gitVersion       # -eks- / -gke. → managed distribution
kubectl get nodes -o jsonpath='{.items[0].metadata.labels.kubernetes\.azure\.com/cluster}' 2>/dev/null   # non-empty → AKS
kubectl get nodes -o jsonpath='{.items[0].spec.providerID}' 2>/dev/null   # aws:// azure:// gce:// — a hint only
git ls-files | grep -E '(^|/)(Chart\.yaml|kustomization\.ya?ml)$'          # charts, overlays
git ls-files '*.yaml' '*.yml' | xargs grep -l '^kind:' 2>/dev/null | head  # plain manifests
ls .github/workflows/ 2>/dev/null; ls .kubescape/ 2>/dev/null               # existing CI, exceptions
```

- Kubescape missing → offer the install (laptop: `brew install kubescape`; CI and servers: the verified download in the reference) before anything else.
- Version below 4 → say so: `--baseline`, `--kube-contexts` and the `disable` exception behaviour described here need v4.
- Current context looks like production (name contains `prod`) → confirm before a cluster scan; it is read-only but heavy on the API server for large clusters.

## Interactive wizard

Ask with the `AskUserQuestion` tool when it is available (one question per call, the recommended option first); otherwise print the numbered menu and wait. Three layers; stop as soon as the mode is clear.

### Layer 1 — What do you want to know? (intent, in their words)

```
What are you trying to find out?
  1. "Is this change / chart safe to deploy?"         → scan
  2. "How secure is my cluster right now?"            → cluster
  3. "Stop insecure Kubernetes changes in PRs"        → ci
  4. "We've accepted this risk — stop flagging it"    → exceptions
  5. "Fix what Kubescape found"                       → fix
  6. "Block this at admission"                        → vap  (Kyverno installed? → /platform-skills:kyverno)
  7. "Is this image vulnerable?"                      → image (CI gate? → /platform-skills:trivy)

  Watch the cluster continuously / runtime alerts / NetworkPolicies → /platform-skills:kubescape-operator
```

Pre-select from Step 0: no cluster but manifests → 1; cluster and no manifests → 2; a workflow directory and no Kubescape job → mention 3.

### Layer 2 — Measured against what? (framework, in plain words)

```
What should it be measured against?
  a. General hardening (NSA-CISA)                     → NSA        [recommended for manifests and charts]
  b. Attacker techniques (MITRE ATT&CK)               → MITRE
  c. An audit benchmark (CIS)                         → picked for you: <cis-eks-t1.8.0 | cis-aks-t1.8.0 | cis-gke-v1.9.0 | cis-v1.12.0>
  d. SOC 2 audit evidence                             → SOC2       (Terraform side → /platform-skills:compliance)
  e. Hardening + attacker techniques                  → nsa,mitre  [recommended for CI]
```

Pick the CIS benchmark from the **distribution**, not the cloud: API server `gitVersion` with `-eks-` → EKS, with `-gke.` → GKE, nodes labelled `kubernetes.azure.com/cluster` → AKS, otherwise `cis-v1.12.0`. `providerID` and the primary cloud above are only hints: a self-managed cluster on EC2 also reports `aws://`. When the hints and the signals disagree, or there is no cluster, ask which distribution it is. Say which benchmark and why. Skip this layer for `exceptions`, `fix` and `image`.

### Layer 3 — Only the settings that can hurt

Ask only where a wrong default causes harm; offer the recommended value so Enter accepts it.

- **Gate strictness** (`ci`, or `scan` in a pipeline): "Fail on new High or Critical findings? [Y]". Explain that without a gate Kubescape always exits 0.
- **Existing debt** (`ci`, when a first scan shows more than about 10 failed controls): "Gate only on findings a PR adds (baseline)? [Y]". Brownfield repos need this, or the first PR after rollout fails for problems it did not create.
- **Accepted risk** (`exceptions`): the reason in one sentence and a review date, default 90 days. Never write an exception without both.
- **Fix scope** (`fix`): "Preview only, write fixed copies, or edit in place? [Preview]".

Do not pepper with questions. If the user typed a full command (`/platform-skills:kubescape scan charts/api`), run it.

## Result card (every mode ends with this)

Translate the report; do not paste the raw table. Build it with the `jq` result-card helper in the reference.

```
Kubescape — NSA on charts/payments-api           Score: 45%   (gate: FAIL, 5 High)

Fix first:
  HIGH  C-0057  Privileged container                     payments-api   → securityContext.privileged: false
  HIGH  C-0041  HostNetwork access                       payments-api   → remove hostNetwork: true
  HIGH  C-0012  Credentials in configuration files       payments-api   → move DB_PASSWORD to a Secret (secretKeyRef)
  HIGH  C-0270  CPU limits not set                       payments-api   → resources.limits.cpu
  HIGH  C-0271  Memory limits not set                    payments-api   → resources.limits.memory

Kubescape can fix 5 of 11 automatically.        Next: /platform-skills:kubescape fix
```

One line of "why it matters" per control when the user is new to it (for example, privileged means root on the node). One suggested next command, not a list.

---

## Mode: scan

1. Resolve the target: a path, a chart (`Chart.yaml`), an overlay (`kustomization.yaml`), a git URL, or `-` for stdin.
2. Helm: when `Chart.yaml` lists `dependencies`, build them first and stop on errors (`helm repo add` each `https://` repository, then `helm dependency build`). Kubescape tries itself but only warns on failure and then scans without the subcharts. Pass `--kube-version` from the target cluster when known.
3. Run:

```bash
kubescape scan framework <framework> <target> --format json --output /tmp/kubescape.json
```

4. Print the result card. If the score is 100, say what was not checked: image contents (`image` mode) and host settings (`cluster` with the operator).

## Mode: cluster

1. Confirm the context from Step 0 and the framework from Layer 2.
2. Run (read-only):

```bash
kubescape scan framework <framework> [--include-namespaces a,b] --format json --output /tmp/cluster.json
# several clusters:
kubescape scan framework <framework> --kube-contexts prod-eu,prod-us --fleet-report fleet.json --output cluster.json
```

3. Print the result card, then the skipped count. When controls are skipped for `missing: hostdata…`, say how many and offer `/platform-skills:kubescape-operator install`: on a CIS scan without it, about 40% of controls cannot run.
4. For a fleet, lead with `divergence`: controls that pass on one cluster and fail on another usually mean configuration drift.

## Mode: ci

1. Copy `examples/kubescape/workflows/kubescape.yml` to `.github/workflows/kubescape.yml`.
2. Set `SCAN_PATH` from Step 0, `FRAMEWORKS` from Layer 2, `SEVERITY_THRESHOLD` from Layer 3.
3. If the repository has a different default branch, check `on.push.branches`.
4. Explain the three behaviours: PRs fail only on new findings (baseline from a worktree of the same clone), main reports without gating, expired `disable` exceptions fail the job.
5. Tell the user to make `posture` a required check.
6. Run `zizmor` on the new workflow if available (`/platform-skills:zizmor`).

Never: `kubescape/github-action` (bundles CLI v3.0.21), `tj-actions/changed-files`, unpinned `uses:`, a gate without `--controls-version`, a scan without `--honor-inline-exceptions=false` (a PR could suppress its own finding with a `kubescape.io/skip-controls` annotation), or a `paths` filter on the `pull_request` trigger of a required check (it would stay pending and block merges).

## Mode: exceptions

1. Identify control ID, resource kind, namespace and name from the user or the last report.
2. Ask the reason and review date (Layer 3).
3. Write the entry to `.kubescape/exceptions.json` with `"actions": ["disable"]` and the name ending `-until-YYYY-MM-DD`. Use `"alertOnly"` only when the user wants the finding to keep failing (acknowledged, still tracked). Never any other `actions` form: an empty list, a missing field, a mixed list or a typo all suppress like `disable`.
4. Re-run the scan with `--exceptions` and show the control moving to `passed (w/exceptions)`.
5. Ask whether the exception should also exist in the cluster: `SecurityException` with `expiresAt` → `/platform-skills:kubescape-operator exceptions`.

State plainly: `alertOnly` does not stop a gate; only `disable` does.

## Mode: fix

1. Scan to JSON, then `kubescape fix <report> --dry-run` and translate the stderr output into a short list.
2. Warn about the two changes that break apps: `readOnlyRootFilesystem: true` (writes outside a volume) and `runAsUser: 1000` (image built for another UID).
3. On approval: `--output-dir` for copies, or in place in a clean git tree so `git diff` is the review.
4. List what was not fixed and give the manual fix for each (limits, seccomp, NetworkPolicy, Secrets).
5. Cluster reports: write patched manifests to Git, never pipe to `kubectl apply` on production.

## Mode: vap

1. Check Kubernetes ≥ 1.30 (`kubectl version`) and whether Kyverno runs (`kubectl get crd | grep kyverno`); if it does, recommend `/platform-skills:kyverno` and stop unless the user insists.
2. `kubescape vap list-policies` to find the policy for the control.
3. Install the library CRD-first (reference), bind one namespace with `--control C-XXXX --action Warn --action Audit`.
4. Show the user the warning a violating pod gets (`kubectl run … --dry-run=server`).
5. After an agreed quiet period, rebind with `--action Deny`. State the blast radius and the one-line rollback (`kubectl delete validatingadmissionpolicybinding <name>`).

## Mode: image

1. If the question is "should CI block this image", hand off to `/platform-skills:trivy image`.
2. Otherwise: `kubescape scan image <ref> [--severity-threshold critical]`; the first run downloads the vulnerability database (about a minute).
3. Summarise counts by severity and the top fixable CVEs (package, installed, fixed version).

---

## Agent behavior

### Never do these
- Report a scan as passing because it exited 0 without a gate flag.
- Write an `alertOnly` exception and tell the user the finding is suppressed.
- Write an exception without a reason and a review date.
- Pipe `kubescape fix` output or a VAP binding with `Deny` into a production cluster.
- Paste the raw Kubescape table as the answer.

### Always do these
- Name the framework and why it was chosen.
- Say what the scan did not cover (images, host settings without the operator).
- End with the result card and one next command.
- Pin `--controls-version` in anything that gates.

## Cross-references

- `references/kubescape.md` — full CLI reference
- `/platform-skills:kubescape-operator` — continuous scanning and runtime
- `/platform-skills:trivy` — image gates · `/platform-skills:kyverno` — admission · `/platform-skills:preflight` — overall readiness
