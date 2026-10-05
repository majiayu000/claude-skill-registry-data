---




name: falco
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '"Provides Falco in Cloud-Native Engineering - Cloud Native Runtime Security"'
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  role: reference
  scope: infrastructure
  triggers: cdn, cloud-native, engineering, falco, infrastructure as code, monitoring,
    cloudformation, cloudfront
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




  related-skills: cncf-aws-kms, cncf-aws-s3, cncf-aws-secrets-manager, cncf-azure-key-vault



# Falco in Cloud-Native Engineering

**Category:** cloud-native  
**Status:** Active  
**Stars:** 8,890  
**Last Updated:** 2026-04-21  
**Primary Language:** C++  
**Documentation:** [https://falco.org/docs/](https://falco.org/docs/)  

---

## Purpose and Use Cases

Falco is a core component of the cloud-native ecosystem, serving as a runtime security observability tool that monitors system calls and detects anomalous activity in containers and hosts.

### What Problem Does It Solve?

The challenge of detecting security threats and anomalous behavior in running containers and hosts without modifying application code or adding heavy monitoring agents.

### When to Use This Project

Use Falco when you need runtime security monitoring for containers and hosts, want to detect anomalous activity based on behavioral baselines, or require compliance auditing for system calls.

### Key Use Cases


- Runtime security monitoring
- Anomaly detection in containers
- System call monitoring
- Compliance auditing
- Intrusion detection for Kubernetes


---

## Architecture Design Patterns

### Core Components


- **Kernel Module**: Captures system calls from kernel
- **eBPF Program**: Alternative to kernel module for syscall capture
- **Rule Engine**: Evaluates system calls against security rules
- **Output Engine**: Sends alerts to configured destinations
- **Rules Files**: YAML files containing security detection rules
- **Syscall Buffer**: Buffer for system call events


### Component Interactions


1. **Kernel → Syscall Buffer**: Captures system calls
2. **Rule Engine → Syscall Buffer**: Evaluates calls
3. **Rule Engine → Output Engine**: Sends alerts
4. **Output Engine → Destinations**: Sends to log files, syslog, etc.


### Data Flow Patterns


1. **Syscall Capture**: Kernel → eBPF/bpf → Buffer → Rule engine
2. **Rule Evaluation**: Syscall → Rule match → Output event → Handler
3. **Alert Handling**: Event → Filter → Output → Destinations


### Design Principles


- **Behavioral Monitoring**: Detects anomalous behavior
- **Rule-Based**: Configurable detection rules
- **Multi-Platform**: Linux kernel and container support
- **Output Flexible**: Multiple output destinations
- **Extensible**: Custom rules and outputs


---

## Integration Approaches

### Integration with Other CNCF Projects


- **Kubernetes**: Native Kubernetes security monitoring
- **Runtime**: Container and host security
- **Audit Logging**: System call monitoring
- **Output Destinations**: Integration with monitoring systems


### API Patterns


- **Config File**: YAML-based configuration
- **Rules File**: YAML-based rule definitions
- **Output Configuration**: Multiple output destinations
- **gRPC API**: Plugin interface (optional)


### Configuration Patterns


- **falco.yaml**: Main configuration
- **Rules Files**: Security rules
- **Output Configuration**: Destination settings
- **GRPC Config**: Plugin configuration


### Extension Mechanisms


- **Rules**: Custom detection rules
- **Output Destinations**: Custom handlers
- **Syscalls**: System call filters
- **Plugin System**: Runtime plugins


---

## Common Pitfalls and How to Avoid Them

### Misconfigurations


- **Rule Syntax**: Incorrect YAML rule syntax
- **Syscall Filters**: Incorrect syscall filters
- **Output Configuration**: Missing or incorrect outputs
- **Rules Priority**: Incorrect rule ordering


### Performance Issues


- **Syscall Overhead**: High kernel overhead
- **Rule Evaluation**: Many rules
- **Buffer Size**: Small buffer causing drops
- **Output Performance**: Slow output destinations


### Operational Challenges


- **Rule Maintenance**: Keeping rules current
- **Performance Impact**: Minimal overhead
- **False Positives**: Tuning rules
- **Log Volume**: Managing alert volume


### Security Pitfalls


- **Rule Security**: Rules accessing sensitive files
- **Output Security**: Unencrypted alert transmission
- **Syscall Filtering**: Incomplete syscall capture


---

## Coding Practices

### Idiomatic Configuration


- **YAML Configuration**: Clear structure
- **Rules Files**: Organized rule definitions
- **Environment Variables**: Override config
- **Output Configuration**: Modular output setup


### API Usage Patterns


- **falco CLI**: Command-line options
- **Rules Files**: Rule management
- **Output Config**: Configure destinations


### Observability Best Practices


- **Alert Metrics**: Alert volume and types
- **Rule Statistics**: Rule match counts
- **Syscall Metrics**: System call volume
- **Output Logs**: Alert destination logs


### Testing Strategies


- **Unit Tests**: Rule tests
- **Integration Tests**: Syscall capture
- **E2E Tests**: Full security monitoring
- **Compatibility Tests**: Kernel versions


### Development Workflow


- **Development**: Falco development setup
- **Testing**: Rule tests, integration tests
- **Debugging**: Debug logs, rule testing
- **Deployment**: DaemonSet, static pods
- **CI/CD**: GitHub Actions, security testing
- **Tools**: falco-driver-loader, falcoctl


---

## Fundamentals

### Essential Concepts


- **Rule**: Security detection rule
- **Syscall**: System call monitoring
- **Output**: Alert destination
- **Event**: Security event
- **Filter**: Rule condition
- **Predicate**: Rule evaluation
- **Macro**: Reusable rule component
- **List**: Reusable list of values
- **eBPF**: Kernel-level capture
- **Kernel Module**: Alternative capture method


### Terminology Glossary


- **Rule**: Detection rule
- **Syscall**: System call
- **Output**: Alert destination
- **Event**: Security event
- **Filter**: Rule condition
- **Predicate**: Rule evaluation
- **Macro**: Reusable component
- **List**: Reusable values
- **eBPF**: Kernel capture
- **Kernel Module**: Capture method


### Data Models and Types


- **Rule**: Rule definition
- **Macro**: Macro definition
- **List**: List definition
- **Filter**: Filter definition
- **Output**: Output configuration
- **Event**: Event data
- **Predicate**: Predicate definition


### Lifecycle Management


- **Event Lifecycle**: Capture → Filter → Match → Output
- **Rule Lifecycle**: Load → Evaluate → Update
- **Alert Lifecycle**: Detect → Process → Notify


### State Management


- **Rule State**: Loaded rules
- **Syscall Buffer State**: Captured syscalls
- **Output State**: Alert destinations
- **Event State**: Pending events


---

## Scaling and Deployment Patterns

### Horizontal Scaling


- **Node Scaling**: Falco on each node
- **Rule Engine Scaling**: Parallel rule evaluation
- **Output Scaling**: Multiple output destinations


### High Availability


- **Node HA**: Falco daemonset
- **Output HA**: Multiple output destinations


### Production Deployments


- **Production Configuration**: Optimized rules
- **Output Configuration**: Production alert destinations
- **Monitoring**: Falco metrics
- **Performance**: Minimal overhead configuration


### Upgrade Strategies


- **Rule Update**: Dynamic rule loading
- **Version Compatibility**: Kernel module compatibility
- **Configuration Reload**: Zero-downtime config update


### Resource Management


- **Buffer Size**: Syscall buffer size
- **Memory Configuration**: Rule evaluation memory
- **CPU Configuration**: Rule evaluation threads


---

## Additional Resources

- **Official Documentation:** [https://falco.org/docs/](https://falco.org/docs/)
- **GitHub Repository:** [github.com/falcosecurity/falco](https://github.com/falcosecurity/falco)
- **CNCF Project Page:** [cncf.io/projects/falco/](https://www.cncf.io/projects/falco/)
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
