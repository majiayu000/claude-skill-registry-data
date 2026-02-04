---
name: script-banner
description: Automatically add standardized info banners to all new scripts and tools. Use when creating new PowerShell scripts, Bash scripts, or any executable tools in this repository.
allowed-tools: Read, Write, Edit
---

# Script Banner Generator Skill

This Skill ensures that **every new script or tool** created in this repository includes a standardized information banner that displays script metadata and requires user confirmation before execution.

## Purpose

All scripts and tools in the tech-support-tools repository must include:
1. An ASCII-formatted banner displaying script information
2. User interaction requiring Enter key press to proceed
3. Consistent branding with author information

## When to Use This Skill

**ALWAYS use this Skill when:**
- Creating a new PowerShell script (`.ps1` file)
- Creating a new Bash script (`.sh` file)
- Creating any new executable tool or utility
- The user requests a new script or tool

**DO NOT use this Skill when:**
- Editing existing scripts (unless adding banner is specifically requested)
- Creating configuration files, documentation, or non-executable files

## Required Banner Information

Every script banner must include:
- **Tool Name**: Descriptive name of the script/tool
- **About**: Brief description of what the script does
- **Author**: Mchael Poncardas
- **Email**: m@poncardas.com
- **Version**: Starting version number (default: 1.0 for new scripts)
- **Last Updated**: Current date in YYYY-MM-DD format
- **Requires**: Platform/version requirements (e.g., "PowerShell 5.1 or later", "Bash 4.0+")

## Implementation Instructions

### For PowerShell Scripts

1. **Console Banner** (before script execution):
   - Use the PowerShell template from `templates/powershell-banner.ps1`
   - Place the banner code AFTER parameter declarations but BEFORE main script logic
   - Include within an `if (-not $NoLogFile)` or similar conditional for scripts with non-interactive modes
   - Always include `Read-Host -Prompt "Press 'Enter' key to run [Script Name]"`

2. **Log File Banner** (if script generates logs):
   - Use the same banner format with `Write-Log` function
   - Place at the beginning of log file output

3. **Banner Width**:
   - Total width: 79 characters (including border characters)
   - Border characters: `+` for corners/lines, `|` for sides
   - Content area: 77 characters (between the `|` characters)

### For Bash Scripts

1. **Console Banner**:
   - Use the Bash template from `templates/bash-banner.sh`
   - Place near the beginning of the script, after shebang and initial setup
   - Always include `read -p "Press Enter to continue..." </dev/tty`

2. **Banner Width**:
   - Same as PowerShell: 79 characters total

### Banner Template Structure

```
+-----------------------------------------------------------------------------+
|                             [SCRIPT NAME HERE]                              |
+-----------------------------------------------------------------------------+
| About        : [Brief description of what the script does - can wrap]      |
| Author       : Mchael Poncardas                                             |
| Email        : m@poncardas.com                                              |
| Version      : [X.Y]                                                        |
| Last Updated : [YYYY-MM-DD]                                                 |
| Requires     : [Platform/version requirements]                             |
+-----------------------------------------------------------------------------+
```

**Formatting Rules:**
- Script name should be CENTERED and UPPERCASE
- Field labels are left-aligned with consistent spacing
- Use `: ` (colon-space) separator after field labels
- Maintain consistent column alignment for readability
- Pad with spaces to keep border alignment

### Version Numbering

- **New scripts**: Start at `1.0`
- **Bug fixes**: Increment patch (1.0 → 1.1)
- **New features**: Increment minor (1.0 → 2.0)
- **Breaking changes**: Increment major if needed

### Date Format

- Always use ISO format: `YYYY-MM-DD`
- Example: `2025-12-26`

## Checklist for New Scripts

Before completing a new script, verify:
- ✅ Banner is present in console output
- ✅ Banner is present in log file output (if applicable)
- ✅ Banner displays script name (centered, uppercase)
- ✅ Banner displays brief description
- ✅ Banner shows author: "Mchael Poncardas"
- ✅ Banner shows email: "m@poncardas.com"
- ✅ Banner shows version number
- ✅ Banner shows last updated date (today's date)
- ✅ Banner shows platform requirements
- ✅ User must press Enter to proceed
- ✅ Banner width is exactly 79 characters
- ✅ All text is properly aligned

## Examples

### Example 1: PowerShell Diagnostic Script

```powershell
# After parameters, before main logic:
if (-not $NoLogFile) {
    Write-Host ""
    Write-Host "+-----------------------------------------------------------------------------+"
    Write-Host "|                          NETWORK DIAGNOSTICS TOOL                           |"
    Write-Host "+-----------------------------------------------------------------------------+"
    Write-Host "| About        : Performs comprehensive network connectivity tests and        |"
    Write-Host "|                generates a detailed diagnostic report.                      |"
    Write-Host "| Author       : Mchael Poncardas                                             |"
    Write-Host "| Email        : m@poncardas.com                                              |"
    Write-Host "| Version      : 1.0                                                          |"
    Write-Host "| Last Updated : 2025-12-26                                                   |"
    Write-Host "| Requires     : PowerShell 5.1 or later                                      |"
    Write-Host "+-----------------------------------------------------------------------------+"
    Write-Host ""
    Read-Host -Prompt "Press 'Enter' key to run Network Diagnostics"
}
```

### Example 2: Bash Backup Script

```bash
#!/bin/bash

# Display banner
echo ""
echo "+-----------------------------------------------------------------------------+"
echo "|                            BACKUP AUTOMATION TOOL                           |"
echo "+-----------------------------------------------------------------------------+"
echo "| About        : Automates incremental backups using rsync with retention     |"
echo "|                policies and detailed logging.                               |"
echo "| Author       : Mchael Poncardas                                             |"
echo "| Email        : m@poncardas.com                                              |"
echo "| Version      : 1.0                                                          |"
echo "| Last Updated : 2025-12-26                                                   |"
echo "| Requires     : Bash 4.0 or later, rsync                                     |"
echo "+-----------------------------------------------------------------------------+"
echo ""
read -p "Press Enter to start backup process..."
```

## Integration with Comment-Based Help

For PowerShell scripts, the banner information should **match** the `.NOTES` section in comment-based help:

```powershell
.NOTES
    Author: Mchael Poncardas (m@poncardas.com)
    Version: 1.0
    Last Updated: 2025-12-26
    Requires: PowerShell 5.1 or later
```

Keep both synchronized when updating versions or dates.

## Reference Files

- `templates/powershell-banner.ps1` - Complete PowerShell banner code template
- `templates/bash-banner.sh` - Complete Bash banner code template

## Notes

- The banner is part of the user experience and branding consistency
- Banners should display BEFORE any actual script operations begin
- For scripts with `-WhatIf` or dry-run modes, still show the banner
- For truly silent/automated scripts (e.g., scheduled tasks), consider making the banner conditional with a `-Silent` parameter

## Workflow

When the user requests a new script:
1. Gather script requirements (name, purpose, platform)
2. **Immediately** include the banner code in your implementation
3. Populate banner fields with:
   - Script name (from requirements)
   - Description (from requirements)
   - Version: 1.0 (for new scripts)
   - Last Updated: Today's date
   - Requires: Appropriate platform/version
4. Ensure Enter key prompt is included
5. Test banner width (should be exactly 79 characters)

**IMPORTANT**: Do not ask the user if they want a banner - it's mandatory for all new scripts in this repository.
