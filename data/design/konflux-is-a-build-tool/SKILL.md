---
name: Konflux is a build tool
description: Use this skill to query Konflux objects from the Kubernetes cluster. Konflux objects are application, component, pipelinerun, taskrun, snapshot and release. The skill can be used to query logs from failed or removed pipelines and pods.
---

# Konflux skill

This skill helps debug OpenShift bare metal installation failures in CI jobs by analyzing dev-scripts logs, libvirt console logs, sosreports, and other metal-specific artifacts.

This still helps to interact and debug Konflux objects in a Kubernetes cluster.

## When to Use This Skill

Use this skill when:
- Understand how to query and correlate Konflux objects like Application, Component, PipelineRun, TaskRun, Snapshot and Release.
- Get already removed PipelineRun, TaskRun and Pod objects
- Get logs from already removed Pod

## Component object

Follows the snippet of Component object:

```yaml
apiVersion: appstudio.redhat.com/v1alpha1
kind: Component
metadata:
  name: otel-collector-main
  namespace: rhosdt-tenant
spec:
  application: otel-main
  build-nudges-ref:
  - otel-bundle-main
  componentName: otel-collector-main
  containerImage: quay.io/redhat-user-workloads/rhosdt-tenant/otel/opentelemetry-collector
  source:
    git:
      context: ./
      dockerfileUrl: Dockerfile.collector
      revision: main
      url: https://github.com/os-observability/konflux-opentelemetry.git
status:
  lastBuiltCommit: d1b34105a829d711460e73d113cd9e47c4b3adfc
  lastPromotedImage: quay.io/redhat-user-workloads/rhosdt-tenant/otel/opentelemetry-collector@sha256:cb0800a5b973f0e3e51c48b686bbaec8651a1417ba74b87f63434883e2331b94
```

## PipelineRun object

Follows the snippet of PipelineRun object:

```yaml
apiVersion: tekton.dev/v1
kind: PipelineRun
metadata:
  labels:
    app.kubernetes.io/managed-by: pipelinesascode.tekton.dev
    app.kubernetes.io/version: v0.38.0
    appstudio.openshift.io/application: otel-main
    appstudio.openshift.io/component: otel-operator-main
    kueue.x-k8s.io/priority-class: konflux-default
    kueue.x-k8s.io/queue-name: pipelines-queue
    pipelines.appstudio.openshift.io/type: build
    pipelinesascode.tekton.dev/check-run-id: "55290806256"
    pipelinesascode.tekton.dev/event-type: incoming
    pipelinesascode.tekton.dev/original-prname: otel-operator-main-on-push
    pipelinesascode.tekton.dev/repository: otel-collector-main
    pipelinesascode.tekton.dev/sha: d1b34105a829d711460e73d113cd9e47c4b3adfc
    pipelinesascode.tekton.dev/state: completed
    pipelinesascode.tekton.dev/url-org: os-observability
    pipelinesascode.tekton.dev/url-repository: konflux-opentelemetry
    tekton.dev/pipeline: otel-operator-main-on-push-ms2kp
  name: otel-operator-main-on-push-ms2kp
  namespace: rhosdt-tenant
status:
  childReferences:
    - apiVersion: tekton.dev/v1
      kind: TaskRun
      name: otel-operator-main-on-push-ms2kp-init
      pipelineTaskName: init
    - apiVersion: tekton.dev/v1
      kind: TaskRun
      name: otel-operator-main-on-push-ms2kp-clone-repository
      pipelineTaskName: clone-repository
      whenExpressions:
        - input: "true"
          operator: in
          values:
            - "true"
    - apiVersion: tekton.dev/v1
      kind: TaskRun
      name: otel-operator-main-on-push-ms2kp-prefetch-dependencies
      pipelineTaskName: prefetch-dependencies
    - apiVersion: tekton.dev/v1
      kind: TaskRun
      name: otel-operator-main-on-push-ms2kp-build-images-0
      pipelineTaskName: build-images
      whenExpressions:
        - input: "true"
          operator: in
          values:
            - "true"
  results:
    - name: IMAGE_URL
      value: quay.io/redhat-user-workloads/rhosdt-tenant/otel/opentelemetry-operator:d1b34105a829d711460e73d113cd9e47c4b3adfc
    - name: IMAGE_DIGEST
      value: sha256:03cc17a2bd8d0d94bac2ff3e55528c7dfad3f84c24b8944309d6b83c7d429e93
    - name: CHAINS-GIT_URL
      value: https://github.com/os-observability/konflux-opentelemetry
    - name: CHAINS-GIT_COMMIT
      value: d1b34105a829d711460e73d113cd9e47c4b3adfc
  conditions:
    - lastTransitionTime: "2025-11-13T11:47:24Z"
      message: 'Tasks Completed: 19 (Failed: 0, Cancelled 0), Skipped: 0'
      reason: Succeeded
      status: "True"
      type: Succeeded
```

## TaskRun object

Follows the snippet of TaskRun object:

```yaml
apiVersion: tekton.dev/v1
kind: TaskRun
metadata:
  labels:
    app.kubernetes.io/managed-by: pipelinesascode.tekton.dev
    app.kubernetes.io/version: v0.38.0
    appstudio.openshift.io/application: otel-main
    appstudio.openshift.io/component: otel-operator-main
    build.appstudio.redhat.com/build_type: docker
    build.appstudio.redhat.com/target-platform: linux-ppc64le
    kueue.x-k8s.io/priority-class: konflux-default
    kueue.x-k8s.io/queue-name: pipelines-queue
    pipelines.appstudio.openshift.io/type: build
    pipelinesascode.tekton.dev/check-run-id: "55217348140"
    pipelinesascode.tekton.dev/event-type: incoming
    pipelinesascode.tekton.dev/original-prname: otel-operator-main-on-push
    pipelinesascode.tekton.dev/repository: otel-collector-main
    pipelinesascode.tekton.dev/sha: 8ba2e60ab95f65af6a61f01dc255f9b05c8c7292
    pipelinesascode.tekton.dev/state: queued
    pipelinesascode.tekton.dev/url-org: os-observability
    pipelinesascode.tekton.dev/url-repository: konflux-opentelemetry
    tekton.dev/memberOf: tasks
    tekton.dev/pipeline: otel-operator-main-on-push-cjz8d
    tekton.dev/pipelineRun: otel-operator-main-on-push-cjz8d
    tekton.dev/pipelineRunUID: 2483e676-9177-4184-844e-c103e5c44313
    tekton.dev/pipelineTask: build-images
    tekton.dev/task: buildah-remote-oci-ta
  name: otel-operator-main-on-push-cjz8d-build-images-2
  namespace: rhosdt-tenant
status:
  podName: otel-operator-main-on-push-cjz8d-build-images-2-pod
  conditions:
    - lastTransitionTime: "2025-11-12T18:11:33Z"
      message: All Steps have completed executing
      reason: Succeeded
      status: "True"
      type: Succeeded
```

## Release object

Follows the snippet of Release object:

```yaml
apiVersion: appstudio.redhat.com/v1alpha1
kind: Release
metadata:
  labels:
    appstudio.openshift.io/application: otel-main
    appstudio.openshift.io/build-pipelinerun: otel-bundle-main-on-push-6r6j8
    appstudio.openshift.io/component: otel-bundle-main
    pac.test.appstudio.openshift.io/check-run-id: "55293065390"
    pac.test.appstudio.openshift.io/event-type: incoming
    pac.test.appstudio.openshift.io/original-prname: otel-bundle-main-on-push
    pac.test.appstudio.openshift.io/repository: otel-collector-main
    pac.test.appstudio.openshift.io/sha: d1b34105a829d711460e73d113cd9e47c4b3adfc
    pac.test.appstudio.openshift.io/state: completed
    pac.test.appstudio.openshift.io/url-org: os-observability
    pac.test.appstudio.openshift.io/url-repository: konflux-opentelemetry
    release.appstudio.openshift.io/automated: "true"
  name: otel-main-2xpp5-d1b3410-j6262
  namespace: rhosdt-tenant
status:
  conditions:
    - lastTransitionTime: "2025-11-13T12:12:37Z"
      message: ""
      reason: Succeeded
      status: "True"
      type: Released
```

## Snapshot object

Follows the snippet of Snapshot obeject:

```yaml
apiVersion: appstudio.redhat.com/v1alpha1
kind: Snapshot
metadata:
  labels:
    appstudio.openshift.io/application: otel-main
    appstudio.openshift.io/build-pipelinerun: otel-target-allocator-main-on-push-b4rj4
    appstudio.openshift.io/component: otel-target-allocator-main
    pac.test.appstudio.openshift.io/check-run-id: "55306002131"
    pac.test.appstudio.openshift.io/event-type: incoming
    pac.test.appstudio.openshift.io/original-prname: otel-target-allocator-main-on-push
    pac.test.appstudio.openshift.io/repository: otel-collector-main
    pac.test.appstudio.openshift.io/sha: d1b34105a829d711460e73d113cd9e47c4b3adfc
    pac.test.appstudio.openshift.io/state: completed
    pac.test.appstudio.openshift.io/url-org: os-observability
    pac.test.appstudio.openshift.io/url-repository: konflux-opentelemetry
    test.appstudio.openshift.io/pipelinerunfinishtime: "1763044403"
    test.appstudio.openshift.io/type: component
  name: otel-main-8s28p
  namespace: rhosdt-tenant
spec:
  components:
    - containerImage: quay.io/redhat-user-workloads/rhosdt-tenant/otel/opentelemetry-bundle@sha256:dfc3d2a037f32fceab65f6be052227c775b49282b02090ed6dcff062bfd0edd0
      name: otel-bundle-main
      source:
        git:
          context: ./
          dockerfileUrl: Dockerfile.bundle
          revision: d1b34105a829d711460e73d113cd9e47c4b3adfc
          url: https://github.com/os-observability/konflux-opentelemetry.git
status:
  conditions:
    - lastTransitionTime: "2025-11-13T14:33:32Z"
      message: No required IntegrationTestScenarios found, skipped testing
      reason: Passed
      status: "True"
      type: AppStudioTestSucceeded
    - lastTransitionTime: "2025-11-13T14:33:32Z"
      message: The Snapshot was auto-released
      reason: AutoReleased
      status: "True"
      type: AutoReleased
```

## Query objects

Any labels can be used to query specific objects:

- **Query by Application**: `kubectl get {object-type} -l appstudio.openshift.io/application={component-name}`
- **Query by Component**: `kubectl get {object-type} -l appstudio.openshift.io/component={component-name}`
- **Query by PipelineRun**: `kubectl get {object-type} -l appstudio.openshift.io/build-pipelinerun={pipelinerun}`
- **Query by Git SHA**: `kubectl get {object-type} -l pac.test.appstudio.openshift.io/sha={git-sha}`

## Get removed PipelineRun, TaskRun, Pods and logs

The [kubearchive CLI](https://kubearchive.github.io/kubearchive/main/cli/installation.html) can be used to query removed objects like PipelineRun, TaskRun, Pods and Pod logs.
The tool has similar commands like `kubectl` but it does not support getting object via label selector.

- **Prerequisites Check**
    - Verify `kubectl ka` CLI is installed: `which kubectl ka`
    - If it is not installed the installation instructions are at https://kubearchive.github.io/kubearchive/main/cli/installation.html
- **Get PipelineRun**
    ```bash
    export KUBECTL_PLUGIN_KA_HOST="https://kubearchive-api-server-product-kubearchive.apps.$(oc whoami --show-server | sed -E 's|^.*api\.?(.*):[0-9]+$|\1|')"
    kubectl ka get pipelinerun {pipelinerun}
    ```
- **Get TaskRun**
    ```bash
    export KUBECTL_PLUGIN_KA_HOST="https://kubearchive-api-server-product-kubearchive.apps.$(oc whoami --show-server | sed -E 's|^.*api\.?(.*):[0-9]+$|\1|')"
    kubectl ka get pipelinerun {taskrun}
    ```
- **Get Pod logs**
    ```bash
    export KUBECTL_PLUGIN_KA_HOST="https://kubearchive-api-server-product-kubearchive.apps.$(oc whoami --show-server | sed -E 's|^.*api\.?(.*):[0-9]+$|\1|')"
    kubectl ka logs pod {pod}
    ```
