---




name: cilium
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '"Cilium in Cloud Native Network - cloud native architecture, patterns"
  pitfalls, and best practices'
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  related-skills: calico, container-network-interface-cni, contour, kong
  role: reference
  scope: infrastructure
  triggers: cdn, cilium, infrastructure as code, monitoring, native, network, cloudformation,
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




 # Cilium in Cloud-Native Engineering

**Category:** network  
**Status:** Active  
**Stars:** 24,186  
**Last Updated:** 2026-04-22  
**Primary Language:** Go  
**Documentation:** [https://github.com/cilium/cilium](https://github.com/cilium/cilium)  

---

## Purpose and Use Cases

Cilium is a cloud-native project that provides network functionality for modern distributed systems.

### What Problem Does It Solve?

Cilium addresses the challenges of network in cloud-native environments, enabling teams to implement network features without embedding them in application code.

### When to Use This Project

Use cilium when you need network capabilities in your Kubernetes or cloud-native infrastructure. It's ideal when you require network with minimal application code changes.

### Key Use Cases


- network for microservices
- Integration with Kubernetes and CNCF ecosystem
- network with declarative configuration
- network for observability and monitoring
- network for security and compliance

---

## Architecture Design Patterns

### Core Components


- **Primary Component**: Core functionality
- **Controller**: Cluster management
- **Agent**: Node-level execution
- **API Server**: Management interface
- **Storage**: Configuration persistence

### Component Interactions


1. **Client → Core**: Request routing
2. **Core → Storage**: Configuration persistence
3. **Controller → Agents**: Command distribution
4. **Agents → Controller**: Status reporting
5. **Storage → Controllers**: Configuration sync

### Data Flow Patterns


1. **Request Flow**: Client → Core → Backend
2. **Configuration Flow**: API → Storage → Nodes
3. **State Flow**: Nodes → Control Plane → Dashboard
4. **Telemetry Flow**: Data → Collector → Storage

### Design Principles


- **Declarative Configuration**: YAML/CRD-based configuration
- **Kubernetes-Native**: Leverages Kubernetes APIs
- **Extensible**: Plugin/adapter architecture
- **Observability First**: Built-in metrics, tracing, logging
- **High Availability**: Multi-node clustering
- **Secure by Default**: TLS, authentication, authorization

---

## Integration Approaches

### Integration with Other CNCF Projects


- **Kubernetes**: Native integration with K8s APIs
- **Prometheus**: Metrics collection integration
- **Grafana**: Dashboard visualization
- **Jaeger/Zipkin**: Distributed tracing
- **CoreDNS**: Service discovery integration
- **Envoy**: Service mesh integration
- **Istio**: Service mesh control plane

### API Patterns


- **RESTful API**: Management endpoints
- **gRPC API**: Internal communication
- **WebSocket API**: Real-time updates
- **Admin API**: Configuration management

### Configuration Patterns


- **YAML Manifests**: Human-readable configs
- **JSON**: Machine-readable format
- **Environment Variables**: Runtime configuration
- **ConfigMaps**: Kubernetes config storage
- **CRDs**: Kubernetes custom resources

### Extension Mechanisms


- **Plugins**: Extend functionality
- **Filters**: Process requests
- **Hooks**: Event callbacks
- **Modules**: Add features

---

## Common Pitfalls and How to Avoid Them

### Misconfigurations


- **Endpoint Configuration**: Wrong API endpoints
- **Authentication**: Missing or incorrect auth
- **Resource Limits**: Insufficient resource allocation
- **SSL/TLS**: Certificate validation issues
- **Network Policy**: Incorrect network rules
- **Scaling**: Under/over-provisioned resources

### Performance Issues


- **Request Latency**: High latency
- **Throughput**: Low throughput
- **Memory Usage**: High memory consumption
- **CPU Usage**: High CPU usage
- **Connection Pooling**: Pool exhaustion
- **Cache Misses**: High cache miss rate

### Operational Challenges


- **Configuration Management**: Config drift
- **Upgrade Management**: Rolling upgrades
- **Monitoring**: Metrics collection
- **Logging**: Log aggregation
- **Troubleshooting**: Issue diagnosis
- **Security**: Security audits

### Security Pitfalls


- **Authentication**: Missing authentication
- **Authorization**: Overly permissive ACLs
- **TLS Configuration**: Weak TLS settings
- **Secrets Management**: Exposed secrets
- **RBAC**: Insufficient access control
- **Vulnerabilities**: Outdated dependencies

---

## Coding Practices

### Idiomatic Configuration


- **YAML**: Configuration files
- **JSON**: API payloads
- **Environment Variables**: Runtime config
- **ConfigMaps**: Kubernetes config

### API Usage Patterns


- **REST API**: Management endpoints
- **gRPC API**: Internal communication
- **WebSocket API**: Real-time updates

### Observability Best Practices


- **Prometheus Metrics**: Custom metrics
- **Tracing**: Distributed tracing
- **Access Logs**: Request logging
- **Alerting**: Health checks

### Testing Strategies


- **Unit Tests**: Component tests
- **Integration Tests**: Service tests
- **E2E Tests**: Full stack tests
- **Load Tests**: Performance tests

### Development Workflow


- **Development**: Local dev setup
- **Testing**: Unit and integration tests
- **Debugging**: Logging, tracing
- **Deployment**: Docker, Kubernetes
- **CI/CD**: GitHub Actions
- **Tools**: Project CLI tools

---

## Fundamentals

### Essential Concepts


- **Cluster**: Node group
- **Node**: Individual server
- **Pod**: Container unit
- **Service**: Network service
- **Config**: Configuration data
- **Secret**: Sensitive data
- **Volume**: Storage volume
- **Namespace**: Logical partition

### Terminology Glossary


- **Cluster**: Cluster of nodes
- **Node**: Individual node
- **Service**: Service endpoint
- **Config**: Configuration data
- **Secret**: Secret data
- **Volume**: Storage
- **Namespace**: Namespace
- **Pod**: Pod unit

### Data Models and Types


- **Config**: Config spec
- **Secret**: Secret spec
- **Service**: Service spec
- **Deployment**: Deployment spec
- **Pod**: Pod spec
- **Volume**: Volume spec
- **Namespace**: Namespace spec

### Lifecycle Management


- **Service Lifecycle**: Create → Deploy → Scale → Delete
- **Pod Lifecycle**: Pending → Running → Succeeded/Failed
- **Config Lifecycle**: Create → Apply → Update → Delete
- **Secret Lifecycle**: Create → Encrypt → Decrypt → Delete

### State Management


- **Config State**: Applied config
- **Service State**: Service state
- **Pod State**: Pod state
- **Volume State**: Volume state
- **Secret State**: Encrypted data
- **Namespace State**: Namespace data

---

## Scaling and Deployment Patterns

### Horizontal Scaling


- **Node Scaling**: Add/remove nodes
- **Container Scaling**: Pod replicas
- **Database Scaling**: Database clusters
- **Cache Scaling**: Cache clusters
- **Load Balancing**: Frontend balancing

### High Availability


- **Multiple Instances**: Redundant instances
- **Load Balancing**: Frontend balancing
- **Health Checking**: Automatic failover
- **Graceful Shutdowns**: Clean shutdown
- **Data Replication**: HA storage

### Production Deployments


- **Configuration**: Production config
- **Load Balancing**: Frontend HA
- **Monitoring**: Metrics setup
- **Alerting**: Alerting setup
- **Logging**: Centralized logging
- **Security**: Security hardening

### Upgrade Strategies


- **Rolling Update**: Rolling deployment
- **Blue-Green**: Blue-green deployment
- **Canary**: Canary release
- **Backup**: Pre-upgrade backup
- **Validation**: Post-upgrade validation

### Resource Management


- **Memory Configuration**: Memory limits
- **CPU Configuration**: CPU limits
- **Storage Configuration**: Storage limits
- **Network Configuration**: Network limits
- **Connection Limits**: Connection limits

---

## Additional Resources

- **Official Documentation:** [{repo_info['html_url']}]({repo_info['html_url']})
- **GitHub Repository:** [{repo_info['html_url']}]({repo_info['html_url']})
- **CNCF Project Page:** [cncf.io/projects/{project_info['name']}/](https://www.cncf.io/projects/{project_info['name']}/)
- **Community:** Check the GitHub repository for community channels
- **Versioning:** Refer to project's release notes for version-specific features

---

## Examples

### Enable Network Policy

```yaml
# Enable Cilium with network policy enforcement
helm install cilium cilium/cilium --namespace kube-system   --set networkPolicy.enabled=true   --set hubble.relay.enabled=true   --set hubble.ui.enabled=true

# Create network policy
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: allow-liveness-probes
spec:
  endpointSelector:
    matchLabels:
      app: frontend
  ingress:
    - fromEntities:
        - cluster
```

### Service Mesh with L7 Policies

```yaml
# Enable Cilium service mesh
helm install cilium cilium/cilium --namespace kube-system   --set hubble.relay.enabled=true   --set hubble.ui.enabled=true   --set config.enabled=true

# L7 policy for HTTP traffic
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: frontend-to-backend
spec:
  endpointSelector:
    matchLabels:
      app: backend
  ingress:
    - fromEndpoints:
        - matchLabels:
            app: frontend
      toPorts:
        - ports:
            - port: "80"
              protocol: TCP
          rules:
            http:
              - method: "GET"
                path: "/api/.*"
```

### Monitor with Hubble

```yaml
# Hubble metrics configuration
helm install cilium cilium/cilium --namespace kube-system   --set hubble.metrics.enabled="{dns,drop,tcp,flow,port-distribution,httpV2}"

# Query metrics
kubectl exec -n kube-system <hubble-relay-pod> -- hubble observe --last 100

# Hubble UI access
kubectl port-forward -n hubble-ui svc/hubble-ui 12000:80
```

## Troubleshooting

### Cilium pods in CrashLoopBackOff

**Cause:** Kernel version incompatibility or resource constraints

**Solution:**

```bash
# Check kernel version requirements
# Cilium requires Linux kernel 4.9.17+ or 5.8+

# Check logs
kubectl logs -n kube-system <cilium-pod>

# Disable bpf masquerade if IP masquerade conflicts
helm install cilium cilium/cilium --set bpf.masquerade=false
```

### Network policies not being enforced

**Cause:** Cilium not installed with network policy support

**Solution:**

```bash
# Verify Cilium is managing the cluster
kubectl get nodes -l alpha.cilium.io/ingress-gateway-ip-alloc

# Enable network policy
kubectl -n kube-system patch daemonset cilium --type=json   -p='[{"op": "add", "path": "/spec/template/spec/containers/0/args/-", "value": "--network-policy"}]'

# Restart Cilium pods
kubectl -n kube-system delete pods -l k8s-app=cilium
```

### Hubble relay connection failures

**Cause:** Hubble relay not properly configured or DNS issues

**Solution:**

```bash
# Enable Hubble relay
helm install cilium cilium/cilium --set hubble.relay.enabled=true

# Check relay status
kubectl -n kube-system get pods -l app.kubernetes.io/name=hubble-relay

# Restart relay
kubectl -n kube-system delete pods -l app.kubernetes.io/name=hubble-relay
```

### L7 policy not matching traffic

**Cause:** Incorrect HTTP rule specification or L7 parser issues

**Solution:**

```bash
# Verify HTTP parsing
cilium status --verbose | grep -A5 "HTTP"

# Use correct HTTP rules format
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: http-policy
spec:
  endpointSelector:
    matchLabels:
      app: backend
  ingress:
    - fromEndpoints:
        - matchLabels:
            app: frontend
      toPorts:
        - ports:
            - port: "80"
              protocol: TCP
          rules:
            http:
              - method: "GET"
              - path: "/api/v1/.*"
```

### IP allocation conflicts

**Cause:** Overlapping IP ranges with other CNI plugins

**Solution:**

```bash
# Configure unique IP ranges
helm install cilium cilium/cilium --set ipam.mode=cilium --set clusterPoolIPv4PodCIDR=10.0.0.0/8

# Or use AWS VPC CNI integration
helm install cilium cilium/cilium   --set kubeProxyReplacement=partial   --set k8sServiceHost=<api-server-ip>   --set k8sServicePort=<api-server-port>
```
*Content generated automatically. Verify against official documentation before production use.*

## Troubleshooting

### Cilium pods not starting or crashing

**Cause:** BPF filesystem not mounted, kernel version incompatible, or configuration errors

**Solution:** Verify BPF filesystem mounted at /sys/fs/bpf, check kernel version requirements, validate Cilium configuration, and examine pod logs for specific errors.


### Network policies not being enforced

**Cause:** Cilium not installed in namespace, wrong policy type, or policy selector mismatch

**Solution:** Verify Cilium is installed in namespace, check policy type (CiliumNetworkPolicy vs NetworkPolicy), ensure pod selectors match target pods, and run `cilium policy get`.


### Service load balancing not working

**Cause:** BPF masquerade not enabled, Cilium not watching correct endpoints, or kube-proxy conflicts

**Solution:** Enable BPF masquerade in Cilium config, ensure Cilium has proper RBAC permissions, verify Cilium is managing endpoints with `cilium service list`, and check for kube-proxy interference.


### High memory usage by Cilium

**Cause:** Large number of endpoints, complex policies, or memory leaks

**Solution:** Check endpoint count with `cilium endpoint list`, optimize policies for fewer rules, monitor memory usage with `cilium status`, and consider upgrading to newer Cilium versions.


### Connectivity issues between pods in different nodes

**Cause:** BGP not configured correctly, tunnel not working, or firewall blocking overlay traffic

**Solution:** Verify BGP peer configuration with `cilium bpg peer status`, check tunnel status with `cilium status`, verify firewall allows overlay traffic, and test direct pod-to-pod connectivity.

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
