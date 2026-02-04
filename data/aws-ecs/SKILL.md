---
name: aws-ecs
description: Deploy and manage containerized applications on ECS/Fargate
sasmp_version: "1.3.0"
bonded_agent: 08-aws-devops
bond_type: PRIMARY_BOND
---

# AWS ECS Skill

Deploy containerized applications with ECS and Fargate.

## Quick Reference

| Attribute | Value |
|-----------|-------|
| AWS Service | ECS, Fargate |
| Complexity | Medium-High |
| Est. Time | 20-45 min |
| Prerequisites | VPC, ECR image, IAM roles |

## Parameters

### Required
| Parameter | Type | Description | Validation |
|-----------|------|-------------|------------|
| cluster_name | string | ECS cluster name | ^[a-zA-Z0-9_-]{1,255}$ |
| service_name | string | Service name | ^[a-zA-Z0-9_-]{1,255}$ |
| image_uri | string | Container image | ECR or Docker Hub URI |
| cpu | int | CPU units | 256, 512, 1024, 2048, 4096 |
| memory | int | Memory MB | Valid for CPU |

### Optional
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| desired_count | int | 2 | Number of tasks |
| launch_type | string | FARGATE | FARGATE or EC2 |
| platform_version | string | LATEST | Fargate platform version |
| health_check_path | string | /health | ALB health check path |
| autoscaling | bool | true | Enable auto-scaling |

## CPU/Memory Combinations (Fargate)

| CPU | Memory Options |
|-----|----------------|
| 256 | 512, 1024, 2048 |
| 512 | 1024-4096 (1GB increments) |
| 1024 | 2048-8192 (1GB increments) |
| 2048 | 4096-16384 (1GB increments) |
| 4096 | 8192-30720 (1GB increments) |

## Implementation

### Task Definition
```json
{
  "family": "my-app",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::123456789012:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::123456789012:role/ecsTaskRole",
  "containerDefinitions": [
    {
      "name": "app",
      "image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app:latest",
      "portMappings": [
        {"containerPort": 8080, "protocol": "tcp"}
      ],
      "essential": true,
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/my-app",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:8080/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 60
      },
      "secrets": [
        {
          "name": "DB_PASSWORD",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:123456789012:secret:db-password"
        }
      ]
    }
  ]
}
```

### Create Service
```bash
aws ecs create-service \
  --cluster prod-cluster \
  --service-name my-service \
  --task-definition my-app:1 \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration '{
    "awsvpcConfiguration": {
      "subnets": ["subnet-111", "subnet-222"],
      "securityGroups": ["sg-xxx"],
      "assignPublicIp": "DISABLED"
    }
  }' \
  --load-balancers '[{
    "targetGroupArn": "arn:aws:elasticloadbalancing:...",
    "containerName": "app",
    "containerPort": 8080
  }]' \
  --deployment-configuration '{
    "maximumPercent": 200,
    "minimumHealthyPercent": 100,
    "deploymentCircuitBreaker": {
      "enable": true,
      "rollback": true
    }
  }'
```

### Auto Scaling
```bash
# Register scalable target
aws application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --resource-id service/prod-cluster/my-service \
  --scalable-dimension ecs:service:DesiredCount \
  --min-capacity 2 \
  --max-capacity 10

# Target tracking policy
aws application-autoscaling put-scaling-policy \
  --service-namespace ecs \
  --resource-id service/prod-cluster/my-service \
  --scalable-dimension ecs:service:DesiredCount \
  --policy-name cpu-tracking \
  --policy-type TargetTrackingScaling \
  --target-tracking-scaling-policy-configuration '{
    "TargetValue": 70.0,
    "PredefinedMetricSpecification": {
      "PredefinedMetricType": "ECSServiceAverageCPUUtilization"
    },
    "ScaleInCooldown": 300,
    "ScaleOutCooldown": 60
  }'
```

## Troubleshooting

### Common Issues
| Symptom | Cause | Solution |
|---------|-------|----------|
| Task won't start | Image pull failed | Check ECR permissions |
| Task unhealthy | Health check failing | Increase startPeriod |
| Service stuck | Deployment circuit breaker | Check task logs |
| OOM killed | Memory exceeded | Increase memory |

### Debug Checklist
- [ ] Image exists in ECR and accessible?
- [ ] Task execution role has permissions?
- [ ] Security group allows container port?
- [ ] Subnets have NAT for ECR access?
- [ ] Secrets Manager accessible?
- [ ] Health check path responding?
- [ ] Container starts within health check startPeriod?

### Task Failure Analysis
```bash
# Get stopped task details
aws ecs describe-tasks \
  --cluster prod-cluster \
  --tasks arn:aws:ecs:...:task/xxx \
  --query 'tasks[0].{status:lastStatus,reason:stoppedReason,containers:containers[*].{name:name,reason:reason}}'
```

### Common Stop Reasons
```
CannotPullContainerError → ECR image or permissions
ResourceInitializationError → Secrets/ENI issue
EssentialContainerExited → Application crash
OutOfMemoryError → Increase memory
HealthCheckFailure → Fix health check
```

## Test Template

```python
def test_ecs_service_healthy():
    # Arrange
    cluster = "prod-cluster"
    service = "my-service"

    # Act
    response = ecs.describe_services(
        cluster=cluster,
        services=[service]
    )

    # Assert
    service_info = response['services'][0]
    assert service_info['status'] == 'ACTIVE'
    assert service_info['runningCount'] >= service_info['desiredCount']
    assert len(service_info['deployments']) == 1  # No pending deployments
```

## Assets

- `assets/task-definition.json` - ECS task definition template

## References

- [ECS User Guide](https://docs.aws.amazon.com/AmazonECS/latest/userguide/)
- [ECS Best Practices](https://docs.aws.amazon.com/AmazonECS/latest/bestpracticesguide/)
