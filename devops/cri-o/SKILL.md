---




name: cri-o
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '"Provides CRI-O in Container Runtime - OCI-compliant container runtime
  for Kubernetes"'
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  role: reference
  scope: infrastructure
  triggers: container, cri o, cri-o, runtime
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

# CRI-O in Cloud-Native Engineering

**Category:** container-runtime  
**Status:** Active  
**Stars:** 2,700  
**Last Updated:** 2026-04-22  
**Primary Language:** Go  
**Documentation:** [https://cri-o.io/](https://cri-o.io/)  

---

## Purpose and Use Cases

CRI-O is a CNCF graduated project that provides a lightweight container runtime for Kubernetes, implementing the Kubernetes Container Runtime Interface (CRI).

### What Problem Does It Solve?

Kubernetes container runtime fragmentation. Before CRI-O, Kubernetes supported Docker, rkt, and other runtimes. CRI-O provides a dedicated Kubernetes runtime that's minimal, secure, and optimized for Kubernetes workloads.

### When to Use This Project

Use CRI-O when you need:
- Lightweight container runtime for Kubernetes
- Security-focused container execution
- Full Kubernetes CRI compliance
- OCI (Open Container Initiative) compatibility
- Integration with containerd and runc

### Key Use Cases

- **Kubernetes Node Runtime**: Primary runtime for Kubernetes nodes
- **Edge Computing**: Lightweight runtime for resource-constrained environments
- **Security-First Deployments**: Minimal attack surface for containers
- **Multi-Container Orchestrators**: Container execution for Pod-based workloads
- **CI/CD Pipelines**: Container runtime for build and test environments

---

## Architecture Design Patterns

### CRI-O Architecture

```
┌─────────────────────────────────────────┐
│           Kubernetes Kubelet            │
│        (CRI Client - gRPC)              │
└──────────────┬──────────────────────────┘
               │ CRI (Container Runtime Interface)
               ▼
┌─────────────────────────────────────────┐
│            CRI-O Daemon                 │
│  ┌──────────────┐  ┌─────────────────┐  │
│  │  Runtime     │  │  Image Manager  │  │
│  │  (runc)      │  │  (containers/image)│ │
│  └──────────────┘  └─────────────────┘  │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│        Storage (OverlayFS, etc.)        │
└─────────────────────────────────────────┘
```

### CRI Interface

CRI defines two services:

```protobuf
// RuntimeService - container lifecycle operations
service RuntimeService {
  rpc RunPodSandbox(RunPodSandboxRequest) returns (RunPodSandboxResponse);
  rpc StopPodSandbox(StopPodSandboxRequest) returns (StopPodSandboxResponse);
  rpc RemovePodSandbox(RemovePodSandboxRequest) returns (RemovePodSandboxResponse);
  rpc CreateContainer(CreateContainerRequest) returns (CreateContainerResponse);
  rpc StartContainer(StartContainerRequest) returns (StartContainerResponse);
  rpc StopContainer(StopContainerRequest) returns (StopContainerResponse);
  rpc RemoveContainer(RemoveContainerRequest) returns (RemoveContainerResponse);
  // ... more methods
}

// ImageService - image management operations
service ImageService {
  rpc ListImages(ListImagesRequest) returns (ListImagesResponse);
  rpc ImageStatus(ImageStatusRequest) returns (ImageStatusResponse);
  rpc PullImage(PullImageRequest) returns (PullImageResponse);
  rpc RemoveImage(RemoveImageRequest) returns (RemoveImageResponse);
  rpc ImageFsInfo(ImageFsInfoRequest) returns (ImageFsInfoResponse);
}
```

### Pod Sandbox

```bash
# Pod sandbox (pause container)
# Minimal container that holds network namespace

# Configuration
pod_sandbox_image: "k8s.gcr.io/pause:3.9"

# Network namespace sharing
# All containers in pod share:
# - Network namespace (port, IP)
# - UTS namespace (hostname)
# - IPC namespace (shared memory)
```

### Image Management

```yaml
# Image configuration
image_config:
  # Default image pull policy
  image_pull_progress_deadline: 60s
  # Image pull credentials
  auth_configs: {}
  # Registry mirrors
  mirrors: {}
```

### Storage Drivers

```yaml
# Storage configuration
storage_driver: overlay2
storage_config:
  overlay2:
    image_store: /var/lib/containers/storage
    mountopt: "metacopy=on"
  graph_root: /var/lib/containers/storage
  run_root: /run/containers/storage
```

---

## Integration Approaches

### Kubernetes Integration

```bash
# Configure kubelet to use CRI-O
cat > /etc/systemd/system/kubelet.service.d/10-cri-o.conf <<EOF
[Service]
Environment="KUBELET_EXTRA_ARGS=--container-runtime=remote --container-runtime-endpoint=unix:///run/crio/crio.sock --image-service-endpoint=unix:///run/crio/crio.sock"
EOF

# Restart kubelet
systemctl daemon-reexec
systemctl restart kubelet
```

#### Pod with CRI-O

```yaml
# Kubernetes pod using CRI-O
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  namespace: default
spec:
  containers:
  - name: nginx
    image: nginx:1.21
    ports:
    - containerPort: 80
    resources:
      limits:
        memory: "128Mi"
        cpu: "500m"
    securityContext:
      readOnlyRootFilesystem: true
      runAsNonRoot: true
      capabilities:
        drop:
        - ALL
```

### Container Engine Compatibility

```bash
# Containerd compatibility mode
# CRI-O can run containerd containers

# Using ctr (containerd CLI) with CRI-O
ctr --address /run/crio/crio.sock images pull nginx:latest

# Using crictl (CRI-compatible CLI)
crictl images
crictl pods
crictl ps
```

### Image Registry Integration

#### 1. Docker Hub

```yaml
# Pull from Docker Hub
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  - name: nginx
    image: nginx:latest
```

#### 2. Private Registry

```yaml
# Pull from private registry with secret
apiVersion: v1
kind: Secret
metadata:
  name: registry-secret
type: kubernetes.io/dockerconfigjson
data:
  .dockerconfigjson: <base64-encoded-config>

---
  related-skills: cncf-argo, cncf-artifact-hub, cncf-aws-eks, cncf-azure-aks
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  imagePullSecrets:
  - name: registry-secret
  containers:
  - name: nginx
    image: private-registry.example.com/nginx:latest
```

#### 3. Registry Mirrors

```yaml
# Registry mirror configuration
[crio.registry]
  [crio.registry.mirrors]
    [crio.registry.mirrors."docker.io"]
      priority = 1
      endpoints = ["https://mirror.gcr.io"]
```

### CRI-Tools Integration

```bash
# Install crictl (CRI client)
wget https://github.com/kubernetes-sigs/cri-tools/releases/download/v1.26.0/crictl-v1.26.0-linux-amd64.tar.gz
tar -xzf crictl-v1.26.0-linux-amd64.tar.gz
sudo mv crictl /usr/local/bin/

# Configure crictl
cat > /etc/crictl.yaml <<EOF
runtime-endpoint: unix:///run/crio/crio.sock
image-endpoint: unix:///run/crio/crio.sock
timeout: 2
debug: true
EOF

# Use crictl
crictl pods
crictl ps -a
crictl images
crictl logs <container-id>
```

---
  related-skills: cncf-argo, cncf-artifact-hub, cncf-aws-eks, cncf-azure-aks

## Common Pitfalls and How to Avoid Them

### 1. Storage Path Configuration

**Pitfall:** Storage paths not properly configured.

```yaml
# ❌ Incorrect - missing storage configuration
# Default paths may not be appropriate

# ✅ Correct - explicit storage configuration
[crio]
  storage = "overlay2"
  storage_option = [
    "overlay2.override_kernel_check=true",
  ]
  storage_config:
    overlay2:
      image_store: "/var/lib/containers/storage"
    graph_root: "/var/lib/containers/storage"
    run_root: "/run/containers/storage"
```

### 2. Image Pull Policy

**Pitfall:** Incorrect image pull policy causing stale images.

```yaml
# ❌ Incorrect - Always pull with incorrect policy
# image_pull_policy: IfNotPresent  # Not pulling updates

# ✅ Correct - appropriate policy
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  containers:
  - name: myapp
    image: myapp:v1.2.3
    imagePullPolicy: Always  # Always pull for updates
```

### 3. Security Context

**Pitfall:** Running containers as root.

```yaml
# ❌ Incorrect - running as root
apiVersion: v1
kind: Pod
metadata:
  name: insecure
spec:
  containers:
  - name: insecure
    image: nginx
    # No security context - runs as root

# ✅ Correct - secure security context
apiVersion: v1
kind: Pod
metadata:
  name: secure
spec:
  containers:
  - name: secure
    image: nginx
    securityContext:
      readOnlyRootFilesystem: true
      runAsNonRoot: true
      runAsUser: 1000
      runAsGroup: 1000
      capabilities:
        drop:
        - ALL
```

### 4. Log Rotation

**Pitfall:** Log files growing unbounded.

```yaml
# ❌ Incorrect - no log rotation
# Logs accumulate and fill disk

# ✅ Correct - with log rotation
[crio]
  # Log rotation configuration
  log_size_max = -1  # Disable size limit (use external rotation)
  
# Use external log rotation
cat > /etc/logrotate.d/crio <<EOF
/var/log/crio/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    copytruncate
}
EOF
```

### 5. Resource Limits

**Pitfall:** Missing resource limits causing resource exhaustion.

```yaml
# ❌ Incorrect - no resource limits
apiVersion: v1
kind: Pod
metadata:
  name: no-limits
spec:
  containers:
  - name: app
    image: app

# ✅ Correct - with resource limits
apiVersion: v1
kind: Pod
metadata:
  name: with-limits
spec:
  containers:
  - name: app
    image: app
    resources:
      requests:
        memory: "64Mi"
        cpu: "100m"
      limits:
        memory: "128Mi"
        cpu: "500m"
```

### 6. SELinux/AppArmor

**Pitfall:** Security module conflicts.

```yaml
# ❌ Incorrect - SELinux not configured
# Can cause permission issues

# ✅ Correct - with SELinux configuration
[crio]
  # SELinux configuration
  selinux = true
  
  # AppArmor configuration
  apparmor_profile = "runtime/default"
```

---
  related-skills: cncf-argo, cncf-artifact-hub, cncf-aws-eks, cncf-azure-aks

## Coding Practices

### CRI Client Library

```go
// CRI client for container operations
package cri

import (
    "context"
    "fmt"
    "time"
    
    "github.com/kubernetes-sigs/cri-api/pkg/apis/runtime/v1alpha2"
    "google.golang.org/grpc"
)

// Client wraps CRI client operations
type Client struct {
    runtimeClient  v1alpha2.RuntimeServiceClient
    imageClient    v1alpha2.ImageServiceClient
    conn           *grpc.ClientConn
}

// NewClient creates a new CRI client
func NewClient(endpoint string) (*Client, error) {
    conn, err := grpc.Dial(
        endpoint,
        grpc.WithInsecure(),
        grpc.WithConnectParams(grpc.ConnectParams{
            Backoff: backoff.Config{
                BaseDelay:  100 * time.Millisecond,
                MaxDelay:   10 * time.Second,
            },
        }),
    )
    if err != nil {
        return nil, fmt.Errorf("failed to connect: %w", err)
    }
    
    return &Client{
        runtimeClient: v1alpha2.NewRuntimeServiceClient(conn),
        imageClient:   v1alpha2.NewImageServiceClient(conn),
        conn:          conn,
    }, nil
}

// RunPodSandbox creates a pod sandbox
func (c *Client) RunPodSandbox(ctx context.Context, config *v1alpha2.PodSandboxConfig) (string, error) {
    req := &v1alpha2.RunPodSandboxRequest{
        Config: config,
    }
    
    resp, err := c.runtimeClient.RunPodSandbox(ctx, req)
    if err != nil {
        return "", fmt.Errorf("failed to run pod sandbox: %w", err)
    }
    
    return resp.PodSandboxId, nil
}

// StopPodSandbox stops a pod sandbox
func (c *Client) StopPodSandbox(ctx context.Context, podSandboxID string) error {
    req := &v1alpha2.StopPodSandboxRequest{
        PodSandboxId: podSandboxID,
    }
    
    _, err := c.runtimeClient.StopPodSandbox(ctx, req)
    return err
}

// RemovePodSandbox removes a pod sandbox
func (c *Client) RemovePodSandbox(ctx context.Context, podSandboxID string) error {
    req := &v1alpha2.RemovePodSandboxRequest{
        PodSandboxId: podSandboxID,
    }
    
    _, err := c.runtimeClient.RemovePodSandbox(ctx, req)
    return err
}

// CreateContainer creates a container in a pod
func (c *Client) CreateContainer(ctx context.Context, podSandboxID string, config *v1alpha2.ContainerConfig, sandboxConfig *v1alpha2.PodSandboxConfig) (string, error) {
    req := &v1alpha2.CreateContainerRequest{
        PodSandboxId:  podSandboxID,
        Config:        config,
        SandboxConfig: sandboxConfig,
    }
    
    resp, err := c.runtimeClient.CreateContainer(ctx, req)
    if err != nil {
        return "", fmt.Errorf("failed to create container: %w", err)
    }
    
    return resp.ContainerId, nil
}

// StartContainer starts a container
func (c *Client) StartContainer(ctx context.Context, containerID string) error {
    req := &v1alpha2.StartContainerRequest{
        ContainerId: containerID,
    }
    
    _, err := c.runtimeClient.StartContainer(ctx, req)
    return err
}

// StopContainer stops a container
func (c *Client) StopContainer(ctx context.Context, containerID string, timeout int64) error {
    req := &v1alpha2.StopContainerRequest{
        ContainerId: containerID,
        Timeout:     timeout,
    }
    
    _, err := c.runtimeClient.StopContainer(ctx, req)
    return err
}

// RemoveContainer removes a container
func (c *Client) RemoveContainer(ctx context.Context, containerID string) error {
    req := &v1alpha2.RemoveContainerRequest{
        ContainerId: containerID,
    }
    
    _, err := c.runtimeClient.RemoveContainer(ctx, req)
    return err
}

// PullImage pulls an image
func (c *Client) PullImage(ctx context.Context, image string, auth *v1alpha2.AuthConfig, podConfig *v1alpha2.PodSandboxConfig) (string, error) {
    req := &v1alpha2.PullImageRequest{
        Image: &v1alpha2.ImageSpec{
            Image: image,
        },
        Auth:         auth,
        SandboxConfig: podConfig,
    }
    
    resp, err := c.imageClient.PullImage(ctx, req)
    if err != nil {
        return "", fmt.Errorf("failed to pull image: %w", err)
    }
    
    return resp.ImageRef, nil
}

// RemoveImage removes an image
func (c *Client) RemoveImage(ctx context.Context, image string) error {
    req := &v1alpha2.RemoveImageRequest{
        Image: &v1alpha2.ImageSpec{
            Image: image,
        },
    }
    
    _, err := c.imageClient.RemoveImage(ctx, req)
    return err
}

// ListImages lists available images
func (c *Client) ListImages(ctx context.Context) ([]*v1alpha2.Image, error) {
    req := &v1alpha2.ListImagesRequest{}
    
    resp, err := c.imageClient.ListImages(ctx, req)
    if err != nil {
        return nil, fmt.Errorf("failed to list images: %w", err)
    }
    
    return resp.Images, nil
}
```

### Pod Sandbox Builder

```go
// Pod sandbox builder
package cri

import (
    "fmt"
    
    "github.com/kubernetes-sigs/cri-api/pkg/apis/runtime/v1alpha2"
)

// PodBuilder builds pod sandbox configurations
type PodBuilder struct {
    config *v1alpha2.PodSandboxConfig
}

// NewPodBuilder creates a new pod builder
func NewPodBuilder(name, namespace string) *PodBuilder {
    return &PodBuilder{
        config: &v1alpha2.PodSandboxConfig{
            Metadata: &v1alpha2.PodSandboxMetadata{
                Name:      name,
                Namespace: namespace,
                Uid:       generateUID(),
                Attempt:   1,
            },
            Hostname:  fmt.Sprintf("%s.%s", name, namespace),
            LogDirectory: "/var/log/pods",
        },
    }
}

// WithLabel adds a label to the pod
func (b *PodBuilder) WithLabel(key, value string) *PodBuilder {
    if b.config.Labels == nil {
        b.config.Labels = make(map[string]string)
    }
    b.config.Labels[key] = value
    return b
}

// WithAnnotation adds an annotation to the pod
func (b *PodBuilder) WithAnnotation(key, value string) *PodBuilder {
    if b.config.Annotations == nil {
        b.config.Annotations = make(map[string]string)
    }
    b.config.Annotations[key] = value
    return b
}

// WithPortMapping adds a port mapping
func (b *PodBuilder) WithPortMapping(containerPort, hostPort int32) *PodBuilder {
    b.config.PortMappings = append(b.config.PortMappings, &v1alpha2.PortMapping{
        ContainerPort: containerPort,
        HostPort:      hostPort,
    })
    return b
}

// WithLinuxOptions adds Linux-specific options
func (b *PodBuilder) WithLinuxOptions(options *v1alpha2.LinuxPodSandboxConfig) *PodBuilder {
    b.config.Linux = options
    return b
}

// WithDNSConfig adds DNS configuration
func (b *PodBuilder) WithDNSConfig(dnsConfig *v1alpha2.DNSConfig) *PodBuilder {
    b.config.DnsConfig = dnsConfig
    return b
}

// Build returns the pod configuration
func (b *PodBuilder) Build() *v1alpha2.PodSandboxConfig {
    return b.config
}

func generateUID() string {
    // Generate unique pod UID
    return "pod-" + generateRandomID(8)
}

func generateRandomID(length int) string {
    // Generate random ID
    // Implementation depends on crypto library
    return ""
}
```

### Container Builder

```go
// Container builder
package cri

import (
    "fmt"
    
    "github.com/kubernetes-sigs/cri-api/pkg/apis/runtime/v1alpha2"
)

// ContainerBuilder builds container configurations
type ContainerBuilder struct {
    config *v1alpha2.ContainerConfig
}

// NewContainerBuilder creates a new container builder
func NewContainerBuilder(name, image string) *ContainerBuilder {
    return &ContainerBuilder{
        config: &v1alpha2.ContainerConfig{
            Metadata: &v1alpha2.ContainerMetadata{
                Name:    name,
                Attempt: 1,
            },
            Image: &v1alpha2.ImageSpec{
                Image: image,
            },
            Command:    []string{},
            Args:       []string{},
            Env:        []*v1alpha2.KeyValue{},
            Labels:     make(map[string]string),
            Annotations: make(map[string]string),
        },
    }
}

// WithCommand sets the container command
func (b *ContainerBuilder) WithCommand(cmd ...string) *ContainerBuilder {
    b.config.Command = cmd
    return b
}

// WithArgs sets the container arguments
func (b *ContainerBuilder) WithArgs(args ...string) *ContainerBuilder {
    b.config.Args = args
    return b
}

// WithEnv adds an environment variable
func (b *ContainerBuilder) WithEnv(key, value string) *ContainerBuilder {
    b.config.Env = append(b.config.Env, &v1alpha2.KeyValue{
        Key:   key,
        Value: value,
    })
    return b
}

// WithLabel adds a label
func (b *ContainerBuilder) WithLabel(key, value string) *ContainerBuilder {
    b.config.Labels[key] = value
    return b
}

// WithAnnotation adds an annotation
func (b *ContainerBuilder) WithAnnotation(key, value string) *ContainerBuilder {
    b.config.Annotations[key] = value
    return b
}

// WithResources sets resource requests and limits
func (b *ContainerBuilder) WithResources(requests, limits map[string]string) *ContainerBuilder {
    b.config.Resources = &v1alpha2.ResourceConfig{
        Limits:   make(map[string]string),
        Requests: make(map[string]string),
    }
    
    for k, v := range limits {
        b.config.Resources.Limits[k] = v
    }
    for k, v := range requests {
        b.config.Resources.Requests[k] = v
    }
    
    return b
}

// WithSecurityContext sets security context
func (b *ContainerBuilder) WithSecurityContext(sc *v1alpha2.SecurityContext) *ContainerBuilder {
    b.config.SecurityContext = sc
    return b
}

// WithVolumeMounts adds volume mounts
func (b *ContainerBuilder) WithVolumeMounts(mounts []*v1alpha2.Mount) *ContainerBuilder {
    b.config.Mounts = mounts
    return b
}

// Build returns the container configuration
func (b *ContainerBuilder) Build() *v1alpha2.ContainerConfig {
    return b.config
}
```

---

## Fundamentals

### CRI-O Components

#### 1. CRI-O Daemon

- Manages container lifecycle
- Implements CRI interface
- Coordinates with container runtime (runc)

#### 2. Runtime (runc)

- OCI-compliant container runtime
- Creates and manages containers
- Handles namespaces and cgroups

#### 3. Image Manager

- Pulls images from registries
- Manages image storage
- Supports multiple image formats

#### 4. Storage Driver

- Manages container filesystem layers
- Supports overlay2, vfs, btrfs, etc.
- Handles image layering

### CRI Command Flow

```
1. Kubelet → CRI-O: CreateContainer
2. CRI-O → Runtime: Create container
3. Runtime → CRI-O: Container created
4. CRI-O → Kubelet: Container ID
5. Kubelet → CRI-O: StartContainer
6. CRI-O → Runtime: Start container
7. Runtime → CRI-O: Container started
```

### Storage Configuration

```yaml
# Storage drivers
- overlay2: Overlay filesystem (recommended)
- vfs: Virtual filesystem (debug)
- btrfs: Btrfs filesystem
- zfs: ZFS filesystem
```

---

## Scaling and Deployment Patterns

### Multi-Node Cluster

```bash
# Deploy CRI-O on multiple nodes
# Each node runs CRI-O daemon

# Node configuration
[crio]
  storage_driver = "overlay2"
  storage_option = [
    "overlay2.override_kernel_check=true",
  ]

# Shared storage (optional)
# For stateful workloads
```

### High Availability

```bash
# HA deployment
# Multiple nodes with CRI-O
# Load balancing for kubelets
# Redundant storage
```

### Resource Management

```yaml
# Per-container resource limits
apiVersion: v1
kind: Pod
metadata:
  name: resource-limited
spec:
  containers:
  - name: app
    image: app
    resources:
      requests:
        cpu: "100m"
        memory: "64Mi"
      limits:
        cpu: "500m"
        memory: "256Mi"
```

### Security hardening

```bash
# Security configuration
# Disable root containers
[crio]
  allow_privilege_escalation = false

# AppArmor profile
apparmor_profile = "runtime/default"

# SELinux
selinux = true

# Seccomp
seccomp_profile = "runtime/default"
```

---
  related-skills: cncf-argo, cncf-artifact-hub, cncf-aws-eks, cncf-azure-aks

## Additional Resources

### Official Documentation

- [CRI-O](https://cri-o.io/) - Project website
- [CRI-O Documentation](https://github.com/cri-o/cri-o/blob/main/README.md) - README documentation
- [CRI-O GitHub](https://github.com/cri-o/cri-o) - Source code
- [CRI Specification](https://github.com/kubernetes/cri-api) - CRI API

### Implementations

- [Kubernetes CRI-O](https://kubernetes.io/docs/setup/production-environment/container-runtimes/#cri-o) - Kubernetes integration
- [CRI-O Operator](https://github.com/cri-o/cri-o-operator) - Operator for CRI-O
- [OpenShift CRI-O](https://docs.openshift.com/container-platform/4.10/openshift_images/controlling-cri-o.html) - OpenShift integration

### Community Resources

- [CNCF CRI-O](https://www.cncf.io/projects/cri-o/) - CNCF project page
- [CRI-O Slack](https://kubernetes.slack.com/archives/CKQ66Q8QV) - Community discussion
- [CRI-O Mailing List](https://lists.cncf.io/g/cncf-cri-o) - Announcements

### Learning Resources

- [CRI-O Getting Started](https://github.com/cri-o/cri-o/blob/main/tutorials/setup.md) - Setup guide
- [CRI-O Examples](https://github.com/cri-o/cri-o/tree/main/tutorials) - Examples
- [CRI-O Webinars](https://www.cncf.io/cri-o-webinars/) - Video content

---

*This SKILL.md file was verified and last updated on 2026-04-22. Content based on CNCF CRI-O project and production usage patterns.*
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
