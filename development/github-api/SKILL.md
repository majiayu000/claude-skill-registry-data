---
name: github-api
description: How to interact with GitHub API. Use this skill for repos, PRs, issues, and user operations.
---

# GitHub API Skill

## Authentication
```powershell
# REST API
$headers = @{ "Authorization" = "token YOUR_TOKEN"; "Accept" = "application/vnd.github.v3+json" }

# GraphQL API
$headers = @{ "Authorization" = "bearer YOUR_TOKEN"; "Content-Type" = "application/json" }
```

## REST API Operations

### Get User Info
```powershell
Invoke-RestMethod -Uri "https://api.github.com/user" -Headers $headers
```

### Create/Update File
```powershell
$contentBase64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($content))
$body = @{ message = "commit msg"; content = $contentBase64; sha = $existingSha } | ConvertTo-Json
Invoke-RestMethod -Uri "https://api.github.com/repos/OWNER/REPO/contents/PATH" -Method PUT -Headers $headers -Body $body
```

### Create PR
```powershell
$body = @{ title = "PR title"; body = "desc"; head = "branch"; base = "main" } | ConvertTo-Json
Invoke-RestMethod -Uri "https://api.github.com/repos/OWNER/REPO/pulls" -Method POST -Headers $headers -Body $body
```

## GraphQL API Operations

### Update User Status (NOT available in REST API!)
```powershell
$query = @{ query = 'mutation { changeUserStatus(input: {emoji: ":sparkles:", message: "Your status"}) { status { emoji message } } }' } | ConvertTo-Json
Invoke-RestMethod -Uri "https://api.github.com/graphql" -Method POST -Headers $headers -Body $query
```

## Important Notes
- User status uses GraphQL, not REST (REST returns 404)
- README.md might be in .github/ folder
- GitHub releases use redirects, curl needs -L flag