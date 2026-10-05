---




name: wasmcloud
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '"Provides wasmCloud in WebAssembly-based distributed applications platform"'
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  related-skills: null
  role: reference
  scope: infrastructure
  triggers: applications, distributed, wasmcloud, webassembly-based
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




# wasmCloud in Cloud-Native Engineering

**Category:** Scheduling & Orchestration  
**Status:** Active  
**Stars:** 1,100  
**Last Updated:** 2026-04-22  
**Primary Language:** Rust  
**Documentation:** [WebAssembly-based distributed applications platform](https://wasmcloud.com/docs/)  

---

## Purpose and Use Cases

wasmCloud is a core component of the cloud-native ecosystem, serving as applications platform

### What Problem Does It Solve?

wasmCloud addresses the challenge of distributed applications using WebAssembly. It provides portability, security, and language agnosticism for distributed systems.

### When to Use This Project

Use wasmCloud when need wasm-based apps, require security isolation, or want language-agnostic distributed computing. Not ideal for simple deployments or when edge computing, microservices with wasm, or secure distributed applications.

### Key Use Cases

- WebAssembly Microservices
- Edge Computing Applications
- Secure Function Execution
- Language-Agnostic Distributed Systems
- Portable Cloud-Native Apps

---

## Architecture Design Patterns

### Core Components

- **Host**: WasmCloud host runtime
- **Actor**: Application logic
- **Provider**: Backend services
- **Controller**: Cluster management
- **Distributed KV**: State management

### Component Interactions

1. **Actor → Provider**: Actor calls provider
1. **Host → Actor**: Host executes actor
1. **Host → Provider**: Host manages provider
1. **Controller → Host**: Controller manages hosts

### Data Flow Patterns

1. **Actor Execution**: Actor loaded → Executed by host → Calls provider
1. **Provider Registration**: Provider starts → Registered with host
1. **Message Flow**: Actor → Provider → Response
1. **State Sync**: Distributed KV sync across hosts

### Design Principles

- **Security First**: Sandboxed execution
- **Portability**: Run anywhere
- **Language Agnostic**: Any language with wasm support
- **Decentralized**: Decentralized architecture

---

## Integration Approaches

### Integration with Other CNCF Projects

- **WASI**: WebAssembly System Interface
- **Kubernetes**: Deployment platform
- **OCF**: Open Cloud Framework
- **Hyperspace**: Distributed KV

### API Patterns

- **Actor API**: Actor interface
- **Provider API**: Provider interface
- **Host API**: Host management API
- **WIT**: WebAssembly Interface Type

### Configuration Patterns

- **Host Config**: Host configuration
- **Actor Config**: Actor configuration
- **Provider Config**: Provider configuration
- **Cluster Config**: Cluster settings

### Extension Mechanisms

- **Custom Providers**: Add custom providers
- **Custom Actors**: Add custom actors
- **Custom Hosts**: Custom host implementations

---

## Common Pitfalls and How to Avoid Them

### Misconfigurations

- **Provider Connection**: Provider connection failures
  - **How to Avoid**: Check provider health, verify configurations
- **WASI Issues**: WASI compatibility issues
  - **How to Avoid**: Use compatible WASI versions, update toolchains

### Performance Issues

- **Host Scalability**: Host scalability issues
  - **How to Avoid**: Scale hosts, optimize provider usage
- **Upgrade Issues**: Upgrade failures
  - **How to Avoid**: Test upgrades, follow upgrade path

### Operational Challenges

- **Performance Issues**: Performance degradation
  - **How to Avoid**: Monitor performance, tune configurations
- **Tooling Issues**: Tooling limitations
  - **How to Avoid**: Use latest tooling, contribute improvements

### Security Pitfalls


---

## Coding Practices

### Idiomatic Configuration

- **Actor Design**: Design actors for portability
- **Provider Integration**: Integrate with providers cleanly
- **State Management**: Manage distributed state effectively

### API Usage Patterns

- **wadm**: WasmCloud deployment tool
- **wash**: WasmCloud host
- **wit**: Wasm Interface Type tool
- **wasm-tools**: Wasm tools

### Observability Best Practices

- **Host Metrics**: Monitor host performance
- **Actor Metrics**: Track actor execution
- **Provider Metrics**: Monitor provider health

### Testing Strategies

- **Integration Tests**: Test actor-provider interactions
- **Security Tests**: Validate security isolation
- **Performance Tests**: Validate performance

### Development Workflow

- **Local Development**: Use wash locally
- **Debug Commands**: Check host and actor logs
- **Test Environment**: Set up test cluster
- **CI/CD Integration**: Automate testing
- **Monitoring Setup**: Configure observability
- **Documentation**: Maintain documentation

---

## Fundamentals

### Essential Concepts

- **Actor**: Application logic
- **Provider**: Backend services
- **Host**: Wasm runtime
- **Capability**: Provider capability
- **WIT**: WebAssembly Interface Type
- **Distributed KV**: State management
- **Controller**: Cluster controller
- **Manifest**: Application manifest

### Terminology Glossary

- **Actor**: Application component
- **Provider**: Service provider
- **Host**: Wasm runtime
- **Capability**: Provider interface
- **WIT**: WebAssembly Interface Type

### Data Models and Types

- **Actor**: Actor definition
- **Provider**: Provider definition
- **Capability**: Capability interface
- **Manifest**: Application manifest

### Lifecycle Management

- **Actor Execution**: Actor loaded → Executed → Calls provider → Returns
- **Provider Registration**: Provider starts → Registered → Ready
- **Message Flow**: Actor → Provider → Response
- **State Sync**: KV state sync across hosts

### State Management

- **Actor State**: Loaded, running, or stopped
- **Provider State**: Running or offline
- **Host State**: Active or degraded
- **KV State**: Synced or outdated

---

## Scaling and Deployment Patterns

### Horizontal Scaling

- **Actor Scaling**: Scale actor instances
- **Provider Scaling**: Scale provider instances
- **Host Scaling**: Scale hosts

### High Availability

- **Host HA**: Multiple hosts
- **Provider HA**: Provider redundancy
- **KV HA**: Distributed KV redundancy

### Production Deployments

- **Cluster Setup**: Deploy wasmCloud cluster
- **Network Configuration**: Configure network
- **Security Setup**: Enable security isolation
- **Monitoring Setup**: Configure metrics
- **Logging Setup**: Centralize logs
- **Backup Strategy**: Backup configurations
- **Resource Quotas**: Set resource limits
- **Performance Tuning**: Optimize performance

### Upgrade Strategies

- **Host Upgrade**: Upgrade wasmCloud host
- **Provider Upgrade**: Upgrade providers
- **Actor Upgrade**: Upgrade actors
- **Testing**: Verify functionality

### Resource Management

- **CPU Resources**: CPU limits
- **Memory Resources**: Memory limits
- **Storage Resources**: Storage configuration
- **Network Resources**: Network configuration

---

## Additional Resources

- **Official Documentation:** https://wasmcloud.com/docs/
- **GitHub Repository:** Check the project's official documentation for repository link
- **CNCF Project Page:** [cncf.io/projects/cncf-wasmcloud/](https://www.cncf.io/projects/cncf-wasmcloud/)
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
