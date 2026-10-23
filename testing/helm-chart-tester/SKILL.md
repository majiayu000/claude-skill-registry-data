---
name: helm-chart-tester
description: "Configures helm-unittest for Helm chart unit testing - installs the `helm-unittest` plugin, authors `tests/*.yaml` per template, asserts on rendered manifests (`isKind`, `equal`, `matchRegex`, snapshots), plus `helm lint` and `helm template` render testing. Use to verify a chart's template logic and rendered shape; this is unit-level correctness testing, not security scanning - to enforce policy on rendered manifests use policy-as-code-runner, and to scan charts for misconfigurations use checkov-policy or trivy-config."
---

# helm-chart-tester

## Overview

**helm-unittest** (Helm plugin) unit-tests the rendered chart
output - assert specific fields, conditional behaviors, value
substitutions - to catch template bugs before deploying.

## When to use

- Team ships Helm charts (in-house apps, OSS contributions).
- A chart has conditional logic (`{{ if .Values.foo }}`); tests
  verify both branches.
- A chart's rendered output must satisfy specific shape contracts
  (env vars, ports, labels).

## Step 1 - Install

```bash
helm plugin install https://github.com/helm-unittest/helm-unittest
helm plugin list   # verify
```

## Step 2 - Author a test

```yaml
# charts/mychart/tests/deployment_test.yaml
suite: deployment template
templates:
  - templates/deployment.yaml
tests:
  - it: should set the right image
    set:
      image.repository: myapp
      image.tag: v1.2.3
    asserts:
      - isKind:
          of: Deployment
      - equal:
          path: spec.template.spec.containers[0].image
          value: myapp:v1.2.3

  - it: should add the configured env vars
    set:
      env:
        - name: API_URL
          value: https://api.example.com
        - name: LOG_LEVEL
          value: debug
    asserts:
      - contains:
          path: spec.template.spec.containers[0].env
          content:
            name: API_URL
            value: https://api.example.com

  - it: should add resource limits when set
    set:
      resources:
        limits:
          memory: 512Mi
          cpu: 500m
    asserts:
      - equal:
          path: spec.template.spec.containers[0].resources.limits.memory
          value: 512Mi

  - it: should NOT add resource limits when unset
    asserts:
      - notExists:
          path: spec.template.spec.containers[0].resources.limits
```

The `set:` block overrides values; `asserts:` checks the rendered
output.

## Step 3 - Common assertions

| Assertion         | Use                                                |
|-------------------|----------------------------------------------------|
| `equal`            | Exact value match                                  |
| `notEqual`         | Inverse                                            |
| `isKind`           | Document is the expected Kind                      |
| `isAPIVersion`     | Specific API version                               |
| `isNullOrEmpty`    | Field is null / empty                              |
| `notNullOrEmpty`   | Field has a value                                  |
| `exists`           | Field exists                                       |
| `notExists`        | Field absent                                       |
| `contains`         | Array contains an item                              |
| `notContains`      | Inverse                                             |
| `matchRegex`       | Field matches regex                                |
| `notMatchRegex`    | Inverse                                             |
| `failedTemplate`    | Template should fail to render (negative test)    |

## Step 4 - Run

```bash
# All tests for a chart
helm unittest charts/mychart/

# Specific test file
helm unittest charts/mychart/ -f tests/deployment_test.yaml

# Update snapshots (if using snapshot assertions)
helm unittest charts/mychart/ -u
```

## Step 5 - Snapshot testing

For complex rendered manifests, snapshot the output:

```yaml
tests:
  - it: should render the full deployment correctly
    asserts:
      - matchSnapshot: {}
```

First run captures the snapshot; subsequent runs compare. A diff
fails the test. Useful for catching unintended template changes.

Per `golden-file-conventions` (in the qa-test-data plugin):
sanitize the snapshots (strip volatile fields like timestamps).

## Step 6 - Chart linting

```bash
helm lint charts/mychart/
```

Catches:
- Missing required fields (`name`, `version`, `appVersion`).
- Broken template syntax.
- YAML formatting issues.
- Schema violations (if `values.schema.json` present).

Run alongside unit tests in CI.

## Step 7 - Render testing

```bash
# See the rendered output without applying
helm template myrelease charts/mychart/ -f values.test.yaml

# Compare two renders (e.g., before / after a change)
helm template myrelease charts/mychart/ -f values.test.yaml > new.yaml
git stash
helm template myrelease charts/mychart/ -f values.test.yaml > old.yaml
git stash pop
diff old.yaml new.yaml
```

Useful for review: "what does this change actually produce?"

## Step 8 - CI integration

```yaml
jobs:
  helm:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: azure/setup-helm@v4
        with: { version: 'v3.16.4' }
      - run: helm plugin install https://github.com/helm-unittest/helm-unittest
      - run: helm lint charts/mychart/
      - run: helm unittest charts/mychart/
```

## Step 9 - Kubernetes admission integration

For deeper verification, render charts and run them through OPA /
Conftest:

```bash
helm template myrelease charts/mychart/ -f values.yaml | conftest test -
```

The Conftest step catches policy violations the unit tests don't
cover (e.g., "all containers must have resource limits"). See
`policy-as-code-runner`.

## Anti-patterns

| Anti-pattern                                                          | Why it fails                                                              | Fix |
|-----------------------------------------------------------------------|---------------------------------------------------------------------------|-----|
| Skipping `helm lint`                                                   | Schema violations slip; install fails at deploy.                         | Always lint (Step 6). |
| Snapshot-only tests (no `equal` checks)                                | Snapshots accept any change; explicit assertions catch intent.           | Mix snapshots + explicit (Step 2 + Step 5). |
| One mega-test file per chart                                           | Test file becomes unreadable; merge conflicts.                           | One test file per template. |
| Hardcoded image tags in tests                                          | Tests pass against the wrong tag if values default.                      | Set image tag explicitly via `set:`. |
| Skipping the negative tests (`notExists`, `failedTemplate`)            | Unintended additions slip through.                                        | Test absences too (Step 2 example). |

## Limitations

- **Unit-level only.** helm-unittest renders templates; doesn't
  install. For install verification, use Helm's `helm install
  --dry-run` + admission webhooks.
- **Snapshot maintenance.** Snapshots accumulate; periodic review
  needed.
- **No cross-chart testing.** Per-chart only; cross-chart
  interactions need integration testing.

## References

- helm-unittest at `github.com/helm-unittest/helm-unittest`.
- Helm docs at `helm.sh/docs/`.
- `policy-as-code-runner` - 
  policy-level testing of rendered manifests.
- `golden-file-conventions` - for snapshot sanitization patterns.
