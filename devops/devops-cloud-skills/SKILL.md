---
name: devops-cloud-skills
description: Master Docker, Kubernetes, Terraform, AWS, Linux, CI/CD, and infrastructure as code. Deploy and manage cloud applications at scale.
sasmp_version: "1.3.0"
skill_type: atomic
version: "2.0.0"

parameters:
  platform:
    type: string
    enum: [aws, gcp, azure, multi-cloud]
    default: aws
  orchestration:
    type: string
    enum: [kubernetes, ecs, nomad]
    default: kubernetes

validation_rules:
  - pattern: "^[a-z][a-z0-9-]*$"
    target: resource_names
    message: Resource names must be lowercase with hyphens
  - pattern: "^v[0-9]+\\.[0-9]+\\.[0-9]+$"
    target: image_tags
    message: Use semantic versioning for images

retry_config:
  max_attempts: 3
  backoff: exponential
  initial_delay_ms: 5000
  max_delay_ms: 120000

logging:
  on_entry: "[DevOps] Starting: {task}"
  on_success: "[DevOps] Completed: {task}"
  on_error: "[DevOps] Failed: {task} - {error}"

dependencies:
  agents:
    - devops-cloud-engineer
---

# DevOps & Cloud Engineering Skills

## Docker Best Practices

```dockerfile
# Multi-stage build for smaller images
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app

# Non-root user for security
RUN useradd -m appuser
USER appuser

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --chown=appuser:appuser . .

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:5000/health || exit 1

ENV PORT=5000
EXPOSE 5000
CMD ["python", "app.py"]
```

```bash
# Docker commands with best practices
docker build --no-cache -t myapp:v1.0.0 .
docker run -d --name myapp \
  --restart=unless-stopped \
  --memory=512m \
  --cpus=0.5 \
  -p 5000:5000 \
  myapp:v1.0.0
```

## Kubernetes Production Config

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app: myapp
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
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
        image: myapp:v1.0.0
        ports:
        - containerPort: 5000
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5
        env:
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: password
---
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  type: ClusterIP
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 5000
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## Terraform with Modules

```hcl
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket = "terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}

# Variables
variable "environment" {
  type        = string
  description = "Deployment environment"
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

# EC2 with proper tagging
resource "aws_instance" "web" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = var.environment == "prod" ? "t3.medium" : "t3.micro"

  tags = {
    Name        = "web-${var.environment}"
    Environment = var.environment
    ManagedBy   = "terraform"
  }

  lifecycle {
    create_before_destroy = true
  }
}

# Output with sensitive handling
output "instance_ip" {
  value       = aws_instance.web.public_ip
  description = "Public IP of the instance"
}
```

## CI/CD with GitHub Actions

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      - run: pip install -r requirements.txt
      - run: pytest --cov=app tests/

  build:
    needs: test
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    outputs:
      image: ${{ steps.build.outputs.image }}
    steps:
      - uses: actions/checkout@v4
      - uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - id: build
        run: |
          IMAGE=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          docker build -t $IMAGE .
          docker push $IMAGE
          echo "image=$IMAGE" >> $GITHUB_OUTPUT

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: azure/k8s-set-context@v3
        with:
          kubeconfig: ${{ secrets.KUBECONFIG }}
      - run: |
          kubectl set image deployment/myapp \
            app=${{ needs.build.outputs.image }}
          kubectl rollout status deployment/myapp
```

## Monitoring & Alerting

```yaml
# Prometheus alert rules
groups:
- name: application
  rules:
  - alert: HighErrorRate
    expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: High error rate detected
      description: "Error rate is {{ $value | humanizePercentage }}"

  - alert: PodNotReady
    expr: kube_pod_status_ready{condition="false"} == 1
    for: 5m
    labels:
      severity: warning
```

## Troubleshooting Guide

| Symptom | Cause | Solution |
|---------|-------|----------|
| ImagePullBackOff | Auth/tag issue | Check registry credentials |
| CrashLoopBackOff | App crashes | Check logs, fix startup |
| OOMKilled | Memory exceeded | Increase limits |
| Pending pods | No resources | Scale cluster or adjust requests |

## Unit Test Template

```bash
#!/bin/bash
# infrastructure-test.sh

set -e

echo "Testing Terraform configuration..."
terraform init -backend=false
terraform validate
terraform fmt -check

echo "Testing Docker build..."
docker build -t test-image:latest .
docker run --rm test-image:latest python -c "print('OK')"

echo "Testing Kubernetes manifests..."
kubectl apply --dry-run=client -f k8s/

echo "All tests passed!"
```

## Key Concepts Checklist

- [ ] Docker images and containers
- [ ] Docker Compose multi-container
- [ ] Kubernetes pods, services, deployments
- [ ] Helm package management
- [ ] Terraform configuration
- [ ] AWS EC2, S3, RDS, VPC
- [ ] CI/CD pipeline setup
- [ ] Monitoring and alerting
- [ ] Log aggregation
- [ ] Infrastructure security
- [ ] Cost optimization
- [ ] Disaster recovery

---

**Source**: https://roadmap.sh
**Version**: 2.0.0
**Last Updated**: 2025-01-01
