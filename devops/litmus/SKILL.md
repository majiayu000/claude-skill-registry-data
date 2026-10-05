---




name: litmus
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '"Litmus in Chaos Engineering - cloud native architecture, patterns,
  pits" and best practices'
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  related-skills: null
  role: reference
  scope: infrastructure
  triggers: cdn, chaos, engineering, infrastructure as code, litmus, monitoring, cloudformation,
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




# Litmus in Cloud-Native Engineering

## Purpose and Use Cases

### What Problem Does It Solve?
- **Chaos engineering at scale**: Enables systematic testing of distributed systems resilience through automated chaos experiments
- **Proactive failure detection**: Identify system weaknesses before they cause production incidents
- **Self-healing verification**: Test and validate automated recovery mechanisms
- **Resilience culturing**: Build engineering teams' confidence in system reliability
- **Compliance and audit**: Document system behavior under failure conditions for regulatory compliance

### When to Use
- **Critical production systems**: Financial, healthcare, or infrastructure systems where failures are costly
- **Complex distributed architectures**: Microservices, multi-cloud, or hybrid deployments
- **After major deployments**: Validate new deployments don't introduce resilience gaps
- **Regular resilience testing**: Scheduled chaos experiments as part of SRE practices
- **Pre-production validation**: Test staging environments before production releases

### Key Use Cases
- **Pod failure testing**: Simulate pod crashes, node failures, or network partitions
- **Resource exhaustion**: Test system behavior under CPU, memory, or disk pressure
- **Network latency and loss**: Simulate network partitions, high latency, or packet loss
- **Dependency failures**: Test failure modes when dependent services fail
- **Self-healing verification**: Confirm Kubernetes self-healing mechanisms work correctly

## Architecture Design Patterns

### Core Components

#### Litmus Chaos Operator
```
litmus
├── chaos-operator (main orchestrator)
├── chaos-exporter (metrics collection)
├── chaos-dashboard (UI and API)
├── experiment-images (chaos experiments)
└── workflow-images (chaos workflows)
```
- **Chaos Operator**: Manages chaos experiments and resources
- **Chaos Exporter**: Exposes experiment metrics to Prometheus
- **Chaos Dashboard**: Web UI for experiment management
- **Experiment Images**: Docker containers running chaos scenarios
- **Workflow Images**: Custom chaos experiment definitions

#### Chaos Experiment Structure
```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosExperiment
metadata:
  name: pod-delete
spec:
  definition:
    execution:
      - name: chaos
        image: litmuschaos/go-runner:latest
        command:
          - /bin/bash
          - -c
          - |
            # Chaos experiment logic
            kubectl delete pod ${CHAOSENGINE} -n ${TARGET_NAMESPACE}
        env:
          - name: TARGET_NAMESPACE
            valueFrom:
              fieldRef:
                fieldPath: metadata.namespace
          - name: CHAOSENGINE
            value: ${CHAOSENGINE}
```
- **Experiment definitions**: YAML configurations for chaos scenarios
- **Execution containers**: Docker images running chaos logic
- **Environment variables**: Configuration passed to experiment
- **RBAC permissions**: Required Kubernetes permissions

#### Chaos Engine
```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: nginx-chaos
  namespace: default
spec:
  appinfo:
    appns: default
    applabel: "app=nginx"
    appkind: deployment
  jobCleanUpPolicy: delete
  engineState: active
  chaosServiceAccount: litmus
  experiments:
    - name: pod-delete
      spec:
        components:
          env:
            - name: TOTAL_CHAOS_DURATION
              value: "30"
            - name: CHAOS_INTERVAL
              value: "10"
            - name: Pod_Delete
              value: "true"
```
- **Engine configuration**: Main orchestration object
- **Target application**: What to test and how
- **Experiment definitions**: List of chaos experiments to run
- **Service account**: RBAC permissions for experiments
- **Job cleanup**: Cleanup behavior after experiments

### Component Interactions
```
Chaos Engine
    ↓ (creates job)
Kubernetes Job
    ↓ (runs experiment)
Chaos Experiment Container
    ↓ (executes chaos)
Target Application
    ↓ (monitors results)
Chaos Exporter
    ↓ (collects metrics)
Prometheus
```

### Data Flow Patterns

#### Experiment Execution Flow
```
1. ChaosEngine resource created
2. Chaos operator detects new engine
3. Creates Kubernetes Job for experiment
4. Job runs chaos experiment container
5. Experiment applies chaos to target
6. Results collected and reported
7. Job completed, results exported
```

#### Self-Healing Test Flow
```
1. Chaos experiment triggers failure
2. Kubernetes self-healing detects failure
3. Kubernetes recreates failed resources
4. Chaos experiment monitors recovery
5. Success/failure reported
6. Results stored for analysis
```

### Design Principles

#### Idempotency
- Experiments can be run multiple times safely
- No state dependencies between runs
- Clean rollback after each experiment

#### Declarative Configuration
- All chaos defined as Kubernetes resources
- Version control friendly YAML configurations
- GitOps compatible chaos workflows

#### Minimal Instrumentation
- No application code changes required
- Works with any Kubernetes application
- Label-based target selection

## Integration Approaches

### Integration with Other CNCF Projects

#### Prometheus Integration
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: litmus-exporter
  namespace: litmus
spec:
  selector:
    matchLabels:
      name: litmus-exporter
  namespaceSelector:
    matchNames:
      - litmus
  endpoints:
    - port: metrics
      path: /metrics
      interval: 30s
```
- **Metrics collection**: Prometheus scrapes chaos exporter
- **Alerting**: Prometheus alerts on chaos failure rates
- **Dashboard integration**: Grafana dashboards for chaos metrics

#### Grafana Integration
```json
{
  "annotations": {
    "list": [{
      "name": "Chaos Experiments",
      "datasource": "Prometheus",
      "enable": true,
      "expr": "chaos_experiment_total"
    }]
  },
  "panels": [
    {
      "title": "Experiment Success Rate",
      "targets": [{
        "expr": "chaos_experiment_success_ratio"
      }]
    }
  ]
}
```
- **Pre-built dashboards**: Chaos experiment visualization
- **Real-time monitoring**: Live experiment status
- **Historical analysis**: Experiment trends over time

#### ArgoCD Integration
```yaml
apiVersion: apps/v1
kind: ConfigMap
metadata:
  name: litmus-gitops
data:
  chaos-engine.yaml: |
    apiVersion: litmuschaos.io/v1alpha1
    kind: ChaosEngine
    metadata:
      name: gitops-chaos
    spec:
      appinfo: ...
      experiments: []
```
- **GitOps chaos**: Chaos experiments version controlled
- **Automated execution**: ArgoCD triggers chaos tests
- **Sync verification**: GitOps sync status validated

#### Tekton Integration
```yaml
apiVersion: tekton.dev/v1beta1
kind: PipelineRun
metadata:
  name: chaos-test-pipeline
spec:
  pipelineRef:
    name: chaos-test-pipeline
  tasks:
    - name: chaos-test
      taskRef:
        name: litmus-chaos-test
      params:
        - name: engine
          value: "my-chaos-engine"
```
- **CI/CD integration**: Chaos tests in CI/CD pipelines
- **Automated chaos**: Trigger chaos on code changes
- **Test results**: Pipeline results include chaos outcomes

#### Kyverno Integration
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-chaos-tests
spec:
  validationFailureAction: Enforce
  rules:
    - name: chaos-tested
      match:
        any:
          - resources:
              kinds:
                - Pod
      validate:
        message: "Production deployments must have chaos test coverage"
        deny: {}
```
- **Policy enforcement**: Ensure chaos testing in CI/CD
- **Compliance checking**: Verify chaos coverage
- **Automated gates**: Block deployments without chaos tests

### API Patterns

#### Experiment API
- **ChaosExperiment**: Defines chaos scenario
- **ChaosEngine**: Orchestrates chaos execution
- **ChaosResult**: Stores experiment results
- **ChaosScheduler**: Schedule recurring experiments

#### Result API
```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosResult
metadata:
  name: nginx-chaos-pod-delete
  namespace: default
spec:
  engine: nginx-chaos
  experiment: pod-delete
  scenario: Chaos
  status:
    verdict: Pass
    failStep: ""
    probeSuccessPercentage: "100"
    lastUpdateTime: "2023-01-01T00:00:00Z"
```

### Configuration Patterns

#### Chaos Engine Configuration
```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: web-app-chaos
spec:
  appinfo:
    appns: default
    applabel: "app=web-app"
    appkind: deployment
  engineState: active
  jobCleanUpPolicy: delete
  chaosServiceAccount: litmus-admin
  experiments:
    - name: pod-delete
      spec:
        components:
          env:
            - name: TARGET_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: TOTAL_CHAOS_DURATION
              value: "60"
            - name: CHAOS_INTERVAL
              value: "15"
            - name: FORCE
              value: "true"
```

#### RBAC Configuration
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: litmus-role
rules:
  - apiGroups: [""]
    resources: ["pods", "services", "configmaps", "events", "pods/log"]
    verbs: ["get", "list", "delete"]
  - apiGroups: ["apps"]
    resources: ["deployments", "replicasets"]
    verbs: ["get", "list", "delete"]
  - apiGroups: ["batch"]
    resources: ["jobs"]
    verbs: ["get", "list", "create", "delete"]
  related-skills: null
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: litmus-binding
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: litmus-role
subjects:
  - kind: ServiceAccount
    name: litmus
    namespace: litmus
```

### Extension Mechanisms

#### Custom Experiment Templates
```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosExperiment
metadata:
  name: custom-experiment
spec:
  definition:
    execution:
      - name: chaos
        image: my-registry/custom-chaos:latest
        command:
          - /bin/bash
          - -c
          - ./run-custom-chaos.sh
        env:
          - name: CUSTOM_PARAM
            value: "value"
```

#### Workflow Templates
```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: WorkflowTemplate
metadata:
  name: resilience-test
spec:
  sequence:
    - experiment: pod-delete
    - experiment: pod-cpu-hog
    - experiment: pod-memory-hog
  parallel:
    - experiment: pod-network-latency
    - experiment: pod-disk-fill
```

## Common Pitfalls and How to Avoid Them

### Configuration Issues

#### Insufficient RBAC
**Problem**: Chaos experiments fail due to missing permissions.

**Solution**:
```yaml
# Ensure proper RBAC
kubectl create clusterrolebinding litmus-binding \
  --clusterrole=litmus-role \
  --serviceaccount=litmus:default
```

#### Target Application Misconfiguration
**Problem**: Experiments don't target correct resources.

**Solutions**:
```yaml
# Verify app labels
kubectl get pods --show-labels

# Correct ChaosEngine configuration
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
spec:
  appinfo:
    appns: default
    applabel: "app=nginx"  # Must match actual labels
    appkind: deployment
```

#### Resource Limits Not Set
**Problem**: Chaos experiments consume too many resources.

**Solution**:
```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: chaos-runner
      resources:
        requests:
          memory: "256Mi"
          cpu: "100m"
        limits:
          memory: "512Mi"
          cpu: "500m"
```

### Performance Issues

#### Experiment Overhead
**Problem**: Chaos experiments impact production performance.

**Solutions**:
- Run experiments in staging first
- Use non-production namespaces for initial testing
- Schedule experiments during low-traffic periods
- Limit experiment duration and frequency

#### Metrics Collection Impact
**Problem**: Chaos exporter affects application performance.

**Solutions**:
- Deploy exporter in separate namespace
- Configure appropriate scrape intervals
- Limit metrics collection scope
- Use remote storage for large-scale deployments

### Operational Challenges

#### Experiment Failures
**Problem**: Experiments fail with unclear error messages.

**Solutions**:
```bash
# Check experiment logs
kubectl logs -f pod/litmus-chaos-runner-xxxxx -n litmus

# Check chaos result
kubectl get chaosresult nginx-chaos-pod-delete -o yaml

# Verify chaos operator logs
kubectl logs -n litmus deploy/chaos-operator
```

#### Cleanup Issues
**Problem**: Experiments leave resources behind.

**Solutions**:
- Use `jobCleanUpPolicy: delete`
- Implement proper cleanup in experiment scripts
- Monitor for orphaned resources
- Regular cleanup audits

#### Version Compatibility
**Problem**: Litmus versions incompatible with Kubernetes.

**Solutions**:
- Check Litmus compatibility matrix
- Test in staging before production
- Use specific Litmus versions
- Follow upgrade guides carefully

### Security Pitfalls

#### Privilege Escalation
**Problem**: Chaos experiments gain excessive permissions.

**Solutions**:
- Use least-privilege RBAC
- Avoid cluster-admin service accounts
- Audit experiment permissions regularly
- Use dedicated chaos service accounts

#### Secret Exposure
**Problem**: Chaos configurations expose sensitive data.

**Solutions**:
- Use Kubernetes secrets for sensitive data
- Avoid secrets in experiment YAMLs
- Encrypt secrets at rest
- Audit secret access

#### Network Policies
**Problem**: Chaos experiments blocked by network policies.

**Solutions**:
- Exclude chaos components from network policies
- Create dedicated network policy exceptions
- Test network chaos separately
- Document network requirements

## Coding Practices

### Idiomatic Configuration

#### Standard Experiment YAML
```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosExperiment
metadata:
  name: pod-delete
  labels:
    name: pod-delete
    app.kubernetes.io/component: chaos-experiment
spec:
  definition:
    execution:
      - name: chaos
        image: litmuschaos/go-runner:latest
        command:
          - /bin/bash
          - -c
          - |
            # chaos logic here
            echo "Starting pod deletion chaos"
        env:
          - name: TARGET_NAMESPACE
            valueFrom:
              fieldRef:
                fieldPath: metadata.namespace
        resources:
          requests:
            memory: 128Mi
            cpu: 100m
          limits:
            memory: 256Mi
            cpu: 200m
```

### API Usage Patterns

#### Running Experiments
```bash
# Create chaos engine
kubectl apply -f chaos-engine.yaml

# Monitor experiment
kubectl get chaosresult -w

# Check experiment status
kubectl get chaosengine nginx-chaos

# View experiment logs
kubectl logs -f deploy/chaos-operator -n litmus
```

#### Updating Experiments
```bash
# Update chaos engine
kubectl patch chaosengine nginx-chaos \
  --type='json' \
  -p='[{"op": "replace", "path": "/spec/experiments/0/spec/components/env/0/value", "value": "90"}]'

# Delete chaos engine
kubectl delete chaosengine nginx-chaos
```

### Observability Best Practices

#### Metrics Collection
- **Experiment duration**: Track experiment execution time
- **Success/failure rates**: Monitor experiment outcomes
- **Resource usage**: Track chaos component resource consumption
- **Failure trends**: Identify recurring failure patterns

#### Logging Strategy
- **Experiment logs**: Detailed chaos execution logs
- **Application logs**: Monitor application response to chaos
- **Audit logs**: Track who ran what experiment and when
- **Error logs**: Capture and alert on failures

### Development Workflow

#### Experiment Development
1. Create experiment YAML definition
2. Build chaos image with experiment logic
3. Test in isolated namespace
4. Verify cleanup behavior
5. Document experiment parameters
6. Version control configuration

#### CI/CD Integration
```yaml
# Example GitLab CI
chaos-test:
  stage: test
  script:
    - kubectl apply -f chaos-engine.yaml
    - kubectl wait --for=condition=Complete job/litmus-chaos-runner --timeout=5m
    - kubectl get chaosresult -o yaml
  rules:
    - if: $CI_COMMIT_BRANCH == 'main'
```

## Fundamentals

### Essential Concepts

#### Chaos Experiment Lifecycle
- **Definition**: YAML file defining chaos scenario
- **Execution**: Kubernetes Job running chaos container
- **Monitoring**: Real-time experiment status
- **Result**: ChaosResult storing experiment outcome
- **Cleanup**: Resource cleanup after completion

#### Litmus Architecture
- **Chaos Operator**: Main orchestrator
- **Chaos Exporter**: Metrics collection
- **Chaos Dashboard**: Web UI
- **Experiment Images**: Docker containers for chaos
- **Workflow Images**: Custom chaos definitions

### Terminology Glossary

| Term | Definition |
|  related-skills: null
| **ChaosExperiment** | Kubernetes resource defining a chaos scenario |
| **ChaosEngine** | Main orchestration resource for chaos execution |
| **ChaosResult** | Result of chaos experiment execution |
| **ChaosOperator** | Controller managing chaos resources |
| **ChaosExporter** | Prometheus metrics exporter for chaos |
| **ChaosRunner** | Container executing chaos experiment |
| **EngineState** | Active or stop state of chaos engine |
| **JobCleanupPolicy** | Policy for cleaning up experiment jobs |
| **Application Info** | Target application configuration |
| **Experiment Spec** | Individual experiment configuration |

### Data Models and Types

#### ChaosExperiment Schema
```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosExperiment
metadata:
  name: string
spec:
  definition:
    execution:
      - name: string
        image: string
        command: []
        env: []
        resources: {}
```

#### ChaosEngine Schema
```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: string
spec:
  appinfo: {}
  engineState: active|stop
  jobCleanUpPolicy: delete|keep
  chaosServiceAccount: string
  experiments: []
```

### Lifecycle Management

#### Installation Lifecycle
1. **Prerequisites**: Kubernetes cluster, kubectl
2. **Install Litmus**: `kubectl apply -f litmus-operator.yaml`
3. **Create Service Account**: RBAC configuration
4. **Deploy Experiments**: Apply experiment YAMLs
5. **Verify Installation**: Run litmus check
6. **Configure Experiments**: Create ChaosEngine resources

#### Experiment Lifecycle
1. **Definition**: Create ChaosExperiment YAML
2. **Execution**: Create ChaosEngine referencing experiment
3. **Monitoring**: Watch experiment progress
4. **Result**: Collect ChaosResult
5. **Cleanup**: Remove ChaosEngine

### State Management

#### Experiment State
- **Pending**: Waiting to start
- **Running**: Currently executing
- **Completed**: Finished execution
- **Failed**: Failed to complete
- **Stopped**: Manually stopped

#### Application State During Chaos
- **Normal**: No chaos active
- **Degraded**: Chaos causing issues
- **Recovered**: Self-healing occurred
- **Failed**: Recovery failed

## Scaling and Deployment Patterns

### Horizontal Scaling

#### Multiple Chaos Engines
```yaml
# Run chaos in multiple namespaces
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: chaos-web-namespace-1
  namespace: namespace-1
spec: ...
  related-skills: null
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: chaos-web-namespace-2
  namespace: namespace-2
spec: ...
```

#### Parallel Experiments
```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
spec:
  experiments:
    - name: pod-delete
    - name: pod-cpu-hog
    - name: pod-network-latency
```

### High Availability

#### Chaos Operator HA
```yaml
# Deploy multiple operator replicas
kubectl scale -n litmus deploy/chaos-operator --replicas=3
```

#### Dashboard HA
```yaml
# Deploy dashboard with replicas
kubectl scale -n litmus deploy/litmus-dashboard --replicas=3
```

### Production Deployments

#### Multi-Cluster Chaos
```bash
# Export chaos results from all clusters
kubectl get chaosresult --all-namespaces -o json > results.json
```

#### Scheduled Experiments
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: weekly-chaos
spec:
  schedule: "0 0 * * 0"  # Sunday at midnight
  jobTemplate:
    spec:
      template:
        spec:
          # Create chaos engine
          restartPolicy: Never
```

### Upgrade Strategies

#### Rolling Updates
1. Test new version in staging
2. Update chaos operator
3. Update experiment images
4. Update chaos engines
5. Verify functionality

#### Blue-Green Updates
1. Deploy new version alongside old
2. Run parallel experiments
3. Compare results
4. Switch traffic to new version
5. Decommission old version

### Resource Management

#### Resource Sizing
```yaml
resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "256Mi"
    cpu: "500m"
```

#### Storage Management
- **Result storage**: ChaosResult storage requirements
- **Log rotation**: Exponential backoff for retries
- **Cleanup**: Automatic resource cleanup
- **Export**: Export results for analysis

## Additional Resources

### Official Documentation
- **Litmus Documentation**: https://litmuschaos.io/
- **Litmus GitHub**: https://github.com/litmuschaos/litmus
- **Chaos Hub**: https://hub.litmuschaos.io/
- **Getting Started**: https://docs.litmuschaos.io/docs/getstarted

### CNCF References
- **Litmus in CNCF Landscape**: https://landscape.cncf.io/?group=projects&filter=chaos-engineering
- **CNCF Chaos Engineering**: https://github.com/cncf/sig-chaos-engineering

### Tools and Libraries
- **litmusctl**: CLI tool for Litmus
- **pylitmus**: Python client library
- **litmus-go**: Go SDK for chaos experiments
- **chaos-mesh**: Alternative chaos platform

### Tutorials and Guides
- **Basic Chaos Experiment**: https://docs.litmuschaos.io/docs/basic-chaos-experiment
- **Custom Experiment**: https://docs.litmuschaos.io/docs/create-custom-experiment
- **Self-Healing**: https://docs.litmuschaos.io/docs/self-healing
- **Multicluster**: https://docs.litmuschaos.io/docs/multicluster-chaos

### Community Resources
- **Litmus Slack**: https://kubernetes.slack.com/archives/CMR557BAG
- **Litmus Twitter**: https://twitter.com/litmus_chaos
- **Blog**: https://litmuschaos.io/blog/
- **Community Calls**: Weekly community meetings

### Related Standards
- **SRE Book**: Google SRE practices
- **Chaos Engineering**: Principles and practices
- **Resilience Patterns**: System resilience patterns

### OpenTelemetry Integration
- **Tracing**: Chaos experiment tracing
- **Metrics**: Prometheus metrics collection
- **Logs**: Chaos-related logging
- **Events**: Kubernetes event integration

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

## Constraints

### MUST DO
- Cite authoritative primary sources (official documentation, RFCs, standards bodies) — avoid secondary or blog references
- Include version-specific guidance when the reference topic has significant version-dependent behavior
- Structure reference content with clear navigation: overview first, then detailed subsections organized by use case
- Keep examples minimal and self-contained so readers can copy-paste without needing external context

### MUST NOT DO
- Do not present opinionated practices as facts — distinguish between standards, recommendations, and personal preferences
- Avoid outdated API references or deprecated patterns; explicitly note version requirements for each code example
- Never include incomplete or pseudocode examples in reference materials — all examples should be runnable
- Do not conflate different product versions when documenting features that vary across releases
