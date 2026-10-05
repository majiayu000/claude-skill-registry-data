---




name: tekton
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '"Provides Tekton in Cloud-Native Engineering - A cloud-native Pipeline
  resource"'
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  role: reference
  scope: infrastructure
  triggers: cloud-native, engineering, pipeline, tekton
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




  related-skills: cncf-argo, cncf-aws-dynamodb, cncf-aws-ec2, cncf-aws-eks


# Tekton in Cloud-Native Engineering

**Category:** cdf  
**Status:** Active  
**Stars:** 8,941  
**Last Updated:** 2026-04-21  
**Primary Language:** Go  
**Documentation:** [https://tekton.dev/docs/](https://tekton.dev/docs/)  

---

## Purpose and Use Cases

Tekton is a core component of the cloud-native ecosystem, serving as a Kubernetes-native CI/CD pipeline framework that enables declarative, container-based pipeline definitions.

### What Problem Does It Solve?

The need for a Kubernetes-native CI/CD solution that leverages containers for pipeline execution, integrates naturally with Kubernetes tooling, and provides declarative pipeline definitions.

### When to Use This Project

Use Tekton when you need a Kubernetes-native CI/CD pipeline framework, want to run pipelines in Kubernetes pods, or need declarative pipeline definitions that integrate with Kubernetes RBAC and security.

### Key Use Cases


- Kubernetes-native CI/CD pipelines
- Declarative pipeline definitions
- Container-based pipeline execution
- Integration with Git and artifact repositories
- Parallel and sequential task execution


---

## Architecture Design Patterns

### Core Components


- **Pipeline**: Sequence of tasks to execute
- **Task**: Reusable sequence of steps
- **Step**: Container that runs a command
- **PipelineRun**: Instance of a pipeline execution
- **TaskRun**: Instance of a task execution
- **PipelineResource**: Input/output resources for pipelines
- **ClusterTask**: Cluster-scoped task definition


### Component Interactions


1. **User → API Server**: Creates PipelineRun
2. **Pipeline Controller → TaskRun**: Creates task instances
3. **TaskRun → Kubernetes**: Creates pod for each step
4. **Step Pod → Container Runtime**: Runs container commands
5. **Result → Artifact Storage**: Saves outputs
6. **Status → API Server**: Updates PipelineRun status


### Data Flow Patterns


1. **Pipeline Execution**: PipelineRun created → TaskRuns created → Pods created → Steps run → Results stored
2. **Resource Processing**: Input resource → Task → Output resource → Pipeline → Next task
3. **Status Updates**: Pod status → TaskRun → PipelineRun → API Server


### Design Principles


- **Kubernetes-Native**: Uses Kubernetes API patterns
- **Container-Based**: Each step in its own container
- **Declarative**: YAML-based definitions
- **Composable**: Tasks and pipelines can be composed
- **Flexible**: Supports any container workload


---

## Integration Approaches

### Integration with Other CNCF Projects


- **Kubernetes**: Native Kubernetes CRDs
- **Git Providers**: GitHub, GitLab, Bitbucket integration
- **Container Runtime**: Runs pipelines in pods
- **Kubernetes API**: Resource management
- **Helm**: Chart deployment in pipelines


### API Patterns


- **Kubernetes API**: Custom resource definitions
- **Status Subresource**: Pipeline run status
- **Finalizers**: Cleanup operations
- **Owner References**: Resource relationships


### Configuration Patterns


- **Pipeline YAML**: Pipeline definitions
- **PipelineRun YAML**: Pipeline instances
- **Task YAML**: Task definitions
- **TaskRun YAML**: Task instances
- **ConfigMap**: Cluster-wide config


### Extension Mechanisms


- **Tasks**: Reusable workflow steps
- **PipelineResources**: Input/output types
- **Conditions**: Conditional execution
- **ClusterTask**: Cluster-wide tasks


---

## Common Pitfalls and How to Avoid Them

### Misconfigurations


- **Task Parameters**: Incorrect parameter types
- **PipelineResources**: Missing or incorrect resources
- **Step Images**: Non-existent container images
- **Service Accounts**: Incorrect permissions
- **Timeouts**: Missing or insufficient timeouts


### Performance Issues


- **Pipeline Run Time**: Slow task execution
- **Pod Startup**: Slow container image pulls
- **Resource Usage**: High resource consumption
- **API Server Load**: Many TaskRuns/PipelineRuns


### Operational Challenges


- **Pipeline Maintenance**: Complex pipeline graphs
- **Resource Cleanup**: Cleaning up old runs
- **Secret Management**: Sensitive data handling
- **Scaling**: Pipeline controller scaling
- **Testing**: Pipeline testing strategies


### Security Pitfalls


- **Service Accounts**: Overly permissive service accounts
- **Pipeline Resources**: Secrets in resources
- **Task Execution**: Privileged task containers
- **Network Exposure**: Access to internal services


---

## Coding Practices

### Idiomatic Configuration


- **YAML Definitions**: Clear structure
- **Task Parameters**: Typed parameters
- **Pipeline Resources**: Explicit inputs/outputs
- **ServiceAccount References**: Explicit auth


### API Usage Patterns


- **kubectl**: Pipeline operations
- **Tekton CLI**: Extended functionality
- **Kubernetes API**: Direct API access
- **Webhooks**: Event triggers


### Observability Best Practices


- **PipelineRun Logs**: Task execution logs
- **Status Metrics**: Run duration and status
- **Resource Usage**: Task resource consumption
- **Event Logging**: Trigger events


### Testing Strategies


- **Unit Tests**: Task and pipeline tests
- **Integration Tests**: Controller tests
- **E2E Tests**: Full pipeline runs
- **Compatibility Tests**: Kubernetes versions


### Development Workflow


- **Development**: Tekton development cluster
- **Testing**: Go tests, E2E tests
- **Debugging**: kubectl, pipeline logs
- **Deployment**: YAML manifests, operator
- **CI/CD**: tektoncd pipelines
- **Tools**: tkn, kubectl


---

## Fundamentals

### Essential Concepts


- **Pipeline**: Sequence of tasks
- **Task**: Reusable workflow step
- **Step**: Container running a command
- **PipelineRun**: Instance of pipeline execution
- **TaskRun**: Instance of task execution
- **Workspace**: Shared storage between steps
- **Param**: Task parameter
- **Result**: Task output
- **Resource**: Input/output resource
- **Condition**: Conditional execution


### Terminology Glossary


- **Pipeline**: Task sequence
- **Task**: Reusable step
- **Step**: Container command
- **PipelineRun**: Pipeline instance
- **TaskRun**: Task instance
- **Workspace**: Shared storage
- **Param**: Task parameter
- **Result**: Task output
- **Resource**: Input/output
- **Condition**: Conditional exec


### Data Models and Types


- **Pipeline**: Pipeline definition
- **Task**: Task definition
- **Step**: Step definition
- **PipelineResource**: Resource definition
- **Param**: Parameter definition
- **Result**: Result definition
- **Workspace**: Workspace definition
- **TaskRun**: TaskRun specification
- **PipelineRun**: PipelineRun specification


### Lifecycle Management


- **PipelineRun Lifecycle**: Created → Running → Succeeded/Failed
- **TaskRun Lifecycle**: Created → Running → Complete
- **Step Lifecycle**: Pull → Start → Run → Complete
- **Resource Lifecycle**: Bind → Process → Release


### State Management


- **TaskRun State**: Task execution state
- **PipelineRun State**: Pipeline execution state
- **Step State**: Step execution state
- **Resource State**: Bound resources
- **Result State**: Task outputs


---

## Scaling and Deployment Patterns

### Horizontal Scaling


- **Pipeline Controller Scaling**: Controller replicas
- **TaskRun Scaling**: Parallel task execution
- **Worker Pool Scaling**: Pipeline runner pool


### High Availability


- **Controller HA**: Multiple controller replicas
- **PipelineRun Resilience**: Automatic retry
- **TaskRun Resilience**: Automatic restart


### Production Deployments


- **Controller Deployment**: Production controller setup
- **Resource Limits**: Appropriate pod resource limits
- **Security**: RBAC, service account configuration
- **Monitoring**: Pipeline metrics
- **Cleanup Strategy**: Old run cleanup


### Upgrade Strategies


- **Controller Upgrade**: Pipeline controller upgrade
- **CRD Migration**: Custom resource definition migration
- **PipelineRun Migration**: Running pipeline migration
- **TaskVersion**: Task version management


### Resource Management


- **Task Resources**: Step resource limits
- **Pipeline Resources**: Pipeline memory limits
- **Workspace Storage**: Workspace storage management
- **Pod Resource Limits**: Per-pod resource limits


---

## Additional Resources

- **Official Documentation:** [https://tekton.dev/docs/](https://tekton.dev/docs/)
- **GitHub Repository:** [github.com/tektoncd/pipeline](https://github.com/tektoncd/pipeline)
- **CNCF Project Page:** [cncf.io/projects/tekton/](https://www.cncf.io/projects/tekton/)
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

### Tekton Pipeline with Multiple Tasks


```yaml
# Tekton Pipeline for CI/CD workflow
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: build-deploy-pipeline
spec:
  workspaces:
  - name: source
  - name: registry-auth
  params:
  - name: image-url
    type: string
  - name: path-context
    type: string
    default: .
  tasks:
  - name: fetch-repository
    taskRef:
      name: git-clone
    workspaces:
    - name: output
      workspace: source
    params:
    - name: url
      value: $(params.git-url)
    - name: revision
      value: $(params.git-revision)

  - name: build
    taskRef:
      name: kaniko
    workspaces:
    - name: source
      workspace: source
    params:
    - name: IMAGE
      value: $(params.image-url)
    - name: CONTEXT
      value: $(params.path-context)
    runAfter:
    - fetch-repository

  - name: deploy
    taskRef:
      name: kubectl-apply
    params:
    - name: IMAGE
      value: $(tasks.build.results.image-url)
    - name: MANIFESTS
      value: $(params.manifests)
    runAfter:
    - build
---
  related-skills: cncf-argo, cncf-aws-dynamodb, cncf-aws-ec2, cncf-aws-eks
# PipelineRun to execute the pipeline
apiVersion: tekton.dev/v1beta1
kind: PipelineRun
metadata:
  name: build-deploy-pipelinerun
spec:
  pipelineRef:
    name: build-deploy-pipeline
  workspaces:
  - name: source
    persistentVolumeClaim:
      claimName: source-pvc
  - name: registry-auth
    secret:
      secretName: registry-credentials
  params:
  - name: image-url
    value: gcr.io/myproject/myapp:latest
  - name: path-context
    value: src
  - name: git-url
    value: https://github.com/myorg/myapp.git
  - name: git-revision
    value: main
```

### Tekton Task with Input/Output Resources


```yaml
# Tekton Task for testing with artifacts
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: test-task
spec:
  workspaces:
  - name: source
  - name: test-results
  steps:
  - name: install-dependencies
    image: node:16
    workingDir: $(workspaces.source.path)
    script: |
      npm ci
  - name: run-tests
    image: node:16
    workingDir: $(workspaces.source.path)
    script: |
      npm test
    volumeMounts:
    - name: test-results
      mountPath: /results
  - name: upload-results
    image: ubuntu
    workingDir: $(workspaces.source.path)
    script: |
      if [ -f /results/junit.xml ]; then
        echo "Test results uploaded"
      else
        echo "No test results to upload"
      fi
---
  related-skills: cncf-argo, cncf-aws-dynamodb, cncf-aws-ec2, cncf-aws-eks
# TaskRun to execute the task
apiVersion: tekton.dev/v1beta1
kind: TaskRun
metadata:
  name: test-task-run
spec:
  taskRef:
    name: test-task
  workspaces:
  - name: source
    persistentVolumeClaim:
      claimName: source-pvc
  - name: test-results
    emptyDir: {}
```

### Tekton PipelineResource for Git and Image


```yaml
# Tekton PipelineResources for external resources
apiVersion: tekton.dev/v1beta1
kind: PipelineResource
metadata:
  name: myapp-git
spec:
  type: git
  params:
  - name: url
    value: https://github.com/myorg/myapp.git
  - name: revision
    value: main

---
  related-skills: cncf-argo, cncf-aws-dynamodb, cncf-aws-ec2, cncf-aws-eks
apiVersion: tekton.dev/v1beta1
kind: PipelineResource
metadata:
  name: myapp-image
spec:
  type: image
  params:
  - name: url
    value: gcr.io/myproject/myapp:latest

---
  related-skills: cncf-argo, cncf-aws-dynamodb, cncf-aws-ec2, cncf-aws-eks
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: build-with-resources
spec:
  resources:
  - name: git-source
    type: git
  - name: app-image
    type: image
  tasks:
  - name: build
    taskRef:
      name: kaniko
    resources:
      inputs:
      - name: git-source
        resources:
        - git-source
      outputs:
      - name: image
        resources:
        - app-image
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
