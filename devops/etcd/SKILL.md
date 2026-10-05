---




name: etcd
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '"Provides etcd in Cloud-Native Engineering - distributed key-value store"'
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  related-skills: null
  role: reference
  scope: infrastructure
  triggers: cloud-native, distributed, engineering, etcd
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




# etcd in Cloud-Native Engineering

**Category:** storage  
**Status:** Graduated  
**Stars:** 36,000  
**Last Updated:** 2026-04-22  
**Primary Language:** Go  
**Documentation:** [https://etcd.io/](https://etcd.io/)  

---

## Purpose and Use Cases

etcd is a distributed key-value store designed to help engineers build, deploy, and manage cloud-native applications.

### What Problem Does It Solve?

etcd addresses complex storage challenges by providing:
- Standardized APIs and interfaces
- Declarative configuration management
- Automatic resource management and reconciliation
- Built-in observability and monitoring
- Extensible architecture for custom integrations

### When to Use This Project

Use etcd when you need distributed key-value store, require storage-specific features, want to integrate with other CNCF projects, need production-ready storage solutions, or require storage-specific best practices.

### Key Use Cases

- **etcd Core**: Primary use case for distributed key-value store
- **Integration with Kubernetes**: Native Kubernetes integration
- **Multi-Cluster Support**: Manage multiple clusters
- **Scalable Operations**: Handle large-scale deployments
- **Automated Management**: Self-healing and automatic recovery
- **Security Features**: Built-in security controls
- **Observability**: Comprehensive metrics and logging

---

## Architecture Design Patterns

### Core Components

- **Main Controller**: Primary reconciliation loop
- **API Server**: REST/gRPC API endpoint
- **Webhook**: Admission webhooks for validation
- **Scheduler**: Work scheduling and distribution
- **Storage Backend**: Persistent state storage
- **Agent**: Worker component for distributed tasks
- **Metrics Collector**: Metrics aggregation

### Component Interactions

1. **User → API Server**: Create/modify resources
2. **API Server → Controller**: Resource creation event
3. **Controller → Storage**: State persistence
4. **Storage → Controller**: State retrieval for reconciliation
5. **Controller → Worker**: Task delegation
6. **Worker → Status**: Status updates back to API

### Data Flow Patterns

1. **Reconciliation Flow**: Resource change → Controller detects → State comparison → Action taken → Status updated
2. **Event Flow**: Event received → Event handler → Reconciler → State updated
3. **Scaling Flow**: Metrics threshold → Controller evaluates → Scale decision → Resource scaled
4. **Failure Flow**: Component failure → Detector → Recovery action → State restored

### Design Principles

- **Kubernetes Native**: Built on Kubernetes APIs and conventions
- **Declarative**: Desired state management
- **Automated**: Self-healing and automatic recovery
- **Extensible**: Plugin architecture for extensions
- ** Observability**: Built-in metrics and logging
- **Secure**: Security-first design principles
- **Reliable**: High availability and disaster recovery

---

## Integration Approaches

### Integration with Other CNCF Projects

- **Kubernetes**: Core platform for etcd
- **Prometheus**: Metrics collection and alerting
- **OpenTelemetry**: Distributed tracing integration
- **Helm**: Chart deployment
- **cert-manager**: TLS certificate management
- **Istio/Linkerd**: Service mesh integration
- **Flux/ArgoCD**: GitOps integration

### API Patterns

- **Kubernetes API**: Standard Kubernetes CRDs
- **REST API**: HTTP/JSON REST API
- **gRPC API**: High-performance gRPC API
- **Webhook API**: Admission webhooks
- **Metrics API**: Prometheus-compatible metrics

### Configuration Patterns

- **YAML Configuration**: Declarative YAML manifests
- **Environment Variables**: Runtime configuration
- **ConfigMaps**: Externalized configuration
- **Secrets**: Sensitive data management
- **Helm Values**: Helm chart configuration

### Extension Mechanisms

- **CRDs**: Custom Resource Definitions
- **Webhooks**: Custom admission webhooks
- **Plugins**: Plugin architecture for extensions
- **Controllers**: Custom controllers
- **Adapters**: Adapter pattern for integrations

---

## Common Pitfalls and How to Avoid Them

### Configuration Issues

- **YAML Syntax Errors**: Incorrect YAML formatting
- **Missing Dependencies**: Missing required resources
- **Invalid Values**: Invalid configuration values
- **Resource Limits**: Insufficient resource limits

**How to Avoid:**
- Use kubectl dry-run for validation
- Implement CI/CD pipeline with yamllint
- Test configurations in staging environment
- Use configuration validation webhooks

### Performance Issues

- **Resource Exhaustion**: CPU or memory limits hit
- **Latency Spikes**: Slow responses under load
- **Scale Bottlenecks**: Scaling limitations
- **Storage Growth**: Unbounded storage growth

**How to Avoid:**
- Monitor resource usage with Prometheus
- Implement appropriate resource limits
- Use horizontalPodAutoscaler
- Configure storage quotas and cleanup policies

### Operational Challenges

- **Upgrade Complexity**: Complex upgrade procedures
- **Data Migration**: Migration between versions
- **Backup and Restore**: Backup procedures
- **Troubleshooting**: Debugging issues

**How to Avoid:**
- Follow official upgrade path documentation
- Test upgrades in staging first
- Implement regular backups
- Use diagnostic tools and logs

### Security Pitfalls

- **Privilege Escalation**: Overly permissive RBAC
- **Secrets Exposure**: Secrets in logs or configs
- **Network Exposure**: Exposed services
- **Authentication**: Weak authentication mechanisms

**How to Avoid:**
- Implement least-privilege RBAC
- Use secrets management
- Implement network policies
- Enable authentication and authorization

---

## Coding Practices

### Idiomatic Configuration

- **Resource Definitions**: Declarative YAML manifests
- **Configuration Management**: Externalized configuration
- **Secret Management**: Secure secrets handling
- **Version Control**: GitOps for configuration

### API Usage Patterns

- **kubectl**: Command-line administration
- **Kubernetes Client Libraries**: Programmatic access
- **REST API**: HTTP API for automation
- **CRUD Operations**: Standard create, read, update, delete

### Observability Best Practices

- **Metrics Collection**: Prometheus metrics
- **Logging**: Structured logging
- **Tracing**: Distributed tracing
- **Dashboards**: Grafana dashboards

### Development Workflow

- **Local Testing**: Kind or Minikube for development
- **Testing**: Integration tests
- **Debugging**: Debug logs and diagnostics
- **CI/CD**: Automated testing and deployment
- **Tools**: kubectl, Helm, kustomize

### Code Examples

```yaml
# Example configuration for etcd
apiVersion: cncf.etcd/v1
kind: Etcd
metadata:
  name: example
  namespace: default
spec:
  # Configuration details
  replicas: 3
  resources:
    requests:
      memory: "256Mi"
      cpu: "250m"
    limits:
      memory: "512Mi"
      cpu: "500m"
```

  related-skills: null

## Fundamentals

### Essential Concepts

- **Resource**: Core abstraction managed by etcd
- **Reconciliation**: Process of achieving desired state
- **Controller**: Component managing resources
- **Webhook**: Admission control mechanism
- **CRD**: Custom Resource Definition
- **Operator**: Pattern for managing complex applications
- **Status**: Current state of the resource

### Terminology Glossary

- **Controller**: Management component
- **Reconciler**: State reconciliation logic
- **CRD**: Custom Resource Definition
- **Webhook**: Admission webhook
- **Operator**: Application operator pattern
- **Reconciliation**: State synchronization

### Data Models and Types

- **Custom Resource**: User-defined resource type
- **Status**: Resource status information
- **Spec**: Desired state specification
- **Owner Reference**: Resource ownership chain

### Lifecycle Management

- **Resource Lifecycle**: Create → Configure → Deploy → Update → Delete
- **Controller Lifecycle**: Start → Watch → Reconcile → Stop
- **Upgrade Lifecycle**: Backup → Upgrade → Verify → Rollback (if needed)

### State Management

- **Desired State**: Spec field in resource
- **Current State**: Status field in resource
- **Reconciliation Loop**: Controller loop for state sync
- **Event Queue**: Change event processing

---

## Scaling and Deployment Patterns

### Horizontal Scaling

- **Controller Scaling**: Multiple controller replicas
- **Worker Scaling**: Scale worker pods based on load
- **API Server Scaling**: Scale API servers
- **Storage Scaling**: Add storage capacity

### High Availability

- **Controller HA**: Multiple controller replicas
- **Storage HA**: HA storage backend
- **Load Balancing**: Distribute traffic
- **Multi-Region**: Geographic distribution

### Production Deployments

- **Standalone**: Single instance deployment
- **HA**: High availability deployment
- **Clustered**: Multi-node cluster
- **Resource Configuration**: CPU, memory, storage limits

### Upgrade Strategies

- **Rolling Update**: Update without downtime
- **Blue-Green**: Blue-green deployments
- **Canary**: Canary releases
- **Version Compatibility**: Follow upgrade path

### Resource Management

- **CPU/Memory Requests**: Appropriate resource requests
- **Limits**: Resource limits for stability
- **Storage Quotas**: Storage allocation
- **Network Bandwidth**: Network resource allocation

### Deployment Patterns

- **DaemonSet**: One instance per node
- **Deployment**: Standard deployment
- **StatefulSet**: Stateful applications
- **Helm Chart**: Chart-based deployment
- **Operator Pattern**: Operator-based management

---

## Additional Resources

- **Official Documentation:** [https://etcd.io/](https://etcd.io/)
- **GitHub Repository:** [github.com/cncf/etcd](https://github.com/cncf/etcd)
- **CNCF Project Page:** [cncf.io/projects/etcd/](https://www.cncf.io/projects/etcd/)
- **Community:** Check the GitHub repository for community channels
- **Versioning:** Refer to project's release notes for version-specific features

---

## Examples

### Single Node Cluster

```yaml
# Single node etcd configuration
etcd --name=single-node   --data-dir=/var/lib/etcd   --listen-client-urls=https://0.0.0.0:2379   --advertise-client-urls=https://127.0.0.1:2379   --listen-peer-urls=https://0.0.0.0:2380   --client-cert-auth=true   --auto-tls=true   --peer-client-cert-auth=true   --peer-auto-tls=true

# With configuration file
etcd --config=/etc/etcd/etcd.conf.yml
```

### Three Node Cluster

```yaml
# Node 1
etcd --name=etcd1   --data-dir=/var/lib/etcd   --initial-advertise-peer-urls=https://10.0.0.1:2380   --listen-peer-urls=https://10.0.0.1:2380   --listen-client-urls=https://10.0.0.1:2379,https://127.0.0.1:2379   --advertise-client-urls=https://10.0.0.1:2379   --initial-cluster=etcd1=https://10.0.0.1:2380,etcd2=https://10.0.0.2:2380,etcd3=https://10.0.0.3:2380   --initial-cluster-token=etcd-cluster-secure-token   --initial-cluster-state=new   --client-cert-auth=true   --peer-client-cert-auth=true

# Node 2 and 3 similar with different IP addresses
```

### Kubernetes Integrated etcd

```yaml
# etcd configuration for Kubernetes
apiVersion: v1
kind: Pod
metadata:
  name: etcd
  namespace: kube-system
spec:
  containers:
  - name: etcd
    image: k8s.gcr.io/etcd:3.5.9-0
    command:
    - etcd
    - --data-dir=/var/lib/etcd
    - --name=etcd0
    - --initial-advertise-peer-urls=https://10.0.0.1:2380
    - --listen-peer-urls=https://0.0.0.0:2380
    - --listen-client-urls=https://0.0.0.0:2379
    - --advertise-client-urls=https://10.0.0.1:2379
    - --initial-cluster=etcd0=https://10.0.0.1:2380,etcd1=https://10.0.0.2:2380,etcd2=https://10.0.0.3:2380
    - --initial-cluster-token=k8s-etcd-cluster-token
    - --initial-cluster-state=new
    - --client-cert-auth=true
    - --peer-client-cert-auth=true
    - --auto-tls=true
    - --peer-auto-tls=true
    volumeMounts:
    - mountPath: /var/lib/etcd
      name: etcd-data
    - mountPath: /etc/ssl/certs
      name: certs
  hostNetwork: true
  volumes:
  - name: etcd-data
    hostPath:
      path: /var/lib/etcd
  - name: certs
    hostPath:
      path: /etc/ssl/certs
```

## Troubleshooting

### etcd cluster health check failing

**Cause:** Network connectivity issues or member failures

**Solution:**

```bash
# Check cluster health
etcdctl endpoint health --endpoints=https://127.0.0.1:2379   --cacert=/etc/etcd/pki/ca.crt   --cert=/etc/etcd/pki/etcd.crt   --key=/etc/etcd/pki/etcd.key

# List members
etcdctl member list --endpoints=https://127.0.0.1:2379   --cacert=/etc/etcd/pki/ca.crt   --cert=/etc/etcd/pki/etcd.crt   --key=/etc/etcd/pki/etcd.key

# Remove failed member
etcdctl member remove <member-id> --endpoints=https://127.0.0.1:2379
```

### etcd disk space exhaustion

**Cause:** Write operations without compaction or retention

**Solution:**

```bash
# Check current database size
etcdctl endpoint status --endpoints=https://127.0.0.1:2379 -w table

# Compact old revisions
etcdctl compact <rev>

# Defragment database
etcdctl defrag --endpoints=https://127.0.0.1:2379

# Set auto-compaction
etcd --auto-compaction-version=3 --auto-compaction-mode=periodic --auto-compaction-retention=1h
```

### Leader election stuck or slow

**Cause:** Network latency or resource constraints

**Solution:**

```bash
# Check leader
etcdctl endpoint status --endpoints=https://127.0.0.1:2379 -w table

# Adjust election timeout (advanced)
# In configuration, increase election-timeout if high latency
--election-timeout=5000 --heartbeat-interval=500

# Ensure adequate resources
# etcd needs consistent I/O performance
```

### Member not syncing with cluster

**Cause:** Network partition or data inconsistency

**Solution:**

```bash
# Remove and re-add member
etcdctl member remove <member-id> --endpoints=https://127.0.0.1:2379

# On the failed node, clear data
rm -rf /var/lib/etcd

# Re-add as new member
etcd --name=<new-name> --initial-cluster-state=existing ...

# Or use etcdctl member add
etcdctl member add <new-name> --peer-urls=https://<ip>:2380
```

### TLS certificate validation failures

**Cause:** Certificate expiration or misconfiguration

**Solution:**

```bash
# Check certificate expiration
openssl x509 -in /etc/etcd/pki/etcd.crt -noout -dates

# Renew certificates before expiration
# Update all members with new certs

# Verify client certs
etcdctl endpoint health --endpoints=https://127.0.0.1:2379   --cacert=/etc/etcd/pki/ca.crt   --cert=/etc/etcd/pki/admin.crt   --key=/etc/etcd/pki/admin.key
```
*Content generated automatically. Verify against official documentation before production use.*

## Troubleshooting

### Deployment failures

**Cause:** Configuration errors or resource constraints

**Solution:** Check pod logs with `kubectl logs <pod>`, verify configuration values, and ensure adequate cluster resources.


### Performance issues

**Cause:** Resource limits or configuration bottlenecks

**Solution:** Monitor resource usage with `kubectl top`, adjust resource limits, and optimize configuration settings.


### Configuration errors

**Cause:** YAML syntax or missing required fields

**Solution:** Validate YAML syntax, check required configuration fields, and verify environment-specific settings.


### Integration problems

**Cause:** API compatibility or version mismatches

**Solution:** Verify API compatibility, check dependency versions, and review integration documentation.


### Connectivity issues

**Cause:** Network policies or service discovery problems

**Solution:** Check network policies, verify service endpoints, and ensure proper DNS resolution.

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

---

## Live References

> **These links are resolved at load time** — content is fetched and inlined to provide the latest documentation.

- [etcd Documentation](https://etcd.io/docs/)
- [etcd Operations Guide](https://etcd.io/docs/latest/op-guide/)
- [etcd API Reference](https://etcd.io/docs/latest/learning/api/)
- [etcd Security Model](https://etcd.io/docs/latest/op-guide/security/)
- [etcd Performance Tuning](https://etcd.io/docs/latest/tuning/)
- [etcd Disaster Recovery](https://etcd.io/docs/latest/op-guide/recovery/)
