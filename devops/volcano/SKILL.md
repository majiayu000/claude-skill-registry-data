---




name: volcano
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '"Configures volcano in batch scheduling infrastructure for kubernetes
  for cloud-native deployment and infrastructure management."'
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  role: reference
  scope: infrastructure
  triggers: batch, cloud infrastructure, infrastructure, scheduling, servers, volcano,
    ec2, virtual machines
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




# Volcano in Cloud-Native Engineering

**Category:** Scheduling & Orchestration  
**Status:** Active  
**Stars:** 2,800  
**Last Updated:** 2026-04-22  
**Primary Language:** Go  
**Documentation:** [Batch scheduling infrastructure for Kubernetes](https://volcano.sh/docs/)  

---

## Purpose and Use Cases

Volcano is a core component of the cloud-native ecosystem, serving as for Kubernetes

### What Problem Does It Solve?

Volcano addresses the challenge of batch job scheduling in Kubernetes. It provides advanced scheduling, gang scheduling, and queue management.

### When to Use This Project

Use Volcano when need batch scheduling, require gang scheduling, or manage ML workloads. Not ideal for simple deployments or when ML training jobs, batch processing, or complex scheduling requirements.

### Key Use Cases

- ML Training Job Scheduling
- Batch Job Management
- Gang Scheduling
- Queue-based Resource Management
- Multi-tenant Job Scheduling

---

## Architecture Design Patterns

### Core Components

- **Scheduler**: Core scheduling engine
- **Job Controller**: Job lifecycle management
- **Queue Controller**: Queue management
- **Scheduler Plugin**: Extensible scheduling plugins
- **Resource Manager**: Resource allocation

### Component Interactions

1. **Job → Scheduler**: Job requests scheduling
1. **Scheduler → Node**: Scheduler allocates nodes
1. **Queue → Scheduler**: Queue enforces resource limits
1. **Job → Pod**: Job creates pods

### Data Flow Patterns

1. **Job Submission**: Job created → Job controller → Scheduler
1. **Scheduling Decision**: Scheduler evaluates → Allocates nodes
1. **Pod Creation**: Job creates pods → Pods scheduled
1. **Queue Enforcement**: Queue enforces limits → Scheduler respects

### Design Principles

- **Batch Support**: Full batch job support
- **Gang Scheduling**: All-or-nothing scheduling
- **Extensible**: Plugin-based architecture
- **Fairness**: Fair resource sharing

---

## Integration Approaches

### Integration with Other CNCF Projects

- **Kubernetes**: Core platform
- **Kube-batch**: Scheduling backend
- **PyTorch**: ML workloads
- **TensorFlow**: ML workloads

### API Patterns

- **Job CRD**: Job definition
- **Queue CRD**: Queue definition
- **Scheduling Profile**: Scheduling profile
- **Scheduler Plugin**: Plugin interface

### Configuration Patterns

- **Volcano Config**: Volcano configuration
- **Queue Config**: Queue configuration
- **Job Config**: Job configuration
- **Scheduler Config**: Scheduler settings

### Extension Mechanisms

- **Custom Scheduler Plugins**: Add scheduling plugins
- **Custom Queues**: Custom queue logic
- **Custom Job Types**: Custom job definitions

---

## Common Pitfalls and How to Avoid Them

### Misconfigurations

- **Queue Resource**: Queue resource limits not enforced
  - **How to Avoid**: Configure queue resources, monitor usage
- **Priority Issues**: Priority inversion
  - **How to Avoid**: Configure priorities, check queue priorities

### Performance Issues

- **Job Status**: Job status not updating
  - **How to Avoid**: Check job controller, verify pod statuses
- **Queue Conflict**: Queue conflicts
  - **How to Avoid**: Configure queue priorities, avoid conflicts

### Operational Challenges

- **Plugin Issues**: Plugin loading issues
  - **How to Avoid**: Verify plugin configuration, check logs
- **Scaling Issues**: Scheduler scalability
  - **How to Avoid**: Scale scheduler, optimize configuration

### Security Pitfalls


---

## Coding Practices

### Idiomatic Configuration

- **Job Design**: Design jobs for batch scheduling
- **Queue Management**: Manage queues effectively
- **Priority Configuration**: Configure job priorities

### API Usage Patterns

- **volcano**: Volcano CLI
- **kubectl apply**: Apply job configurations
- **volcano schedctl**: Scheduler CLI
- **kubectl describe**: Describe job status

### Observability Best Practices

- **Job Metrics**: Track job performance
- **Scheduler Metrics**: Monitor scheduler health
- **Queue Metrics**: Track queue utilization

### Testing Strategies

- **Integration Tests**: Test job scheduling
- **Gang Tests**: Test gang scheduling
- **Performance Tests**: Validate scheduling performance

### Development Workflow

- **Local Development**: Use kind or minikube
- **Debug Commands**: Check volcano logs
- **Test Environment**: Set up test cluster
- **CI/CD Integration**: Automate testing
- **Monitoring Setup**: Configure observability
- **Documentation**: Maintain documentation

---

## Fundamentals

### Essential Concepts

- **Job**: Batch job definition
- **Queue**: Resource queue
- **Scheduler**: Scheduling engine
- **Gang**: Gang scheduling group
- **Priority**: Priority level
- **Queue**: Resource queue
- **Plugin**: Scheduling plugin
- **Profile**: Scheduling profile

### Terminology Glossary

- **Job**: Batch job
- **Queue**: Resource queue
- **Gang**: Gang group
- **Priority**: Priority level
- **Scheduler**: Scheduler engine

### Data Models and Types

- **Job**: Job definition
- **Queue**: Queue definition
- **SchedulingProfile**: Scheduling profile
- **Plugin**: Scheduler plugin

### Lifecycle Management

- **Job Submission**: Job created → Job controller → Scheduled → Running
- **Scheduling**: Job submitted → Scheduler evaluates → Nodes allocated
- **Gang Scheduling**: Gang all ready → Gang started
- **Queue Enforcement**: Job submitted → Queue checks → Job scheduled

### State Management

- **Job State**: Pending, running, or completed
- **Queue State**: Active or paused
- **Scheduler State**: Running or degraded
- **Pod State**: Scheduled, running, or pending

---

## Scaling and Deployment Patterns

### Horizontal Scaling

- **Scheduler Scaling**: Scale scheduler replicas
- **Job Scaling**: Scale jobs across queues
- **Node Scaling**: Add nodes to cluster

### High Availability

- **Scheduler HA**: Multiple scheduler replicas
- **Job HA**: Job replica management
- **Queue HA**: Queue redundancy

### Production Deployments

- **Cluster Setup**: Deploy volcano cluster
- **Queue Configuration**: Configure queues
- **Network Configuration**: Configure network
- **Security Setup**: Enable RBAC
- **Monitoring Setup**: Configure metrics
- **Logging Setup**: Centralize logs
- **Resource Quotas**: Set resource limits
- **Performance Tuning**: Optimize scheduling

### Upgrade Strategies

- **Volcano Upgrade**: Upgrade volcano components
- **Queue Migration**: Migrate queue configurations
- **Testing**: Verify functionality

### Resource Management

- **CPU Resources**: CPU limits
- **Memory Resources**: Memory limits
- **Storage Resources**: Storage configuration
- **Network Resources**: Network configuration

---

## Additional Resources

- **Official Documentation:** https://volcano.sh/docs/
- **GitHub Repository:** Check the project's official documentation for repository link
- **CNCF Project Page:** [cncf.io/projects/cncf-volcano/](https://www.cncf.io/projects/cncf-volcano/)
- **Community:** Check the official documentation for community channels
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
