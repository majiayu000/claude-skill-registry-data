---




name: opencost
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '"OpenCost in Kubernetes Cost Monitoring - cloud native architecture,
  patterns" pitfalls, and best practices'
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  related-skills: argo, artifact-hub, aws-cloudwatch, aws-eks
  role: reference
  scope: infrastructure
  triggers: cdn, container orchestration, infrastructure as code, k8s, monitoring,
    opencost, cloudformation, cloudfront
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




# OpenCost in Cloud-Native Engineering

**Category:** observability  
**Status:** Sandbox  
**Stars:** 4,900  
**Last Updated:** 2026-04-22  
**Primary Language:** Go  
**Documentation:** [https://opencost.io/](https://opencost.io/)  

---

## Purpose and Use Cases

### What Problem Does It Solve?

OpenCost addresses the challenge of understanding and managing Kubernetes cluster costs. Traditional cost monitoring tools focus on cloud billing rather than actual Kubernetes resource consumption, making it difficult to identify cost outliers, optimize resource allocation, or attribute costs to specific teams or applications. OpenCost provides accurate, real-time Kubernetes cost data that integrates seamlessly with existing observability tooling.

### When to Use This Project

Use OpenCost when you need:
- Real-time Kubernetes cost monitoring
- Cost attribution to namespaces, pods, or teams
- Idle resource identification and cost optimization
- Integration with Prometheus for cost-based alerting
- Cost data alongside existing metrics and logs
- Historical cost analysis and forecasting

### Key Use Cases

- **Team Cost Attribution**: Assign costs to specific teams or departments
- **Cluster Optimization**: Identify underutilized nodes and right-size
- **Budget Tracking**: Monitor cluster costs against budget
- **Anomaly Detection**: Alert on unexpected cost spikes
- **Investment ROI**: Measure the value of infrastructure investments
- **Multi-Cluster Cost**: Aggregate costs across multiple clusters

---

## Architecture Design Patterns

### Core Components

- **Cost Metrics Exporter**: Exposes Kubernetes cost metrics in Prometheus format
- **Cluster Cost Model**: Calculates costs based on cluster resources
- **Cloud Provider Connector**: Integrates with cloud APIs for pricing data
- **Storage Backend**: Stores historical cost data
- **Prometheus Integration**: Metrics scraping and querying
- **UI/Dashboard**: Visual representation of cost data
- **Cost API**: REST API for programmatic cost queries

### Component Interactions

1. **Metrics Exporter → Prometheus**: Expose cost metrics for scraping
2. **Cost Model → Cloud Provider API**: Fetch current pricing data
3. **Cluster Data → Cost Model**: Get resource utilization data
4. **Prometheus → Cost Dashboard**: Query cost metrics for visualization
5. **API Server → Cost Model**: Handle cost data queries
6. **Webhook → Prometheus**: Event notifications for cost thresholds

### Data Flow Patterns

1. **Cost Calculation**: Resource usage → Pricing data → Cost calculation → Metrics export
2. **Metric Collection**: Prometheus scrape → Cost metrics → Dashboard query → Visualization
3. **Historical Storage**: Metrics → Long-term storage → Trend analysis → Reporting
4. **Allocation**: Pod/namespace → Resource usage → Cost allocation → Attribution

### Design Principles

- **Prometheus-Native**: First-class Prometheus metrics support
- **Accurate Pricing**: Real-time cloud pricing integration
- **Detailed Attribution**: Break down costs to pod level
- **Low Overhead**: Minimal performance impact on cluster
- **Flexible Storage**: Support for various storage backends
- **Open Standard**: Use standard Prometheus metric naming conventions

---

## Integration Approaches

### Integration with Other CNCF Projects

- **Prometheus**: Primary metrics collection and storage
- **Grafana**: Pre-built dashboards for cost visualization
- **Kubernetes**: Access cluster resource data via API
- **Prometheus Operator**: Automate cost metrics scraping
- **Loki**: Combine cost with log analysis
- **Velero**: Track backup costs
- **Helm**: Deploy cost monitoring via Helm chart

### API Patterns

- **Prometheus Metrics**: Standard Prometheus format for scraping
- **Cost API**: REST API for programmatic cost queries
- **Allocation API**: Query cost allocations by namespace, pod, etc.
- **Webhook**: Event notifications for cost thresholds

### Configuration Patterns

- **Prometheus Scraping**: Configure Prometheus to scrape cost metrics
- **Cloud Provider**: Configure cloud provider for pricing data
- **Cost Model**: Customize cost calculation parameters
- **Label Mapping**: Map Kubernetes labels to cost attributes

### Extension Mechanisms

- **Custom Pricing**: Support for non-standard pricing models
- **Custom Labels**: Extend label-based cost attribution
- **Storage Backends**: Add support for additional storage systems
- **Alerting Integrations**: Extend alerting to additional platforms

---

## Common Pitfalls and How to Avoid Them

### Configuration Issues

- **Cloud Provider Credentials**: Ensure proper access to cloud pricing APIs
- **Label Mapping**: Configure label mapping for accurate cost attribution
- **Time Range Alignment**: Align cost data with billing cycles
- **Metric Naming**: Use standard metric names for compatibility

### Performance Issues

- **Scraping Overhead**: Monitor Prometheus scraping performance
- **API Rate Limits**: Respect cloud provider API rate limits
- **Data Retention**: Balance data retention with storage costs
- **Query Performance**: Optimize queries for large cluster environments

### Operational Challenges

- **Cost Data Accuracy**: Verify cost calculations match billing
- **Data Gaps**: Implement data backup and recovery
- **Version Updates**: Test cost model updates before production
- **Multi-Cluster**: Coordinate cost data across clusters

### Security Pitfalls

- **Cloud Credentials**: Store cloud credentials securely in Kubernetes secrets
- **Access Control**: Restrict access to cost data
- **Audit Logging**: Enable audit logging for compliance

---

## Coding Practices

### Idiomatic Configuration

- **Prometheus Rules**: Use standard Prometheus rule format
- **Cloud Provider YAML**: Declarative cloud configuration
- **Cost Model Settings**: Custom cost calculation parameters
- **Label Configuration**: Kubernetes label to cost attribution mapping

### API Usage Patterns

- **Prometheus Queries**: Query cost metrics for dashboards
- **REST API Calls**: Integrate cost API into applications
- **Allocation Queries**: Calculate costs by namespace, pod, or team
- **Alerting Rules**: Create alerting rules based on cost metrics

### Observability Best Practices

- **Cost Metrics**: Monitor cluster costs alongside existing metrics
- **Alerting**: Set up alerts for cost anomalies and thresholds
- **Dashboard**: Use Grafana dashboards for cost visualization
- **Audit Trail**: Log all cost data access and modifications

### Development Workflow

- **Local Testing**: Test cost calculation locally first
- **Staging Environment**: Verify cost attribution in staging
- **CI/CD Integration**: Monitor deployment costs in CI/CD
- **Rollback Plans**: Test recovery from configuration errors

---

## Fundamentals

### Essential Concepts

- **Cost Attribution**: Assigning costs to specific Kubernetes resources
- **Prometheus Metrics**: Cost data in standard Prometheus format
- **Cloud Pricing**: Real-time pricing data from cloud providers
- **Resource Utilization**: CPU, memory, storage usage metrics
- **Namespace Allocation**: Cost attribution by Kubernetes namespace
- **Idle Resources**: Underutilized resources identified for optimization

### Terminology Glossary

- **Cost Attribution**: Assigning costs to specific resources
- **Namespace Allocation**: Cost breakdown by namespace
- **Pod-Level Cost**: Individual pod cost calculation
- **Idle Resource**: Underutilized node or resource
- **Cost Model**: Calculation method for Kubernetes costs
- **Cloud Connector**: Integration with cloud provider APIs
- **Prometheus Query**: Query cost metrics using PromQL

### Data Models and Types

- **Cost Metric**: Kubernetes resource cost over time
- **Allocation**: Cost breakdown by namespace, pod, or label
- **Pricing Data**: Cloud provider pricing information
- **Resource Usage**: CPU, memory, storage utilization

### Lifecycle Management

- **Metrics Lifecycle**: Collection → Calculation → Export → Query → Visualization
- **Cost Attribution Lifecycle**: Resource usage → Pricing → Allocation → Reporting
- **Data Retention**: Short-term → Long-term storage → Archive

### State Management

- **Cost State**: Current cost data, historical data, predictions
- **Resource State**: CPU, memory, storage utilization metrics
- **Pricing State**: Current pricing data from cloud provider

---

## Scaling and Deployment Patterns

### Horizontal Scaling

- **Prometheus Scaling**: Scale Prometheus for large cluster environments
- **Cost Metrics Exporter**: Scale for high-cardinality metrics
- **Storage**: Scale storage for historical cost data

### High Availability

- **Prometheus HA**: Deploy Prometheus in HA mode
- **Cost Metrics**: Ensure metrics are available during failures
- **Data Backup**: Regular backup of historical cost data
- **Multi-Cluster**: Coordinate cost data across clusters

### Production Deployments

- **Production Metrics**: Deploy cost metrics with production-grade Prometheus
- **Dashboard**: Deploy Grafana dashboards for cost visualization
- **Alerting**: Set up alerting for cost thresholds
- **Monitoring**: Monitor cost metrics for anomalies

### Upgrade Strategies

- **Minor Version**: In-place upgrade with metric compatibility
- **Major Version**: Test cost model changes before deployment
- **Data Migration**: Plan for historical data migration
- **Rollback Plan**: Keep previous version available

### Resource Management

- **Prometheus Storage**: Monitor and manage Prometheus storage
- **Cost Metrics**: Monitor cost metric cardinality
- **API Usage**: Monitor cloud provider API usage
- **Network**: Monitor network traffic for cost data

---

## Additional Resources

- **Official Documentation:** [https://opencost.io/docs/](https://opencost.io/docs/)
- **GitHub Repository:** [github.com/kubecost/cost-model](https://github.com/kubecost/cost-model)
- **CNCF Project Page:** [cncf.io/projects/opencost/](https://www.cncf.io/projects/opencost/)
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
