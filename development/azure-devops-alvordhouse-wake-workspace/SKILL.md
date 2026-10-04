---
name: azure-devops
description: List Azure DevOps projects, repositories, and branches; create pull requests; manage work items; check build status. Use when working with Azure DevOps resources, checking PR status, querying project structure, or automating DevOps workflows.
metadata: {"openclaw": {"emoji": "☁️", "requires": {"bins": ["curl", "jq"], "env": ["AZURE_DEVOPS_PAT"]}, "primaryEnv": "AZURE_DEVOPS_PAT"}}
---

# Azure DevOps Skill

List projects, repositories, branches. Create pull requests. Manage work items. Check build status.

## Check before running for valid Configuration, if values missing ask the user!

**Required:**
- `AZURE_DEVOPS_PAT`: Personal Access Token
- `AZURE_DEVOPS_ORG`: Organization name

**If values are missing from `~/.openclaw/openclaw.json`, the agent should:**
1. **ASK** the user for the missing PAT and/or organization name
2. Store them in `~/.openclaw/openclaw.json` under `skills.entries["azure-devops"]`

### Example Config

```json5
{
  skills: {
    entries: {
      "azure-devops": {
        apiKey: "YOUR_PERSONAL_ACCESS_TOKEN",  // AZURE_DEVOPS_PAT
        env: {
          AZURE_DEVOPS_ORG: "YourOrganizationName"
        }
      }
    }
  }
}
```

## Commands

### List Projects

```bash
curl -s -u ":${AZURE_DEVOPS_PAT}" \
  "https://dev.azure.com/${AZURE_DEVOPS_ORG}/_apis/projects?api-version=7.1" \
  | jq -r '.value[] | "\(.name) - \(.description // "No description")"'
```

### List Repositories in a Project

```bash
PROJECT="YourProject"
curl -s -u ":${AZURE_DEVOPS_PAT}" \
  "https://dev.azure.com/${AZURE_DEVOPS_ORG}/${PROJECT}/_apis/git/repositories?api-version=7.1" \
  | jq -r '.value[] | "\(.name) - \(.webUrl)"'
```

### List Branches in a Repository

```bash
PROJECT="YourProject"
REPO="YourRepo"
curl -s -u ":${AZURE_DEVOPS_PAT}" \
  "https://dev.azure.com/${AZURE_DEVOPS_ORG}/${PROJECT}/_apis/git/repositories/${REPO}/refs?filter=heads/&api-version=7.1" \
  | jq -r '.value[] | .name | sub("refs/heads/"; "")'
```

### Create a Pull Request

```bash
PROJECT="YourProject"
REPO_ID="repo-id-here"
SOURCE_BRANCH="feature/my-branch"
TARGET_BRANCH="main"
TITLE="PR Title"
DESCRIPTION="PR Description"

curl -s -u ":${AZURE_DEVOPS_PAT}" \
  -H "Content-Type: application/json" \
  -X POST \
  -d '{
    "sourceRefName": "refs/heads/'"${SOURCE_BRANCH}"'",
    "targetRefName": "refs/heads/'"${TARGET_BRANCH}"'",
    "title": "'"${TITLE}"'",
    "description": "'"${DESCRIPTION}"'"
  }' \
  "https://dev.azure.com/${AZURE_DEVOPS_ORG}/${PROJECT}/_apis/git/repositories/${REPO_ID}/pullrequests?api-version=7.1"
```

### Get Repository ID

```bash
PROJECT="YourProject"
REPO_NAME="YourRepo"
curl -s -u ":${AZURE_DEVOPS_PAT}" \
  "https://dev.azure.com/${AZURE_DEVOPS_ORG}/${PROJECT}/_apis/git/repositories/${REPO_NAME}?api-version=7.1" \
  | jq -r '.id'
```

### List Pull Requests

```bash
PROJECT="YourProject"
REPO_ID="repo-id"
curl -s -u ":${AZURE_DEVOPS_PAT}" \
  "https://dev.azure.com/${AZURE_DEVOPS_ORG}/${PROJECT}/_apis/git/repositories/${REPO_ID}/pullrequests?api-version=7.1" \
  | jq -r '.value[] | "#\(.pullRequestId): \(.title) [\(.sourceRefName | sub("refs/heads/"; ""))] -> [\(.targetRefName | sub("refs/heads/"; ""))] - \(.createdBy.displayName)"'
```

## Notes

- Base URL: `https://dev.azure.com/${AZURE_DEVOPS_ORG}`
- API Version: `7.1`
- Auth: Basic Auth with empty username and PAT as password
- Never log or expose the PAT in responses
- Documentation: https://learn.microsoft.com/en-us/rest/api/azure/devops/
