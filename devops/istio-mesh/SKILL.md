---
name: istio-mesh
description: Use when istio service mesh — traffic management, security, observability
  for Kubernetes microservices. Use when working with istio mesh.
domain: devops
author: oyi77
license: Apache-2.0
subdomain: devops
tags:
- ci-cd
- devops
- infrastructure
- istio
- kubernetes
- mesh
version: 1.0.0
category: devops
---



## Overview

Istio provides a service mesh for Kubernetes with traffic management, mutual TLS, and observability. Uses Envoy sidecar proxies for data plane and istiod for control plane.

## Capabilities

- Traffic routing (canary, A/B, mirroring)
- Automatic mTLS between services
- Request-level telemetry (metrics, logs, traces)
- Circuit breaking and retry policies
- Authorization policies
- Multi-cluster federation

## When to Use
**Trigger phrases:**
- "istio mesh"
- "Istio service mesh — traffic management, security, observability for Kubernetes "


- Kubernetes microservice architectures
- Need zero-trust networking with mTLS
- Canary deployments with traffic splitting
- Distributed tracing and service graph
- Fine-grained access control between services

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code

The istio-mesh workflow follows a standard pipeline pattern.

Core flow:
```
# istio-mesh primary flow
input = prepare(raw_data)
result = process(input, config={istio, kubernetes, management, mesh, microservices})
validate(result)
deliver(result)
```

Error handling:
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Traffic Management
```yaml
# VirtualService - canary routing
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: web-vs
spec:
  hosts:
    - web
  http:
    - match:
        - headers:
            x-canary:
              exact: "true"
      route:
        - destination:
            host: web
            subset: canary
    - route:
        - destination:
            host: web
            subset: stable
          weight: 90
        - destination:
            host: web
            subset: canary
          weight: 10
---
# DestinationRule
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: web-dr
spec:
  host: web
  subsets:
    - name: stable
      labels:
        version: v1
    - name: canary
      labels:
        version: v2
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
    circuitBreaker:
      consecutive5xxErrors: 5
```

### mTLS Policy
```yaml
# PeerAuthentication - strict mTLS
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: STRICT
```

### Authorization
```yaml
# AuthorizationPolicy
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: api-policy
spec:
  selector:
    matchLabels:
      app: api
  rules:
    - from:
        - source:
            principals: ["cluster.local/ns/default/sa/web"]
      to:
        - operation:
            methods: ["GET"]
            paths: ["/api/*"]
```

### Telemetry
```yaml
apiVersion: telemetry.istio.io/v1alpha1
kind: Telemetry
metadata:
  name: mesh-telemetry
spec:
  tracing:
    - providers:
        - name: jaeger
      randomSamplingPercentage: 10
```

## Common Patterns

- **Sidecar injection**: `istio-injection=enabled` namespace label
- **Fault injection**: test resilience with delays/aborts
- **Mirroring**: copy traffic to canary for testing
- **Egress gateway**: control outbound traffic
- **Kiali dashboard**: visualize service graph

## How to Use

1. Define infrastructure as code (Terraform, CloudFormation, Pulumi)
2. Review changes through PR process before applying
3. Configure monitoring and alerting for critical paths
4. Set up secrets management (Vault, AWS Secrets Manager, etc.)
5. Document runbooks for deployment, rollback, and incident response
6. Test disaster recovery procedures regularly

## Red Flags

- **Infrastructure changes without review**: Unreviewed changes cause outages — use PRs for infra code
- **No rollback strategy**: Every deployment needs a tested rollback plan before it runs
- **Secrets in configuration files**: Secrets in YAML/JSON get committed to version control
- **Missing monitoring and alerting**: Without monitoring, outages go undetected until users report them
- **No documentation for runbooks**: Without runbooks, on-call engineers waste time re-discovering procedures

## Verification

- [ ] Skill output matches expected behavior

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Manual deployments are fine" | Manual deployments are error-prone and不可 repeatable. Automate. |
| "We do not need monitoring" | Without monitoring, you are flying blind. Add observability from day one. |
| "Infrastructure as code is overkill" | IaC enables reproducibility, version control, and disaster recovery. |