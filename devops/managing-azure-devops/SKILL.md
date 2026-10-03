---
name: managing-azure-devops
description: Author Azure DevOps YAML pipelines — multi-stage deploys, templates, variable groups, environment approvals.
when_to_use: Reach for this when building or editing CI/CD on Azure DevOps (azure-pipelines.yml). For running GitHub Actions locally use act-local-ci; for tracking Azure DevOps *work items/boards* this skill is pipelines-only — use managing-jira-issues or managing-linear-issues for general issue tracking. Provisioning Azure infra is using-terraform-azure.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
paths:
  - "azure-pipelines*.yml"
  - ".azure/**"
  - "**/*.yml"
---

# Azure DevOps Pipelines Skill

Fast reference for Azure DevOps YAML pipelines. See [REFERENCE.md](REFERENCE.md) for template libraries, service connections, container jobs, caching, and advanced patterns.

---

## When to Use

**Auto-Detection**: `azure-pipelines.yml` in project root, `.azuredevops/` directory, user mentions Azure DevOps.

---

## CRITICAL: Azure DevOps vs GitHub Actions

**Models frequently confuse these two systems.** They have different syntax.

| Concept | Azure DevOps | GitHub Actions (WRONG) |
|---------|-------------|------------------------|
| **Built-in step** | `task: TaskName@Version` | `uses: action/name@v1` |
| **Script step** | `script:` or `bash:` | `run:` |
| **Trigger (push)** | `trigger:` | `on:` |
| **Trigger (PR)** | `pr:` | `on: pull_request` |
| **Variable (runtime)** | `$(variableName)` | `${{ env.VAR }}` |
| **Variable (compile-time)** | `${{ parameters.x }}` | `${{ inputs.x }}` |
| **Variable (condition)** | `$[variables.x]` | N/A |
| **Artifacts upload** | `PublishBuildArtifacts@1` | `actions/upload-artifact` |
| **Environment deploy** | `deployment:` job + `environment:` | `environment:` on job |

### Variable Expression Syntax (THREE distinct syntaxes)

| Syntax | Evaluated At | Use Case | Example |
|--------|-------------|----------|---------|
| `${{ }}` | **Compile time** | Template parameters, structural decisions | `${{ parameters.env }}` |
| `$( )` | **Runtime** | Variables, secrets, predefined variables | `$(Build.SourceBranch)` |
| `$[ ]` | **Runtime conditions** | Conditional expressions in YAML | `$[eq(variables['Build.Reason'], 'PullRequest')]` |

---

## Multi-Stage Pipeline Structure

Pipelines use a **stages > jobs > steps** hierarchy:

```yaml
trigger:
  branches:
    include: [main, release/*]
  paths:
    exclude: [docs/**, '*.md']

pr:
  branches:
    include: [main]

pool:
  vmImage: 'ubuntu-latest'

variables:
  - group: 'my-variable-group'
  - name: buildConfiguration
    value: 'Release'

stages:
  - stage: Build
    jobs:
      - job: BuildJob
        steps:
          - task: DotNetCoreCLI@2
            inputs:
              command: 'build'
              projects: '**/*.csproj'
              arguments: '--configuration $(buildConfiguration)'
          - task: PublishBuildArtifacts@1
            inputs:
              PathtoPublish: '$(Build.ArtifactStagingDirectory)'
              ArtifactName: 'drop'

  - stage: DeployStaging
    dependsOn: Build
    jobs:
      - deployment: DeployStaging
        environment: 'staging'
        strategy:
          runOnce:
            deploy:
              steps:
                - script: echo 'Deploying to staging...'

  - stage: DeployProduction
    dependsOn: DeployStaging
    jobs:
      - deployment: DeployProduction
        environment: 'production'
        strategy:
          runOnce:
            deploy:
              steps:
                - script: echo 'Deploying to production...'
```

---

## Deployment Jobs

### CRITICAL: Use `deployment` Not `job` for Environments

Deployment jobs REQUIRE a `strategy:` block. Regular `job:` does NOT support `environment:`.

```yaml
# WRONG
- job: Deploy
    environment: 'production'    # Will NOT work

# CORRECT
- deployment: Deploy
    environment: 'production'
    strategy:                    # REQUIRED
      runOnce:
        deploy:
          steps:
            - script: echo deploy
```

### Deployment Strategies

**runOnce** (most common): Single deployment with optional lifecycle hooks.
```yaml
strategy:
  runOnce:
    preDeploy:
      steps: [...]
    deploy:
      steps: [...]
    on:
      failure:
        steps: [...]
```

**rolling**: Incremental deployment across targets.
```yaml
strategy:
  rolling:
    maxParallel: 2
    deploy:
      steps: [...]
```

**canary**: Percentage-based rollout.
```yaml
strategy:
  canary:
    increments: [10, 20]
    deploy:
      steps: [...]
```

---

## Template References

Templates enable reusable pipeline components (step, job, stage, and variable templates).

### Step Template

**File: `templates/build-steps.yml`**
```yaml
parameters:
  - name: dotnetVersion
    type: string
    default: '8.x'

steps:
  - task: UseDotNet@2
    inputs:
      version: '${{ parameters.dotnetVersion }}'
  - task: DotNetCoreCLI@2
    inputs:
      command: 'build'
```

**Usage:** `- template: templates/build-steps.yml`

### Stage Template

**File: `templates/deploy-stage.yml`**
```yaml
parameters:
  - name: environment
    type: string
  - name: serviceConnection
    type: string
  - name: appName
    type: string

stages:
  - stage: Deploy_${{ parameters.environment }}
    jobs:
      - deployment: Deploy
        environment: '${{ parameters.environment }}'
        strategy:
          runOnce:
            deploy:
              steps:
                - task: AzureWebApp@1
                  inputs:
                    azureSubscription: '${{ parameters.serviceConnection }}'
                    appName: '${{ parameters.appName }}'
```

**Usage:**
```yaml
- template: templates/deploy-stage.yml
  parameters:
    environment: 'production'
    serviceConnection: 'Azure-Prod'
    appName: 'myapp-prod'
```

### Extends Template (Governance)

Forces all pipelines through a required base template:

```yaml
# Pipeline file
extends:
  template: templates/pipeline-base.yml
  parameters:
    stages:
      - stage: Build
        jobs:
          - job: Build
            steps:
              - script: echo 'Building...'
```

### Compile-Time vs Runtime in Templates

```yaml
# ${{ }} - Compile time: structural decisions, template parameters
- ${{ if eq(parameters.includeTests, true) }}:
  - task: DotNetCoreCLI@2
    inputs:
      command: 'test'

# $() - Runtime: pipeline variables, secrets
- script: echo $(Build.BuildId)
```

See [REFERENCE.md](REFERENCE.md#template-library-patterns) for complete template library patterns.

---

## Variable Groups and Key Vault

```yaml
variables:
  - group: 'my-app-variables'       # Variable group from UI
  - group: 'keyvault-secrets'       # Linked to Azure Key Vault
  - name: localVar
    value: 'inline-value'
```

### AzureKeyVault Task (Inline Fetch)

```yaml
- task: AzureKeyVault@2
  inputs:
    azureSubscription: 'my-service-connection'
    KeyVaultName: 'my-keyvault'
    SecretsFilter: 'db-password,api-key'
    RunAsPreJob: false

- script: echo "Secret length: ${#DB_PASSWORD}"
  env:
    DB_PASSWORD: $(db-password)
```

---

## Environment Approvals

### CRITICAL: Approvals Are Configured in the UI, NOT in YAML

The YAML just references the environment name. Approval gates are set on the **Environment** in Project Settings.

```yaml
# YAML: just references the environment
- deployment: DeployProd
    environment: 'production'    # Approvals configured on this environment in UI
```

**Where to configure** (all in Azure DevOps UI):
1. **Pipelines > Environments** > select environment > **Approvals and checks**
2. Add: Approvals, Branch control, Business hours, Exclusive lock, Template validation

---

## .NET Build and Test Tasks

```yaml
# Install SDK
- task: UseDotNet@2
  inputs:
    packageType: 'sdk'
    version: '8.x'

# Restore
- task: DotNetCoreCLI@2
  inputs:
    command: 'restore'
    projects: '**/*.csproj'

# Build
- task: DotNetCoreCLI@2
  inputs:
    command: 'build'
    arguments: '--configuration $(buildConfiguration) --no-restore'

# Test with coverage
- task: DotNetCoreCLI@2
  inputs:
    command: 'test'
    projects: '**/*Tests.csproj'
    arguments: '--no-build --collect:"XPlat Code Coverage" --logger trx'

# Publish
- task: DotNetCoreCLI@2
  inputs:
    command: 'publish'
    publishWebProjects: true
    arguments: '--output $(Build.ArtifactStagingDirectory)'
    zipAfterPublish: true
```

---

## Artifact Publishing

```yaml
# Pipeline Artifacts (preferred)
- task: PublishPipelineArtifact@1
  inputs:
    targetPath: '$(Build.ArtifactStagingDirectory)'
    artifact: 'drop'

- task: DownloadPipelineArtifact@2
  inputs:
    artifactName: 'drop'
    targetPath: '$(Pipeline.Workspace)/drop'

# Build Artifacts (legacy)
- task: PublishBuildArtifacts@1
  inputs:
    PathtoPublish: '$(Build.ArtifactStagingDirectory)'
    ArtifactName: 'drop'

- task: DownloadBuildArtifacts@1
  inputs:
    buildType: 'current'
    artifactName: 'drop'
```

---

## Common Patterns

### Conditions

```yaml
# Stage: deploy only from main
condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))

# Step: run only on PRs
condition: eq(variables['Build.Reason'], 'PullRequest')

# Step: run only on manual trigger
condition: eq(variables['Build.Reason'], 'Manual')
```

### Scheduled and Manual Triggers

```yaml
trigger: none    # Disable CI trigger

schedules:
  - cron: '0 2 * * *'
    displayName: 'Nightly build'
    branches:
      include: [main]
    always: true

parameters:
  - name: environment
    type: string
    default: 'staging'
    values: [staging, production]
```

### Predefined Variables

| Variable | Description |
|----------|-------------|
| `$(Build.BuildId)` | Unique build ID |
| `$(Build.SourceBranch)` | Full branch ref (`refs/heads/main`) |
| `$(Build.SourceBranchName)` | Short branch name (`main`) |
| `$(Build.SourceVersion)` | Commit SHA |
| `$(Build.Reason)` | `IndividualCI`, `PullRequest`, `Manual`, `Schedule` |
| `$(Build.ArtifactStagingDirectory)` | Staging directory for artifacts |
| `$(Pipeline.Workspace)` | Workspace root |

---

## Quick Reference Card

```yaml
# --- Triggers ---
trigger:
  branches:
    include: [main]
pr:
  branches:
    include: [main]

# --- Variables ---
variables:
  - group: 'my-variable-group'
  - name: myVar
    value: 'my-value'

# --- Build Stage ---
stages:
  - stage: Build
    jobs:
      - job: Build
        pool:
          vmImage: 'ubuntu-latest'
        steps:
          - task: UseDotNet@2           # task: not uses:
            inputs:
              version: '8.x'
          - script: dotnet build        # script: not run:

# --- Deploy Stage ---
  - stage: Deploy
    jobs:
      - deployment: Deploy              # NOT job:
        environment: 'production'       # Approvals in UI
        strategy:                       # REQUIRED
          runOnce:
            deploy:
              steps:
                - script: echo deploy

# --- Templates ---
  - template: templates/steps.yml
    parameters:
      env: 'production'

# --- Key Vault ---
  - task: AzureKeyVault@2
    inputs:
      azureSubscription: 'my-conn'
      KeyVaultName: 'my-vault'
      SecretsFilter: 'secret1,secret2'

# --- Variable Syntax ---
# ${{ parameters.x }}  --> compile-time (templates)
# $(variableName)      --> runtime (variables, secrets)
# $[variables.x]       --> runtime conditions
```

---

**See [REFERENCE.md](REFERENCE.md) for**: Template library patterns, service connections and managed identity, container jobs and self-hosted agents, pipeline caching, release pipelines vs YAML pipelines, Azure CLI and script tasks, and advanced patterns.
