---
name: infra-kit.domain.helm
description: Create, review, validate, refactor, or troubleshoot Helm charts, values.yaml files, templates, helpers, releases, and Kubernetes deployment defaults.
---

# Helm

Use this skill when the user is working on Helm charts, `values.yaml`, templates, helper functions, release configuration, or chart review for Kubernetes workloads.

Reuse `examples/minimal-web-app/` when the user wants a clean starter chart with helpers, labels, probes, ingress, and explicit resource defaults.

## Outcomes

- Scaffold clean Helm charts that are easy to override and review
- Fix broken templates, values wiring, and release behavior
- Review charts for Kubernetes safety, upgrade stability, and maintainability
- Explain how Helm values, helpers, and templates map to rendered manifests

## Where This Fits In The Flow

- Use after `infra-kit.workflow` / `infra-kit.workflow.design` when the deliverable is a chart or a chart refactor.
- Use during implementation to harden defaults and validate with `helm lint` / `helm template` where possible.

## Workflow

1. Inspect the existing chart layout before changing files:
   - `Chart.yaml`
   - `values.yaml`
   - `templates/`
   - `_helpers.tpl`
   - `charts/`
   - `crds/`
2. Identify whether the request is about:
   - authoring a new chart
   - fixing templates or values wiring
   - hardening workload defaults
   - debugging render or upgrade behavior
3. Confirm the chart contract:
   - chart name and purpose
   - supported Kubernetes version
   - required values
   - optional overrides
   - subchart or dependency behavior
4. Keep templates DRY:
   - centralize names and common labels in `_helpers.tpl`
   - avoid copy-pasting metadata blocks across resources
5. Prefer predictable values design:
   - use clear lower-camel-case or existing repo conventions
   - keep nesting shallow unless grouping materially improves readability
   - document values that users are expected to override often
6. Apply Kubernetes-safe defaults for workload charts when the user has not defined them:
   - standard labels
   - resource requests and limits
   - liveness, readiness, and startup probes when the workload supports them
   - pod and container security context when compatible with the image
7. If the chart renders CRDs or third-party APIs, look up the exact upstream documentation before changing templates.
8. After editing, run the strongest local Helm and manifest validation available.

## Hallucination Guardrails

- Open and quote the actual chart files (`Chart.yaml`, `values.yaml`, `templates/<file>`) before describing changes so every recommendation is anchored to evidence instead of assumptions.
- When referencing Kubernetes resources or Helm helpers, double-check the API version and function signature from official docs to avoid inventing fields or behavior.
- If a value, helper, or manifest is missing, state that absence plainly and explain whether you are proposing to add it rather than speaking as if it already exists.
- When `helm lint`, `helm template`, or cluster-side validation cannot run, document the limitation and keep findings scoped to static review rather than implying manifests were validated.

## Output Standards

- Lead with the current chart status (what changed or what was reviewed) before diving into file-by-file commentary so users get the headline immediately.
- Cite the Helm or Kubernetes best practice that backs each recommendation—examples include stable selectors, standard labels, resource sizing, probe coverage, or security-context requirements.
- Always list the validation commands executed (or why they were skipped) so maintainers understand test coverage before trusting the result.
- When residual risks remain (upgrade drift, CRDs, missing sizing), state them explicitly along with the follow-up action required.

## Authoring Rules

- Keep `Chart.yaml` metadata deliberate:
  - `apiVersion: v2` unless the repo has a specific reason not to
  - SemVer `version`
  - accurate `appVersion` when relevant
- Prefer named templates for:
  - fullname generation
  - chart labels
  - selector labels
  - service account names
- Keep selectors stable. Do not mutate `matchLabels` patterns casually in an existing chart.
- Standardize labels across rendered resources. Include Helm/Kubernetes common labels when they fit:
  - `app.kubernetes.io/name`
  - `app.kubernetes.io/instance`
  - `app.kubernetes.io/component`
  - `app.kubernetes.io/part-of`
  - `app.kubernetes.io/managed-by`
  - `helm.sh/chart`
- Avoid hiding critical behavior behind clever template logic. Readability beats template tricks.
- Prefer explicit values over deeply magical defaults.
- For workloads, expose image repository, tag, and pull policy explicitly.
- For workloads, do not leave resource sizing undefined by default unless the chart is intentionally tiny, local-only, or the user asked for a minimal scaffold.
- If limits are set, set requests deliberately too instead of relying on cluster-side defaulting.
- Prefer configurable pod annotations, node selectors, tolerations, affinity, and extra labels when the chart is intended for reusable platform use.
- Avoid embedding secrets directly in `values.yaml`; prefer existing secret references or clearly marked placeholders.
- Use `with`, `range`, `include`, and `nindent` only when they improve template clarity.

## Review Priorities

When reviewing or debugging Helm, check in this order:

1. Broken template syntax, indentation, or bad function usage
2. Incorrect values paths or missing required values
3. Selector and label mismatches that can break upgrades or Services
4. Unsafe workload defaults:
   - no resources
   - no probes
   - weak security context
   - privileged or root execution without need
5. Dependency and subchart issues:
   - wrong values inheritance
   - version drift
   - brittle condition or tags behavior
6. Upgrade and operability risks:
   - immutable field changes
   - hook misuse
   - CRD handling mistakes
   - unreadable helper sprawl

## Validation Loop

Use what exists in the target repo. Prefer this order when available:

```bash
helm lint <chart>
helm template <release-name> <chart> --values <values-file>
helm upgrade --install <release-name> <chart> --namespace <ns> --dry-run --debug
```

If the repo uses additional tooling, include it:

```bash
kubeconform -strict
kubectl apply --dry-run=server -f <rendered-manifests>
helm dependency update <chart>
helm unittest <chart>
```

If cluster access, dependencies, schemas, or plugins are unavailable, say exactly what was skipped and continue with the strongest offline review possible.

Bundled helper:

```bash
bash scripts/validate_helm.sh <chart> [values-file]
```

## Delivery Standard

Always leave the user with:

- the chart files changed or recommended
- the values and template assumptions you made
- the validation commands run
- unresolved risks around upgrades, CRDs, workload security, or resource sizing
