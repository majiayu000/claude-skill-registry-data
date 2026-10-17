---
name: k8s-troubleshooter
description: "Systematic Kubernetes troubleshooting and incident response. Use this skill whenever the user mentions Kubernetes, K8s, kubectl, pods, containers, or clusters. Triggers include diagnosing CrashLoopBackOff, ImagePullBackOff, OOMKilled, or Pending pods, responding to production incidents, troubleshooting node NotReady or DiskPressure, debugging service connectivity or networking, investigating PVC or storage failures, analyzing performance degradation, checking cluster health, troubleshooting Helm releases, and conducting post-incident reviews."
---

# Kubernetes Troubleshooter & Incident Response

Systematic approach to diagnosing and resolving Kubernetes issues in production environments.

## Core Troubleshooting Workflow

Follow this systematic approach for any Kubernetes issue:

### 1. Gather Context
- What is the observed symptom?
- When did it start?
- What changed recently (deployments, config, infrastructure)?
- What is the scope (single pod, service, node, cluster)?
- What is the business impact (severity level)?

### 2. Initial Triage

Run cluster health check:
```bash
# Check node status and health
kubectl get nodes

# Find non-running pods across all namespaces
kubectl get pods -A --field-selector status.phase!=Running

# Check node resource usage
kubectl top nodes
```

This provides an overview of:
- Node health status
- Pending and failed pods across all namespaces
- Node resource utilization

### 3. Deep Dive Investigation

Based on triage results, focus investigation:

**For Namespace-Level Issues:**
```bash
python3 scripts/check_namespace.py <namespace>
```

This provides comprehensive namespace health:
- Pod status (running, pending, failed, crashlooping)
- Service health and endpoints
- Deployment availability
- PVC status
- Resource quota usage
- Recent events
- Actionable recommendations

**For Pod Issues:**
```bash
# Get full pod details (status, events, conditions, resource config)
kubectl describe pod <pod-name> -n <namespace>

# Check current and previous container logs
kubectl logs <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> --previous

# Get events specific to the pod
kubectl get events -n <namespace> --field-selector involvedObject.name=<pod-name>
```

This reveals:
- Pod phase and readiness
- Container statuses and states
- Restart counts and exit codes
- Recent events and scheduling decisions
- Resource requests and limits

**For additional investigations:**
- Check all namespace events: `kubectl get events -n <namespace> --sort-by='.lastTimestamp'`

### 4. Identify Root Cause

Consult references/common_issues.md for detailed information on:
- ImagePullBackOff / ErrImagePull
- CrashLoopBackOff
- Pending Pods
- OOMKilled
- Node issues (NotReady, DiskPressure)
- Networking failures
- Storage/PVC issues
- Resource quotas and throttling
- RBAC permission errors

Each issue includes:
- Symptoms
- Common causes
- Diagnostic commands
- Remediation steps
- Prevention strategies

### 5. Apply Remediation

Follow remediation steps from common_issues.md based on root cause identified.

Always:
- Test fixes in non-production first if possible
- Document actions taken
- Monitor for effectiveness
- Have rollback plan ready

### 6. Verify & Monitor

After applying fix:
- Verify issue is resolved
- Monitor for recurrence (15-30 minutes minimum)
- Check related systems
- Update documentation

## Incident Response

For production incidents, follow structured response in references/incident_response.md:

**Severity Assessment:**
- SEV-1 (Critical): Complete outage, data loss, security breach
- SEV-2 (High): Major degradation, significant user impact
- SEV-3 (Medium): Minor impairment, workaround available
- SEV-4 (Low): Cosmetic, minimal impact

**Incident Phases:**
1. **Detection** - Identify and assess
2. **Triage** - Determine scope and impact
3. **Investigation** - Find root cause
4. **Resolution** - Apply fix
5. **Post-Incident** - Document and improve

**Common Incident Scenarios:**
- Complete cluster outage
- Service degradation
- Node failure
- Storage issues
- Security incidents

See references/incident_response.md for detailed playbooks.

## Quick Reference Commands

### Cluster Overview
```bash
kubectl cluster-info
kubectl get nodes
kubectl get pods --all-namespaces | grep -v Running
kubectl get events --all-namespaces --sort-by='.lastTimestamp' | tail -20
```

### Pod Diagnostics
```bash
kubectl describe pod <pod> -n <namespace>
kubectl logs <pod> -n <namespace>
kubectl logs <pod> -n <namespace> --previous
kubectl exec -it <pod> -n <namespace> -- /bin/sh
kubectl get pod <pod> -n <namespace> -o yaml
```

### Node Diagnostics
```bash
kubectl describe node <node>
kubectl top nodes
kubectl top pods --all-namespaces
ssh <node> "systemctl status kubelet"
ssh <node> "journalctl -u kubelet -n 100"
```

### Service & Network
```bash
kubectl describe svc <service> -n <namespace>
kubectl get endpoints <service> -n <namespace>
kubectl get networkpolicies --all-namespaces
```

### Storage
```bash
kubectl get pvc,pv --all-namespaces
kubectl describe pvc <pvc> -n <namespace>
kubectl get storageclass
```

### Resource & Configuration
```bash
kubectl describe resourcequota -n <namespace>
kubectl describe limitrange -n <namespace>
kubectl get rolebindings,clusterrolebindings -n <namespace>
```

## Diagnostic Scripts

### check_namespace.py

Namespace-level health check and diagnostics:
- Pod health (running, pending, failed, crashlooping, image pull errors)
- Service health and endpoints
- Deployment availability status
- PersistentVolumeClaim status
- Resource quota usage and limits
- Recent namespace events
- Health status assessment
- Actionable recommendations

**Usage:**
```bash
# Human-readable output
python3 scripts/check_namespace.py <namespace>

# JSON output for automation
python3 scripts/check_namespace.py <namespace> --json

# Include more events
python3 scripts/check_namespace.py <namespace> --events 20
```

Best used when troubleshooting issues in a specific namespace or assessing overall namespace health.

### Cluster-Level Diagnostics (kubectl)

For cluster-wide health checks, use kubectl directly:
```bash
# Node health and status
kubectl get nodes
kubectl top nodes

# Find non-running pods across all namespaces
kubectl get pods -A --field-selector status.phase!=Running

# System pod health
kubectl get pods -n kube-system
```

### Pod-Level Diagnostics (kubectl)

For detailed pod investigation, use kubectl directly:
```bash
# Full pod details (status, events, conditions, resource config)
kubectl describe pod <pod-name> -n <namespace>

# Current and previous container logs
kubectl logs <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> --previous

# Events specific to the pod
kubectl get events -n <namespace> --field-selector involvedObject.name=<pod-name>
```

## Reference Documentation

### references/common_issues.md
Comprehensive guide to common Kubernetes issues with:
- Detailed symptom descriptions
- Root cause analysis
- Step-by-step diagnostic procedures
- Remediation instructions
- Prevention strategies

Covers:
- Pod issues (ImagePullBackOff, CrashLoopBackOff, Pending, OOMKilled)
- Node issues (NotReady, DiskPressure)
- Networking issues (pod-to-pod communication, service access)
- Storage issues (PVC pending, volume mount failures)
- Resource issues (quota exceeded, CPU throttling)
- Security issues (vulnerabilities, RBAC)

Read this when you identify a specific issue type but need detailed remediation steps.

### references/incident_response.md
Structured incident response framework including:
- Incident response phases (Detection → Triage → Investigation → Resolution → Post-Incident)
- Severity level definitions
- Detailed playbooks for common incident scenarios
- Communication guidelines
- Post-incident review template
- Best practices for prevention, preparedness, response, and recovery

Read this when responding to production incidents or planning incident response procedures.

### references/performance_troubleshooting.md

Comprehensive performance diagnosis and optimization guide covering:
- **High Latency Issues** - API response time, request latency troubleshooting
- **CPU Performance** - Throttling detection, profiling, optimization
- **Memory Performance** - OOM issues, leak detection, heap profiling
- **Network Performance** - Latency, packet loss, DNS resolution
- **Storage I/O Performance** - Disk performance testing, optimization
- **Application-Level Metrics** - Prometheus integration, distributed tracing
- **Cluster-Wide Performance** - Control plane, scheduler, resource utilization

Read this when:
- Investigating slow application response times
- Diagnosing CPU or memory performance issues
- Troubleshooting network latency or connectivity
- Optimizing storage I/O performance
- Setting up performance monitoring

### references/helm_troubleshooting.md

Complete guide to Helm troubleshooting including:
- **Release Issues** - Stuck releases, missing resources, state problems
- **Installation Failures** - Chart conflicts, validation errors, template rendering
- **Upgrade and Rollback** - Failed upgrades, immutable field errors, rollback procedures
- **Values and Configuration** - Values not applied, parsing errors, secret handling
- **Chart Dependencies** - Dependency updates, version conflicts, subchart values
- **Hooks and Lifecycle** - Hook failures, cleanup issues
- **Repository Issues** - Chart access problems, version mismatches

Read this when:
- Working with Helm-deployed applications
- Troubleshooting chart installations or upgrades
- Debugging Helm release states
- Managing chart dependencies
