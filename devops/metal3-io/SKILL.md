---




name: metal3-io
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '"metal3.io in Bare Metal Provisioning - cloud native architecture, patterns"
  pitfalls, and best practices'
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  related-skills: null
  role: reference
  scope: infrastructure
  triggers: cdn, infrastructure as code, metal, metal3 io, metal3-io, monitoring,
    provisioning, cloudformation
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




# Metal3.io in Cloud-Native Engineering

**Category:** infrastructure  
**Status:** Incubating  
**Stars:** 2,000  
**Last Updated:** 2026-04-22  
**Primary Language:** Go  
**Documentation:** [https://metal3.io/](https://metal3.io/)  

---

## Purpose and Use Cases

### What Problem Does It Solve?

Metal3.io bridges the gap between traditional bare metal infrastructure and cloud-native Kubernetes operations. It provides an open-source framework for provisioning and managing bare metal hosts using Kubernetes APIs, eliminating the need for out-of-band infrastructure management tools and enabling infrastructure-as-code practices for physical servers.

### When to Use This Project

Use Metal3.io when you need:
- Kubernetes-native bare metal host provisioning
- Infrastructure-as-code for physical servers
- Integration with existing cloud-native tooling
- Automated hardware discovery and validation
- Integration with IPMI, Redfish, or other out-of-band management
- Consistent management of on-prem and cloud infrastructure

### Key Use Cases

- **On-Prem Kubernetes**: Deploy Kubernetes clusters on bare metal infrastructure
- **Edge Computing**: Provision and manage edge servers consistently
- **Hybrid Cloud**: Unify management of cloud and on-prem resources
- **CI/CD for Infrastructure**: Use GitOps for infrastructure provisioning
- **Disaster Recovery**: Rapid infrastructure re-provisioning
- **Multi-Cluster Management**: Manage multiple bare metal clusters

---

## Architecture Design Patterns

### Core Components

- **Bare Metal Host**: Kubernetes CRD representing physical server
- **Provisioner**: Manages the provisioning lifecycle of bare metal hosts
- **Ironic**: OpenStack Ironic service for hardware management
- **Inspector**: Discovers and validates hardware capabilities
- **BMC Controller**: Manages Baseboard Management Controllers
- **Machine Config**: Configuration for machine provisioning
- **Cluster API Provider**: Integrates with Cluster API for cluster deployment
- **Image Downloader**: Downloads and caches OS images

### Component Interactions

1. **User → Kubernetes API**: Create BareMetalHost CRD for a physical server
2. **BareMetalHost → BMC Controller**: Access and configure BMC
3. **BMC Controller → Ironic**: Provisioning orchestration
4. **Ironic → Provisioner**: Hardware management operations
5. **Provisioner → Image Downloader**: Download and cache OS images
6. **Inspector → Hardware**: Discover and validate hardware capabilities
7. **Cluster API Provider → Metal3**: Provision worker nodes for cluster

### Data Flow Patterns

1. **Host Registration**: Physical server → BareMetalHost CRD → BMC validation → Hardware inspection
2. **Provisioning**: BareMetalHost → Ironic → Image download → Disk preparation → OS installation
3. **Machine Creation**: Machine CR → Metal3 Provider → BareMetalHost allocation → Provisioning
4. **Health Monitoring**: BMC → BareMetalHost status → Reconciliation loop → Failure detection
5. **Image Management**: Registry → Image Downloader → Caching → Provisioning

### Design Principles

- **Kubernetes-Native**: Full CRD integration with standard Kubernetes patterns
- **Open Standards**: Support for IPMI, Redfish, and other industry standards
- **Extensible**: Plugin architecture for different hardware providers
- **Self-Healing**: Automatic recovery from provisioning failures
- **Consistent State**: Reconciliation loop ensures desired state matches actual state

---

## Integration Approaches

### Integration with Other CNCF Projects

- **Kubernetes**: Full integration for container workloads on bare metal
- **Cluster API**: Provider for provisioning Kubernetes nodes
- **Prometheus**: Expose hardware metrics and provisioning status
- **Grafana**: Dashboards for hardware health and provisioning status
- **CoreDNS**: DNS configuration for provisioned hosts
- **Cert-Manager**: Certificate management for secure boot
- **OpenShift**: Support for OpenShift bare metal deployments

### API Patterns

- **BareMetalHost CRD**: Manage bare metal host lifecycle
- **Machine CRD**: Cluster API machine provisioning
- **BMC Secret**: Secure credentials for out-of-band management
- **HardwareProfile**: Pre-defined hardware configurations
- **Provisioning State**: Lifecycle state machine for hosts

### Configuration Patterns

- **BMC Credentials**: Securely store credentials in Kubernetes secrets
- **Hardware Profiles**: Define reusable hardware configurations
- **Provisioning Images**: Customize OS images for different use cases
- **Network Configuration**: Define network settings for provisioned hosts
- **Power Management**: Configure power policies and schedules

### Extension Mechanisms

- **Custom Hardware Profiles**: Add support for new hardware models
- **Custom Provisioners**: Implement support for alternative provisioning tools
- **Webhooks**: Add validation and mutation for BareMetalHost CRDs
- **Metrics Export**: Extend metrics with custom hardware data

---

## Common Pitfalls and How to Avoid Them

### Configuration Issues

- **BMC Credentials**: Ensure correct and accessible BMC credentials
- **Network Configuration**: Validate network settings before provisioning
- **Image Availability**: Ensure required OS images are available and accessible
- **Hardware Compatibility**: Verify hardware is supported by Ironic drivers
- **Firewall Rules**: Configure proper firewall rules for BMC access

### Performance Issues

- **Image Download Speed**: Use caching and local image repositories
- **Provisioning Time**: Optimize hardware inspection and disk preparation
- **Concurrent Provisioning**: Balance workload across provisioner workers
- **Database Performance**: Monitor and optimize Ironic database performance

### Operational Challenges

- **Hardware Failures**: Implement monitoring and alerting for hardware issues
- **BMC Outages**: Plan for BMC unavailability during provisioning
- **Image Updates**: Test image updates before production deployment
- **Capacity Planning**: Monitor hardware inventory and plan for expansion

### Security Pitfalls

- **BMC Security**: Use secure credentials and limit BMC network access
- **Image Security**: Verify OS image signatures and integrity
- **Network Isolation**: Isolate provisioning network from production
- **Access Control**: Restrict access to BareMetalHost CRDs

---

## Coding Practices

### Idiomatic Configuration

- **BMC Secret Management**: Use Kubernetes secrets for sensitive credentials
- **Hardware Profile Templates**: Create reusable hardware configurations
- **Network ConfigMaps**: Use ConfigMaps for network configuration
- **Image Registry Configuration**: Configure image pull secrets and registry settings

### API Usage Patterns

- **BareMetalHost Operations**: Register, validate, provision, and deprovision hosts
- **Machine Integration**: Integrate with Cluster API for cluster provisioning
- **Status Monitoring**: Monitor BareMetalHost status for provisioning progress
- **Event Handling**: Handle provisioning events and failures

### Observability Best Practices

- **Metrics Collection**: Prometheus scrape Metal3 metrics endpoint
- **Alerting**: Set up alerts for provisioning failures and hardware issues
- **Dashboard**: Use Grafana dashboards for provisioning status
- **Log Analysis**: Monitor Metal3 component logs for issues
- **Hardware Monitoring**: Track hardware health metrics

### Development Workflow

- **Local Development**: Use Vagrant or virtual environments for testing
- **Testing**: Test provisioning workflows in staging environment
- **CI/CD Integration**: Automate infrastructure provisioning in CI/CD
- **Rollback Plans**: Test rollback procedures for failed provisioning

---

## Fundamentals

### Essential Concepts

- **Bare Metal Host**: Physical server managed by Metal3
- **BMC**: Baseboard Management Controller for out-of-band management
- **Provisioning**: Process of installing OS and configuring hardware
- **Ironic**: OpenStack service for bare metal provisioning
- **Image Registration**: Preparing and registering OS images
- **Hardware Inspection**: Discovering hardware capabilities
- **Machine**: Kubernetes node provisioned by Metal3

### Terminology Glossary

- **Bare Metal Host**: CRD representing a physical server
- **BMC**: Baseboard Management Controller
- **Provisioning**: Installing OS and configuring hardware
- **Deprovisioning**: Cleaning up and returning host to ready state
- **Hardware Profile**: Pre-defined hardware configuration
- **Inspection**: Discovering hardware capabilities
- **Image Registration**: Registering OS images for provisioning
- **Power State**: Current power state of the host

### Data Models and Types

- **BareMetalHost**: Full specification and status of a bare metal host
- **BMC Secret**: Kubernetes secret containing BMC credentials
- **HardwareProfile**: Pre-defined hardware configuration template
- **Provisioning State**: Lifecycle state of the host
- **Hardware Information**: Discovered hardware capabilities

### Lifecycle Management

- **Host Lifecycle**: Register → Validate → Inspect → Provision → Ready → Deprovision → Free
- **Machine Lifecycle**: Request → Allocation → Provisioning → Running → Delete
- **Image Lifecycle**: Upload → Registration → Caching → Provisioning → Cleanup

### State Management

- **Host State**: Registering, inspecting, provisioning, ready, deprovisioning, error
- **Image State**: Uploading, registered, caching, available, error
- **Power State**: On, off, rebooting, error

---

## Scaling and Deployment Patterns

### Horizontal Scaling

- **Provisioner Replicas**: Scale provisioner for concurrent provisioning
- **Image Downloader**: Cache images across multiple nodes
- **Ironic Database**: Scale database for large deployments
- **BMC Connections**: Distribute BMC connections across provisioner workers

### High Availability

- **Provisioner Redundancy**: Multiple provisioner instances for failover
- **Image Caching**: Distribute image cache across provisioner nodes
- **BMC Redundancy**: Configure redundant BMC connections
- **Database HA**: Deploy Ironic database in HA mode

### Production Deployments

- **Production Cluster**: Deploy Metal3 with high availability
- **Image Registry**: Use local registry for image caching
- **Network Segmentation**: Isolate provisioning network
- **Monitoring**: Set up Prometheus and Grafana for monitoring

### Upgrade Strategies

- **Minor Version**: In-place upgrade with zero-downtime
- **Major Version**: Follow upgrade guide with backup
- **Rollback Plan**: Keep previous version images for rollback
- **Pre-Upgrade Check**: Run health checks before upgrade

### Resource Management

- **Memory**: Configure provisioner resource requests
- **CPU**: Balance CPU usage across provisioner workers
- **Network**: Monitor provisioning network utilization
- **Storage**: Manage image cache storage usage

---

## Additional Resources

- **Official Documentation:** [https://metal3.io/docs/](https://metal3.io/docs/)
- **GitHub Repository:** [github.com/metal3-io/metal3-docs](https://github.com/metal3-io/metal3_docs)
- **CNCF Project Page:** [cncf.io/projects/metal3/](https://www.cncf.io/projects/metal3/)
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
