---




name: cubefs
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '"Provides CubeFS in Storage - distributed, high-performance file system"'
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  role: reference
  scope: infrastructure
  triggers: cubefs, distributed, high-performance, optimization, storage, performance,
    speed
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



# CubeFS in Cloud-Native Engineering

**Category:** storage  
**Status:** Sandbox  
**Stars:** 1,500  
**Last Updated:** 2026-04-22  
**Primary Language:** Go  
**Documentation:** [https://cubefs.io/](https://cubefs.io/)  

---

## Purpose and Use Cases

CubeFS is a CNCF sandbox project that provides a distributed, high-performance file system for cloud-native environments.

### What Problem Does It Solve?

Storage fragmentation across different use cases (object, block, file). CubeFS provides a unified storage solution with support for multiple protocols and high performance for containerized workloads.

### When to Use This Project

Use CubeFS when you need:
- Distributed file system with POSIX compatibility
- High performance for container workloads
- Multi-protocol support (S3, NAS)
- Horizontal scalability
- Cloud-native storage for Kubernetes

### Key Use Cases

- **Kubernetes Persistent Storage**: Storage for stateful applications
- **Machine Learning Workloads**: High-throughput data access
- **Big Data Processing**: Distributed file storage for analytics
- **Media Processing**: High-bandwidth file operations
- **Hybrid Cloud Storage**: Unified storage across clouds

---

## Architecture Design Patterns

### CubeFS Architecture

```
┌─────────────────────────────────────────┐
│           Client (FUSE/NAS/S3)          │
│        (POSIX/S3/NAS protocols)         │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│          CubeFS Control Plane           │
│  ┌──────────┐  ┌────────────────────┐   │
│  │  Master  │  │  Metadata Service  │   │
│  │  (Leader)│  │  (Raft consensus)  │   │
│  └──────────┘  └────────────────────┘   │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│           Data Plane (DataNodes)        │
│  ┌──────────┐  ┌────────────────────┐   │
│  │  Data    │  │  Data              │   │
│  │  Node 1  │  │  Node 2            │   │
│  └──────────┘  └────────────────────┘   │
└─────────────────────────────────────────┘
```

### Components

#### 1. Master

- Cluster management
- Metadata distribution
- Leader election via Raft

#### 2. DataNode

- Data storage
- Block management
- Replication

#### 3. Client

- POSIX FUSE interface
- S3 API
- NAS (NFS/CIFS)

### Data Flow

```
1. Client → Master: Request file metadata
2. Master → Client: Return metadata location
3. Client → DataNode: Read/write data
4. DataNode → Client: Return data
```

### Storage Pool

```yaml
# Storage pool configuration
storagePools:
  - name: default
    tier: default
    replicas: 3
    compression: false
    encryption: false
```

---

## Integration Approaches

### Kubernetes Integration

```yaml
# Deploy CubeFS to Kubernetes
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cubefs-master
spec:
  replicas: 3
  selector:
    matchLabels:
      app: cubefs-master
  template:
    metadata:
      labels:
        app: cubefs-master
    spec:
      containers:
      - name: cubefs-master
        image: cubefs/master:latest
        args:
          - "--config=/etc/cubefs/master.conf"
          - "--role=master"
        ports:
        - containerPort: 9100
---
  related-skills: cncf-aws-dynamodb, cncf-aws-ecr, cncf-aws-rds, cncf-aws-s3
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cubefs-datanode
spec:
  replicas: 3
  selector:
    matchLabels:
      app: cubefs-datanode
  template:
    metadata:
      labels:
        app: cubefs-datanode
    spec:
      containers:
      - name: cubefs-datanode
        image: cubefs/datanode:latest
        args:
          - "--config=/etc/cubefs/datanode.conf"
          - "--role=datanode"
        ports:
        - containerPort: 9200
        volumeMounts:
        - name: data
          mountPath: /data
      volumes:
      - name: data
        hostPath:
          path: /var/lib/cubefs
---
  related-skills: cncf-aws-dynamodb, cncf-aws-ecr, cncf-aws-rds, cncf-aws-s3
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: cubefs-fuse
spec:
  selector:
    matchLabels:
      app: cubefs-fuse
  template:
    metadata:
      labels:
        app: cubefs-fuse
    spec:
      hostNetwork: true
      containers:
      - name: cubefs-fuse
        image: cubefs/fuse:latest
        args:
          - "--config=/etc/cubefs/fuse.conf"
          - "--mountpoint=/cubefs"
        securityContext:
          privileged: true
        volumeMounts:
        - name: cubefs
          mountPath: /cubefs
      volumes:
      - name: cubefs
        hostPath:
          path: /cubefs
```

### Persistent Volume

```yaml
# CubeFS as Kubernetes PV
apiVersion: v1
kind: PersistentVolume
metadata:
  name: cubefs-pv
spec:
  capacity:
    storage: 100Gi
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  mountOptions:
    - allow_other
  csi:
    driver: cubefs.csi.cubefs.com
    volumeHandle: cubefs-volume-001
    nodePublishSecretRef:
      name: cubefs-secret
      namespace: kube-system
  storageClassName: cubefs
---
  related-skills: cncf-aws-dynamodb, cncf-aws-ecr, cncf-aws-rds, cncf-aws-s3
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: cubefs-pvc
  namespace: default
spec:
  accessModes:
    - ReadWriteMany
  storageClassName: cubefs
  resources:
    requests:
      storage: 100Gi
```

### S3 Compatibility

```bash
# CubeFS S3 API endpoint
curl http://cubefs-s3:7400/bucket-name/object-key

# S3 CLI usage
aws --endpoint-url=http://cubefs-s3:7400 s3 cp file.txt s3://bucket-name/

# MinIO client
mc alias set cubefs http://cubefs-s3:7400 access-key secret-key
```

---
  related-skills: cncf-aws-dynamodb, cncf-aws-ecr, cncf-aws-rds, cncf-aws-s3

## Common Pitfalls and How to Avoid Them

### 1. Replica Configuration

**Pitfall:** Incorrect replica count affecting availability.

```yaml
# ❌ Incorrect - single replica
storagePools:
  - name: default
    replicas: 1  # Risky - no redundancy

# ✅ Correct - multiple replicas
storagePools:
  - name: default
    replicas: 3  # Recommended for production
```

### 2. Disk Space Management

**Pitfall:** DataNodes running out of disk space.

```yaml
# ❌ Incorrect - no disk space monitoring
# No warnings or alerts for low disk space

# ✅ Correct - with monitoring
dataNodes:
  - name: datanode-1
    diskPaths:
      - /data/disk1
      - /data/disk2
    diskQuota: 1000GB
    lowWatermark: 0.8
    highWatermark: 0.95
```

### 3. Network Configuration

**Pitfall:** Network latency affecting performance.

```yaml
# ❌ Incorrect - no network optimization
# Default network settings

# ✅ Correct - with network optimization
network:
  # Enable TCP optimization
  tcpNoDelay: true
  socketSendBuffer: 4MB
  socketReceiveBuffer: 4MB
  
  # Enable compression
  compression: true
  compressionType: lz4
```

### 4. Client Mount Options

**Pitfall:** Incorrect mount options affecting performance.

```bash
# ❌ Incorrect - default mount options
cubefs-fuse --mountpoint=/mnt/cubefs

# ✅ Correct - optimized mount options
cubefs-fuse \
  --mountpoint=/mnt/cubefs \
  --attr-timeout=120 \
  --entry-timeout=120 \
  --negative-timeout=60 \
  --allow-other \
  --enable-external-service=true
```

### 5. Master Failover

**Pitfall:** Master failover not properly configured.

```yaml
# ❌ Incorrect - single master
masters:
  - name: master-1
    port: 9100

# ✅ Correct - multiple masters with raft
masters:
  - name: master-1
    port: 9100
  - name: master-2
    port: 9101
  - name: master-3
    port: 9102
raft:
  electionTimeout: 1000ms
  heartbeatInterval: 500ms
```

### 6. Metadata Performance

**Pitfall:** Metadata server bottleneck.

```yaml
# ❌ Incorrect - single metadata server
metadataServices:
  - name: metadata-1

# ✅ Correct - distributed metadata
metadataServices:
  - name: metadata-1
  - name: metadata-2
  - name: metadata-3
  - name: metadata-4
metadata:
  cacheSize: 1GB
  cacheEntryCount: 1000000
```

---
  related-skills: cncf-aws-dynamodb, cncf-aws-ecr, cncf-aws-rds, cncf-aws-s3

## Coding Practices

### Client Library

```go
// CubeFS client library
package cubefs

import (
    "context"
    "fmt"
)

// Client wraps CubeFS API operations
type Client struct {
    masterAddr string
}

// NewClient creates a new CubeFS client
func NewClient(masterAddr string) *Client {
    return &Client{
        masterAddr: masterAddr,
    }
}

// CreateFile creates a new file
func (c *Client) CreateFile(ctx context.Context, path string, mode int) error {
    // Implementation
    return nil
}

// OpenFile opens an existing file
func (c *Client) OpenFile(ctx context.Context, path string) (*File, error) {
    // Implementation
    return nil, nil
}

// ReadFile reads a file
func (c *Client) ReadFile(ctx context.Context, path string) ([]byte, error) {
    // Implementation
    return nil, nil
}

// WriteFile writes to a file
func (c *Client) WriteFile(ctx context.Context, path string, data []byte) error {
    // Implementation
    return nil
}

// DeleteFile deletes a file
func (c *Client) DeleteFile(ctx context.Context, path string) error {
    // Implementation
    return nil
}

// ListDir lists a directory
func (c *Client) ListDir(ctx context.Context, path string) ([]string, error) {
    // Implementation
    return nil, nil
}

// File represents an open file
type File struct {
    fd int
    path string
}

// Read reads from file
func (f *File) Read(p []byte) (int, error) {
    // Implementation
    return 0, nil
}

// Write writes to file
func (f *File) Write(p []byte) (int, error) {
    // Implementation
    return 0, nil
}

// Close closes the file
func (f *File) Close() error {
    // Implementation
    return nil
}
```

### CSI Driver

```go
// CubeFS CSI Driver
package csi

import (
    "context"
    "fmt"
    
    "github.com/container-storage-interface/spec/lib/go/csi"
    "google.golang.org/grpc/codes"
    "google.golang.org/grpc/status"
)

// Driver implements CSI interface
type Driver struct {
    nodeID   string
    endpoint string
    client   *Client
}

// NewDriver creates a new CSI driver
func NewDriver(nodeID, endpoint string, client *Client) *Driver {
    return &Driver{
        nodeID:   nodeID,
        endpoint: endpoint,
        client:   client,
    }
}

// CreateVolume creates a new volume
func (d *Driver) CreateVolume(ctx context.Context, req *csi.CreateVolumeRequest) (*csi.CreateVolumeResponse, error) {
    name := req.GetName()
    if name == "" {
        return nil, status.Error(codes.InvalidArgument, "Volume name must be provided")
    }
    
    capacity := req.GetCapacityRange().GetRequiredBytes()
    
    // Create CubeFS volume
    err := d.client.CreateVolume(ctx, name, capacity)
    if err != nil {
        return nil, status.Errorf(codes.Internal, "Failed to create volume: %v", err)
    }
    
    return &csi.CreateVolumeResponse{
        Volume: &csi.Volume{
            VolumeId:      name,
            CapacityBytes: capacity,
            VolumeContext: req.GetParameters(),
        },
    }, nil
}

// DeleteVolume deletes a volume
func (d *Driver) DeleteVolume(ctx context.Context, req *csi.DeleteVolumeRequest) (*csi.DeleteVolumeResponse, error) {
    volumeID := req.GetVolumeId()
    if volumeID == "" {
        return nil, status.Error(codes.InvalidArgument, "Volume ID must be provided")
    }
    
    err := d.client.DeleteVolume(ctx, volumeID)
    if err != nil {
        return nil, status.Errorf(codes.Internal, "Failed to delete volume: %v", err)
    }
    
    return &csi.DeleteVolumeResponse{}, nil
}

// PublishVolume mounts a volume
func (d *Driver) PublishVolume(ctx context.Context, req *csi.NodePublishVolumeRequest) (*csi.NodePublishVolumeResponse, error) {
    volumeID := req.GetVolumeId()
    targetPath := req.GetTargetPath()
    
    err := d.client.MountVolume(ctx, volumeID, targetPath)
    if err != nil {
        return nil, status.Errorf(codes.Internal, "Failed to mount volume: %v", err)
    }
    
    return &csi.NodePublishVolumeResponse{}, nil
}

// UnpublishVolume unmounts a volume
func (d *Driver) UnpublishVolume(ctx context.Context, req *csi.NodeUnpublishVolumeRequest) (*csi.NodeUnpublishVolumeResponse, error) {
    volumeID := req.GetVolumeId()
    targetPath := req.GetTargetPath()
    
    err := d.client.UnmountVolume(ctx, volumeID, targetPath)
    if err != nil {
        return nil, status.Errorf(codes.Internal, "Failed to unmount volume: %v", err)
    }
    
    return &csi.NodeUnpublishVolumeResponse{}, nil
}

// NodeStageVolume stages a volume
func (d *Driver) NodeStageVolume(ctx context.Context, req *csi.NodeStageVolumeRequest) (*csi.NodeStageVolumeResponse, error) {
    volumeID := req.GetVolumeId()
    stagingTargetPath := req.GetStagingTargetPath()
    
    err := d.client.StagingVolume(ctx, volumeID, stagingTargetPath)
    if err != nil {
        return nil, status.Errorf(codes.Internal, "Failed to stage volume: %v", err)
    }
    
    return &csi.NodeStageVolumeResponse{}, nil
}

// NodeUnstageVolume unstages a volume
func (d *Driver) NodeUnstageVolume(ctx context.Context, req *csi.NodeUnstageVolumeRequest) (*csi.NodeUnstageVolumeResponse, error) {
    volumeID := req.GetVolumeId()
    stagingTargetPath := req.GetStagingTargetPath()
    
    err := d.client.UnstageVolume(ctx, volumeID, stagingTargetPath)
    if err != nil {
        return nil, status.Errorf(codes.Internal, "Failed to unstage volume: %v", err)
    }
    
    return &csi.NodeUnstageVolumeResponse{}, nil
}
```

---

## Fundamentals

### CubeFS Storage Model

#### 1. Block

- Fixed-size data unit (default 4MB)
- Replicated across DataNodes
- Referenced by files

#### 2. File

- Metadata + block references
- Stored in metadata service
- Supports POSIX operations

#### 3. Volume

- Logical container for files
- Configurable replica count
- Storage pool assignment

### Protocol Support

#### 1. POSIX (FUSE)

- Full POSIX compliance
- Standard file operations

#### 2. S3

- S3-compatible API
- Object storage operations

#### 3. NAS

- NFS v3/v4 support
- CIFS/SMB support

---

## Scaling and Deployment Patterns

### Horizontal Scaling

```bash
# Scale CubeFS horizontally
# Add more DataNodes for capacity
# Add more metadata servers for metadata performance
```

### Multi-Region

```bash
# Multi-region deployment
# Primary region: active traffic
# Secondary region: backup/failover
# Tertiary region: disaster recovery
```

### Backup and Recovery

```bash
# Backup CubeFS data
# Use CubeFS snapshot feature
# Export to S3 for long-term storage
```

---

## Additional Resources

### Official Documentation

- [CubeFS](https://cubefs.io/) - Project website
- [CubeFS Documentation](https://cubefs.io/docs/) - Complete documentation
- [CubeFS GitHub](https://github.com/cubefs/cubefs) - Source code

### Community Resources

- [CNCF CubeFS](https://www.cncf.io/projects/cubefs/) - CNCF project page
- [CubeFS Slack](https://kubernetes.slack.com/archives/...) - Community discussion

### Learning Resources

- [CubeFS Getting Started](https://cubefs.io/docs/getting-started/) - Tutorial
- [CubeFS Examples](https://github.com/cubefs/cubefs/tree/master/examples) - Examples

---

*This SKILL.md file was verified and last updated on 2026-04-22. Content based on CNCF CubeFS project and production usage patterns.*
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
