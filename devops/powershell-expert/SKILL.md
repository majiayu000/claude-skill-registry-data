---
name: powershell-expert
description: Deep PowerShell expertise for automation and systems administration. Use when writing PowerShell scripts, building modules, managing Windows/Azure.
---

# PowerShell Expert

Specialized expertise in PowerShell scripting and automation, providing deep guidance on modern patterns, error handling, module development, pipeline design, remote management, .NET interop, and testing with Pester. Covers both Windows PowerShell 5.1 and PowerShell 7+ (cross-platform).

## When to Use This Skill

Use this skill for:

- Writing production-grade PowerShell scripts and modules
- Automating Windows and Azure infrastructure
- Building CI/CD pipelines with PowerShell
- Implementing advanced functions with proper parameter validation
- Managing remote systems with PSRemoting and SSH
- Integrating PowerShell with .NET libraries and classes
- Writing and running Pester tests

**Trigger phrases**: "powershell", "pwsh", "ps1", "cmdlet", "PSRemoting", "Pester", "PowerShell module", "PowerShell automation"

## What This Skill Does

Provides PowerShell expertise including:

- **Modern Patterns**: Splatting, pipeline design, CmdletBinding, parameter validation, ShouldProcess
- **Error Handling**: ErrorActionPreference, terminating vs non-terminating errors, error records
- **Module Development**: Manifests, exports, PSScriptAnalyzer, publishing to PSGallery
- **Pipeline and Data**: Custom objects, filtering, grouping, JSON/CSV conversion
- **Remote Management**: PSRemoting, Invoke-Command, SSH remoting, parallel execution
- **.NET Interop**: Using .NET types, Add-Type, PowerShell classes, calling C# from PS
- **Testing**: Pester 5 with Describe/Context/It, mocking, TestDrive, code coverage

## Instructions

### Step 1: Master Modern PowerShell Patterns

**Splatting for Clean Parameter Passing**:

```powershell
# Without splatting (hard to read)
Get-ChildItem -Path "C:\Logs" -Filter "*.log" -Recurse -Force -ErrorAction SilentlyContinue

# With splatting (clean and composable)
$params = @{
    Path        = "C:\Logs"
    Filter      = "*.log"
    Recurse     = $true
    Force       = $true
    ErrorAction = "SilentlyContinue"
}
Get-ChildItem @params

# Conditional splatting: add parameters only when needed
$params = @{ Path = $SourcePath; Filter = "*.csv" }
if ($Recurse) { $params["Recurse"] = $true }
if ($Since)   { $params["After"] = $Since }
Get-ChildItem @params
```

**Advanced Functions with CmdletBinding and ShouldProcess**:

Always use `[CmdletBinding()]` on functions intended for production use. It enables common parameters (`-Verbose`, `-Debug`, `-ErrorAction`) and unlocks `ShouldProcess` support for destructive operations.

```powershell
function Remove-StaleLogFiles {
    [CmdletBinding(SupportsShouldProcess, ConfirmImpact = "High")]
    param(
        [Parameter(Mandatory, ValueFromPipeline)]
        [ValidateNotNullOrEmpty()]
        [string[]]$Path,

        [ValidateRange(1, 365)]
        [int]$DaysOld = 30,

        [ValidateSet("Delete", "Archive", "Compress")]
        [string]$Action = "Delete"
    )

    begin { $cutoff = (Get-Date).AddDays(-$DaysOld); $count = 0 }

    process {
        foreach ($p in $Path) {
            Get-ChildItem -Path $p -File |
                Where-Object { $_.LastWriteTime -lt $cutoff } |
                ForEach-Object {
                    if ($PSCmdlet.ShouldProcess($_.FullName, $Action)) {
                        Remove-Item -Path $_.FullName -Force
                        $count++
                    }
                }
        }
    }

    end { Write-Verbose "Processed $count files" }
}

# Usage: -WhatIf previews without deleting; -Confirm prompts per file
Remove-StaleLogFiles -Path "C:\Logs" -DaysOld 90 -WhatIf
```

**Parameter Validation Attributes**:

```powershell
function Deploy-Application {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [ValidatePattern("^[a-zA-Z][\w\-]{2,49}$")]
        [string]$AppName,

        [ValidateScript({
            if (-not (Test-Path $_ -PathType Container)) { throw "Directory '$_' not found" }
            $true
        })]
        [string]$SourcePath,

        [ValidateSet("Development", "Staging", "Production")]
        [string]$Environment = "Development",

        [ValidateRange(1, 65535)]
        [int]$Port = 8080
    )
    Write-Verbose "Deploying $AppName to $Environment on port $Port"
}
```

**Cross-Platform Considerations (5.1 vs 7+)**:

```powershell
# Detect version and platform
if ($PSVersionTable.PSEdition -eq "Core") {
    Write-Output "PowerShell 7+ on $($PSVersionTable.OS)"
} else {
    Write-Output "Windows PowerShell 5.1"
}

# Cross-platform path handling (avoid hardcoded backslashes)
$configPath = Join-Path -Path $HOME -ChildPath ".config" -AdditionalChildPath "myapp", "settings.json"

# PS 7+ only: ternary, null-coalescing, pipeline chain operators
$status = $IsWindows ? "Windows" : "Non-Windows"
$value = $env:MY_VAR ?? "default-value"
Get-Process notepad && Write-Output "Running"

# For 5.1 compatibility, use traditional constructs
$value = if ($env:MY_VAR) { $env:MY_VAR } else { "default-value" }
```

### Step 2: Handle Errors and Debug Effectively

**Terminating vs Non-Terminating Errors**:

PowerShell has two error categories. Non-terminating errors write to the error stream but continue. Terminating errors halt execution. Understanding this distinction is essential for reliable automation.

```powershell
# Non-terminating: cmdlet writes error, next line still runs
Get-Item -Path "C:\nonexistent"
Write-Output "This still executes"

# Convert non-terminating to terminating with -ErrorAction Stop
try {
    Get-Item -Path "C:\nonexistent" -ErrorAction Stop
} catch {
    Write-Warning "Caught: $($_.Exception.Message)"
}

# Script-wide preference (use cautiously)
$ErrorActionPreference = "Stop"
```

**Structured Error Handling**:

```powershell
function Import-DataFile {
    [CmdletBinding()]
    param([Parameter(Mandatory)] [string]$FilePath)

    $stream = $null
    try {
        if (-not (Test-Path -Path $FilePath)) {
            throw [System.IO.FileNotFoundException]::new("File not found: $FilePath")
        }
        $stream = [System.IO.StreamReader]::new($FilePath)
        $data = $stream.ReadToEnd() | ConvertFrom-Json
        return $data
    }
    catch [System.IO.FileNotFoundException] {
        Write-Error "File does not exist: $($_.Exception.Message)"
    }
    catch {
        Write-Error "Unexpected error: $($_.Exception.GetType().Name) - $($_.Exception.Message)"
        Write-Verbose "Stack trace: $($_.ScriptStackTrace)"
    }
    finally {
        if ($stream) { $stream.Dispose() }
    }
}
```

**Error Records, Write-Error vs throw, and StrictMode**:

```powershell
# Inspect the last error in detail
$record = $Error[0]
$record.Exception.Message       # Human-readable message
$record.FullyQualifiedErrorId   # Unique error identifier
$record.ScriptStackTrace        # PowerShell call stack

# Write-Error: non-terminating (respects -ErrorAction)
Write-Error -Message "Soft failure" -ErrorId "SoftFail" -Category InvalidOperation

# throw: terminating (always stops unless caught)
throw [System.InvalidOperationException]::new("Hard failure")

# Set-StrictMode catches undeclared variables and missing properties
Set-StrictMode -Version Latest

# ErrorView (PS 7+)
$ErrorView = "ConciseView"   # Short single-line errors (default in PS 7)
```

### Step 3: Build PowerShell Modules

**Module Structure**:

```
MyModule/
    MyModule.psd1          # Module manifest
    MyModule.psm1          # Root module (dot-sources functions)
    Public/                # Exported functions
        Get-Widget.ps1
        Set-Widget.ps1
    Private/               # Internal helpers (not exported)
        Invoke-WidgetApi.ps1
    Tests/
        Get-Widget.Tests.ps1
```

```powershell
# MyModule.psm1 - Root module file
$Public  = @(Get-ChildItem -Path "$PSScriptRoot\Public\*.ps1"  -ErrorAction SilentlyContinue)
$Private = @(Get-ChildItem -Path "$PSScriptRoot\Private\*.ps1" -ErrorAction SilentlyContinue)

foreach ($import in @($Public + $Private)) {
    try { . $import.FullName }
    catch { Write-Error "Failed to import $($import.FullName): $_" }
}

Export-ModuleMember -Function $Public.BaseName
```

**Module Manifest and Publishing**:

```powershell
# Generate a manifest
$manifestParams = @{
    Path              = ".\MyModule\MyModule.psd1"
    RootModule        = "MyModule.psm1"
    ModuleVersion     = "1.0.0"
    Author            = "Your Name"
    Description       = "Manages widget resources via the Widget API"
    PowerShellVersion = "5.1"
    FunctionsToExport = @("Get-Widget", "Set-Widget", "Remove-Widget")
    CmdletsToExport   = @()
    VariablesToExport  = @()
    AliasesToExport    = @()
    Tags              = @("Widget", "API", "Automation")
}
New-ModuleManifest @manifestParams

# Run PSScriptAnalyzer
Install-Module -Name PSScriptAnalyzer -Scope CurrentUser -Force
Invoke-ScriptAnalyzer -Path .\MyModule -Recurse -Severity Warning

# Publish to PSGallery
Publish-Module -Path ".\MyModule" -NuGetApiKey $env:PSGALLERY_API_KEY -Repository "PSGallery"
```

### Step 4: Work with the Object Pipeline and Data

**Custom Objects and Pipeline Operators**:

Everything in PowerShell is an object. Use `[PSCustomObject]` for structured data and pipeline operators for filtering, sorting, grouping, and transforming.

```powershell
# Create custom objects
$servers = foreach ($i in 1..5) {
    [PSCustomObject]@{
        Name   = "web-{0:D2}" -f $i
        CPU    = Get-Random -Minimum 10 -Maximum 100
        Status = ("Running", "Stopped", "Degraded") | Get-Random
    }
}

# Filter
$critical = $servers | Where-Object { $_.CPU -gt 80 -and $_.Status -eq "Running" }

# Project with calculated properties
$report = $servers | Select-Object Name, Status, @{
    Name = "CPUPercent"; Expression = { "{0:N1}%" -f $_.CPU }
}

# Group and measure
$servers | Group-Object -Property Status | ForEach-Object { "$($_.Name): $($_.Count)" }
$stats = $servers | Measure-Object -Property CPU -Average -Minimum -Maximum
```

**Data Format Conversion**:

```powershell
# JSON round-trip
$data = @{ Name = "config"; Values = @(1, 2, 3) }
$json = $data | ConvertTo-Json -Depth 10
$restored = $json | ConvertFrom-Json

# CSV import/export
$servers | Export-Csv -Path "servers.csv" -NoTypeInformation -Encoding UTF8
$imported = Import-Csv -Path "servers.csv"

# Hashtable lookup from CSV
$lookup = @{}
Import-Csv -Path "mapping.csv" | ForEach-Object { $lookup[$_.Code] = $_.Description }

# Format for display only (never use Format-* for data processing)
$servers | Format-Table -AutoSize -Property Name, Status, CPU
```

### Step 5: Manage Remote Systems and Parallel Execution

**PSRemoting with Invoke-Command**:

```powershell
# Run on multiple machines in parallel (fan-out)
$servers = "web-01", "web-02", "web-03", "db-01"
$results = Invoke-Command -ComputerName $servers -ScriptBlock {
    [PSCustomObject]@{
        Hostname   = $env:COMPUTERNAME
        DiskFreeGB = [math]::Round((Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'").FreeSpace / 1GB, 2)
    }
} -ThrottleLimit 10

# Pass variables with $using: scope modifier
$serviceName = "W3SVC"
Invoke-Command -ComputerName "server01" -ScriptBlock {
    Restart-Service -Name $using:serviceName -Force
}

# Persistent sessions (avoids repeated authentication)
$sessions = New-PSSession -ComputerName "web-01", "web-02" -Credential (Get-Credential)
Invoke-Command -Session $sessions -ScriptBlock { Get-Process | Measure-Object }
Copy-Item -Path ".\deploy.zip" -Destination "C:\Temp\" -ToSession $sessions[0]
$sessions | Remove-PSSession

# SSH remoting (PowerShell 7+ on any platform)
$session = New-PSSession -HostName "linux-server" -UserName "admin" -KeyFilePath "~/.ssh/id_rsa"
Invoke-Command -Session $session -ScriptBlock { uname -a }
```

**Background Jobs and Parallel Execution**:

```powershell
# ThreadJob (faster than Start-Job, uses threads instead of processes)
$jobs = 1..10 | ForEach-Object {
    Start-ThreadJob -ScriptBlock {
        param($id)
        [PSCustomObject]@{ WorkerId = $id; Result = "Done" }
    } -ArgumentList $_
}
$results = $jobs | Wait-Job | Receive-Job
$jobs | Remove-Job

# ForEach-Object -Parallel (PowerShell 7+ only)
$threshold = 80
$servers | ForEach-Object -Parallel {
    try {
        $ping = Test-Connection -ComputerName $_ -Count 1 -ErrorAction Stop
        [PSCustomObject]@{ Server = $_; Latency = $ping.Latency; Status = "Online" }
    } catch {
        [PSCustomObject]@{ Server = $_; Latency = -1; Status = "Offline" }
    }
} -ThrottleLimit 5
```

### Step 6: Leverage .NET Interop and PowerShell Classes

**Using .NET Types Directly**:

```powershell
# Static methods and constructors
$guid = [System.Guid]::NewGuid()
$base64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("Hello"))
$uri = [System.Uri]::new("https://api.example.com/v2/users")
$stopwatch = [System.Diagnostics.Stopwatch]::StartNew()

# .NET generic collections (faster than arrays for large datasets)
$list = [System.Collections.Generic.List[string]]::new()
$list.Add("item1")
$list.AddRange(@("item2", "item3"))

$dict = [System.Collections.Generic.Dictionary[string, int]]::new()
$dict["key1"] = 100

# StringBuilder for efficient string building in loops
$sb = [System.Text.StringBuilder]::new(1024)
foreach ($line in $lines) { [void]$sb.AppendLine($line) }
$result = $sb.ToString()
```

**Add-Type for Inline C#**:

```powershell
Add-Type -TypeDefinition @"
using System;
using System.Security.Cryptography;
using System.Text;

public static class HashHelper
{
    public static string ComputeSha256(string input)
    {
        using (var sha = SHA256.Create())
        {
            byte[] bytes = sha.ComputeHash(Encoding.UTF8.GetBytes(input));
            return BitConverter.ToString(bytes).Replace("-", "").ToLowerInvariant();
        }
    }
}
"@

$hash = [HashHelper]::ComputeSha256("my-secret-data")
```

**PowerShell Classes and Enums**:

```powershell
enum DeploymentStatus {
    Pending = 0; InProgress = 1; Succeeded = 2; Failed = 3; Cancelled = 4
}

class ServerInventory {
    [string]$Name
    [string]$Environment
    [DeploymentStatus]$Status

    ServerInventory([string]$name, [string]$env) {
        $this.Name = $name
        $this.Environment = $env
        $this.Status = [DeploymentStatus]::Pending
    }

    [bool] IsHealthy() { return $this.Status -eq [DeploymentStatus]::Succeeded }
    [string] GetSummary() { return "$($this.Name) [$($this.Environment)] - $($this.Status)" }

    static [ServerInventory[]] FromCsv([string]$path) {
        return Import-Csv -Path $path | ForEach-Object {
            [ServerInventory]::new($_.Name, $_.Environment)
        }
    }
}

# Inheritance
class WebServer : ServerInventory {
    [int]$Port
    WebServer([string]$name, [int]$port) : base($name, "Production") { $this.Port = $port }
    [string] GetUrl() { return "https://$($this.Name):$($this.Port)" }
}
```

### Step 7: Test with Pester

**Pester 5 Fundamentals**:

Pester is the standard testing framework for PowerShell. Version 5 uses `BeforeAll`, `BeforeEach`, container-scoped discovery, and improved mocking.

```powershell
BeforeAll {
    . "$PSScriptRoot\..\Public\Get-Widget.ps1"
}

Describe "Get-Widget" {
    Context "when the widget exists" {
        It "returns a widget by ID" {
            Mock Invoke-WidgetApi { [PSCustomObject]@{ Id = 1; Name = "TestWidget" } }
            $result = Get-Widget -Id 1
            $result | Should -Not -BeNullOrEmpty
            $result.Name | Should -Be "TestWidget"
        }
    }

    Context "when the widget does not exist" {
        It "returns null and writes a warning" {
            Mock Invoke-WidgetApi { return $null }
            Mock Write-Warning {}
            $result = Get-Widget -Id 999
            $result | Should -BeNullOrEmpty
            Should -Invoke Write-Warning -Times 1 -Exactly
        }
    }
}
```

**Should Assertions**:

```powershell
Describe "Should assertion examples" {
    It "equality"    { 42 | Should -Be 42; "Hello" | Should -BeExactly "Hello" }
    It "patterns"    { "hello" | Should -BeLike "hel*"; "hello world" | Should -Match "hello\s\w+" }
    It "collections" { @(1,2,3) | Should -Contain 2; @(1,2,3) | Should -HaveCount 3 }
    It "types"       { 42 | Should -BeOfType [int]; Get-Date | Should -BeOfType [datetime] }
    It "comparisons" { 10 | Should -BeGreaterThan 5; $true | Should -BeTrue }
    It "exceptions"  { { throw "boom" } | Should -Throw -ExpectedMessage "boom" }
}
```

**Mocking and TestDrive**:

```powershell
Describe "Service deployment" {
    BeforeAll { . "$PSScriptRoot\..\Public\Deploy-Service.ps1" }

    Context "successful deployment" {
        BeforeEach {
            Mock Test-Connection { $true }
            Mock Copy-Item {}
            Mock Invoke-Command { [PSCustomObject]@{ Status = "Running" } }
        }

        It "copies files to the target server" {
            Deploy-Service -Name "MyApp" -Server "web-01" -SourcePath "C:\Build"
            Should -Invoke Copy-Item -Times 1 -Exactly -ParameterFilter {
                $Destination -like "*web-01*"
            }
        }
    }

    Context "file operations with TestDrive" {
        It "creates and reads a config file" {
            $path = Join-Path $TestDrive "config.json"
            @{ Server = "web-01"; Port = 8080 } | ConvertTo-Json | Set-Content -Path $path
            $path | Should -Exist
            (Get-Content $path | ConvertFrom-Json).Port | Should -Be 8080
        }
    }
}
```

**Code Coverage and CI Integration**:

```powershell
$config = New-PesterConfiguration
$config.Run.Path = ".\Tests"
$config.Run.PassThru = $true
$config.CodeCoverage.Enabled = $true
$config.CodeCoverage.Path = @(".\Public\*.ps1", ".\Private\*.ps1")
$config.CodeCoverage.CoveragePercentTarget = 80
$config.TestResult.Enabled = $true
$config.TestResult.OutputFormat = "NUnitXml"
$config.TestResult.OutputPath = ".\TestResults.xml"

$result = Invoke-Pester -Configuration $config

if ($result.FailedCount -gt 0) { throw "$($result.FailedCount) tests failed" }
if ($result.CodeCoverage.CoveragePercent -lt 80) {
    throw "Coverage $($result.CodeCoverage.CoveragePercent)% below 80% threshold"
}
```

## Best Practices

- **Use CmdletBinding on every function** intended for production; it adds `-Verbose`, `-Debug`, and `-ErrorAction` support for free
- **Prefer splatting** over long parameter lines; it makes conditional parameter construction trivial
- **Never suppress errors silently**; use `-ErrorAction SilentlyContinue` only when you explicitly handle the absence of a result
- **Emit objects, not formatted text**; let the caller decide how to display or process output
- **Validate parameters at the boundary** with `[Validate*]` attributes rather than manual checks inside the function body
- **Run PSScriptAnalyzer** on every commit; treat warnings as errors in CI
- **Use Pester for all testable logic**; target 80% code coverage
- **Avoid aliases in scripts** (`gci`, `%`, `?`, `sls`); always use full cmdlet names for clarity and portability

## Common Patterns

### Pattern 1: Retry with Exponential Backoff

```powershell
function Invoke-WithRetry {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)] [scriptblock]$ScriptBlock,
        [int]$MaxRetries = 3,
        [int]$BaseDelaySeconds = 2
    )

    for ($attempt = 1; $attempt -le $MaxRetries; $attempt++) {
        try { return & $ScriptBlock }
        catch {
            if ($attempt -eq $MaxRetries) { throw }
            $delay = [math]::Pow($BaseDelaySeconds, $attempt)
            Write-Warning "Attempt $attempt failed. Retrying in ${delay}s..."
            Start-Sleep -Seconds $delay
        }
    }
}

$response = Invoke-WithRetry -ScriptBlock {
    Invoke-RestMethod -Uri "https://api.example.com/data" -TimeoutSec 10
}
```

### Pattern 2: Configuration Management

```powershell
function Get-AppConfig {
    [CmdletBinding()]
    param(
        [string]$ConfigPath = (Join-Path $PSScriptRoot "config.json"),
        [string]$Environment = ($env:APP_ENVIRONMENT ?? "Development")
    )

    if (-not (Test-Path $ConfigPath)) { throw "Config not found: $ConfigPath" }
    $config = Get-Content -Path $ConfigPath -Raw | ConvertFrom-Json
    $env = $config.$Environment
    if (-not $env) { throw "No config section for: $Environment" }

    [PSCustomObject]@{
        DatabaseServer = $env.DatabaseServer ?? $config.Defaults.DatabaseServer
        LogLevel       = $env.LogLevel ?? "Information"
        MaxRetries     = $env.MaxRetries ?? 3
        Environment    = $Environment
    }
}
```

## Quality Checklist

- [ ] All functions use `[CmdletBinding()]`
- [ ] Parameters have appropriate `[Validate*]` attributes
- [ ] Destructive functions implement `SupportsShouldProcess`
- [ ] Errors are handled explicitly (no silent failures)
- [ ] Output is objects, not formatted strings
- [ ] PSScriptAnalyzer produces zero warnings
- [ ] Pester tests cover all public functions
- [ ] Code coverage meets 80% threshold
- [ ] No aliases used in script files
- [ ] Script works on both PS 5.1 and PS 7+ (or documents the requirement)

## Related Skills

- `cicd-architect` - PowerShell in CI/CD pipelines
- `code-quality` - PowerShell code standards and PSScriptAnalyzer
- `csharp-expert` - Deep .NET integration from PowerShell
- `kubernetes-expert` - PowerShell for AKS and container management

---

**Version**: 1.0.0
**Last Updated**: March 2026
**Based on**: PowerShell best practices, Pester 5 documentation, PSScriptAnalyzer rules


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
