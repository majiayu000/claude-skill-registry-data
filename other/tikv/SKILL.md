---




name: tikv
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '"TiKV in Distributed transactional key-value database inspired by Google"
  Spanner'
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  role: reference
  scope: infrastructure
  triggers: distributed, key-value, tikv, transactional
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




  related-skills: cncf-aws-dynamodb, cncf-aws-ecr, cncf-aws-rds, cncf-aws-s3


# TiKV in Cloud-Native Engineering

**Category:** Database  
**Status:** Active  
**Stars:** 10,000  
**Last Updated:** 2026-04-22  
**Primary Language:** Rust  
**Documentation:** [Distributed transactional key-value database inspired by Google Spanner](https://tikv.org/docs/)  

---

## Purpose and Use Cases

TiKV is a core component of the cloud-native ecosystem, serving as Google Spanner

### What Problem Does It Solve?

TiKV addresses the challenge of distributed transactional key-value storage with strong consistency. It provides horizontal scalability, ACID transactions, and cloud-native architecture.

### When to Use This Project

Use TiKV when need distributed storage, require strong consistency, or manage large-scale data. Not ideal for simple deployments or when distributed database requirements, transactional workloads, or horizontal scaling needs.

### Key Use Cases

- Distributed Database Storage
- Transaction Processing
- High Availability Storage
- Multi-Region Deployments
- Hybrid Cloud Storage

---

## Architecture Design Patterns

### Core Components

- **PD**: Placement Driver for cluster management
- **TiKV Node**: Storage node
- **Raft**: Consensus protocol
- **Transaction**: Transaction engine
- **Region**: Data partition unit

### Component Interactions

1. **Client → TiKV**: Client reads/writes to TiKV
1. **TiKV → PD**: PD manages region distribution
1. **TiKV → TiKV**: Raft replication between nodes
1. **PD → TiKV**: PD schedules regions

### Data Flow Patterns

1. **Write Flow**: Client writes → Raft leader → Raft followers → Ack → Response
1. **Read Flow**: Client reads → Raft leader → Response (or follower)
1. **Region Split**: Region grows → Split → New regions
1. **Region Balance**: PD schedules → Region moved → Balance restored

### Design Principles

- **Consistency**: Strong consistency with Raft
- **Scalability**: Horizontal scalability
- **Availability**: High availability with replication
- **Transaction Support**: ACID transactions

---

## Integration Approaches

### Integration with Other CNCF Projects

- **TiDB**: SQL layer
- **TiFlash**: Columnar storage
- **TiCDC**: Change data capture
- **PD**: Placement Driver

### API Patterns

- **KV API**: Key-value operations
- **PD API**: Cluster management API
- **Raft API**: Raft consensus API
- **Transaction API**: Transaction operations

### Configuration Patterns

- **TiKV Config**: TiKV configuration
- **PD Config**: Placement Driver config
- **Raft Config**: Raft configuration
- **Transaction Config**: Transaction settings

### Extension Mechanisms

- **Custom Storage Engines**: Add storage engines
- **Custom PD Schedulers**: Custom scheduling logic
- **Custom Transaction Logic**: Custom transaction handling

---

## Common Pitfalls and How to Avoid Them

### Misconfigurations

- **Disk Space**: Disk space exhaustion
  - **How to Avoid**: Monitor disk space, configure disk quota, add nodes
- **Replication Issues**: Replication lag
  - **How to Avoid**: Monitor replication, check network, tune settings

### Performance Issues

- **Raft Issues**: Raft consensus problems
  - **How to Avoid**: Monitor Raft health, check node availability
- **PD Issues**: PD cluster problems
  - **How to Avoid**: Monitor PD health, scale PD cluster

### Operational Challenges

- **Memory Pressure**: High memory usage
  - **How to Avoid**: Configure memory limits, tune cache settings
- **Upgrade Issues**: Upgrade failures
  - **How to Avoid**: Test upgrades, follow upgrade path

### Security Pitfalls


---

## Coding Practices

### Idiomatic Configuration

- **Transaction Design**: Design efficient transactions
- **Key Design**: Design keys for even distribution
- **Region Management**: Manage region size

### API Usage Patterns

- **tikv-ctl**: TiKV control utility
- **KV API**: Key-value operations
- **PD API**: PD management API
- **gRPC**: TiKV gRPC API

### Observability Best Practices

- **TiKV Metrics**: Monitor TiKV performance
- **PD Metrics**: Monitor PD health
- **Raft Metrics**: Track Raft operations

### Testing Strategies

- **Integration Tests**: Test TiKV functionality
- **Failover Tests**: Test cluster failover
- **Performance Tests**: Validate performance

### Development Workflow

- **Local Development**: Use tikv-server locally
- **Debug Commands**: Check TiKV and PD logs
- **Test Environment**: Set up test cluster
- **CI/CD Integration**: Automate testing
- **Monitoring Setup**: Configure observability
- **Documentation**: Maintain documentation

---

## Fundamentals

### Essential Concepts

- **Region**: Data partition unit
- **Raft Group**: Replica group
- **PD**: Placement Driver
- **Transaction**: Transaction engine
- ** MVCC**: Multi-version concurrency control
- **Lock**: Lock mechanism
- **Write Batch**: Batch write operations
- **Snapshot**: Snapshot isolation

### Terminology Glossary

- **Region**: Data partition
- **Raft Group**: Replica group
- **PD**: Placement Driver
- **Transaction**: Transaction engine
- **MVCC**: Multi-version concurrency control

### Data Models and Types

- **Region**: Data partition
- **Raft Log**: Raft log entries
- **Write Batch**: Batch write data
- **Transaction State**: Transaction state

### Lifecycle Management

- **Write Flow**: Client writes → Raft leader → Replicate → Response
- **Read Flow**: Client reads → Read from leader or follower
- **Region Split**: Region grows → Split → New regions created
- **Region Balance**: PD schedules → Region moved → Balance restored

### State Management

- **Region State**: Available, splitting, or merging
- **Replica State**: Leader, follower, or learner
- **Transaction State**: Active, committed, or aborted
- **PD State**: Leader, follower, or offline

---

## Scaling and Deployment Patterns

### Horizontal Scaling

- **Region Scaling**: Split regions as data grows
- **Node Scaling**: Add TiKV nodes
- **PD Scaling**: Scale PD cluster
- **Replica Scaling**: Adjust replica count

### High Availability

- **Region HA**: Multiple replicas per region
- **Raft HA**: Raft consensus with quorum
- **PD HA**: PD cluster with leader election
- **Node HA**: Distribute regions across nodes

### Production Deployments

- **Cluster Setup**: Deploy TiKV cluster
- **Network Configuration**: Configure network
- **Security Setup**: Enable TLS, authentication
- **Monitoring Setup**: Configure metrics
- **Logging Setup**: Centralize logs
- **Backup Strategy**: Configure backups
- **Resource Quotas**: Set resource limits
- **Performance Tuning**: Optimize settings

### Upgrade Strategies

- **TiKV Upgrade**: Upgrade TiKV nodes
- **PD Upgrade**: Upgrade PD cluster
- **Rolling Upgrade**: Rolling node upgrade
- **Testing**: Verify functionality

### Resource Management

- **CPU Resources**: CPU limits
- **Memory Resources**: Memory limits
- **Storage Resources**: Storage configuration
- **Network Resources**: Network configuration

---

## Additional Resources

- **Official Documentation:** https://tikv.org/docs/
- **GitHub Repository:** Check the project's official documentation for repository link
- **CNCF Project Page:** [cncf.io/projects/cncf-tikv/](https://www.cncf.io/projects/cncf-tikv/)
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

### TiKV Cluster Configuration


```yaml
# TiKV configuration for a production cluster
[tikv]
# Server configuration
addr = "192.168.1.101:20160"
advertise-addr = "192.168.1.101:20160"
status-addr = "192.168.1.101:20180"

# PD configuration
pd-endpoints = ["192.168.1.101:2379","192.168.1.102:2379","192.168.1.103:2379"]

# Storage configuration
storage.data-dir = "/data/tikv"
storage.engine-addr = "192.168.1.101:20160"
storage.block-cache.capacity = "8GB"

# Logging configuration
log-level = "info"
log-file = "/var/log/tikv/tikv.log"

# Coprocessor configuration
coprocessor.split-region-on-table = true
coprocessor.batch-split-limit = 10
coprocessor.region-max-size = "96MB"
coprocessor.region-split-size = "64MB"
```

### TiKV with TiFlash Configuration


```yaml
# TiKV configuration with TiFlash replication
[tikv]
addr = "192.168.1.101:20160"
advertise-addr = "192.168.1.101:20160"
status-addr = "192.168.1.101:20180"

pd-endpoints = ["192.168.1.101:2379"]

storage.data-dir = "/data/tikv"
storage.engine-addr = "192.168.1.101:20160"

[server]
engine-addr = "192.168.1.101:20160"
status-addr = "192.168.1.101:20180"
tidb-status-addr = "192.168.1.101:10080"

[raftstore]
apply-pool-size = 4
store-pool-size = 4
raft-entry-max-size = 8
raft-snapshot-count = 10000

[coprocessor]
region-max-keys = 100000
region-split-keys = 50000
```

### TiKV Backup and Restore Configuration


```yaml
# TiKV backup configuration for BR (Backup & Restore)
[br]
# Backup configuration
backup-concurrency = 16
checksum-concurrency = 4
send-credentials-to-tikv = true
send-stores-to-tikv = true

[restore]
# Restore configuration
restore-concurrency = 16
data-concurrency = 4
index-concurrency = 4
region-merge-concurrency = 4

[pd]
pd-endpoints = ["192.168.1.101:2379"]

[tikv]
# Ensure sufficient resources for backup/restore
storage.write-thread-num = 4
storage.backup-thread-num = 4
coprocessorThreadPoolSize = 4
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
