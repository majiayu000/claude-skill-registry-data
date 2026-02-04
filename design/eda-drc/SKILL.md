---
name: eda-drc
description: Design validation and review. Run DRC/ERC checks, verify against constraints, check component availability, and prepare comprehensive validation reports.
allowed-tools: Read, Write, Glob, WebSearch, mcp__kicad-pcb__run_drc, mcp__kicad-pcb__get_drc_violations, mcp__kicad-pcb__get_design_rules, mcp__kicad-pcb__get_board_info, mcp__kicad-pcb__get_board_2d_view, mcp__jlc__*
---

# EDA DRC Skill

Design validation, rule checking, and pre-manufacturing review.

## Auto-Activation Triggers

This skill activates when:
- User asks to "check design", "validate", "run DRC"
- User asks about design errors or warnings
- User mentions manufacturing readiness
- Project is approaching completion
- User asks "is this ready for fabrication?"

## Context Requirements

**Requires:**
- `hardware/*.kicad_sch` - Schematic files
- `hardware/*.kicad_pcb` - PCB layout
- `docs/design-constraints.json` - Project constraints
- `docs/component-selections.md` - Selected components

**Produces:**
- `docs/validation-report.md` - Comprehensive validation report

## Validation Scopes

### `/eda-check schematic`
- Run ERC (Electrical Rules Check)
- Verify power connections
- Check decoupling capacitors
- Validate against datasheet requirements
- Check component values

### `/eda-check pcb`
- Run DRC (Design Rules Check)
- Verify placement guidelines
- Check routing rules
- Validate copper pours
- Review silkscreen

### `/eda-check components`
- Verify stock availability on LCSC
- Check current pricing
- Identify lifecycle issues
- Suggest alternatives if needed

### `/eda-check manufacturing`
- Generate and review Gerbers
- Verify BOM completeness
- Check position file accuracy
- Validate against manufacturer specs

### `/eda-check full`
- Run all above checks
- Comprehensive pre-manufacturing validation

## Workflow

### 1. Load Context
```
@docs/design-constraints.json
@docs/component-selections.md
@docs/schematic-status.md
@docs/pcb-status.md
```

### 2. Run Automated Checks
- Execute DRC/ERC via KiCad MCP
- Capture all violations and warnings

### 3. Manual Review Checklist
Use reference documents to verify:
- Common issues are addressed
- Manufacturer constraints are met
- Design guidelines followed

### 4. Component Verification
For each selected component:
- Check LCSC stock status
- Verify pricing
- Check for lifecycle warnings

### 5. Generate Report
Create comprehensive validation report documenting:
- Pass/fail status for each check
- List of issues found
- Recommended actions
- Sign-off status

## Output Format

### validation-report.md

```markdown
# Validation Report

Project: [name]
Generated: [timestamp]
Scope: [schematic|pcb|components|manufacturing|full]

## Summary

| Check | Status | Issues |
|-------|--------|--------|
| ERC | PASS/FAIL | X errors, Y warnings |
| DRC | PASS/FAIL | X errors, Y warnings |
| Components | PASS/FAIL | X issues |
| Manufacturing | PASS/FAIL | X issues |
| **Overall** | **PASS/FAIL** | |

## Critical Issues
Items that MUST be fixed before manufacturing:
1. [Issue description] - [Location] - [Fix]
2. ...

## Warnings
Items that SHOULD be reviewed:
1. [Warning description] - [Location] - [Recommendation]
2. ...

## Notes
Items for information only:
1. [Note]
2. ...

---

## Detailed Results

### Schematic (ERC)

**Status:** PASS/FAIL

**Errors:**
- [ ] [Error type]: [Details]

**Warnings:**
- [ ] [Warning type]: [Details]

**Checks Passed:**
- [x] All power pins connected
- [x] All ICs have decoupling
- [x] No unconnected pins (except intentional NC)
- [x] Net names consistent

### PCB (DRC)

**Status:** PASS/FAIL

**Errors:**
- [ ] [Error type]: [Details]

**Warnings:**
- [ ] [Warning type]: [Details]

**Checks Passed:**
- [x] Trace width meets minimum
- [x] Clearances meet minimum
- [x] Via drill meets minimum
- [x] Silkscreen not on pads

### Components

| Component | LCSC | Stock | Price | Status |
|-----------|------|-------|-------|--------|
| [name] | C#### | #### | $X.XX | OK/LOW/OOS |

**Issues:**
- [Component]: [Issue]

### Manufacturing

**Target:** [JLCPCB/PCBWay/etc.]

**Checks:**
- [ ] Board size within limits
- [ ] Layer count supported
- [ ] Minimum features met
- [ ] BOM complete
- [ ] Position file accurate

---

## Action Items

### Before Manufacturing
1. [ ] [Action required]
2. [ ] [Action required]

### Recommendations
1. [ ] [Optional improvement]

---

## Sign-off

- [ ] Schematic review complete
- [ ] PCB review complete
- [ ] Components verified
- [ ] Ready for manufacturing

Reviewed by: [name/date]
```

## Guidelines

- Run DRC frequently during layout, not just at the end
- Address all errors before manufacturing
- Document intentional rule violations
- Verify component availability before finalizing design
- Keep validation report updated as issues are fixed

## Reference Documents

- `reference/COMMON-ISSUES.md` - Frequent problems and solutions
- `reference/MANUFACTURER-SPECS.md` - Manufacturer capabilities
- `reference/VALIDATION-CHECKLIST.md` - Pre-manufacturing checklist

## Next Steps

After validation passes:
1. Run `/eda-export [format]` to generate manufacturing files
2. Update `design-constraints.json` stage to "complete"
