---
name: k8s
description: Kubernetes deep expertise including cluster management, performance tuning, security hardening, debugging, networking, storage, and production operations. Use when troubleshooting K8s issues, optimizing performance, securing clusters, or managing production workloads.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Kubernetes (K8s) Skill

You are a Kubernetes expert responsible for production cluster management, performance optimization, security hardening, and troubleshooting complex issues. You understand K8s internals, networking, storage, and can debug any cluster problem.

## Core Responsibilities

1. **Cluster Management**
   - Cluster architecture design
   - Node management
   - Upgrades and migrations
   - Multi-cluster strategies

2. **Performance Tuning**
   - Resource optimization
   - Scaling strategies
   - Scheduling optimization
   - etcd performance

3. **Security**
   - Pod security standards
   - Network policies
   - RBAC
   - Secret management
   - Admission controllers

4. **Debugging & Troubleshooting**
   - Pod failures
   - Networking issues
   - Storage problems
   - Performance degradation

5. **Production Operations**
   - Monitoring
   - Backup/restore
   - Disaster recovery
   - High availability

## Cluster Architecture

### Production Cluster Design

```yaml
# production-cluster.yml
cluster_spec:
  control_plane:
    topology: highly_available
    node_count: 3
    instance_type: m6i.2xlarge
    etcd:
      separate_cluster: true
      node_count: 3
      instance_type: m6i.xlarge
      storage: io1, 1000_iops
    api_server:
      load_balancer: internal_tcp
      replicas: 3
    scheduler:
      profiles:
        - default
        - bin_packing
    controller_manager:
      replicas: 3

  worker_nodes:
    node_pools:
      - name: system
        instance_type: m6i.xlarge
        min_size: 3
        max_size: 10
        labels:
          node-type: system
        taints:
          - key: system
            effect: NoSchedule

      - name: general
        instance_type: m6i.2xlarge
        min_size: 5
        max_size: 100
        labels:
          node-type: general

      - name: spot
        instance_type: m6i.2xlarge
        min_size: 0
        max_size: 200
        capacity_type: spot
        labels:
          node-type: spot
          spot: "true"
        taints:
          - key: spot
            value: "true"
            effect: NoSchedule

      - name: gpu
        instance_type: p4d.24xlarge
        min_size: 0
        max_size: 20
        labels:
          nvidia.com/gpu: "true"
        taints:
          - key: nvidia.com/gpu
            value: "true"
            effect: NoSchedule

  networking:
    cni: cilium
    pod_cidr: 10.244.0.0/16
    service_cidr: 10.96.0.0/12
    network_policy: enabled
    service_mesh: istio
    ingress: nginx

  storage:
    csi_drivers:
      - ebs
      - efs
      - s3
    default_storage_class: gp3
    snapshot_enabled: true

  addons:
    - cluster_autoscaler
    - metrics_server
    - prometheus
    - grafana
    - fluent_bit
    - cert_manager
    - external_dns
```

## Performance Optimization

### Resource Optimization

```yaml
# resource-optimization.yml
optimization_strategies:
  rightsizing:
    vertical_pod_autoscaler:
      mode: Auto  # Auto, Initial, Off
      update_mode: Auto
      recommendation:
        min_allowed:
          cpu: 50m
          memory: 64Mi
        max_allowed:
          cpu: 4000m
          memory: 8Gi

    goldilocks:
      enabled: true
      vpa_mode: "off"  # Recommend only, don't apply

  horizontal_scaling:
    hpa:
      api_version: autoscaling/v2
      min_replicas: 3
      max_replicas: 100
      metrics:
        - type: Resource
          resource:
            name: cpu
            target:
              type: Utilization
              averageUtilization: 70
        - type: Resource
          resource:
            name: memory
            target:
              type: Utilization
              averageUtilization: 80
      behavior:
        scale_down:
          stabilization_window_seconds: 300
          policies:
            - type: Percent
              value: 50
              period_seconds: 60
        scale_up:
          stabilization_window_seconds: 60
          policies:
            - type: Percent
              value: 100
              period_seconds: 15

    keda:
      triggers:
        - type: prometheus
          metadata:
            serverAddress: http://prometheus:9090
            metricName: http_requests_total
            threshold: "1000"
            query: |
              sum(rate(http_requests_total{service="api"}[2m]))

  cluster_autoscaler:
    enabled: true
    scale_down_delay: 10m
    scale_down_utilization_threshold: 0.5
    skip_nodes_with_local_storage: false
    skip_nodes_with_system_pods: true
    balance_similar_node_groups: true

  bin_packing:
    scheduler_profiles:
      - name: bin-packing
        plugins:
          score:
            enabled:
              - name: NodeResourcesFit
                weight: 100
            disabled:
              - name: NodeResourcesFit
        pluginConfig:
          - name: NodeResourcesFit
            args:
              scoringStrategy:
                type: MostAllocated
                resources:
                  - name: cpu
                    weight: 1
                  - name: memory
                    weight: 1
```

### etcd Performance Tuning

```yaml
# etcd-optimization.yml
etcd_tuning:
  storage:
    disk_type: ssd
    disk_iops: 3000
    filesystem: ext4
    mount_options: "noatime,nodiratime"

  configuration:
    quota_backend_bytes: 8589934592  # 8GB
    snapshot_count: 10000
    heartbeat_interval: 100
    election_timeout: 1000
    max_snapshots: 5
    max_wals: 5

  defragmentation:
    enabled: true
    schedule: "0 3 * * *"  # Daily at 3 AM
    threshold: 50  # Defrag when fragmentation > 50%

  backup:
    interval: 15m
    retention: 24h
    s3_bucket: etcd-backups
```

### DNS Optimization

```yaml
# coredns-optimization.yml
coredns_config: |
  .:53 {
    errors
    health {
      lameduck 5s
    }
    ready
    kubernetes cluster.local in-addr.arpa ip6.arpa {
      pods insecure
      fallthrough in-addr.arpa ip6.arpa
    }
    prometheus :9153
    forward . /etc/resolv.conf {
      max_concurrent 1000
    }
    cache {
      success 9984  # Cache successful responses for ~2.75 hours
      denial 9984   # Cache NXDOMAIN for ~2.75 hours
      prefetch 10   # Prefetch before TTL expires
    }
    loop
    reload
    loadbalance
  }

dns_policy:
  ndots: 2  # Reduce DNS lookups
  timeout: 2
  attempts: 2
```

## Security Hardening

### Pod Security Standards

```yaml
# pod-security-standards.yml
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
---
# Restricted pod example
apiVersion: v1
kind: Pod
metadata:
  name: secure-app
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    runAsGroup: 1000
    fsGroup: 1000
    seccompProfile:
      type: RuntimeDefault
  containers:
    - name: app
      image: myapp:v1.0.0
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        capabilities:
          drop:
            - ALL
        seccompProfile:
          type: RuntimeDefault
      resources:
        limits:
          cpu: "500m"
          memory: "512Mi"
        requests:
          cpu: "100m"
          memory: "128Mi"
      volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: cache
          mountPath: /app/cache
  volumes:
    - name: tmp
      emptyDir: {}
    - name: cache
      emptyDir:
        sizeLimit: 100Mi
  automountServiceAccountToken: false
```

### Network Policies

```yaml
# default-deny-all.yml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Ingress
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-egress
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Egress
---
# Allow specific traffic
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-allow-ingress
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
        - podSelector:
            matchLabels:
              app: frontend
      ports:
        - protocol: TCP
          port: 8080
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-allow-egress
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
    - Egress
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: database
      ports:
        - protocol: TCP
          port: 5432
    - to:
        - namespaceSelector: {}
          podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - protocol: UDP
          port: 53
```

### RBAC Least Privilege

```yaml
# service-account.yml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-sa
  namespace: production
automountServiceAccountToken: false
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-role
  namespace: production
rules:
  - apiGroups: [""]
    resources: ["configmaps"]
    verbs: ["get", "list"]
    resourceNames: ["app-config"]
  - apiGroups: [""]
    resources: ["secrets"]
    verbs: ["get"]
    resourceNames: ["app-secrets"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-rb
  namespace: production
subjects:
  - kind: ServiceAccount
    name: app-sa
    namespace: production
roleRef:
  kind: Role
  name: app-role
  apiGroup: rbac.authorization.k8s.io
```

## Debugging Commands

### Pod Debugging

```bash
# Debug pod startup issues
kubectl logs my-pod --previous
kubectl describe pod my-pod
kubectl get events --field-selector involvedObject.name=my-pod

# Get into running container
kubectl exec -it my-pod -- /bin/sh

# Debug with ephemeral container (K8s 1.23+)
kubectl debug my-pod -it --image=busybox --target=my-app

# Copy files from pod
kubectl cp my-pod:/app/logs/error.log ./error.log

# Port forward for local debugging
kubectl port-forward pod/my-pod 8080:8080

# Check resource usage
kubectl top pod my-pod
kubectl top pod my-pod --containers

# Network debugging
kubectl run -it --rm debug --image=nicolaka/netshoot --restart=Never -- bash
# Inside debug pod:
nslookup kubernetes.default
netstat -tlnp
tcpdump -i eth0 -n

# Storage debugging
kubectl get pvc
kubectl get pv
kubectl describe pv my-pv
```

### Node Debugging

```bash
# Check node status
kubectl describe node my-node
kubectl get node my-node -o yaml

# SSH to node and check
kubectl debug node/my-node -it --image=mcr.microsoft.com/dotnet/runtime-deps:6.0

# Check kubelet logs
journalctl -u kubelet -f

# Check container runtime
crictl ps
ctr -n k8s.io containers ls

# Check CNI
ls /etc/cni/net.d/
cat /etc/cni/net.d/10-aws.conflist

# Check iptables
iptables -L -n -v
iptables -t nat -L -n -v

# IPVS (if using kube-proxy in ipvs mode)
ipvsadm -Ln
```

### Common Issues

```yaml
# troubleshooting-guide.yml
common_issues:
  image_pull_backoff:
    causes:
      - invalid_image_name
      - image_not_found
      - registry_auth_failed
      - network_issues
    diagnosis:
      - kubectl describe pod
      - kubectl get events
      - docker pull locally
    fixes:
      - check_image_name
      - verify_registry_credentials
      - check_network_connectivity

  crash_loop_backoff:
    causes:
      - application_error
      - missing_config
      - resource_limits
      - health_check_failure
    diagnosis:
      - kubectl logs --previous
      - kubectl describe pod
      - check_resource_limits
    fixes:
      - fix_application_bug
      - add_missing_configmaps
      - increase_resource_limits
      - adjust_liveness_probe

  pending_pods:
    causes:
      - insufficient_resources
      - node_selector_mismatch
      - taints_tolerations
      - pvc_not_bound
    diagnosis:
      - kubectl describe pod
      - kubectl get nodes
      - kubectl get pv,pvc
    fixes:
      - scale_cluster
      - adjust_node_selector
      - add_tolerations
      - check_storage_class

  dns_issues:
    causes:
      - coredns_down
      - network_policy_blocking
      - ndots_misconfigured
    diagnosis:
      - kubectl get pods -n kube-system
      - nslookup from debug pod
      - check_network_policies
    fixes:
      - restart_coredns
      - fix_network_policy
      - adjust_ndots_in_dnsConfig

  oom_killed:
    causes:
      - memory_limit_too_low
      - memory_leak
    diagnosis:
      - kubectl describe pod
      - kubectl top pod
    fixes:
      - increase_memory_limit
      - fix_memory_leak

  network_connectivity:
    causes:
      - network_policy
      - service_not_selecting_pods
      - kube_proxy_issues
    diagnosis:
      - kubectl get endpoints
      - kubectl get networkpolicy
      - check_iptables_rules
    fixes:
      - fix_selector_labels
      - update_network_policy
      - restart_kube_proxy
```

## Production Runbooks

```markdown
# K8s Production Runbook

## Pod Eviction

**Symptoms**: Pods showing `Evicted` status

**Check**:
```bash
kubectl get pods --all-namespaces | grep Evicted
kubectl describe node <node-name>
```

**Common Causes**:
- Disk pressure
- Memory pressure
- PID pressure
- Node not ready

**Fix**:
1. Clean up node:
   ```bash
   kubectl drain <node> --ignore-daemonsets
   # Clean up on node
   docker system prune -a
   # Or kubelet garbage collection
   systemctl restart kubelet
   ```

2. Add resource limits to prevent

## etcd Backup/Restore

**Backup**:
```bash
ETCDCTL_API=3 etcdctl snapshot save snapshot.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key
```

**Restore**:
```bash
# Stop kube-apiserver
systemctl stop kubelet

# Restore snapshot
ETCDCTL_API=3 etcdctl snapshot restore snapshot.db \
  --data-dir=/var/lib/etcd-restored

# Update etcd to use restored data
# Update manifest
vim /etc/kubernetes/manifests/etcd.yaml

# Restart
systemctl start kubelet
```

## Cluster Autoscaler Issues

**Symptoms**: Pods stuck Pending, no new nodes

**Check**:
```bash
kubectl logs -n kube-system deployment/cluster-autoscaler
kubectl get configmap cluster-autoscaler-status -n kube-system -o yaml
```

**Common Issues**:
- ASG max size reached
- Insufficient instance types
- IAM permissions
- Spot interruption

## DNS Resolution Failures

**Symptoms**: `nslookup: can't resolve`

**Check**:
```bash
kubectl get pods -n kube-system -l k8s-app=kube-dns
kubectl logs -n kube-system deployment/coredns

# Test from pod
kubectl run -it --rm debug --image=busybox:1.28 --restart=Never -- nslookup kubernetes.default
```

**Fix**:
- Restart CoreDNS
- Check network policies
- Check CoreDNS ConfigMap
- Check node DNS settings
```

## Monitoring

```yaml
# prometheus-rules.yml
groups:
  - name: kubernetes
    rules:
      - alert: KubernetesPodNotReady
        expr: |
          kube_pod_status_phase{phase=~"Pending|Unknown|Failed"} == 1
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "Pod {{ $labels.pod }} not ready"

      - alert: KubernetesContainerHighCPU
        expr: |
          sum(rate(container_cpu_usage_seconds_total{container!="POD",container!=""}[5m])) by (pod, namespace)
          /
          sum(kube_pod_container_resource_limits{resource="cpu"}) by (pod, namespace)
          > 0.8
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage in {{ $labels.namespace }}/{{ $labels.pod }}"

      - alert: KubernetesContainerHighMemory
        expr: |
          sum(container_memory_working_set_bytes{container!="POD",container!=""}) by (pod, namespace)
          /
          sum(kube_pod_container_resource_limits{resource="memory"}) by (pod, namespace)
          > 0.8
        for: 10m
        labels:
          severity: warning

      - alert: KubernetesNodeNotReady
        expr: |
          kube_node_status_condition{condition="Ready",status="false"} == 1
        for: 15m
        labels:
          severity: critical

      - alert: EtcdHighFsyncDurations
        expr: |
          histogram_quantile(0.99, rate(etcd_disk_wal_fsync_duration_seconds_bucket[5m]))
          > 0.5
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "etcd fsync latency too high"
```
