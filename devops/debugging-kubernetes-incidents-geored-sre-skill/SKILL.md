---
name: debugging-kubernetes-incidents
description: Use when investigating Kubernetes pod failures, crashes, resource issues, or service degradation. Provides systematic investigation methodology for incident triage, root cause analysis, and remediation planning in any Kubernetes environment.
---

# Debugging Kubernetes Incidents

## Overview

**Core Principles:**
- **Read-Only Investigation** - Observe and analyze, never modify resources
- **Systematic Methodology** - Follow structured phases for thorough analysis
- **Multi-Source Correlation** - Combine logs, events, metrics for complete picture
- **Root Cause Focus** - Identify underlying cause, not just symptoms

**Key Abbreviations:**
- **RCA** - Root Cause Analysis
- **MTTR** - Mean Time To Resolution
- **P1/P2/P3/P4** - Severity levels (Critical/High/Medium/Low)

## When to Use

Invoke this skill when:
- ✅ Pods are crashing, restarting, or stuck in `CrashLoopBackOff`
- ✅ Services are returning errors or experiencing high latency
- ✅ Resources are exhausted (CPU, memory, storage)
- ✅ Certificate errors or TLS handshake failures occur
- ✅ Deployments are failing or stuck in rollout
- ✅ Need to perform incident triage or post-mortem analysis

## Quick Reference: Investigation Phases

| Phase | Focus | Primary Tools |
|-------|-------|--------------|
| **1. Triage** | Severity & scope | Pod status, events |
| **2. Data Collection** | Logs, events, metrics | kubectl logs, events, top |
| **3. Correlation** | Pattern detection | Timeline analysis |
| **4. Root Cause** | Underlying issue | Multi-source synthesis |
| **5. Remediation** | Fix & prevention | Recommendations only |

## Common Confusions

### Wrong vs. Correct Approaches

❌ **WRONG:** Jump directly to pod logs without checking events
✅ **CORRECT:** Check events first to understand context, then investigate logs

❌ **WRONG:** Only look at the current pod state
✅ **CORRECT:** Check previous container logs if pod restarted (use `--previous` flag)

❌ **WRONG:** Investigate single data source in isolation
✅ **CORRECT:** Correlate logs + events + metrics for complete picture

❌ **WRONG:** Assume first error found is root cause
✅ **CORRECT:** Identify temporal sequence - what happened FIRST?

❌ **WRONG:** Recommend changes without understanding full impact
✅ **CORRECT:** Provide read-only recommendations with manual review required

## Decision Tree: Incident Type

**Q: Is the pod running?**
- **No** → Check pod status and events
  - ImagePullBackOff → [Image Pull Issues](#image-pull-issues)
  - Pending → [Resource Constraints](#resource-constraints)
  - CrashLoopBackOff → [Application Crashes](#application-crashes)
  - OOMKilled → [Memory Issues](#memory-issues)

**Q: Is the pod running but unhealthy?**
- **Yes** → Check logs and resource usage
  - High CPU/Memory → [Resource Saturation](#resource-saturation)
  - Application errors → [Log Analysis](#log-analysis)
  - Failed health checks → [Liveness/Readiness Probes](#probe-failures)

**Q: Is this a service-level issue?**
- **Yes** → Check service endpoints and network
  - No endpoints → [Pod Selector Issues](#selector-issues)
  - Connection timeouts → [Network Issues](#network-issues)
  - Certificate errors → [TLS Issues](#tls-issues)

## Rules: Investigation Methodology

### Phase 1: Triage

**CRITICAL:** Assess severity before diving deep

1. **Determine incident type**:
   - Pod-level: Single pod failure
   - Deployment-level: Multiple pods affected
   - Service-level: API/service unavailable
   - Cluster-level: Node or system-wide issue

2. **Assess severity**:
   - **P1 (Critical)**: Production service down, data loss risk
   - **P2 (High)**: Major feature broken, significant user impact
   - **P3 (Medium)**: Minor feature degraded, limited impact
   - **P4 (Low)**: No immediate user impact

3. **Identify scope**:
   - Single pod, deployment, namespace, or cluster-wide?
   - How many users affected?
   - What services depend on this?

### Phase 2: Data Collection

**Gather comprehensive data from multiple sources:**

**Pod Information:**
```bash
kubectl get pods -n <namespace>
kubectl describe pod <pod-name> -n <namespace>
kubectl get pod <pod-name> -n <namespace> -o yaml
```

**Logs:**
```bash
# Current logs
kubectl logs <pod-name> -n <namespace> --tail=100

# Previous container (if restarted)
kubectl logs <pod-name> -n <namespace> --previous

# All containers in pod
kubectl logs <pod-name> -n <namespace> --all-containers=true
```

**Events:**
```bash
# Namespace events
kubectl get events -n <namespace> --sort-by='.lastTimestamp'

# Pod-specific events
kubectl describe pod <pod-name> -n <namespace> | grep -A 10 Events
```

**Resource Usage:**
```bash
kubectl top pods -n <namespace>
kubectl top nodes
```

### Phase 3: Correlation & Analysis

**Create unified timeline:**

1. **Extract timestamps** from logs, events, metrics
2. **Align data sources** on common timeline
3. **Identify temporal patterns**:
   - What happened first? (root cause)
   - What happened simultaneously? (correlation)
   - What happened after? (cascading effects)

**Look for common patterns:**
- Memory spike → OOMKilled → Pod restart
- Image pull failure → Pending → Timeout
- Probe failure → Unhealthy → Traffic removed
- Certificate expiry → TLS errors → Connection failures

### Phase 4: Root Cause Determination

**CRITICAL:** Distinguish correlation from causation

**Validate root cause:**
1. **Temporal precedence**: Did it happen BEFORE the symptom?
2. **Causal mechanism**: Does it logically explain the symptom?
3. **Evidence**: Is there supporting data from multiple sources?

**Common root causes:**
- Application bugs (crashes, exceptions)
- Resource exhaustion (CPU, memory, disk)
- Configuration errors (wrong env vars, missing secrets)
- Network issues (DNS failures, timeouts)
- Infrastructure problems (node failures, storage issues)

### Phase 5: Remediation Planning

**Provide structured recommendations:**

**Immediate mitigation:**
- Rollback deployment
- Scale resources
- Restart pods
- Apply emergency config

**Permanent fix:**
- Code changes
- Resource limit adjustments
- Configuration updates
- Infrastructure improvements

**Prevention:**
- Monitoring alerts
- Resource quotas
- Automated testing
- Runbook updates

## Common Issue Types

### Image Pull Issues

**Symptoms:**
- Pod status: `ImagePullBackOff` or `ErrImagePull`
- Events: "Failed to pull image"

**Investigation:**
```
├── Check image name and tag in pod spec
├── Verify image exists in registry
├── Check image pull secrets
└── Validate network connectivity to registry
```

**Common causes:**
- Wrong image name/tag
- Missing/expired image pull secret
- Private registry authentication failure
- Network connectivity to registry

### Resource Constraints

**Symptoms:**
- Pod status: `Pending`
- Events: "Insufficient cpu/memory"

**Investigation:**
```
├── Check namespace resource quotas
├── Check pod resource requests/limits
├── Review node capacity
└── Check for pod priority and preemption
```

**Common causes:**
- Namespace quota exceeded
- Insufficient cluster capacity
- Resource requests too high
- No nodes matching pod requirements

### Application Crashes

**Symptoms:**
- Pod status: `CrashLoopBackOff`
- Container exit code: non-zero
- Frequent restarts

**Investigation:**
```
├── Get logs from current container
├── Get logs from previous container (--previous)
├── Check exit code in pod status
├── Review application startup logs
└── Check for environment variable issues
```

**Common causes:**
- Application exceptions/errors
- Missing required environment variables
- Database connection failures
- Invalid configuration

### Memory Issues

**Symptoms:**
- Pod status shows: `OOMKilled`
- Events: "Container exceeded memory limit"
- High memory usage before restart

**Investigation:**
```
├── Check memory limits vs actual usage
├── Review memory usage trends
├── Analyze for memory leaks
└── Check for spike patterns
```

**Common causes:**
- Memory leak in application
- Insufficient memory limits
- Unexpected traffic spike
- Large dataset processing

### TLS Issues

**Symptoms:**
- Logs show: "tls: bad certificate" or "x509: certificate has expired"
- Connection failures between services
- HTTP 503 errors

**Investigation:**
```
├── Check certificate expiration dates
├── Verify certificate CN/SAN matches hostname
├── Check CA bundle configuration
└── Review certificate secret in namespace
```

**Common causes:**
- Expired certificates
- Certificate CN mismatch
- Missing CA certificate
- Incorrect certificate chain

## Real-World Example: Pod Crash Loop Investigation

**Scenario:** API gateway pods crashing repeatedly

**Step 1: Triage**
```bash
$ kubectl get pods -n production | grep api-gateway
api-gateway-7d8f9b-xyz   0/1   CrashLoopBackOff   5   10m
```
Severity: P2 (High) - Production API affected

**Step 2: Check Events**
```bash
$ kubectl describe pod api-gateway-7d8f9b-xyz -n production | grep -A 10 Events
Events:
  10m   Warning   BackOff   Pod   Back-off restarting failed container
  9m    Warning   Failed    Pod   Error: container exceeded memory limit
```
Key finding: OOMKilled event

**Step 3: Check Logs (Previous Container)**
```bash
$ kubectl logs api-gateway-7d8f9b-xyz -n production --previous --tail=50
...
[ERROR] Database connection pool exhausted: 50/50 connections in use
[WARN] High memory pressure detected
[CRITICAL] Memory usage at 98%, OOM imminent
```
Pattern: Connection pool → Memory pressure → OOM

**Step 4: Check Resource Limits**
```bash
$ kubectl get pod api-gateway-7d8f9b-xyz -n production -o yaml | grep -A 5 resources
resources:
  limits:
    memory: "2Gi"
  requests:
    memory: "1Gi"
```

**Step 5: Root Cause Analysis**
```
Timeline:
09:00 - Database query slowdown (from logs)
09:05 - Connection pool exhausted
09:10 - Memory usage spike (connections held)
09:15 - OOM killed
09:16 - Pod restart
```

**Root Cause:** Slow database queries → connection pool exhaustion → memory leak → OOM

**Recommendations:**
```markdown
Immediate:
1. Increase memory limit to 4Gi (temporary)
2. Add connection timeout (10s)

Permanent:
1. Optimize slow database query
2. Increase connection pool size
3. Implement connection timeout
4. Add memory alerts at 80%

Prevention:
1. Monitor database query performance
2. Add Prometheus alert for connection pool usage
3. Regular load testing
```

## Troubleshooting Decision Matrix

| Symptom | First Check | Common Cause | Quick Fix |
|---------|-------------|--------------|-----------|
| ImagePullBackOff | `describe pod` events | Wrong image/registry | Fix image name |
| Pending | Resource quotas | Insufficient resources | Increase quota |
| CrashLoopBackOff | Logs (--previous) | App error | Fix application |
| OOMKilled | Memory limits | Memory leak | Increase limits |
| Unhealthy | Readiness probe | Slow startup | Increase probe delay |
| No endpoints | Service selector | Label mismatch | Fix selector |

## Keywords for Search

kubernetes, pod failure, crashloopbackoff, oomkilled, pending pod, debugging, incident investigation, root cause analysis, pod logs, events, kubectl, container restart, image pull error, resource constraints, memory leak, application crash, service degradation, tls error, certificate expiry, readiness probe, liveness probe, troubleshooting, production incident, cluster debugging, namespace investigation, deployment failure, rollout stuck, error analysis, log correlation
