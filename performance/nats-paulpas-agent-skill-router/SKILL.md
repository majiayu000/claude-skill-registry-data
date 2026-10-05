---




name: nats
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '"NATS in Cloud Native Messaging - cloud native architecture, patterns"
  pitfalls, and best practices'
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  related-skills: calico, cilium, cloudevents, container-network-interface-cni
  role: reference
  scope: infrastructure
  triggers: cdn, infrastructure as code, messaging, monitoring, native, nats, cloudformation,
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




# NATS in Cloud-Native Engineering

**Category:** messaging  
**Status:** Incubating  
**Stars:** 14,500  
**Last Updated:** 2026-04-22  
**Primary Language:** Go  
**Documentation:** [https://nats.io/](https://nats.io/)  

---

## Purpose and Use Cases

### What Problem Does It Solve?

NATS addresses the critical need for lightweight, high-performance messaging in distributed systems. Traditional messaging systems like RabbitMQ or Kafka often introduce complexity, overhead, and operational burden that are unnecessary for many cloud-native workloads. NATS provides a simple, fast, and secure messaging infrastructure that scales effortlessly from microservices to large distributed systems.

### When to Use This Project

Use NATS when you need:
- Low-latency, high-throughput messaging
- Simple pub/sub messaging patterns
- Request-reply patterns for RPC
- Microservice communication with minimal overhead
- Edge and IoT messaging with constrained resources
- Cloud-native service discovery and health checks
- Streaming with durable subscriptions and at-least-once delivery

### Key Use Cases

- **Microservice Communication**: Lightweight service-to-service messaging
- **Event-Driven Architecture**: Publish-subscribe event distribution
- **Request-Reply Patterns**: Synchronous RPC over NATS
- **Configuration Management**: Distributed configuration updates
- **Health Monitoring**: Service health and status broadcasting
- **IoT Messaging**: Edge device communication with low latency
- **Serverless Triggering**: Event-based function invocation
- **Streaming Analytics**: High-throughput event streaming

---

## Architecture Design Patterns

### Core Components

- **NATS Server**: Lightweight message broker for pub/sub and request-reply
- **NATS Streaming (Streaming)**: Persistent message streaming with durability
- **JetStream**: Native streaming and queue subscription support
- **NATS Client**: Language-specific client libraries for message operations
- **Leaf Nodes**: Connect separate NATS clusters for federation
- **Gateways**: Wide area network (WAN) cluster connections
- **NATS Resolver**: Dynamic cluster configuration and discovery
- **User Authentication**: JWT-based user and account management

### Component Interactions

1. **Publisher → NATS Server**: Publish messages to subjects
2. **NATS Server → Subscriber**: Deliver messages to interested subscribers
3. **Client → NATS Server**: Connect, subscribe, publish, and receive messages
4. **Server → Server**: Interconnect for clustering and federation
5. **JetStream → Storage**: Persist messages to file-based storage
6. **NATS Resolver → Server**: Dynamic configuration distribution

### Data Flow Patterns

1. **Publish-Subscribe**: Publisher sends to subject → Server routes to all subscribers
2. **Request-Reply**: Request sent → Server routes → Reply from one service
3. **Queue Subscription**: Message delivered to one worker from queue group
4. **JetStream Production**: Message published → Stored → Available for consumers
5. **Consumer Group**: Multiple consumers share message processing load
6. **Federation**: Leaf node connects → Cluster sync → Cross-cluster messaging

### Design Principles

- **Simplicity**: Minimal concepts (subjects, subscribers, publishers)
- **Speed**: Zero-copy architecture for maximum throughput
- **Reliability**: At-least-once delivery with JetStream
- **Scalability**: Stateless servers with horizontal scaling
- **Flexibility**: Multiple messaging patterns and delivery modes
- **Security**: JWT-based authentication and authorization

---

## Integration Approaches

### Integration with Other CNCF Projects

- **Kubernetes**: Service discovery via NATS Service Import/Export
- **Prometheus**: Expose server metrics for monitoring
- **Grafana**: Pre-built dashboards for NATS metrics
- **Tekton**: Event-driven pipeline triggering
- **Helm**: Deploy NATS using Helm chart
- **Istio**: Service mesh integration for mTLS
- **OpenTelemetry**: Distributed tracing support
- **Cert-Manager**: TLS certificate management

### API Patterns

- **Subject-Based Routing**: Messages routed by subject patterns
- **Queue Groups**: Load balance across multiple subscribers
- **JetStream API**: Advanced streaming with durable consumers
- **NATS RPC**: Request-reply pattern for RPC
- **Websocket API**: Browser-based client access
- **HTTP API**: REST-style interface for simple clients

### Configuration Patterns

- **Server Configuration**: YAML-based server configuration
- **JetStream Settings**: Configure streams and consumers
- **Authorization**: JWT-based user and permission management
- **Clustering**: Configure server cluster for HA
- **Leaf Node**: Connect separate NATS clusters
- **Gateway**: Configure wide area clustering

### Extension Mechanisms

- **NATS Scripts**: Execute NATS script for automation
- **Webhooks**: Integrate with webhook-based systems
- **Custom Clients**: Implement custom NATS protocol clients
- **Metrics Export**: Extend metrics with custom data

---

## Common Pitfalls and How to Avoid Them

### Configuration Issues

- **Subject Design**: Plan subjects carefully for scalability and organization
- **Memory Limits**: Configure memory limits to prevent server overload
- **JetStream Storage**: Allocate sufficient disk space for persistent streams
- **TLS Configuration**: Properly configure TLS certificates and verification
- **Authentication**: Set up JWT authentication correctly

### Performance Issues

- **Subscriber Overload**: Scale subscribers to handle message volume
- **Message Batching**: Batch messages for high-throughput scenarios
- **Connection Limits**: Monitor and limit concurrent connections
- **Flow Control**: Implement flow control for slow consumers
- **Network Latency**: Optimize network topology for latency-sensitive apps

### Operational Challenges

- **Server Clustering**: Configure cluster for proper quorum and failover
- **JetStream Recovery**: Plan for stream and consumer recovery
- **Log Rotation**: Configure log rotation to prevent disk exhaustion
- **Backup and Restore**: Implement backup strategy for JetStream data
- **Version Upgrades**: Plan zero-downtime upgrades

### Security Pitfalls

- **Subject Permissions**: Carefully manage subject-level permissions
- **JWT Security**: Secure JWT signing keys and distribution
- **Anonymous Connections**: Disable anonymous connections in production
- **TLS Verification**: Always verify certificates in production
- **Audit Logging**: Enable audit logging for compliance

---

## Coding Practices

### Idiomatic Configuration

- **Server YAML**: Declarative server configuration
- **JetStream Streams**: Define streams with retention policies
- **Consumer Groups**: Configure durable consumers withacks
- **Authorization**: Use JWT for fine-grained permissions

### API Usage Patterns

- **Basic Pub/Sub**: Subscribe to subjects, publish messages
- **Queue Subscriptions**: Load balance across workers
- **Request-Reply**: Use NATS for RPC patterns
- **JetStream API**: Advanced streaming with durable consumers
- **Flow Control**: Implement backpressure handling

### Observability Best Practices

- **Metrics Collection**: Prometheus scrape NATS metrics endpoint
- **Alerting**: Set up alerts for slow consumers and connection issues
- **Dashboard**: Use Grafana dashboards for NATS monitoring
- **Log Analysis**: Monitor server logs for errors and warnings
- **Tracing**: Integrate OpenTelemetry for distributed tracing

### Development Workflow

- **Local Development**: Use NATS server in Docker for testing
- **Testing**: Test messaging patterns in staging environment
- **CI/CD Integration**: Integrate NATS in CI/CD workflows
- **Rollback Plans**: Test rollback procedures for configuration changes

---

## Fundamentals

### Essential Concepts

- **Subject**: Topic or channel for message routing
- **Subscriber**: Client that receives messages for a subject
- **Publisher**: Client that sends messages to a subject
- **Queue Group**: Multiple subscribers sharing message load
- **JetStream**: Native streaming with durability and persistence
- **Consumer**: JetStream consumer that processes messages
- **Stream**: JetStream stream that stores messages
- **Delivery Policy**: Define how messages are delivered to consumers

### Terminology Glossary

- **Subject**: Message routing key
- **Queue**: Group of subscribers sharing message load
- **JetStream**: Native streaming engine
- **Stream**: Log of messages with retention policy
- **Consumer**: Reader of messages from a stream
- **Ack Policy**: Acknowledgment requirements for consumers
- **Durable Consumer**: Consumer with state persistence
- **Redelivery**: Re-send messages that weren't acknowledged

### Data Models and Types

- **Message**: Subject, payload, headers, and metadata
- **Stream**: Name, subjects, retention, storage type
- **Consumer**: Name, filter subject, acknowledgment policy
- **Subscription**: Client subscription to subject(s)
- **Connection**: Client connection to NATS server

### Lifecycle Management

- **Publisher Lifecycle**: Connect → Publish → Disconnect
- **Subscriber Lifecycle**: Connect → Subscribe → Receive → Unsubscribe
- **JetStream Producer**: Create stream → Publish → Manage
- **JetStream Consumer**: Create consumer → Subscribe → Process

### State Management

- **Connection State**: Connected, disconnected, reconnecting
- **Subscription State**: Active, inactive, paused
- **Stream State**: Messages stored, bytes, first/last sequence
- **Consumer State**: Deliver sequence, ack floor, pending

---

## Scaling and Deployment Patterns

### Horizontal Scaling

- **Server Clustering**: Add servers to increase capacity
- **Queue Groups**: Scale consumers for message processing
- **JetStream Clusters**: Scale streaming capacity
- **Leaf Nodes**: Federate clusters for cross-region messaging

### High Availability

- **Server Redundancy**: Deploy multiple servers for failover
- **JetStream Quorum**: Use multiple replicas for stream durability
- **Consumer Failover**: Automatic consumer failover
- **Cluster Rebalancing**: Automatically rebalance during failures

### Production Deployments

- **Production Cluster**: Deploy multiple servers with clustering
- **JetStream Replication**: Configure stream replication across nodes
- **TLS Encryption**: Enable TLS for all connections
- **Monitoring**: Set up Prometheus and Grafana for monitoring

### Upgrade Strategies

- **Rolling Update**: Update servers one at a time
- **JetStream Migration**: Plan for stream migration during upgrades
- **Client Compatibility**: Test client compatibility before upgrade
- **Rollback Plan**: Keep previous version available for rollback

### Resource Management

- **Memory Limits**: Configure memory limits for server stability
- **Disk Space**: Monitor disk space for JetStream storage
- **Connection Limits**: Limit concurrent connections
- **Network Bandwidth**: Monitor network utilization

---

## Additional Resources

- **Official Documentation:** [https://docs.nats.io/](https://docs.nats.io/)
- **GitHub Repository:** [github.com/nats-io/nats-server](https://github.com/nats-io/nats-server)
- **CNCF Project Page:** [cncf.io/projects/nats/](https://www.cncf.io/projects/nats/)
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
