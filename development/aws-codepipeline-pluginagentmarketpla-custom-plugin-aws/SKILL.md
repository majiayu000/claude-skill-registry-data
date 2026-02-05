---
name: aws-codepipeline
description: Build automated CI/CD pipelines with CodePipeline and CodeBuild
sasmp_version: "1.3.0"
bonded_agent: 08-aws-devops
bond_type: SECONDARY_BOND
---

# AWS CodePipeline Skill

Create automated CI/CD pipelines for application deployment.

## Quick Reference

| Attribute | Value |
|-----------|-------|
| AWS Service | CodePipeline, CodeBuild |
| Complexity | Medium |
| Est. Time | 20-45 min |
| Prerequisites | Source repo, IAM role, deployment target |

## Parameters

### Required
| Parameter | Type | Description | Validation |
|-----------|------|-------------|------------|
| pipeline_name | string | Pipeline name | ^[A-Za-z0-9.@_-]{1,100}$ |
| source_provider | string | Source type | GitHub, CodeCommit, S3 |
| deployment_target | string | Deploy target | ECS, Lambda, EC2, S3 |

### Optional
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| branch | string | main | Source branch |
| build_image | string | aws/codebuild/standard:7.0 | Build environment |
| deploy_strategy | string | rolling | rolling, blue_green, canary |
| approval_required | bool | false | Manual approval gate |

## Pipeline Architecture

```
┌──────────┐   ┌───────┐   ┌──────┐   ┌─────────────┐
│  Source  │───│ Build │───│ Test │───│  Deploy-Dev │
└──────────┘   └───────┘   └──────┘   └──────┬──────┘
                                             │
┌─────────────┐   ┌──────────┐   ┌──────────┴──────────┐
│ Deploy-Prod │◄──│ Approval │◄──│  Deploy-Staging     │
└─────────────┘   └──────────┘   └─────────────────────┘
```

## Implementation

### Create Pipeline
```bash
# Create pipeline with GitHub source
aws codepipeline create-pipeline --cli-input-json '{
  "pipeline": {
    "name": "my-app-pipeline",
    "roleArn": "arn:aws:iam::123456789012:role/CodePipelineRole",
    "stages": [
      {
        "name": "Source",
        "actions": [{
          "name": "GitHub",
          "actionTypeId": {
            "category": "Source",
            "owner": "ThirdParty",
            "provider": "GitHub",
            "version": "2"
          },
          "configuration": {
            "ConnectionArn": "arn:aws:codestar-connections:...",
            "FullRepositoryId": "org/repo",
            "BranchName": "main"
          },
          "outputArtifacts": [{"name": "SourceOutput"}]
        }]
      },
      {
        "name": "Build",
        "actions": [{
          "name": "CodeBuild",
          "actionTypeId": {
            "category": "Build",
            "owner": "AWS",
            "provider": "CodeBuild",
            "version": "1"
          },
          "inputArtifacts": [{"name": "SourceOutput"}],
          "outputArtifacts": [{"name": "BuildOutput"}],
          "configuration": {
            "ProjectName": "my-build-project"
          }
        }]
      }
    ]
  }
}'
```

### BuildSpec Template
```yaml
# buildspec.yml
version: 0.2

env:
  variables:
    NODE_ENV: production
  secrets-manager:
    DB_PASSWORD: prod/db:password

phases:
  install:
    runtime-versions:
      nodejs: 20
    commands:
      - npm ci

  pre_build:
    commands:
      - npm run lint
      - npm run test:unit

  build:
    commands:
      - npm run build
      - docker build -t $ECR_REPO:$CODEBUILD_RESOLVED_SOURCE_VERSION .

  post_build:
    commands:
      - docker push $ECR_REPO:$CODEBUILD_RESOLVED_SOURCE_VERSION
      - printf '[{"name":"app","imageUri":"%s"}]' $ECR_REPO:$CODEBUILD_RESOLVED_SOURCE_VERSION > imagedefinitions.json

artifacts:
  files:
    - imagedefinitions.json
    - appspec.yml

cache:
  paths:
    - node_modules/**/*
```

## Deployment Strategies

| Strategy | Risk | Rollback | Use Case |
|----------|------|----------|----------|
| Rolling | Medium | Minutes | Standard updates |
| Blue/Green | Low | Instant | Zero-downtime |
| Canary | Lowest | Instant | Gradual validation |
| All-at-once | High | Minutes | Dev/test only |

## Troubleshooting

### Common Issues
| Symptom | Cause | Solution |
|---------|-------|----------|
| Source failed | Connection issue | Check GitHub connection |
| Build failed | buildspec error | Check CodeBuild logs |
| Deploy failed | IAM or target | Check deployment logs |
| Stuck at approval | No approver | Notify approvers |

### Debug Checklist
- [ ] Pipeline IAM role has permissions?
- [ ] Source connection authorized?
- [ ] Build environment has required tools?
- [ ] Artifact bucket accessible?
- [ ] Deploy target accessible?
- [ ] AppSpec/imagedefinitions correct?

### Pipeline Execution Analysis
```bash
# Get failed execution details
aws codepipeline get-pipeline-execution \
  --pipeline-name my-pipeline \
  --pipeline-execution-id abc-123

# Get action execution details
aws codepipeline list-action-executions \
  --pipeline-name my-pipeline \
  --filter 'pipelineExecutionId=abc-123'
```

## Test Template

```python
def test_buildspec_syntax():
    # Arrange
    buildspec_path = "buildspec.yml"

    # Act
    with open(buildspec_path) as f:
        buildspec = yaml.safe_load(f)

    # Assert
    assert buildspec['version'] == 0.2
    assert 'phases' in buildspec
    assert 'build' in buildspec['phases']
```

## Assets

- `assets/buildspec.yml` - CodeBuild specification template

## References

- [CodePipeline User Guide](https://docs.aws.amazon.com/codepipeline/latest/userguide/)
- [CodeBuild User Guide](https://docs.aws.amazon.com/codebuild/latest/userguide/)
