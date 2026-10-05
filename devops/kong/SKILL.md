---




name: kong
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '"Kong in API Gateway - cloud native architecture, patterns, pitfalls"
  and best practices'
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  related-skills: calico, cilium, kong-ingress-controller, longhorn
  role: reference
  scope: infrastructure
  triggers: cdn, gateway, infrastructure as code, kong, monitoring, native, api gateway,
    api management
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




 # Kong in Cloud-Native Engineering

**Category:** api-gateway  
**Status:** Active  
**Stars:** 43,238  
**Last Updated:** 2026-04-22  
**Primary Language:** Lua  
**Documentation:** [https://github.com/Kong/kong](https://github.com/Kong/kong)  

---

## Purpose and Use Cases

Kong is a cloud-native project that provides api-gateway functionality for modern distributed systems.

### What Problem Does It Solve?

Kong addresses the challenges of api-gateway in cloud-native environments, enabling teams to implement api-gateway features without embedding them in application code.

### When to Use This Project

Use kong when you need api-gateway capabilities in your Kubernetes or cloud-native infrastructure. It's ideal when you require api-gateway with minimal application code changes.

### Key Use Cases


- api-gateway for microservices
- Integration with Kubernetes and CNCF ecosystem
- api-gateway with declarative configuration
- api-gateway for observability and monitoring
- api-gateway for security and compliance

---

## Architecture Design Patterns

### Core Components


- **Primary Component**: Core functionality
- **Controller**: Cluster management
- **Agent**: Node-level execution
- **API Server**: Management interface
- **Storage**: Configuration persistence

### Component Interactions


1. **Client → Core**: Request routing
2. **Core → Storage**: Configuration persistence
3. **Controller → Agents**: Command distribution
4. **Agents → Controller**: Status reporting
5. **Storage → Controllers**: Configuration sync

### Data Flow Patterns


1. **Request Flow**: Client → Core → Backend
2. **Configuration Flow**: API → Storage → Nodes
3. **State Flow**: Nodes → Control Plane → Dashboard
4. **Telemetry Flow**: Data → Collector → Storage

### Design Principles


- **Declarative Configuration**: YAML/CRD-based configuration
- **Kubernetes-Native**: Leverages Kubernetes APIs
- **Extensible**: Plugin/adapter architecture
- **Observability First**: Built-in metrics, tracing, logging
- **High Availability**: Multi-node clustering
- **Secure by Default**: TLS, authentication, authorization

---

## Integration Approaches

### Integration with Other CNCF Projects


- **Kubernetes**: Native integration with K8s APIs
- **Prometheus**: Metrics collection integration
- **Grafana**: Dashboard visualization
- **Jaeger/Zipkin**: Distributed tracing
- **CoreDNS**: Service discovery integration
- **Envoy**: Service mesh integration
- **Istio**: Service mesh control plane

### API Patterns


- **RESTful API**: Management endpoints
- **gRPC API**: Internal communication
- **WebSocket API**: Real-time updates
- **Admin API**: Configuration management

### Configuration Patterns


- **YAML Manifests**: Human-readable configs
- **JSON**: Machine-readable format
- **Environment Variables**: Runtime configuration
- **ConfigMaps**: Kubernetes config storage
- **CRDs**: Kubernetes custom resources

### Extension Mechanisms


- **Plugins**: Extend functionality
- **Filters**: Process requests
- **Hooks**: Event callbacks
- **Modules**: Add features

---

## Common Pitfalls and How to Avoid Them

### Misconfigurations


- **Endpoint Configuration**: Wrong API endpoints
- **Authentication**: Missing or incorrect auth
- **Resource Limits**: Insufficient resource allocation
- **SSL/TLS**: Certificate validation issues
- **Network Policy**: Incorrect network rules
- **Scaling**: Under/over-provisioned resources

### Performance Issues


- **Request Latency**: High latency
- **Throughput**: Low throughput
- **Memory Usage**: High memory consumption
- **CPU Usage**: High CPU usage
- **Connection Pooling**: Pool exhaustion
- **Cache Misses**: High cache miss rate

### Operational Challenges


- **Configuration Management**: Config drift
- **Upgrade Management**: Rolling upgrades
- **Monitoring**: Metrics collection
- **Logging**: Log aggregation
- **Troubleshooting**: Issue diagnosis
- **Security**: Security audits

### Security Pitfalls


- **Authentication**: Missing authentication
- **Authorization**: Overly permissive ACLs
- **TLS Configuration**: Weak TLS settings
- **Secrets Management**: Exposed secrets
- **RBAC**: Insufficient access control
- **Vulnerabilities**: Outdated dependencies

---

## Coding Practices

### Idiomatic Configuration


- **YAML**: Configuration files
- **JSON**: API payloads
- **Environment Variables**: Runtime config
- **ConfigMaps**: Kubernetes config

### API Usage Patterns


- **REST API**: Management endpoints
- **gRPC API**: Internal communication
- **WebSocket API**: Real-time updates

### Observability Best Practices


- **Prometheus Metrics**: Custom metrics
- **Tracing**: Distributed tracing
- **Access Logs**: Request logging
- **Alerting**: Health checks

### Testing Strategies


- **Unit Tests**: Component tests
- **Integration Tests**: Service tests
- **E2E Tests**: Full stack tests
- **Load Tests**: Performance tests

### Development Workflow


- **Development**: Local dev setup
- **Testing**: Unit and integration tests
- **Debugging**: Logging, tracing
- **Deployment**: Docker, Kubernetes
- **CI/CD**: GitHub Actions
- **Tools**: Project CLI tools

---

## Fundamentals

### Essential Concepts


- **Cluster**: Node group
- **Node**: Individual server
- **Pod**: Container unit
- **Service**: Network service
- **Config**: Configuration data
- **Secret**: Sensitive data
- **Volume**: Storage volume
- **Namespace**: Logical partition

### Terminology Glossary


- **Cluster**: Cluster of nodes
- **Node**: Individual node
- **Service**: Service endpoint
- **Config**: Configuration data
- **Secret**: Secret data
- **Volume**: Storage
- **Namespace**: Namespace
- **Pod**: Pod unit

### Data Models and Types


- **Config**: Config spec
- **Secret**: Secret spec
- **Service**: Service spec
- **Deployment**: Deployment spec
- **Pod**: Pod spec
- **Volume**: Volume spec
- **Namespace**: Namespace spec

### Lifecycle Management


- **Service Lifecycle**: Create → Deploy → Scale → Delete
- **Pod Lifecycle**: Pending → Running → Succeeded/Failed
- **Config Lifecycle**: Create → Apply → Update → Delete
- **Secret Lifecycle**: Create → Encrypt → Decrypt → Delete

### State Management


- **Config State**: Applied config
- **Service State**: Service state
- **Pod State**: Pod state
- **Volume State**: Volume state
- **Secret State**: Encrypted data
- **Namespace State**: Namespace data

---

## Scaling and Deployment Patterns

### Horizontal Scaling


- **Node Scaling**: Add/remove nodes
- **Container Scaling**: Pod replicas
- **Database Scaling**: Database clusters
- **Cache Scaling**: Cache clusters
- **Load Balancing**: Frontend balancing

### High Availability


- **Multiple Instances**: Redundant instances
- **Load Balancing**: Frontend balancing
- **Health Checking**: Automatic failover
- **Graceful Shutdowns**: Clean shutdown
- **Data Replication**: HA storage

### Production Deployments


- **Configuration**: Production config
- **Load Balancing**: Frontend HA
- **Monitoring**: Metrics setup
- **Alerting**: Alerting setup
- **Logging**: Centralized logging
- **Security**: Security hardening

### Upgrade Strategies


- **Rolling Update**: Rolling deployment
- **Blue-Green**: Blue-green deployment
- **Canary**: Canary release
- **Backup**: Pre-upgrade backup
- **Validation**: Post-upgrade validation

### Resource Management


- **Memory Configuration**: Memory limits
- **CPU Configuration**: CPU limits
- **Storage Configuration**: Storage limits
- **Network Configuration**: Network limits
- **Connection Limits**: Connection limits

---

## Additional Resources

- **Official Documentation:** [{repo_info['html_url']}]({repo_info['html_url']})
- **GitHub Repository:** [{repo_info['html_url']}]({repo_info['html_url']})
- **CNCF Project Page:** [cncf.io/projects/{project_info['name']}/](https://www.cncf.io/projects/{project_info['name']}/)
- **Community:** Check the GitHub repository for community channels
- **Versioning:** Refer to project's release notes for version-specific features

---

## Troubleshooting

### Common Issues

1. **Deployment Failures**
   - Check pod logs for errors
   - Verify configuration values
   - Ensure network connectivity

2. **Performance Issues**
   - Monitor resource usage
   - Adjust resource limits
   - Check for bottlenecks

3. **Configuration Errors**
   - Validate YAML syntax
   - Check required fields
   - Verify environment-specific settings

4. **Integration Problems**
   - Verify API compatibility
   - Check dependency versions
   - Review integration documentation

### Getting Help

- Check official documentation
- Search GitHub issues
- Join community channels
- Review logs and metrics
*Content generated automatically. Verify against official documentation before production use.*

## Examples

### Kong Ingress Controller with TLS Termination


```yaml
# Kong Ingress Controller configuration
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    kubernetes.io/ingress.class: kong
    konghq.com/strip-path: "true"
    konghq.com/preserve-host: "true"
spec:
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: myapp-service
            port:
              number: 80
      - path: /graphql
        pathType: Prefix
        backend:
          service:
            name: graphql-service
            port:
              number: 4000
  tls:
  - hosts:
    - api.example.com
    secretName: myapp-tls-secret
```

### Kong Plugin Configuration


```yaml
# Kong Consumer and Plugin configuration
apiVersion: v1
kind: Secret
metadata:
  name: myapp-api-key
type: Opaque
stringData:
  apikey: my-secret-api-key

---
apiVersion: configuration.konghq.com/v1
kind: KongConsumer
metadata:
  name: myapp-consumer
  annotations:
    konghq.com/credentials: myapp-api-key
username: myapp
credentials:
- myapp-api-key

---
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: rate-limiting
config:
  minute: 100
  policy: local
plugin: rate-limiting

---
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: request-transformer
config:
  headers:
  - add: X-Request-ID
    value: $pid
plugin: request-transformer
```

### Kong Service and Route Configuration


```yaml
# Kong Service and Route via CRD
apiVersion: configuration.konghq.com/v1
kind: KongService
metadata:
  name: myapp-service
  namespace: production
spec:
  url: http://myapp-service.production.svc:8080
  retries: 3
  connect_timeout: 60000
  write_timeout: 60000
  read_timeout: 60000

---
apiVersion: configuration.konghq.com/v1
kind: KongRoute
metadata:
  name: myapp-route
  namespace: production
spec:
  service:
    name: myapp-service
  paths:
  - /api
  - /api/*
  strip_path: true
  preserve_host: true
  protocols:
  - http
  - https
```

---

## When to Use

Use this skill when:

- **Integrating a CNCF project into Kubernetes infrastructure** — You need to configure, deploy, or troubleshoot a cloud-native tool within a cluster
- **Designing cloud-native architecture** — You are selecting and integrating CNCF tools to solve specific infrastructure challenges
- **Resolving operational issues** — A CNCF component is misbehaving, underperforming, or needs configuration changes
---

## Core Workflow

1. **Assess Requirements** — Understand the use case, scale, integration needs, and existing infrastructure. **Checkpoint:** Document requirements, constraints, and success criteria.

2. **Design Architecture** — Plan component interactions, data flow, and deployment strategy using cloud-native best practices. **Checkpoint:** Verify the architecture addresses all requirements and follows CNCF conventions.

3. **Implement & Configure** — Create manifests, configurations, and deployment scripts. Include resource limits, health checks, and observability hooks. **Checkpoint:** Validate all YAML against schema and test in a staging environment.

4. **Deploy & Monitor** — Apply manifests to the cluster, verify component health, and confirm observability is working. **Checkpoint:** Confirm all pods/services are running, probes passing, and metrics/alerts configured.

---

## Constraints

### MUST DO
- Include at least one complete working YAML manifest example
- Note when content is auto-generated vs. manually verified
- Reference relevant CNCF project documentation

### MUST NOT DO
- Deploy manifests without testing in a staging environment first
- Use deprecated API versions (e.g., apps/v1beta1)
- Omit resource limits and requests in Kubernetes manifests
