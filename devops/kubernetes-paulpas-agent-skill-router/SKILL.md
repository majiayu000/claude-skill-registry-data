---




name: kubernetes
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '"Kubernetes in Cloud-Native Engineering - Production-Grade Container
  Scheduling" and Management'
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  role: reference
  scope: infrastructure
  triggers: cloud-native, container orchestration, engineering, k8s, production-grade,
    kubernetes
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



# Kubernetes in Cloud-Native Engineering

**Category:** cncf  
**Status:** Active  
**Stars:** 121,832  
**Last Updated:** 2026-04-22  
**Primary Language:** Go  
**Documentation:** [https://kubernetes.io/docs/](https://kubernetes.io/docs/)  

---

## Purpose and Use Cases

Kubernetes is a core component of the cloud-native ecosystem, serving as a container orchestration platform that automates the deployment, scaling, and management of containerized applications.

### What Problem Does It Solve?

Manual container orchestration at scale, including scheduling, networking, storage, self-healing, and service discovery. It eliminates the need to manually manage container lifecycles across multiple hosts.

### When to Use This Project

Use Kubernetes when you need to manage containerized applications at scale, require self-healing capabilities, need advanced scheduling, or want to leverage the broader cloud-native ecosystem. Not ideal for simple single-service deployments or when you need complete control over the underlying infrastructure.

### Key Use Cases


- Microservices orchestration and management
- Batch job scheduling and execution
- Hybrid and multi-cloud deployments
- CI/CD pipeline orchestration
- Machine learning workflow management
- Edge computing deployments


---

## Architecture Design Patterns

### Core Components


- **API Server**: Central REST interface for all cluster communication
- **etcd**: Distributed key-value store for cluster state
- **Scheduler**: Assigns pods to nodes based on resource requirements
- **Controller Manager**: Runs controller processes (node, replication, endpoints, etc.)
- **Kubelet**: Agent on each node that manages containers
- **Kube Proxy**: Network proxy and load balancer for service access
- **Cloud Controller Manager**: Cloud-provider-specific controllers


### Component Interactions


1. **User/Tool → API Server**: All operations go through the API server
2. **Scheduler watches API Server**: For unscheduled pods
3. **Controller Manager watches API Server**: For state reconciliation
4. **Kubelet watches API Server**: For pods assigned to its node
5. **Kubelet → Container Runtime**: Creates/manages containers
6. **API Server → etcd**: Persists cluster state
7. **Kube Proxy → iptables/ipvs**: Configures network rules


### Data Flow Patterns


1. **Pod Creation**: API Server stores pod spec → Scheduler selects node → Kubelet creates pod
2. **Service Discovery**: Service object created → Kube Proxy updates iptables → DNS updated
3. **Scaling**: ReplicaSet detects mismatch → Creates new pods → Scheduler assigns nodes
4. **Health Checks**: Kubelet performs probes → API Server stores status → Controller-manager responds
5. **Networking**: Pod created → CNI plugin configures network → Pod gets IP → Service endpoint updated


### Design Principles


- **Declarative API**: Resources defined by desired state
- **Reconciliation**: Controllers continuously reconcile state
- **RESTful Interface**: All operations through HTTP API
- **Extensibility**: Custom resources, controllers, and admission webhooks
- **Decentralized**: No single point of failure in control plane
- **Self-Healing**: Automatic recovery from failures


---

## Integration Approaches

### Integration with Other CNCF Projects


- **Containerd**: Default container runtime (CRI implementation)
- **CNI**: Standard for pod networking
- **Prometheus**: Metrics collection and monitoring
- **etcd**: Backend store for cluster state
- **Helm**: Application deployment tool
- **Istio/Envoy**: Service mesh integration
- **Tekton**: CI/CD pipeline execution
- **CoreDNS**: Default DNS server


### API Patterns


- **RESTful API**: HTTP-based operations
- **CRUD Operations**: Create, Read, Update, Delete
- **Watch API**: Real-time event streaming
- **Subresources**: Nested resource operations
- **CRDs**: Custom Resource Definitions for extensions
- **Webhooks**: Admission control and configuration
- **API Groups**: Versioned APIs (v1, apps/v1, etc.)


### Configuration Patterns


- **YAML Manifests**: Resource definitions
- **ConfigMaps**: Non-sensitive configuration
- **Secrets**: Sensitive data storage
- **Helm Values**: Chart configuration
- **kubeconfig**: Client configuration
- **Kubelet Config**: Node-level configuration


### Extension Mechanisms


- **CRDs**: Define custom resources
- **Admission Webhooks**: Validate/modify requests
- **Custom Controllers**: Operator pattern
- **CNI Plugins**: Network implementations
- **CRI Implementations**: Container runtimes
- **CSI Drivers**: Storage providers
- **cloud-controller-manager**: Cloud-specific controllers


---

## Common Pitfalls and How to Avoid Them

### Misconfigurations


- **Resource Limits**: Not setting CPU/memory limits
- **Security Context**: Running as root
- **Image Tags**: Using :latest or mutable tags
- **RBAC**: Overly permissive roles
- **Network Policies**: Not enforcing network isolation
- **Secrets**: Storing secrets in ConfigMaps
- **Persistent Volumes**: Not setting access modes correctly
- **Health Checks**: Missing or incorrect probes


### Performance Issues


- **API Server Load**: Too many watch connections
- **etcd Performance**: High latency or throughput issues
- **Scheduler Bottlenecks**: Complex scheduling requirements
- **Kubelet CPU Usage**: High resource consumption
- **Network Overhead**: CNI plugin performance
- **Pod Startup Time**: Slow image pulls or resource constraints
- **Controller Manager**: High reconciliation overhead


### Operational Challenges


- **Version Upgrades**: In-place upgrades and compatibility
- **Backup and Recovery**: etcd backup strategies
- **Cluster Federation**: Multi-cluster management
- **Scaling**: Controlling cluster growth
- **Monitoring**: Comprehensive observability
- **Cost Management**: Resource optimization
- **Security Hardening**: CIS benchmarks compliance
- **Migration**: Legacy application migration


### Security Pitfalls


- **RBAC**: Overly permissive cluster-admin roles
- **Network Policies**: Missing network isolation
- **Pod Security**: Running as root or privileged
- **Secrets Management**: Secrets in environment variables
- **Image Security**: Using untrusted images
- **API Server Exposure**: Unauthenticated access
- **Control Plane Security**: Missing authentication
- **Service Account Tokens**: Overly broad permissions


---

## Coding Practices

### Idiomatic Configuration


- **Declarative YAML**: Desired state configuration
- **Immutable Resources**: Create, update, delete
- **Labels and Annotations**: Metadata for organization
- **Namespaces**: Resource isolation
- **Kustomize**: Config overlays
- **Helm**: Template-based configuration
- **Validating Webhooks**: Config validation


### API Usage Patterns


- **Kubectl**: Command-line interface
- **Client Libraries**: Official and community clients
- **Kustomize**: Configuration management
- **CRD Operations**: Custom resource management
- **Watch API**: Real-time updates
- **Subresource Operations**: Specialized operations


### Observability Best Practices


- **Metrics**: Kubelet, API server, etcd metrics
- **Logging**: Container logs to centralized systems
- **Tracing**: OpenTelemetry integration
- **Audit Logging**: K8s audit log
- **Events**: Resource events monitoring
- **Dashboard**: Grafana and Kubernetes Dashboard


### Testing Strategies


- **Unit Tests**: Component-level tests
- **Integration Tests**: API and controller tests
- **End-to-End Tests**: Full cluster tests
- **Conformance Tests**: Kubernetes compatibility
- **Load Tests**: Cluster scalability
- **Security Tests**: Vulnerability scanning


### Development Workflow


- **Development**: minikube, kind, k3s for local
- **Testing**: kubectl apply, debug pods
- **Debugging**: kubectl exec, logs, describe
- **Deployment**: Helm, kustomize, GitOps
- **CI/CD**: Tekton, GitLab CI, GitHub Actions
- **Tools**: kustomize, kubectl, k9s, Lens


---

## Fundamentals

### Essential Concepts


- **Cluster**: Set of nodes running containerized applications
- **Node**: Worker machine in the cluster
- **Pod**: Smallest deployable unit, one or more containers
- **Namespace**: Logical partition of cluster resources
- **Deployment**: Manages ReplicaSets for pod updates
- **Service**: Abstraction for pod networking
- **ConfigMap/Secret**: Configuration and sensitive data
- **Volume**: Storage attachment to pods
- **StatefulSet**: Manages stateful applications
- **DaemonSet**: Runs pods on all nodes
- **Job/CronJob**: Batch processing
- **Ingress**: HTTP routing to services


### Terminology Glossary


- **APIServer**: Kubernetes API server
- **Controller Manager**: Runs controllers for cluster state
- **Scheduler**: Assigns pods to nodes
- **Kubelet**: Node agent managing containers
- **Kube Proxy**: Network proxy on nodes
- **etcd**: Distributed key-value store
- **kubeconfig**: Client configuration file
- **Kubelet Config**: Node-level configuration
- **CRD**: Custom Resource Definition
- **Webhook**: Admission control endpoint


### Data Models and Types


- **Object Meta**: Metadata for resources
- **Object Spec**: Desired state specification
- **Object Status**: Current state
- **Pod Spec**: Container configuration
- **Service Spec**: Service configuration
- **Deployment Spec**: Deployment configuration
- **Volume**: Storage configuration
- **Container**: Container definition
- **Env**: Environment variables
- **Resource Requirements**: CPU/memory limits


### Lifecycle Management


- **Pod Lifecycle**: Pending → Running → Succeeded/Failed
- **Container Lifecycle**: PreStart → Running → PreStop
- **Resource Lifecycle**: Create → Update → Delete
- **Controller Lifecycle**: Reconcile loop
- **Health Check Lifecycle**: Startup → Liveness → Readiness
- **Upgrade Lifecycle**: Rolling update, rollback
- **Scale Lifecycle**: Horizontal pod autoscaler
- **Cordon and Drain**: Node maintenance lifecycle


### State Management


- **etcd**: Cluster state persistence
- **Object Status**: Current state in API
- **Replica Management**: Desired vs actual replicas
- **Volume State**: Persistent volume claims
- **ConfigMap/Secret**: Configuration state
- **Network State**: Service endpoints
- **Controller State**: Resource reconciliation


---

## Scaling and Deployment Patterns

### Horizontal Scaling


- **Pod Scaling**: Horizontal Pod Autoscaler (HPA)
- **Cluster Scaling**: Node pool scaling
- **Control Plane**: API server replicas
- **Controller Scaling**: Replica count for controllers
- **Load Balancing**: Service load balancing
- **Ingress Scaling**: Ingress controller scaling
- **Stateful Workloads**: StatefulSet scaling considerations


### High Availability


- **Control Plane HA**: Multiple API servers, etcd cluster
- **etcd Cluster**: Odd number of nodes (3, 5, 7)
- **Node Redundancy**: Multiple worker nodes
- **Pod Disruption Budgets**: Controlled disruptions
- **Multi-Zone Deployments**: Spread across availability zones
- **Storage HA**: Persistent volumes with replication
- **Network HA**: CNI plugin HA configuration


### Production Deployments


- **Cluster Setup**: kubeadm, kops, EKS, GKE, AKS
- **Node Configuration**: Hardened OS, secure boot
- **Control Plane Security**: RBAC, authentication, admission controllers
- **Network Policy**: Enforced network isolation
- **Storage Class**: Appropriate storage provisioners
- **Ingress Controller**: Production-grade ingress
- **Logging and Monitoring**: Centralized logging and metrics
- **Backup and Restore**: etcd backup strategies
- **Security Scanning**: Container image scanning


### Upgrade Strategies


- **Control Plane Upgrade**: api-server, scheduler, controller-manager
- **Node Upgrade**: Rolling node upgrade with cordon/drain
- **etcd Upgrade**: Cluster member replacement
- **Kubernetes Versions**: Version skew policy
- **Backup Before Upgrade**: etcd snapshot
- **Rollback Strategy**: Version rollback procedure
- **Canary Upgrade**: Gradual rollout to new version


### Resource Management


- **CPU/Memory Limits**: Appropriate resource requests and limits
- **Resource Quotas**: Namespace-level resource limits
- **Vertical Pod Autoscaler**: VPA for automatic resource tuning
- **Horizontal Pod Autoscaler**: HPA for scaling
- **Pod Disruption Budgets**: PDB for availability
- **Priority Classes**: Pod priority and preemption
- **Resource Limits Range**: Default and maximum limits


---

## Additional Resources

- **Official Documentation:** [https://kubernetes.io/docs/](https://kubernetes.io/docs/)
- **GitHub Repository:** [github.com/kubernetes/kubernetes](https://github.com/kubernetes/kubernetes)
- **CNCF Project Page:** [cncf.io/projects/kubernetes/](https://www.cncf.io/projects/kubernetes/)
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

### StatefulSet with Persistent Volume Claims


```yaml
# StatefulSet for stateful applications like databases
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgresql
spec:
  serviceName: postgresql
  replicas: 3
  selector:
    matchLabels:
      app: postgresql
  template:
    metadata:
      labels:
        app: postgresql
    spec:
      containers:
      - name: postgresql
        image: postgres:14
        ports:
        - containerPort: 5432
          name: postgres
        env:
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secrets
              key: password
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: standard
      resources:
        requests:
          storage: 10Gi
```

### ConfigMap and Secret Management


```yaml
# ConfigMap for application configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  database.host: "postgresql"
  database.port: "5432"
  log.level: "info"
  cache.ttl: "3600"

# Secret for sensitive data
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  database.password: cG9zdGdyZXMxMjM=
  api.key: YWJjZGVmMTIzNDU2
---
  related-skills: cncf-argo, cncf-artifact-hub, cncf-aws-eks, cncf-azure-aks
# Using ConfigMap and Secret in Pod
apiVersion: v1
kind: Pod
metadata:
  name: app
spec:
  containers:
  - name: app
    image: myapp:latest
    env:
    - name: DB_HOST
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: database.host
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: app-secrets
          key: database.password
    volumeMounts:
    - name: config
      mountPath: /etc/config
  volumes:
  - name: config
    configMap:
      name: app-config
```

### NetworkPolicy for Service Isolation


```yaml
# NetworkPolicy to restrict traffic to specific pods
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: frontend-network-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: frontend
  policyTypes:
  - Ingress
  - Egress
  ingress:
  # Allow traffic from ingress controller
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 80
  # Allow traffic from backend pods
  - from:
    - podSelector:
        matchLabels:
          app: backend
    ports:
    - protocol: TCP
      port: 8080
  egress:
  # Allow DNS resolution
  - to:
    - namespaceSelector: {}
      podSelector:
        matchLabels:
          k8s-app: kube-dns
    ports:
    - protocol: UDP
      port: 53
  # Allow traffic to backend and database
  - to:
    - podSelector:
        matchLabels:
          app: backend
    ports:
    - protocol: TCP
      port: 8080
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

---

## Live References

> **These links are resolved at load time** — content is fetched and inlined to provide the latest documentation.

- [Kubernetes API Reference](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.32/)
- [Kubernetes Concepts Overview](https://kubernetes.io/docs/concepts/)
- [Kubernetes Tasks - Debug](https://kubernetes.io/docs/tasks/debug/)
- [Kubernetes RBAC Reference](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [Kubernetes Networking](https://kubernetes.io/docs/concepts/services-networking/)
- [Kubernetes Storage](https://kubernetes.io/docs/concepts/storage/)
- [Kubernetes Security Best Practices](https://kubernetes.io/docs/concepts/security/overview/)
