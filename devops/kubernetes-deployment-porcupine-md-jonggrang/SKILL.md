---
name: kubernetes-deployment
description: Deep knowledge about deploying applications to Kubernetes clusters using kubectl, helm, and manifests.
type: transform
tier: library
domain: deploy
trigger: "when deploying to Kubernetes"
---

## Context
Deploying {{project_name}} ({{project_type}}) to Kubernetes.
You will follow a strict 6-phase Deployment Lifecycle Contract. 

## Instructions

Execute the following phases in order:

### Phase 1: Authentication
1. Ensure the `KUBECONFIG` environment variable is set to a valid configuration file, or the configuration is located in `~/.kube/config`.
2. Authenticate to the cluster (if using cloud providers like AWS EKS or GCP GKE, use their respective commands: `aws eks update-kubeconfig` or `gcloud container clusters get-credentials`).
3. Verify access by running `kubectl cluster-info` and `kubectl get nodes`.

### Phase 2: Build
1. Prepare the artifacts for deployment.
2. Build your Docker image: `docker build -t <registry>/<image-name>:<tag> .`
3. Push the image to your container registry (DockerHub, GHCR, ECR, GCR): `docker push <registry>/<image-name>:<tag>`

### Phase 3: Install / Provisioning
1. Ensure the target Kubernetes namespace exists: `kubectl create namespace <namespace>` (if it doesn't exist).
2. Create or update necessary ConfigMaps and Secrets: `kubectl apply -f k8s/configmap.yaml` or use `kubectl create secret generic`.
3. If using Helm, ensure the Helm chart dependencies are updated: `helm dependency update <chart-dir>`.

### Phase 4: Deploy
1. Ship the artifact to Kubernetes.
2. Using raw manifests: Update the image tag in your Deployment YAML, then run `kubectl apply -f k8s/`.
3. Using Kustomize: `kustomize build k8s/ | kubectl apply -f -`.
4. Using Helm: `helm upgrade --install <release-name> <chart-dir> --namespace <namespace> --set image.tag=<tag>`.

### Phase 5: Checking
1. Verify the deployment was successful.
2. Check the rollout status: `kubectl rollout status deployment/<deployment-name> -n <namespace>`. This command will block until the deployment is successful or fails.
3. Check pod status if there are issues: `kubectl get pods -n <namespace>`.
4. Inspect pod logs if they are crashing: `kubectl logs -l app=<app-label> -n <namespace>`.
5. Curl the service or ingress URL if available externally.

### Phase 6: Update / Rollback
1. If Phase 5 fails (e.g., rollout gets stuck or pods crashloop), immediately initiate a rollback.
2. Using kubectl: `kubectl rollout undo deployment/<deployment-name> -n <namespace>`.
3. Using Helm: `helm rollback <release-name> -n <namespace>`.
4. Note the failure in the progress log.

## Validation
- [ ] Cluster authentication (`kubectl cluster-info`) succeeds.
- [ ] Docker image builds and pushes successfully.
- [ ] Kubernetes rollout status is successful.
- [ ] Pods are running and healthy.
