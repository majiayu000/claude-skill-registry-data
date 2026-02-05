---
name: file-editor
description: Edit files locally using built-in tools instead of PowerShell string replacement. 5000% efficiency boost!
---

# File Editor Skill

## Workflow

1. **Preview local files** using built-in tools
2. **Download files** from forked repo to `.ciallo/temp/`
3. **Edit files** using built-in file editor (fsWrite, strReplace, etc.)
4. **Upload & commit** using PowerShell git commands
5. **Review diff** before creating PR

## Usage

### Step 1: Preview file
Use `readFile` tool to preview the file content

### Step 2: Download to temp
```powershell
# Create temp directory
New-Item -ItemType Directory -Path ".ciallo/temp" -Force

# Download file from GitHub
$headers = @{ "Authorization" = "token YOUR_TOKEN" }
$file = Invoke-RestMethod -Uri "https://api.github.com/repos/OWNER/REPO/contents/PATH" -Headers $headers
$content = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($file.content))
$content | Out-File -FilePath ".ciallo/temp/filename.ext" -Encoding UTF8
```

### Step 3: Edit locally
Use built-in tools: `fsWrite`, `strReplace`, `readFile`

### Step 4: Upload & commit
```powershell
$content = Get-Content ".ciallo/temp/filename.ext" -Raw
$contentBase64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($content))
$body = @{ message = "commit msg"; content = $contentBase64; sha = $existingSha } | ConvertTo-Json
Invoke-RestMethod -Uri "https://api.github.com/repos/OWNER/REPO/contents/PATH" -Method PUT -Headers $headers -Body $body
```

### Step 5: Review diff
Check the commit diff on GitHub before creating PR

## Notes
- Purchased: 2025-12-18 (5 Ciallo coins)
- Much more efficient than PowerShell string replacement!