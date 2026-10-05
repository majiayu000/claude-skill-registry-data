---




name: fluid
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '"Fluid in A Kubernetes-native data acceleration layer for data-intensive"
  applications'
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  role: reference
  scope: infrastructure
  triggers: acceleration, container orchestration, fluid, kubernetes-native, layer,
    kubernetes, k8s
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




# Fluid in Cloud-Native Engineering

**Category:** Streaming & Data Processing  
**Status:** Active  
**Stars:** 4,800  
**Last Updated:** 2026-04-22  
**Primary Language:** Go  
**Documentation:** [A Kubernetes-native data acceleration layer for data-intensive applications](https://fluid.io/docs/)  

---

## Purpose and Use Cases

Fluid is a core component of the cloud-native ecosystem, serving as data-intensive applications

### What Problem Does It Solve?

Fluid addresses the challenge of data-intensive applications that require fast access to data stored in remote systems like object storage. It provides seamless integration with Kubernetes for data access acceleration, cache management, and data mobility.

### When to Use This Project

Use Fluid when running data-intensive workloads on Kubernetes that need to access data from remote storage systems. Not ideal for simple deployments or when low-latency data access, data locality optimization, and seamless data movement across storage backends.

### Key Use Cases

- Machine learning data preprocessing with fast dataset access
- Big data analytics with cached data on edge nodes
- Multi-cloud data mobility for analytics workloads
- Accelerating access to object storage from Kubernetes
- Cross-cluster data sharing for collaborative workloads

---

## Architecture Design Patterns

### Core Components

- **Dataset Controller**: Manages dataset lifecycle and exposes data as Kubernetes Volumes
- **Runtime Controllers**: Implement specific data orchestration logic (Spark, Alluxio, etc.)
- **Cache Layer**: Caches data on node-local storage for low-latency access
- **FUSE Mounter**: Provides POSIX-compatible file system interface
- **Scheduler**: Ensures data locality by placing workloads near data

### Component Interactions

1. **Dataset → Pod**: Dataset controller exposes data as Kubernetes Volume that pods can mount
1. **Runtime → Cache**: Runtime controller manages caching logic based on access patterns
1. **Scheduler → Dataset**: Scheduler considers data locality when placing pods

### Data Flow Patterns

1. **Data Access Request**: Pod reads data → FUSE → Runtime → Check cache → Fetch if needed → Return data
1. **Dataset Creation**: User creates Dataset → Controller creates PVC → FUSE mounts → Data accessible
1. **Cache Warm-up**: Workload starts → Data accessed → Cache populated → Subsequent access fast

### Design Principles

- **Transparent**: Applications access data through standard Kubernetes Volume interface
- **Extensible**: Supports multiple backends (OSS, HDFS, Ceph) through runtime pattern
- **Efficient**: Data locality optimization reduces network traffic
- **Kubernetes-Native**: Integrates seamlessly with Kubernetes ecosystem

---

## Integration Approaches

### Integration with Other CNCF Projects

- **Kubernetes**: Core platform for data orchestration and scheduling
- **Alluxio**: One of the supported runtimes for data orchestration
- **Spark**: Workload that can benefit from data caching
- **Helm**: Installation method for Fluid

### API Patterns

- **Dataset CRD**: Custom resource defining how data should be orchestrated
- **Runtime CRD**: Custom resource for specific data engine configuration
- **Kubernetes Volume**: Standard way to access orchestrated data

### Configuration Patterns

- **Dataset YAML**: Define data sources and access patterns
- **Runtime YAML**: Configure caching strategy and backend
- **Helm Values**: Chart configuration for deployment

### Extension Mechanisms

- **Custom Runtimes**: Implement custom data orchestration logic
- **FUSE Options**: Configure FUSE mount options
- **Cache Policies**: Define cache eviction and warming strategies

---

## Common Pitfalls and How to Avoid Them

### Misconfigurations

- **Data Locality Not Achieved**: Workloads not placed near cached data
  - **How to Avoid**: Configure scheduler extensions to consider data locality, use pod affinity rules
- **Network Bottleneck**: Network not optimized for data access
  - **How to Avoid**: Use high-speed network, implement data compression, optimize access patterns

### Performance Issues

- **Memory Pressure**: Cache consuming too much memory
  - **How to Avoid**: Set memory limits, implement cache tiering, monitor memory usage
- **Multi-Tenant Isolation**: Data access not properly isolated
  - **How to Avoid**: Use namespaces, implement RBAC for data access, encrypt data

### Operational Challenges

- **Version Upgrades**: Upgrading Fluid breaking existing configurations
  - **How to Avoid**: Test upgrades in staging, use versioned configurations, backup before upgrade
- **Multi-Cloud Data Mobility**: Data transfer costs and latency
  - **How to Avoid**: Use regional caches, implement data lifecycle policies, optimize transfer schedules

### Security Pitfalls

- **Secrets in Config**: Storing credentials in plaintext
  - **How to Avoid**: Use Kubernetes Secrets, integrate with vault, encrypt at rest

---

## Coding Practices

### Idiomatic Configuration

- **Declarative Data Definition**: Use YAML manifests to define data requirements
- **Policy-as-Code**: Define caching and eviction policies in code
- **Infrastructure-as-Code**: Manage Fluid deployments with CI/CD

### API Usage Patterns

- **kubectl apply**: Apply Dataset and Runtime configurations
- **kubectl describe**: Inspect dataset status and cache state
- **Custom Controllers**: Build operators for data workflow automation

### Observability Best Practices

- **Prometheus Metrics**: Expose cache hit ratio, latency, and throughput metrics
- **Logs Collection**: Collect and analyze FUSE and runtime logs
- **Tracing Integration**: Trace data access patterns through the stack

### Testing Strategies

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test end-to-end data flow in Kubernetes
- **Performance Tests**: Validate caching effectiveness and latency SLAs

### Development Workflow

- **Local Development**: Use kind or minikube for development
- **Debug Commands**: Use kubectl logs and exec for debugging
- **Test Environment**: Set up test cluster with sample data
- **CI/CD Integration**: Automate testing and deployment with GitHub Actions
- **Monitoring Setup**: Configure Prometheus and Grafana for visibility
- **Documentation**: Maintain comprehensive documentation and examples

---

## Fundamentals

### Essential Concepts

- **Dataset**: Abstraction representing data that needs orchestration
- **Runtime**: Implementation of data orchestration logic
- **Cache**: Local storage used to accelerate data access
- **FUSE**: Filesystem interface for accessing orchestrated data
- **Data Locality**: Placing workloads near cached data
- **Metadata Cache**: Cached file metadata for fast lookup
- **Data Prefetch**: Loading data into cache before requested
- **Eviction Policy**: Algorithm for removing data from cache
- **Backends**: External storage systems (OSS, HDFS, etc.)
- **Affinity**: Pod scheduling based on data location

### Terminology Glossary

- **Dataset Controller**: Kubernetes controller that manages Dataset resources
- **Runtime Controller**: Controller implementing specific data orchestration logic
- **FUSE Mounter**: Component that mounts data as filesystem
- **Cache Manager**: Component managing local cache storage
- **Scheduler Extension**: Component that considers data locality during scheduling

### Data Models and Types

- **DatasetSpec**: Desired state of a dataset
- **DatasetStatus**: Current state of a dataset
- **CachePolicy**: Configuration for cache behavior
- **RuntimeSpec**: Configuration for a specific runtime

### Lifecycle Management

- **Dataset Creation**: Create Dataset → Controller reconciles → PVC created → Mount ready
- **Cache Warm-up**: Data requested → Check cache → Fetch if needed → Populate cache
- **Data Access**: Application reads → FUSE intercepts → Cache check → Data returned
- **Cache Eviction**: Policy triggered → Data selected → Cache freed → Metadata updated
- **Dataset Deletion**: Delete Dataset → Controller cleans up → PVC deleted → Resources freed

### State Management

- **Dataset State**: Bound, Available, or Failed
- **Cache State**: Hot (cached) or Cold (not cached)
- **Runtime State**: Ready or Not Ready
- **Mount State**: Mounted or Unmounted

---

## Scaling and Deployment Patterns

### Horizontal Scaling

- **Horizontal Pod Autoscaling**: Scale workloads based on cache utilization
- **Cluster Scaling**: Add nodes to increase total cache capacity
- **Cache Layer Scaling**: Scale runtime controllers independently

### High Availability

- **Multi-Node Caching**: Replicate cache across multiple nodes
- **Controller HA**: Run controllers with replicas for high availability
- **Data Redundancy**: Configure backend data replication
- **Graceful Degradation**: Continue serving even if cache is lost

### Production Deployments

- **Cluster Setup**: Install Fluid using Helm with production values
- **Storage Configuration**: Configure appropriate local storage for cache
- **Network Optimization**: Enable high-speed networking for data access
- **Security Hardening**: Enable RBAC, network policies, and secrets management
- **Monitoring Setup**: Configure Prometheus metrics and Grafana dashboards
- **Backup Strategy**: Backup Dataset configurations and runtime state
- **Resource Quotas**: Set namespace-level resource limits
- **Update Strategy**: Plan rolling updates with minimal disruption

### Upgrade Strategies

- **Chart Upgrade**: Upgrade Fluid Helm chart with new version
- **Config Migration**: Update Dataset configurations to new API versions
- **Cache Clear**: Clear cache and warm it up with new version
- **Backward Compatibility**: Test with existing workloads before full rollout

### Resource Management

- **CPU Configuration**: Set appropriate CPU requests and limits for runtimes
- **Memory Configuration**: Configure memory limits based on cache requirements
- **Disk Quotas**: Set storage class with appropriate quotas
- **Network Bandwidth**: Configure network policies for data traffic

---

## Additional Resources

- **Official Documentation:** https://fluid.io/docs/
- **GitHub Repository:** Check the project's official documentation for repository link
- **CNCF Project Page:** [cncf.io/projects/cncf-fluid/](https://www.cncf.io/projects/cncf-fluid/)
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
