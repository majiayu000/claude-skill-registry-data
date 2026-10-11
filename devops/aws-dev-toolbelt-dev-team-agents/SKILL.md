---
name: aws
description: AWS — ECS, EC2, RDS, S3, CloudFront, ALB, IAM best practices.
---

# AWS Deployment

## Core Principle: Cost-First Architecture

Always ask: "Is there a managed service or simpler option that costs less?" Before adding a service, estimate monthly cost at expected load.

**Free tier / low-cost anchors**: EC2 t3.micro, RDS t3.micro, S3 Standard, CloudFront (1TB/month free tier), Lambda (1M req/month free).

---

## Common Stack Options

### Option A — EC2 + Docker (simplest, lowest cost)
Best for: small teams, predictable traffic, tight budgets.

```
Route 53 → CloudFront → ALB → EC2 (Docker + docker-compose) → RDS
```

Cost estimate (us-east-1): ~$30–80/month for t3.small EC2 + db.t3.micro RDS.

### Option B — ECS Fargate (no server management)
Best for: variable traffic, no ops overhead.

```
Route 53 → CloudFront → ALB → ECS Fargate Tasks → RDS Aurora Serverless
```

Cost estimate: ~$50–150/month depending on task size and usage.

### Option C — App Runner (zero ops)
Best for: simple HTTP APIs, minimal config.

```
ECR → App Runner → RDS Proxy → RDS
```

---

## ECR — Container Registry

```bash
# Authenticate
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  123456789.dkr.ecr.us-east-1.amazonaws.com

# Build and push
docker build -t myapp .
docker tag myapp:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/myapp:$GIT_SHA
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/myapp:$GIT_SHA

# Enable lifecycle policy to avoid storage costs
aws ecr put-lifecycle-policy --repository-name myapp \
  --lifecycle-policy-text '{"rules":[{"rulePriority":1,"selection":{"tagStatus":"untagged","countType":"imageCountMoreThan","countNumber":3},"action":{"type":"expire"}}]}'
```

## ECS Fargate — Task Definition

```json
{
  "family": "myapp",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::ACCOUNT:role/ecsTaskExecutionRole",
  "containerDefinitions": [{
    "name": "app",
    "image": "ACCOUNT.dkr.ecr.REGION.amazonaws.com/myapp:TAG",
    "portMappings": [{"containerPort": 8000}],
    "environment": [{"name": "APP_ENV", "value": "production"}],
    "secrets": [
      {"name": "DB_PASSWORD", "valueFrom": "arn:aws:ssm:REGION:ACCOUNT:parameter/myapp/db-password"}
    ],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "/ecs/myapp",
        "awslogs-region": "us-east-1",
        "awslogs-stream-prefix": "ecs"
      }
    },
    "healthCheck": {
      "command": ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"],
      "interval": 30,
      "timeout": 5,
      "retries": 3
    }
  }]
}
```

## Secrets — Parameter Store (SSM)

Never use environment variables for secrets in task definitions. Use SSM Parameter Store:

```bash
# Store
aws ssm put-parameter \
  --name "/myapp/db-password" \
  --value "supersecret" \
  --type SecureString

# The ECS task execution role needs ssm:GetParameters permission
```

## IAM — Least Privilege

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": [
      "ssm:GetParameters",
      "secretsmanager:GetSecretValue"
    ],
    "Resource": [
      "arn:aws:ssm:REGION:ACCOUNT:parameter/myapp/*"
    ]
  }]
}
```

**Rules**:
- Never use root account for deployments
- Create IAM users/roles with minimum permissions needed
- Use IAM roles for EC2/ECS — never embed access keys in containers
- Enable MFA for all human users

## Cost Optimization Checklist

- [ ] Right-size instances (start small, scale based on CloudWatch metrics)
- [ ] Use Savings Plans or Reserved Instances for predictable workloads (up to 72% off)
- [ ] Enable ECR lifecycle policies to remove old images
- [ ] Set CloudWatch log retention (default is unlimited — costs add up)
- [ ] Use S3 Intelligent-Tiering for infrequently accessed objects
- [ ] Set up AWS Budgets alerts at 80% and 100% of monthly budget
- [ ] Delete unused Elastic IPs (charged when not attached)
- [ ] Use Aurora Serverless v2 for dev/staging databases (scales to zero)

## Useful CLI Commands

```bash
# Check running ECS tasks
aws ecs list-tasks --cluster myapp-cluster --service-name myapp

# Get task logs
aws logs tail /ecs/myapp --follow

# Force new deployment
aws ecs update-service --cluster myapp-cluster --service myapp --force-new-deployment

# Check costs
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-01-31 \
  --granularity MONTHLY \
  --metrics BlendedCost
```
