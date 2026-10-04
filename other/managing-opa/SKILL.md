---
name: managing-opa
description: |
  Use when working with Opa — oPA/Gatekeeper policy engine management. Covers
  Rego policy authoring, constraint templates, constraint management, audit
  results, data queries, and policy testing. Use when managing Kubernetes
  admission policies with Gatekeeper, writing Rego rules, debugging policy
  violations, or querying OPA data.
connection_type: opa
preload: false
---

# OPA/Gatekeeper Policy Management Skill

Manage and inspect OPA policies, Gatekeeper constraints, and Rego rules.

## MANDATORY: Discovery-First Pattern

**Always check Gatekeeper status and existing constraints before creating policies.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Gatekeeper Version ==="
kubectl get deployment gatekeeper-controller-manager -n gatekeeper-system \
    -o jsonpath='{.spec.template.spec.containers[0].image}' 2>/dev/null
echo ""

echo ""
echo "=== Gatekeeper Pods ==="
kubectl get pods -n gatekeeper-system 2>/dev/null

echo ""
echo "=== Constraint Templates ==="
kubectl get constrainttemplates 2>/dev/null | head -15

echo ""
echo "=== Active Constraints ==="
kubectl get constraints 2>/dev/null | head -15

echo ""
echo "=== Audit Summary ==="
kubectl get constraints -o json 2>/dev/null | jq '
    [.items[] | {
        kind: .kind,
        name: .metadata.name,
        violations: (.status.totalViolations // 0)
    }] | sort_by(-.violations) | .[0:10]
'
```

## Core Helper Functions

```bash
#!/bin/bash

# OPA eval helper (standalone OPA)
opa_eval() {
    local query="$1"
    local input="${2:-}"
    local data="${3:-}"
    if [ -n "$input" ]; then
        opa eval --input "$input" --data "$data" "$query" --format pretty 2>/dev/null
    else
        opa eval "$query" --format pretty 2>/dev/null
    fi
}

# OPA test runner
opa_test() {
    local policy_dir="${1:-.}"
    opa test "$policy_dir" -v 2>/dev/null
}

# Gatekeeper constraint status
gk_violations() {
    local kind="$1"
    kubectl get "$kind" -o json 2>/dev/null | jq '.items[].status.violations[]?'
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use `-o json` with jq for Gatekeeper resources
- Use `opa eval --format pretty` for readable policy evaluation
- Never dump full constraint template Rego -- extract key rules

## Common Operations

### Constraint Template Inspection

```bash
#!/bin/bash
TEMPLATE="${1:-}"

if [ -n "$TEMPLATE" ]; then
    echo "=== Constraint Template: $TEMPLATE ==="
    kubectl get constrainttemplate "$TEMPLATE" -o json 2>/dev/null | jq '{
        name: .metadata.name,
        crd_kind: .spec.crd.spec.names.kind,
        parameters: .spec.crd.spec.validation.openAPIV3Schema.properties,
        rego_targets: [.spec.targets[].target]
    }'

    echo ""
    echo "=== Rego Policy ==="
    kubectl get constrainttemplate "$TEMPLATE" -o jsonpath='{.spec.targets[0].rego}' 2>/dev/null | head -30
else
    echo "=== All Constraint Templates ==="
    kubectl get constrainttemplates -o json 2>/dev/null | jq -r '
        .items[] | "\(.metadata.name)\t\(.spec.crd.spec.names.kind)\t\(.status.created // false)"
    ' | column -t
fi
```

### Constraint Violations

```bash
#!/bin/bash
echo "=== All Violations ==="
kubectl get constraints -o json 2>/dev/null | jq '
    [.items[] | {
        kind: .kind,
        name: .metadata.name,
        enforcement: .spec.enforcementAction,
        total_violations: (.status.totalViolations // 0),
        violations: [.status.violations[]? | {
            kind: .kind,
            name: .name,
            namespace: .namespace,
            message: .message
        }][:5]
    }] | sort_by(-.total_violations)
' | head -50

echo ""
echo "=== Violation Summary ==="
kubectl get constraints -o json 2>/dev/null | jq '{
    total_constraints: (.items | length),
    enforcing: ([.items[] | select(.spec.enforcementAction == "deny" or .spec.enforcementAction == null)] | length),
    dry_run: ([.items[] | select(.spec.enforcementAction == "dryrun")] | length),
    total_violations: ([.items[].status.totalViolations // 0] | add)
}'
```

### Rego Policy Testing

```bash
#!/bin/bash
POLICY_DIR="${1:-.}"

echo "=== Running OPA Tests ==="
opa test "$POLICY_DIR" -v 2>&1 | tail -30

echo ""
echo "=== Policy Evaluation ==="
POLICY="${2:-}"
INPUT="${3:-}"
if [ -n "$POLICY" ] && [ -n "$INPUT" ]; then
    opa eval --input "$INPUT" --data "$POLICY" "data.main.violation" --format pretty 2>/dev/null
fi
```

### Audit Results Analysis

```bash
#!/bin/bash
echo "=== Gatekeeper Audit Status ==="
kubectl get constrainttemplate -o json 2>/dev/null | jq '
    [.items[] | {
        template: .metadata.name,
        status: .status.byPod[0].observedGeneration,
        created: .metadata.creationTimestamp
    }]
'

echo ""
echo "=== Resources Violating Policies ==="
kubectl get constraints -o json 2>/dev/null | jq -r '
    .items[].status.violations[]? |
    "\(.kind)/\(.name)\t\(.namespace // "cluster")\t\(.message[:60])"
' | sort -u | column -t | head -20

echo ""
echo "=== Audit Logs ==="
kubectl logs -n gatekeeper-system deployment/gatekeeper-audit-controller --tail=20 2>/dev/null | \
    grep -E '(violation|error)' | head -10
```

### Data and Config Sync

```bash
#!/bin/bash
echo "=== Config Resource ==="
kubectl get config -n gatekeeper-system -o json 2>/dev/null | jq '{
    sync_kinds: [.spec.sync.syncOnly[]? | "\(.group)/\(.version)/\(.kind)"],
    match_namespaces: .spec.match
}'

echo ""
echo "=== Synced Data ==="
kubectl get config -n gatekeeper-system -o json 2>/dev/null | jq '
    .status.byPod[]? | {
        pod: .id,
        operations: .operations
    }
'
```

## Safety Rules

- **`enforcementAction: deny` blocks non-compliant admissions** -- always test with `dryrun` first
- **Constraint template changes affect all constraints** using that template
- **Gatekeeper webhook failure** with `failurePolicy: Fail` blocks all admissions -- monitor pod health
- **Config sync** copies cluster data into OPA -- be careful with sensitive data
- **Rego policies must terminate** -- infinite loops can hang admission requests

## Output Format

Present results as a structured report:
```
Managing Opa Report
═══════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

- **Webhook timeout**: Complex Rego policies can exceed webhook timeout (3s default) -- optimize queries
- **Audit lag**: Audit controller runs periodically -- violations may not appear immediately
- **Config sync required**: Rego policies that reference other resources need those resources synced via Config
- **Namespace exclusions**: System namespaces should be excluded from constraints -- use `match.excludedNamespaces`
- **Template compilation errors**: Rego syntax errors silently prevent constraint enforcement -- check template status
- **Dry run limitations**: Dry run still evaluates but does not block -- mutations are not captured
- **Multi-version templates**: Upgrading constraint templates requires careful migration of existing constraints
- **Resource limits**: Gatekeeper pods need adequate memory for large clusters -- OOM kills disable enforcement
