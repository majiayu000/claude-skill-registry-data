---




name: longhorn
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '"Longhorn in Cloud Native Storage - cloud native architecture, patterns"
  pitfalls, and best practices'
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  related-skills: calico, cilium, container-network-interface-cni, contour
  role: reference
  scope: infrastructure
  triggers: cdn, infrastructure as code, longhorn, monitoring, native, storage, cloudformation,
    cloudfront
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




# Longhorn in Cloud-Native Engineering

**Category:** storage  
**Status:** Graduated  
**Stars:** 4,800  
**Last Updated:** 2026-04-22  
**Primary Language:** Go  
**Documentation:** [https://longhorn.io/](https://longhorn.io/)  

---

## Purpose and Use Cases

### What Problem Does It Solve?

Longhorn addresses the critical gap in Kubernetes-native storage by providing a distributed block storage system that integrates seamlessly with Kubernetes. Traditional storage solutions were either cloud-specific, complex to deploy, or lacked Kubernetes-native features like automated failover, backups, and snapshots.

### When to Use This Project

Use Longhorn when you need:
- Kubernetes-native block storage with PVC support
- Automatic data replication across nodes
- Built-in backup and disaster recovery
- Storage class integration with dynamic provisioning
- High availability for stateful workloads
- Easy management through Kubernetes APIs

### Key Use Cases

- **Database Storage**: Run PostgreSQL, MySQL, MongoDB with persistent, replicated storage
- **Stateful Applications**: Deploy Redis, Elasticsearch, Kafka with reliable storage
- **CI/CD Pipelines**: Store build artifacts and caches with redundancy
- **AI/ML Workloads**: Provide high-throughput storage for training data
- **Backup and DR**: Automated snapshots and off-cluster backups
- **Multi-Cluster Storage**: Sync data across multiple Kubernetes clusters

---

## Architecture Design Patterns

### Core Components

- **Engine**: Handles block device operations and data replication
- **Replica**: Individual copy of volume data on a node
- **Controller**: Manages the engine and coordinates replication
- **Instance Manager**: Manages engine and replica processes
- **Driver**: Kubernetes CSI driver for volume provisioning
- **Scheduler**: Schedules volumes to nodes with available resources
- **Reconciler**: Ensures desired state matches actual state
- **Backup Controller**: Manages backup creation and restoration

### Component Interactions

1. **User → Kubernetes API**: Create PVC requesting Longhorn storage
2. **Provisioner → Controller**: Volume provisioning request
3. **Controller → Engine**: Engine management for block device
4. **Engine → Replicas**: Data write operations to all replicas
5. **Replica → Instance Manager**: Process lifecycle management
6. **Instance Manager → Node**: Schedule processes on appropriate nodes
7. **Reconciler → All Components**: Continuously sync desired state
8. **Backup Controller → Object Store**: Off-cluster backup storage

### Data Flow Patterns

1. **Volume Creation**: PVC request → Provisioner → Controller → Engine → Replicas → Storage
2. **Write Operation**: Application → Block device → Engine → Replicas (parallel writes)
3. **Read Operation**: Application → Block device → Engine → Replica (quorum read)
4. **Rebuild Process**: Failed replica detected → New replica created → Data synced from healthy replicas
5. **Backup Process**: Trigger backup → Create snapshot → Send to object store → Update backup metadata
6. **Restore Process**: Restore backup → Download from object store → Create replica → Sync to engine

### Design Principles

- **Kubernetes-Native**: Full CSI driver integration
- **Self-Healing**: Automatic recovery from node and disk failures
- **Data Redundancy**: Configurable replica count with automatic rebuild
- **Decoupled Architecture**: Engine and replica separation for flexibility
- **Conflict Detection**: Detect and prevent split-brain scenarios
- **Backup Integration**: Native integration with S3-compatible storage

---

## Integration Approaches

### Integration with Other CNCF Projects

- **Kubernetes**: Full CSI integration for PVC management
- **Prometheus**: Expose metrics for monitoring and alerting
- **Grafana**: Pre-built dashboards for storage metrics
- **Tekton**: Storage provisioned for CI/CD pipeline workloads
- **Helm**: Deploy Longhorn using Helm chart
- **Rancher**: Manage Longhorn through Rancher UI
- **Velero**: Backup and restore Longhorn volumes

### API Patterns

- **CSI RPCs**: CreateVolume, DeleteVolume, ControllerPublish/Unpublish, NodeStage/Unstage
- **Kubernetes API**: PVC, PV, StorageClass, Snapshot, RestoreCRD
- **Longhorn API**: Direct API for volume management and operations
- **Webhook**: Admission controller for validation and mutation

### Configuration Patterns

- **StorageClass**: Define Longhorn storage classes with parameters
- **Volume Settings**: Replica count, data locality, snapshot count
- **Backup Configuration**: S3 bucket, credential, and policy settings
- **Node Tags**: Assign nodes to specific storage pools
- **Disk Configuration**: Allocate disk space on nodes

### Extension Mechanisms

- **Custom Storage Classes**: Create storage classes for specific needs
- **Backup Policies**: Define custom backup schedules and retention
- **Volume Hooks**: Execute hooks before/after operations
- **Monitoring Integration**: Extend metrics with custom queries

---

## Common Pitfalls and How to Avoid Them

### Configuration Issues

- **Insufficient Disk Space**: Monitor free space and configure cleanup policies
- **Replica Scheduling**: Ensure enough nodes have available disk space
- **Network Partition**: Configure proper network and firewall rules between nodes
- **Backup Configuration**: Verify S3 credentials and bucket accessibility
- **Resource Limits**: Set appropriate resource requests for engines and replicas

### Performance Issues

- **Slow I/O**: Check disk utilization and network connectivity between nodes
- **Rebuild Delays**: Monitor rebuild progress and adjust priority
- **Snapshot Overhead**: Limit snapshot count and frequency
- **Engine Contention**: Avoid overprovisioning engines on single node
- **Network Bottleneck**: Use dedicated network for replica communication

### Operational Challenges

- **Node Failure**: Implement automated recovery and monitoring
- **Disk Failure**: Replace failed disks and trigger rebuilds
- **Data Corruption**: Use checksums and detect silent corruption
- **Backup Failures**: Monitor backup status and retry mechanisms
- **Upgrade Complexity**: Plan upgrades carefully with rollback strategies

### Security Pitfalls

- **Access Control**: Restrict access to Longhorn API and backend storage
- **Secret Management**: Use Kubernetes secrets for credentials
- **Encryption**: Enable encryption at rest for sensitive data
- **Network Security**: Isolate storage network from public access
- **Audit Logging**: Enable audit logs for compliance

---

## Coding Practices

### Idiomatic Configuration

- **StorageClass Parameters**: Use specific Longhorn parameters for fine-grained control
- **Volume Settings**: Configure settings at volume level for specific workloads
- **Node Management**: Tag nodes for storage pool organization
- **Backup Policies**: Define backup schedules and retention policies

### API Usage Patterns

- **PVC Creation**: Standard Kubernetes PVC with Longhorn StorageClass
- **Snapshot Management**: Create and manage snapshots through Kubernetes API
- **Backup Operations**: Trigger backups via Longhorn API or Kubernetes Snapshot
- **Restore Operations**: Restore from backup through Longhorn API
- **Volume Expansion**: Expand PVC and trigger volume expansion

### Observability Best Practices

- **Metrics Collection**: Prometheus scrape Longhorn metrics endpoint
- **Alerting**: Set up alerts for disk space, replica status, and rebuild status
- **Dashboard**: Use pre-built Grafana dashboards for storage monitoring
- **Log Analysis**: Monitor Longhorn component logs for issues
- **Health Checks**: Implement automated health checks for storage availability

### Development Workflow

- **Local Development**: Use Longhorn for local Kubernetes storage needs
- **Testing**: Test storage operations in staging environment
- **CI/CD Integration**: Provision storage for CI/CD workloads
- **Disaster Recovery**: Test backup and restore procedures regularly

---

## Fundamentals

### Essential Concepts

- **Volume**: Block device exposed to Kubernetes as PVC
- **Replica**: Individual copy of volume data on a node
- **Engine**: Process managing volume I/O and replica coordination
- **Snapshot**: Point-in-time copy of volume data
- **Backup**: Snapshot copied to external object storage
- **Data Locality**: Preference for replicas on same node as pod
- **Automated Failover**: Automatic volume failover on node failure
- **Rebuild**: Process of creating new replica after failure

### Terminology Glossary

- **Volume**: Kubernetes PVC backed by Longhorn block storage
- **Replica**: Individual copy of volume data stored on a node
- **Engine**: Manages volume I/O and replica coordination
- **Controller**: Kubernetes CSI controller for Longhorn volumes
- **Replica Manager**: Manages replica processes on a node
- **Snapshot**: Point-in-time copy of volume data
- **Backup**: Snapshot copied to external object storage
- **Data Locality**: Scheduling preference for pods and replicas
- **Auto-Disaster Recovery**: Automatic failover for volumes

### Data Models and Types

- **Volume**: Configuration, status, and metadata for block device
- **Replica**: Disk path, node, status, and sync status
- **Snapshot**: Creation time, size, children, and backup status
- **Backup**: Volume name, snapshot name, and S3 metadata
- **Node**: Disk configuration, tags, and scheduling status
- **Setting**: Global configuration for Longhorn behavior

### Lifecycle Management

- **Volume Lifecycle**: Create → Attach → Mount → Use → Unmount → Detach → Delete
- **Replica Lifecycle**: Create → Sync → Healthy → Failed → Rebuild
- **Snapshot Lifecycle**: Create → Use → Expire → Delete
- **Backup Lifecycle**: Trigger → Snapshot → Upload → Update → Cleanup

### State Management

- **Volume State**: Creating, attached, detaching, detached, faulted
- **Replica State**: Running, stopped, error, unknown
- **Engine State**: Running, stopped, error, unknown
- **Backup State**: Created, creating, error, completed

---

## Scaling and Deployment Patterns

### Horizontal Scaling

- **Storage Capacity**: Add nodes with dedicated disks for Longhorn
- **Replica Distribution**: Distribute replicas across failure domains
- **Volume Distribution**: Spread volumes across multiple nodes
- **Network Scaling**: Use dedicated network for replica communication

### High Availability

- **Multi-Node Deployment**: Deploy across multiple availability zones
- **Automatic Failover**: Fail volumes to replicas on other nodes
- **Disk Failure Recovery**: Automatic rebuild on disk replacement
- **Node Failure Recovery**: Automatic failover and rebuild

### Production Deployments

- **Production Cluster**: Deploy Longhorn with 3+ nodes for redundancy
- **Storage Class**: Define storage classes for different performance needs
- **Backup Destination**: Configure off-cluster backup to S3-compatible storage
- **Monitoring**: Set up Prometheus and Grafana for monitoring

### Upgrade Strategies

- **Minor Version**: In-place upgrade with zero-downtime
- **Major Version**: Follow upgrade guide with backup and testing
- **Rollback Plan**: Keep previous version images for rollback
- **Pre-Upgrade Check**: Run health checks before upgrade

### Resource Management

- **Disk Space**: Monitor and alert on free disk space
- **Memory**: Configure resource requests for engine and replica processes
- **CPU**: Balance CPU usage across nodes
- **Network**: Monitor network utilization between nodes

---

## Additional Resources

- **Official Documentation:** [https://longhorn.io/docs/](https://longhorn.io/docs/)
- **GitHub Repository:** [github.com/longhorn/longhorn](https://github.com/longhorn/longhorn)
- **CNCF Project Page:** [cncf.io/projects/longhorn/](https://www.cncf.io/projects/longhorn/)
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
