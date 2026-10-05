---




name: argo
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '"Argo in Cloud-Native Engineering - Kubernetes-Native Workflow, CI/CD"
  and Governance'
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  role: reference
  scope: infrastructure
  triggers: argo, cloud-native, container orchestration, engineering, kubernetes-native,
    kubernetes, k8s
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




  related-skills: cncf-artifact-hub, cncf-aws-dynamodb, cncf-aws-ec2, cncf-aws-eks



# Argo in Cloud-Native Engineering

**Category:** workflow  
**Status:** Active  
**Stars:** 14,600  
**Last Updated:** 2026-04-22  
**Primary Language:** Go  
**Documentation:** [https://argoproj.github.io/](https://argoproj.github.io/)  

---

## Purpose and Use Cases

Argo is a family of Kubernetes-native projects providing workflow management, CI/CD, and governance capabilities for cloud-native applications.

### What Problem Does It Solve?

Complex workflow orchestration, CI/CD automation, and governance across Kubernetes clusters. It enables reproducible deployments, audit trails, and policy enforcement for cloud-native applications.

### When to Use This Project

Use Argo Workflows for complex multi-step workflows, Argo CD for GitOps deployment, Argo Events for event-driven automation, or Argo Rollouts for progressive delivery. Ideal when you need Kubernetes-native workflow management with full auditability.

### Key Use Cases

- **Argo Workflows**: Multi-step batch processing, ML pipeline orchestration, data engineering workflows
- **Argo CD**: GitOps continuous deployment, multi-cluster application deployment, app-of-apps patterns
- **Argo Events**: Event-driven workflows, webhook integration, external trigger handling
- **Argo Rollouts**: Progressive delivery, canary deployments, blue-green deployments
- **Argo Workflows Engine**: Generic workflow execution engine for Kubernetes

---

## Architecture Design Patterns

### Core Components

**Argo Workflows:**
- **Workflow Controller**: Main controller managing workflow lifecycle
- **Workflow Executor**: Runs workflow steps in pods
- **Container Runtime Interface**: Docker/Containerd execution
- **Workflow Repository**: CRD for workflow definitions

**Argo CD:**
- **API Server**: REST API for operations
- **Repo Server**: Git repository operations and manifest generation
- **Application Controller**: Kubernetes controller for app synchronization
- **Database**: Cluster state storage

**Argo Events:**
- **Event Bus**: Communication layer (NATS, Kafka)
- **Sensor**: Event processing and trigger execution
- **Event Source**: External event adapters
- **Workflow Controller**: Workflow execution integration

### Component Interactions

**Argo Workflows:**
1. User submits workflow → Workflow Controller creates executor pods
2. Executor runs steps → Updates workflow status → Final state persisted
3. Workflow CRD → API Server → Controller reconciliation loop

**Argo CD:**
1. Git repo changes detected → Repo server fetches manifests
2. Application controller compares desired vs actual state
3. Sync operation applies changes to cluster
4. Health and sync status updated in API

**Argo Events:**
1. External event triggers event source
2. Event source sends to event bus
3. Sensor listens and triggers workflow/execution

### Data Flow Patterns

**Argo Workflows:**
1. Workflow CRD created → Controller analyzes DAG → Creates pod templates → Executor pods run → Status updates
2. Parallel steps execute → Wait for completion → Next step
3. Artifact passing between steps via volumes or HTTP

**Argo CD:**
1. Git webhook → Repo server sync → Application controller compares → Sync or diff → K8s API apply
2. Health assessment → State comparison → Sync decision → Apply manifests

**Argo Events:**
1. Webhook receives → Event source parses → Event bus publishes → Sensor processes → Triggers workflow

### Design Principles

- **Declarative Workflows**: CRDs for workflow definitions
- **GitOps First**: Declarative configuration management
- **Kubernetes Native**: Runs entirely on Kubernetes
- **Extensible**: Custom steps, plugins, and integrations
- **Audit Trail**: Full history and provenance tracking
- **Security**: RBAC, secret management, policy enforcement

---

## Integration Approaches

### Integration with Other CNCF Projects

- **Kubernetes**: Core platform for execution
- **Prometheus**: Metrics collection and monitoring
- **Argo Rollouts**: Progressive delivery extension
- **Tekton**: Alternative workflow engine (complementary)
- **Helm**: Chart deployment integration
- **CoreDNS**: Service discovery for workflow steps
- **OpenTelemetry**: Distributed tracing integration
- **Kyverno**: Policy validation for workflows

### API Patterns

- **REST API**: Argo CD web UI and CLI communication
- **gRPC API**: Internal service communication
- **Webhook API**: Git and external event triggers
- **Kubernetes API**: CRD operations
- **Event Bus API**: Argo Events message passing

### Configuration Patterns

**Argo Workflows:**
- **YAML Workflow Definitions**: Kubernetes CRDs
- **Parameters**: Input values and variables
- **Artifacts**: Input/output data passing
- **Steps**: Workflow execution units
- **DAG**: Directed acyclic graph execution

**Argo CD:**
- **Application CRD**: Application definitions
- **Project CRD**: Access control and resource grouping
- **Repository Connections**: Git, Helm, Kustomize configs
- **Sync Policy**: Automated or manual sync
- **Project Role**: RBAC configuration

### Extension Mechanisms

- **Workflow Templates**: Reusable workflow definitions
- **Step Templates**: Reusable step configurations
- **Plugin System**: Custom step types
- **Webhook Integrations**: External event triggers
- **RBAC Policies**: Fine-grained access control

---

## Common Pitfalls and How to Avoid Them

### Misconfigurations

- **Resource Limits**: Not setting CPU/memory for workflow steps
- **Artifact Storage**: Missing PVC or S3 configuration
- **RBAC Permissions**: Missing service account permissions
- **Image Pull Secrets**: Not configuring for private registries
- **Network Policies**: Blocking pod-to-pod communication
- **Git Credentials**: Missing or expired repository credentials
- **Webhook Secrets**: Not verifying webhook signatures

### Performance Issues

- **Workflow Overhead**: Too many small steps causing pod startup latency
- **Artifact Size**: Large artifacts causing storage bottlenecks
- **Concurrent Workflows**: Resource contention and queueing
- **Git Polling Frequency**: Excessive repository polling
- **Controller Load**: High reconciliation overhead

### Operational Challenges

- **Workflow Cleanup**: Orphaned pods and resources
- **Retry Logic**: Proper handling of transient failures
- **Timeout Management**: Workflows hanging indefinitely
- **Artifact Retention**: Storage exhaustion from old artifacts
- **Git Branch Strategy**: Merge conflicts and race conditions
- **Cluster Federation**: Multi-cluster deployment complexity

### Security Pitfalls

- **Secret Exposure**: Secrets in workflow step outputs
- **Privilege Escalation**: Overly permissive service accounts
- **Image Verification**: Running untrusted container images
- **Network Isolation**: Workflows accessing internal services
- **Audit Log Retention**: Insufficient logging for compliance
- **RBAC Misconfiguration**: Users accessing unauthorized workflows

---

## Coding Practices

### Idiomatic Configuration

- **Declarative YAML**: Workflow definitions as Kubernetes resources
- **GitOps**: Store workflows in Git repositories
- **Parameterization**: Use parameters for reusability
- **Artifact References**: Pass data via artifacts, not environment variables
- **Template Reuse**: Create templates for common step patterns
- **Error Handling**: Use retry logic and error handling

### API Usage Patterns

- **kubectl apply**: Create and update workflows
- **argo CLI**: Workflow submission and management
- **argocd CLI**: CD operations and status checks
- **Argo Server API**: Programmatic workflow management
- **Kubernetes Client Libraries**: Integration with application code

### Observability Best Practices

- **Metrics Collection**: PromQL queries for workflow metrics
- **Logging**: Standardized logging in workflow steps
- **Tracing**: OpenTelemetry integration for distributed tracing
- **Dashboard**: Grafana dashboards for workflow status
- **Alerting**: Notifications for failed workflows
- **Audit Trail**: Complete operation history

### Testing Strategies

- **Unit Tests**: Step-level testing
- **Integration Tests**: Workflow execution testing
- **E2E Tests**: Full workflow validation
- **Artifact Tests**: Data passing validation
- **Security Tests**: RBAC and policy validation

### Development Workflow

- **Local Testing**: minikube/kind for workflow testing
- **Debugging**: argo logs, argo watch, kubectl describe
- **Version Control**: Git-based workflow versioning
- **CI/CD Pipeline**: Automated workflow testing
- **Tools**: argo, argocd, kubectl, Lens

---

## Fundamentals

### Essential Concepts

- **Workflow**: Kubernetes CRD for workflow definition
- **Steps**: Individual units of execution
- **DAG**: Directed acyclic graph of steps
- **Artifacts**: Input/output data passing
- **Parameters**: Workflow input values
- **Template**: Reusable step definition
- **Pod Template**: Execution environment configuration
- **Exit Handler**: Cleanup and notification logic
- **CronWorkflow**: Scheduled workflow execution

**Argo CD Specific:**
- **Application**: Deployed application definition
- **Project**: Resource grouping and access control
- **Sync**: Synchronize cluster to Git state
- **Health**: Application health status
- **Sync Policy**: Automated sync configuration
- **Revision History**: Application deployment history

### Terminology Glossary

- **DAG**: Directed acyclic graph workflow pattern
- **Artifact**: Data passed between workflow steps
- **Parameter**: Workflow input value
- **Template**: Reusable workflow component
- **Executor**: Pod running workflow steps
- **Sync**: Align cluster state with Git state
- **Health**: Current application status
- **Revision**: Git commit reference

### Data Models and Types

- **Workflow Spec**: Desired workflow configuration
- **Workflow Status**: Current execution state
- **Step Status**: Individual step execution status
- **Artifact Location**: Storage reference for artifacts
- **Parameter Values**: Runtime parameter values
- **Git Repository**: Repository connection configuration
- **Application State**: Sync and health status

### Lifecycle Management

**Workflow Lifecycle:**
1. Submit → 2. Pending → 3. Running → 4. Success/Failed → 5. Cleanup

**Argo CD Lifecycle:**
1. Application create → 2. Sync → 3. Health assessment → 4. Auto-sync → 5. Rollback

### State Management

- **Workflow Status**: Current execution state stored in CR
- **Step Status**: Individual step results
- **Artifact Storage**: Reference to artifact location
- **Git State**: Repository branch and revision
- **Cluster State**: Current deployment status
- **Revision History**: Full deployment history

---

## Scaling and Deployment Patterns

### Horizontal Scaling

- **Controller Scaling**: Multiple workflow controllers for parallel execution
- **Executor Scaling**: Pod-based parallel step execution
- **API Server Scaling**: Multiple Argo CD API servers
- **Repo Server Scaling**: Parallel Git operations
- **Controller Scaling**: Multiple controllers for load distribution

### High Availability

- **Controller HA**: Multiple controller replicas
- **State Persistence**: CRDs for workflow state
- **Etcd HA**: Kubernetes cluster HA ensures workflow state availability
- **API Server HA**: Multiple API server instances
- **Database HA**: PostgreSQL/MySQL HA for Argo CD

### Production Deployments

**Argo Workflows:**
- **Execution Environment**: Proper RBAC and resource limits
- **Artifact Storage**: S3, NFS, or persistent volumes
- **Monitoring**: Prometheus metrics integration
- **Security**: Network policies and PodSecurityPolicies
- **Backup**: CRD state backup strategies

**Argo CD:**
- **Repository Configuration**: Secure Git access (SSH keys, tokens)
- **RBAC Configuration**: Fine-grained access control
- **Webhook Setup**: Secure Git webhook configuration
- **Certificate Management**: TLS for API server
- **Multi-tenancy**: Namespace isolation and project separation

### Upgrade Strategies

- **CRD Migration**: Handle CRD schema changes
- **Controller Rolling Update**: Zero-downtime controller updates
- **Argo CD Rollout**: Application reconciliation during upgrade
- **Database Migration**: Argo CD database schema updates
- **Git Repository Strategy**: Version control for configurations

### Resource Management

- **CPU/Memory Limits**: Appropriate resource requests for workflows
- **Artifact Storage Quotas**: Prevent storage exhaustion
- **Concurrent Workflow Limits**: Prevent cluster resource exhaustion
- **Pod Security Policies**: Resource isolation
- **Priority Classes**: Workflow priority management

---

## Additional Resources

- **Official Documentation:** [https://argoproj.github.io/](https://argoproj.github.io/)
- **GitHub Repository:** [github.com/argoproj/argo-workflows](https://github.com/argoproj/argo-workflows)
- **CNCF Project Page:** [cncf.io/projects/argo/](https://www.cncf.io/projects/argo/)
- **Community:** Check the GitHub repository for community channels
- **Versioning:** Refer to project's release notes for version-specific features

---

## Examples

### Argo Workflows DAG for Data Pipeline


```yaml
# Data processing workflow with DAG execution
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: data-pipeline-
spec:
  entrypoint: data-pipeline
  templates:
  - name: data-pipeline
    steps:
    - - name: extract
        template: extract
    - - name: transform
        template: transform
    - - name: load
        template: load

  - name: extract
    container:
      image: python:3.9-slim
      command: [python]
      args: ["-c", "import json; print(json.dumps({'data': 'extracted'}))"]
      volumeMounts:
      - name: scratch
        mountPath: /data
    outputs:
      artifacts:
      - name: data
        path: /data/extracted.json
        raw:
          dataKey: data

  - name: transform
    container:
      image: python:3.9-slim
      command: [python]
      args: ["-c", "import json; print(json.dumps({'transformed': True}))"]
      volumeMounts:
      - name: scratch
        mountPath: /data
    inputs:
      artifacts:
      - name: data
        path: /data/
        raw:
          dataKey: data

  - name: load
    container:
      image: python:3.9-slim
      command: [python]
      args: ["-c", "print('Data loaded successfully')"]

  volumes:
  - name: scratch
    emptyDir: {}
```

### Argo CD Application for GitOps Deployment


```yaml
# Argo CD Application for GitOps continuous deployment
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/myapp.git
    targetRevision: HEAD
    path: k8s
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
    - FailOnSharedResource=true
  revisionHistoryLimit: 10
```

### Argo Rollouts Canary Deployment


```yaml
# Argo Rollouts Canary deployment with progressive delivery
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: myapp
spec:
  replicas: 5
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myregistry/myapp:v1
        ports:
        - containerPort: 8080
  strategy:
    canary:
      steps:
      - setWeight: 20
      - pause: {duration: 5m}
      - setWeight: 40
      - pause: {duration: 5m}
      - setWeight: 60
      - pause: {duration: 5m}
      - setWeight: 80
      - pause: {duration: 5m}
      - setWeight: 100
      analysis:
        templates:
        - templateName: success-rate
        startingStep: 2
---
  related-skills: cncf-artifact-hub, cncf-aws-dynamodb, cncf-aws-ec2, cncf-aws-eks
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate
spec:
  args:
  - name: service-name
  metrics:
  - name: success-rate
    interval: 1m
    count: 5
    successCondition: result[0] >= 0.95
    provider:
      prometheus:
        address: http://prometheus:9090
        query: |
          sum(rate(http_requests_total{service="{{args.service-name}}",status=~"2.."}[1m]))
          /
          sum(rate(http_requests_total{service="{{args.service-name}}"}[1m]))
```
## Tutorial

This tutorial will guide you through installing, configuring, and using Argo projects from scratch.

### Prerequisites

Before beginning, ensure you have:
- A running Kubernetes cluster (minikube, kind, EKS, GKE, AKS, or any other)
- `kubectl` configured to access your cluster
- `helm` CLI (for Helm installation method)
- `argo` CLI (for workflow operations)
- `argocd` CLI (for CD operations)

Verify your setup:

```bash
# Check cluster connectivity
kubectl cluster-info

# Verify kubectl configuration
kubectl get nodes

# Check Helm installation
helm version
```

---
  related-skills: cncf-artifact-hub, cncf-aws-dynamodb, cncf-aws-ec2, cncf-aws-eks

### 1. Installation

Argo projects can be installed using `kubectl apply` (manifests) or Helm charts. Both methods are covered below.

#### Method 1: Using kubectl apply

**Install Argo Workflows:**

```bash
# Apply Argo Workflows CRDs and controller
kubectl create namespace argo
kubectl apply -n argo -f https://github.com/argoproj/argo-workflows/releases/latest/download/install.yaml

# Verify installation
kubectl get pods -n argo -l app=argo-workflows
```

**Install Argo CD:**

```bash
# Create namespace and apply Argo CD manifests
kubectl create namespace argocd
kubectl apply -n argocd -f https://github.com/argoproj/argo-cd/releases/latest/download/install.yaml

# Verify installation
kubectl get pods -n argocd
```

**Install Argo Events:**

```bash
# Apply Argo Events CRDs first
kubectl apply -f https://github.com/argoproj/argo-events/releases/latest/download/crds.yaml

# Create namespace and apply Argo Events
kubectl create namespace argo-events
kubectl apply -n argo-events -f https://github.com/argoproj/argo-events/releases/latest/download/manifests.yaml

# Verify installation
kubectl get pods -n argo-events
```

**Install Argo Rollouts:**

```bash
# Create namespace and apply Argo Rollouts
kubectl create namespace argo-rollouts
kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml

# Verify installation
kubectl get pods -n argo-rollouts
```

#### Method 2: Using Helm

**Install Argo Workflows with Helm:**

```bash
# Add the Argo Helm repository
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update

# Install Argo Workflows
helm install argo argo/argo-workflows \
  --namespace argo \
  --create-namespace \
  --wait

# Verify installation
helm list -n argo
kubectl get pods -n argo
```

**Install Argo CD with Helm:**

```bash
# Add the Argo CD Helm repository
helm repo add argo-cd https://argoproj.github.io/argo-helm

# Install Argo CD with server disabled (for CLI-only setup)
helm install argocd argo-cd/argocd \
  --namespace argocd \
  --create-namespace \
  --set server.enabled=false \
  --wait

# Verify installation
helm list -n argocd
kubectl get pods -n argocd
```

**Install Argo Events with Helm:**

```bash
# Add the Argo Events Helm repository
helm repo add argo-events https://argoproj.github.io/argo-helm

# Install Argo Events
helm install argo-events argo-events/argo-events \
  --namespace argo-events \
  --create-namespace \
  --wait

# Verify installation
helm list -n argo-events
kubectl get pods -n argo-events
```

**Install Argo Rollouts with Helm:**

```bash
# Add the Argo Rollouts Helm repository
helm repo add argo-rollouts https://argoproj.github.io/argo-helm

# Install Argo Rollouts
helm install argo-rollouts argo-rollouts/argo-rollouts \
  --namespace argo-rollouts \
  --create-namespace \
  --wait

# Verify installation
helm list -n argo-rollouts
kubectl get pods -n argo-rollouts
```

---

### 2. Basic Configuration

#### Argo Workflows Configuration

**Access the Argo Workflows UI:**

```bash
# Port-forward the Argo Workflows server
kubectl -n argo port-forward svc/argo-server 2746:2746

# Access UI at http://localhost:2746
```

**Configure Artifact Storage (S3 example):**

```yaml
# Create a ConfigMap for artifact storage configuration
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: argo-workflows-artifact-repositories
  namespace: argo
data:
  archiveLogs: "false"
  s3-artifact-repo: |
    endpoint: s3.amazonaws.com
    bucket: my-argo-artifacts
    keyFormat: workflows/{{ workflow.name }}/{{ pod.name }}
    region: us-east-1
    insecure: false
    accessKeySecret:
      name: s3-secret
      key: access-key
    secretKeySecret:
      name: s3-secret
      key: secret-key
EOF

# Set as default artifact repository
kubectl -n argo patch configmap/argo-workflows \
  -p '{"data":{"config":"artifactRepository:\n  s3ArtifactRepo: s3-artifact-repo"}}'
```

**Configure RBAC for Workflows:**

```yaml
# Create a ServiceAccount for workflow execution
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ServiceAccount
metadata:
  name: workflow-sa
  namespace: argo
---
  related-skills: cncf-artifact-hub, cncf-aws-dynamodb, cncf-aws-ec2, cncf-aws-eks
# Create Role for workflow execution
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: workflow-role
  namespace: argo
rules:
- apiGroups: [""]
  resources: ["pods", "pods/log"]
  verbs: ["get", "watch", "patch"]
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["argoproj.io"]
  resources: ["workflows", "workflowtemplates", "cronworkflows"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
---
  related-skills: cncf-artifact-hub, cncf-aws-dynamodb, cncf-aws-ec2, cncf-aws-eks
# Bind role to service account
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: workflow-role-binding
  namespace: argo
subjects:
- kind: ServiceAccount
  name: workflow-sa
  namespace: argo
roleRef:
  kind: Role
  name: workflow-role
  apiGroup: rbac.authorization.k8s.io
EOF
```

#### Argo CD Configuration

**Access the Argo CD UI:**

```bash
# Get the initial admin password
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d; echo

# Port-forward the Argo CD server
kubectl -n argocd port-forward svc/argocd-server 8080:443

# Access UI at https://localhost:8080
# Login with user: admin, password: (from above)
```

**Configure Repository Credentials:**

```bash
# Add a Git repository for deployment
argocd repo add https://github.com/myorg/myapp.git \
  --username mygithubuser \
  --password mygithubtoken

# Verify repository configuration
argocd repo list

# Or use SSH with a private key
argocd repo add git@github.com:myorg/myapp.git \
  --ssh-private-key-path ~/.ssh/id_rsa
```

**Configure RBAC for Argo CD:**

```yaml
# Configure RBAC policies in argocd-rbac-configmap
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-rbac-cfg
  namespace: argocd
data:
  policy.csv: |
    # Admin role has full access
    p, role:admin, applications, *, */*, allow
    p, role:admin, clusters, *, *, allow
    p, role:admin, repositories, *, *, allow
    p, role:admin, settings, *, *, allow
    p, role:admin, logs, *, *, allow
    p, role:admin, events, *, *, allow
    
    # Developer role can sync and sync applications in dev projects
    p, role:developer, applications, sync, */*, allow
    p, role:developer, applications, override, */*, allow
    
  policy.default: role:readonly
  scopes: '[groups]'
EOF

# Configure keycloak or other OIDC provider
# (See official documentation for detailed OIDC configuration)
```

#### Argo Events Configuration

**Install NATS Event Bus:**

```bash
# Argo Events uses NATS as the default event bus
# Install NATS via Helm
helm repo add nats https://nats-io.github.io/k8s/helm/
helm repo update

# Install NATS
kubectl create namespace nats-io
helm install nats nats/nats \
  --namespace nats-io \
  --wait

# Verify NATS installation
kubectl get pods -n nats-io
```

**Create a Basic Event Source:**

```yaml
# Create an HTTP webhook event source
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: event-source-config
  namespace: argo-events
data:
  webhook.json: |
    {
      "source": {
        "webhook": {
          "endpoint": "/webhook",
          "port": "12000",
          "sourceType": "webhook",
          "webhook": {
            "method": "POST"
          }
        }
      },
      "type": "webhook",
      "context": {
        "type": "com.argoproj.event.source.webhook",
        "source": "my-webhook"
      },
      "data": {
        "path": "body"
      }
    }
EOF
```

**Create a Sensor for Event Processing:**

```yaml
# Create a sensor that triggers a workflow on webhook events
cat <<EOF | kubectl apply -f -
apiVersion: argoproj.io/v1alpha1
kind: Sensor
metadata:
  name: webhook-sensor
  namespace: argo-events
spec:
  template:
    spec:
      containers:
      - name: sensor
        image: argoproj/sensor:v3.5.0
        command: ["/usr/local/bin/sensor"]
      serviceAccountName: argo-events-sa
  dependencies:
  - name: webhook-dep
    eventSourceName: webhook-event-source
    eventName: webhook
  triggers:
  - template:
      name: workflow-trigger
      source:
        webhook:
          endpoint: /trigger
          port: "12001"
          method: "POST"
      kubernetes:
        group: argoproj.io
        version: v1alpha1
        resource: workflows
        operation: create
        source:
          resource:
            apiVersion: argoproj.io/v1alpha1
            kind: Workflow
            metadata:
              generateName: webhook-workflow-
              namespace: argo
            spec:
              entrypoint: main
              templates:
              - name: main
                container:
                  image: alpine:3.18
                  command: [sh, -c]
                  args: ["echo 'Triggered by webhook!'"]
        parameters:
        - src:
            dependencyName: webhook-dep
            dataKey: body
          dest: spec.arguments.parameters.0.value
EOF
```

**Create Event Source and Sensor Resources:**

```yaml
# Create the webhook event source
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: webhook-event-source
  namespace: argo-events
data:
  webhook.json: |
    {
      "type": "webhook",
      "source": {
        "type": "webhook",
        "webhook": {
          "endpoint": "/webhook",
          "port": "12000",
          "sourceType": "webhook",
          "method": "POST"
        }
      },
      "context": {
        "type": "com.argoprojo.event.source.webhook",
        "source": "github-webhook"
      },
      "data": {
        "path": "body"
      }
    }
EOF

# Create the webhook sensor
cat <<EOF | kubectl apply -f -
apiVersion: argoproj.io/v1alpha1
kind: Sensor
metadata:
  name: github-webhook-sensor
  namespace: argo-events
spec:
  template:
    spec:
      serviceAccountName: argo-events-sa
  dependencies:
  - name: github-webhook
    eventSourceName: webhook-event-source
    eventName: webhook
  triggers:
  - template:
      name: argo-workflow-trigger
      argoWorkflow:
        group: argoproj.io
        version: v1alpha1
        resource: workflows
        operation: create
        source:
          resource:
            apiVersion: argoproj.io/v1alpha1
            kind: Workflow
            metadata:
              generateName: github-workflow-
              namespace: argo
            spec:
              entrypoint: main
              arguments:
                parameters:
                - name: commit-sha
                  value: "unknown"
              templates:
              - name: main
                container:
                  image: alpine:3.18
                  command: [sh, -c]
                  args:
                  - |
                    echo "Building commit: {{ arguments.parameters.0.value }}"
                    echo "Event: {{ dependencies.github-webhook.body }}"
EOF
```

#### Argo Rollouts Configuration

**Access the Rollouts Dashboard:**

```bash
# Port-forward the Argo Rollouts dashboard
kubectl -n argo-rollouts port-forward svc/argo-rollouts 3100:3100

# Access dashboard at http://localhost:3100
```

**Install Kubectl Rollouts Plugin:**

```bash
# Download and install kubectl rollouts plugin
curl -sLO "https://github.com/argoproj/argo-rollouts/releases/latest/download/kubectl-rollouts-$(uname -s)-$(uname -m)"
chmod +x kubectl-rollouts-$(uname -s)-$(uname -m)
sudo mv kubectl-rollouts-$(uname -s)-$(uname -m) /usr/local/bin/kubectl-rollouts

# Verify installation
kubectl rollouts version
```

---
  related-skills: cncf-artifact-hub, cncf-aws-dynamodb, cncf-aws-ec2, cncf-aws-eks

### 3. Basic Usage Examples

#### Submitting Your First Argo Workflow

**Create a simple "Hello World" workflow:**

```yaml
# hello-world.yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: hello-world-
spec:
  entrypoint: whalesay
  templates:
  - name: whalesay
    container:
      image: docker/whalesay:latest
      command: [cowsay]
      args: ["Hello, Argo Workflows!"]
```

**Submit the workflow:**

```bash
# Submit the workflow
argo submit hello-world.yaml --watch

# Or submit without watching
argo submit hello-world.yaml

# List workflows
argo list

# Get workflow status
argo get hello-world-xxxxx
```

**View workflow logs:**

```bash
# View logs for a specific workflow
argo logs hello-world-xxxxx

# Watch workflow execution in real-time
argo watch hello-world-xxxxx

# Get logs for a specific step
argo logs hello-world-xxxxx whalesay
```

#### Creating Your First Argo CD Application

**Create an application YAML file:**

```yaml
# myapp.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/argoproj/argocd-example-apps.git
    targetRevision: HEAD
    path: guestbook
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
```

**Apply the application:**

```bash
# Apply the application manifest
kubectl apply -f myapp.yaml

# Or use argocd CLI
argocd app create myapp \
  --project default \
  --repo https://github.com/argoproj/argocd-example-apps.git \
  --path guestbook \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace default \
  --sync-policy automated

# List applications
argocd app list

# Get application details
argocd app get myapp
```

**Sync the application:**

```bash
# Sync the application to the cluster
argocd app sync myapp

# Sync with dry-run to see what would be applied
argocd app sync myapp --dry-run

# Sync with pruning enabled
argocd app sync myapp --prune
```

#### Setting Up Git Webhook for Automated Sync

**Configure GitHub webhook:**

```bash
# Get Argo CD webhook secret
WEBHOOK_SECRET=$(kubectl -n argocd get secret argocd-secret \
  -o jsonpath='{.data.webhook.gitlab.secret}' | base64 -d)

# Or generate a new secret
WEBHOOK_SECRET=$(openssl rand -hex 20)
kubectl -n argocd patch secret argocd-secret \
  --type='string' \
  -p="{\"data\": {\"webhook.github.secret\": \"$(echo -n $WEBHOOK_SECRET | base64)\"}}"

# Configure webhook in GitHub
# 1. Go to your repository on GitHub
# 2. Settings → Webhooks → Add webhook
# 3. Set Payload URL: https://argocd.example.com/api/webhook
# 4. Set Content type: application/json
# 5. Set Secret: (use the WEBHOOK_SECRET)
# 6. Select events: Just the push event
```

**Create an application with webhook integration:**

```yaml
# myapp-with-webhook.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
  annotations:
    argocd.argoproj.io/sync-wave: "0"
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/myapp.git
    targetRevision: main
    path: manifests
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
  revisionHistoryLimit: 10
```

#### Deploying Your First Canary Rollout

**Create a Deployment with Rollout strategy:**

```yaml
# myapp-rollout.yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: myapp
spec:
  replicas: 5
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myregistry/myapp:v1
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "500m"
  strategy:
    canary:
      steps:
      - setWeight: 20  # Route 20% traffic to canary
      - pause: {duration: 5m}  # Wait 5 minutes
      - setWeight: 40  # Route 40% traffic to canary
      - pause: {duration: 5m}
      - setWeight: 60  # Route 60% traffic to canary
      - pause: {duration: 5m}
      - setWeight: 80  # Route 80% traffic to canary
      - pause: {duration: 5m}
      - setWeight: 100  # Route 100% traffic to canary
      analysis:
        templates:
        - templateName: success-rate
        startingStep: 2  # Start analysis after setWeight: 40
---
  related-skills: cncf-artifact-hub, cncf-aws-dynamodb, cncf-aws-ec2, cncf-aws-eks
# Create the AnalysisTemplate for health checks
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate
spec:
  args:
  - name: service-name
  metrics:
  - name: success-rate
    interval: 1m
    count: 5
    successCondition: result[0] >= 0.95
    provider:
      prometheus:
        address: http://prometheus-server.prometheus.svc.cluster.local:9090
        query: |
          sum(rate(http_requests_total{service="{{args.service-name}}",status=~"2.."}[1m]))
          /
          sum(rate(http_requests_total{service="{{args.service-name}}"}[1m]))
```

**Apply the rollout:**

```bash
# Apply the rollout
kubectl apply -f myapp-rollout.yaml

# Watch rollout progress
kubectl rollouts get rollout myapp --watch

# Check rollout status
kubectl rollouts status myapp

# List rollouts
kubectl rollouts list rollouts

# View rollout history
kubectl rollouts history myapp

# Promote rollout if analysis fails
kubectl rollouts promote myapp

# Undo rollout to previous version
kubectl rollouts undo myapp
```

---
  related-skills: cncf-artifact-hub, cncf-aws-dynamodb, cncf-aws-ec2, cncf-aws-eks

### 4. Common Operations

#### Monitoring Workflows

**Watch workflow execution:**

```bash
# Watch a specific workflow
argo watch hello-world-xxxxx

# Watch all workflows in a namespace
argo watch --namespace argo

# Watch with specific labels
argo watch -l app=myapp --namespace argo
```

**View workflow logs:**

```bash
# View logs for all steps
argo logs hello-world-xxxxx

# View logs with follow mode
argo logs -f hello-world-xxxxx

# View logs for a specific step
argo logs hello-world-xxxxx step-name

# Download logs to a file
argo logs hello-world-xxxxx > workflow.log
```

**Workflow status commands:**

```bash
# List all workflows
argo list

# List workflows with specific status
argo list --phase Succeeded
argo list --phase Failed

# List workflows from last 24 hours
argo list --minutes 1440

# Get detailed workflow info
argo get hello-world-xxxxx -o wide

# Get workflow YAML
argo get hello-world-xxxxx -o yaml
```

#### Syncing Applications with Argo CD

**Sync an application:**

```bash
# Sync an application
argocd app sync myapp

# Sync with dry-run
argocd app sync myapp --dry-run

# Sync multiple applications
argocd app sync myapp1 myapp2

# Sync with prune and delete policies
argocd app sync myapp --prune --cascade
```

**Application status and diff:**

```bash
# Get application status
argocd app get myapp

# Show diff between Git and cluster
argocd app diff myapp

# Show diff for specific path
argocd app diff myapp --path k8s/deployment.yaml
```

**Sync history and rollback:**

```bash
# List sync history
argocd app history myapp

# Rollback to a specific revision
argocd app rollback myapp 3

# Get application info with history
argocd app get myapp --history
```

#### Viewing Rollout Status

**Rollout status commands:**

```bash
# Get rollout status
kubectl rollouts status myapp

# Watch rollout progress
kubectl rollouts status myapp --watch

# Get detailed rollout info
kubectl rollout status deployment/myapp

# List all rollouts
kubectl rollouts list rollouts

# List rollouts with specific label
kubectl rollouts list rollouts -l app=myapp
```

**Rollout history and promotion:**

```bash
# View rollout history
kubectl rollouts history myapp

# View specific revision details
kubectl rollouts history myapp --revision 3

# Promote rollout (skip analysis)
kubectl rollouts promote myapp

# Abort rollout
kubectl rollouts abort myapp

# Restart rollout
kubectl rollouts restart myapp
```

**Canary-specific commands:**

```bash
# Get canary status
kubectl get rollout myapp -o yaml | grep -A 10 "canary"

# View canary steps
kubectl rollout status myapp

# Set canary weight manually
kubectl annotate rollout myapp argo-rollouts.argoproj.io/step-index=2

# Pause rollout at specific step
kubectl annotate rollout myapp argo-rollouts.argoproj.io/pause=

# Resume paused rollout
kubectl annotate rollout myapp argo-rollouts.argoproj.io/pause-
```

---

### Best Practices

#### Workflow Best Practices

1. **Resource Management**: Always set resource requests and limits for workflow containers
2. **Artifact Cleanup**: Implement artifact retention policies to prevent storage exhaustion
3. **Error Handling**: Use retry logic for transient failures
4. **Security**: Use dedicated service accounts with minimal permissions
5. **Idempotency**: Design workflow steps to be idempotent for reliable retries
6. **Monitoring**: Set up alerts for failed workflows

#### Argo CD Best Practices

1. **GitOps Principles**: Keep all configurations in Git with proper version control
2. **RBAC**: Implement fine-grained access control using projects and roles
3. **Webhook Security**: Always use webhook secrets and verify signatures
4. **Sync Windows**: Define sync windows for controlled deployment schedules
5. **Health Checks**: Implement custom health assessments for applications
6. **Audit Logging**: Enable and monitor Argo CD audit logs

#### Argo Events Best Practices

1. **Event Bus Scaling**: Use a dedicated, scalable event bus for production
2. **Sensor Isolation**: Separate sensors by environment and purpose
3. **Error Handling**: Implement retry logic for failed triggers
4. **Security**: Use TLS for event bus communication
5. **Monitoring**: Monitor event throughput and trigger success rates

#### Argo Rollouts Best Practices

1. **Gradual Rollout**: Use gradual weight increases for canary deployments
2. **Health Checks**: Implement comprehensive metrics analysis
3. **Rollback Strategy**: Define clear rollback criteria and thresholds
4. **Monitoring**: Monitor rollouts with dedicated dashboards
5. **Testing**: Test canary strategies in staging before production
6. **Traffic Splitting**: Use service mesh for precise traffic control

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
