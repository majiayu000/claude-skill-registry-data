---
name: paas
description: Platform as a Service cloud computing
license: MIT
compatibility: opencode
metadata:
  audience: developer, devops-engineer
  category: devops
---

## What I do

- Deploy applications to PaaS platforms
- Configure managed services and databases
- Implement auto-scaling and high availability
- Set up CI/CD for PaaS deployments
- Manage application performance
- Optimize PaaS costs

## When to use me

- When focusing on code, not infrastructure
- When building web applications quickly
- When needing managed databases
- When implementing auto-scaling
- When reducing operational overhead
- When building cloud-native applications

## Key Concepts

### Heroku Deployment

```yaml
# app.json - Heroku Review Apps
{
  "name": "myapp",
  "buildpacks": [
    {
      "url": "heroku/python"
    }
  ],
  "environments": {
    "review": {
      "addons": ["heroku-postgresql:hobby-dev"],
      "environment": {
        "LOG_LEVEL": "DEBUG"
      },
      "formation": {
        "web": {
          "quantity": 1,
          "size": "hobby"
        }
      }
    },
    "production": {
      "addons": ["heroku-postgresql:standard-0"],
      "formation": {
        "web": {
          "quantity": 2,
          "size": "performance-m"
        }
      }
    }
  }
}
```

### AWS Elastic Beanstalk

```yaml
# .ebextensions/python.config
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: application:application
  aws:elasticbeanstalk:environment:proxy:staticfiles:
    /static: static
  aws:autoscaling:asg:
    MinSize: 2
    MaxSize: 10
  aws:autoscaling:trigger:
    MeasureName: CPUUtilization
    UpperThreshold: 80
    LowerThreshold: 20
```

### Azure App Service

```yaml
# azure-pipelines.yml
trigger: main

pool:
  vmImage: 'ubuntu-latest'

variables:
  azureSubscription: 'Azure-Service-Connection'
  appName: 'myapp'
  runtime: 'python'
  version: '3.11'

stages:
  - stage: Build
    jobs:
      - job: BuildJob
        steps:
          - task: UsePythonVersion@0
          - script: |
              pip install -r requirements.txt
              pip install pytest
              pytest tests/
          - task: ArchiveFiles@2
            inputs:
              rootFolder: '$(System.DefaultWorkingDirectory)'
              archiveFile: '$(Build.ArtifactStagingDirectory)/$(Build.BuildId).zip'
          - publish: $(Build.ArtifactStagingDirectory)/$(Build.BuildId).zip
            artifact: drop

  - stage: Deploy
    jobs:
      - deployment: DeployJob
        environment: 'production'
        strategy:
          runOnce:
            deploy:
              steps:
                - task: AzureWebApp@1
                  inputs:
                    azureSubscription: $(azureSubscription)
                    appType: 'webApp'
                    appName: $(appName)
                    package: '$(Pipeline.Workspace)/drop/**/*.zip'
```

### GCP App Engine

```yaml
# app.yaml
runtime: python311
env: standard

instance_class: F2
automatic_scaling:
  min_instances: 1
  max_instances: 10
  target_cpu_utilization: 0.65
  min_latency: '500ms'

inbound_services:
  - warmup

liveness_check:
  path: /_ah/health
  check_interval_seconds: 30
  timeout_seconds: 4
  failure_threshold: 2
  success_threshold: 2

readiness_check:
  path: /_ah/ready
  check_interval_seconds: 5
  timeout_seconds: 4
  failure_threshold: 2
  success_threshold: 1

env_variables:
  LOG_LEVEL: 'INFO'
  DATABASE_URL: 'postgres://...'

beta_settings:
  cloud_sql_instances: 'project:region:instance'
```

### Cloud Run Deployment

```yaml
# cloudrun.yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: myapp
  annotations:
    run.googleapis.com/launch-stage: BETA
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: "1"
        autoscaling.knative.dev/maxScale: "10"
    spec:
      containers:
        - image: gcr.io/project/myapp:latest
          ports:
            - containerPort: 8080
          resources:
            limits:
              cpu: "1000m"
              memory: "512Mi"
          env:
            - name: PORT
              value: "8080"
          startupProbe:
            httpGet:
              path: /_ah/health
            initialDelaySeconds: 0
            periodSeconds: 10
            timeoutSeconds: 1
            failureThreshold: 3
```

### PaaS Comparison

| Platform | Languages | Database | Scaling | Best For |
|----------|-----------|----------|---------|----------|
| Heroku | All | Add-ons | Auto | Quick deployment |
| AWS EB | All | RDS, ElastiCache | Auto | AWS integration |
| Azure App Service | .NET, Node, Python | SQL, Cosmos | Auto | Enterprise .NET |
| Cloud Run | All | Cloud SQL | Auto | Containers |
| Vercel | Node, Go, Python | External | Auto | Frontend/JAMstack |

### Key Benefits

- **Managed Runtime**: Don't manage OS or middleware
- **Auto-scaling**: Handle traffic spikes automatically
- **Managed Services**: Databases, caches, queues
- **CI/CD**: Built-in deployment pipelines
- **Monitoring**: Integrated logging and metrics
- **Security**: Patched and secured platforms
