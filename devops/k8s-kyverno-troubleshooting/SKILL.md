---
name: k8s-kyverno-troubleshooting
description: >-
  Use when Kyverno blocks, changes or fails to police resources in Kubernetes: "admission
  webhook \"validate.kyverno.svc-fail\" denied the request", "resource ... was blocked
  due to the following policies", "Policy ... failed" from a ValidatingPolicy, a policy
  that should block but only reports (Audit), PolicyReports with failures, a policy that
  is not Ready, mutate or generate rules that do nothing, UpdateRequests stuck, or
  "failed calling webhook" for kyverno when its pods are down. Covers ClusterPolicy and
  Policy (kyverno.io) and the CEL policies (policies.kyverno.io). Investigates with
  kubectl get, describe, events and logs, and proposes fixes. Reads first and asks
  before changing anything.
license: Apache-2.0
metadata:
  verified-with: "kubernetes 1.37, kyverno 1.19"
  verified-on: "2026-10-24"
---

# Kyverno troubleshooting

Find out why Kyverno denies, changes or does not police a resource, and propose a fix.
**Read first, ask before changing.** Run the investigation commands freely. Run a
command under an "Ask first" line only after the user approves that exact command; if
your credentials do not allow it, give it to the user to run. Never run a "Proposed
fix"; hand it to the user.

Kyverno runs as admission webhooks plus background controllers. Two policy families
exist side by side:

- **ClusterPolicy and Policy** (`kyverno.io/v1`): rules with `validate`, `mutate`,
  `generate` or `verifyImages`. Deprecated in Kyverno 1.19 and planned for removal in
  1.20; the API server prints a deprecation warning for them.
- **CEL policies** (`policies.kyverno.io/v1`): ValidatingPolicy, MutatingPolicy,
  GeneratingPolicy, DeletingPolicy, ImageValidatingPolicy, and their `Namespaced*`
  variants.

A policy is a cluster-wide guardrail someone chose on purpose. The usual fix is to make
the resource comply, not to weaken the policy; changing or excepting a policy is a
decision for its owners.

The commands use placeholders: `my-namespace`, `my-app`, `my-policy` and `my-rule`.
Replace them with the real names. Never read Secrets (policies can reference them for
image verification or context; read their names only).

## When to use

- Applying a manifest, a Helm install or a GitOps sync fails with a Kyverno denial.
- A resource is admitted although a policy should have blocked it.
- PolicyReports show `FAIL` results, or a policy is not Ready.
- A mutate or generate rule does not change or create what it should.
- Every create or update fails with `failed calling webhook` naming kyverno.

Hand-offs, by skill name. When the evidence points elsewhere, continue with that skill;
if it is not installed, keep going with the steps here and tell the user which skill
would help:

- The Kyverno pods crash or stay Pending: `k8s-workload-troubleshooting`.
- A different admission controller denies the request (Gatekeeper, a cloud policy
  add-on): `k8s-gatekeeper-troubleshooting`.

## Investigate

Work through the steps in order. Stop when you have the cause and its evidence.

**1. Read the denial** the user got. It names the webhook, the policy and the rule:
`validate.kyverno.svc-fail` (ClusterPolicy and Policy) or `vpol.validate.kyverno.svc-fail`
(ValidatingPolicy). Rules that Kyverno generated for Deployments, StatefulSets, Jobs
and similar from a Pod rule are named `autogen-<rule>` (`autogen-cronjob-<rule>` for
CronJobs).

**2. List the policies** and their state.

```bash
kubectl get clusterpolicies,policies -A
kubectl get validatingpolicies,mutatingpolicies,generatingpolicies,imagevalidatingpolicies
kubectl get namespacedvalidatingpolicies -A
```

**3. Read the policy** named in the denial: its match, its failure action, its rules.

```bash
kubectl get clusterpolicy my-policy -o yaml
kubectl describe clusterpolicy my-policy
kubectl get validatingpolicy my-policy -o jsonpath='{.spec.validationActions}{"\n"}{.spec.matchConstraints}{"\n"}{.spec.validations}{"\n"}{.status}{"\n"}'
```

For ClusterPolicy and Policy, the failure action is `validate.failureAction` on each
rule (`Enforce` blocks, `Audit` only reports), or the older `spec.validationFailureAction`.
For a ValidatingPolicy it is `spec.validationActions` (`Deny`, `Audit`, `Warn`).

**4. Read the policy reports** for the resource: results of background scans and of
admission in Audit mode.

```bash
kubectl get policyreports -n my-namespace
kubectl get clusterpolicyreports
kubectl get policyreports -n my-namespace -o jsonpath='{range .items[*].results[?(@.result=="fail")]}{.policy}{" "}{.rule}{" "}{.message}{"\n"}{end}'
kubectl events -n my-namespace | grep -i policy
```

**5. If Kyverno itself may be the problem**, read its pods, its webhook configurations
and its logs.

```bash
kubectl get deployments,pods -n kyverno
kubectl get validatingwebhookconfigurations,mutatingwebhookconfigurations | grep -i kyverno
kubectl logs -n kyverno deployment/kyverno-admission-controller --tail=100
kubectl get configmap kyverno -n kyverno -o jsonpath='{.data.resourceFilters}{"\n"}'
```

**6. Open the matching reference** and follow its steps:

| What you see | Reference |
|---|---|
| A denial, `was blocked due to the following policies`, `Policy ... failed`, a policy that should block but only reports, PolicyReport failures | [references/validation.md](references/validation.md) |
| Mutations that do not happen, generated resources missing, UpdateRequests, cleanup policies | [references/mutate-and-generate.md](references/mutate-and-generate.md) |
| `failed calling webhook` naming kyverno, a policy not Ready, namespaces Kyverno ignores, controllers down | [references/webhooks-and-controllers.md](references/webhooks-and-controllers.md) |

## Read the results

What the common findings mean (Kyverno 1.19):

- **`admission webhook "validate.kyverno.svc-fail" denied the request: resource
  <Kind>/<ns>/<name> was blocked due to the following policies`**, followed by
  `<policy>:` and `<rule>: <message>`: a ClusterPolicy or Policy rule in Enforce mode
  failed. The message after the rule name is the policy's own text plus the path that
  failed (`failed at path /spec/template/metadata/labels/...`).
- **`admission webhook "vpol.validate.kyverno.svc-fail" denied the request: Policy
  <name> failed: <message>`**: a ValidatingPolicy with `Deny` failed.
- **An `autogen-` rule name**: the policy was written for Pods; Kyverno applies it to
  the pod template of the controller you applied.
- **Admitted, and a `fail` result in a PolicyReport**: the rule runs in `Audit` (or a
  ValidatingPolicy with `Audit`): Kyverno reports and lets it through.
- **No report and no denial at all**: the policy does not match the resource (kinds,
  namespaces, selectors), the namespace is in the `resourceFilters` of the `kyverno`
  ConfigMap (by default `kube-system`, `kube-public`, `kube-node-lease` and `kyverno`),
  or the policy is not Ready.
- **`failed calling webhook "validate.kyverno.svc-fail"`** (or another kyverno webhook):
  the API server cannot reach Kyverno, and the webhook fails closed. Nothing about the
  resource is wrong.

State the cause in one sentence, then the evidence you saw (the denial or report, the
policy and rule, its failure action, its match), then the proposed fix.

## Proposed fix

Show each fix to the user before running it: what it changes and how to undo it.
Make the resource comply: change it in its source (manifest, Helm values, GitOps
repository), so the next apply passes. Changing a policy's failure action or match,
adding a PolicyException, and touching Kyverno's webhook configurations or ConfigMap
change what is enforced for everyone: never run them yourself; hand them to the
policy's owners as proposed fixes and say why. Write each undo with the values you
found.

Bring back a Kyverno admission controller that was scaled to zero (write the undo with
the replicas you found):

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl scale deployment/kyverno-admission-controller -n kyverno --replicas=1
# Undo: kubectl scale deployment/kyverno-admission-controller -n kyverno --replicas=0
```

For a resource that must not comply (a real exception), the policy's owners add a
PolicyException. Exceptions are turned off by default in Kyverno and must be enabled
first (`--enablePolicyException`); see
[references/validation.md](references/validation.md).

## Sources

Checked against the Kyverno 1.19 documentation and source (v1.19.2):

- [Troubleshooting](https://kyverno.io/docs/guides/troubleshooting/).
- [Policy types](https://kyverno.io/docs/policy-types/overview/) and
  [ValidatingPolicy](https://kyverno.io/docs/policy-types/validating-policy/).
- [Validate rules](https://kyverno.io/docs/policy-types/cluster-policy/validate/),
  [mutate rules](https://kyverno.io/docs/policy-types/cluster-policy/mutate/) and
  [generate rules](https://kyverno.io/docs/policy-types/cluster-policy/generate/).
- [Policy reports](https://kyverno.io/docs/guides/reports/) and
  [policy exceptions](https://kyverno.io/docs/guides/exceptions/).
- [Upgrading to 1.19](https://kyverno.io/docs/installation/upgrading/) (ClusterPolicy
  deprecated) and [releases](https://kyverno.io/docs/installation/releases/): 1.19 is
  tested with Kubernetes 1.33 to 1.35; these steps were also seen working on 1.37.
- [Customization](https://kyverno.io/docs/installation/customization/): container
  flags and the `resourceFilters` ConfigMap key.
- Denial formats from the source:
  [block.go](https://github.com/kyverno/kyverno/blob/v1.19.2/pkg/webhooks/utils/block.go),
  [vpol/handler.go](https://github.com/kyverno/kyverno/blob/v1.19.2/pkg/webhooks/resource/vpol/handler.go),
  [autogen rule.go](https://github.com/kyverno/kyverno/blob/v1.19.2/pkg/autogen/v1/rule.go).
  The denials quoted here were also seen on a Kubernetes 1.37 kind cluster with Kyverno
  1.19.2.
