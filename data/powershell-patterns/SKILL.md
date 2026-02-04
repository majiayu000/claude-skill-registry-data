---
name: PowerShell Patterns
description: PowerShell best practices for Windows development, including cmdlet patterns, module development, and error handling
keywords:
  - powershell
  - windows
  - scripting
  - cmdlets
  - modules
---

# PowerShell Patterns

## When to Use

**Perfect for:**
- Windows system administration and automation
- CI/CD pipelines on Windows runners
- Build scripts and deployment automation
- Cross-platform .NET/PowerShell tooling
- Windows service management and monitoring

**Not ideal for:**
- Unix-only environments (use bash/sh instead)
- Simple one-off commands (use cmd.exe for basic operations)
- Performance-critical loops (consider compiled .NET instead)

## Quick Reference

### Cmdlet Naming & Creation
```powershell
# Standard verb-noun naming
# Get-Item, Set-Property, New-Item, Remove-Item, Test-Path, Invoke-Command

# Function with proper error handling
function Get-MyData {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,

        [Parameter()]
        [int]$Timeout = 30
    )

    process {
        try {
            Write-Verbose "Retrieving data from $Path"
            Get-Content -Path $Path -ErrorAction Stop
        }
        catch {
            Write-Error "Failed to get data: $_"
            throw
        }
    }
}
```

### Pipeline & Splatting
```powershell
# Pipeline-aware functions
function Process-Items {
    [CmdletBinding()]
    param(
        [Parameter(ValueFromPipeline = $true)]
        [object[]]$InputObject
    )

    process {
        $InputObject | ForEach-Object {
            # Process each item
            $_
        }
    }
}

# Splatting for complex commands
$params = @{
    Path            = "C:\data"
    Filter          = "*.txt"
    Recurse         = $true
    ErrorAction     = "Stop"
    WarningAction   = "SilentlyContinue"
}

Get-ChildItem @params
```

### Error Handling Pattern
```powershell
try {
    # Primary operation
    $result = Invoke-Command -ComputerName $Server -ScriptBlock { Get-Process }
}
catch [System.UnauthorizedAccessException] {
    Write-Error "Access denied to $Server"
    exit 1
}
catch [System.Net.NetworkInformation.PingException] {
    Write-Error "$Server is unreachable"
    exit 2
}
catch {
    Write-Error "Unexpected error: $_"
    exit 99
}
finally {
    Write-Verbose "Cleanup operations"
}
```

### Module Development
```powershell
# Module structure: MyModule/
# ├── MyModule.psd1 (manifest)
# ├── MyModule.psm1 (main module)
# └── Public/
#     └── Get-Data.ps1

# MyModule.psm1
$PublicFunctions = @(Get-ChildItem -Path "$PSScriptRoot/Public/*.ps1" -ErrorAction SilentlyContinue)

foreach ($Function in $PublicFunctions) {
    . $Function.FullName
}

Export-ModuleMember -Function @($PublicFunctions.Basename)
```

### Hashtables & PSCustomObject
```powershell
# Hashtable for structured data
$config = @{
    Server   = "localhost"
    Port     = 5432
    Database = "mydb"
    Timeout  = 30
}

# PSCustomObject for better null-coalescing and export
$result = [PSCustomObject]@{
    Name      = "Item"
    Count     = 42
    Status    = "Active"
    Timestamp = Get-Date
}

# Export to JSON/CSV
$result | Export-Csv -Path "output.csv" -NoTypeInformation
$result | ConvertTo-Json | Out-File "output.json"
```

### Script Signing
```powershell
# Create self-signed certificate for testing
$cert = New-SelfSignedCertificate -CertStoreLocation Cert:\CurrentUser\My -Subject "MyCodeSign"

# Sign script
Set-AuthenticodeSignature -FilePath "script.ps1" -Certificate $cert

# Verify signature
Get-AuthenticodeSignature -FilePath "script.ps1"

# Set execution policy (may need admin)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Deep Dive

### Advanced Pipeline Processing
```powershell
# Begin/Process/End pattern for efficiency
function Invoke-Batch {
    [CmdletBinding()]
    param(
        [Parameter(ValueFromPipeline = $true)]
        [object[]]$InputObject,

        [int]$BatchSize = 10
    )

    begin {
        $batch = @()
    }

    process {
        $batch += $_

        if ($batch.Count -ge $BatchSize) {
            # Process batch
            $batch | ForEach-Object { Write-Output $_ }
            $batch = @()
        }
    }

    end {
        # Process remaining items
        if ($batch.Count -gt 0) {
            $batch | ForEach-Object { Write-Output $_ }
        }
    }
}
```

### Parallel Processing
```powershell
# ForEach-Object -Parallel (PowerShell 7+)
$items = 1..100

$items | ForEach-Object -Parallel {
    Write-Output "Processing $_"
    Start-Sleep -Seconds 1
} -ThrottleLimit 4

# Using jobs for older PowerShell
$jobs = foreach ($item in $items) {
    Start-Job -ScriptBlock {
        param($i)
        "Processed $i"
    } -ArgumentList $item
}

$jobs | Wait-Job | Receive-Job
```

### Advanced Error Handling
```powershell
# Create custom exception
class CustomException : System.Exception {
    [int]$ErrorCode

    CustomException([string]$Message, [int]$Code) : base($Message) {
        $this.ErrorCode = $Code
    }
}

# Use custom error records
$errorRecord = New-Object System.Management.Automation.ErrorRecord(
    (New-Object CustomException("Something failed", 42)),
    "CustomError",
    [System.Management.Automation.ErrorCategory]::OperationStopped,
    $null
)

$PSCmdlet.WriteError($errorRecord)
```

### Configuration Management
```powershell
# Use JSON/YAML config with validation
$configPath = "config.json"
$config = Get-Content $configPath | ConvertFrom-Json

# Validate with schema
$schema = @{
    Server    = "string"
    Port      = "integer"
    Timeout   = "integer"
    Retries   = "integer"
}

foreach ($key in $schema.Keys) {
    if (-not $config.PSObject.Properties[$key]) {
        throw "Missing required config: $key"
    }
}
```

## Anti-Patterns

### DON'T: Use Write-Host for Output
```powershell
# Bad - output is hard to redirect/pipe
Write-Host "Result: $result"

# Good - use Write-Output or pipeline
Write-Output "Result: $result"
$result
```

### DON'T: Ignore $ErrorActionPreference
```powershell
# Bad - silently continues on error
Get-Item "missing.txt"

# Good - be explicit about error handling
Get-Item "missing.txt" -ErrorAction Stop
# Or handle explicitly:
if (Test-Path "missing.txt") {
    Get-Item "missing.txt"
}
```

### DON'T: Use String Concatenation for Commands
```powershell
# Bad - security risk and hard to maintain
$cmd = "Get-Process | Where-Object {$_.Name -like '$pattern'}"
Invoke-Expression $cmd

# Good - use parameters and splatting
Get-Process | Where-Object {$_.Name -like $pattern}
```

### DON'T: Ignore Pipeline Value Types
```powershell
# Bad - assumes string input
function Process {
    param([string]$Value)
    # Only works with strings
}

# Good - accept multiple types
function Process {
    param([object]$Value)
    # Works with any object
}
```

### DON'T: Mix Write-Verbose/Write-Error with Write-Host
```powershell
# Bad - inconsistent output handling
Write-Host "Info: $msg"
Write-Error "Error: $err"

# Good - consistent stream usage
Write-Verbose "Info: $msg"
Write-Error "Error: $err"
```

### DON'T: Hard-code Paths
```powershell
# Bad - breaks on different systems
$path = "C:\Users\Admin\AppData"

# Good - use environment variables
$path = $env:APPDATA
$path = "$env:ProgramFiles\MyApp"
$path = [System.IO.Path]::GetTempPath()
```
