---




name: cni
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '"Cni in Cloud-Native Engineering - Container Network Interface - networking"
  for Linux containers'
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  role: reference
  scope: infrastructure
  triggers: cloud-native, cni, container, engineering
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




  related-skills: cncf-aws-route53, cncf-azure-cdn, cncf-azure-traffic-manager, cncf-azure-virtual-networks


# Cni in Cloud-Native Engineering

**Category:** containers  
**Status:** Active  
**Stars:** 6,032  
**Last Updated:** 2026-04-21  
**Primary Language:** Go  
**Documentation:** [https://github.com/containernetworking/cni/blob/master/SPEC.md](https://github.com/containernetworking/cni/blob/master/SPEC.md)  

---

## Purpose and Use Cases

Cni is a core component of the cloud-native ecosystem, serving as a Container Network Interface specification and plugins that provide networking for containers in Kubernetes.

### What Problem Does It Solve?

The lack of a standardized interface for container networking in Kubernetes, requiring each CNI plugin to implement the same interface differently.

### When to Use This Project

Use CNI when you need to configure networking for containers in Kubernetes, or when building your own container networking solution that integrates with Kubernetes.

### Key Use Cases


- Kubernetes pod networking
- Container network configuration
- Network policy enforcement
- CNI plugin development
- Custom networking solutions for containers


---

## Architecture Design Patterns

### Core Components


- **Plugin**: Network implementation (bridge, host-local, flannel, etc.)
- **ConfFile**: Configuration file specifying plugin and network
- **Network Namespace**: Isolated network context for containers
- **IPAM**: IP Address Management plugin
- **Result**: Network configuration result returned to caller


### Component Interactions


1. **Container Runtime → CNI Plugin**: Network setup request
2. **ConfFile → Plugin**: Provides network configuration
3. **IPAM Plugin**: Allocates IP address
4. **Plugin → Network Namespace**: Configures network
5. **Result → Runtime**: Returns network configuration


### Data Flow Patterns


1. **Network Setup**: Add network → Plugin config → IPAM → Namespace setup → Result returned
2. **IP Allocation**: Pool check → IP assignment → Lease created → Result returned
3. **Network Cleanup**: Delete network → Plugin cleanup → IP release → Namespace cleanup


### Design Principles


- **Simple Interface**: Minimal API for network setup
- **Declarative**: Configuration-based
- **Pluggable**: Multiple implementations
- **Standardized**: Consistent behavior across implementations
- **Namespace-Scoped**: Per-container configuration


---

## Integration Approaches

### Integration with Other CNCF Projects


- **Kubernetes**: Pod networking standard
- **Containerd**: Container runtime integration
- **Flannel, Calico, Cilium**: Popular CNI implementations


### API Patterns


- **Config File**: JSON-based network configuration
- **Executable Protocol**:stdin/stdout communication
- **Result Schema**: Network configuration output


### Configuration Patterns


- **Conf File**: Network configuration
- **Conf List**: Multiple network configuration
- **IPAM Section**: IP address management config


### Extension Mechanisms


- **Plugins**: Network implementations
- **IPAM Plugins**: IP address management
- **Version Support**: Multiple spec versions


---

## Common Pitfalls and How to Avoid Them

### Misconfigurations


- **Plugin Order**: Incorrect plugin sequence
- **Network Name**: Duplicate network names
- **IPAM Pool**: Insufficient IP addresses
- **Conflicting Networks**: Overlapping subnets


### Performance Issues


- **Network Setup Time**: Slow plugin execution
- **IP Allocation**: Slow IPAM performance
- **Plugin Chaining**: Multiple plugins overhead


### Operational Challenges


- **Plugin Compatibility**: Multiple plugin versions
- **Network Upgrades**: Zero-downtime network changes
- **Debugging**: Network connectivity issues
- **IPAM Management**: IP pool exhaustion


### Security Pitfalls


- **Network Policies**: Missing policies in plugins
- **IP Allocation**: Address space exhaustion
- **Plugin Vulnerabilities**: Outdated plugins


---

## Coding Practices

### Idiomatic Configuration


- **Conf File**: Single file per network
- **Conf List**: Multiple networks
- **Plugin Configuration**: Nested in plugin blocks


### API Usage Patterns


- **CNI Plugin Protocol**: stdin/stdout
- **Config File**: JSON configuration
- **Exec-in-Container**: Network setup


### Observability Best Practices


- **Plugin Metrics**: Performance metrics
- **IPAM Statistics**: IP allocation stats
- **Error Logging**: Network errors


### Testing Strategies


- **Unit Tests**: Plugin tests
- **Integration Tests**: Network behavior
- **E2E Tests**: Full network setup
- **Compatibility Tests**: Spec compliance


### Development Workflow


- **Development**: CNI plugin development
- **Testing**: Plugin tests
- **Debugging**: Plugin logs, network inspection
- **Deployment**: DaemonSet, static pods
- **CI/CD**: Plugin-specific CI
- **Tools**: cilium-cli, calicoctl


---

## Fundamentals

### Essential Concepts


- **Plugin**: Network implementation
- **Conf File**: Configuration file
- **Conf List**: Multiple network config
- **Network Namespace**: Container network context
- **IPAM**: IP address management
- **Result**: Network configuration output
- **Version**: Spec version
- **Type**: Plugin type
- **Name**: Network name
- **Routes**: Network routes


### Terminology Glossary


- **Plugin**: Network implementation
- **Conf File**: Config file
- **Conf List**: Multi-network config
- **Namespace**: Network context
- **IPAM**: IP management
- **Result**: Config output
- **Version**: Spec version
- **Type**: Plugin type
- **Name**: Network name
- **Routes**: Network routes


### Data Models and Types


- **Conf File**: Network configuration
- **Conf List**: Multiple network config
- **IPAM Config**: IPAM configuration
- **Result**: Network result
- **Route**: Route definition
- **DNS**: DNS configuration


### Lifecycle Management


- **Network Lifecycle**: Add → Setup → Delete → Cleanup
- **IPAM Lifecycle**: Allocate → Config → Release
- **Namespace Lifecycle**: Enter → Configure → Exit


### State Management


- **IPAM State**: IP allocations
- **Network State**: Network configuration
- **Namespace State**: Network namespace


---

## Scaling and Deployment Patterns

### Horizontal Scaling


- **Plugin Scaling**: Multiple plugin instances
- **IP Pool Scaling**: IP address pool
- **Network Scaling**: Multiple network instances


### High Availability


- **Node HA**: CNI plugin on each node
- **Network HA**: Multiple network configurations


### Production Deployments


- **Production Configuration**: Production plugin configuration
- **Network Policy**: Enforced network policies
- **Monitoring**: Network metrics
- **Security**: Network isolation


### Upgrade Strategies


- **Plugin Upgrade**: Plugin version compatibility
- **Network Reconfiguration**: Zero-downtime network update


### Resource Management


- **IP Address Pool**: IP address management
- **Network Storage**: Network configuration storage


---

## Additional Resources

- **Official Documentation:** [https://github.com/containernetworking/cni/blob/master/SPEC.md](https://github.com/containernetworking/cni/blob/master/SPEC.md)
- **GitHub Repository:** [github.com/containernetworking/cni](https://github.com/containernetworking/cni)
- **CNCF Project Page:** [cncf.io/projects/cni/](https://www.cncf.io/projects/cni/)
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
