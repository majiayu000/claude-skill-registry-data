---
name: health
description: Run the HUMMBL governance kernel health CLI and report its observed state.
version: 0.1.2
execution-mode: advisory
category: governance-compliance
status: candidate
---
## Context Gathering

Before executing this skill, gather the following context:
- **Target repository/environment**: Confirm where `hummbl_governance` resolves.
- **Health status**: Run the platform command below from the target repository
  or an environment where the package is installed.

# Health Command

## When to Use
- Start of ops session
- After deploying a change to services
- When something feels broken but you are not sure what
- Before reporting status to stakeholders
- Debugging connectivity issues
Run the implemented kernel health CLI and display its observed state.

## Usage

```bash
[health]               # Run all health probes
```

## Execution

### 1. Run health check

**Unix (bash/zsh):**

```bash
python3 -m hummbl_governance.kernel health
```

**Windows (PowerShell):**

```powershell
py -m hummbl_governance.kernel health
```

Use this implemented entry point. If the kernel module cannot be imported,
report the exact error and mark the health prerequisite incomplete.

### 2. Parse results

The kernel health command returns JSON including:
- `status`: kernel lifecycle state, such as `NOT_BOOTED`
- `healthy`: boolean aggregate
- kernel inventory such as `receipts_total`, `laws`, `identities`, and
  `schedules`

### 3. Format output

## Output Format

```
Health Check | <YYYY-MM-DD HH:MMZ>
═══════════════════════════════════

Overall: 🟢 HEALTHY / 🔴 UNHEALTHY
Kernel state: <status>

| Field | Observed value |
|-------|----------------|
| receipts_total | ... |
| laws | ... |
| identities | ... |
| schedules | ... |

<if unhealthy>
## Issues
<report the kernel state and exact command result>
## Recommended Actions
<specific remediation steps>
</if>
```

## Constraints

- This is READ-ONLY. Do not fix issues, only report them.
- Do not fabricate health results -- always run the actual command.
- A successful command execution is `PASS` evidence that the health workflow
  ran; the reported system may still be unhealthy. Preserve both facts.
- If the health module fails to import, report the error and do not emit `PASS`
  evidence for the prerequisite.
