---
name: policy-as-code-runner
description: "Configures policy-as-code testing using OPA / Conftest / Cedar - authors policies in Rego (OPA's language), runs Conftest against Kubernetes manifests / Terraform plans / Dockerfiles / arbitrary structured data, integrates with CI for PR-time policy gates. Per OPA's docs: \"an open source, general-purpose policy engine that unifies policy enforcement across the stack.\" Use to express + enforce custom policies (cost limits, tagging requirements, security baselines) that Checkov / tfsec / KICS don't cover."
---

# policy-as-code-runner

## Overview

[opa]: https://www.openpolicyagent.org/docs/

**Conftest** is a CLI that uses OPA ([opa-docs][opa]) to test
structured configuration files (Kubernetes manifests, Terraform
plans, Dockerfiles, etc.) against Rego policies. This skill
covers Conftest invocation + Rego policy authoring as the custom
policy layer alongside Checkov / tfsec / KICS (which carry
built-in checks).

## When to use

- The team has custom policies that off-the-shelf scanners
  (Checkov / tfsec / KICS) don't cover (e.g., "all production
  resources must have a cost-center tag").
- A Kubernetes admission policy is needed (OPA Gatekeeper).
- Dockerfiles need policy review (no `:latest` tags, no `apt-get
  upgrade`, etc.).
- A multi-language IaC stack needs unified policy enforcement.

## Step 1 - Install Conftest

```bash
# macOS
brew install conftest

# Or download binary
curl -LO https://github.com/open-policy-agent/conftest/releases/latest/download/conftest_<version>_Linux_x86_64.tar.gz
```

## Step 2 - Author a policy in Rego

```rego
# policies/kubernetes/required_labels.rego
package main

# All pods must have these labels
required_labels := {"app", "version", "owner"}

deny[msg] {
    input.kind == "Deployment"
    label := required_labels[_]
    not input.spec.template.metadata.labels[label]
    msg := sprintf("Deployment '%s' missing required label '%s'", [input.metadata.name, label])
}

# All deployments must specify resource limits
deny[msg] {
    input.kind == "Deployment"
    container := input.spec.template.spec.containers[_]
    not container.resources.limits.memory
    msg := sprintf("Container '%s' in deployment '%s' missing memory limit", [container.name, input.metadata.name])
}

deny[msg] {
    input.kind == "Deployment"
    container := input.spec.template.spec.containers[_]
    not container.resources.limits.cpu
    msg := sprintf("Container '%s' in deployment '%s' missing CPU limit", [container.name, input.metadata.name])
}
```

The `deny` rule pattern: each `deny[msg]` rule that holds adds a
message to the deny set. If `deny` is non-empty, the test fails.

## Step 3 - Run Conftest

```bash
# Test a single manifest
conftest test deployment.yaml

# Test all manifests
conftest test manifests/

# With specific policy directory
conftest test deployment.yaml --policy ./policies/

# JSON output for CI parsing
conftest test deployment.yaml --output json
```

## Step 4 - Test against Helm chart output

```bash
helm template myrelease charts/mychart/ -f values.yaml | conftest test -
```

The chart renders to manifests; Conftest validates them.

## Step 5 - Test against Terraform plan

```bash
terraform plan -out=plan.tfplan
terraform show -json plan.tfplan > plan.json
conftest test plan.json --policy policies/terraform/
```

```rego
# policies/terraform/cost_center_tag.rego
package main

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_instance"
    not resource.change.after.tags.cost_center
    msg := sprintf("EC2 instance '%s' missing cost_center tag", [resource.address])
}
```

## Step 6 - Test against Dockerfile

```rego
# policies/dockerfile/no_latest.rego
package main

deny[msg] {
    input[i].Cmd == "from"
    val := input[i].Value
    contains(val[0], ":latest")
    msg := sprintf("Avoid :latest tag in FROM (line %d)", [i])
}

deny[msg] {
    input[i].Cmd == "run"
    val := input[i].Value[0]
    contains(val, "apt-get upgrade")
    msg := sprintf("Avoid 'apt-get upgrade' (line %d) - pin specific package versions", [i])
}
```

```bash
conftest test Dockerfile
```

## Step 7 - Author tests for policies

Policies themselves should be tested:

```rego
# policies/kubernetes/required_labels_test.rego
package main

test_deployment_missing_labels {
    deny[_] with input as {
        "kind": "Deployment",
        "metadata": {"name": "test"},
        "spec": {"template": {"metadata": {"labels": {}}}}
    }
}

test_deployment_with_all_labels {
    count(deny) == 0 with input as {
        "kind": "Deployment",
        "metadata": {"name": "test"},
        "spec": {"template": {"metadata": {"labels": {"app": "x", "version": "1.0", "owner": "team"}}}, "spec": {"containers": [{"resources": {"limits": {"memory": "512Mi", "cpu": "500m"}}}]}}
    }
}
```

```bash
opa test policies/
```

## Step 8 - CI integration

```yaml
jobs:
  policy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - run: |
          curl -L https://github.com/open-policy-agent/conftest/releases/download/v0.50.0/conftest_0.50.0_Linux_x86_64.tar.gz | tar xz
          # user-owned bin dir on PATH: no sudo, no write to /usr/local/bin
          mkdir -p "$HOME/.local/bin" && mv conftest "$HOME/.local/bin/"
          echo "$HOME/.local/bin" >> "$GITHUB_PATH"
      - name: Test policies
        run: opa test policies/
      - name: Conftest manifests
        run: conftest test manifests/ --policy policies/
      - name: Conftest Helm
        run: helm template myrelease charts/mychart/ -f values.yaml | conftest test - --policy policies/
      - name: Conftest Terraform
        run: |
          terraform plan -out=plan.tfplan
          terraform show -json plan.tfplan > plan.json
          conftest test plan.json --policy policies/terraform/
```

## Step 9 - Bundle policies for OPA Gatekeeper (Kubernetes admission)

For runtime enforcement (vs PR-time):

```yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: requiredlabels
spec:
  crd:
    spec:
      names: { kind: RequiredLabels }
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        # Same Rego from Step 2
```

Cluster admins install Gatekeeper; the constraint blocks Deployments
that violate the policy at admission time.

## Anti-patterns

| Anti-pattern                                                          | Why it fails                                                              | Fix |
|-----------------------------------------------------------------------|---------------------------------------------------------------------------|-----|
| Untested policies                                                      | Policy bugs let bad config through; over-strict policies block good config. | `opa test` against test fixtures (Step 7). |
| Policies in production without PR-time gating                         | Surprises at admission time; deployments fail.                          | CI gate first (Step 8); Gatekeeper second. |
| One mega-policy file                                                   | Hard to reason about; merge conflicts.                                    | Per-domain policy files. |
| Rego complexity for simple checks                                      | Hard to maintain; Rego learning curve.                                   | Use Checkov / tfsec for built-in checks; OPA for custom. |
| Skipping the negation tests                                            | Policy may pass for the wrong reason.                                   | Test both deny and not-deny cases (Step 7). |

## Limitations

- **Rego learning curve.** New language; per [opa-docs][opa] it's
  "purpose-built" but takes time to master.
- **Per-tool integration varies.** Conftest wraps OPA cleanly;
  some tools have native OPA integration, others don't.
- **Policy proliferation.** Like step libraries (per `bdd-step-library-curator` in the qa-bdd plugin),
  policies can multiply; periodic review needed.

## References

- [opa][opa] - OPA overview, Rego language, common applications,
  CNCF graduated status.
- Conftest at `conftest.dev`.
- `$GITHUB_PATH` for a user-owned install dir in CI:
  [GitHub Actions: adding a system path](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands#adding-a-system-path).
- OPA Gatekeeper at `open-policy-agent.github.io/gatekeeper/`.
- `checkov-policy`,
  `trivy-config` - sister scanners with
  built-in checks (use these first; OPA for custom).
