---




name: vitess
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '"Provides Vitess in Database clustering system for horizontal scaling
  of MySQL"'
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  role: reference
  scope: infrastructure
  triggers: clustering, system, vitess
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


# Vitess in Cloud-Native Engineering

**Category:** Database  
**Status:** Active  
**Stars:** 10,000  
**Last Updated:** 2026-04-22  
**Primary Language:** Go  
**Documentation:** [Database clustering system for horizontal scaling of MySQL](https://vitess.io/docs/)  

---

## Purpose and Use Cases

Vitess is a core component of the cloud-native ecosystem, serving as of MySQL

### What Problem Does It Solve?

Vitess addresses the challenge of horizontal scaling of MySQL for large-scale deployments. It provides MySQL compatibility, horizontal scaling, and high availability.

### When to Use This Project

Use Vitess when need MySQL scaling, require high availability, or manage large datasets. Not ideal for simple deployments or when MySQL horizontal scaling, sharding requirements, or large-scale deployments.

### Key Use Cases

- MySQL Horizontal Scaling
- Database Sharding
- High Availability MySQL
- Multi-Region Deployments
- Cloud-Native MySQL

---

## Architecture Design Patterns

### Core Components

- **VTGate**: Query routing layer
- **VTTablet**: MySQL wrapper
- **VTController**: Cluster management
- **Keyspace**: Logical database
- **Shard**: Data partition

### Component Interactions

1. **Client → VTGate**: Client queries VTGate
1. **VTGate → VTTablet**: VTGate routes to tablets
1. **VTTablet → MySQL**: VTTablet manages MySQL
1. **VTController → VTTablet**: VTController manages tablets

### Data Flow Patterns

1. **Query Routing**: Query → VTGate → VTTablet → MySQL
1. **Shard Placement**: Keyspace → Shard → VTTablet → MySQL
1. **Replication**: MySQL master → MySQL replicas
1. **Failsafe**: VTTablet detects failure → Promote replica

### Design Principles

- **MySQL Compatible**: Full MySQL protocol
- **Horizontal Scaling**: Shard and scale
- **High Availability**: Automatic failover
- **Operational Simplicity**: Easy to operate

---

## Integration Approaches

### Integration with Other CNCF Projects

- **MySQL**: Primary database
- **Kubernetes**: Deployment platform
- **Vitess Operator**: Kubernetes operator
- **Prometheus**: Metrics collection

### API Patterns

- **MySQL Protocol**: MySQL client protocol
- **VTGate Protocol**: VTGate internal protocol
- **VTTablet API**: Tablet management API
- **Keyspace API**: Keyspace management API

### Configuration Patterns

- **VTGate Config**: VTGate configuration
- **VTTablet Config**: Tablet configuration
- **Keyspace Config**: Keyspace configuration
- **Shard Config**: Shard settings

### Extension Mechanisms

- **Custom Sharding**: Custom sharding logic
- **Custom Replication**: Custom replication logic
- **Custom VTGate Plugins**: Custom query routing

---

## Common Pitfalls and How to Avoid Them

### Misconfigurations

- **Shard Split**: Shard split failures
  - **How to Avoid**: Monitor shard splits, use proper tools
- **VTGate Memory**: VTGate high memory usage
  - **How to Avoid**: Configure memory limits, optimize queries

### Performance Issues

- **Schema Changes**: Schema change issues
  - **How to Avoid**: Use Vitess schema management, test changes
- **VTTablet Issues**: Tablet health issues
  - **How to Avoid**: Monitor tablet health, check MySQL status

### Operational Challenges

- **Performance Issues**: Query performance
  - **How to Avoid**: Optimize queries, add indexes, monitor slow queries
- **Failover Issues**: Failover problems
  - **How to Avoid**: Test failover, verify replica health

### Security Pitfalls


---

## Coding Practices

### Idiomatic Configuration

- **Shard Key Design**: Design efficient shard keys
- **Schema Management**: Use Vitess schema management
- **Connection Management**: Manage connections efficiently

### API Usage Patterns

- **vtctl**: Vitess control utility
- **mysql client**: MySQL protocol client
- **VTGate API**: VTGate API
- **Vitess Operator**: Kubernetes operator

### Observability Best Practices

- **Vitess Metrics**: Monitor Vitess performance
- **MySQL Metrics**: MySQL performance metrics
- **Replication Metrics**: Track replication health

### Testing Strategies

- **Integration Tests**: Test Vitess functionality
- **Failover Tests**: Test failover scenarios
- **Performance Tests**: Validate performance

### Development Workflow

- **Local Development**: Use vitess local cluster
- **Debug Commands**: Check VTGate and tablet logs
- **Test Environment**: Set up test cluster
- **CI/CD Integration**: Automate testing
- **Monitoring Setup**: Configure observability
- **Documentation**: Maintain documentation

---

## Fundamentals

### Essential Concepts

- **Keyspace**: Logical database
- **Shard**: Data partition
- **VTGate**: Query router
- **VTTablet**: MySQL wrapper
- **Replication**: MySQL replication
- **Failsafe**: Automatic failover
- **Topology Service**: Cluster state storage
- **VSchema**: Sharding schema

### Terminology Glossary

- **Keyspace**: Logical database
- **Shard**: Data partition
- **VTGate**: Query router
- **VTTablet**: Tablet
- **Failsafe**: Failover mechanism

### Data Models and Types

- **Keyspace**: Keyspace configuration
- **Shard**: Shard configuration
- **VSchema**: Sharding schema
- **Tablet**: Tablet state

### Lifecycle Management

- **Query Flow**: Client queries → VTGate → VTTablet → MySQL
- **Shard Split**: Split initiated → New shards → Data copied → Cutover
- **Failover**: Failure detected → Replica promoted → Traffic routed
- **Upgrade**: Rolling upgrade → New version

### State Management

- **Keyspace State**: Available, splitting, or merging
- **Shard State**: Primary, replica, or spares
- **VTTablet State**: Master, replica, or spare
- **VTGate State**: Healthy or degraded

---

## Scaling and Deployment Patterns

### Horizontal Scaling

- **Shard Scaling**: Add shards for more capacity
- **VTGate Scaling**: Scale VTGate instances
- **Replica Scaling**: Add replicas for read scale
- **MySQL Scaling**: Scale MySQL instances

### High Availability

- **Shard HA**: Multiple replicas per shard
- **VTTablet HA**: Tablet failover
- **VTGate HA**: VTGate cluster
- **MySQL HA**: MySQL replication

### Production Deployments

- **Cluster Setup**: Deploy Vitess cluster
- **Network Configuration**: Configure network
- **Security Setup**: Enable authentication
- **Monitoring Setup**: Configure metrics
- **Logging Setup**: Centralize logs
- **Backup Strategy**: Configure backups
- **Resource Quotas**: Set resource limits
- **Performance Tuning**: Optimize settings

### Upgrade Strategies

- **Vitess Upgrade**: Upgrade Vitess components
- **MySQL Upgrade**: Upgrade MySQL version
- **Rolling Upgrade**: Rolling component upgrade
- **Testing**: Verify functionality

### Resource Management

- **CPU Resources**: CPU limits
- **Memory Resources**: Memory limits
- **Storage Resources**: MySQL storage
- **Network Resources**: Network configuration

---

## Additional Resources

- **Official Documentation:** https://vitess.io/docs/
- **GitHub Repository:** Check the project's official documentation for repository link
- **CNCF Project Page:** [cncf.io/projects/cncf-vitess/](https://www.cncf.io/projects/cncf-vitess/)
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

### Vitess Keyspace Configuration


```yaml
# Vitess keyspace configuration for a sharded database
{
  "keyspace": {
    "name": "commerce",
    "sharding_column_name": "user_id",
    "sharding_column_type": "INT64",
    "served_froms": [
      {
        "cell": "zone1",
        "type": "BACKUP"
      }
    ]
  },
  "vindexes": {
    "hash": {
      "type": "hash"
    },
    "numeric": {
      "type": "numeric"
    }
  },
  "tables": {
    "users": {
      "column_vindexes": [
        {
          "column": "user_id",
          "name": "hash"
        }
      ]
    },
    "orders": {
      "column_vindexes": [
        {
          "column": "order_id",
          "name": "numeric"
        }
      ]
    }
  }
}
```

### Vitens VTGate Configuration


```yaml
# VTGate configuration for connection routing
vtgate:
  port: 15001
  grpc-port: 15000
  auth-module: none
  cell: zone1
  root-zone: zone1
  enable-gtids: true
  enable-partial-route: true
  enable-planning-trace: true
  tablet-layout-timeout: 1m
  tablet-layout-refresh: 10s
  query-cache-size: 10000
  query-log-sampling-rate: 1
  stream-pool-size: 100
  enable-separate-cache: true
  enable-native-sharding: true
  enable-pkid-sharding: true
```

### Vitess VSchema Example


```yaml
{
  "commerce": {
    "sharded": true,
    "vindexes": {
      "hash": {
        "type": "hash"
      }
    },
    "tables": {
      "users": {
        "column_vindexes": [
          {
            "column": "user_id",
            "name": "hash"
          }
        ],
        "auto_increment": {
          "column": "user_id",
          "type": "VTAUTO"
        }
      },
      "products": {
        "column_vindexes": [
          {
            "column": "product_id",
            "name": "hash"
          }
        ]
      },
      "orders": {
        "column_vindexes": [
          {
            "column": "order_id",
            "name": "hash"
          }
        ],
        "column_vindexes": [
          {
            "column": "user_id",
            "name": "hash"
          }
        ]
      }
    }
  }
}
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
