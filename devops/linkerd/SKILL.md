---




name: linkerd
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '"Linkerd in Service Mesh - cloud native architecture, patterns, pitfalls"
  and best practices'
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  related-skills: calico, cilium, contour, kuma
  role: reference
  scope: infrastructure
  triggers: cdn, infrastructure as code, k8s service, kubernetes service, linkerd,
    monitoring, native, service
  archetypes:
  - educational
  - strategic
  anti_triggers:
  - brainstorming
  - vague ideation
  - non-containerized architecture
  response_profile:
    verbosity: medium
    directive_strength: low
    abstraction_level: strategic
version: "1.0.0"




---




# Linkerd in Cloud-Native Engineering

## Purpose and Use Cases

### What Problem Does It Solve?
- **Zero-trust service communication**: Provides secure, observable, and reliable service-to-service communication without code changes
- **Operational simplicity**: Lightweight service mesh that focuses on observability, reliability, and security with minimal configuration
- **Performance overhead reduction**: Minimal latency addition (typically <1ms) compared to heavier mesh alternatives
- **Security without encryption complexity**: Automatic mTLS with certificate rotation, identity-based policies, and audit logging
- **Platform abstraction**: Works across Kubernetes, bare metal, VMs, and hybrid environments

### When to Use
- **Kubernetes-first deployments**: When Kubernetes is your primary platform and you need service mesh capabilities
- **Gradual adoption**: When you want to start small and incrementally adopt mesh features
- **Observability requirements**: When you need distributed tracing, metrics, and service maps out of the box
- **Security compliance**: When you need mTLS, identity-based access control, and audit trails
- **Resource-constrained environments**: When you need a lightweight mesh with minimal resource overhead

### Key Use Cases
- **Service-to-service mTLS**: Automatically encrypt all service communication
- **Traffic splitting**: Canary deployments, A/B testing with traffic policies
- **Observability dashboards**: Real-time service health, latency, and error rate metrics
- **Policy enforcement**: Access control between services based on identity
- **Resilience patterns**: Circuit breaking, retries, and timeouts for service reliability

## Architecture Design Patterns

### Core Components

#### Control Plane
```
control-plane
├── linkerd-controller (identity, web, tap, destination)
├── linkerd-proxy-injector (admission webhook)
└── linkerd-prometheus (metrics collection)
```
- **Controller**: Manages mesh configuration and state
- **Identity service**: Provides mTLS certificates with short-lived TTL
- **Web service**: UI and API server
- **Tap service**: Real-time traffic observation endpoint
- **Destination service**: Service discovery and load balancing
- **Proxy injector**: Admits pods with sidecar proxy injection

#### Data Plane (Proxy)
```
pod
├── application container
└── linkerd-proxy sidecar container
    ├── inbound listener
    ├── outbound listener
    └── metrics collection
```
- **-proxy**:Transparent proxy that intercepts all traffic
- **Inbound listener**: Handles incoming connections with mTLS
- **Outbound listener**: Routes outgoing traffic with load balancing
- **Metrics**: Collects latency, success rate, and throughput

### Component Interactions
```
Client Pod
    ↓ (proxy intercepts)
Linkerd Proxy (Outbound)
    ↓ (mTLS)
Service Mesh Network
    ↓ (destination service lookup)
Linkerd Proxy (Inbound)
    ↓ (proxy forwards)
Server Pod
```

### Data Flow Patterns

#### Request Flow
```
1. Application sends request to localhost
2. Proxy intercepts and encrypts with mTLS
3. Proxy uses destination service for routing
4. Request forwarded to destination proxy
5. Destination proxy validates certificate and forwards
6. Application receives decrypted response
```

#### Certificate Flow
```
1. Proxy requests certificate from identity service
2. Identity service validates pod identity
3. Certificate issued with short TTL (8 hours default)
4. Certificate rotated automatically before expiration
5. Certificate revocation supported for compromised pods
```

### Design Principles

#### Transparency
- **Zero code changes required**: Proxy intercepts all traffic automatically
- **No service awareness needed**: Works with any application protocol
- **Non-invasive**: Can be added/removed without application changes

#### Security First
- **Automatic mTLS**: All communication encrypted by default
- **Short-lived certificates**: Automatic rotation every 8 hours
- **Identity-based policies**: Access control based on service identity
- **Audit logging**: All policy decisions logged

#### Observability
- **Built-in metrics**: Latency, success rate, throughput
- **Service graphs**: Visualize service dependencies
- **Tap capability**: Real-time request inspection
- **Debugging tools**: CLI tools for troubleshooting

## Integration Approaches

### Integration with Other CNCF Projects

#### Prometheus Integration
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: linkerd-prometheus-config
data:
  prometheus.yaml: |
    scrape_configs:
      - job_name: 'linkerd-proxy'
        static_configs:
          - targets: ['localhost:4191']
```
- **Metrics scraping**: Proxy exposes `/metrics` endpoint
- **Dashboards**: Pre-built Grafana dashboards available
- **Alerting**: Alertmanager integration for SLO violations

#### Grafana Integration
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: linkerd-grafana-dashboards
data:
  linkerd-service-dashboard.json: |
    {
      "annotations": {},
      "panels": [
        // Linkerd service panels
      ]
    }
```
- **Service dashboard**: Real-time service health visualization
- **Mesh dashboard**: Complete mesh topology
- **Resource dashboard**: CPU, memory usage by proxy

#### OPA Integration
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-policy
spec:
  podSelector:
    matchLabels:
      app: payment-service
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              linkerd.io/control-plane-namespace: linkerd
              linkerd.io/proxy-deployment: payment-gateway
```
- **Policy enforcement**: Kubernetes NetworkPolicies + Linkerd policies
- **Custom policies**: OPA Gatekeeper for additional compliance

#### Jaeger Integration
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: linkerd-jaeger-config
data:
  jaeger.yaml: |
    endpoint: jaeger-collector:14268
    tags: |
      service.name=linkerd-proxy
```
- **Distributed tracing**: Linkerd integrates with existing tracing systems
- **Request IDs**: Propagates trace context
- **Latency tracking**: End-to-end latency measurement

### API Patterns

#### Service Profile API
```yaml
apiVersion: linkerd.io/v1alpha2
kind: ServiceProfile
metadata:
  name: payments-service.default.svc.cluster.local
spec:
  routes:
    - name: GET /payments
      condition:
        method: GET
        pathRegex: /payments
      responseTimeout: 1s
    - name: POST /payments
      condition:
        method: POST
        pathRegex: /payments
      retryBudget:
        retryRatio: 0.2
        minRetriesPerSecond: 10
        ttl: 30s
  decisionTimeout: 100ms
```
- **Route definitions**: HTTP route-based policies
- **Timeouts and retries**: Per-route configuration
- **Rate limiting**: Request rate control

#### Authorization Policy API
```yaml
apiVersion: policy.linkerd.io/v1beta1
kind: ServerPolicy
metadata:
  name: payments-service-policy
spec:
  selector:
    matchLabels:
      app: payments-service
  rules:
    - ports:
        - port: 8080
      authenticationModes:
        - PERMISSIVE
        - STRICT

---

---

## Constraints

### MUST DO
- Cite authoritative primary sources (official documentation, RFCs, standards bodies) — avoid secondary or blog references
- Include version-specific guidance when the reference topic has significant version-dependent behavior
- Structure reference content with clear navigation: overview first, then detailed subsections organized by use case
- Keep examples minimal and self-contained so readers can copy-paste without needing external context

### MUST NOT DO
- Do not present opinionated practices as facts — distinguish between standards, recommendations, and personal preferences
- Avoid outdated API references or deprecated patterns; explicitly note version requirements for each code example
- Never include incomplete or pseudocode examples in reference materials — all examples should be runnable
- Do not conflate different product versions when documenting features that vary across releases


## Live References

> Authoritative documentation links for this skill's domain. The model follows markdown links at load time to resolve external references and inline content.

- [Primary Documentation](https://linkerd.io/2.15/getting-started)
- [API Reference or Getting Started](https://linkerd.io/2.15/reference/cli/install)
- [Configuration Guide](https://linkerd.io/2.15/features/service-profiles)
- [Best Practices](https://linkerd.io/2.15/features/mutual-tls)
- [Common Patterns or Tutorials](https://linkerd.io/2.15/reference/proxy-config)

