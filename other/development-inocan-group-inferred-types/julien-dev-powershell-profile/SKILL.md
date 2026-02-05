---
name: julien-dev-powershell-profile
description: "Manage PowerShell profile, aliases, functions. Triggers: add alias, update profile, modify claude command, Microsoft.PowerShell_profile.ps1"
triggers:
  - powershell profile
  - add alias
  - update profile
  - modify claude command
  - powershell alias
  - ps1 profile
---

# PowerShell Profile Manager

**Profile**: `C:\Users\julien\OneDrive\Documents\PowerShell\Microsoft.PowerShell_profile.ps1`

## Workflow

1. Read profile to identify correct section (11 numbered sections)
2. Edit profile (or use Python if OneDrive sync fails)
3. User runs `rup` to reload

## Reference Files

| Need | File |
|------|------|
| Section details | [references/profile-structure.md](references/profile-structure.md) |
| Code patterns | [references/code-patterns.md](references/code-patterns.md) |
| OneDrive issues | [references/troubleshooting.md](references/troubleshooting.md) |

## Skill Chaining

### Skills Required Before
- None (entry point skill)

### Input Expected
- User request to modify profile/alias/function
- Clear description of desired behavior

### Output Produced
- **Format**: Modified `Microsoft.PowerShell_profile.ps1`
- **Side effects**: Changes apply after `rup` or new terminal

### Compatible Skills After
- None typically (standalone modifications)

### Tools Used
- `Read` (read current profile state)
- `Edit` (modify profile sections)
- `Bash` with Python (workaround for OneDrive sync)

### Visual Workflow

```
User: "Add/modify PowerShell alias"
    ↓
[THIS SKILL]
    ├─► Read profile + refs as needed
    ├─► Identify correct section
    ├─► Edit (or Python workaround)
    └─► Verify modification
    ↓
User runs `rup` or opens new terminal
```
