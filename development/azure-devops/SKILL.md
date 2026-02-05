---
name: azure-devops
description: Guide for Azure DevOps automation using az CLI with azure-devops extension. Covers Azure Pipelines, Azure Repos, Azure Boards, work items, pull requests, artifacts, service connections, variable groups, and DevOps automation. Use when working with ADO, az devops commands, YAML pipelines, or Azure DevOps REST API.
---

# Azure DevOps CLI Guide

## Purpose

Comprehensive guide for automating Azure DevOps operations using the `az` CLI with the `azure-devops` extension. Covers common patterns, best practices, and examples for working with Azure Pipelines, Repos, Boards, and Artifacts.

## When to Use This Skill

Activates when you mention:
- Azure DevOps, ADO, or az devops
- Azure Pipelines, Azure Repos, Azure Boards
- Work items, pull requests, or code reviews in Azure DevOps
- DevOps automation, CI/CD pipelines
- az CLI commands for DevOps
- YAML pipeline definitions
- Service connections, variable groups, artifacts

---

## Prerequisites

### 1. Install Azure CLI
```bash
# Ubuntu/WSL
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Verify installation
az --version
```

### 2. Install Azure DevOps Extension
```bash
az extension add --name azure-devops
az extension update --name azure-devops  # Update to latest
```

### 3. Login to Azure
```bash
az login

# Or use Personal Access Token (PAT)
export AZURE_DEVOPS_EXT_PAT=<your-pat-token>
```

### 4. Set Default Organization and Project
```bash
# Set defaults to avoid repeating on every command
az devops configure --defaults organization=https://dev.azure.com/YourOrg project=YourProject

# View current defaults
az devops configure --list
```

---

## Authentication Methods

### Method 1: Interactive Login (Recommended for Development)
```bash
az login
# Opens browser for authentication
```

### Method 2: Personal Access Token (PAT)
```bash
# Set as environment variable
export AZURE_DEVOPS_EXT_PAT=<your-pat-token>

# Or use --org and --detect flags
az devops project list --org https://dev.azure.com/YourOrg
```

### Method 3: Service Principal (CI/CD)
```bash
az login --service-principal \
  --username <app-id> \
  --password <password-or-cert> \
  --tenant <tenant-id>
```

---

## Common Commands by Category

### Organization & Projects

```bash
# List organizations (requires authentication)
az devops project list --org https://dev.azure.com/YourOrg

# Show project details
az devops project show --project MyProject

# Create new project
az devops project create --name MyNewProject --visibility private

# List teams in project
az devops team list --project MyProject
```

### Azure Repos

```bash
# List repositories
az repos list --project MyProject

# Create repository
az repos create --name MyNewRepo --project MyProject

# Show repo details
az repos show --repository MyRepo --project MyProject

# Import repository
az repos import create \
  --git-source-url https://github.com/user/repo \
  --repository MyRepo

# List branches
az repos ref list --repository MyRepo

# Create branch
az repos ref create \
  --name refs/heads/feature/new-feature \
  --object-id <commit-sha> \
  --repository MyRepo

# Delete branch
az repos ref delete \
  --name refs/heads/old-branch \
  --object-id <commit-sha> \
  --repository MyRepo
```

### Pull Requests

```bash
# List pull requests
az repos pr list --repository MyRepo --status active

# Create pull request
az repos pr create \
  --repository MyRepo \
  --source-branch feature/my-feature \
  --target-branch main \
  --title "My Feature" \
  --description "Description here"

# Show PR details
az repos pr show --id 123

# Update PR
az repos pr update --id 123 --title "Updated Title"

# Add reviewers
az repos pr reviewer add --id 123 --reviewers user@domain.com

# Complete/merge PR
az repos pr set-vote --id 123 --vote approve
az repos pr update --id 123 --status completed

# Abandon PR
az repos pr update --id 123 --status abandoned

# List PR work items
az repos pr work-item list --id 123
```

### Azure Pipelines

```bash
# List pipelines
az pipelines list --project MyProject

# Show pipeline details
az pipelines show --name MyPipeline

# Create pipeline from YAML
az pipelines create \
  --name MyPipeline \
  --repository MyRepo \
  --branch main \
  --yml-path azure-pipelines.yml

# Run pipeline
az pipelines run --name MyPipeline

# Run with parameters
az pipelines run --name MyPipeline \
  --parameters param1=value1 param2=value2

# List pipeline runs
az pipelines runs list --pipeline-ids 123

# Show run details
az pipelines runs show --id 456

# List pipeline artifacts
az pipelines runs artifact list --run-id 456

# Download artifact
az pipelines runs artifact download \
  --run-id 456 \
  --artifact-name drop \
  --path ./artifacts
```

### Work Items

```bash
# List work items
az boards work-item query --wiql "SELECT [System.Id], [System.Title] FROM WorkItems WHERE [System.State] = 'Active'"

# Show work item
az boards work-item show --id 1234

# Create work item
az boards work-item create \
  --type "User Story" \
  --title "My User Story" \
  --description "Story description" \
  --assigned-to user@domain.com

# Update work item
az boards work-item update --id 1234 --state "In Progress"

# Add comment to work item
az boards work-item relation add \
  --id 1234 \
  --relation-type Comment \
  --target-id <comment-text>

# Link work items
az boards work-item relation add \
  --id 1234 \
  --relation-type Related \
  --target-id 5678
```

### Variable Groups

```bash
# List variable groups
az pipelines variable-group list

# Create variable group
az pipelines variable-group create \
  --name MyVariableGroup \
  --variables key1=value1 key2=value2

# Show variable group
az pipelines variable-group show --group-id 123

# Update variable
az pipelines variable-group variable create \
  --group-id 123 \
  --name newKey \
  --value newValue

# Delete variable
az pipelines variable-group variable delete \
  --group-id 123 \
  --name oldKey
```

### Service Connections

```bash
# List service connections
az devops service-endpoint list --project MyProject

# Create Azure RM service connection
az devops service-endpoint azurerm create \
  --name MyAzureConnection \
  --azure-rm-service-principal-id <sp-id> \
  --azure-rm-subscription-id <subscription-id> \
  --azure-rm-subscription-name "My Subscription" \
  --azure-rm-tenant-id <tenant-id>

# Show service connection
az devops service-endpoint show --id <connection-id>
```

---

## Common Patterns & Scripts

### Pattern 1: Auto-approve and Complete PR if CI Passes

```bash
#!/bin/bash
PR_ID=$1

# Wait for PR build to complete
while true; do
  STATUS=$(az repos pr show --id $PR_ID --query "mergeStatus" -o tsv)
  if [ "$STATUS" == "succeeded" ]; then
    echo "Build passed, approving PR..."
    az repos pr set-vote --id $PR_ID --vote approve
    az repos pr update --id $PR_ID --status completed --delete-source-branch true
    break
  elif [ "$STATUS" == "failed" ]; then
    echo "Build failed, not approving PR"
    break
  fi
  sleep 30
done
```

### Pattern 2: Bulk Create Work Items from File

```bash
#!/bin/bash
# work-items.txt format: Type|Title|Description

while IFS='|' read -r type title description; do
  az boards work-item create \
    --type "$type" \
    --title "$title" \
    --description "$description"
done < work-items.txt
```

### Pattern 3: Clone All Repos in a Project

```bash
#!/bin/bash
ORG="https://dev.azure.com/YourOrg"
PROJECT="YourProject"

az repos list --project $PROJECT --query "[].name" -o tsv | while read repo; do
  echo "Cloning $repo..."
  git clone "$ORG/$PROJECT/_git/$repo"
done
```

### Pattern 4: Run Pipeline and Wait for Completion

```bash
#!/bin/bash
PIPELINE_NAME="MyPipeline"

# Start pipeline run
RUN_ID=$(az pipelines run --name $PIPELINE_NAME --query "id" -o tsv)
echo "Started run $RUN_ID"

# Poll for completion
while true; do
  STATUS=$(az pipelines runs show --id $RUN_ID --query "status" -o tsv)
  RESULT=$(az pipelines runs show --id $RUN_ID --query "result" -o tsv)

  if [ "$STATUS" == "completed" ]; then
    echo "Run completed with result: $RESULT"
    [ "$RESULT" == "succeeded" ] && exit 0 || exit 1
  fi

  sleep 10
done
```

---

## Best Practices

### 1. Use Configuration Defaults
Set defaults to avoid repeating org/project on every command:
```bash
az devops configure --defaults \
  organization=https://dev.azure.com/YourOrg \
  project=YourProject
```

### 2. Use Output Formats Effectively
```bash
# Table format (human-readable)
az repos list -o table

# JSON for scripting
az repos list -o json

# TSV for parsing
az repos list --query "[].name" -o tsv
```

### 3. Use JMESPath Queries
```bash
# Get specific fields
az repos list --query "[].{Name:name, Id:id}" -o table

# Filter results
az repos pr list --query "[?status=='active'].id" -o tsv
```

### 4. Store PAT Securely
```bash
# Never hardcode PAT in scripts
# Use environment variables or Azure Key Vault
export AZURE_DEVOPS_EXT_PAT=$(az keyvault secret show --name ado-pat --vault-name myvault --query value -o tsv)
```

### 5. Error Handling in Scripts
```bash
set -e  # Exit on error
set -o pipefail  # Exit on pipe failure

if ! az repos show --repository MyRepo 2>/dev/null; then
  echo "Repository does not exist"
  exit 1
fi
```

### 6. Use Service Principals for CI/CD
Never use personal accounts for automated pipelines - use service principals with minimal required permissions.

---

## Integration with .NET Projects

### Trigger Pipeline After dotnet build
```bash
# Build .NET project
dotnet build MyProject.csproj

# If build succeeds, trigger Azure Pipeline
if [ $? -eq 0 ]; then
  az pipelines run --name DeployPipeline
fi
```

### Create Work Items for Build Failures
```bash
# In Azure Pipeline YAML
- script: |
    if [ $(Agent.JobStatus) == "Failed" ]; then
      az boards work-item create \
        --type Bug \
        --title "Build $(Build.BuildNumber) failed" \
        --description "Build failed: $(Build.BuildUri)"
    fi
  condition: failed()
  displayName: 'Create work item on failure'
```

---

## Useful Query Examples

### Find Active PRs Older Than 7 Days
```bash
DATE_7_DAYS_AGO=$(date -d '7 days ago' +%Y-%m-%d)

az repos pr list --status active --query \
  "[?creationDate<'$DATE_7_DAYS_AGO'].{ID:pullRequestId, Title:title, Created:creationDate}" \
  -o table
```

### List Failed Pipeline Runs in Last 24 Hours
```bash
az pipelines runs list \
  --query "[?finishTime>='$(date -d '1 day ago' --iso-8601=seconds)' && result=='failed'].{ID:id, Pipeline:definition.name, Result:result}" \
  -o table
```

### Get All Work Items Assigned to Me
```bash
MY_EMAIL="user@domain.com"

az boards work-item query --wiql \
  "SELECT [System.Id], [System.Title], [System.State] FROM WorkItems WHERE [System.AssignedTo] = '$MY_EMAIL' AND [System.State] <> 'Closed'"
```

---

## Troubleshooting

### Issue: "TF400813: Resource not available for anonymous access"
**Solution:** Ensure you're authenticated:
```bash
az login
# Or set PAT
export AZURE_DEVOPS_EXT_PAT=<your-token>
```

### Issue: "The term 'az' is not recognized"
**Solution:** Install Azure CLI and add to PATH

### Issue: Extension not found
**Solution:** Install azure-devops extension:
```bash
az extension add --name azure-devops
```

### Issue: Permission denied errors
**Solution:** Check PAT scopes - ensure it has required permissions:
- Code (Read, Write, Manage)
- Build (Read, Execute)
- Work Items (Read, Write)

---

## Quick Reference

```bash
# Setup
az extension add --name azure-devops
az login
az devops configure --defaults organization=<org> project=<project>

# Repos
az repos list
az repos pr list --status active

# Pipelines
az pipelines list
az pipelines run --name <pipeline>

# Work Items
az boards work-item show --id <id>

# Output formats
-o json    # JSON output
-o table   # Table format
-o tsv     # Tab-separated values
--query    # JMESPath query
```

---

**Related Documentation:**
- [Azure CLI DevOps Extension Docs](https://learn.microsoft.com/en-us/cli/azure/devops)
- [Azure DevOps REST API](https://learn.microsoft.com/en-us/rest/api/azure/devops)
- [JMESPath Query Reference](https://jmespath.org/)

**Skill Type:** Domain
**Enforcement:** Suggest
**Line Count:** ~450 lines ✅
