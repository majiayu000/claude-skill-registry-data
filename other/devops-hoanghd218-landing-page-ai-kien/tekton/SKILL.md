---
name: Tekton
description: Tekton Pipelines CI/CD best practices for Kubernetes-native workflows. USE WHEN working with Tekton tasks, pipelines, triggers, building container images, GitOps integration, or cloud-native CI/CD.
---

# Tekton

Expert guidance on Tekton Pipelines, a Kubernetes-native CI/CD framework for building, testing, and deploying applications with declarative, reusable workflows.

### Context Detection

**This skill activates when:**
- Current directory contains Tekton YAML files (Task, Pipeline, PipelineRun, etc.)
- User asks about Tekton tasks, pipelines, or triggers
- User mentions `tkn` CLI commands
- Files contain `tekton.dev/v1` or `triggers.tekton.dev` API versions
- User is troubleshooting pipeline runs or debugging CI/CD workflows

## Workflow Routing

**When executing a workflow, output this notification directly:**

```
Running the **WorkflowName** workflow from the **Tekton** skill...
```

| Workflow | Trigger | File |
|----------|---------|------|
| **Debug** | "debug pipeline", "troubleshoot task", "pipeline failing", "taskrun error" | `workflows/Debug.md` |
| **TknCli** | "tkn command", "view logs", "pipeline run", "task run" | `workflows/TknCli.md` |
| **Tasks** | "create task", "task definition", "step", "taskrun" | `workflows/Tasks.md` |
| **Pipelines** | "create pipeline", "pipeline workflow", "pipelinerun" | `workflows/Pipelines.md` |
| **Triggers** | "webhook", "eventlistener", "trigger", "github integration" | `workflows/Triggers.md` |
| **Build** | "build image", "kaniko", "buildah", "container build" | `workflows/Build.md` |
| **GitOps** | "argocd", "flux", "gitops integration", "deployment automation" | `workflows/GitOps.md` |
| **BestPractices** | "tekton best practices", "optimization", "security" | `workflows/BestPractices.md` |

## Quick Reference

### Essential tkn Commands

```bash
# Pipeline operations
tkn pipeline list
tkn pipeline describe <pipeline-name>
tkn pipeline start <pipeline-name>
tkn pipeline delete <pipeline-name>

# PipelineRun operations
tkn pipelinerun list
tkn pipelinerun describe <pipelinerun-name>
tkn pipelinerun logs <pipelinerun-name> -f
tkn pipelinerun cancel <pipelinerun-name>
tkn pipelinerun delete <pipelinerun-name>

# Task operations
tkn task list
tkn task start <task-name>
tkn taskrun logs <taskrun-name> -f

# ClusterTask operations (deprecated - use resolvers)
tkn clustertask list
```

### Common Aliases

```bash
alias tkn-logs='tkn pipelinerun logs --last -f'
alias tkn-list='tkn pipelinerun list'
alias tkn-desc='tkn pipelinerun describe --last'
alias tkn-cancel='tkn pipelinerun cancel --last'
```

## Core Concepts

### Tekton Building Blocks

**Task**: Single unit of work with one or more Steps
- Reusable, parameterized
- Executes in containers
- Can emit Results (<4KB)
- Declares Workspace requirements

**Pipeline**: Orchestrates multiple Tasks
- Defines task execution order (sequential/parallel)
- Manages data flow between tasks
- DAG (Directed Acyclic Graph) execution

**Trigger**: Event-driven pipeline execution
- EventListener: Listens for webhooks
- TriggerBinding: Extracts event data
- TriggerTemplate: Creates PipelineRun/TaskRun

**Workspace**: Shared filesystem storage
- PersistentVolumeClaim (best for sharing)
- emptyDir (temporary)
- ConfigMap/Secret (configuration)

### Task Example

```yaml
apiVersion: tekton.dev/v1
kind: Task
metadata:
  name: hello-world
spec:
  params:
    - name: greeting
      description: The greeting message
      default: "Hello"
  steps:
    - name: echo
      image: alpine
      script: |
        echo "$(params.greeting), World!"
```

### Pipeline Example

```yaml
apiVersion: tekton.dev/v1
kind: Pipeline
metadata:
  name: build-deploy
spec:
  params:
    - name: git-url
    - name: image-name
  workspaces:
    - name: shared-data
  tasks:
    - name: clone
      taskRef:
        name: git-clone
      workspaces:
        - name: output
          workspace: shared-data
      params:
        - name: url
          value: $(params.git-url)

    - name: build
      taskRef:
        name: kaniko
      runAfter:
        - clone
      workspaces:
        - name: source
          workspace: shared-data
      params:
        - name: IMAGE
          value: $(params.image-name)
```

## Common Workflow Patterns

### CI/CD Pipeline Pattern

```
1. Git Clone    → Fetch source code
2. Test         → Run unit/integration tests
3. Build        → Build container image (Kaniko/Buildah)
4. Scan         → Security scan (Trivy)
5. Push         → Push to container registry
6. Deploy       → Update GitOps repo or deploy directly
```

### Task Execution Control

**Sequential execution:**
```yaml
- name: build
  runAfter:
    - test
```

**Parallel execution:**
```yaml
- name: lint
  # No runAfter - runs in parallel
- name: test
  # No runAfter - runs in parallel
```

**Conditional execution:**
```yaml
- name: deploy-prod
  when:
    - input: "$(params.environment)"
      operator: in
      values: ["production"]
```

**Cleanup (always runs):**
```yaml
finally:
  - name: cleanup
    taskRef:
      name: cleanup-workspace
```

## Tekton Hub Integration

**Reference tasks from Tekton Hub:**
```yaml
taskRef:
  resolver: hub
  params:
    - name: name
      value: git-clone
    - name: version
      value: "0.10.0"
```

**Popular Hub Tasks:**
- `git-clone`: Clone Git repositories
- `kaniko`: Build and push container images
- `kubernetes-actions`: Run kubectl commands
- `helm-upgrade`: Deploy Helm charts
- `trivy-scanner`: Security scanning

**Browse tasks:** https://hub.tekton.dev

## Integration with Kubernetes Skill

This Tekton skill builds on the Kubernetes skill:

- **Kubernetes/Debug**: Debug pods created by Tekton TaskRuns
- **Kubernetes/Deploy**: Understanding where Tekton deploys workloads
- **Kubernetes/Resources**: Tekton creates Kubernetes CRDs (Tasks, Pipelines)
- **Kubernetes/Security**: RBAC for Tekton ServiceAccounts
- **Kubernetes/Context**: Managing Tekton across multiple clusters

**Before using Tekton, ensure you're familiar with:**
- Kubernetes pods and containers
- PersistentVolumeClaims (PVCs)
- ServiceAccounts and RBAC
- Secrets and ConfigMaps
- kubectl basics

## Key Best Practices

### Security
- Use workspace-based authentication (not built-in credential init)
- Create dedicated ServiceAccounts per pipeline
- Follow least privilege principle for RBAC
- Use personal access tokens, not passwords
- Never commit secrets to Git

### Performance
- Always set resource requests/limits
- Configure pipeline pruner for automatic cleanup
- Use volumeClaimTemplate for isolation
- Leverage caching (Kaniko layers, Maven deps)
- Be aware of PVC access mode limitations

### Reusability
- Parameterize everything (no hardcoded values)
- Use Tekton Hub tasks when available
- Emit Results for small data (<4KB)
- Use Workspaces for larger data
- Keep tasks focused (single responsibility)

### Anti-Patterns to Avoid
1. **Don't use ClusterTasks** - Deprecated, use resolvers instead
2. **Don't use PipelineResources** - Deprecated, use Tasks with Results
3. **Don't skip resource limits** - Causes scheduling issues
4. **Don't share ReadWriteOnce PVCs in parallel** - Will fail
5. **Don't use built-in credential init only** - Moving to workspace-based auth
6. **Don't create monolithic tasks** - Break into focused tasks
7. **Don't ignore pipeline pruner** - Old resources fill etcd

## Troubleshooting Quick Reference

```bash
# View pipeline run status
tkn pipelinerun describe <name>

# Stream logs
tkn pipelinerun logs <name> -f

# Check why task failed
kubectl describe taskrun <taskrun-name>

# View events
kubectl get events --sort-by=.metadata.creationTimestamp

# Check pod logs directly
kubectl logs <pod-name> -c step-<step-name>

# Debug container
kubectl debug -it <pod-name> --image=alpine --target=<container>
```

## Examples

**Example 1: Create CI pipeline**
```
User: "Create a Tekton pipeline that clones a repo, runs tests, and builds a container image"
→ Invokes Pipelines workflow
→ Creates pipeline with git-clone, test, and kaniko tasks
→ Configures workspaces for source sharing
→ Sets up proper task dependencies
```

**Example 2: Set up GitHub webhook**
```
User: "Set up GitHub webhook to trigger my pipeline on push"
→ Invokes Triggers workflow
→ Creates EventListener with GitHub interceptor
→ Configures TriggerBinding to extract commit info
→ Sets up TriggerTemplate to start PipelineRun
```

**Example 3: Integrate with ArgoCD**
```
User: "How do I integrate Tekton with ArgoCD for GitOps?"
→ Invokes GitOps workflow
→ Explains CI (Tekton) vs CD (ArgoCD) separation
→ Shows how Tekton updates GitOps repo
→ ArgoCD syncs changes to cluster
```

## Installation

**Install Tekton Pipelines:**
```bash
kubectl apply --filename https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml
```

**Install Tekton Triggers:**
```bash
kubectl apply --filename https://storage.googleapis.com/tekton-releases/triggers/latest/release.yaml
```

**Install tkn CLI:**
```bash
# macOS
brew install tektoncd-cli

# Linux
curl -LO https://github.com/tektoncd/cli/releases/latest/download/tkn_<version>_Linux_x86_64.tar.gz
sudo tar xvzf tkn_<version>_Linux_x86_64.tar.gz -C /usr/local/bin/ tkn
```

**Verify installation:**
```bash
kubectl get pods -n tekton-pipelines
tkn version
```

## Related Skills

- **Kubernetes**: Foundation for Tekton (pods, PVCs, RBAC)
- **Git**: Source control integration and GitOps workflows
- **Golang**: Writing custom Tekton tasks and controllers
- **Nix/Homelab**: Managing Tekton in NixOS/K3s environments
