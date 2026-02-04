---
name: Creating Ephemeral Kubernetes Exec Pods
description: This skill creates ephemeral pods cloned from existing deployments for interactive shell access with full application context. Use this when you need Rails console, database access, or debugging with env vars and secrets without affecting production pods.
allowed-tools: [Bash, Read]
---

# Creating Ephemeral Kubernetes Exec Pods

Create a dedicated pod cloned from an existing deployment for interactive shell access with full application context (environment variables, secrets, volume mounts).

## When to Use This

- Running Rails console in a Kubernetes environment
- Executing database migrations or one-off scripts
- Debugging with full app configuration
- Running commands that would disrupt a live pod

**Why not `kubectl exec` into an existing pod?** This approach:
- Won't affect production traffic
- Has configurable resources (memory/CPU)
- Stays alive for your session only
- Can run disruptive commands safely

## Prerequisites

- `kubectl` installed and configured
- `jq` installed (for JSON transformation)
- Kubeconfig with access to target cluster
- Know your target:
  - Namespace where the app runs
  - Label selector to find the deployment
  - Main app container name (not sidecars)

### AWS SSO Authentication (if applicable)

If your cluster uses AWS EKS with SSO authentication:

```bash
# Check if SSO session is valid
kubectl get deployments -n <NAMESPACE> 2>&1 | grep -q "SSO session" && echo "SSO expired"

# Find the AWS profile from your kubeconfig
grep -A15 'exec:' <KUBECONFIG_PATH> | grep 'AWS_PROFILE' -A1

# Login with the profile
aws sso login --profile <PROFILE_NAME>
```

## Usage

**Important:** Keep the same terminal session open throughout. Variables must persist across all steps.

### Step 1: Set up environment

```bash
export KUBECONFIG=/path/to/your/kubeconfig
```

### Step 2: Find the source deployment

```bash
# List matching deployments
kubectl get deployments -n <NAMESPACE> -l <LABEL_SELECTOR>

# Pick one and store the name
DEPLOYMENT_NAME=<name-from-output>

# List containers to find the app container (not sidecars like linkerd-proxy, proxy, envoy)
kubectl get deployment "$DEPLOYMENT_NAME" -n <NAMESPACE> -o jsonpath='{.spec.template.spec.containers[*].name}'

# The app container usually matches the deployment name
CONTAINER_NAME=<app-container-name>
NAMESPACE=<namespace>
```

### Step 3: Extract and transform to pod spec

```bash
# Generate a unique pod name
POD_NAME="${DEPLOYMENT_NAME}-exec-`date +%s`"
echo "Pod name: $POD_NAME"

# Extract deployment and transform to ephemeral pod
kubectl get deployment "$DEPLOYMENT_NAME" -n "$NAMESPACE" -o json | jq \
  --arg podname "$POD_NAME" \
  --arg namespace "$NAMESPACE" \
  --arg container "$CONTAINER_NAME" '
  .spec.template |
  .apiVersion = "v1" |
  .kind = "Pod" |
  .metadata = {name: $podname, namespace: $namespace, labels: {ephemeral: "true"}} |
  .spec.restartPolicy = "Never" |
  .spec.containers = [.spec.containers[] | select(.name == $container) | .command = ["sleep", "14400"] | .args = [] | del(.readinessProbe) | del(.livenessProbe) | del(.startupProbe)] |
  del(.spec.initContainers)
' > /tmp/exec-pod.json

# Verify the pod spec looks correct
jq '{name: .metadata.name, namespace: .metadata.namespace, containers: [.spec.containers[].name]}' /tmp/exec-pod.json
```

This creates a pod that:
- Extracts only the app container (strips sidecars)
- Copies env vars, volumes, secrets from the source
- Runs `sleep 14400` (4 hours) instead of the app's entrypoint
- Removes probes (they'd fail since the app isn't running)

### Step 4: Optionally adjust memory

```bash
# If you need more memory (e.g., 1024Mi):
jq '.spec.containers[0].resources = {
  limits: {memory: "1024Mi"},
  requests: {memory: "1024Mi"}
}' /tmp/exec-pod.json > /tmp/exec-pod-final.json && mv /tmp/exec-pod-final.json /tmp/exec-pod.json
```

### Step 5: Create and wait for the pod

```bash
kubectl apply -f /tmp/exec-pod.json
kubectl wait --for=condition=Ready "pod/$POD_NAME" -n "$NAMESPACE" --timeout=120s
```

### Step 6: Exec into the pod

```bash
# Interactive shell
kubectl exec -it "$POD_NAME" -n "$NAMESPACE" -- bash

# Or run Rails console directly
kubectl exec -it "$POD_NAME" -n "$NAMESPACE" -- bin/rails console
```

## Cleanup

Always delete the pod when done:

```bash
kubectl delete pod "$POD_NAME" -n "$NAMESPACE" --grace-period=1
```

Find orphaned exec pods:

```bash
kubectl get pods -n "$NAMESPACE" -l ephemeral=true
```

## Troubleshooting

### Lost your variables (new terminal session)

```bash
export KUBECONFIG=/path/to/your/kubeconfig
NAMESPACE=<namespace>

# Find your most recent exec pod
POD_NAME=$(kubectl get pods -n "$NAMESPACE" -l ephemeral=true --sort-by=.metadata.creationTimestamp -o jsonpath='{.items[-1:].metadata.name}')
echo "Found pod: $POD_NAME"
```

### SSO session expired

```
The SSO session associated with this profile has expired or is otherwise invalid.
```
Re-authenticate with `aws sso login --profile <PROFILE_NAME>`.

### Pod stuck in Pending

```bash
kubectl describe pod "$POD_NAME" -n "$NAMESPACE"
```
Common causes: insufficient cluster resources, node selector can't be satisfied, image pull secrets missing.

### ImagePullBackOff

Check image pull secrets are included:
```bash
kubectl get deployment "$DEPLOYMENT_NAME" -n "$NAMESPACE" -o jsonpath='{.spec.template.spec.imagePullSecrets}'
```

### OOMKilled

Pod ran out of memory. Recreate with higher memory value in step 4.

### Container has no bash

Try `sh` instead:
```bash
kubectl exec -it "$POD_NAME" -n "$NAMESPACE" -- sh
```

## Variations

**Run a one-off command:**
```bash
kubectl exec "$POD_NAME" -n "$NAMESPACE" -- bin/rails runner "puts User.count"
```

**Shorter timeout (1 hour):**
In step 3, change `"sleep", "14400"` to `"sleep", "3600"`.
