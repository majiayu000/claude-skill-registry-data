---
name: kubernetes-skill
description: Kubernetes 클러스터 관리 스킬. kubectl로 파드/디플로이먼트/서비스 관리, 로그 조회, 포트포워딩, 디버깅 지원. "k8s", "kubectl", "파드" 키워드로 활성화.
trigger-keywords: kubernetes, k8s, kubectl, pod, pods, deployment, deployments, service, services, namespace, configmap, secret, ingress, helm, 쿠버네티스, 파드, 디플로이먼트, 서비스, 네임스페이스
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Kubernetes Skill

## Overview

Kubernetes 클러스터 관리를 위한 포괄적인 스킬입니다.
kubectl CLI를 통해 클러스터 운영, 리소스 관리, 로그 검사, 디버깅, 배포 자동화를 지원합니다.

## When to Use

**명시적 요청:**
- "파드 상태 확인해줘"
- "디플로이먼트 스케일 조정해줘"
- "로그 보여줘"
- "포트포워딩 설정해줘"
- "매니페스트 적용해줘"

**자동 활성화 키워드:**
- "kubernetes", "k8s", "kubectl"
- "pod", "deployment", "service", "namespace"
- "helm", "ingress", "configmap", "secret"
- "쿠버네티스", "파드", "디플로이먼트"

## Features

### 1. **Cluster Operations**
- **Context Management**: Switch between clusters and namespaces
- **Cluster Info**: View cluster status, nodes, and resources
- **Health Checks**: Verify cluster and component health

### 2. **Resource Management**
- **Pods**: List, describe, delete, exec into pods
- **Deployments**: Create, scale, rollout, rollback deployments
- **Services**: Manage service endpoints and load balancers
- **ConfigMaps/Secrets**: Create and manage configuration
- **Namespaces**: Organize and isolate resources

### 3. **Debugging & Troubleshooting**
- **Logs**: View and follow container logs
- **Events**: Inspect cluster and resource events
- **Describe**: Detailed resource inspection
- **Port Forward**: Access services locally

### 4. **Deployment Operations**
- **Apply**: Apply YAML manifests
- **Rollout**: Manage deployment rollouts
- **Scale**: Adjust replica counts
- **Delete**: Remove resources

## Prerequisites

This skill requires `kubectl` CLI to be installed and configured:

```bash
# macOS
brew install kubectl

# Verify installation
kubectl version --client

# Check cluster connection
kubectl cluster-info
```

## Workflow

### Step 1: 클러스터 연결 확인

```bash
# 현재 컨텍스트 확인
kubectl config current-context

# 클러스터 연결 테스트
kubectl cluster-info
```

### Step 2: 작업 유형별 분기

**조회 작업 (Read):**
1. `kubectl get` 으로 리소스 목록 조회
2. `kubectl describe` 로 상세 정보 확인
3. `kubectl logs` 로 로그 조회

**변경 작업 (Write):**
1. 현재 상태 확인 (`get`, `describe`)
2. 변경 명령 실행 (`apply`, `scale`, `delete`)
3. 결과 확인 및 롤백 준비

**디버깅:**
1. `kubectl get events` 로 이벤트 확인
2. `kubectl describe` 로 상세 상태 확인
3. `kubectl logs --previous` 로 이전 로그 확인

---

## Usage Scenarios

### Scenario 1: Check Pod Status

**User Request**: "Show me all pods in the production namespace"

**Skill Actions**:
1. Execute `kubectl get pods -n production`
2. Format output with status, restarts, and age
3. Highlight any pods not in Running state

### Scenario 2: View Pod Logs

**User Request**: "Show logs for the api-server pod"

**Skill Actions**:
1. Find matching pod(s) with `kubectl get pods`
2. Execute `kubectl logs <pod-name>` with appropriate flags
3. Support multi-container pods with `-c` flag
4. Optionally follow logs with `-f` flag

### Scenario 3: Debug Failing Deployment

**User Request**: "Why is my deployment failing?"

**Skill Actions**:
1. Get deployment status with `kubectl get deployment`
2. Describe deployment for events `kubectl describe deployment`
3. Check pod status and events
4. Analyze container restart reasons
5. Provide actionable recommendations

### Scenario 4: Scale Deployment

**User Request**: "Scale the web-app deployment to 5 replicas"

**Skill Actions**:
1. Verify current deployment state
2. Execute `kubectl scale deployment web-app --replicas=5`
3. Monitor rollout progress
4. Confirm scaling completed

### Scenario 5: Port Forward to Service

**User Request**: "Forward local port 8080 to the api service"

**Skill Actions**:
1. Find service or pod matching criteria
2. Execute `kubectl port-forward svc/api 8080:80`
3. Provide access instructions
4. Handle cleanup on termination

### Scenario 6: Apply Configuration

**User Request**: "Apply this Kubernetes manifest"

**Skill Actions**:
1. Validate YAML syntax
2. Execute `kubectl apply -f <manifest>`
3. Verify resource creation/update
4. Report any errors or warnings

## Environment Variables

Optional environment variables for configuration:

```bash
# Default namespace (if not specified)
KUBE_NAMESPACE=default

# Kubeconfig file path (optional, uses default if not set)
KUBECONFIG=~/.kube/config

# Default context (optional)
KUBE_CONTEXT=my-cluster
```

## Core Commands Reference

### Cluster Information

```bash
# View current context
kubectl config current-context

# List all contexts
kubectl config get-contexts

# Switch context
kubectl config use-context <context-name>

# Cluster info
kubectl cluster-info

# Node status
kubectl get nodes -o wide
```

### Pod Operations

```bash
# List pods (all namespaces)
kubectl get pods -A

# List pods (specific namespace)
kubectl get pods -n <namespace>

# Pod details
kubectl describe pod <pod-name> -n <namespace>

# Pod logs
kubectl logs <pod-name> -n <namespace>
kubectl logs <pod-name> -c <container> -n <namespace>  # multi-container
kubectl logs -f <pod-name> -n <namespace>  # follow logs
kubectl logs --tail=100 <pod-name> -n <namespace>  # last 100 lines

# Execute command in pod
kubectl exec -it <pod-name> -n <namespace> -- /bin/sh

# Delete pod
kubectl delete pod <pod-name> -n <namespace>
```

### Deployment Operations

```bash
# List deployments
kubectl get deployments -n <namespace>

# Deployment details
kubectl describe deployment <name> -n <namespace>

# Scale deployment
kubectl scale deployment <name> --replicas=<count> -n <namespace>

# Rollout status
kubectl rollout status deployment/<name> -n <namespace>

# Rollout history
kubectl rollout history deployment/<name> -n <namespace>

# Rollback
kubectl rollout undo deployment/<name> -n <namespace>

# Restart deployment
kubectl rollout restart deployment/<name> -n <namespace>
```

### Service Operations

```bash
# List services
kubectl get svc -n <namespace>

# Service details
kubectl describe svc <name> -n <namespace>

# Port forward
kubectl port-forward svc/<name> <local-port>:<service-port> -n <namespace>
kubectl port-forward pod/<pod-name> <local-port>:<container-port> -n <namespace>
```

### ConfigMap & Secret Operations

```bash
# List configmaps
kubectl get configmap -n <namespace>

# View configmap
kubectl get configmap <name> -n <namespace> -o yaml

# Create configmap from file
kubectl create configmap <name> --from-file=<path> -n <namespace>

# List secrets
kubectl get secrets -n <namespace>

# View secret (base64 encoded)
kubectl get secret <name> -n <namespace> -o yaml

# Decode secret value
kubectl get secret <name> -n <namespace> -o jsonpath='{.data.<key>}' | base64 -d
```

### Namespace Operations

```bash
# List namespaces
kubectl get namespaces

# Create namespace
kubectl create namespace <name>

# Delete namespace
kubectl delete namespace <name>

# Set default namespace for context
kubectl config set-context --current --namespace=<namespace>
```

### Resource Management

```bash
# Apply manifest
kubectl apply -f <file.yaml>
kubectl apply -f <directory>/

# Delete resources
kubectl delete -f <file.yaml>
kubectl delete <resource-type> <name> -n <namespace>

# Get all resources
kubectl get all -n <namespace>

# Watch resources
kubectl get pods -n <namespace> -w
```

### Debugging Commands

```bash
# Events (cluster-wide)
kubectl get events --sort-by='.lastTimestamp'

# Events (namespace)
kubectl get events -n <namespace> --sort-by='.lastTimestamp'

# Resource usage
kubectl top nodes
kubectl top pods -n <namespace>

# Describe for troubleshooting
kubectl describe pod <pod-name> -n <namespace>

# Check container status
kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.status.containerStatuses}'
```

## Common Troubleshooting Patterns

### Pod Not Starting

```bash
# 1. Check pod status
kubectl get pod <pod-name> -n <namespace>

# 2. Describe for events
kubectl describe pod <pod-name> -n <namespace>

# 3. Check logs (if container started)
kubectl logs <pod-name> -n <namespace> --previous

# Common issues:
# - ImagePullBackOff: Check image name, registry credentials
# - CrashLoopBackOff: Check application logs, resource limits
# - Pending: Check node resources, PVC binding
```

### Deployment Not Rolling Out

```bash
# 1. Check deployment status
kubectl rollout status deployment/<name> -n <namespace>

# 2. Check replica sets
kubectl get rs -n <namespace>

# 3. Describe deployment
kubectl describe deployment <name> -n <namespace>

# 4. Check pod events
kubectl get events -n <namespace> --field-selector involvedObject.kind=Pod
```

### Service Not Accessible

```bash
# 1. Check service exists
kubectl get svc <name> -n <namespace>

# 2. Check endpoints
kubectl get endpoints <name> -n <namespace>

# 3. Check pod labels match selector
kubectl get pods -n <namespace> --show-labels

# 4. Test from within cluster
kubectl run test --rm -it --image=busybox -- wget -qO- http://<service>:<port>
```

## Security Policy

### Read-Focused Operations

**Primary Use Cases:**
- `kubectl get` - View resources
- `kubectl describe` - Inspect details
- `kubectl logs` - View container logs
- `kubectl top` - Resource metrics
- `kubectl events` - Cluster events

### Write Operations (Require Confirmation)

**Modifying Operations:**
- `kubectl apply` - Apply configurations
- `kubectl scale` - Scale deployments
- `kubectl delete` - Remove resources
- `kubectl rollout` - Deployment operations

### Blocked Operations

**Destructive Commands:**
- `kubectl delete namespace kube-system` - System namespace deletion
- `kubectl delete --all` - Bulk deletion without specific target
- `kubectl drain` without flags - Node draining without safety flags

## Best Practices

### 1. Always Specify Namespace

```bash
# Explicit namespace prevents accidents
kubectl get pods -n production

# Set namespace for session
kubectl config set-context --current --namespace=production
```

### 2. Use Labels for Selection

```bash
# Select by label
kubectl get pods -l app=web-server

# Delete by label
kubectl delete pods -l app=test-app
```

### 3. Dry Run Before Apply

```bash
# Validate without applying
kubectl apply -f manifest.yaml --dry-run=client

# Server-side validation
kubectl apply -f manifest.yaml --dry-run=server
```

### 4. Use Output Formats

```bash
# JSON output for parsing
kubectl get pods -o json

# YAML for backup/editing
kubectl get deployment <name> -o yaml > deployment-backup.yaml

# Custom columns
kubectl get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase
```

## Helm Integration

For Helm chart management:

```bash
# List releases
helm list -n <namespace>

# Install chart
helm install <release> <chart> -n <namespace>

# Upgrade release
helm upgrade <release> <chart> -n <namespace>

# Rollback
helm rollback <release> <revision> -n <namespace>

# Uninstall
helm uninstall <release> -n <namespace>
```

## Integration with Claude Code

The skill integrates seamlessly with Claude Code's workflow:

1. **Automatic Activation**: Triggered by keywords like "kubernetes", "k8s", "kubectl", "pod"
2. **Context Awareness**: Remembers namespace and context preferences
3. **Error Analysis**: Provides actionable recommendations for common errors
4. **YAML Generation**: Can generate Kubernetes manifests from descriptions
5. **Multi-Cluster Support**: Works with multiple kubeconfig contexts

## Examples

### Example 1: Quick Cluster Overview

```
User: "Show me the cluster status"

Skill executes:
  kubectl cluster-info
  kubectl get nodes
  kubectl get pods -A --field-selector=status.phase!=Running

Returns:
  Cluster: kubernetes-production (healthy)
  Nodes: 3/3 Ready
  Problematic Pods: 2 found
    - api-server-xyz (CrashLoopBackOff)
    - worker-abc (Pending)
```

### Example 2: Application Deployment

```
User: "Deploy nginx with 3 replicas to the web namespace"

Skill generates manifest and executes:
  kubectl create deployment nginx --image=nginx:latest --replicas=3 -n web
  kubectl expose deployment nginx --port=80 --type=ClusterIP -n web
  kubectl rollout status deployment/nginx -n web

Returns:
  Deployment nginx created successfully
  Service nginx exposed on port 80
  All 3 replicas are running
```

### Example 3: Log Analysis

```
User: "Show me error logs from the payment-service"

Skill executes:
  kubectl get pods -n production -l app=payment-service
  kubectl logs -l app=payment-service -n production --tail=500 | grep -i error

Returns:
  Found 2 pods running payment-service
  Recent errors:
    [2025-01-10 10:23:45] ERROR: Database connection timeout
    [2025-01-10 10:24:12] ERROR: Retry failed after 3 attempts
```

## Troubleshooting

### kubectl Not Found

```bash
# Install kubectl
brew install kubectl  # macOS
apt-get install kubectl  # Debian/Ubuntu
```

### Cannot Connect to Cluster

```bash
# Check kubeconfig
echo $KUBECONFIG
cat ~/.kube/config

# Test connection
kubectl cluster-info

# Verify context
kubectl config current-context
```

### Permission Denied

```bash
# Check RBAC permissions
kubectl auth can-i get pods
kubectl auth can-i --list

# View your identity
kubectl auth whoami
```

## Related Skills

- **Docker Skill**: Container image management
- **Helm Skill**: Kubernetes package management
- **Terraform Skill**: Infrastructure provisioning
- **CI/CD Skills**: Deployment automation

## References

- [Kubernetes Official Documentation](https://kubernetes.io/docs/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Kubernetes Troubleshooting Guide](https://kubernetes.io/docs/tasks/debug/)
- [Helm Documentation](https://helm.sh/docs/)
