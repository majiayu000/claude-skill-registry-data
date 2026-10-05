---




name: rook
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '"Configures rook in cloud-native storage orchestration for kubernetes
  for cloud-native deployment and infrastructure management."'
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  role: reference
  scope: infrastructure
  triggers: cloud-native, orchestration, rook, storage
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




  related-skills: cncf-argo, cncf-artifact-hub, cncf-aws-dynamodb, cncf-aws-ecr


# Rook in Cloud-Native Engineering

**Category:** Cloud Native Storage  
**Status:** Active  
**Stars:** 8,000  
**Last Updated:** 2026-04-22  
**Primary Language:** Go  
**Documentation:** [Cloud-Native Storage Orchestration for Kubernetes](https://rook.io/docs/)  

---

## Purpose and Use Cases

Rook is a core component of the cloud-native ecosystem, serving as for Kubernetes

### What Problem Does It Solve?

Rook addresses the challenge of storage orchestration for Kubernetes clusters. It provides automated storage management, support for multiple storage backends, and cloud-native storage.

### When to Use This Project

Use Rook when need storage orchestration, want automated storage management, or require storage integration with Kubernetes. Not ideal for simple deployments or when deploying distributed storage systems, need automated storage provisioning, or managing storage at scale.

### Key Use Cases

- Ceph Storage on Kubernetes
- NFS Storage Provisioning
- File Storage for Pods
- Block Storage for Databases
- Object Storage for Applications

---

## Architecture Design Patterns

### Core Components

- **Ceph Cluster**: Distributed storage cluster
- **Rook Operator**: Manages storage clusters
- **Rook Agent**: Runs on each node for storage operations
- **Ceph Monitors**: Cluster monitoring daemons
- **Ceph OSDs**: Object storage daemons

### Component Interactions

1. **Rook → Ceph Cluster**: Rook creates and manages Ceph cluster
1. **Kubernetes → Rook**: Kubernetes uses Rook for storage
1. **Pod → Ceph**: Pods access Ceph storage
1. **Node → Rook Agent**: Node-level storage operations

### Data Flow Patterns

1. **Cluster Creation**: Rook Operator → Ceph Cluster → Monitors → OSDs
1. **Volume Provisioning**: PVC created → Rook → Ceph → Volume created
1. **Data I/O**: Pod writes → Ceph → Replicated to OSDs
1. **Health Monitoring**: Ceph → Rook → Kubernetes events

### Design Principles

- **Native Integration**: Deep Kubernetes integration
- **Automated Management**: Full lifecycle management
- **Flexible Storage**: Support for multiple storage types
- **Production Ready**: Enterprise-grade storage

---

## Integration Approaches

### Integration with Other CNCF Projects

- **Kubernetes**: Core platform
- **Ceph**: Primary storage backend
- **NFS**: NFS provisioning
- **Local PV**: Local storage support

### API Patterns

- **CRDs**: CephCluster, CephFilesystem, etc.
- **Storage Classes**: Auto-provisioned storage classes
- **Volume Snapshots**: Storage snapshot support
- **PV/PVC**: Standard Kubernetes storage

### Configuration Patterns

- **CephCluster YAML**: Ceph cluster configuration
- **StorageClass YAML**: Storage class definitions
- **Rook Ceph YAML**: Rook operator configuration
- **Helm Chart**: Rook deployment

### Extension Mechanisms

- **Custom Storage Classes**: Customize storage behavior
- **Custom Monitoring**: Add custom metrics
- **Custom Backends**: Add new storage backends

---

## Common Pitfalls and How to Avoid Them

### Misconfigurations

- **Cluster Failure**: Ceph cluster failure
  - **How to Avoid**: Monitor Ceph health, set up alerts, plan for recovery
- **Performance Issues**: Storage performance degradation
  - **How to Avoid**: Monitor I/O patterns, tune settings, check disk health

### Performance Issues

- **Upgrade Issues**: Ceph version upgrade problems
  - **How to Avoid**: Test upgrades, follow upgrade path, backup before upgrade
- **Disk Failure**: Physical disk failure
  - **How to Avoid**: Monitor disk health, replace failed disks

### Operational Challenges

- **Memory Pressure**: Ceph consuming too much memory
  - **How to Avoid**: Configure memory limits, tune Ceph settings
- **OSD Issues**: OSD failures or degraded state
  - **How to Avoid**: Monitor OSD health, check disk space

### Security Pitfalls


---

## Coding Practices

### Idiomatic Configuration

- **Declarative Storage**: Define storage in YAML
- **Storage Class Management**: Manage storage classes through Rook
- **Monitoring Integration**: Integrate with Prometheus

### API Usage Patterns

- **kubectl apply**: Apply storage configurations
- **ceph status**: Check Ceph cluster status
- **Rook CLI**: Rook-specific commands
- **kubectl describe**: Describe storage resources

### Observability Best Practices

- **Ceph Metrics**: Expose Ceph cluster metrics
- **Rook Metrics**: Expose operator metrics
- **Storage Metrics**: Track storage utilization

### Testing Strategies

- **Integration Tests**: Test storage operations
- **Failover Tests**: Test cluster failover
- **Performance Tests**: Validate storage performance

### Development Workflow

- **Local Development**: Use minikube or kind
- **Debug Commands**: Check Rook and Ceph logs
- **Test Environment**: Set up test cluster
- **CI/CD Integration**: Automate storage testing
- **Monitoring Setup**: Configure storage observability
- **Documentation**: Maintain storage guides

---

## Fundamentals

### Essential Concepts

- **Ceph Cluster**: Distributed storage cluster
- **Rook Operator**: Storage orchestrator
- **Monitors**: Cluster monitors
- **OSDs**: Object storage daemons
- **MDS**: Metadata server
- **RGW**: Object storage gateway
- **NFS**: NFS server
- **Block Pool**: Block storage pool
- **File System**: Ceph file system
- **Object Store**: Rados gateway

### Terminology Glossary

- **Ceph**: Distributed storage system
- **Rook**: Storage orchestrator
- **OSD**: Object Storage Daemon
- **MON**: Monitor
- **MDS**: Metadata Server
- **RGW**: Rados Gateway
- **PVC**: PersistentVolumeClaim
- **SC**: StorageClass

### Data Models and Types

- **CephCluster**: Ceph cluster definition
- **CephFilesystem**: Ceph file system
- **CephBlockPool**: Block pool configuration
- **CephObjectStore**: Object store configuration

### Lifecycle Management

- **Cluster Creation**: Create CephCluster → Rook creates cluster → Cluster ready
- **Volume Provisioning**: Create PVC → Rook creates volume → Pod mounts volume
- **Upgrade Process**: Update Ceph version → Rolling update → New version ready
- **Failure Recovery**: Detect failure → Heal → Restore redundancy

### State Management

- **Cluster State**: Health, status, and readiness
- **Pool State**: Pool capacity and usage
- **OSD State**: OSD health and status
- **PVC State**: Binding and usage status

---

## Scaling and Deployment Patterns

### Horizontal Scaling

- **OSD Scaling**: Add OSDs to cluster
- **Monitor Scaling**: Scale monitor count
- **Pod Scaling**: Scale pods using storage
- **Cluster Scaling**: Add nodes to cluster

### High Availability

- **Cluster HA**: Multi-node Ceph cluster
- **Monitor HA**: Multiple monitor nodes
- **OSD HA**: Replicated data across OSDs
- **Node HA**: Distribute storage across nodes

### Production Deployments

- **Cluster Setup**: Deploy Ceph cluster via Rook
- **Network Configuration**: Configure storage network
- **Security Setup**: Enable encryption, RBAC
- **Monitoring Setup**: Configure Ceph metrics
- **Logging Setup**: Centralize Ceph logs
- **Backup Strategy**: Configure Ceph backups
- **Resource Quotas**: Set storage quotas
- **Performance Tuning**: Optimize Ceph settings

### Upgrade Strategies

- **Ceph Version**: Upgrade Ceph version
- **Rook Version**: Upgrade Rook operator
- **Node Upgrade**: Upgrade storage nodes
- **Testing**: Verify storage functionality

### Resource Management

- **CPU Resources**: Set Ceph CPU limits
- **Memory Resources**: Configure Ceph memory limits
- **Storage Resources**: Configure disk storage
- **Network Resources**: Configure storage network

---

## Additional Resources

- **Official Documentation:** https://rook.io/docs/
- **GitHub Repository:** Check the project's official documentation for repository link
- **CNCF Project Page:** [cncf.io/projects/cncf-rook/](https://www.cncf.io/projects/cncf-rook/)
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
