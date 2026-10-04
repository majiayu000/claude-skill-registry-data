---
name: azure-compute
description: >
  Select and implement the right Azure compute platform for a workload.
  Decision tree guides choice based on workload characteristics, scaling needs, and operational maturity.
  Covers serverless, PaaS, containers, Kubernetes, and IaaS patterns.
compatibility:
  models: [any-llm]
  cloud: azure
  frameworks: [well-architected]
  platforms: [functions, app-service, container-apps, aks, vm]
---

# Azure Compute

Choose the compute option with the lowest operational burden that meets your workload's functional and non-functional requirements.
Managed services first; IaaS only when control is mandatory.

## Use This Skill When

- The user asks which Azure compute service to use (Functions vs. App Service vs. AKS)
- A workload must move from on-premises or another cloud to Azure
- The user needs trade-off analysis: cost, scaling, latency, compliance
- The user needs operational readiness assessment

## Context: Compute Maturity Spectrum

```
Serverless (Least ops):
  Azure Functions
  └─ Pro: Zero infrastructure, auto-scale, pay-per-exec
  └─ Con: Cold starts, max 10-min timeout, limited languages

PaaS (Low ops):
  App Service
  └─ Pro: Built-in scaling, diagnostics, deployment slots
  └─ Con: Single-region, limited customization
  
  Container Apps
  └─ Pro: Container-native, auto-scaling, event-driven
  └─ Con: Smaller ecosystem, newer service

Containers + Orchestration:
  Azure Kubernetes Service (AKS)
  └─ Pro: Full Kubernetes control, multi-region, custom scaling
  └─ Con: Requires Kubernetes expertise, higher operational burden

IaaS (Most control, Most ops):
  Virtual Machines / VMSS
  └─ Pro: OS-level control, custom binaries, legacy support
  └─ Con: Requires manual patching, scaling, monitoring
```

## Required Inputs

- **Workload type**: Web API, background job, ML training, legacy app, real-time analytics
- **Traffic pattern**: Constant, bursty, seasonal, event-driven
- **Latency requirement**: Sub-100ms, <500ms, or flexible
- **Availability**: 99%, 99.9%, 99.95%?
- **Scaling needs**: Min/max instances, target response time
- **Compliance**: On-premises only, specific regions, data residency
- **Team skills**: DevOps, Kubernetes expertise, vendor lock-in tolerance
- **Budget**: TCO vs. OpEx preference

## Decision Tree

```
Is this a background job triggered by an event (file upload, message queue, timer)?
├─ Yes → Azure Functions (lowest cost, auto-scale, easy)
│         But if: Job runs >10 min → Container Apps or App Service
└─ No → Continue

Is this a stateless HTTP API or web app?
├─ Yes → App Service (built-in scaling, diagnostics)
│         Or: Container Apps (if containerized, multi-region)
├─ Needs Kubernetes → AKS
└─ No → Continue

Does this need OS-level control (custom packages, specific kernel version)?
├─ Yes → Virtual Machines or VMSS
└─ No → One of above managed options

Is latency critical (< 100ms p99)?
├─ Yes → Consider colocating compute with data store (same region/AZ)
│         Evaluate: App Service Plan, VMSS, or Container Apps with CPU optimization
└─ No → Standard deployment acceptable

Do you need to orchestrate multiple microservices?
├─ Yes → AKS (service mesh, traffic mgmt, multi-region)
│         Or: App Service + API Management (simpler, less overhead)
└─ No → Single-service option (Functions, App Service)
```

## Workflow

### Phase 1: Characterize Workload

1. **Inventory current state**:
   - Runtime: Node.js, Python, .NET, Java, Go, etc.
   - Concurrency: Single-threaded, multi-threaded, async?
   - State: Stateless, session affinity, distributed cache?
   - Dependencies: Database, message queue, cache, external APIs?
   - Constraints: Max execution time, memory, disk I/O?

2. **Predict load profile**:
   - Baseline (off-peak): 10 req/sec
   - Average (peak): 100 req/sec
   - Spike (flash sale, viral event): 500 req/sec
   - Duration of spikes: Seconds or hours?

3. **Define SLA**:
   - Availability: 99% (5.2 hours downtime/month) vs. 99.95% (21 minutes/month)
   - Response time p99: Must be <500ms? <100ms?
   - Cost sensitivity: $500/month budget or flexible?

### Phase 2: Evaluate Candidates

**Candidate 1: Azure Functions**
```
✓ Event-driven, API-triggered, timer-based workloads
✓ Zero infrastructure, auto-scale to thousands
✓ Pay only for execution time
✗ Cold starts (first invocation 1-5 sec)
✗ Max 10-minute execution timeout
✗ Limited to 1.5 GB memory per invocation
✗ Not suitable for stateful or long-running tasks

Cost estimate: 1M invocations/month × $0.20/1M = $0.20 + compute duration charges
```

**Candidate 2: App Service**
```
✓ Web APIs, web apps, long-running services
✓ Instant startup (no cold start)
✓ Built-in auto-scale, deployment slots
✓ Integrated diagnostics, backups
✗ Single region (unless you manage multi-region)
✗ Always-on instances (minimum cost even at 0 traffic)

Cost estimate: P1V2 plan (1 core, 1.75 GB) = $74/month × 2 instances = $148/month
```

**Candidate 3: Container Apps**
```
✓ Containerized microservices, event-scale
✓ Auto-scale to zero (similar to Functions)
✓ Multi-region deployment
✗ Newer service, smaller ecosystem
✗ Kubernetes learning curve

Cost estimate: 0.5 vCPU, 1 GB memory, auto-scale = ~$30-50/month
```

**Candidate 4: AKS**
```
✓ Complex microservices orchestration
✓ Service mesh, traffic mgmt, canary deployments
✓ Multi-region, high availability
✓ Kubernetes portability
✗ Requires Kubernetes expertise
✗ Significant operational overhead
✗ Higher minimum cost (node pool)

Cost estimate: 3-node cluster (B2S VMs) = $30/month × 3 + storage + egress = $100-200/month+
```

**Candidate 5: Virtual Machines**
```
✓ Legacy app, custom OS packages, GPL software
✓ OS-level control
✗ Manual scaling, patching, monitoring
✗ Highest operational burden
✗ Highest minimum cost

Cost estimate: D2s_v3 VM = $97/month × 2 (HA) = $194/month minimum
```

### Phase 3: Size and Scale

1. **Baseline sizing** (off-peak):
   - Functions: $5-10/month (very low)
   - App Service: 1 instance × plan cost (~$50/month)
   - Container Apps: 0.25 vCPU (~$10/month)
   - AKS: 2-3 node minimum (~$100-150/month)
   - VMs: 2 instances (HA) (~$200/month)

2. **Scaling policy**:
   - **Functions**: Auto, no configuration needed
   - **App Service**: Auto-scale rule: 50-80 CPU%, scale out when >80%, scale in when <30%
   - **Container Apps**: CPU 70%, memory 80%
   - **AKS**: Kubernetes HPA: target CPU 70%
   - **VMs/VMSS**: Scale set: CPU 70%, add 2 instances at a time

3. **Cost impact of scaling**:
   - Functions: $0.20 per 1M invocations + duration
   - App Service: +$74/month per standard instance
   - Container Apps: +$30-50/month per scaled instance
   - AKS: +$30/month per node

## Output Contract

1. **Recommended Compute Option**
   - Why this option is best for your workload
   - Confidence level (80%, 95%, etc.)

2. **Justification & Trade-Offs**
   - Operational burden vs. cost vs. flexibility
   - Why alternatives were rejected

3. **Sizing & Scaling**
   - Baseline instance count, VM size
   - Auto-scale rules (CPU/memory thresholds)
   - Peak capacity and estimated cost

4. **Cold Start & Latency Impact**
   - If Functions: ~1-5 sec cold start time, 100 ms warm
   - Mitigation: Keep-alive, premium plan, container warm-up

5. **Operational Checklist**
   - Monitoring (Application Insights)
   - Logging (Log Analytics)
   - Backup/DR strategy
   - CI/CD pipeline type

6. **Migration Readiness**
   - Dependency adjustments (connection strings, auth)
   - Testing strategy (smoke, integration, load)
   - Rollback plan (old platform stays active until validated)

## Practical Examples

### Example 1: Bursty Event-Driven Workload
**Workload**: Image resize triggered on file upload to blob storage
- Traffic: 10 images/day (steady), 1000 images/day on marketing campaign (spiky)
- Latency: <30 sec acceptable (async)
- **Recommendation**: Azure Functions (Premium Plan for concurrency control)
- **Cost**: ~$40/month steady + $0.20 per 1M invocations

### Example 2: Steady HTTP API
**Workload**: REST API for mobile app
- Traffic: 100 req/sec average, 500 req/sec peak
- Latency: <100ms p99 (critical)
- Availability: 99.95%
- **Recommendation**: App Service P1V2 (2+ instances) + CDN for static assets
- **Cost**: $148/month (2 instances) + egress

### Example 3: Microservices Architecture
**Workload**: 5 services: API gateway, auth, billing, inventory, notifications
- Need service-to-service communication, canary deployments
- Team: Kubernetes-experienced DevOps team
- **Recommendation**: AKS with Helm charts, Istio service mesh
- **Cost**: $100-150/month (3-node cluster) + storage, egress

## Guardrails

- **Avoid over-engineering**: Use Functions for simple tasks; don't add AKS until you need it.
- **Be honest about operational burden**: AKS requires dedicated DevOps; App Service works with dev teams.
- **Consider lock-in**: App Service is Azure-only; AKS is portable (but requires Kubernetes skills).
- **Latency matters**: Functions cold starts may violate SLA; test realistic load.
- **Monitor from day one**: Set up alerts before go-live (CPU, memory, errors, latency).
- **Plan for growth**: Today's App Service might become tomorrow's AKS; design for portability.
