---
name: windows-powershell
description: Windows PowerShell command patterns for terminal operations. Use when running commands, scripts, or terminal operations on Windows. Keywords - PowerShell, Windows, terminal, commands, scripts, never use &&.
compatibility: Windows PowerShell 5.1 and PowerShell 7+
metadata:
  version: "2.0.0"
  author: jpmorgan-payments
  lastUpdated: "2025-12-24"
  priority: high
---

# Windows PowerShell Commands

## ⚠️ CRITICAL: NEVER Use && in PowerShell

PowerShell does NOT support `&&` for command chaining. Use semicolons `;` instead.

```powershell
# ❌ WRONG - Will fail
cd embedded-components && yarn test

# ✅ CORRECT - Use semicolon
cd embedded-components; yarn test

# ✅ ALSO CORRECT - Separate commands
cd embedded-components
yarn test
```

## Command Chaining

### Semicolon (;) - Execute Regardless

Runs the second command even if the first fails:

```powershell
cd embedded-components; yarn test
```

### Pipeline (|) - Pass Output

Passes output from one command to another:

```powershell
Get-ChildItem | Where-Object { $_.Extension -eq ".tsx" }
```

### Logical AND (-and) - Conditional Execution

PowerShell equivalent of `&&`:

```powershell
if (Test-Path embedded-components) { cd embedded-components; yarn test }
```

## Common Development Commands

### Navigation

```powershell
# Change directory
cd embedded-components

# Go to parent
cd ..

# Go to root
cd \

# List contents
Get-ChildItem
# or shorthand
ls
dir
```

### File Operations

```powershell
# Create file
New-Item -Path "file.txt" -ItemType File

# Create directory
New-Item -Path "folder" -ItemType Directory

# Remove file
Remove-Item -Path "file.txt"

# Remove directory recursively
Remove-Item -Path "folder" -Recurse -Force

# Copy file
Copy-Item -Path "source.txt" -Destination "dest.txt"

# Move file
Move-Item -Path "source.txt" -Destination "dest.txt"
```

### Package Management

```powershell
# Install dependencies
cd embedded-components; yarn install

# Run tests
cd embedded-components; yarn test

# Run specific script
cd embedded-components; yarn format

# Multiple commands
cd embedded-components; yarn format; yarn lint:fix; yarn test
```

### Git Operations

```powershell
# Status
git status

# Add files
git add .

# Commit
git commit -m "feat: add new component"

# Push
git push

# Pull
git pull

# Create branch
git checkout -b feature/new-feature

# Multiple git commands
git add .; git commit -m "fix: update tests"; git push
```

### Process Management

```powershell
# Find process by port
netstat -ano | findstr :3000

# Kill process by PID
taskkill /PID 1234 /F

# Stop all node processes
Get-Process node | Stop-Process -Force
```

### Environment Variables

```powershell
# Set environment variable (current session)
$env:NODE_ENV = "development"
$env:NODE_OPTIONS = "--max-old-space-size=4096"

# Use environment variable
Write-Output $env:NODE_ENV

# Set for command execution
$env:NODE_ENV="test"; yarn test
```

### Path Operations

```powershell
# Get current directory
$PWD
Get-Location

# Check if path exists
Test-Path "embedded-components"

# Get absolute path
Resolve-Path "embedded-components"

# Join paths
Join-Path "embedded-components" "src"
```

### File Search

```powershell
# Find files by name
Get-ChildItem -Recurse -Filter "*.tsx"

# Find files with content
Select-String -Path "*.tsx" -Pattern "useEffect"

# Find and count
(Get-ChildItem -Recurse -Filter "*.test.tsx").Count
```

### Text Processing

```powershell
# Read file
Get-Content "file.txt"

# Write file
"content" | Out-File "file.txt"

# Append to file
"content" | Add-Content "file.txt"

# Search and replace
(Get-Content "file.txt") -replace "old", "new" | Set-Content "file.txt"
```

## Development Workflow Commands

### Complete Test Workflow

```powershell
# Navigate and run tests
cd embedded-components; yarn test

# Fix formatting and linting
cd embedded-components; yarn format; yarn lint:fix

# Re-run tests
cd embedded-components; yarn test

# If all pass, commit
git add .; git commit -m "fix: update component"; git push
```

### Build and Deploy

```powershell
# Clean, install, build
cd embedded-components; Remove-Item -Recurse -Force node_modules; yarn install; yarn build

# Run Storybook
cd embedded-components; yarn storybook
```

### Cache Management

```powershell
# Clear yarn cache
cd embedded-components; yarn cache clean

# Remove node_modules and reinstall
cd embedded-components; Remove-Item -Recurse -Force node_modules; yarn install

# Clear all caches
cd embedded-components; yarn cache clean; Remove-Item -Recurse -Force node_modules, .cache; yarn install
```

## PowerShell-Specific Features

### Aliases

```powershell
# Common aliases
ls    # Get-ChildItem
dir   # Get-ChildItem
cd    # Set-Location
pwd   # Get-Location
cat   # Get-Content
rm    # Remove-Item
cp    # Copy-Item
mv    # Move-Item
```

### Execution Policy

```powershell
# Check current policy
Get-ExecutionPolicy

# Set execution policy (admin required)
Set-ExecutionPolicy RemoteSigned
```

### Profile

```powershell
# Edit PowerShell profile
notepad $PROFILE

# Reload profile
. $PROFILE
```

## Error Handling

```powershell
# Try-catch block
try {
    cd embedded-components
    yarn test
} catch {
    Write-Error "Command failed: $_"
}

# Check if command succeeded
if ($LASTEXITCODE -eq 0) {
    Write-Output "Success"
} else {
    Write-Output "Failed with code $LASTEXITCODE"
}
```

## Variables and Strings

```powershell
# Variables
$projectPath = "embedded-components"
$command = "yarn test"

# String interpolation
cd $projectPath; Invoke-Expression $command

# Here-strings for multi-line
$script = @"
cd embedded-components
yarn format
yarn lint:fix
yarn test
"@
Invoke-Expression $script
```

## Common Patterns

### Conditional Navigation and Execution

```powershell
if (Test-Path "embedded-components") {
    cd embedded-components
    yarn test
} else {
    Write-Error "Directory not found"
}
```

### Loop Through Files

```powershell
Get-ChildItem -Recurse -Filter "*.test.tsx" | ForEach-Object {
    Write-Output "Testing: $($_.Name)"
    yarn test $_.Name
}
```

### Backup and Restore

```powershell
# Backup
Copy-Item -Path "embedded-components" -Destination "embedded-components-backup" -Recurse

# Restore
Remove-Item -Path "embedded-components" -Recurse -Force
Move-Item -Path "embedded-components-backup" -Destination "embedded-components"
```

## Best Practices

1. **Use semicolons (;)** - Never use `&&`
2. **Quote paths with spaces** - Use quotes for paths containing spaces
3. **Use cmdlet names** - Prefer `Get-ChildItem` over `ls` in scripts
4. **Check exit codes** - Use `$LASTEXITCODE` to verify command success
5. **Use try-catch** - For error-prone operations
6. **Test paths** - Use `Test-Path` before operations
7. **Be explicit** - Use full cmdlet names in important scripts

## Common Mistakes

❌ Using `&&` for command chaining  
❌ Not quoting paths with spaces  
❌ Forgetting to check `$LASTEXITCODE`  
❌ Not handling errors  
❌ Using forward slashes in paths (use backslashes or forward slashes, but be consistent)  

## Quick Reference

```powershell
# Navigate to project
cd i:\ds\projects\oss\embedded-banking\embedded-components

# Run quality workflow
yarn test

# Fix issues
yarn format; yarn lint:fix

# Re-test
yarn test

# Commit changes
cd ..; git add .; git commit -m "feat: new component"; git push
```

## References

- See `.github/copilot/prompts/` for related prompts
- See `.github/copilot/skills/code-quality-workflow/` for testing workflow
- Microsoft PowerShell documentation: https://docs.microsoft.com/powershell/
