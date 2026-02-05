---
name: infrastructure-testing
description: Run TestKube and PGBouncer tests on Kubernetes clusters with mandatory context verification to prevent accidental deployments to wrong environments
---

# Infrastructure Testing

Test infrastructure components (TestKube, PGBouncer) on Kubernetes clusters. **CRITICAL**: Always verify context to prevent wrong-cluster operations.

## ⚠️ SAFETY FIRST

**MANDATORY before ANY operation:**

```bash
# Verify current context
kubectl config current-context

# Confirm it matches your intended environment
# NEVER proceed if context is wrong
```

## Pre-Flight Checklist

- [ ] Verified kubectl context matches target environment
- [ ] TestKube CLI installed and configured
- [ ] Required secrets exist in testkube namespace
- [ ] Understood which environment you're targeting

## TestKube Workflow

### 1. Set Context (MANDATORY)

```bash
# Switch to correct context
kubectl config use-context fbg-inf-dev-1

# Verify
kubectl config current-context
```

### 2. Configure TestKube CLI

```bash
# Use proxy client mode with current context
testkube set context --client proxy --kubeconfig ~/.kube/config --namespace testkube
```

### 3. Run TestWorkflows

```bash
# Run with real-time output
testkube run testworkflow <workflow-name> --watch

# Example
testkube run testworkflow k6-pgbouncer-rolling-restart-psql --watch
```

### 4. Alternative: kubectl Direct

```bash
kubectl create -f - <<EOF
apiVersion: testworkflows.testkube.io/v1
kind: TestWorkflowExecution
metadata:
  name: test-$(date +%s)
  namespace: testkube
spec:
  testWorkflow:
    name: <workflow-name>
EOF
```

## Legacy Test Commands

**ALWAYS specify --context explicitly:**

```bash
# Run test
kubectl --context=fbg-inf-dev-1 testkube run test <test-name> -v TEST_ENVIRONMENT=fbg-inf-dev-1

# With secrets
kubectl --context=fbg-inf-dev-1 testkube run testworkflow <name> \
  -v TEST_ENVIRONMENT=fbg-inf-dev-1 \
  --secret-variable IGT_USER=username \
  --secret-variable IGT_PW=password

# Deploy test
kubectl --context=fbg-inf-dev-1 apply -f tests/your-test.yaml
```

## Verification Commands

```bash
# List tests
kubectl --context=fbg-inf-dev-1 get tests -n testkube

# List pods
kubectl --context=fbg-inf-dev-1 get pods -n testkube

# Check execution status
testkube get testworkflowexecution <execution-id>
```

## Environment Reference

| Environment | Context | Notes |
|-------------|---------|-------|
| Dev | `fbg-inf-dev-1` | Safe for testing |
| Staging | `fbg-inf-staging-1` | Pre-prod validation |
| Prod | `fbg-inf-prod-1` | **EXTREME CAUTION** |

## PGBouncer Configuration

- **Service**: `pgbouncer-ats` port 5432
- **Auth**: AWS IAM roles + SSM Parameter Store
- **Role**: `arn:aws:iam::222019643140:role/eks-application-iam-pgbouncer-role`

## Best Practices

- ✅ Always use proxy client mode locally
- ✅ Set kubectl context before testkube configuration
- ✅ Use --watch flag for real-time output
- ✅ Verify branch targeting in test YAML files
- ✅ Never hardcode credentials - use SSM/secrets

## Web UI

Access: https://testkube.cicd.fanatics.bet/clusters/inf-dev-1/tests
