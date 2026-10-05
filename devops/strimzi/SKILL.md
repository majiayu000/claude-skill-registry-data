---




name: strimzi
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '"Provides Strimzi in Kafka on Kubernetes - Apache Kafka for cloud-native
  environments"'
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  role: reference
  scope: infrastructure
  triggers: apache, container orchestration, event streaming, k8s, kafka, message
    streaming, strimzi, kubernetes
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



# Strimzi in Cloud-Native Engineering

**Category:** Streaming & Messaging  
**Status:** Active  
**Stars:** 2,900  
**Last Updated:** 2026-04-22  
**Primary Language:** Java  
**Documentation:** [Kafka on Kubernetes - Apache Kafka for cloud-native environments](https://strimzi.io/docs/)  

---

## Purpose and Use Cases

Strimzi is a core component of the cloud-native ecosystem, serving as cloud-native environments

### What Problem Does It Solve?

Strimzi addresses the challenge of running Apache Kafka on Kubernetes with native integration. It provides Kafka-native on Kubernetes, automated management, and cloud-native scalability.

### When to Use This Project

Use Strimzi when need Kafka on Kubernetes, want managed Kafka, or require Kafka at scale. Not ideal for simple deployments or when event-driven architecture, Kafka-native deployment, or Kafka scaling requirements.

### Key Use Cases

- Kafka on Kubernetes Deployments
- Event-Driven Architecture
- Real-Time Data Streaming
- Kafka Multi-Tenancy
- Kafka Migration to Cloud

---

## Architecture Design Patterns

### Core Components

- **Cluster Operator**: Manages Kafka clusters
- **Kafka Node**: Kafka broker instance
- **ZooKeeper Node**: ZooKeeper ensemble member
- **Topic Operator**: Manages topics
- **User Operator**: Manages users and ACLs

### Component Interactions

1. **Operator → Kafka**: Operator manages Kafka cluster
1. **Kafka → ZooKeeper**: Kafka stores metadata in ZooKeeper
1. **Topic Operator → Kafka**: Topic operator manages topics
1. **User Operator → Kafka**: User operator manages users

### Data Flow Patterns

1. **Cluster Creation**: Create Kafka CR → Operator creates cluster → Kafka ready
1. **Topic Creation**: Create Topic CR → Topic operator → Kafka topic
1. **Message Flow**: Producer → Kafka → Consumer
1. **Configuration Sync**: Config updates → Kafka pods

### Design Principles

- **Kafka Native**: Full Kafka compatibility
- **Automated Management**: Full lifecycle management
- **Kubernetes Native**: Deep integration
- **Operational Simplicity**: Easy to operate

---

## Integration Approaches

### Integration with Other CNCF Projects

- **Kafka**: Apache Kafka core
- **ZooKeeper**: Metadata storage
- **Kubernetes**: Platform integration
- **Prometheus**: Metrics collection

### API Patterns

- **Kafka CRD**: Kafka cluster definition
- **Topic CRD**: Topic definition
- **User CRD**: User definition
- **Kafka Connect CRD**: Connect cluster definition

### Configuration Patterns

- **Kafka YAML**: Cluster configuration
- **Topic YAML**: Topic configuration
- **User YAML**: User configuration
- **Connect YAML**: Connect configuration

### Extension Mechanisms

- **Custom Connectors**: Add Kafka connectors
- **Custom Metrics**: Add custom metrics
- **Custom Config**: Custom Kafka config

---

## Common Pitfalls and How to Avoid Them

### Misconfigurations

- **Disk Space**: Kafka log storage exhaustion
  - **How to Avoid**: Monitor disk space, configure retention, scale storage
- **Network Issues**: Network partitions
  - **How to Avoid**: Configure network isolation, monitor latency

### Performance Issues

- **Upgrade Issues**: Kafka version upgrade problems
  - **How to Avoid**: Test upgrades, follow upgrade path, backup
- **Schema Registry**: Schema registry issues
  - **How to Avoid**: Configure registry, monitor health

### Operational Challenges

- **TLS Issues**: TLS configuration problems
  - **How to Avoid**: Verify certificates, check TLS settings
- **Replication Issues**: Replication lag
  - **How to Avoid**: Monitor replication, check network

### Security Pitfalls


---

## Coding Practices

### Idiomatic Configuration

- **Declarative Configuration**: Define Kafka in YAML
- **Topic Management**: Use KafkaTopic CRs
- **Monitoring Integration**: Integrate with Prometheus

### API Usage Patterns

- **kubectl apply**: Apply Kafka configurations
- **strimzi-cli**: Strimzi-specific commands
- **Kafka CLI**: Kafka tools
- **kubectl describe**: Describe Kafka resources

### Observability Best Practices

- **Kafka Metrics**: Monitor Kafka cluster metrics
- **Operator Metrics**: Monitor operator health
- **Topic Metrics**: Track topic statistics

### Testing Strategies

- **Integration Tests**: Test Kafka functionality
- **Failover Tests**: Test cluster failover
- **Performance Tests**: Validate performance

### Development Workflow

- **Local Development**: Use minikube or kind
- **Debug Commands**: Check Kafka and operator logs
- **Test Environment**: Set up test cluster
- **CI/CD Integration**: Automate testing
- **Monitoring Setup**: Configure observability
- **Documentation**: Maintain documentation

---

## Fundamentals

### Essential Concepts

- **Kafka Cluster**: Kafka cluster definition
- **Cluster Operator**: Cluster management
- **Kafka Broker**: Kafka broker instance
- **ZooKeeper**: ZooKeeper ensemble
- **Topic Operator**: Topic management
- **User Operator**: User management
- **Kafka Connect**: Kafka Connect cluster
- **Kafka Mirror Maker**: Data replication

### Terminology Glossary

- **Cluster Operator**: Manages Kafka clusters
- **Kafka Broker**: Kafka server instance
- **Topic Operator**: Manages topics
- **User Operator**: Manages users
- **Mirror Maker**: Data replication

### Data Models and Types

- **Kafka**: Kafka cluster definition
- **KafkaTopic**: Topic definition
- **KafkaUser**: User definition
- **KafkaConnect**: Connect cluster

### Lifecycle Management

- **Cluster Creation**: Create Kafka CR → Operator creates → Cluster ready
- **Topic Creation**: Create Topic CR → Operator creates → Topic exists
- **Upgrade Process**: Update Kafka version → Rolling restart → New version
- **Failure Recovery**: Detect failure → Heal → Restore

### State Management

- **Cluster State**: Ready, error, or scaling
- **Broker State**: Running, stopped, or starting
- **Topic State**: Created, updating, or deleted
- **Operator State**: Running or error

---

## Scaling and Deployment Patterns

### Horizontal Scaling

- **Broker Scaling**: Add/remove brokers
- **Consumer Scaling**: Scale consumer groups
- **Topic Scaling**: Replication factor changes
- **Cluster Scaling**: Add nodes to cluster

### High Availability

- **Broker HA**: Multiple brokers per partition
- **Replication HA**: ISR configuration
- **Operator HA**: Multiple operator instances
- **ZooKeeper HA**: ZooKeeper ensemble

### Production Deployments

- **Cluster Setup**: Deploy Kafka cluster
- **Network Configuration**: Configure network
- **Security Setup**: Enable TLS, SASL, RBAC
- **Monitoring Setup**: Configure metrics
- **Logging Setup**: Centralize logs
- **Backup Strategy**: Configure backups
- **Resource Quotas**: Set resource limits
- **Performance Tuning**: Optimize Kafka settings

### Upgrade Strategies

- **Kafka Upgrade**: Upgrade Kafka version
- **Operator Upgrade**: Upgrade operator
- **Broker Upgrade**: Rolling broker upgrade
- **Testing**: Verify functionality

### Resource Management

- **CPU Resources**: Broker CPU limits
- **Memory Resources**: Broker memory limits
- **Storage Resources**: Log storage configuration
- **Network Resources**: Network configuration

---

## Additional Resources

- **Official Documentation:** https://strimzi.io/docs/
- **GitHub Repository:** Check the project's official documentation for repository link
- **CNCF Project Page:** [cncf.io/projects/cncf-strimzi/](https://www.cncf.io/projects/cncf-strimzi/)
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
