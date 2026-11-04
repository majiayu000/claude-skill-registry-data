---
name: k8s-gatekeeper-troubleshooting
description: >-
  Use when OPA Gatekeeper blocks, warns about or fails to police resources in
  Kubernetes: "admission webhook \"validation.gatekeeper.sh\" denied the request:
  [constraint] message", warnings from constraints in warn mode, a constraint that should
  block but only shows violations in audit (dryrun), a ConstraintTemplate that does not
  compile (ingest_error, rego_parse_error), "no matches for kind" when applying a
  constraint, referential policies that never fire (sync), mutations that do not apply,
  or Gatekeeper that stopped enforcing because its webhook is down. Investigates with
  kubectl get, describe and logs, and proposes fixes. Reads first and asks before
  changing anything.
license: Apache-2.0
metadata:
  verified-with: "kubernetes 1.37, gatekeeper 3.23"
  verified-on: "2026-10-24"
---

# OPA Gatekeeper troubleshooting

Find out why Gatekeeper denies, warns about or does not police a resource, and propose
a fix. **Read first, ask before changing.** Run the investigation commands freely. Run
a command under an "Ask first" line only after the user approves that exact command; if
your credentials do not allow it, give it to the user to run. Never run a "Proposed
fix"; hand it to the user.

A **ConstraintTemplate** holds the policy code (Rego, or CEL under
`K8sNativeValidation`) and makes Gatekeeper create a new kind in
`constraints.gatekeeper.sh` (for example `K8sRequiredLabels`). A **constraint** of that
kind says where the policy applies (`spec.match`), with which parameters, and what
happens on a violation (`spec.enforcementAction`: `deny`, `dryrun`, `warn` or
`scoped`). The admission webhook checks new requests; the **audit** checks what already
exists and writes the results into each constraint's status.

A constraint is a guardrail someone chose on purpose. The usual fix is to make the
resource comply; changing, scoping or exempting a constraint is a decision for its
owners.

The commands use placeholders: `my-namespace`, `my-app`, `k8srequiredlabels` (a
template) and `my-constraint` (a constraint of kind `K8sRequiredLabels`). Replace them
with the real names. The built-in `view` role cannot read Gatekeeper's objects
(Gatekeeper adds nothing to it); if the commands are forbidden, say so and ask the user
for the constraint and template status. Never read Secrets.

## When to use

- A request is denied by `validation.gatekeeper.sh`, or prints a Gatekeeper warning.
- A constraint does not block what it should, or lists violations in its status.
- Applying a constraint fails because its kind does not exist.
- A policy that looks at other objects (unique hostnames, namespaces) never fires.
- Gatekeeper mutations do not change resources.

Hand-offs, by skill name. When the evidence points elsewhere, continue with that skill;
if it is not installed, keep going with the steps here and tell the user which skill
would help:

- The Gatekeeper pods crash or stay Pending: `k8s-workload-troubleshooting`.
- The denial comes from Kyverno (`validate.kyverno.svc-fail`, `vpol.validate.kyverno`):
  `k8s-kyverno-troubleshooting`.

## Investigate

Work through the steps in order. Stop when you have the cause and its evidence.

**1. Read the denial or warning.** The text in square brackets is the constraint's
name: `admission webhook "validation.gatekeeper.sh" denied the request: [<constraint>]
<message>`. A warning reads `Warning: [<constraint>] <message>`.

**2. List templates and constraints.** Every constraint kind is its own resource;
`constraints` lists them all.

```bash
kubectl get constrainttemplates
kubectl get constraints
```

**3. Read the constraint**: what it matches, its action, its parameters, and the
audit's violations.

```bash
kubectl get k8srequiredlabels my-constraint -o yaml
kubectl get k8srequiredlabels my-constraint -o jsonpath='{.spec.enforcementAction}{"\n"}{.spec.match}{"\n"}{.spec.parameters}{"\n"}{.status.totalViolations}{"\n"}{.status.violations}{"\n"}'
```

**4. Read the template's status**: whether it compiled on every Gatekeeper pod.

```bash
kubectl get constrainttemplate k8srequiredlabels -o jsonpath='{.status.created}{"\n"}{range .status.byPod[*]}{.id}{" "}{.errors}{"\n"}{end}'
kubectl get crds | grep constraints.gatekeeper.sh
```

**5. If Gatekeeper itself may be the problem**, read its pods, webhooks, Config and
logs.

```bash
kubectl get deployments,pods -n gatekeeper-system
kubectl get validatingwebhookconfiguration gatekeeper-validating-webhook-configuration -o jsonpath='{range .webhooks[*]}{.name}{" "}{.failurePolicy}{"\n"}{end}'
kubectl get configs.config.gatekeeper.sh -n gatekeeper-system -o yaml
kubectl get namespace my-namespace --show-labels
kubectl logs -n gatekeeper-system deployment/gatekeeper-controller-manager -c manager --tail=100
kubectl logs -n gatekeeper-system deployment/gatekeeper-audit -c manager --tail=100
```

**6. Open the matching reference** and follow its steps:

| What you see | Reference |
|---|---|
| A denial or warning, violations in a constraint's status, a constraint that does not block (`dryrun`, `warn`, `scoped`, match) | [references/constraints.md](references/constraints.md) |
| A template that does not compile, `no matches for kind`, ValidatingAdmissionPolicies Gatekeeper generates | [references/templates.md](references/templates.md) |
| Gatekeeper stopped enforcing, webhook down, exempt namespaces, sync for referential policies, mutation | [references/webhook-sync-mutation.md](references/webhook-sync-mutation.md) |

## Read the results

What the common findings mean (Gatekeeper 3.23):

- **`denied the request: [<constraint>] <message>`**: the constraint has
  `enforcementAction: deny` (the default) and the resource violates it. The message is
  the template's own text.
- **Violations in `status.violations` but nothing blocked**: the constraint is
  `dryrun` (audit only) or `warn`, or the resource existed before the constraint (the
  webhook checks only new requests; the audit finds the rest). `status.violations` holds
  at most 20 entries by default; `totalViolations` is the full count.
- **A template with `byPod[].errors` such as `ingest_error` `Could not ingest Rego: ...
  rego_parse_error`**: the policy code does not compile. Gatekeeper accepts the template
  object but never creates its constraint kind.
- **`no matches for kind "<Kind>" in version "constraints.gatekeeper.sh/v1beta1"`** or
  `the server could not find the requested resource` when applying a constraint: the
  kind does not exist yet, because its template is missing or failed to compile.
- **Nothing enforced, yet the constraint is right**: the Gatekeeper webhook pods are
  down. `validation.gatekeeper.sh` uses `failurePolicy: Ignore`, so the API server
  admits everything while Gatekeeper is unreachable, and only the audit notices.
- **A namespace never checked**: it carries the label `admission.gatekeeper.sh/ignore`,
  is listed in the Config's `excludedNamespaces`, or the constraint's `match` leaves it
  out. `gatekeeper-system` is always exempt.

State the cause in one sentence, then the evidence you saw (the denial or violation,
the constraint and its action, the template status), then the proposed fix.

## Proposed fix

Show each fix to the user before running it: what it changes and how to undo it.
Make the resource comply in its source (manifest, Helm values, GitOps repository).
Changing a constraint's action or match, fixing a template, exempting a namespace and
editing Gatekeeper's Config or webhooks change what is enforced for everyone: never run
them yourself; hand them to the constraint's owners as proposed fixes. Write each undo
with the values you found.

Bring back Gatekeeper's webhook after it was scaled to zero (write the undo with the
replicas you found):

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl scale deployment/gatekeeper-controller-manager -n gatekeeper-system --replicas=3
# Undo: kubectl scale deployment/gatekeeper-controller-manager -n gatekeeper-system --replicas=0
```

Resources admitted while the webhook was down stay as they are; the audit lists them in
the constraints' `status.violations`, and they are fixed in their source.

## Sources

Checked against the Gatekeeper 3.23 documentation and source (v3.23.1):

- [How to use Gatekeeper](https://open-policy-agent.github.io/gatekeeper/website/docs/howto),
  [ConstraintTemplates](https://open-policy-agent.github.io/gatekeeper/website/docs/constrainttemplates)
  and [handling violations](https://open-policy-agent.github.io/gatekeeper/website/docs/violations):
  enforcement actions, the denial and warning format.
- [Audit](https://open-policy-agent.github.io/gatekeeper/website/docs/audit) and
  [debugging](https://open-policy-agent.github.io/gatekeeper/website/docs/debug).
- [Exempting namespaces](https://open-policy-agent.github.io/gatekeeper/website/docs/exempt-namespaces),
  [replicating data](https://open-policy-agent.github.io/gatekeeper/website/docs/sync),
  [mutation](https://open-policy-agent.github.io/gatekeeper/website/docs/mutation),
  [failing closed](https://open-policy-agent.github.io/gatekeeper/website/docs/failing-closed)
  and [emergency recovery](https://open-policy-agent.github.io/gatekeeper/website/docs/emergency).
- [Integration with Kubernetes validating admission policy](https://open-policy-agent.github.io/gatekeeper/website/docs/validating-admission-policy).
- Message formats and status codes from the source:
  [policy.go](https://github.com/open-policy-agent/gatekeeper/blob/v3.23.1/pkg/webhook/policy.go)
  and [constants.go](https://github.com/open-policy-agent/gatekeeper/blob/v3.23.1/pkg/controller/constrainttemplate/constants.go).
  The messages quoted here were also seen on a Kubernetes 1.37 kind cluster with
  Gatekeeper 3.23.1.
