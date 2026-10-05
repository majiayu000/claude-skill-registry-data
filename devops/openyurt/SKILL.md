---




name: openyurt
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '''''Provides OpenYurt in Extending Kubernetes to edge computing scenarios
  with cloud-edgeu534F'' u540C'''''
domain: cncf
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  role: reference
  scope: infrastructure
  triggers: openyurt, extending, kubernetes, computing, container orchestration, k8s
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
role: reference
scope: infrastructure
triggers: computing, container orchestration, extending, k8s, openyurt, kubernetes
version: "1.0.0"




---




  related-skills: cncf-argo, cncf-artifact-hub, cncf-aws-eks, cncf-azure-aks



# OpenYurt in Cloud-Native Engineering

**Category:** Edge Computing  
**Status:** Active  
**Stars:** 1,600  
**Last Updated:** 2026-04-22  
**Primary Language:** Go  
**Documentation:** [Extending Kubernetes to edge computing scenarios with cloud-edge协同](https://openyurt.io/docs/)  

---

## Purpose and Use Cases

OpenYurt is a core component of the cloud-native ecosystem, serving as with cloud-edge协同

### What Problem Does It Solve?

OpenYurt addresses the challenge of running Kubernetes workloads in edge computing environments. It provides cloud-edge协同, offline node support, and reduced cloud dependency.

### When to Use This Project

Use OpenYurt when need to run Kubernetes at the edge, require offline operation, or have latency constraints. Not ideal for simple deployments or when edge AI workloads, IoT device management, or distributed cloud architectures.

### Key Use Cases

- Edge AI Inference
- IoT Device Management
- CDN and Edge Computing
- Offline Kubernetes Operation
- Hybrid Cloud-Edge Deployments

---

## Architecture Design Patterns

### Core Components

- **Yurttunnel**: Enables cloud-to-edge tunnel communication
- **Yurthub**: Edge-side cache and API server proxy
- **Edge Controller**: Manages edge nodes and workloads
- **OpenYurt Dashboard**: UI for managing edge clusters
- **Edge DNS**: Local DNS resolution at edge

### Component Interactions

1. **Edge Node → Yurthub**: Nodes communicate through edge hub
1. **Yurthub → Cloud API Server**: Yurthub proxies to cloud API server
1. **Yurttunnel → Cloud**: Tunnel establishes secure connection
1. **Edge Controller → Nodes**: Manages edge node lifecycle

### Data Flow Patterns

1. **Workload Deployment**: Yurt-ctl creates workloads → Deployed to edge nodes
1. **Health Monitoring**: Kubelet → Yurthub → Cloud for health status
1. **Config Sync**: ConfigMap/Secret sync between cloud and edge
1. **Tunnel Communication**: Cloud ↔ Edge secure tunnel establishment

### Design Principles

- **Edge Autonomy**: Edge can operate without cloud connectivity
- **Cloud-Edge Synergy**: Seamless integration between cloud and edge
- **Kubernetes Compatibility**: Full Kubernetes API compatibility
- **Security**: Secure communication between cloud and edge

---

## Integration Approaches

### Integration with Other CNCF Projects

- **Kubernetes**: Core platform with edge extensions
- **KubeEdge**: Alternative edge solution
- **Istio**: Service mesh for edge
- **Prometheus**: Monitoring for edge workloads

### API Patterns

- **Yurt-ctl CLI**: Edge-specific kubectl extension
- **YurtHub API**: Edge API server proxy
- **Tunnel Server API**: Tunnel management
- **CRDs**: Custom resources for edge features

### Configuration Patterns

- **Yurtctl Commands**: Edge cluster setup commands
- **YurtHub Configuration**: Edge hub settings
- **Tunnel Configuration**: Tunnel connection settings
- **Helm Chart**: OpenYurt deployment configuration

### Extension Mechanisms

- **Custom Yurthub Plugins**: Extend edge caching logic
- **Custom Tunnel Handlers**: Add tunnel protocol support
- **Edge Controllers**: Custom edge workload management

---

## Common Pitfalls and How to Avoid Them

### Misconfigurations

- **Network Partition**: Cloud-edge network disconnection
  - **How to Avoid**: Configure offline operation, implement local caching
- **Tunnel Latency**: High latency in tunnel connections
  - **How to Avoid**: Optimize network paths, use regional tunnels

### Performance Issues

- **Config Sync Delay**: Delayed config synchronization
  - **How to Avoid**: Adjust sync intervals, optimize config sizes
- **Controller Missing**: Cloud controllers not available at edge
  - **How to Avoid**: Use edge-native controllers, implement fallback logic

### Operational Challenges

- **DNS Resolution**: Local DNS failing
  - **How to Avoid**: Configure edge DNS, cache DNS entries
- **Upgrade Complexity**: Cloud and edge version mismatches
  - **How to Avoid**: Test upgrades together, use version matrix

### Security Pitfalls


---

## Coding Practices

### Idiomatic Configuration

- **Edge-Aware Workloads**: Design workloads for edge constraints
- **Config Management**: Minimize config dependencies
- **Health Checks**: Implement edge-appropriate health checks

### API Usage Patterns

- **Yurt-ctl join**: Join node to edge cluster
- **Yurt-ctl init**: Initialize edge cluster
- **kubectl commands**: Standard kubectl operations
- **Custom CRDs**: Edge-specific custom resources

### Observability Best Practices

- **Edge Metrics**: Collect edge-specific metrics
- **Offline Monitoring**: Monitor edge autonomy
- **Network Monitoring**: Track cloud-edge connectivity

### Testing Strategies

- **Network Partition Tests**: Test offline operation
- **Latency Tests**: Validate tunnel performance
- **Failover Tests**: Test cloud-edge failover

### Development Workflow

- **Local Development**: Use kind with Yurt extension
- **Debug Commands**: Check Yurthub and tunnel logs
- **Test Environment**: Set up edge cluster simulator
- **CI/CD Integration**: Automate edge testing
- **Monitoring Setup**: Configure edge observability
- **Documentation**: Maintain edge deployment guides

---

## Fundamentals

### Essential Concepts

- **Yurt-Hub**: Edge-side cache and proxy
- **Yurt-Tunnel**: Cloud-edge tunnel
- **Edge-Node**: Kubernetes node at edge
- **Cloud-Edge**: Cloud-edge communication pattern
- **Yurt-ctl**: Edge management CLI
- **Edge-DNS**: Local DNS resolver
- **Edge-Pool**: Group of edge nodes
- **Edge-Controller**: Edge workload manager

### Terminology Glossary

- **Yurt-Hub**: Edge hub for API proxy and caching
- **Yurt-Tunnel**: Secure tunnel for cloud-edge
- **Edge-Pool**: Group of edge nodes
- **Edge-Node**: Kubernetes node at edge location
- **Cloud-Edge**: Architecture pattern

### Data Models and Types

- **EdgePool**: Grouping of edge nodes
- **YurtHubConfig**: Edge hub configuration
- **YurtTunnelConfig**: Tunnel configuration

### Lifecycle Management

- **Node Join**: Node joins edge pool → Yurthub sync → Ready
- **Workload Deploy**: Cloud creates → Edge deploy → Status sync
- **Health Check**: Kubelet → Yurthub → Cloud status
- **Network Fail**: Connection lost → Local operation → Reconnect

### State Management

- **Yurthub State**: Cached Kubernetes state
- **Tunnel State**: Tunnel connection status
- **Edge Node State**: Node health and readiness
- **Edge Pool State**: Pool membership and status

---

## Scaling and Deployment Patterns

### Horizontal Scaling

- **Edge Pool Scaling**: Add edge nodes to pool
- **Yurthub Scaling**: Scale Yurthub instances
- **Tunnel Scaling**: Scale tunnel servers

### High Availability

- **Yurthub HA**: Multiple Yurthub instances
- **Tunnel HA**: Redundant tunnel connections
- **Edge Controller HA**: Edge controller replicas
- **Node Redundancy**: Multiple edge nodes per pool

### Production Deployments

- **Cluster Setup**: Initialize cloud and edge clusters
- **Network Configuration**: Configure secure cloud-edge network
- **Security Setup**: Enable TLS, certificates, RBAC
- **Monitoring Setup**: Configure edge-specific metrics
- **Logging Setup**: Centralize edge logs
- **Backup Strategy**: Backup configurations
- **Resource Quotas**: Limit edge node resources
- **Update Strategy**: Plan cloud-edge coordinated updates

### Upgrade Strategies

- **Chart Upgrade**: Upgrade OpenYurt components
- **Yurtctl Upgrade**: Upgrade edge cluster components
- **Node Upgrade**: Upgrade edge nodes one at a time
- **Testing**: Validate cloud-edge communication

### Resource Management

- **CPU Resources**: Set Yurthub and tunnel limits
- **Memory Resources**: Configure cache memory limits
- **Network Resources**: Configure tunnel bandwidth
- **Storage Resources**: Local storage for edge workloads

---

## Additional Resources

- **Official Documentation:** https://openyurt.io/docs/
- **GitHub Repository:** Check the project's official documentation for repository link
- **CNCF Project Page:** [cncf.io/projects/cncf-openyurt/](https://www.cncf.io/projects/cncf-openyurt/)
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
