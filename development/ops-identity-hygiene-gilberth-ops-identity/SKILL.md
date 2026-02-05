---
name: ops-identity-hygiene
description: Active Directory operational hygiene analyzer for OpsIdentity project. Detects administrative disorder, architectural debt, and suboptimal configurations—not offensive security. Use when (1) improving OpsIdentity PowerShell collection functions, (2) adding AI analysis prompts to server.js, (3) analyzing coverage gaps against 87 industry metrics, (4) implementing smart filtering or anti-hallucination rules. Triggers on AD health, GPO analysis, replication, trusts, token size, FSMO, site topology, DNS/DHCP hygiene, or requests to analyze existing OpsIdentity code.
---

# OpsIdentity Operational Hygiene Skill

Improve OpsIdentity code to detect **administrative disorder, architectural debt, and configuration drift** in Active Directory environments.

> "Not looking for Russian hackers. Looking for administrative chaos, poor architecture, and suboptimal configurations."

## When to Use This Skill

| Trigger | Action |
|---------|--------|
| "Analyze OpsIdentity code coverage" | Load [🔍 Analyzer Prompt](./references/analyzer-prompt.md) |
| "Add new AD metric" | Check [📊 Coverage Matrix](./references/coverage-matrix.md) first |
| "Create PowerShell function" | Follow patterns in [⚙️ PowerShell Functions](./references/powershell-functions.md) |
| "Add AI analysis prompt" | Use templates from [📝 Prompt Templates](./references/prompt-templates.md) |

## Mission

This skill focuses on **operational hygiene**, not penetration testing:

| Focus Area | What We Detect | Impact |
|------------|----------------|--------|
| Architecture | 40+ trusts without justification | Unnecessary complexity |
| Permissions | 100 accounts with Global Admin | Audit difficulty |
| GPO | Monolithic GPO with 200+ settings | Slow logon, impossible debugging |
| Infrastructure | 8-hour replication latency | Data inconsistency |
| Configuration | AD Recycle Bin disabled | No object recovery |
| Topology | 15 subnets not assigned to sites | Clients authenticate to remote DC |

## Stack Overview

- **Frontend**: React + TypeScript + Vite + TailwindCSS + shadcn/ui
- **Backend**: Node.js + Express + PostgreSQL
- **Collection**: PowerShell embedded in `client/src/pages/NewAssessment.tsx`
- **AI**: Anthropic Claude (Opus 4.5 for complex, Sonnet 4.5 for standard)
- **Anti-Hallucination**: Smart Filtering + Grounding Validation + Deterministic Rules

## Key Files

| File | Purpose |
|------|---------|
| `client/src/pages/NewAssessment.tsx` | PowerShell script (35+ Get-* functions) |
| `server/server.js` | AI prompts, Smart Filtering, Validation |
| `server/analyzers/userRules.js` | Deterministic rules (Users category) |

---

## Workflow

### Phase 1: Identify Coverage Gap

Check current coverage (37% of 87 metrics). Reference [📊 Coverage Matrix](./references/coverage-matrix.md) for:
- Missing metrics by category
- Priority level (Critical/High/Medium)
- Implementation complexity

### Phase 2: Implement PowerShell Function

Add collection function in `NewAssessment.tsx`. **All functions must follow anti-null pattern:**

```powershell
function Get-NewMetric {
    $results = @()  # Always initialize as empty array
    
    try {
        $items = @(Get-ADObject -Filter * -ErrorAction Stop)  # Force array
        
        foreach ($item in $items) {
            try {
                $obj = @{
                    Name = $item.Name
                    IsProblematic = $false
                    # Add detection logic
                }
                $results += $obj
            } catch {
                Write-Host "[!] Error processing $($item.Name): $_" -ForegroundColor Yellow
            }
        }
        
        return @($results)  # Always return array
    } catch {
        Write-Host "[!] CRITICAL: $_" -ForegroundColor Red
        return @()  # Never return null
    }
}
```

### Phase 3: Add Smart Filtering

Update `filterCategoryData()` in `server.js` to pre-filter problematic objects:

```javascript
case 'NewCategory':
  return data.filter(item => 
    item.IsProblematic === true ||
    item.RiskLevel === 'HIGH' ||
    item.SpecificCondition > threshold
  );
```

### Phase 4: Create AI Prompt

Add category instructions in `server.js`. See [📝 Prompt Templates](./references/prompt-templates.md).

### Phase 5: Add Validation Rules

Update `ATTRIBUTE_VALIDATION_RULES` to prevent hallucinations:

```javascript
'NEW_FINDING_TYPE': {
  category: 'NewCategory',
  identifierField: 'Name',
  validate: (obj) => obj.Condition === expectedValue
}
```

### Phase 6: Increment Version

Update version in `App.tsx` after changes.

---

## Critical Patterns

### Anti-Null Guarantees

```powershell
# ✅ CORRECT
$list = @()                              # Initialize empty
$items = @(Get-ADObject -Filter *)       # Force array context
return @($list)                          # Always return array

# ❌ WRONG
$list = $null                            # Never initialize as null
return $items                            # May return null if empty
```

### Finding Output Format

```javascript
{
  type_id: 'UPPERCASE_WITH_UNDERSCORES',
  title: '[Count] + specific problem',
  description: 'Current state + operational impact + compliance',
  recommendation: 'Copy-paste ready commands',
  affected_objects: ['REAL objects from JSON data']
}
```

---

## What NOT to Do

- ❌ Focus on offensive security (Golden Ticket, lateral movement)
- ❌ Code without robust error handling
- ❌ Prompts that generate findings without real data
- ❌ Ignore anti-hallucination system
- ❌ Functions returning null instead of `@()`
- ❌ Unnecessary complexity

## Valid Improvements

- ✅ Detect GPOs with 50+ settings (monolithic)
- ✅ Identify subnets not associated to any AD site
- ✅ Calculate replication latency between all DCs
- ✅ Find empty groups or groups without defined manager
- ✅ Detect users with estimated token size > 12KB
- ✅ Identify trusts with password > 90 days without rotation

---

## Reference Files

Load these as needed during development:

- [🔍 Analyzer Prompt](./references/analyzer-prompt.md) - Full analysis prompt with 87 metrics baseline, output format, web search rules
- [📊 Coverage Matrix](./references/coverage-matrix.md) - Current coverage status, gaps by category, sprint priorities
- [📝 Prompt Templates](./references/prompt-templates.md) - AI prompt structure for new categories with examples
- [⚙️ PowerShell Functions](./references/powershell-functions.md) - Ready-to-use function implementations

---

## Quick Reference: 87 Industry Metrics

| Category | Total | Key Checks |
|----------|-------|------------|
| Users | 12 | PwdNeverExpires, Kerberoastable, Delegation, AdminSDHolder |
| Computers | 10 | Obsolete OS, LAPS, Delegation, Password Age |
| Groups | 10 | Tier0 size, Nesting depth, Empty, Token bloat |
| GPOs | 12 | Unlinked, Monolithic, Version mismatch, cpassword |
| DCs | 14 | FSMO, KRBTGT age, SMBv1, LDAP signing, Spooler |
| Replication | 8 | Latency, Lingering objects, USN rollback |
| DNS | 8 | Scavenging, Stale records, Zone security |
| DHCP | 6 | Rogue servers, Exhaustion, Options 6/15 |
| Sites | 7 | Orphaned subnets, Missing links, UGMC |

**Current coverage: 37% → Target: 80%+**
