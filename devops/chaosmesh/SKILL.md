---




name: chaosmesh
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '''''Provides Chaos Mesh in Cloud-Native Engineering -u6DF7u6C8Cu5DE5u7A0B
  u5E73'' u53F0 for Kubernetes'''''
domain: cncf
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  role: reference
  scope: infrastructure
  triggers: chaosmesh, chaos, cloud-native, engineering
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
output-format: manifests
related-skills: null
role: reference
scope: infrastructure
triggers: chaos, chaosmesh, cloud-native, engineering
version: "1.0.0"




---




# Chaos Mesh in Cloud-Native Engineering

**Category:** chaos  
**Status:** Incubating  
**Stars:** 9,000  
**Last Updated:** 2026-04-22  
**Primary Language:** Go  
**Documentation:** [https://chaos-mesh.org/](https://chaos-mesh.org/)  

---

## Purpose and Use Cases

Chaos Mesh is a Chaos Engineering platform designed specifically for Kubernetes environments, enabling developers to simulate various failure scenarios to test system resilience.

### What Problem Does It Solve?

The difficulty of testing distributed system resilience in production-like environments. It provides a declarative way to inject faults and observe system behavior to identify weaknesses.

### When to Use This Project

Use Chaos Mesh when you want to test Kubernetes application resilience, simulate network failures, disk failures, pod failures, or need a comprehensive chaos engineering platform for Kubernetes.

### Key Use Cases


- **Pod Failure Injection**: Simulate pod crashes and failures
- **Network Chaos**: Inject network delays, losses, and partitions
- **Disk Chaos**: Simulate disk failures and I/O errors
- **Time Chaos**: Inject time shifts for testing
- **Kernel Chaos**: Inject kernel failures
- **HTTP Chaos**: Inject HTTP request errors
- **Experiment Scheduling**: Schedule chaos experiments
- **Workflow Orchestration**: Complex chaos workflows


---

## Architecture Design Patterns

### Core Components

- **Chaos Dashboard**: Web UI for experiment management
- **Controller Manager**: Main controller for chaos experiments
- **Scheduler**: Schedule chaos experiments
- **Chaos Daemon**: Node-level chaos injection agent
- **API Server**: REST API for chaos operations
- **Recorder**: Record experiment results

### Component Interactions

1. **User → Dashboard**: Create and manage experiments
2. **Dashboard → API Server**: REST API calls
3. **API Server → Controller**: Experiment creation
4. **Controller → Scheduler**: Schedule experiments
5. **Scheduler → Experiments**: Execute experiments
6. **Experiments → Chaos Daemon**: Inject chaos on nodes
7. **Chaos Daemon → Container Runtime**: Inject faults
8. **Recorder → Database**: Store experiment results

### Data Flow Patterns

1. **Experiment Creation**: Dashboard → API → Controller → Experiment → Scheduler → Execution
2. **Chaos Injection**: Scheduler → Pod/Node → Chaos Daemon → Container Runtime → Fault Injection
3. **Result Recording**: Experiment → Recorder → Database → Dashboard display
4. **Experiment Scheduling**: Schedule request → Time-based scheduling → Execution → Cleanup

### Design Principles

- **Kubernetes Native**: Uses CRDs and Kubernetes API
- **Declarative**: Chaos experiments as YAML manifests
- **Extensible**: Custom chaos experiments and actions
- **Safe**: Experiment rollback and safety controls
- **Observability**: Experiment results and metrics
- **Flexible**: Support for multiple chaos types

---

## Integration Approaches

### Integration with Other CNCF Projects

- **Kubernetes**: Core platform for chaos injection
- **Prometheus**: Chaos metrics collection
- **Grafana**: Chaos experiment visualization
- **OpenTelemetry**: Chaos tracing
- **Argo Workflows**: Chaos workflow integration
- **Tekton**: CI/CD chaos testing
- **Jaeger**: Distributed tracing for chaos
- **Helm**: Chaos Mesh deployment

### API Patterns

- **Kubernetes API**: CRD operations for experiments
- **REST API**: Dashboard API
- **Webhook API**: Experiment notifications
- **gRPC API**: Internal service communication

### Configuration Patterns

- **Experiment YAML**: Declarative chaos experiments
- **Schedule YAML**: Experiment scheduling configuration
- **Workflow YAML**: Chaos workflow definitions
- **Controller Configuration**: Controller settings

### Extension Mechanisms

- **Custom Chaos Types**: Implement custom chaos experiments
- **Webhooks**: Custom notification hooks
- **Metrics Collectors**: Custom metrics collection

---

## Common Pitfalls and How to Avoid Them

### Configuration Issues

- **Experiment YAML**: Incorrect chaos experiment definitions
- **Role-Based Access**: Missing RBAC permissions
- **Chaos Daemon**: Daemon not running on nodes
- **Scheduler Configuration**: Incorrect scheduling configuration
- **Network Policies**: Blocking chaos daemon communication

### Performance Issues

- **Experiment Overhead**: High resource usage during chaos
- **Controller Load**: High reconciliation overhead
- **Network Latency**: Chaos impact on network
- **Disk I/O**: Chaos impact on disk performance

### Operational Challenges

- **Experiment Rollback**: Manual rollback when needed
- **Experiment Safety**: Unintended chaos effects
- **Multi-Cluster**: Chaos across multiple clusters
- **Experiment Replay**: Re-run experiments
- **Result Analysis**: Analyze chaos results

### Security Pitfalls

- **RBAC**: Overly permissive chaos permissions
- **Network Isolation**: Chaos affecting production networks
- **Experiment Scope**: Too broad experiment scope
- **Access Control**: Unauthorized chaos execution

---

## Coding Practices

### Idiomatic Configuration

- **Experiment CRDs**: Declarative chaos experiments
- **Schedule CRDs**: Declarative scheduling
- **Workflow CRDs**: Chaos workflow definitions
- **Controller Config**: Controller configuration

### API Usage Patterns

- **kubectl apply**: Create and update experiments
- **Dashboard API**: Programmatic experiment management
- **Controller API**: Experiment control API
- **Recorder API**: Results access API

### Observability Best Practices

- **Metrics**: Experiment duration, success rate, failure rate
- **Logging**: Experiment execution logs
- **Tracing**: Chaos execution tracing
- **Dashboard**: Visual experiment monitoring
- **Alerting**: Experiment failure alerts

### Development Workflow

- **Local Testing**: minikube/kind for development
- **Debugging**: Experiment logs inspection
- **Testing**: Chaos experiment testing
- **CI/CD**: Automated chaos testing
- **Tools**: kubectl, chaos-dashboard, chaos-controller

---

## Fundamentals

### Essential Concepts

- **Experiment**: Chaos experiment definition
- **Schedule**: Scheduled experiment execution
- **Workflow**: Complex chaos workflow
- **Chaos Daemon**: Node-level chaos agent
- **Scheduler**: Experiment scheduling service
- **Recorder**: Results recording service

### Terminology Glossary

- **Experiment**: Chaos experiment definition
- **Schedule**: Scheduled execution
- **Workflow**: Complex chaos flow
- **Chaos Daemon**: Node agent
- **Scheduler**: Scheduling service
- **Recorder**: Results storage

### Data Models and Types

- **Experiment**: Chaos experiment configuration
- **Schedule**: Schedule configuration
- **Workflow**: Workflow definition
- **Recorder**: Results data
- **Status**: Experiment status

### Lifecycle Management

- **Experiment Lifecycle**: Create → Schedule → Execute → Complete → Cleanup
- **Schedule Lifecycle**: Schedule → Trigger → Execute → Complete
- **Workflow Lifecycle**: Create → Run → Complete → Record

### State Management

- **Experiment State**: Current experiment status
- **Schedule State**: Scheduled execution state
- **Workflow State**: Workflow execution state
- **Recorder State**: Results storage state

---

## Scaling and Deployment Patterns

### Horizontal Scaling

- **Controller Scaling**: Multiple controller replicas
- **Scheduler Scaling**: Multiple scheduler instances
- **Daemon Scaling**: Chaos daemon scaling
- **Dashboard Scaling**: Dashboard server scaling

### High Availability

- **Controller HA**: Multiple controller replicas
- **Scheduler HA**: Scheduler cluster
- **Daemon HA**: Daemon on all nodes
- **Dashboard HA**: Dashboard server HA
- **Storage HA**: etcd HA for state

### Production Deployments

- **Controller Deployment**: Production controller setup
- **Chaos Daemon**: Node-level deployment
- **Network Policies**: Allow chaos communication
- **RBAC**: Proper access control
- **Monitoring**: Experiment monitoring
- **Security**: Security scanning

### Upgrade Strategies

- **CRD Migration**: Handle CRD schema changes
- **Controller Rolling Update**: Zero-downtime updates
- **Daemon Rollout**: Daemon update strategy
- **Dashboard Update**: Dashboard upgrade

### Resource Management

- **CPU/Memory Limits**: Appropriate resource requests
- **Storage**: Experiment state storage
- **Network**: Daemon communication
- **Disk I/O**: Chaos impact management

---

## Additional Resources

- **Official Documentation:** [https://chaos-mesh.org/docs/](https://chaos-mesh.org/docs/)
- **GitHub Repository:** [github.com/chaos-mesh/chaos-mesh](https://github.com/chaos-mesh/chaos-mesh)
- **CNCF Project Page:** [cncf.io/projects/chaosmesh/](https://www.cncf.io/projects/chaosmesh/)
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
