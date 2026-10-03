---
name: azure-devops
description: Build and manage CI/CD pipelines with Azure DevOps. Configure builds, releases, and automate software delivery workflows.
triggers:
- /azure devops
- /ado pipelines
---

# Azure DevOps Pipelines

This skill covers building, configuring, and optimizing CI/CD pipelines using Azure DevOps Services for automated software delivery.

## When to use this skill

Use this skill when you need to:
- Create build pipelines for continuous integration
- Set up release pipelines for continuous deployment
- Implement multi-stage deployment workflows
- Configure automated testing in pipelines
- Set up infrastructure as code deployments
- Manage pipeline variables and secrets

## Prerequisites

- Azure DevOps organization and project
- Source code in Azure Repos or GitHub
- Service connections configured (Azure, Docker, etc.)
- Appropriate permissions (Build Admin or higher)

## Guidelines

### Pipeline Structure

**YAML Pipelines (Recommended)**
Store pipeline definitions in version control alongside code:

```yaml
# azure-pipelines.yml
trigger:
  branches:
    include:
      - main
      - develop

variables:
  buildConfiguration: 'Release'
  dotnetSdkVersion: '8.x'

stages:
- stage: Build
  jobs:
  - job: BuildAndTest
    pool:
      vmImage: 'ubuntu-latest'
    steps:
    - task: UseDotNet@2
      inputs:
        version: $(dotnetSdkVersion)
    
    - script: dotnet build --configuration $(buildConfiguration)
      displayName: 'Build solution'
    
    - task: DotNetCoreCLI@2
      inputs:
        command: 'test'
        projects: '**/*Tests.csproj'
      displayName: 'Run tests'

- stage: Deploy
  condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
  jobs:
  - deployment: DeployToProd
    environment: 'Production'
    strategy:
      runOnce:
        deploy:
          steps:
          - script: echo "Deploying to production..."
```

### Pipeline Organization

**Folder Structure**
```
azure-pipelines/
├── ci.yml              # Continuous integration
├── pr-validation.yml   # Pull request builds
├── deploy-dev.yml      # Development deployment
├── deploy-staging.yml  # Staging deployment
└── deploy-prod.yml     # Production deployment
```

**Template Reuse**
- Create reusable templates in `templates/` folder
- Share common steps across pipelines
- Parameterize environment-specific values

### Security and Secrets

**Variable Groups**
- Create environment-specific variable groups
- Mark sensitive variables as "secret"
- Link variable groups to pipelines

**Service Connections**
- Use service principals with minimal permissions
- Rotate credentials regularly
- Enable audit logging for connections

### Best Practices

**Pipeline Performance**
- Use caching for dependencies (npm, NuGet, pip)
- Run jobs in parallel where possible
- Use self-hosted agents for specialized requirements
- Implement build matrices for multi-platform testing

**Deployment Strategies**
- Blue-green deployments for zero downtime
- Canary releases for risk mitigation
- Feature flags for controlled rollouts
- Automated rollback on failure

**Testing Integration**
- Run unit tests on every build
- Integration tests on PR merges
- Performance tests in staging
- Security scanning with SonarQube/Trivy

## Examples

See the `examples/` directory for:
- `dotnet-webapp.yml` - ASP.NET Core CI/CD pipeline
- `nodejs-container.yml` - Node.js Docker build and push
- `infrastructure-deployment.yml` - Terraform deployment
- `multi-environment.yml` - Dev/Staging/Prod workflow

## References

- [Azure Pipelines documentation](https://docs.microsoft.com/azure/devops/pipelines/)
- [YAML schema reference](https://docs.microsoft.com/azure/devops/pipelines/yaml-schema/)
- [Pipeline templates](https://docs.microsoft.com/azure/devops/pipelines/process/templates)
- [Deployment strategies](https://docs.microsoft.com/azure/devops/pipelines/process/deployment-jobs)
