---
name: kubernetes
description: Comprehensive Kubernetes cluster management skill. Use this skill when working with Kubernetes resources, kubectl operations, Helm charts, container orchestration, debugging pods, managing deployments, or any Kubernetes-related infrastructure tasks.
allowed-tools:
  - Bash(kubectl:*)
  - Bash(helm:*)
  - Bash(kustomize:*)
---

# Kubernetes Management Skill

This skill provides comprehensive capabilities for managing Kubernetes clusters, resources, and workloads using kubectl, Helm, and Kustomize.

## When to Use This Skill

Use this skill when working with:
- Kubernetes resources (pods, deployments, services, configmaps, secrets, etc.)
- Debugging containerized applications and troubleshooting cluster issues
- Helm chart installation, upgrades, and management
- kubectl operations (get, describe, apply, create, delete, logs, exec, scale, rollout)
- Context and namespace management
- Deployment strategies (rolling updates, blue-green, canary)
- Configuration management and resource optimization

## How to Use This Skill

### 1. Verify Context and Namespace

**Always start by verifying your current context and namespace:**
```bash
kubectl config current-context
kubectl config view --minify
```

Set namespace if needed:
```bash
kubectl config set-context --current --namespace=<namespace>
```

### 2. Load Appropriate Reference Files

Based on the task at hand, load the relevant reference documentation:

**For kubectl Operations:**
Load [kubectl Reference](./references/kubectl_reference.md) when you need detailed information about:
- Getting, describing, creating, updating, or deleting resources
- Viewing logs or executing commands in containers
- Port forwarding and debugging
- Scaling deployments
- Managing rollouts and rollbacks
- Context and namespace operations
- Output formats and filtering

**For Helm Operations:**
Load [Helm Reference](./references/helm_reference.md) when you need detailed information about:
- Installing or upgrading Helm charts
- Managing releases (list, status, uninstall, rollback)
- Repository management
- Chart development and inspection
- Values configuration and overrides
- Troubleshooting Helm issues

**For Common Workflows:**
Load [Workflows Reference](./references/workflows.md) when you need guidance on:
- Debugging failing pods or services
- Deploying applications
- Updating deployments with different strategies
- Blue-green and canary deployments
- Configuration management (ConfigMaps and Secrets)
- Maintenance operations (draining nodes, backup/restore)
- Cluster inspection and cleanup

**For Best Practices:**
Load [Best Practices Reference](./references/best_practices.md) when you need guidance on:
- Safety and validation before operations
- Efficiency and optimization
- Debugging approaches
- YAML and manifest management
- High availability patterns
- Error handling and troubleshooting
- Integration with other tools
- Environment-specific practices

### 3. General Workflow

**For Resource Management:**
1. Verify context and namespace
2. Use `kubectl get` to list resources
3. Use `kubectl describe` for detailed information
4. Apply changes with `kubectl apply` or `kubectl patch`
5. Monitor with `kubectl rollout status` or `kubectl get events`

**For Debugging:**
1. Check pod status with `kubectl get pods`
2. Describe the resource with `kubectl describe`
3. View logs with `kubectl logs`
4. Check events with `kubectl get events`
5. Exec into container if needed with `kubectl exec -it`

**For Deployments:**
1. Validate manifests with `--dry-run`
2. Apply manifests with `kubectl apply`
3. Monitor rollout with `kubectl rollout status`
4. Verify with `kubectl get` and `kubectl logs`
5. Rollback if needed with `kubectl rollout undo`

## Key Principles

### Safety First
- Always verify context and namespace before operations
- Use `--dry-run=client` or `--dry-run=server` to validate changes
- Use `kubectl diff` to preview changes before applying
- Be cautious with destructive operations (delete, force, drain)

### Declarative Over Imperative
- Prefer `kubectl apply -f file.yaml` over imperative commands
- Store manifests in version control
- Use Kustomize for environment-specific overlays
- Make infrastructure reproducible and auditable

### Efficient Resource Usage
- Use label selectors to operate on groups of resources
- Use output formats (`-o json|yaml`) for automation and parsing
- Filter with `--field-selector` and sort with `--sort-by`
- Watch resources in real-time with `-w` flag

### Systematic Debugging
- Follow the debugging workflow: status → describe → logs → events → exec
- Use timestamps in logs for correlation
- Check recent events with `kubectl get events --sort-by='.lastTimestamp'`
- Test connectivity with temporary debug pods

## Quick Command Reference

**Most Common Operations:**
```bash
# Get resources
kubectl get pods
kubectl get pods -o wide
kubectl get pods -l app=myapp

# Describe for details
kubectl describe pod <pod-name>

# View logs
kubectl logs <pod-name>
kubectl logs <pod-name> -f
kubectl logs <pod-name> --previous

# Exec into pod
kubectl exec -it <pod-name> -- /bin/sh

# Apply manifests
kubectl apply -f deployment.yaml
kubectl apply -f ./manifests/

# Scale deployment
kubectl scale deployment/<name> --replicas=3

# Check rollout
kubectl rollout status deployment/<name>
kubectl rollout undo deployment/<name>

# Port forward
kubectl port-forward service/<name> 8080:80

# Helm operations
helm install <release> <chart>
helm upgrade <release> <chart>
helm list
helm uninstall <release>
```

## Important Notes

- Reference files contain comprehensive details - load them as needed to avoid context overhead
- Always validate configurations before applying to production
- Use namespaces for resource isolation
- Set resource requests and limits for all containers
- Implement health checks (liveness, readiness, startup probes)
- Use PodDisruptionBudgets for high availability
- Store sensitive data in Secrets, not ConfigMaps
- Tag images with specific versions, avoid `:latest` in production

## Integration Points

This skill works well with:
- **Docker** for container image management
- **Git** for manifest version control (GitOps)
- **Terraform** for infrastructure provisioning
- **CI/CD pipelines** for automated deployments
- **Monitoring tools** (Prometheus, Grafana) for observability
- **Logging systems** (EFK stack) for centralized logging

---

**Remember:** Load the specific reference files only when you need detailed information about kubectl commands, Helm operations, specific workflows, or best practices. This keeps the context manageable and efficient.
