---
name: docker-registry-deployment
description: Deep knowledge about building and pushing container images to Docker registries (DockerHub, GHCR, ECR, GCR).
type: transform
tier: library
domain: deploy
trigger: "when deploying to a Docker Registry"
---

## Context
Deploying {{project_name}} ({{project_type}}) to a Docker Registry (DockerHub, GitHub Container Registry, AWS ECR, Google Artifact Registry).
You will follow a strict 6-phase Deployment Lifecycle Contract. 

## Instructions

Execute the following phases in order:

### Phase 1: Authentication
1. Authenticate to the target container registry.
2. For DockerHub or GHCR, use `docker login <registry-url> -u <username> -p <password/token>`. (For GHCR, the URL is `ghcr.io`).
3. For AWS ECR, run `aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com`.
4. For GCP GCR/Artifact Registry, run `gcloud auth configure-docker <region>-docker.pkg.dev`.

### Phase 2: Build
1. Prepare the artifacts for deployment.
2. Build your Docker image: `docker build -t <registry-url>/<repository-name>/<image-name>:<tag> .`
3. Consider using `--build-arg` if your `Dockerfile` requires environment variables during the build process.
4. (Optional but recommended) Build multi-architecture images using `docker buildx build --platform linux/amd64,linux/arm64 -t <registry-url>/<repository-name>/<image-name>:<tag> --push .`

### Phase 3: Install / Provisioning
1. Ensure the target repository exists in the registry.
2. For AWS ECR, you might need to create the repository first: `aws ecr create-repository --repository-name <repository-name>`.
3. For DockerHub or GHCR, pushing to a new repository name usually creates it automatically (if permissions allow).

### Phase 4: Deploy
1. Ship the artifact to the registry.
2. Push the image: `docker push <registry-url>/<repository-name>/<image-name>:<tag>`.
3. If you used `docker buildx build --push` in Phase 2, this step is already completed.
4. Optionally, tag the same image as `latest` and push it as well: `docker tag <registry-url>/<repository-name>/<image-name>:<tag> <registry-url>/<repository-name>/<image-name>:latest && docker push <registry-url>/<repository-name>/<image-name>:latest`.

### Phase 5: Checking
1. Verify the deployment was successful.
2. The `docker push` command output should confirm all layers were pushed.
3. You can also verify by pulling the image: `docker pull <registry-url>/<repository-name>/<image-name>:<tag>`.
4. For ECR, you can list images: `aws ecr describe-images --repository-name <repository-name>`.

### Phase 6: Update / Rollback
1. If Phase 5 fails (e.g., authentication error or network timeout), check your credentials and network connection.
2. If a bad image was pushed, there is no direct "rollback" in a registry, but you should delete the bad tag or push the previous known-good image to the `latest` tag.
3. Note the failure in the progress log.

## Validation
- [ ] Registry authentication (`docker login`) succeeds.
- [ ] Docker image builds successfully.
- [ ] Docker image is pushed to the registry.
- [ ] Image can be pulled successfully.
