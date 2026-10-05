---
name: envoy-proxy
description: Use when envoy proxy — L4/L7 filtering, load balancing, circuit breaking,
  observability, extensibility. Use when working with envoy proxy.
domain: devops
author: oyi77
license: Apache-2.0
subdomain: devops
tags:
- ci-cd
- devops
- envoy
- infrastructure
- proxy
version: 1.0.0
category: devops
---



## Overview

Envoy is a high-performance L4/L7 proxy designed for microservice architectures. Provides advanced load balancing, rate limiting, circuit breaking, and rich observability via stats, logging, and tracing.

## Capabilities

- HTTP/1.1, HTTP/2, gRPC, TCP proxying
- Advanced load balancing (round robin, ring hash, least request)
- Rate limiting and circuit breaking
- Extensible via Lua/Wasm filters
- Built-in stats, logging, and distributed tracing
- xDS API for dynamic configuration

## When to Use
**Trigger phrases:**
- "envoy proxy"
- "Envoy proxy — L4/L7 filtering, load balancing, circuit breaking, observability, "


- Service mesh data plane (Istio, Consul Connect)
- API gateway / edge proxy
- gRPC load balancing
- Canary routing and traffic shifting
- Need rich observability metrics

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code

The envoy-proxy workflow follows a standard pipeline pattern.

Core flow:
```
# envoy-proxy primary flow
input = prepare(raw_data)
result = process(input, config={balancing, breaking, circuit, envoy, extensibility})
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


### Static Configuration
```yaml
# envoy.yaml
static_resources:
  listeners:
    - name: listener_0
      address:
        socket_address: { address: 0.0.0.0, port_value: 8080 }
      filter_chains:
        - filters:
            - name: envoy.filters.network.http_connection_manager
              typed_config:
                "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
                stat_prefix: ingress_http
                route_config:
                  virtual_hosts:
                    - name: backend
                      domains: ["*"]
                      routes:
                        - match: { prefix: "/" }
                          route:
                            cluster: service_cluster
                            timeout: 30s
                            retry_policy:
                              retry_on: "5xx"
                              num_retries: 3
                http_filters:
                  - name: envoy.filters.http.router

  clusters:
    - name: service_cluster
      type: STRICT_DNS
      lb_policy: LEAST_REQUEST
      load_assignment:
        cluster_name: service_cluster
        endpoints:
          - lb_endpoints:
              - endpoint:
                  address:
                    socket_address: { address: service1, port_value: 8080 }
              - endpoint:
                  address:
                    socket_address: { address: service2, port_value: 8080 }
      circuit_breakers:
        thresholds:
          - max_connections: 100
            max_pending_requests: 50
            max_requests: 200
```

### Rate Limiting
```yaml
http_filters:
  - name: envoy.filters.http.local_ratelimit
    typed_config:
      "@type": type.googleapis.com/envoy.extensions.filters.http.local_ratelimit.v3.LocalRateLimit
      stat_prefix: rate_limit
      token_bucket:
        max_tokens: 100
        tokens_per_fill: 10
        fill_interval: 1s
```

### Health Checking
```yaml
clusters:
  - name: backend
    health_checks:
      - timeout: 5s
        interval: 10s
        unhealthy_threshold: 3
        healthy_threshold: 2
        http_health_check:
          path: "/healthz"
```

## Common Patterns

- **Circuit breaking**: prevent cascade failures
- **Retry policies**: automatic retry on 5xx/connect failures
- **Shadow traffic**: mirror requests for testing
- **Fault injection**: simulate errors for chaos testing
- **Wasm filters**: custom logic without recompiling Envoy

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