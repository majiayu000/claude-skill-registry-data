---




name: knative
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '"Provides Knative in Cloud-Native Engineering - serverless on Kubernetes"'
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  role: reference
  scope: infrastructure
  triggers: cloud-native, engineering, knative, serverless
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




  related-skills: cncf-argo, cncf-artifact-hub, cncf-aws-eks, cncf-azure-aks

# Knative in Cloud-Native Engineering

**Category:** serverless  
**Status:** Graduated  
**Stars:** 12,000  
**Last Updated:** 2026-04-22  
**Primary Language:** Go  
**Documentation:** [https://knative.dev/](https://knative.dev/)  

---

## Purpose and Use Cases

Knative is a serverless on Kubernetes designed to help engineers build, deploy, and manage cloud-native applications.

### What Problem Does It Solve?

Knative addresses complex serverless challenges by providing:
- Standardized APIs and interfaces
- Declarative configuration management
- Automatic resource management and reconciliation
- Built-in observability and monitoring
- Extensible architecture for custom integrations

### When to Use This Project

Use Knative when you need serverless on Kubernetes, require serverless-specific features, want to integrate with other CNCF projects, need production-ready serverless solutions, or require serverless-specific best practices.

### Key Use Cases

- **Knative Core**: Primary use case for serverless on Kubernetes
- **Integration with Kubernetes**: Native Kubernetes integration
- **Multi-Cluster Support**: Manage multiple clusters
- **Scalable Operations**: Handle large-scale deployments
- **Automated Management**: Self-healing and automatic recovery
- **Security Features**: Built-in security controls
- **Observability**: Comprehensive metrics and logging

---

## Architecture Design Patterns

### Core Components

- **Main Controller**: Primary reconciliation loop
- **API Server**: REST/gRPC API endpoint
- **Webhook**: Admission webhooks for validation
- **Scheduler**: Work scheduling and distribution
- **Storage Backend**: Persistent state storage
- **Agent**: Worker component for distributed tasks
- **Metrics Collector**: Metrics aggregation

### Component Interactions

1. **User → API Server**: Create/modify resources
2. **API Server → Controller**: Resource creation event
3. **Controller → Storage**: State persistence
4. **Storage → Controller**: State retrieval for reconciliation
5. **Controller → Worker**: Task delegation
6. **Worker → Status**: Status updates back to API

### Data Flow Patterns

1. **Reconciliation Flow**: Resource change → Controller detects → State comparison → Action taken → Status updated
2. **Event Flow**: Event received → Event handler → Reconciler → State updated
3. **Scaling Flow**: Metrics threshold → Controller evaluates → Scale decision → Resource scaled
4. **Failure Flow**: Component failure → Detector → Recovery action → State restored

### Design Principles

- **Kubernetes Native**: Built on Kubernetes APIs and conventions
- **Declarative**: Desired state management
- **Automated**: Self-healing and automatic recovery
- **Extensible**: Plugin architecture for extensions
- ** Observability**: Built-in metrics and logging
- **Secure**: Security-first design principles
- **Reliable**: High availability and disaster recovery

---

## Integration Approaches

### Integration with Other CNCF Projects

- **Kubernetes**: Core platform for Knative
- **Prometheus**: Metrics collection and alerting
- **OpenTelemetry**: Distributed tracing integration
- **Helm**: Chart deployment
- **cert-manager**: TLS certificate management
- **Istio/Linkerd**: Service mesh integration
- **Flux/ArgoCD**: GitOps integration

### API Patterns

- **Kubernetes API**: Standard Kubernetes CRDs
- **REST API**: HTTP/JSON REST API
- **gRPC API**: High-performance gRPC API
- **Webhook API**: Admission webhooks
- **Metrics API**: Prometheus-compatible metrics

### Configuration Patterns

- **YAML Configuration**: Declarative YAML manifests
- **Environment Variables**: Runtime configuration
- **ConfigMaps**: Externalized configuration
- **Secrets**: Sensitive data management
- **Helm Values**: Helm chart configuration

### Extension Mechanisms

- **CRDs**: Custom Resource Definitions
- **Webhooks**: Custom admission webhooks
- **Plugins**: Plugin architecture for extensions
- **Controllers**: Custom controllers
- **Adapters**: Adapter pattern for integrations

---

## Common Pitfalls and How to Avoid Them

### Configuration Issues

- **YAML Syntax Errors**: Incorrect YAML formatting
- **Missing Dependencies**: Missing required resources
- **Invalid Values**: Invalid configuration values
- **Resource Limits**: Insufficient resource limits

**How to Avoid:**
- Use kubectl dry-run for validation
- Implement CI/CD pipeline with yamllint
- Test configurations in staging environment
- Use configuration validation webhooks

### Performance Issues

- **Resource Exhaustion**: CPU or memory limits hit
- **Latency Spikes**: Slow responses under load
- **Scale Bottlenecks**: Scaling limitations
- **Storage Growth**: Unbounded storage growth

**How to Avoid:**
- Monitor resource usage with Prometheus
- Implement appropriate resource limits
- Use horizontalPodAutoscaler
- Configure storage quotas and cleanup policies

### Operational Challenges

- **Upgrade Complexity**: Complex upgrade procedures
- **Data Migration**: Migration between versions
- **Backup and Restore**: Backup procedures
- **Troubleshooting**: Debugging issues

**How to Avoid:**
- Follow official upgrade path documentation
- Test upgrades in staging first
- Implement regular backups
- Use diagnostic tools and logs

### Security Pitfalls

- **Privilege Escalation**: Overly permissive RBAC
- **Secrets Exposure**: Secrets in logs or configs
- **Network Exposure**: Exposed services
- **Authentication**: Weak authentication mechanisms

**How to Avoid:**
- Implement least-privilege RBAC
- Use secrets management
- Implement network policies
- Enable authentication and authorization

---

## Coding Practices

### Idiomatic Configuration

- **Resource Definitions**: Declarative YAML manifests
- **Configuration Management**: Externalized configuration
- **Secret Management**: Secure secrets handling
- **Version Control**: GitOps for configuration

### API Usage Patterns

- **kubectl**: Command-line administration
- **Kubernetes Client Libraries**: Programmatic access
- **REST API**: HTTP API for automation
- **CRUD Operations**: Standard create, read, update, delete

### Observability Best Practices

- **Metrics Collection**: Prometheus metrics
- **Logging**: Structured logging
- **Tracing**: Distributed tracing
- **Dashboards**: Grafana dashboards

### Development Workflow

- **Local Testing**: Kind or Minikube for development
- **Testing**: Integration tests
- **Debugging**: Debug logs and diagnostics
- **CI/CD**: Automated testing and deployment
- **Tools**: kubectl, Helm, kustomize

### Code Examples

```yaml
# Example configuration for Knative
apiVersion: cncf.knative/v1
kind: Knative
metadata:
  name: example
  namespace: default
spec:
  # Configuration details
  replicas: 3
  resources:
    requests:
      memory: "256Mi"
      cpu: "250m"
    limits:
      memory: "512Mi"
      cpu: "500m"
```

---
  related-skills: cncf-argo, cncf-artifact-hub, cncf-aws-eks, cncf-azure-aks

## Fundamentals

### Essential Concepts

- **Resource**: Core abstraction managed by Knative
- **Reconciliation**: Process of achieving desired state
- **Controller**: Component managing resources
- **Webhook**: Admission control mechanism
- **CRD**: Custom Resource Definition
- **Operator**: Pattern for managing complex applications
- **Status**: Current state of the resource

### Terminology Glossary

- **Controller**: Management component
- **Reconciler**: State reconciliation logic
- **CRD**: Custom Resource Definition
- **Webhook**: Admission webhook
- **Operator**: Application operator pattern
- **Reconciliation**: State synchronization

### Data Models and Types

- **Custom Resource**: User-defined resource type
- **Status**: Resource status information
- **Spec**: Desired state specification
- **Owner Reference**: Resource ownership chain

### Lifecycle Management

- **Resource Lifecycle**: Create → Configure → Deploy → Update → Delete
- **Controller Lifecycle**: Start → Watch → Reconcile → Stop
- **Upgrade Lifecycle**: Backup → Upgrade → Verify → Rollback (if needed)

### State Management

- **Desired State**: Spec field in resource
- **Current State**: Status field in resource
- **Reconciliation Loop**: Controller loop for state sync
- **Event Queue**: Change event processing

---

## Scaling and Deployment Patterns

### Horizontal Scaling

- **Controller Scaling**: Multiple controller replicas
- **Worker Scaling**: Scale worker pods based on load
- **API Server Scaling**: Scale API servers
- **Storage Scaling**: Add storage capacity

### High Availability

- **Controller HA**: Multiple controller replicas
- **Storage HA**: HA storage backend
- **Load Balancing**: Distribute traffic
- **Multi-Region**: Geographic distribution

### Production Deployments

- **Standalone**: Single instance deployment
- **HA**: High availability deployment
- **Clustered**: Multi-node cluster
- **Resource Configuration**: CPU, memory, storage limits

### Upgrade Strategies

- **Rolling Update**: Update without downtime
- **Blue-Green**: Blue-green deployments
- **Canary**: Canary releases
- **Version Compatibility**: Follow upgrade path

### Resource Management

- **CPU/Memory Requests**: Appropriate resource requests
- **Limits**: Resource limits for stability
- **Storage Quotas**: Storage allocation
- **Network Bandwidth**: Network resource allocation

### Deployment Patterns

- **DaemonSet**: One instance per node
- **Deployment**: Standard deployment
- **StatefulSet**: Stateful applications
- **Helm Chart**: Chart-based deployment
- **Operator Pattern**: Operator-based management

---

## Additional Resources

- **Official Documentation:** [https://knative.dev/](https://knative.dev/)
- **GitHub Repository:** [github.com/cncf/knative](https://github.com/cncf/knative)
- **CNCF Project Page:** [cncf.io/projects/knative/](https://www.cncf.io/projects/knative/)
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

### Basic Configuration


```yaml
# Basic configuration example
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{project_name}}-config
  namespace: default
data:
  # Configuration goes here
  config.yaml: |
    # Base configuration
    # Add your settings here
```

### Kubernetes Deployment


```yaml
# Kubernetes deployment for {{project_name}}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{project_name}}
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {{project_name}}
  template:
    metadata:
      labels:
        app: {{project_name}}
    spec:
      containers:
      - name: {{project_name}}
        image: {{project_name}}:latest
        ports:
        - containerPort: 8080
        resources:
          limits:
            memory: "128Mi"
            cpu: "500m"
```

### Kubernetes Service


```yaml
# Kubernetes service for {{project_name}}
apiVersion: v1
kind: Service
metadata:
  name: {{project_name}}
  namespace: default
spec:
  selector:
    app: {{project_name}}
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: ClusterIP
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
